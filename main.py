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


def llm_as_a_judge(query: str, response: str, expected_answer: str,system_message:str) -> dict:
    """
    Turkish-specific LLM judge with language-aware evaluation.
    """
    llm = ChatGroq(model="deepseek-r1-distill-qwen-32b")
    
    evaluation_prompt = """You are a judge evaluating the quality of an AI's response to a question.
Please evaluate the response based on the following criteria:
1. Accuracy: How well does the response match the expected answer?
2. Completeness: Does the response contain all necessary information?
3. Clarity: Is the response clear and well-structured?
4. Relevance: Does the response directly address the question?

Rate each criterion on a scale of 0-10 and provide brief feedback for each.
Then provide an overall score (0-100) and summary.

IMPORTANT: Your response must be a valid JSON object with exactly this structure:
{{
    "accuracy_score": <number between 0-10>,
    "completeness_score": <number between 0-10>,
    "clarity_score": <number between 0-10>,
    "relevance_score": <number between 0-10>,
    "overall_score": <number between 0-100>,
    "feedback": {{
        "accuracy": "<your feedback text>",
        "completeness": "<your feedback text>",
        "clarity": "<your feedback text>",
        "relevance": "<your feedback text>"
    }},
    "summary": "<your overall summary>"
}}

DO NOT include any text before or after the JSON object. Return ONLY the JSON object.

Query: {query}
Expected Answer: {expected_answer}
Response to Evaluate: {response}
"""

    messages = [
        SystemMessage(content="You are a precise JSON evaluator. Always respond with valid JSON only, no additional text."),
        HumanMessage(content=evaluation_prompt.format(
            query=query,
            expected_answer=expected_answer,
            response=response
        ))
    ]
    
    try:
        response = llm.invoke(messages)
        # Clean the response content to ensure it's valid JSON
        content = response.content.strip()
        # Remove any markdown code block markers if present
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        # Parse the JSON response
        evaluation = json.loads(content)
        
        # Validate the required fields
        required_fields = ["accuracy_score", "completeness_score", "clarity_score", 
                         "relevance_score", "overall_score", "feedback", "summary"]
        for field in required_fields:
            if field not in evaluation:
                raise ValueError(f"Missing required field: {field}")
        
        return evaluation
    except (json.JSONDecodeError, AttributeError, ValueError) as e:
        log(f"Error parsing LLM judge evaluation: {e}")
        log(f"Raw response: {response.content if 'response' in locals() else 'No response'}")
        return {
            "accuracy_score": 0,
            "completeness_score": 0,
            "clarity_score": 0,
            "relevance_score": 0,
            "overall_score": 0,
            "feedback": {
                "accuracy": "Error evaluating response",
                "completeness": "Error evaluating response",
                "clarity": "Error evaluating response",
                "relevance": "Error evaluating response"
            },
            "summary": "Failed to evaluate response"
        }


def rerank_with_cross_encoder(query, retrieved_chunks, cross_encoder_model_name, top_k=None):
    """
    Improved re-ranking with robust error handling and fallback mechanisms.
    """
  
    cross_encoder = CrossEncoder(cross_encoder_model_name)
    try:
        # Prepare pairs of (query, chunk) for the cross-encoder
        pairs = [(query, chunk.page_content) for chunk in retrieved_chunks]
        
        # Get relevance scores with error handling
        scores = cross_encoder.predict(pairs)
        
        # Create list of (chunk, score) tuples
        chunk_score_pairs = list(zip(retrieved_chunks, scores))
        
        # Sort by score in descending order
        reranked_chunks = sorted(chunk_score_pairs, key=lambda x: x[1], reverse=True)
        
        # Return top_k chunks if specified, otherwise return all
        if top_k is not None:
            reranked_chunks = reranked_chunks[:top_k]
        
        # Add logging for re-ranking details
        log(f"Re-ranking results: Original chunks={len(retrieved_chunks)}, Reranked chunks={len(reranked_chunks)}")
        
        return [chunk for chunk, _ in reranked_chunks]
    
    except Exception as e:
        log(f"Cross-encoder re-ranking error: {e}")
        return retrieved_chunks


def run_one_test(test_case:TestCase, query_expeced_answer):
    """
    Run a single test with the given parameters and save the results to a JSON file.
    """
    print("INSIDEEEEEE")
    log_test(test_case,query_expeced_answer)
    
    vector_db = load_vectordb(test_case.embedding_model_name, test_case.chunk_size, test_case.chunk_overlap)

    # Querying the document
    retrieved_chunks = vector_db.similarity_search(query_expeced_answer["query"], test_case.similar_vector_count)
    
    cross_encoder_option = None
    for option in test_case.options:
        if option.name == "CE" and option.is_enabled:
            cross_encoder_option = option
            break
    if cross_encoder_option:
        cross_encoder_model_name = cross_encoder_option.data
        top_k = 7  # Default
        
        if isinstance(cross_encoder_option.data, dict):
            cross_encoder_model_name = cross_encoder_option.data.get("model_name")
            top_k = cross_encoder_option.data.get("top_k", top_k)
        
        log(f"Re-ranking with cross-encoder: {cross_encoder_model_name}")
        retrieved_chunks = rerank_with_cross_encoder(
            query_expeced_answer["query"], 
            retrieved_chunks, 
            cross_encoder_model_name,
            top_k
        )
    
    context = "\n\n".join([chunk.page_content for chunk in retrieved_chunks])
    
    # Use Groq API for response generation
    llm = ChatGroq(model=test_case.llm_name)
    messages = [
        SystemMessage(content=test_case.system_message),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query_expeced_answer['query']}")
    ]
    response = llm.invoke(messages)
    
    # Get LLM judge evaluation
    evaluation = llm_as_a_judge(
        query_expeced_answer["query"],
        response.content,
        query_expeced_answer["answer"],system_message=test_case.system_message
    )
    
    log(f"Response: {response.content}")
    log(f"LLM Judge Evaluation: {json.dumps(evaluation, indent=2)}")
    
    # Add evaluation results to test results
    add_test_result(test_case, query_expeced_answer, response, retrieved_chunks, evaluation)
    return response.content, evaluation

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
                top_k = 7  # Default to using all chunks
                
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


            # Use Groq API for response generation
            llm = ChatGroq(model=test_case.llm_name)  # Load Llama model
            messages = [
                SystemMessage(content=test_case.system_message),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query_expeced_answer['query']}")
            ]
            response = llm.invoke(messages)

            evaluation = llm_as_a_judge(
                query_expeced_answer["query"],
                response.content,
                query_expeced_answer["answer"],system_message=test_case.system_message
            )
                    
            log(f"Response: {response.content}")
            log(f"LLM Judge Evaluation: {json.dumps(evaluation, indent=2)}")
            add_test_result(test_case,query_expeced_answer, response, retrieved_chunks,evaluation)


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