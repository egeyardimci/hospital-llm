from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT
from backend.web.database.utils import from_mongo

class TestService:
    @staticmethod
    def get_tests():
        """
        Get test cases from the database.

        Returns:
            List of test cases
        """
        collection = GLOBAL_MONGO_DB_CLIENT.get_test_cases_collection()
        documents = list(collection.find())
        return from_mongo(documents)