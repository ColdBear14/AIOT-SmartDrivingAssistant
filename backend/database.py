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
  def ensure_collection(func):
    def wrapper(self, collection_name, document):
      if collection_name not in self.db.list_collection_names():
          self.db.create_collection(
              collection_name,
              timeseries={"timeField": "timestamp", "granularity": "seconds"}
          )
          print(f"Collection '{collection_name}' created successfully.")
      return func(self, collection_name, document)
    return wrapper  
  @ensure_collection
  def push_to_db(self,collection_name,document):
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