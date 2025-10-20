from backend.web.database.main import GLOBAL_MONGO_DB_CLIENT
from backend.web.database.utils import from_mongo

class RunsService:
    @staticmethod
    def get_test_runs():
      collection = GLOBAL_MONGO_DB_CLIENT.get_runs_collection()
      documents = list(collection.find().sort("time_stamp", -1))
      return from_mongo(documents)