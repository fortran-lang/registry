import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
from gridfs import GridFS
from app import app
from flask import jsonify, send_file
import subprocess

load_dotenv()
database_name = os.environ['MONGO_DB_NAME']
try:
    mongo_uri = os.environ['MONGO_URI']
    mongo_username = os.environ['MONGO_USER_NAME']
    mongo_password = os.environ['MONGO_PASSWORD']
    client = MongoClient(mongo_uri)
except KeyError as err:
    print("Add MONGO_URI to .env file")

db = client[database_name]
file_storage = GridFS(db, collection="tarballs")


@app.route("/registry/clone", methods=["GET"])
def clone():
    filename = "registry.tar.gz"
    static_path = os.path.join(os.getcwd(), "static")
    file_path = os.path.join(static_path, filename)

    # Check if the file exists and was modified less than 1 week ago
    if os.path.exists(file_path):
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        if datetime.now() - mod_time < timedelta(days=7):
            return send_file(file_path, as_attachment=True)
    
    generate_latest_tarball()
    return send_file(file_path, as_attachment=True)


def generate_latest_tarball():
    backup_dir = "static"
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)

    # Execute the mongodump command
    command = f"mongodump --host {mongo_uri} --authenticationDatabase admin --username {mongo_username} --password {mongo_password} --db {database_name} --out {backup_dir}"
    subprocess.call(command, shell=True)

    # Create a tar archive of the backup directory
    archive_name = "registry.tar.gz"
    archive_path = os.path.join(backup_dir, archive_name)
    
    # Create the archive file
    command = f"tar -czvf {archive_path} static/"
    subprocess.call(command, shell=True)

    # # Remove the backup directory
    # command = f"rm -rf {backup_dir}"
    # subprocess.call(command, shell=True)

    print(f"Backup archive created: {archive_name}")

generate_latest_tarball()