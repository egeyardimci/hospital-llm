import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from vectordb import load_vectordb
from data import load_test_cases, load_queries_expected_answers, add_test_result
from logger import log
import datetime
from data import TestCase
from sentence_transformers import CrossEncoder
import sys
# Hybrid retrieval imports
from rank_bm25 import BM25Okapi
import numpy as np

# Load environment variables
load_dotenv()

vector_db_g = None


class JudgeOutput(BaseModel):
    """
    The output of the LLM judge.
    """
    score: int = Field(
        description="Score determined by the LLM judge"
    )
    output: str = Field(
        description="The output of the LLM judge. It should be a string that all the output of the LLM judge"
    )

def evaluate_retrieval(query: str, retrieved_chunks: List, ground_truth_answer: str, k_precision=7, k_recall=20, cross_encoder_model="cross-encoder/ms-marco-MiniLM-L-6-v2"):
    """
    Evaluates retrieval using semantic Precision@k and Recall@k via a cross-encoder.
    """
    cross_encoder = CrossEncoder(cross_encoder_model, trust_remote_code=True)

    # Pair the ground truth answer with each chunk
    pairs = [(ground_truth_answer, chunk.page_content) for chunk in retrieved_chunks]
    scores = cross_encoder.predict(pairs)

    # Sort retrieved chunks by semantic similarity to ground truth answer
    scored_chunks = sorted(zip(retrieved_chunks, scores), key=lambda x: x[1], reverse=True)

    precision_hits = sum(1 for _, score in scored_chunks[:k_precision] if score > 0.5)
    recall_hits = sum(1 for _, score in scored_chunks[:k_recall] if score > 0.5)

    precision_at_k = precision_hits / k_precision
    recall_at_k = recall_hits / k_recall

    return {
        "precision@3": round(precision_at_k, 3),
        "recall@5": round(recall_at_k, 3)
    }


def llm_as_a_judge(query: str, response: str, expected_answer: str) -> str:
    """
    Turkish-specific LLM judge with language-aware evaluation.
    """
    instruction = """
    You are a helpful assistant specializing in document analysis. Answer questions strictly based on the provided context and DO NOT use any external knowledge. Do not assume or infer information that is not explicitly stated in the context.

    When responding:
    1. If the context contains sufficient information, provide a clear and accurate answer based solely on that information.
    2. If the context does not contain enough information, clearly state that you cannot provide an answer based on the available context.
    3. Always cite your sources by referencing the exact page numbers using this format: <a href='yourfile.pdf#page=PAGENUMBER' target='_blank'>Sayfa PAGENUMBER</a>
    4. When multiple references exist across different pages, summarize the collective information before providing your answer.
    5. Structure your responses with bullet points, numbered lists, or short paragraphs as appropriate to the question.
    6. Communicate exclusively in Turkish, using formal and grammatically correct language unless the user's tone suggests informality is appropriate.

    Remember to analyze the context thoroughly before responding, as the context is formatted as:
    Page Number: [page number]: [content of that page]
    """
    
    llm = ChatGroq(model="deepseek-r1-distill-llama-70b")
    
    evaluation_prompt = """###Task Description:
    An instruction (might include an Input inside it), a response to evaluate, a reference answer that gets a score of 5, and a score rubric representing a evaluation criteria are given.
    1. Write a detailed feedback that assess the quality of the response strictly based on the given score rubric, not evaluating in general.
    2. After writing a feedback, write a score that is an integer between 1 and 5. You should refer to the score rubric.

    ###The instruction to evaluate:
    {instruction}

    ###Response to evaluate:
    {response}

    ###Reference Answer (Score 5):
    {reference_answer}

    ###Score Rubrics:
    [Is the response correct, accurate, and factual based on the reference answer?]
    Score 1: The response is completely incorrect, inaccurate, and/or not factual.
    Score 2: The response is mostly incorrect, inaccurate, and/or not factual.
    Score 3: The response is somewhat correct, accurate, and/or factual.
    Score 4: The response is mostly correct, accurate, and factual.
    Score 5: The response is completely correct, accurate, and factual.

    Respond ONLY with a JSON object with the fields: `score` (integer, 1–5) and `output` (string).
    Do not include any explanations or other text!!! 
    """

    messages = [
        SystemMessage(content="You are an LLM as a judge being used in a RAG system."),
        HumanMessage(content=evaluation_prompt.format(
            instruction=query,
            reference_answer=expected_answer,
            response=response
        ))
    ]
    
    llm = llm.with_structured_output(JudgeOutput)
    evaluation = llm.invoke(messages)
    return evaluation

