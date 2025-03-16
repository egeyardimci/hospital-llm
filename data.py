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
    def __init__(self, is_enabled, name ,data):
        self.is_enabled = is_enabled
        self.name = ""
        self.data = data

class TestCase():
    def __init__(self, llm_name, embedding_model_name, system_message, chunk_size, chunk_overlap, similar_vector_count):
        self.llm_name = llm_name
        self.embedding_model_name = embedding_model_name
        self.system_message = system_message
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.similar_vector_count = similar_vector_count
        
        self.options = []
        
    def update_option(self, option_name, option_value, data):
        for option in self.options:
            if option.name == option_name:
                option.is_enabled = option_value
                option.data = data
                return
            
        option = TestOption(option_name, option_value, data)
        self.options.append(option)

def load_test_cases():
    """
    Load test cases from the test_cases.json file.
    
    Returns:
        List of TestCase objects
    """
    test_cases = []
    with open(test_case_input_file, "r") as file:
        data = json.load(file)
        for case in data:
            test_case = TestCase(case["llm_name"], case["embedding_model_name"], case["system_message"], case["chunk_size"], case["chunk_overlap"], case["similar_vector_count"])
            test_cases.append(test_case)
    
    return test_cases

def load_queries_expected_answers():
    """
    Load queries and expected answers from the queries_expected_answers.json file.
    
    Returns:
        List of dictionaries containing queries and expected answers
    """
    with open(queries_expected_answer_input_file, "r") as file:
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

def add_test_result(test_case: TestCase ,query_expected_answer ,response, retrieved_chunks):
    """
    Add a test result to the existing results.
    """
    results = load_existing_test_results()  # List to store results
    # Store results in a dictionary
    results.append({
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
        "options": test_case.options
    })
    
    # Write results to a JSON file (append mode)
    with open(test_results_output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    
    log(f"Result saved to {test_results_output_file}")
    

document_name = "doc.docx"
test_results_output_file = "results.json"
test_case_input_file = "test_cases.json"
queries_expected_answer_input_file = "queries_expected_answers.json"