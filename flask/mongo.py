import os
from pymongo import MongoClient
from dotenv import load_dotenv
from gridfs import GridFS

load_dotenv()

try:
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
except KeyError as err:
    print("Add MONGO_URI to .env file")

db = client.fpmregistry
file_storage = GridFS(db, collection="tarballs")
