'''
This module defines various directory paths used in the backend application.
'''
from pathlib import Path
from backend.common.constants import *

CURRENT_DIR = Path(__file__).parent
BACKEND_DIR = CURRENT_DIR.parent
AI_DIR = BACKEND_DIR / AI
WEB_DIR = BACKEND_DIR / WEB
DOCUMENTS_DIR = AI_DIR / DOCUMENTS
TESTING_DIR = AI_DIR / TESTING
TESTING_CONFIG_DIR = TESTING_DIR / CONFIG

REACT_BUILD_PATH = WEB_DIR / REACT_BUILD
TEST_RESULTS_PATH = TESTING_CONFIG_DIR / TEST_RESULTS_FILE_NAME
TEST_CASES_PATH = TESTING_CONFIG_DIR / TEST_CASES_FILE_NAME
TEST_QUERIES_AND_EXPECTED_ANSWERS_PATH = TESTING_CONFIG_DIR / TEST_QUERIES_AND_EXPECTED_ANSWERS_FILE_NAME
SGK_DOCUMENT_PATH = DOCUMENTS_DIR / SGK_DOCUMENT_FILE_NAME
CHROMA_DB_PATH = AI_DIR / CHROMA_DB
DOCUMENTS_PATH = AI_DIR / DOCUMENTS

def construct_db_path(embedding_mode_name, chunk_size, chunk_overlap):
    """
    Construct a new database path based on the embedding mode name, chunk size, and chunk overlap.
    """
    return CHROMA_DB_PATH / f"chroma_db_{embedding_mode_name}_{chunk_size}_{chunk_overlap}"