def rerank_with_cross_encoder(query, retrieved_chunks, cross_encoder_model_name, top_k=None):
    """
    Improved re-ranking with robust error handling and fallback mechanisms.
    """
  
    cross_encoder = CrossEncoder(cross_encoder_model_name, trust_remote_code=True)
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
    log_test(test_case,query_expeced_answer)
    
    vector_db = vector_db_g

    # Hybrid retrieve: vector + BM25
    # Get top N vector results with scores
    vector_results = vector_db.similarity_search_with_score(
        query_expeced_answer["query"], 
        max(test_case.similar_vector_count, 20)
    )
    retrieved_chunks, vector_scores = zip(*vector_results)

    # Compute BM25 scores on these chunks
    tokenized_texts = [
        chunk.page_content.lower().split() for chunk in retrieved_chunks
    ]
    bm25 = BM25Okapi(tokenized_texts)
    query_tokens = query_expeced_answer["query"].lower().split()
    bm25_scores = bm25.get_scores(query_tokens)

    # Normalize scores
    v = np.array(vector_scores, dtype=float)
    b = np.array(bm25_scores, dtype=float)
    v_norm = (v - v.min()) / (v.max() - v.min() + 1e-8)
    b_norm = (b - b.min()) / (b.max() - b.min() + 1e-8)

    # Weighted hybrid score
    alpha = 0.5
    hybrid_scores = alpha * v_norm + (1 - alpha) * b_norm

    # Sort and keep top 15
    hybrid_pairs = sorted(
        zip(retrieved_chunks, hybrid_scores),
        key=lambda x: x[1], reverse=True
    )
    retrieved_chunks = [chunk for chunk, score in hybrid_pairs[:15]]
    
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
    
    context = "\n\n".join([f'Page Number: {chunk.metadata.get("page", "Unknown")}: {chunk.page_content}\n' for chunk in retrieved_chunks])

    
    # Use Groq API for response generation
    llm = ChatGroq(model=test_case.llm_name)
    messages = [
        SystemMessage(content=test_case.system_message),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query_expeced_answer['query']}")
    ]
    response = llm.invoke(messages)
    evaluation = None

    try:
        # Get LLM judge evaluation
        evaluation = llm_as_a_judge(
            query_expeced_answer["query"],
            response.content,
            query_expeced_answer["answer"]
        )

        add_test_result(test_case,query_expeced_answer, response, retrieved_chunks,evaluation)
        
        log(f"Response: {response.content}")
        log(f"LLM Judge Evaluation: {evaluation.output}")
    except Exception as e:
        log(f"LLM judge evaluation error: {e}")
    
        # Evaluate retrieval metrics before reranking/generation
    retrieval_metrics = evaluate_retrieval(
        query_expeced_answer["query"],
        retrieved_chunks,
        query_expeced_answer["answer"]
    )
    log(f"Retrieval evaluation: {retrieval_metrics}")

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
            
            vector_db = vector_db_g
        
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

            context = "\n\n".join([f'Page Number: {chunk.metadata.get("page", "Unknown")}: {chunk.page_content}\n' for chunk in retrieved_chunks])


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
                query_expeced_answer["answer"]
            )
                    
            log(f"Response: {response.content}")
            log(f"LLM Judge Evaluation: {evaluation.output}")
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
    
    #test_cases = load_test_cases()
    #queries_and_expected_answers = load_queries_expected_answers()
    #run_tests(test_cases, queries_and_expected_answers)
    
    # If you want to run just one test use function bellow.
    #run_one_test(llm_names[0], embedding_model_names[0], system_messages[0], queries_and_expected_answers[0], chunk_sizes_and_chunk_overlaps[0][0], chunk_sizes_and_chunk_overlaps[0][1], similar_vector_counts[0])
    #test_case = TestCase("llama-3.3-70b-versatile", "sentence-transformers/all-MiniLM-L6-v2", "Hello, how can I help you today?", 500, 50, 10)
    #query_expeced_answer = {"query": "What is the capital of France?", "answer": "Paris"}
    #run_one_test(test_case, query_expeced_answer)

    test_cases = load_test_cases()
    queries_and_expected_answers = load_queries_expected_answers()
    test_id = int(sys.argv[1])
    vector_db_g = load_vectordb(test_cases[test_id-1].embedding_model_name,test_cases[test_id-1].chunk_size,test_cases[test_id-1].chunk_overlap)
    for query in queries_and_expected_answers:
        run_one_test(test_cases[test_id-1], query)