from bson import ObjectId
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from backend.ai.llm.llm_as_a_judge.models import JudgeOutput
from backend.ai.llm.rag import rag_invoke
from backend.ai.vectordb.utils import load_vectordb
from backend.utils.logger import log, log_test
from backend.ai.testing.io_utils import add_test_result, load_queries_expected_answers_batch_by_id, load_test_case_by_test_id, load_system_message_by_id, load_run_count, increment_run_count
from backend.ai.testing.models import RagResponse, TestCase
from backend.ai.llm.llm_as_a_judge.agent import llm_as_a_judge
from backend.ai.llm.cross_encoder import rerank_with_cross_encoder
import sys

from backend.utils.logger2 import get_logger

# Load environment variables

logger = get_logger()

def run_test(test_case:TestCase, query_expeced_answer, run_count:int):
    """
    Run a single test with the given parameters and save the results to a JSON file.
    """
    log_test(test_case,query_expeced_answer)
    evaluation: None | JudgeOutput = None
    chunk_evaluation: None | JudgeOutput = None
    rag_response: None | str = None
    rag_metadata: None | dict = None

    vector_db = load_vectordb(test_case.embedding_model_name,test_case.chunk_size,test_case.chunk_overlap)

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
        logger.error(f"RAG system error: {e}")
        return

    try:
        evaluation, chunk_evaluation = llm_as_a_judge(
            query_expeced_answer["query"],
            rag_response,
            query_expeced_answer["answer"],
            rag_metadata["retrieved_chunks"]
        )

    except Exception as e:
        logger.error(f"LLM judge evaluation error: {e}")
        return

    add_test_result(test_case,query_expeced_answer, rag_response, rag_metadata["retrieved_chunks"],evaluation,chunk_evaluation, run_count)

    log("\n---------------------------------------------------------")
    log(f"RAG Response: {rag_response}")
    log(f"LLM Judge Evaluation: {evaluation.feedback}")
    log("---------------------------------------------------------\n")

def run_test_case_by_test_id(test_id):
    load_dotenv(override=True)

    try:
        logger.debug(f"Loading test case with ID: {test_id}")
        test_case = load_test_case_by_test_id(test_id)
        qa_batch_id = test_case.qa_batch
        queries_and_expected_answers = load_queries_expected_answers_batch_by_id(qa_batch_id)
        logger.debug(f"Successfully loaded test case and {len(queries_and_expected_answers)} Q&A pairs")
    except Exception as e:
        logger.error(f"Failed to load test case or Q&A batch for test_id {test_id}: {e}")
        raise Exception(f"Test case loading failed: {e}") from e

    try:
        logger.debug(f"Loading system message with ID: {test_case.system_message}")
        system_message = load_system_message_by_id(test_case.system_message)
        run_count = load_run_count()
        test_case.system_message = system_message["content"]
        logger.debug("Successfully loaded system message")
    except Exception as e:
        logger.error(f"Failed to load system message for test_id {test_id}: {e}")
        raise Exception(f"System message loading failed: {e}") from e

    logger.info(f"Running test case {test_case.test_id} with {len(queries_and_expected_answers)} queries.")

    try:
        for i, query in enumerate(queries_and_expected_answers, 1):
            logger.debug(f"Processing query {i}/{len(queries_and_expected_answers)}")
            run_test(test_case, query, run_count)
        
        increment_run_count()
        logger.info(f"Successfully completed all {len(queries_and_expected_answers)} tests")
    except Exception as e:
        logger.error(f"Test execution failed during query processing: {e}")
        raise Exception(f"Test execution failed: {e}") from e

if __name__ == "__main__":
    test_id = int(sys.argv[1])
    run_test_case_by_test_id(test_id)
