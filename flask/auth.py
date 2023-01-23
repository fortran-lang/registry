import os
from dotenv import load_dotenv
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from uuid import uuid4
from app import app
from mongo import db
import hashlib

load_dotenv()

try:
    salt = os.getenv("SALT")
except KeyError as err:
    print("Add SALT to .env file")


def generate_uuid():
    uuid = uuid4().hex
    user = db.users.find_one({"uuid": uuid})
    while user:
        uuid = uuid4().hex
        user = db.users.find_one({"uuid": uuid})
    return uuid


@app.route("/auth/login", methods=["POST"])
def login():
    uuid = request.form.get("uuid")
    if not uuid:
        email = request.form.get("email")
        password = request.form.get("password")
        password += salt
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = db.users.find_one({"email": email, "password": hashed_password})
        uuid = generate_uuid()
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return "Invalid email or password", 401

    db.users.update_one({"_id": user["_id"]}, {"$set": {"loginAt": datetime.utcnow()}})

    db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": uuid}})

    return jsonify({"message": "Login successful", "uuid": uuid, "code": 200})


@app.route("/auth/signup", methods=["POST"])
def signup():
    uuid = request.form.get("uuid")
    if not uuid:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        password += salt
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        registry_user = db.users.find_one({"$or": [{"name": name}, {"email": email}]})
        uuid = generate_uuid()
    else:
        return "A user with this email already exists", 400

    user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "lastLogin": datetime.utcnow(),
        "createdAt": datetime.utcnow(),
        "uuid": uuid,
    }
    if not registry_user:
        db.users.insert_one(user)
        return jsonify({"message": "Signup successful", "uuid": uuid, "code": 200})
    else:
        return "A user with this email already exists", 400


@app.route("/auth/logout", methods=["POST"])
def logout():
    uuid = request.form.get("uuid")
    if not uuid:
        return jsonify({"message": "User not found", "code": 404})

    user = db.users.find_one({"uuid": uuid})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    db.users.update_one(
        {"_id": user["_id"]}, {"$set": {"lastLogout": datetime.utcnow()}}
    )

    db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": ""}})

    return jsonify({"message": "Logout successful", "uuid": "", "code": 200})


@app.route("/auth/reset-password", methods=["GET"])
def reset_password():
    password = request.form.get("password")
    uuid = request.form.get("uuid")
    user = db.users.find_one({"uuid": uuid})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    password += salt
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    db.users.update_one(
        {"uuid": uuid}, {"$set": {"password": hashed_password, "uuid": ""}}
    )
    return jsonify({"message": "Password reset successful", "code": 200})


@app.route("/auth/forgot-password", methods=["POST"])
def forgot_password():
    email = request.form.get("email")
    user = db.users.find({"email": email})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    uuid = generate_uuid()
    db.users.update_one({"email": email}, {"$set": {"uuid": uuid}})

    # send the uuid link in the email

    return jsonify({"message": "Password reset link sent to your email", "code": 200})
