import sqlite3
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DocumentDBManager:
    """Manage document storage in SQLite database"""
    
    def __init__(self, db_path: str = "backend/ai/documents/storage/documents.db"):
        self.db_path = db_path
        self._ensure_db_directory()
        self.setup_database()
    
    def _ensure_db_directory(self):
        """Create storage directory if not exists"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def setup_database(self):
        """Create tables if not exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_contents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            sheet_name TEXT,
            content TEXT NOT NULL,
            content_format TEXT DEFAULT 'string',
            file_size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(file_name, sheet_name)
        )
        ''')
        
        # Create index for faster search
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_file_name 
        ON document_contents(file_name)
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")
    
    def insert_document(self, file_name: str, file_type: str, 
                       sheet_name: str, content: str, 
                       content_format: str = 'string',
                       file_size: int = 0):
        """Insert or update document content"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO document_contents 
                (file_name, file_type, sheet_name, content, content_format, file_size, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(file_name, sheet_name) 
                DO UPDATE SET 
                    content = excluded.content,
                    updated_at = excluded.updated_at
            ''', (file_name, file_type, sheet_name, content, 
                  content_format, file_size, datetime.now()))
            
            conn.commit()
            logger.info(f"Inserted/Updated: {file_name} - {sheet_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to insert {file_name}: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def search_by_filename(self, file_name_query: str) -> List[Dict]:
        """Search documents by filename (partial match)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT file_name, sheet_name, content, content_format, created_at
            FROM document_contents 
            WHERE file_name LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{file_name_query}%',))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'file_name': row[0],
                'sheet_name': row[1],
                'content': row[2],
                'content_format': row[3],
                'created_at': row[4]
            })
        
        conn.close()
        return results
    
    def get_all_filenames(self) -> List[str]:
        """Get list of all stored filenames"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT file_name FROM document_contents')
        filenames = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return filenames
    
    def delete_document(self, file_name: str) -> bool:
        """Delete all sheets of a document"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM document_contents WHERE file_name = ?', (file_name,))
            conn.commit()
            logger.info(f"✓ Deleted: {file_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete {file_name}: {e}")
            return False
        finally:
            conn.close()
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(DISTINCT file_name) FROM document_contents')
        file_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM document_contents')
        sheet_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(LENGTH(content)) FROM document_contents')
        total_size = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_files': file_count,
            'total_sheets': sheet_count,
            'total_content_size': total_size,
            'db_path': self.db_path
        }