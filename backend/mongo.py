import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
from gridfs import GridFS
from app import app
from flask import jsonify
import logging

load_dotenv()
database_name = os.environ["MONGO_DB_NAME"]
try:
    mongo_uri = os.environ["MONGO_URI"]
    mongo_username = os.environ["MONGO_USER_NAME"]
    mongo_password = os.environ["MONGO_PASSWORD"]
    client = MongoClient(mongo_uri)
except KeyError as err:
    print("Add MONGO_URI to .env file")

db = client[database_name]
file_storage = GridFS(db, collection="tarballs")

# Create a collection to store the logs
class MongoDBHandler(logging.Handler):
    def __init__(self, collection):
        super().__init__()
        self.collection = collection

    def emit(self, record):
        log_document = {
            "timestamp": datetime.utcnow(),
            "level": record.levelname,
            "message": self.format(record)
        }
        self.collection.insert_one(log_document)

# Create the MongoDB logging handler
mongo_handler = MongoDBHandler(collection=db.logs)
mongo_handler.setLevel(logging.DEBUG)  # Set the handler's log level to the lowest (DEBUG)

# Configure the root logger with the MongoDB handler
logging.root.addHandler(mongo_handler)

@app.route("/registry/archives", methods=["GET"])
def clone():
    folder_path = "static"
    file_list = os.listdir(folder_path)
    return jsonify(
        {"message": "Successfully Fetched Archives", "archives": file_list, "code": 200}
    )
