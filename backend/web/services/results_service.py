from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT
from backend.web.database.utils import from_mongo

class ResultsService:
    @staticmethod
    def get_test_results():
      """
      Read and return test results from the JSON file.
      
      Returns:
          Dictionary containing the test results data
          
      Raises:
          Exception: If there's an error reading the JSON file
      """
      collection = GLOBAL_MONGO_DB_CLIENT.get_results_collection()
      documents = list(collection.find())
      return from_mongo(documents)