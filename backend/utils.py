from pymongo import MongoClient
from config import config

client = MongoClient(config.mongo_url)
db = client[config.db_name]

def get_collection(name: str):
    '''Return MongoDB collections'''
    return db[name]
