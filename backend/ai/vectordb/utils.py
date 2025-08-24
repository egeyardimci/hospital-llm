import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain.docstore.document import Document
from backend.utils.logger import log
from backend.common.paths import SGK_DOCUMENT_PATH, construct_db_path
from backend.common.constants import LABSE

load_dotenv()

"""
This file contains the functions to create and load ChromaDB instances for the tests.
"""

def create_vectordb(embedding_model_name, chunk_size, chunk_overlap):
    embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
    db_path = construct_db_path(embedding_model_name, chunk_size, chunk_overlap)
    if os.path.exists(db_path):
        log("ChromaDB already exists.")
        return
    else:
        log(f"Started creating ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}")
        
        # Load PDF document using a PDF loader (e.g., PyPDFLoader)
        # Ensure that 'document_name' points to your PDF file
        loader = PyPDFLoader(SGK_DOCUMENT_PATH)
        docs = loader.load()
        
        # Ensure each page/document has page number metadata.
        # Many PDF loaders return one Document per page.
        updated_docs = []
        for i, doc in enumerate(docs):
            metadata = doc.metadata.copy() if doc.metadata else {}
            metadata["page"] = i + 1  # Assign page number starting at 1
            updated_docs.append(Document(page_content=doc.page_content, metadata=metadata))
        
        # Split the pages into smaller chunks while retaining the metadata (including page number)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(updated_docs)
        
        # Create the ChromaDB instance and store the embeddings
        Chroma.from_documents(chunks, embedding_model, persist_directory=str(db_path))
        log(f"Created and saved ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}")

def load_vectordb(embedding_model_name,chunk_size,chunk_overlap):
    db_path = construct_db_path(embedding_model_name, chunk_size, chunk_overlap)
    log(f"Trying to load ChromaDB instance from {db_path}")
    embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)

    if os.path.exists(db_path):
        vector_db = Chroma(persist_directory=str(db_path), embedding_function=embedding_model)
        log(f"Loaded existing ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}")
        return vector_db
    else:
        log(f"ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap} does not exist. Please create it first.")
    
def create_multiple_vectordbs(embedding_models,chunk_sizes_and_chunk_overlaps):
    for embedding_model_name in embedding_models:
        for chunk_size, chunk_overlap in chunk_sizes_and_chunk_overlaps:
            create_vectordb(embedding_model_name,chunk_size,chunk_overlap)

if __name__ == "__main__":
    embedding_model_names = [LABSE]
    chunk_sizes_and_chunk_overlaps = [(500,50),(1000,100),(2000,200)]
    
    #create_multiple_vectordb(embedding_model_names,chunk_sizes_and_chunk_overlaps)
    create_vectordb(embedding_model_names[0],700,70)