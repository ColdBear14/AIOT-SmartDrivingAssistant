from pymongo import MongoClient
from config import config
import re


client = MongoClient(config.mongo_url)
db = client[config.db_name]
ttl = 300

def create_user_collection():
    """Creates the 'user' collection for storing user credentials."""
    collection_name = "user"
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        db[collection_name].create_index("username", unique=True)  # Ensure unique usernames
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")

def create_userconfig_collection():
    """Creates the 'userconfig' collection for storing user preferences."""
    collection_name = "userconfig"
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        db[collection_name].create_index("uid", unique=True)  # Ensure unique UID
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")  

def create_time_series_collection(collection_name,ttl=300):
    if collection_name not in db.list_collection_names():
        remake = input("Do you want to remake the collection?")
        if remake.lower().startswith('yes'):
            db[collection_name].drop()
            print(f"Dropped existing collection '{collection_name}'")
        
        db.create_collection(
            collection_name,
            timeseries={
                "timeField": "timestamp",
                "metaField": "metadata",
                "granularity": "seconds"
            },
            expireAfterSeconds=ttl  # 5min TTL 
        )
        print(f"Time-Series Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")
def init_db():
    global db
    is_drop = input("Do you want to recreate the database?(Y/N)")
    if is_drop.lower().startswith('y'):
        client.drop_database(config.db_name)
        db = client[config.db_name]
        print(f"Database '{config.db_name}'recreated")
    create_user_collection()
    create_userconfig_collection()
    create_time_series_collection('environment_sensor')
    create_time_series_collection('camera')
    print("Database setup complete")
if __name__ == '__main__':
    
        
