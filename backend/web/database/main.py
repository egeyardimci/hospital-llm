# db.py
import os
from threading import Lock
from dotenv import load_dotenv
from pymongo import MongoClient
class MongoDBClient:
    _instance = None
    _lock = Lock()
    client: MongoClient = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self.client is None:
          load_dotenv()
          MONGO_DB_URI = os.getenv('MONGO_DB_URI')
          self.client = MongoClient(MONGO_DB_URI)
            
    def get_client(self):
        return self.client
    
    def get_hospital_db(self):
        return self.client['hospital']
    
    def get_results_collection(self):
        db = self.get_hospital_db()
        return db['results']
    
    def get_queries_collection(self):
        db = self.get_hospital_db()
        return db['queries']
    
    def get_qa_batches_collection(self):
        db = self.get_hospital_db()
        return db['qa_batches']
    
    def get_test_cases_collection(self):
        db = self.get_hospital_db()
        return db['test_cases']
    
    def get_system_prompts_collection(self):
        db = self.get_hospital_db()
        return db['system_prompts']

# Global instance
GLOBAL_MONGO_DB_CLIENT = MongoDBClient()