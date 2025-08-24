import datetime
import json
import os
from backend.ai.llm.llm_as_a_judge.models import JudgeOutput
from backend.utils.logger import log
from backend.ai.testing.models import TestCase
from backend.common.paths import TEST_CASES_PATH, TEST_RESULTS_PATH, TEST_QUERIES_AND_EXPECTED_ANSWERS_PATH
from langchain_core.documents import Document

def load_test_cases() -> list[TestCase]:
    """
    Load test cases from the test_cases.json file.
    
    Returns:
        List of TestCase objects
    """
    test_cases = []
    with open(TEST_CASES_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
        for case in data:
            test_case = TestCase(case["test_id"],case["llm_name"], case["embedding_model_name"], case["system_message"], case["chunk_size"], case["chunk_overlap"], case["similar_vector_count"],case["options"])
            test_cases.append(test_case)
    
    return test_cases

def load_queries_expected_answers():
    """
    Load queries and expected answers from the queries_expected_answers.json file.
    
    Returns:
        List of dictionaries containing queries and expected answers
    """
    with open(TEST_QUERIES_AND_EXPECTED_ANSWERS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

# Function to load existing JSON data
def load_existing_test_results():
    """
    Load existing results from the output file.
        
    Returns:
        List: List of existing results
    """

    if os.path.exists(TEST_RESULTS_PATH):
        with open(TEST_RESULTS_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)  # Load existing results
            except json.JSONDecodeError:
                return []  # Return an empty list if JSON is corrupted
    return []  # Return an empty list if file doesn't exist

def add_test_result(test_case: TestCase ,query_expected_answer: dict ,response: str ,retrieved_chunks: list[Document] ,evaluation: JudgeOutput ,chunk_evaluation: JudgeOutput):
    """
    Add a test result to the existing results.
    """
    results = load_existing_test_results()  # List to store results
    # Store results in a dictionary
    results.append({
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
        "evaluation": evaluation.output,
        "evaluation_score": evaluation.score,
        "chunk_evaluation": chunk_evaluation.output,
        "chunk_evaluation_score": chunk_evaluation.score
        })
    
    # Write results to a JSON file (append mode)
    with open(TEST_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


    log(f"Result saved to {TEST_RESULTS_PATH}")