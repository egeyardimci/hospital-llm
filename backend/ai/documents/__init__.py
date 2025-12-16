from pyparsing import Dict
from .excel_parser import ExcelParser
from .word_parser import WordParser
from .db_manager import DocumentDBManager
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DocumentLoader:
    """Load Excel/Doc files into database"""
    
    def __init__(self, db_path: str = "backend/ai/documents/storage/documents.db", 
                 format_type: str = 'markdown'):
        """
        Args:
            db_path: Database path
            format_type: 'markdown' (recommended for Excel), 'string', or 'csv'
        """
        self.excel_parser = ExcelParser()
        self.word_parser = WordParser()
        self.db_manager = DocumentDBManager(db_path)
        self.format_type = format_type
    
    def load_excel_file(self, file_path: str) -> bool:
        """Load single Excel file into database"""
        try:
            file_info = self.excel_parser.get_file_info(file_path)
            logger.info(f"Loading Excel: {file_info['file_name']}")
            
            sheets_data = self.excel_parser.parse_excel(file_path, self.format_type)
            
            for sheet_name, content, content_format in sheets_data:
                self.db_manager.insert_document(
                    file_name=file_info['file_name'],
                    file_type=file_info['file_type'],
                    sheet_name=sheet_name,
                    content=content,
                    content_format=content_format,
                    file_size=file_info['file_size']
                )
            
            logger.info(f"Successfully loaded {file_info['file_name']} ({len(sheets_data)} sheets)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            return False
    
    def load_word_file(self, file_path: str) -> bool:
        """Load single Word file into database"""
        try:
            file_info = self.word_parser.get_file_info(file_path)
            logger.info(f"Loading Word: {file_info['file_name']}")
            
            content, content_format = self.word_parser.parse_word(file_path)
            
            self.db_manager.insert_document(
                file_name=file_info['file_name'],
                file_type=file_info['file_type'],
                sheet_name='main',  # Word files don't have sheets
                content=content,
                content_format=content_format,
                file_size=file_info['file_size']
            )
            
            logger.info(f"Successfully loaded {file_info['file_name']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            return False
    
    def load_file(self, file_path: str) -> bool:
        """Load any supported file (Excel or Word)"""
        path = Path(file_path)
        
        if path.suffix in ['.xlsx', '.xls']:
            return self.load_excel_file(file_path)
        elif path.suffix in ['.docx']:
            return self.load_word_file(file_path)
        else:
            logger.warning(f"Unsupported file type: {path.suffix}")
            return False
    
    def load_directory(self, directory_path: str, 
                      extensions: list = ['.xlsx', '.xls', '.docx']) -> Dict:
        """Load all supported files from directory"""
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory not found: {directory_path}")
            return {'success': 0, 'failed': 0, 'files': []}
        
        results = {'success': 0, 'failed': 0, 'files': []}
        
        for ext in extensions:
            for file_path in directory.glob(f"*{ext}"):
                logger.info(f"\n{'='*50}")
                success = self.load_file(str(file_path))
                
                if success:
                    results['success'] += 1
                    results['files'].append(str(file_path))
                else:
                    results['failed'] += 1
        
        logger.info(f"\n{'='*50}")
        logger.info(f"Summary: {results['success']} success, {results['failed']} failed")
        return results
    
    def search_and_format_for_prompt(self, query: str) -> str:
        """Search database and format content for LLM prompt"""
        results = self.db_manager.search_by_filename(query)
        
        if not results:
            return ""
        
        prompt_addition = "\n\n## Relevant Documents:\n"
        
        for doc in results:
            prompt_addition += f"\n### {doc['file_name']}"
            if doc['sheet_name'] and doc['sheet_name'] != 'main':
                prompt_addition += f" - Sheet: {doc['sheet_name']}"
            prompt_addition += f"\n\n{doc['content']}\n"
        
        return prompt_addition
    
    def get_stats(self):
        """Get database statistics"""
        return self.db_manager.get_stats()

# Export
__all__ = ['DocumentLoader', 'ExcelParser', 'WordParser', 'DocumentDBManager']