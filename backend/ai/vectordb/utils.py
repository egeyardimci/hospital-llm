import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain.docstore.document import Document
from backend.common.paths import SUT_JSON_PATH, construct_db_path
from backend.common.constants import LABSE
from backend.utils.logger import get_logger
logger = get_logger()

load_dotenv()

"""
This file contains the functions to create and load ChromaDB instances for the tests.
"""

def load_sut_json_documents():
    """
    Load the structured SUT JSON file and convert it to LangChain Documents with rich metadata.
    Each paragraph/item becomes a document with metadata including section_id, title, parent_path, etc.
    """
    with open(SUT_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    documents = []

    def process_section(section, parent_path="", parent_titles=""):
        """Recursively process sections, subsections, paragraphs, and items."""
        section_id = section.get("id", "")
        section_title = section.get("title", "")

        current_path = f"{parent_path} > {section_id}" if parent_path else section_id
        current_titles = f"{parent_titles} > {section_title}" if parent_titles else section_title
        amendments = section.get("amendments", [])
        amendments_str = " | ".join(amendments) if amendments else ""

        # Process paragraphs
        for paragraph in section.get("paragraphs", []):
            paragraph_id = paragraph.get("id", "")
            content = paragraph.get("content", "")

            if content:
                metadata = {
                    "section_id": section_id,
                    "section_title": section_title,
                    "parent_path": current_path,
                    "parent_titles": current_titles,
                    "paragraph_id": paragraph_id,
                    "content_type": "paragraph",
                    "amendments": amendments_str
                }
                documents.append(Document(page_content=content, metadata=metadata))

            # Process items within paragraphs
            for item in paragraph.get("items", []):
                process_item(item, current_path, current_titles, section_id, section_title, amendments_str)

        # Process direct items (not within paragraphs)
        for item in section.get("items", []):
            if isinstance(item, str):
                metadata = {
                    "section_id": section_id,
                    "section_title": section_title,
                    "parent_path": current_path,
                    "parent_titles": current_titles,
                    "content_type": "item",
                    "amendments": amendments_str
                }
                documents.append(Document(page_content=item, metadata=metadata))
            else:
                process_item(item, current_path, current_titles, section_id, section_title, amendments_str)

        # Process subsections recursively
        for subsection in section.get("subsections", []):
            process_section(subsection, current_path, current_titles)

    def process_item(item, parent_path, parent_titles, section_id, section_title, amendments_str):
        """Process an item which can be a string or an object with id, content, and sub_items."""
        if isinstance(item, str):
            metadata = {
                "section_id": section_id,
                "section_title": section_title,
                "parent_path": parent_path,
                "parent_titles": parent_titles,
                "content_type": "item",
                "amendments": amendments_str
            }
            documents.append(Document(page_content=item, metadata=metadata))
        elif isinstance(item, dict):
            item_id = item.get("id", "")
            content = item.get("content", "")

            if content:
                metadata = {
                    "section_id": section_id,
                    "section_title": section_title,
                    "parent_path": parent_path,
                    "parent_titles": parent_titles,
                    "item_id": item_id,
                    "content_type": "item",
                    "amendments": amendments_str
                }
                documents.append(Document(page_content=content, metadata=metadata))

            # Process sub_items recursively
            for sub_item in item.get("sub_items", []):
                if isinstance(sub_item, str):
                    sub_metadata = {
                        "section_id": section_id,
                        "section_title": section_title,
                        "parent_path": parent_path,
                        "parent_titles": parent_titles,
                        "item_id": item_id,
                        "content_type": "sub_item",
                        "amendments": amendments_str
                    }
                    documents.append(Document(page_content=sub_item, metadata=sub_metadata))
                elif isinstance(sub_item, dict):
                    sub_item_id = sub_item.get("id", "")
                    sub_content = sub_item.get("content", "")
                    if sub_content:
                        sub_metadata = {
                            "section_id": section_id,
                            "section_title": section_title,
                            "parent_path": parent_path,
                            "parent_titles": parent_titles,
                            "item_id": item_id,
                            "sub_item_id": sub_item_id,
                            "content_type": "sub_item",
                            "amendments": amendments_str
                        }
                        documents.append(Document(page_content=sub_content, metadata=sub_metadata))

    # Process all top-level sections
    for section in data.get("sections", []):
        process_section(section)

    logger.info(f"Loaded {len(documents)} documents from SUT JSON file")
    return documents


def create_vectordb(embedding_model_name, chunk_size, chunk_overlap):
    try:
        embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
        db_path = construct_db_path(embedding_model_name, chunk_size, chunk_overlap)
        if os.path.exists(db_path):
            logger.warning("ChromaDB already exists.")
            return
        else:
            logger.info(f"Started creating ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}")

            # Load structured JSON document with rich metadata
            docs = load_sut_json_documents()

            # Split the documents into smaller chunks while retaining the metadata
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            chunks = text_splitter.split_documents(docs)

            logger.info(f"Split {len(docs)} documents into {len(chunks)} chunks")

            # Create the ChromaDB instance and store the embeddings
            Chroma.from_documents(chunks, embedding_model, persist_directory=str(db_path), collection_name="sgk")
            logger.info(f"Created and saved ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}")
    except Exception as e:
        logger.error(f"Error creating ChromaDB: {e}")

def load_vectordb(embedding_model_name,chunk_size,chunk_overlap):
    try:
        db_path = construct_db_path(embedding_model_name, chunk_size, chunk_overlap)
        logger.info(f"Trying to load ChromaDB instance from {db_path}")
        embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)

        if os.path.exists(db_path):
            vector_db = Chroma(persist_directory=str(db_path), embedding_function=embedding_model, collection_name="sgk")
            logger.info(f"Loaded existing ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}")
            return vector_db
        else:
            logger.error(f"ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap} does not exist. Please create it first.")
    except Exception as e:
        logger.error(f"Error loading ChromaDB: {e}")

def create_multiple_vectordbs(embedding_models,chunk_sizes_and_chunk_overlaps):
    for embedding_model_name in embedding_models:
        for chunk_size, chunk_overlap in chunk_sizes_and_chunk_overlaps:
            create_vectordb(embedding_model_name,chunk_size,chunk_overlap)

if __name__ == "__main__":
    embedding_model_names = [LABSE]
    chunk_sizes_and_chunk_overlaps = [(500,50),(1000,100),(2000,200)]
    
    #create_multiple_vectordb(embedding_model_names,chunk_sizes_and_chunk_overlaps)
    create_vectordb(embedding_model_names[0],500,50)