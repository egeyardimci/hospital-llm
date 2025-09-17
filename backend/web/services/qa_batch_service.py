from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT
from backend.web.database.utils import from_mongo
from bson import ObjectId

class QABatchService:
    @staticmethod
    def get_qa_batches():
        """
        Get QA pairs from the database.
        
        Returns:
            List of QA pairs
        """
        collection = GLOBAL_MONGO_DB_CLIENT.get_qa_batches_collection()
        documents = list(collection.find())
        return from_mongo(documents)

    @staticmethod
    def add_qa_batch(title, description):
        collection = GLOBAL_MONGO_DB_CLIENT.get_qa_batches_collection()
        result = collection.insert_one({"title": title, "description": description})
        return str(result.inserted_id)
    
    @staticmethod
    def delete_qa_batch(_id):
        collection = GLOBAL_MONGO_DB_CLIENT.get_qa_batches_collection()
        collection.delete_one({"_id": ObjectId(_id)})

    @staticmethod
    def update_qa_batch(_id, title, description):
        collection = GLOBAL_MONGO_DB_CLIENT.get_qa_batches_collection()
        collection.update_one({"_id": ObjectId(_id)}, {"$set": {"title": title, "description": description}})