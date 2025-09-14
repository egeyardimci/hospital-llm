from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT
from backend.web.database.utils import from_mongo

class QAService:
    @staticmethod
    def get_qa_pairs():
        """
        Get QA pairs from the database.
        
        Returns:
            List of QA pairs
        """
        collection = GLOBAL_MONGO_DB_CLIENT.get_queries_collection()
        documents = list(collection.find())
        return from_mongo(documents)