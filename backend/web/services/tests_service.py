from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT
from backend.web.database.utils import from_mongo
from bson import ObjectId

class TestService:
    @staticmethod
    def get_tests():
        """
        Get test cases from the database.

        Returns:
            List of test cases
        """
        collection = GLOBAL_MONGO_DB_CLIENT.get_test_cases_collection()
        documents = list(collection.find().sort("test_id", 1)) 
        return from_mongo(documents)
    
    @staticmethod
    def add_test(test_data):
        """
        Add a new test case to the database.

        Args:
            test_data: Data of the test case to be added

        Returns:
            The inserted test case
        """
        collection = GLOBAL_MONGO_DB_CLIENT.get_test_cases_collection()
        result = collection.insert_one(test_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update_test(_id, test_data):
        """
        Update an existing test case in the database.

        Args:
            object_id: ID of the test case to be updated
            test_data: Updated data of the test case
        """
        collection = GLOBAL_MONGO_DB_CLIENT.get_test_cases_collection()
        collection.update_one({"_id": ObjectId(_id)}, {"$set": test_data})

    @staticmethod
    def delete_test(_id):
        """
        Delete a test case from the database.

        Args:
            object_id: ID of the test case to be deleted
        """
        collection = GLOBAL_MONGO_DB_CLIENT.get_test_cases_collection()
        collection.delete_one({"_id": ObjectId(_id)})