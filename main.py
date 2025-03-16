import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from vectordb import load_vectordb
from data import load_test_cases, load_queries_expected_answers, add_test_result
from logger import log
import datetime
from data import TestCase
from sentence_transformers import CrossEncoder

# Load environment variables
load_dotenv()

def rerank_with_cross_encoder(query, retrieved_chunks, cross_encoder_model_name, top_k=None):
    """
    Re-rank retrieved chunks using a cross-encoder.
    
    Args:
        query: The query string
        retrieved_chunks: List of retrieved document chunks
        cross_encoder_model_name: Name of the cross-encoder model
        top_k: Number of top chunks to return after re-ranking (default: return all)
        
    Returns:
        List of re-ranked document chunks
    """
    cross_encoder = CrossEncoder(cross_encoder_model_name)

    # Debug log
    log(f"Original chunks count: {len(retrieved_chunks)}")
    log(f"Cross-encoder top_k parameter: {top_k}")
    
    
    # Prepare pairs of (query, chunk) for the cross-encoder
    pairs = [(query, chunk.page_content) for chunk in retrieved_chunks]
    
    # Get relevance scores
    scores = cross_encoder.predict(pairs)
    
    # Create list of (chunk, score) tuples
    chunk_score_pairs = list(zip(retrieved_chunks, scores))
    
    # Sort by score in descending order
    reranked_chunks = sorted(chunk_score_pairs, key=lambda x: x[1], reverse=True)
    
    # Return top_k chunks if specified, otherwise return all
    if top_k is not None:
        reranked_chunks = reranked_chunks[:top_k]
    
    # Return just the chunks, not the scores
    return [chunk for chunk, _ in reranked_chunks]


def run_one_test(test_case:TestCase, query_expeced_answer):
    """
    Run a single test with the given parameters and save the results to a JSON file.
    
    Args:
        test_case: TestCase object
        query_expeced_answer: Dictionary containing the query and expected
        
    Returns:
        None
    """
    print("INSIDEEEEEE")
    log_test(test_case,query_expeced_answer)
    
    vector_db = load_vectordb(test_case.embedding_model_name, test_case.chunk_size, test_case.chunk_overlap)

    # Querying the document
    retrieved_chunks = vector_db.similarity_search(query_expeced_answer["query"], test_case.similar_vector_count)  # Get top 20 relevant chunks
    
    cross_encoder_option = None
    for option in test_case.options:
        if option.name == "CE" and option.is_enabled:
            cross_encoder_option = option
            break
    if cross_encoder_option:
        cross_encoder_model_name = cross_encoder_option.data
        top_k = 5  # Default to using all chunks
        
        # If data is a dictionary, check for top_k parameter
        if isinstance(cross_encoder_option.data, dict):
            cross_encoder_model_name = cross_encoder_option.data.get("model_name")
            top_k = cross_encoder_option.data.get("top_k")
        
        log(f"Re-ranking with cross-encoder: {cross_encoder_model_name}")
        retrieved_chunks = rerank_with_cross_encoder(
            query_expeced_answer["query"], 
            retrieved_chunks, 
            cross_encoder_model_name,
            top_k
        )
    
    
    context = "\n\n".join([chunk.page_content for chunk in retrieved_chunks])
    print("AAAAAAAAAA ",len(retrieved_chunks))
    # Use Groq API for response generation
    llm = ChatGroq(model=test_case.llm_name)  # Load Llama model
    messages = [
        SystemMessage(content=test_case.system_message),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query_expeced_answer['query']}")
    ]
    response = llm.invoke(messages)
    
    log(f"Response: {response.content}")
    
    add_test_result(test_case, query_expeced_answer, response, retrieved_chunks)
    return response.content

# Run the query for every LLM and every embedding model
def run_tests(test_cases:list[TestCase], queryies_expeced_answers):
    """
    Run tests for all combinations of LLMs, embedding models, system messages, queries, chunk sizes, chunk overlaps, and similar vector counts.
    
    Args:
        test_cases: List of TestCase objects
        queries_and_expected_answers: List of dictionaries containing queries and expected answers
    Returns:
        None
    """
    for test_case in test_cases:
        for query_expeced_answer in queryies_expeced_answers:
            log_test(test_case,query_expeced_answer)
            
            vector_db = load_vectordb(test_case.embedding_model_name, test_case.chunk_size, test_case.chunk_overlap)
        
            # Querying the document
            retrieved_chunks = vector_db.similarity_search(query_expeced_answer["query"], test_case.similar_vector_count)  # Get top 20 relevant chunks
            

            cross_encoder_option = None
            for option in test_case.options:
                if option.name == "CE" and option.is_enabled:
                    cross_encoder_option = option
                    break
            if cross_encoder_option:
                cross_encoder_model_name = cross_encoder_option.data
                top_k = 5  # Default to using all chunks
                
                # If data is a dictionary, check for top_k parameter
                if isinstance(cross_encoder_option.data, dict):
                    cross_encoder_model_name = cross_encoder_option.data.get("model_name")
                    top_k = cross_encoder_option.data.get("top_k")
                    
                log(f"Re-ranking with cross-encoder: {cross_encoder_model_name}")
                retrieved_chunks = rerank_with_cross_encoder(
                    query_expeced_answer["query"], 
                    retrieved_chunks, 
                    cross_encoder_model_name,
                    top_k
                )

            context = "\n\n".join([f'{chunk.page_content} Page Number: {chunk.metadata.get("page", "Unknown")}' for chunk in retrieved_chunks])

            print("AAAAAAAAAA ",len(retrieved_chunks))
            # Use Groq API for response generation
            llm = ChatGroq(model=test_case.llm_name)  # Load Llama model
            messages = [
                SystemMessage(content=test_case.system_message),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query_expeced_answer['query']}")
            ]
            response = llm.invoke(messages)
                    
            log(f"Response: {response.content}")
            add_test_result(test_case,query_expeced_answer, response, retrieved_chunks)


def log_test(test_case:TestCase, quey_expected_answer):
    """
    Log the test parameters.
    """
    
    try:
        log(f"Running test for LLM: {test_case.llm_name}")
        log(f"Embedding model: {test_case.embedding_model_name}")
        log(f"System message: {test_case.system_message}")
        log(f"Query: {quey_expected_answer['query']}")
        log(f"Exptected answer: {quey_expected_answer['answer']}")
        log(f"Chunk size: {test_case.chunk_size}")
        log(f"Chunk overlap: {test_case.chunk_overlap}")
        log(f"Similar vector count: {test_case.similar_vector_count}")
        log(f"Options: {[str(option) for option in test_case.options]}")
    except Exception as e:
        log(f"Error logging test: {e}")

if __name__ == "__main__":
    # Run all tests
    
    test_cases = load_test_cases()
    queries_and_expected_answers = load_queries_expected_answers()
    run_tests(test_cases, queries_and_expected_answers)
    
    # If you want to run just one test use function bellow.
    #run_one_test(llm_names[0], embedding_model_names[0], system_messages[0], queries_and_expected_answers[0], chunk_sizes_and_chunk_overlaps[0][0], chunk_sizes_and_chunk_overlaps[0][1], similar_vector_counts[0])
    #test_case = TestCase("llama-3.3-70b-versatile", "sentence-transformers/all-MiniLM-L6-v2", "Hello, how can I help you today?", 500, 50, 10)
    #query_expeced_answer = {"query": "What is the capital of France?", "answer": "Paris"}
    #run_one_test(test_case, query_expeced_answer)