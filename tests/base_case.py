import unittest
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from gridfs import GridFS
from flask import Flask

app = Flask(__name__)
load_dotenv()

database_name = os.environ['MONGO_DB_NAME']
try:
    mongo_uri = os.environ['MONGO_URI']
    client = MongoClient(mongo_uri)
except KeyError as err:
    print("Add MONGO_URI to .env file")

db = client[database_name]
file_storage = GridFS(db, collection="tarballs")

class BaseTestClass(unittest.TestCase):
    def setUp(self):

        # set up any variables or configurations needed for your tests
        self.client = app.test_client()

    def tearDown(self):
        # tear down any variables or configurations set up in setUp() 
        client.drop_database('testregistry')
