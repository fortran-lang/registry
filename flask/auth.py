import os
from dotenv import load_dotenv
from flask import request, jsonify
from datetime import datetime
from uuid import uuid4
from app import app
from mongo import db
import hashlib
from app import swagger
from flasgger.utils import swag_from

load_dotenv()

try:
    salt = os.getenv("SALT")
except KeyError as err:
    print("Add SALT to .env file")


def generate_uuid():
    while True:
        uuid = uuid4().hex
        user = db.users.find_one({"uuid": uuid})
        if not user:
            return uuid


@app.route("/auth/login", methods=["POST"])
@swag_from("documentation/login.yaml", methods=["POST"])
def login():
    uuid = request.form.get("uuid")
    if not uuid:
        email = request.form.get("email")
        password = request.form.get("password")
        password += salt
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = db.users.find_one({"email": email, "password": hashed_password})
        uuid = generate_uuid() if user['loggedCount']==0 else user['uuid']
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "Invalid email or password", "code": 401}), 401

    user["loggedCount"] += 1

    db.users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "loginAt": datetime.utcnow(),
                "uuid": uuid,
                "loggedCount": user["loggedCount"],
            }
        },
    )

    return (
        jsonify(
            {
                "message": "Login successful",
                "uuid": uuid,
                "code": 200,
                "username": user["username"],
            }
        ),
        200,
    )


@app.route("/auth/signup", methods=["POST"])
@swag_from("documentation/signup.yaml", methods=["POST"])
def signup():
    uuid = request.form.get("uuid")

    if not uuid:
        uuid = generate_uuid()

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username:
        return jsonify({"message": "Username is required", "code": 400}), 400

    if not email:
        return jsonify({"message": "Email is required", "code": 400}), 400

    if not password:
        return jsonify({"message": "Password is required", "code": 400}), 400

    password += salt
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    registry_user = db.users.find_one({"$or": [{"username": username}, {"email": email}]})

    user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "lastLogin": datetime.utcnow(),
        "createdAt": datetime.utcnow(),
        "uuid": uuid,
        "loggedCount": 1,
    }
    if not registry_user:
        db.users.insert_one(user)

        return (
            jsonify(
                {
                    "message": "Signup successful",
                    "uuid": uuid,
                    "code": 200,
                    "username": user["username"],
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"message": "A user with this email already exists", "code": 400}),
            400,
        )


@app.route("/auth/logout", methods=["POST"])
@swag_from("documentation/logout.yaml", methods=["POST"])
def logout():
    uuid = request.form.get("uuid")
    if not uuid:
        return jsonify({"message": "User not found", "code": 404})

    user = db.users.find_one({"uuid": uuid})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    user["loggedCount"] -= 1
    
    uuid = '' if user['loggedCount'] == 0 else uuid

    db.users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "lastLogout": datetime.utcnow(),
                "uuid": uuid,
                "loggedCount": user["loggedCount"],
            }
        },
    )

    return jsonify({"message": "Logout successful", "code": 200}), 200


@app.route("/auth/reset-password", methods=["POST"])
@swag_from("documentation/reset_password.yaml", methods=["POST"])
def reset_password():
    password = request.form.get("password")
    oldpassword = request.form.get("oldpassword")
    uuid = request.form.get("uuid")
    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404
    
    if oldpassword:
        oldpassword += salt
        hashed_password = hashlib.sha256(oldpassword.encode()).hexdigest()
        if hashed_password != user["password"]:
            return jsonify({"message": "Invalid password", "code": 401}), 401

    password += salt
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    db.users.update_one(
        {"uuid": uuid}, {"$set": {"password": hashed_password, "uuid": ""}}
    )
    return jsonify({"message": "Password reset successful", "code": 200}), 200


@app.route("/auth/forgot-password", methods=["POST"])
@swag_from("documentation/forgot_password.yaml", methods=["POST"])
def forgot_password():
    email = request.form.get("email")
    user = db.users.find({"email": email})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    uuid = generate_uuid()
    db.users.update_one({"email": email}, {"$set": {"uuid": uuid}})

    # send the uuid link in the email

    return (
        jsonify({"message": "Password reset link sent to your email", "code": 200}),
        200,
    )
