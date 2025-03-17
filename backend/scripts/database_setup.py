import sys
import os

# Add 'backend/' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymongo import MongoClient
from config import config
import re


client = MongoClient(config.mongo_url)
TTL = 300

def create_user_collection(db):
    """Creates the 'user' collection for storing user credentials."""
    collection_name = "user"
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        db[collection_name].create_index("username", unique=True)  # Ensure unique usernames
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")

def create_userconfig_collection(db):
    """Creates the 'userconfig' collection for storing user preferences."""
    collection_name = "userconfig"
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        db[collection_name].create_index("uid", unique=True)  # Ensure unique UID
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")  

def create_time_series_collection(db,collection_name, ttl=TTL):
    """Creates a time-series collection with TTL, ensuring safe deletion logic."""
    
    # Check if the collection exists before dropping
    if collection_name in db.list_collection_names():
        remake = input(f"Collection '{collection_name}' exists. Do you want to remake it? (y/N): ")
        if remake.lower().startswith('y'):
            db[collection_name].drop()
            print(f"Dropped existing collection '{collection_name}'")

    # Create the time-series collection with correct parameters
    db.create_collection(
        collection_name,
        timeseries={
            "timeField": "timestamp",
            "metaField": "metadata",
            "granularity": "seconds"
        },
        expireAfterSeconds=ttl  # Set TTL
    )

    print(f"✅ Time-Series Collection '{collection_name}' created successfully.")
    
    
def init_db(db_name=config.db_name):
    if db_name in client.list_database_names():
        is_drop = input("Do you want to recreate the database?(Y/N)")
        if is_drop.lower().startswith('y'):
            client.drop_database(db_name)
            print(f"Database '{db_name}'recreated")
    db = client[db_name]    
    create_user_collection(db)
    create_userconfig_collection(db)
    create_time_series_collection(db,'environment_sensor')
    create_time_series_collection(db,'camera')
    print("Database setup complete")
if __name__ == '__main__':
    init_db()
        
