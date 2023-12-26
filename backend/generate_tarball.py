import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
from gridfs import GridFS
from app import app
from flask import jsonify
import subprocess

load_dotenv()
database_name = os.environ["MONGO_DB_NAME"]
try:
    mongo_uri = os.environ["MONGO_URI"]
    mongo_username = os.environ["MONGO_USER_NAME"]
    mongo_password = os.environ["MONGO_PASSWORD"]
    client = MongoClient(mongo_uri)
except KeyError as err:
    print("Add MONGO_URI to .env file")

def generate_latest_tarball():
    # Execute the mongodump command
    archive_date = datetime.now().strftime("%Y-%m-%d")
    command = f"mongodump --uri={mongo_uri} --archive=static/registry-{archive_date}.tar.gz --db={database_name} --gzip --excludeCollection=users"
    subprocess.call(command, shell=True)
    print("Database backup created successfully")

generate_latest_tarball()