import os
from pymongo import MongoClient
from dotenv import load_dotenv
from gridfs import GridFS
from app import app

load_dotenv()
database_name = os.environ['MONGO_DB_NAME']
try:
    mongo_uri = os.environ['MONGO_URI']
    client = MongoClient(mongo_uri)
except KeyError as err:
    print("Add MONGO_URI to .env file")

db = client[database_name]
file_storage = GridFS(db, collection="tarballs")
