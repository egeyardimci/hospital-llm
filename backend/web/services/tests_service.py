from backend.ai.vectordb.utils import load_vectordb
from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT
from backend.web.database.utils import from_mongo
from bson import ObjectId
from backend.ai.testing.io_utils import load_test_case_by_test_id, load_queries_expected_answers_batch_by_id
from backend.ai.testing.main import run_test_case_by_test_id
from backend.utils.logger2 import get_logger

logger = get_logger()

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
        
    @staticmethod
    def run_test_service(test_id):
        """
        Run a test case.

        Args:
            test_id: ID of the test case to be run

        Returns:
            dict: Result with success status and message

        Raises:
            Exception: If test execution fails
        """
        logger.info(f"Starting test execution for test_id: {test_id}")

        try:
            run_test_case_by_test_id(test_id)
            logger.info(f"Test case {test_id} completed successfully")
            return {"success": True, "message": f"Test {test_id} completed successfully"}
        except Exception as e:
            logger.error(f"Test case {test_id} failed: {e}", exc_info=True)
            # Re-raise so the API layer can handle it appropriately
            raise Exception(f"Test execution failed for test_id {test_id}: {e}") from e
