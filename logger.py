from datetime import datetime
from typing import Any
import inspect
import os

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

# Example usage
if __name__ == "__main__":
    log("Starting application...", "INFO")
    log("Debug message here", "DEBUG")
    log("Warning! Something looks wrong", "WARNING")
    log("Error occurred!", "ERROR")
    log({"key": "value", "numbers": [1,2,3]})  # Works with non-string types too