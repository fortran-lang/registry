import os
from flask import Flask
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from pymongo import MongoClient   
import re
from uuid import uuid4

app = Flask(__name__)

client = MongoClient("mongo:27017") 
db = client.fpmregistry 

@app.route('/')
def index():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        uuid = request.cookies.get("uuid")
        if not uuid:
            email=request.form.get('email')
            password=request.form.get('password')
            user = db.users.find_one({"email": email, "password": password})
        else:
            user = db.users.find_one({"uuid": uuid})

        if not user:
            return "Invalid email or password", 401

        db.users.update_one({"_id": user["_id"]}, {"$set": {"loginAt": datetime.utcnow()}})

        uuid = uuid4().hex

        db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": uuid}})

        response = make_response("Login successful")
        response.set_cookie("uuid", uuid)
        return response
    else:
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        uuid = request.cookies.get("uuid")
        if not uuid:
            name=request.form.get('name')
            email=request.form.get('email')
            password=request.form.get('password')
            user = db.users.find_one({"email": email})
        else:
            user = db.users.find_one({"uuid": uuid})

        if user:
            return "A user with this email already exists", 400

        user = {
            "name": name,
            "email": email,
            "password": password,
            "lastLogin": datetime.utcnow(),
            "createdAt": datetime.utcnow(),
            "uuid":"",
        }
        db.users.insert_one(user)
        uuid = uuid4().hex
        db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": uuid}})

        response = make_response("Signup successful")
        response.set_cookie("uuid", uuid)
        return response
    else:
        return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    uuid = request.cookies.get("uuid")
    if not uuid:
        return jsonify({"message": "UUID not found", "code": 404})

    user = db.users.find_one({"uuid": uuid})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    db.users.update_one({"_id": user["_id"]}, {"$set": {"lastLogout": datetime.utcnow()}})

    db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": ""}})

    response = make_response("Logout successful")
    response.set_cookie("uuid", "", expires=0)
    return response

@app.route("/forgotpassword/", methods=["POST"])
def forgotpassword():
    password=request.form.get('password')
    uuid=request.form.get('uuid')
    user = db.users.find_one({"uuid": uuid})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": ""}})
    db.users.update_one({"_id": user["_id"]}, {"$set": {"password": password}})
    response = make_response("Password reset successful")
    response.set_cookie("uuid", "", expires=0)
    return response

@app.route("/reset-password", methods=["POST"])
def reset_password():
    if request.method == 'POST':
        email = request.form["email"]
        user = db.users.find_one({"email": email})
        if not user:
            return jsonify({"message": "User not found", "code": 404})

        uuid = uuid4().hex

        db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": uuid}})

        # send the link in the email

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

