import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelParser:
    """Parse Excel and XLS files"""
    
    @staticmethod
    def parse_excel(file_path: str, format_type: str = 'markdown') -> List[Tuple[str, str, str]]:
        """
        Parse Excel file and return (sheet_name, content, format)
        
        Args:
            file_path: Path to Excel file
            format_type: 'markdown' (best for LLM), 'string', or 'csv'
        
        Returns:
            List of (sheet_name, content, format_type)
        """
        results = []
        file_name = Path(file_path).name
        
        try:
            # Read Excel file
            xls = pd.ExcelFile(file_path)
            logger.info(f"Reading {file_name} - Found {len(xls.sheet_names)} sheets")
            
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Clean empty rows and columns
                df = df.dropna(how='all')
                df = df.dropna(axis=1, how='all')
                
                # Format based on type
                if format_type == 'markdown':
                    # Markdown table format (best for LLM)
                    content = df.to_markdown(index=False)
                elif format_type == 'csv':
                    # CSV format (compact)
                    content = df.to_csv(index=False)
                else:
                    # String format (readable)
                    content = df.to_string(index=False, max_rows=None)
                
                results.append((sheet_name, content, format_type))
                logger.info(f"  ✓ Sheet: {sheet_name} - {len(df)} rows, {len(df.columns)} columns")
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to parse {file_name}: {e}")
            raise
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict:
        """Get file metadata"""
        path = Path(file_path)
        return {
            'file_name': path.name,
            'file_type': path.suffix,
            'file_size': path.stat().st_size,
            'exists': path.exists()
        }