#!/usr/bin/env python
import os
from flask import Flask
from flask import render_template
from flask import flash, request
from pymongo import MongoClient
import itertools
from datetime import datetime
import json

app = Flask(__name__)

client = MongoClient("mongo:27017")
db = client.fpmregistry

@app.route('/')
def index():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    return "Hello world, Mongo Flask"

@app.route('/login', methods=['GET'])
def render_main():
   return render_template('login.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

