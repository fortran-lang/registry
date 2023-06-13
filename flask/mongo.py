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

db = client[database_name]
file_storage = GridFS(db, collection="tarballs")


@app.route("/registry/clone", methods=["GET"])
def clone():
    folder_path = "static"
    file_list = os.listdir(folder_path)

    # Check if the folder exists and was modified more than 1 week ago
    if os.path.exists(folder_path):
        mod_time = datetime.fromtimestamp(os.path.getmtime(folder_path))
        if datetime.now() - mod_time > timedelta(days=7):
            generate_latest_tarball()

    return jsonify(
        {"message": "Successfully Fetched Archives", "archives": file_list, "code": 200}
    )


def generate_latest_tarball():
    # Execute the mongodump command
    archive_date = datetime.datetime.now().strftime("%Y-%m-%d")
    command = f"mongodump --uri={mongo_uri}--archive=static/registry-{archive_date}.tar.gz --db={database_name} --gzip --excludeCollection=users"
    subprocess.call(command, shell=True)