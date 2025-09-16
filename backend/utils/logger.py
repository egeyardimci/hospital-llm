from datetime import datetime
from typing import Any
import inspect
import os

from backend.ai.testing.models import TestCase

# ANSI color codes
COLORS = {
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'PURPLE': '\033[95m',
    'CYAN': '\033[96m',
    'GRAY': '\033[90m',
    'WHITE': '\033[97m',
    'BOLD': '\033[1m',
    'END': '\033[0m'
}

def log(message: Any, level: str = 'INFO', show_line: bool = True) -> None:
    """
    Simple colored logging function for better terminal visibility.
    
    Args:
        message: Message to log (can be any type)
        level: Log level ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        show_line: Show the file and line number where log was called
    """
    # Color mapping for different log levels
    level_colors = {
        'DEBUG': COLORS['GRAY'],
        'INFO': COLORS['GREEN'],
        'WARNING': COLORS['YELLOW'],
        'ERROR': COLORS['RED']
    }
    
    # Get timestamp
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    # Get caller info if show_line is True
    caller_info = ''
    if show_line:
        frame = inspect.currentframe().f_back
        filename = os.path.basename(frame.f_code.co_filename)
        line_no = frame.f_lineno
        caller_info = f"{COLORS['PURPLE']}{filename}:{line_no}{COLORS['END']} "
    
    # Format the level
    level_str = f"{level_colors.get(level, COLORS['WHITE'])}{level:7}{COLORS['END']}"
    
    # Format the message (handle non-string messages)
    if not isinstance(message, str):
        message = str(message)
    
    # Print the formatted log
    print(f"{COLORS['BOLD']}[{timestamp}]{COLORS['END']} {level_str} {caller_info}{message}")

def log_test(test_case:TestCase, query_expected_answer):
    """
    Log the test parameters.
    """
    
    try:
        log("\n---------------------------------------------------------")
        #log(f"Running test for LLM: {test_case.llm_name}")
        #log(f"Embedding model: {test_case.embedding_model_name}")
        #log(f"System message: {test_case.system_message}")
        log(f"Query: {query_expected_answer['query']}")
        log(f"Exptected answer: {query_expected_answer['answer']}")
        #log(f"Chunk size: {test_case.chunk_size}")
        #log(f"Chunk overlap: {test_case.chunk_overlap}")
        #log(f"Similar vector count: {test_case.similar_vector_count}")
        #log(f"Options: {[str(option) for option in test_case.options]}")
        log("---------------------------------------------------------\n")
    except Exception as e:
        log(f"Error logging test: {e}")
