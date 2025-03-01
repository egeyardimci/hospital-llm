import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from vectordb import load_vectordb
from data import llm_names, embedding_model_names, system_messages, chunk_sizes_and_chunk_overlaps, similar_vector_counts, queries_and_expected_answers, test_results_output_file
from logger import log
import datetime

# Load environment variables
load_dotenv()

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
    log_test(llm_name, embedding_model_name, system_message, query, chunk_size, chunk_overlap, similar_vector_count)
    
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
    
    log(f"Response: {response.content}")
    add_test_result(llm_name, embedding_model_name, system_message, query, chunk_size, chunk_overlap, similar_vector_count, response, retrieved_chunks)

# Run the query for every LLM and every embedding model
def run_tests(llm_names, embedding_model_names, system_messages, queries_and_answers, similar_vector_counts):
    """
    Run tests for all combinations of LLMs, embedding models, system messages, queries, chunk sizes, chunk overlaps, and similar vector counts.
    
    Args:
        llm_names (list): List of LLM names
        embedding_model_names (list): List of embedding model names
        system_messages (list): List of system messages
        queries_and_answers (list): List of queries and expected answers
        chunk_sizes_and_chunk_overlaps (list): List of tuples containing chunk sizes and chunk overlaps
        similar_vector_counts (list): List of similar vector counts
        
    Returns:
        None
    """

    for llm_name in llm_names:
        for embedding_model_name in embedding_model_names:
            for chunk_size, chunk_overlap in chunk_sizes_and_chunk_overlaps:
                for system_message in system_messages:
                    for similar_vector_count in similar_vector_counts:
                        for query_and_answer in queries_and_answers:
                            log_test(llm_name, embedding_model_name, system_message, query_and_answer, chunk_size, chunk_overlap, similar_vector_count)
                            
                            vector_db = load_vectordb(embedding_model_name, chunk_size, chunk_overlap)
                        
                            # Querying the document
                            retrieved_chunks = vector_db.similarity_search(query_and_answer["query"], similar_vector_count)  # Get top 20 relevant chunks
                            context = "\n\n".join([chunk.page_content for chunk in retrieved_chunks])

                            # Use Groq API for response generation
                            llm = ChatGroq(model=llm_name)  # Load Llama model
                            messages = [
                                SystemMessage(content=system_message),
                                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query_and_answer['query']}")
                            ]
                            response = llm.invoke(messages)
                                   
                            log(f"Response: {response.content}")
                            add_test_result(llm_name, embedding_model_name, system_message, query_and_answer, chunk_size, chunk_overlap, similar_vector_count, response, retrieved_chunks)

# Function to load existing JSON data
def load_existing_results():
    """
    Load existing results from the output file.
        
    Returns:
        List: List of existing results
    """
    
    if os.path.exists(test_results_output_file):
        with open(test_results_output_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)  # Load existing results
            except json.JSONDecodeError:
                return []  # Return an empty list if JSON is corrupted
    return []  # Return an empty list if file doesn't exist

def add_test_result(llm_name, embedding_model_name, system_message, query_and_answer, chunk_size, chunk_overlap, similar_vector_count, response, retrieved_chunks):
    """
    Add a test result to the existing results.
    """
    results = load_existing_results()  # List to store results
    # Store results in a dictionary
    results.append({
        "llm": llm_name,
        "embedding_model": embedding_model_name,
        "system_message": system_message,
        "query": query_and_answer["query"],
        "expected_answer": query_and_answer["answer"],
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "similar_vector_count" : similar_vector_count,
        "retrieved_chunks": [chunk.page_content for chunk in retrieved_chunks],
        "response": response.content,
        "time_stamp" : str(datetime.datetime.now())
    })
    
    # Write results to a JSON file (append mode)
    with open(test_results_output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    
    log(f"Result saved to {test_results_output_file}")
    

def log_test(llm_name, embedding_model_name, system_message, query_and_answer, chunk_size, chunk_overlap, similar_vector_count):
    """
    Log the test parameters.
    """
    
    log(f"Running test for LLM: {llm_name}")
    log(f"Embedding model: {embedding_model_name}")
    log(f"System message: {system_message}")
    log(f"Query: {query_and_answer['query']}")
    log(f"Exptected answer: {query_and_answer['answer']}")
    log(f"Chunk size: {chunk_size}")
    log(f"Chunk overlap: {chunk_overlap}")
    log(f"Similar vector count: {similar_vector_count}")

if __name__ == "__main__":
    # Run all tests
    run_tests(llm_names, embedding_model_names, system_messages, queries_and_expected_answers, similar_vector_counts)
    
    # If you want to run just one test use function bellow.
    #run_one_test(llm_names[0], embedding_model_names[0], system_messages[0], queries_and_expected_answers[0], chunk_sizes_and_chunk_overlaps[0][0], chunk_sizes_and_chunk_overlaps[0][1], similar_vector_counts[0])
