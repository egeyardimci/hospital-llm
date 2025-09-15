from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT
from backend.web.database.utils import from_mongo
from bson import ObjectId

class SystemPromptsService:
    @staticmethod
    def get_system_prompts():
        """
        Get system prompts from the database.
        
        Returns:
            List of system prompts
        """
        collection = GLOBAL_MONGO_DB_CLIENT.get_system_prompts_collection()
        documents = list(collection.find())
        return from_mongo(documents)

    @staticmethod
    def add_system_prompt(title, content):
        collection = GLOBAL_MONGO_DB_CLIENT.get_system_prompts_collection()
        result = collection.insert_one({"title": title, "content": content})
        return str(result.inserted_id)
    
    @staticmethod
    def delete_system_prompt(_id):
        collection = GLOBAL_MONGO_DB_CLIENT.get_system_prompts_collection()
        collection.delete_one({"_id": ObjectId(_id)})

    @staticmethod
    def update_system_prompt(_id, title, content):
        collection = GLOBAL_MONGO_DB_CLIENT.get_system_prompts_collection()
        collection.update_one({"_id": ObjectId(_id)}, {"$set": {"title": title, "content": content}})