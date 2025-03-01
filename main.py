import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from vectordb import load_vectordb
from data import llm_names, embedding_model_names, system_messages, chunk_sizes_and_chunk_overlaps, similar_vector_counts, queries
from logger import log
import datetime

# Load environment variables
load_dotenv()

output_file = "results.json"

# Function to load existing JSON data
def load_existing_results():
    
    """
    Load existing results from the output file.
        
    Returns:
        List: List of existing results
    """
    
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)  # Load existing results
            except json.JSONDecodeError:
                return []  # Return an empty list if JSON is corrupted
    return []  # Return an empty list if file doesn't exist

def run_one_test(llm_name, embedding_model_name, system_message, query, chunk_size, chunk_overlap, similar_vector_count):
    """
    Run a single test with the given parameters and save the results to a JSON file.
    
    Args:
        llm_name (str): Name of the LLM model
        embedding_model_name (str): Name of the embedding model
        system_message (str): System message to be used for the test
        query (str): Query to be used for the test
        chunk_size (int): Size of the text chunks
        chunk_overlap (int): Overlap size between the text chunks
        similar_vector_count (int): Number of similar vectors to retrieve
        
    Returns:
        None
    """
    
    results = load_existing_results()  # List to store results

    log(f"Running test for LLM: {llm_name}")
    log(f"Embedding model: {embedding_model_name}")
    log(f"System message: {system_message}")
    log(f"Query: {query}")
    log(f"Chunk size: {chunk_size}")
    log(f"Chunk overlap: {chunk_overlap}")
    log(f"Similar vector count: {similar_vector_count}")
    
    vector_db = load_vectordb(embedding_model_name, chunk_size, chunk_overlap)

    # Querying the document
    retrieved_chunks = vector_db.similarity_search(query, similar_vector_count)  # Get top 20 relevant chunks
    context = "\n\n".join([chunk.page_content for chunk in retrieved_chunks])

    # Use Groq API for response generation
    llm = ChatGroq(model=llm_name)  # Load Llama model
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
    ]
    response = llm.invoke(messages)

    # Store results in a dictionary
    results.append({
        "llm": llm_name,
        "embedding_model": embedding_model_name,
        "system_message": system_message,
        "query": query,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "similar_vector_count" : similar_vector_count,
        "retrieved_chunks": [chunk.page_content for chunk in retrieved_chunks],
        "response": response.content,
        "time_stamp" : str(datetime.datetime.now())
    })
    
    log(f"Response: {response.content}")

    # Write results to a JSON file (append mode)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    log(f"Results saved to {output_file}")

# Run the query for every LLM and every embedding model
def run_tests(llm_names, embedding_model_names, system_messages, queries, similar_vector_counts):
    """
    Run tests for all combinations of LLMs, embedding models, system messages, queries, chunk sizes, chunk overlaps, and similar vector counts.
    
    Args:
        llm_names (list): List of LLM names
        embedding_model_names (list): List of embedding model names
        system_messages (list): List of system messages
        queries (list): List of queries
        similar_vector_counts (list): List of similar vector counts
        
    Returns:
        None
    """
    
    results = load_existing_results()  # List to store results

    for llm_name in llm_names:
        for embedding_model_name in embedding_model_names:
            for chunk_size, chunk_overlap in chunk_sizes_and_chunk_overlaps:
                for system_message in system_messages:
                    for similar_vector_count in similar_vector_counts:
                        for query in queries:
                            log(f"Running test for LLM: {llm_name}")
                            log(f"Embedding model: {embedding_model_name}")
                            log(f"System message: {system_message}")
                            log(f"Query: {query}")
                            log(f"Chunk size: {chunk_size}")
                            log(f"Chunk overlap: {chunk_overlap}")
                            log(f"Similar vector count: {similar_vector_count}")
                            
                            vector_db = load_vectordb(embedding_model_name, chunk_size, chunk_overlap)

                            # Querying the document
                            retrieved_chunks = vector_db.similarity_search(query, similar_vector_count)  # Get top 20 relevant chunks
                            context = "\n\n".join([chunk.page_content for chunk in retrieved_chunks])

                            # Use Groq API for response generation
                            llm = ChatGroq(model=llm_name)  # Load Llama model
                            messages = [
                                SystemMessage(content=system_message),
                                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
                            ]
                            response = llm.invoke(messages)

                            # Store results in a dictionary
                            results.append({
                                "llm": llm_name,
                                "embedding_model": embedding_model_name,
                                "system_message": system_message,
                                "query": query,
                                "chunk_size": chunk_size,
                                "chunk_overlap": chunk_overlap,
                                "similar_vector_count" : similar_vector_count,
                                "retrieved_chunks": [chunk.page_content for chunk in retrieved_chunks],
                                "response": response.content,
                                "time_stamp" : str(datetime.datetime.now())
                            })
                            
                            log(f"Response: {response.content}")

    # Write results to a JSON file (append mode)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    log(f"Results saved to {output_file}")

if __name__ == "__main__":
    # Run all tests
    run_tests(llm_names, embedding_model_names, system_messages, queries, similar_vector_counts)
    
    # If you want to run just one test use function bellow.
    #run_one_test(llm_names[0], embedding_model_names[0], system_messages[0], queries[0], chunk_sizes_and_chunk_overlaps[0][0], chunk_sizes_and_chunk_overlaps[0][1], similar_vector_counts[0])
