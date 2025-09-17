from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT
from backend.web.database.utils import from_mongo
from bson import ObjectId

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

    @staticmethod
    def add_qa_pair(query, answer, batch_id=None):
        collection = GLOBAL_MONGO_DB_CLIENT.get_queries_collection()
        result = collection.insert_one({"query": query, "answer": answer, "batch_id": batch_id})
        return str(result.inserted_id)
    
    @staticmethod
    def delete_qa_pair(_id):
        collection = GLOBAL_MONGO_DB_CLIENT.get_queries_collection()
        collection.delete_one({"_id": ObjectId(_id)})

    @staticmethod
    def update_qa_pair(_id, query, answer, batch_id):
        collection = GLOBAL_MONGO_DB_CLIENT.get_queries_collection()
        collection.update_one({"_id": ObjectId(_id)}, {"$set": {"query": query, "answer": answer, "batch_id": batch_id}})