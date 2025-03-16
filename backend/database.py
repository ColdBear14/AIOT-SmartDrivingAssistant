from pymongo import MongoClient
import requests
import json
from datetime import datetime
from config import config
from utils import client
#MongoDB setup
client = MongoClient(config.mongo_url)
db = client[config.db_name]

class Database():
  def __init__(self,db_name = config.db_name,expire_time=300):
    self._client = client
    self._db = self._client[db_name]
    self._expire_time = expire_time
    self.collections = set(self._db.list_collection_names())
  
  def _set_ttl(self,collection_name,index):
    db[collection_name].create_index(index,expireAfterSeconds=self._expire_time)
  
  def ensure_time_series_collection(self, collection_name):
    """Ensure the collection exists and is a time-series collection."""
    if collection_name not in self.collections:
      self._db.create_collection(
          collection_name,
          timeseries={"timeField": "timestamp", "granularity": "seconds"}
      )
      
      self.collections.add(collection_name)  # Update internal cache
      print(f"Collection '{collection_name}' created successfully.")
      
      self._set_ttl(collection_name,"timestamp")
      
  def insert_collection(self,collection_name,document):
    self._db[collection_name].insert_one(document)
    print(f'Store in MongoDB: {document}')
     
  def insert_ts_collection(self,collection_name,document):
    self.ensure_time_series_collection(collection_name)
    document['timestamp'] = datetime.now()
    
    self.insert_collection(collection_name,document)
    


if __name__ == '__main__':
  db = Database('test')
  document = {
    'a': 'a',
    'b': 'b'
  }
  db.insert_ts_collection('collection',document)