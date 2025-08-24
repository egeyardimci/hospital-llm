from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from backend.ai.vectordb.utils import load_vectordb
from backend.utils.logger import log, log_test
from backend.ai.testing.io_utils import add_test_result, load_test_cases, load_queries_expected_answers
from backend.ai.testing.models import TestCase
from backend.ai.llm.llm_as_a_judge.agent import llm_as_a_judge
from backend.ai.llm.cross_encoder import rerank_with_cross_encoder
import sys

# Load environment variables
load_dotenv()

vector_db_g = None

def run_test(test_case:TestCase, query_expeced_answer):
    """
    Run a single test with the given parameters and save the results to a JSON file.
    """
    log_test(test_case,query_expeced_answer)
    
    vector_db = vector_db_g

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
        evaluation, chunk_evaluation = llm_as_a_judge(
            query_expeced_answer["query"],
            response.content,
            query_expeced_answer["answer"],
            retrieved_chunks
        )

        add_test_result(test_case,query_expeced_answer, response, retrieved_chunks,evaluation,chunk_evaluation)
        
        log(f"Response: {response.content}")
        log(f"LLM Judge Evaluation: {evaluation.output}")
    except Exception as e:
        log(f"LLM judge evaluation error: {e}")
    
    return response.content, evaluation


if __name__ == "__main__":
    test_cases = load_test_cases()
    queries_and_expected_answers = load_queries_expected_answers()
    test_id = int(sys.argv[1])
    vector_db_g = load_vectordb(test_cases[test_id-1].embedding_model_name,test_cases[test_id-1].chunk_size,test_cases[test_id-1].chunk_overlap)
    for query in queries_and_expected_answers:
        run_test(test_cases[test_id-1], query)