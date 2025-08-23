"""
This file contains the data for the tests to be run.

llm_names: List of LLM names to be used for the tests.
embedding_model_names: List of embedding model names to be used for the tests.
system_messages: List of system messages to be used for the tests.
chunk_sizes_and_chunk_overlaps: List of tuples containing chunk sizes and chunk overlaps to be used for the tests.
similar_vector_counts: List of similar vector counts to be used for the tests.
queries: List of queries to be used for the tests.
document_name: Name of the document to be used for the tests and db creation.
"""

import datetime
import json
import os
from logger import log

class TestOption():
    def __init__(self, name,is_enabled ,data):
        self.name = name
        self.is_enabled = is_enabled
        self.data = data
        
    def __str__(self):
        return f"Option: {self.name}, Enabled: {self.is_enabled}, Data: {self.data}"

class TestCase():
    def __init__(self, test_id,llm_name, embedding_model_name, system_message, chunk_size, chunk_overlap, similar_vector_count,options=None):
        self.test_id = test_id
        self.llm_name = llm_name
        self.embedding_model_name = embedding_model_name
        self.system_message = system_message
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.similar_vector_count = similar_vector_count
        
        self.options = []
        if options:
            self.load_options(options)
        
    def load_options(self, options):
        for option in options:
            option_obj = TestOption(option["name"], option["is_enabled"], option["data"])
            self.options.append(option_obj)
        
    def update_option(self, option_name, option_value, data):
        for option in self.options:
            if option.name == option_name:
                option.is_enabled = option_value
                option.data = data
                return
            
        option = TestOption(option_name, option_value, data)
        self.options.append(option)

def load_test_cases() -> list[TestCase]:
    """
    Load test cases from the test_cases.json file.
    
    Returns:
        List of TestCase objects
    """
    test_cases = []
    with open(test_case_input_file, "r", encoding="utf-8") as file:
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
    with open(queries_expected_answer_input_file, "r", encoding="utf-8") as file:
        return json.load(file)

# Function to load existing JSON data
def load_existing_test_results():
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

def add_test_result(test_case: TestCase ,query_expected_answer ,response, retrieved_chunks,evaluation,chunk_evaluation):
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
        "response": response.content,
        "time_stamp" : str(datetime.datetime.now()),
        "retrieved_chunks": [chunk.page_content for chunk in retrieved_chunks],
        "options": [{"name": option.name, "is_enabled": option.is_enabled, "data": option.data} for option in test_case.options],
        "evaluation": evaluation.output,
        "evaluation_score": evaluation.score,
        "chunk_evaluation": chunk_evaluation.output,
        "chunk_evaluation_score": chunk_evaluation.score
        })
    
    # Write results to a JSON file (append mode)
    with open(test_results_output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    
    log(f"Result saved to {test_results_output_file}")
    

document_name = "doc.pdf"
test_results_output_file = "results.json"
test_case_input_file = "test_cases.json"
queries_expected_answer_input_file = "queries_expected_answers.json"