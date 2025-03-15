from pymongo import MongoClient
import requests
import json
from datetime import datetime
from utils import Config
# AdaFruit Credential
config = Config()
#MongoDB setup
class Database():
  def __init__(self,db_name = config.db_name):
    self.client = MongoClient(config.mongo_url)
    self.db = self.client[db_name]
    self.collections = set(self.db.list_collection_names())
    
  def ensure_time_series_collection(self, collection_name):
    """Ensure the collection exists and is a time-series collection."""
    if collection_name not in self.collections:
        self.db.create_collection(
            collection_name,
            timeseries={"timeField": "timestamp", "granularity": "seconds"}
        )
        self.db[collection_name].create_index("timestamp", expireAfterSeconds=86400)  # Auto-delete after 1 day
        self.collections.add(collection_name)  # Update internal cache
        print(f"Collection '{collection_name}' created successfully.")
  
  def push_to_db(self,collection_name,document):
    self.ensure_time_series_collection(collection_name)
    document['timestamp'] = datetime.now()
    self.db[collection_name].insert_one(document)
    print(f'Store in MongoDB: {document}')


if __name__ == '__main__':
  db = Database('test')
  document = {
    'a': 'a',
    'b': 'b'
  }
  db.push_to_db('collection',document)