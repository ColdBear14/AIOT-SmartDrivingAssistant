from utils.custom_logger import CustomLogger

from pymongo import MongoClient
from datetime import datetime
import gridfs

class Database:
    FIELD_MONGO_URL = "mongo_url"
    FIELD_DB_NAME = "db_name"
    FIELD_USER_COLLECTION = "user"
    FIELD_ENV_SENSOR_COLLECTION = "environment_sensor"
    FIELD_USER_CONFIG_COLLECTION = "user_config"
    _instance = None
    _cache_data = {}

    def __new__(cls, config: dict=None, test_mode: bool=False):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_database(config, test_mode)
        return cls._instance

    def _init_database(self, config: dict=None, test_mode: bool=False):
        if config == None or not config.contains(self.FIELD_MONGO_URL) or not config.contains(self.FIELD_DB_NAME):
            from dotenv import load_dotenv
            import os

            load_dotenv()
            config = {
                self.FIELD_MONGO_URL: os.getenv("MONGODB_URL"),
                self.FIELD_DB_NAME: os.getenv("MONGODB_DB_NAME")
            }
            CustomLogger().get_logger().info("Database's config: " + str(config))

        self.client = MongoClient(config[self.FIELD_MONGO_URL])
        if test_mode:
            CustomLogger().get_logger().info("Database: Test mode.")
            self.db = self.client['test']
        else:
            self.db = self.client[config[self.FIELD_DB_NAME]]
            self.fs = gridfs.GridFS(self.db, os.getenv("MONGOBD_AVATAR_COL"))

    def _add_doc_with_timestamp(self, collection_name: str=None, document: dict=None):
        '''Add new document to collection with timestamp'''
        if collection_name is None or document is None:
            return None
        
        document['timestamp'] = datetime.now()

        result = self.db[collection_name].insert_one(document)

        CustomLogger().get_logger().info(f'Added document with ID: {result.inserted_id}')
        return result.inserted_id
    
# User region
    def get_user_collection(self):
        return self.db.get_collection(self.FIELD_USER_COLLECTION)
    
    def get_user_config_collection(self):
        return self.db.get_collection(self.FIELD_USER_CONFIG_COLLECTION)
# End user region
    
# IOT region
    def get_env_sensor_collection(self):
        return self.db.get_collection(self.FIELD_ENV_SENSOR_COLLECTION)
# End IOT region

if __name__ == '__main__':
    def test():
        CustomLogger().get_logger().info("Database: Test mode.")

        document = {
            'key': 'value'
        }
        result = Database(None, True)._instance._add_doc_with_timestamp('test_collection', document)

    test()