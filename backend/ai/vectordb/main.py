# db.py
from threading import Lock
from backend.ai.vectordb.utils import load_vectordb
from langchain_chroma import Chroma

import os
os.environ['ALLOW_RESET'] = 'TRUE'

class VectorDB:
    _instance = None
    _lock = Lock()
    db: Chroma = None
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_db(self):
        return self.db
    
    def get_db_name(self):
        return self.name

    def load_db(self, embedding_model, chunk_size, chunk_overlap):
        self.close()
        self.db = load_vectordb(embedding_model, chunk_size, chunk_overlap)
        self.name = f"{embedding_model}_{chunk_size}_{chunk_overlap}"

    def close(self):
        if hasattr(self, 'db'):
            if hasattr(self.db, '_client'):
                self.db._client.reset()  # Reset the client

            # Clear references
            self.db = None

            # Force garbage collection
            import gc
            gc.collect()

# Global instance
GLOBAL_VECTOR_DB = VectorDB()