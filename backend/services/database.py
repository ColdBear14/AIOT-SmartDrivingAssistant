from motor.motor_asyncio import AsyncIOMotorClient 
from datetime import datetime
from config import config

from helpers.custom_logger import CustomLogger

#MongoDB setup
client = AsyncIOMotorClient(config.mongo_url)

class Database:
    _instance = None

    def __new__(cls, db_name=config.db_name):
        if (db_name == None):
          if cls._instance is None:
              cls._instance = super(Database, cls).__new__(cls)
              cls._instance._init_database()
          return cls._instance
        else:
            CustomLogger().get_logger().info("Create test database.")
            return super(Database, cls).__new__(cls)

    def _init_database(self, db_name=config.db_name):
        if self.__initialized:
            return
        self.client = client
        self.db = self.client[db_name]
        self.collections = set()
        self.__initialized = True

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
            CustomLogger().get_logger().info(f"Ensured time series collection: {collection_name}")

    async def push_to_db(self, collection_name, document):
        '''Insert a document to a collection'''
        await self._ensure_time_series_collection(collection_name)

        document['timestamp'] = datetime.now()

        result = await self.db[collection_name].insert_one(document)

        # print(f'Store in MongoDB: {result}')
        CustomLogger().get_logger().info(f'Store in MongoDB: {result}')


if __name__ == '__main__':
  db = Database('test')
  document = {
    'a': 'a',
    'b': 'b'
  }
  db.push_to_db('collection',document)