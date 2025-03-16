from pymongo import MongoClient
import requests
import json
from datetime import datetime
from config import config
#MongoDB setup
client = MongoClient(config.mongo_url)

class Database():
  def __init__(self,db_name = config.db_name,expire_time=300):
    self._client = client
    self._db = self._client[db_name]
    self._expire_time = expire_time
    self.collections = set(self._db.list_collection_names())
  
  
  def ensure_time_series_collection(self, collection_name):
    """Ensure the collection exists and is a time-series collection."""
    if collection_name not in self.collections:
      self._db.create_collection(
          collection_name,
          timeseries={
            "timeField": "timestamp", 
            "metaField": "metadata",
            "granularity": "seconds",
            },
          expireAfterSeconds= self._expire_time
      )
      
      self.collections.add(collection_name)  # Update internal cache
      print(f"Collection '{collection_name}' created successfully.")
    sensor_collection = self.get_sensor_collection()
    index_info = sensor_collection.index_information()
    if not 'timestamp_1' in index_info.keys():
      sensor_collection.create_index('timestamp',expireAfterSeconds=self._expire_time)      
      
  def insert_collection(self,collection_name,document):
    result = self._db[collection_name].insert_one(document)
    print(f'Store in MongoDB: {result}')
     
  def insert_ts_collection(self,collection_name,document):
    self.ensure_time_series_collection(collection_name)
    document['timestamp'] = datetime.now()
    
    self.insert_collection(collection_name,document)
    
  def get_collection(self,name: str):
    '''Return MongoDB collections'''
    return self._client[config.db_name][name]
  
  def get_sensor_collection(self):
    return self.get_collection('enviroment_sensor')
    


if __name__ == '__main__':
  db = Database('test',expire_time=1)
  document = {
    'timestamp': datetime.now(),
    'metadata': {
      'val' : 8
    }
  }
  db.insert_ts_collection('collection',document)