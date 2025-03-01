import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from data import embedding_model_names, document_name, chunk_sizes_and_chunk_overlaps
from logger import log

load_dotenv()

"""
This file contains the functions to create and load ChromaDB instances for the tests.

create_vectordb: Function to create a new ChromaDB instance.
load_vectordb: Function to load an existing ChromaDB instance.
create_test_dbs: Function to create ChromaDB instances for all embedding models and chunk sizes.
create_singe_test_db: Function to create a single ChromaDB instance for a given embedding model and chunk size.
"""

def create_vectordb(embedding_model,chunk_size,chunk_overlap):
    """
    Create a new ChromaDB instance for the given embedding model and chunk size.
    
    Args:
        embedding_model: Embedding model to be used for the ChromaDB
        chunk_size: Size of the text chunks to be used for the ChromaDB
        chunk_overlap: Overlap size between the text chunks
    
    Returns:
        None
    """
    CHROMA_DB_PATH = f"chroma_db/chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}"
    if os.path.exists(CHROMA_DB_PATH):
        log("ChromaDB already exists.")
    else:
        log(f"Started creating ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}")
        # Load Word document
        loader = UnstructuredWordDocumentLoader(document_name)
        docs = loader.load()

        # Split document into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(docs)

        # Create ChromaDB and store embeddings
        vector_db = Chroma.from_documents(chunks, embedding_model, persist_directory=CHROMA_DB_PATH)
        log(f"Created and saved ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}")
    
def load_vectordb(embedding_model_name,chunk_size,chunk_overlap):
    """
    Load an existing ChromaDB instance for the given embedding model and chunk size.
    
    Args:
        embedding_model_name: Name of the embedding model
        chunk_size: Size of the text chunks
        chunk_overlap: Overlap size between the text chunks
    
    Returns:
        ChromaDB instance
    """
    embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name) # vector size kaç? embeding modllerini incele
    CHROMA_DB_PATH = f"chroma_db/chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}"
    if os.path.exists(CHROMA_DB_PATH):
        vector_db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embedding_model)
        log(f"Loaded existing ChromaDB instance chroma_db_{embedding_model.model_name}_{chunk_size}_{chunk_overlap}")
        return vector_db
    
def create_test_dbs(embedding_models,chunk_size=500,chunk_overlap=50):
    """
    Create ChromaDB instances for all embedding models and chunk sizes.
    
    Args:
        embedding_models: List of embedding model names
        chunk_size: Size of the text chunks
        chunk_overlap: Overlap size between the text chunks
        
    Returns:
        None
    """
    for embedding_model_name in embedding_models:
        for chunk_size, chunk_overlap in chunk_sizes_and_chunk_overlaps:
            embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name) # vector size kaç? embeding modllerini incele
            create_vectordb(embedding_model,chunk_size,chunk_overlap)
            
def create_singe_test_db(embedding_model_name,chunk_size=500,chunk_overlap=50):
    """
    Create a single ChromaDB instance for a given embedding model and chunk size.
    
    Args:
        embedding_model_name: Name of the embedding model
        chunk_size: Size of the text chunks
        chunk_overlap: Overlap size between the text chunks

    Returns:
        None
    """
    for chunk_size, chunk_overlap in chunk_sizes_and_chunk_overlaps:
        embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name) # vector size kaç? embeding modllerini incele
        create_vectordb(embedding_model,chunk_size,chunk_overlap)
    
if __name__ == "__main__":
    create_test_dbs(embedding_model_names,500,50)
    #create_singe_test_db(embedding_model_names[0],500,50)