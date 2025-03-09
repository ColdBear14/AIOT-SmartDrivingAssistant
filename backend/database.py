from pymongo import MongoClient
import requests
from datetime import datetime
from backend.utils import Config
# AdaFruit Credential
config = Config()
#MongoDB setup
class Database():
  def __init__(self):
    self.client = MongoClient(config.mongo_url)
    self.db = self.client['va_database']
    self.collections = ['lux','temp','humid']
  def push_to_db(self,collection_name,document):
    self.db[collection_name].insert_one(document)
    print(f'Store in MongoDB: {document}')
