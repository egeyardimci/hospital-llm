import datetime

from bson import ObjectId
from backend.ai.llm.llm_as_a_judge.models import JudgeOutput
from backend.ai.testing.models import TestCase
from langchain_core.documents import Document
from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT
from backend.utils.logger import get_logger
logger = get_logger()

def load_test_cases() -> list[TestCase]:
    """
    Load test cases from the test_cases.json file.
    
    Returns:
        List of TestCase objects
    """
    test_cases = []
    collection = GLOBAL_MONGO_DB_CLIENT.get_test_cases_collection()
    documents = list(collection.find().sort("test_id", 1)) 
    for case in documents:
        test_case = TestCase(case["test_id"],case["llm_name"], case["embedding_model_name"], case["system_message"], case["chunk_size"], case["chunk_overlap"], case["similar_vector_count"],case["options"])
        test_cases.append(test_case)
    
    return test_cases

def load_test_case_by_test_id(test_id) -> TestCase:
    """
    Load a single test case by its ID from the database.
    
    Args:
        test_id: ID of the test case to be loaded

    Returns:
        TestCase object
    """
    collection = GLOBAL_MONGO_DB_CLIENT.get_test_cases_collection()
    document = collection.find_one({"test_id": test_id})
    if document:
        return TestCase(document["test_id"], document["llm_name"], document["embedding_model_name"], document["system_message"], document["chunk_size"], document["chunk_overlap"], document["similar_vector_count"], document["options"],document["qa_batch"], document.get("rag_database", None))
    return None

def load_queries_expected_answers():
    """
    Load queries and expected answers from the queries_expected_answers.json file.
    
    Returns:
        List of dictionaries containing queries and expected answers
    """
    collection = GLOBAL_MONGO_DB_CLIENT.get_queries_collection()
    documents = list(collection.find())
    return documents

def load_queries_expected_answers_batch_by_id(batch_id):
    collection = GLOBAL_MONGO_DB_CLIENT.get_queries_collection()
    documents = list(collection.find({"batch_id": batch_id}))
    return documents

def load_system_message_by_id(system_message_id):
    collection = GLOBAL_MONGO_DB_CLIENT.get_system_prompts_collection()
    document = collection.find_one({"_id": ObjectId(system_message_id)})
    return document

def load_run_count():
    collection = GLOBAL_MONGO_DB_CLIENT.get_config_collection()
    document = collection.find_one({"name": "run_count"})
    run_count = document["data"]

    return run_count

def increment_run_count():
    collection = GLOBAL_MONGO_DB_CLIENT.get_config_collection()
    document = collection.find_one({"name": "run_count"})
    run_count = document["data"]
    run_count += 1
    collection.update_one({"name": "run_count"}, {"$set": {"data": run_count}})
    return run_count
    

# Function to load existing JSON data
def load_existing_test_results():
    """
    Load existing results from the output file.
        
    Returns:
        List: List of existing results
    """
    collection = GLOBAL_MONGO_DB_CLIENT.get_results_collection()
    documents = list(collection.find())
    return documents

def add_test_result(test_case: TestCase ,query_expected_answer: dict ,response: str ,retrieved_chunks: list[Document] ,evaluation: JudgeOutput ,chunk_evaluation: JudgeOutput, run_count: int, error: str = "", retrieval_metrics: dict = None, generation_metrics: dict = None):
    """
    Add a test result to the existing results.

    Args:
        retrieval_metrics: Optional dict containing retrieval quality metrics (RAGAs context metrics, etc.)
        generation_metrics: Optional dict containing generation quality metrics (RAGAs, ROUGE, BLEU, etc.)
    """
    # Store results in a dictionary
    result = {
        "test_id": test_case.test_id,
        "llm": test_case.llm_name,
        "embedding_model": test_case.embedding_model_name,
        "system_message": test_case.system_message,
        "query": query_expected_answer["query"],
        "chunk_size": test_case.chunk_size,
        "chunk_overlap": test_case.chunk_overlap,
        "similar_vector_count" : test_case.similar_vector_count,
        "expected_answer": query_expected_answer["answer"],
        "response": response,
        "time_stamp" : str(datetime.datetime.now()),
        "retrieved_chunks": [chunk.page_content for chunk in retrieved_chunks],
        "options": [{"name": option.name, "is_enabled": option.is_enabled, "data": option.data} for option in test_case.options],
        "evaluation": evaluation.feedback if evaluation is not None else '',
        "evaluation_score": evaluation.score if evaluation is not None else 0,
        "evaluation_reasoning": evaluation.reasoning if evaluation is not None else '',
        "chunk_evaluation": chunk_evaluation.feedback if chunk_evaluation is not None else '',
        "chunk_evaluation_score": chunk_evaluation.score if chunk_evaluation is not None else 0,
        "chunk_evaluation_reasoning": chunk_evaluation.reasoning if chunk_evaluation is not None else '',
        "run_count" : run_count,
        "rag_database": test_case.rag_database,
        "error": error if error else '',
        "retrieval_metrics": retrieval_metrics or {},
        "generation_metrics": generation_metrics or {}
        }

    collection = GLOBAL_MONGO_DB_CLIENT.get_results_collection()
    collection.insert_one(result)

    logger.info(f"Result saved to database.")

def add_run_record(run_count: int, test_case: TestCase, qa_batch_id: str | None = None):
    """
    Add a run record to the runs collection.
    """
    run_record = {
        "test_id": test_case.test_id,
        "llm": test_case.llm_name,
        "embedding_model": test_case.embedding_model_name,
        "system_message": test_case.system_message,
        "chunk_size": test_case.chunk_size,
        "chunk_overlap": test_case.chunk_overlap,
        "similar_vector_count" : test_case.similar_vector_count,
        "time_stamp" : str(datetime.datetime.now()),
        "options": [{"name": option.name, "is_enabled": option.is_enabled, "data": option.data} for option in test_case.options],
        "run_count" : run_count,
        "rag_database": test_case.rag_database,
        "qa_batch_id": qa_batch_id
        }

    collection = GLOBAL_MONGO_DB_CLIENT.get_runs_collection()
    collection.insert_one(run_record)

    logger.info(f"Run record for run {run_count} added to database.")

if __name__ == "__main__":
    test_cases = load_test_cases()
    print(f"Loaded {len(test_cases)} test cases.")
    queries_expected_answers = load_queries_expected_answers()
    print(f"Loaded {len(queries_expected_answers)} queries and expected answers.")
    existing_results = load_existing_test_results()
    print(f"Loaded {len(existing_results)} existing results.")
    print("test:", existing_results[0])