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
            
  def insert_collection(self,collection_name,document):
    result = self._db[collection_name].insert_one(document)
    print(f'Store in MongoDB: {result}')
  def find_sensor_data(self,uid,sensor_type,amt):
    return list(self.get_sensor_collection().find({'uid': uid,'sensor_type': sensor_type}).limit(amt))
  
  def get_collection(self,name: str):
    '''Return MongoDB collections'''
    return self._client[config.db_name][name]
  
  def get_sensor_collection(self):
    return self.get_collection('enviroment_sensor')
  
  def get_user_collection(self):
    return self.get_collection('user')
  
  def get_user_config(self):
    return self.get_collection('user_config')
    
db = Database()

if __name__ == '__main__':
  db = Database('test',expire_time=1)
  document = {
    'timestamp': datetime.now(),
    'metadata': {
      'val' : 8
    }
  }
  db.insert_ts_collection('collection',document)