from motor.motor_asyncio import AsyncIOMotorClient 
import requests
import json
from datetime import datetime
from config import config
from utils import client
import asyncio

#MongoDB setup
client = AsyncIOMotorClient(config.mongo_url)

class Database():
  def __init__(self,db_name = config.db_name):
    self.client = client
    self.db = self.client[db_name]
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
        
        print(f"Collection '{collection_name}' created successfully.")
        
      self.collections.add(collection_name)  # Update internal cache

  
  async def push_to_db(self,collection_name,document):
    '''Insert a document to a collection'''
    await self._ensure_time_series_collection(collection_name)
    
    document['timestamp'] = datetime.now()
    
    result = await self.db[collection_name].insert_one(document)
    
    print(f'Store in MongoDB: {result}')


if __name__ == '__main__':
  db = Database('test')
  document = {
    'a': 'a',
    'b': 'b'
  }
  db.push_to_db('collection',document)