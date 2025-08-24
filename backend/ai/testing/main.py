from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from backend.ai.llm.llm_as_a_judge.models import JudgeOutput
from backend.ai.llm.rag import rag_invoke
from backend.ai.vectordb.utils import load_vectordb
from backend.utils.logger import log, log_test
from backend.ai.testing.io_utils import add_test_result, load_test_cases, load_queries_expected_answers
from backend.ai.testing.models import RagResponse, TestCase
from backend.ai.llm.llm_as_a_judge.agent import llm_as_a_judge
from backend.ai.llm.cross_encoder import rerank_with_cross_encoder
import sys

# Load environment variables
load_dotenv()

vector_db_g: Chroma = None

def run_test(test_case:TestCase, query_expeced_answer):
    """
    Run a single test with the given parameters and save the results to a JSON file.
    """
    log_test(test_case,query_expeced_answer)
    evaluation: None | JudgeOutput = None
    chunk_evaluation: None | JudgeOutput = None
    rag_response: None | str = None
    rag_metadata: None | dict = None

    vector_db = vector_db_g
    try:
        rag: RagResponse = rag_invoke(
            test_case.llm_name,
            test_case.system_message,
            vector_db,
            test_case.similar_vector_count,
            query_expeced_answer["query"],
            test_case.options
        )
        rag_response = rag.content
        rag_metadata = rag.metadata
    except Exception as e:
        log(f"RAG system error: {e}")
        return

    try:
        # Get LLM judge evaluation
        #TODO: write a better system prompt this prompt fails to generate valid json often 
        evaluation, chunk_evaluation = llm_as_a_judge(
            query_expeced_answer["query"],
            rag_response,
            query_expeced_answer["answer"],
            rag_metadata["retrieved_chunks"]
        )

    except Exception as e:
        log(f"LLM judge evaluation error: {e}")
        return

    add_test_result(test_case,query_expeced_answer, rag_response, rag_metadata["retrieved_chunks"],evaluation,chunk_evaluation)

    log(f"RAG Response: {rag_response}")
    log(f"LLM Judge Evaluation: {evaluation.output}")

if __name__ == "__main__":
    test_cases = load_test_cases()
    queries_and_expected_answers = load_queries_expected_answers()
    test_id = int(sys.argv[1])
    vector_db_g = load_vectordb(test_cases[test_id-1].embedding_model_name,test_cases[test_id-1].chunk_size,test_cases[test_id-1].chunk_overlap)
    for query in queries_and_expected_answers:
        run_test(test_cases[test_id-1], query)