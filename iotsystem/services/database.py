import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.custom_logger import CustomLogger

from pymongo import MongoClient
from datetime import datetime

class Database:
    _instance = None
    _cache_data = {}

    def __new__(cls, config=None, test_mode=False):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_database(config, test_mode)
        return cls._instance

    def _init_database(self, config, test_mode=False):
        if config == None or not config.contains("mongo_url") or not config.contains("db_name"):
            from dotenv import load_dotenv
            import os

            load_dotenv()
            config = {
                "mongo_url": os.getenv("MONGODB_URL"),
                "db_name": os.getenv("MONGODB_DB_NAME")
            }
            CustomLogger().get_logger().info("Database's config: " + str(config))

        self.client = MongoClient(config["mongo_url"])
        CustomLogger().get_logger().info(f"Database: Connected with client {self.client}.")
        if test_mode:
            CustomLogger().get_logger().info("Database: Test mode.")
            self.db = self.client['test']
        else:
            self.db = self.client[config["db_name"]]
            CustomLogger().get_logger().info(f"Database: Connected with database {self.db}.")
        self.collections = set()

    def _add_doc_with_timestamp(self, collection_name=None, document=None):
        '''Add new document to collection with timestamp'''
        if collection_name is None or document is None:
            return None
        
        document['timestamp'] = datetime.now()

        result = self.db[collection_name].insert_one(document)

        CustomLogger().get_logger().info(f'Added document with ID: {result.inserted_id}')
        return result.inserted_id
    
    def get_sensor_collection(self):
        return self.db.get_collection('environment_sensor')
    
    def get_sensor_doc_by_id(self, id):
        return self.get_sensor_collection().find_one({'_id': id})
    
    def get_services_status_collection(self):
        return self.db.get_collection('services_status')

# Device region
    def get_device_collection(self):
        return self.db.get_collection('device_control')
# End device region

if __name__ == '__main__':
    def test():
        CustomLogger().get_logger().info("Database: Test mode.")

        document = {
            'key': 'value'
        }
        result = Database(None, True)._instance._add_doc_with_timestamp('test_collection', document)

    test()