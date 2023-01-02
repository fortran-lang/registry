import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

try:
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
except KeyError as err:
    print("Add MONGO_URI to .env file")

db = client.fpmregistry
