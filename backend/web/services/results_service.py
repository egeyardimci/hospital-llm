from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT

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
      documents = list(collection.find({}, {'_id': 0}))  # Exclude the MongoDB _id field
      return documents