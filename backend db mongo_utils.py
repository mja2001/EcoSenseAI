from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os

load_dotenv()

def get_collection():
    try:
        client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Test connection
        return client["ecosense_db"]["sensor_data"]
    except ConnectionFailure:
        raise Exception("MongoDB connection failed")