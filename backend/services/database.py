import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.custom_logger import CustomLogger

from motor.motor_asyncio import AsyncIOMotorClient 
from datetime import datetime

#MongoDB setup
# client = AsyncIOMotorClient(config.mongo_url)

class Database:
    _instance = None

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

        self.client = AsyncIOMotorClient(config["mongo_url"])
        if test_mode:
            CustomLogger().get_logger().info("Database: Test mode.")
            self.db = self.client['test']
        else:
            self.db = self.client[config["db_name"]]
        self.collections = set()

    async def _ensure_time_series_collection(self, collection_name):
        """Ensure the collection exists and is a time-series collection."""
        if collection_name not in self.collections:
            existing_collections = await self.db.list_collection_names()

            if collection_name not in existing_collections:
                await self.db.create_collection(
                    collection_name,
                    timeseries={"timeField": "timestamp", "granularity": "seconds"}
                )
                # print(f"Collection '{collection_name}' created successfully.")
                CustomLogger().get_logger().info(f"Collection '{collection_name}' created successfully.")

            self.collections.add(collection_name)  # Update internal cache
            CustomLogger().get_logger().info(f"Successfully ensure time series collection: {collection_name}")

    async def push_to_db(self, collection_name, document):
        '''Insert a document to a collection'''
        await self._ensure_time_series_collection(collection_name)

        document['timestamp'] = datetime.now()

        result = await self.db[collection_name].insert_one(document)

        # print(f'Store in MongoDB: {result}')
        CustomLogger().get_logger().info(f'Store in MongoDB: {result}')


if __name__ == '__main__':
  CustomLogger().get_logger().info("Database: __main__")
  db = Database(None, True)
#   document = {
#     'a': 'a',
#     'b': 'b'
#   }
#   db.push_to_db('collection',document)