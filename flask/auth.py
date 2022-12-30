import os
from dotenv import load_dotenv
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from uuid import uuid4
from app import app
from mongo import db
import bcrypt

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


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uuid = request.cookies.get("uuid")
        if not uuid:
            email = request.form.get("email")
            password = request.form.get("password")
            hashed_password = bcrypt.hashpw(password, salt)
            user = db.users.find_one({"email": email, "password": hashed_password})
            uuid = generate_uuid()
        else:
            user = db.users.find_one({"uuid": uuid})

        if not user:
            return "Invalid email or password", 401

        db.users.update_one(
            {"_id": user["_id"]}, {"$set": {"loginAt": datetime.utcnow()}}
        )

        db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": uuid}})

        response = make_response("Login successful")
        response.set_cookie("uuid", uuid)
        return response
    else:
        return render_template("login.html")


@app.route("/auth/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uuid = request.cookies.get("uuid")
        if not uuid:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            hashed_password = bcrypt.hashpw(password, salt)
            user = db.users.find_one({"email": email})
            uuid = generate_uuid()
        else:
            user = db.users.find_one({"uuid": uuid})

        if user:
            return "A user with this email already exists", 400

        user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "lastLogin": datetime.utcnow(),
            "createdAt": datetime.utcnow(),
            "uuid": uuid,
        }
        db.users.insert_one(user)

        response = make_response("Signup successful")
        response.set_cookie("uuid", uuid)
        return response
    else:
        return render_template("signup.html")


@app.route("/auth/logout", methods=["POST"])
def logout():
    uuid = request.cookies.get("uuid")
    if not uuid:
        return jsonify({"message": "User not found", "code": 404})

    user = db.users.find_one({"uuid": uuid})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    db.users.update_one(
        {"_id": user["_id"]}, {"$set": {"lastLogout": datetime.utcnow()}}
    )

    db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": ""}})

    response = make_response("Logout successful")
    response.set_cookie("uuid", "", expires=0)
    return response


@app.route("/auth/forgot-password", methods=["POST"])
def forgotpassword():
    password = request.form.get("password")
    uuid = request.form.get("uuid")
    user = db.users.find_one({"uuid": uuid})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    hashed_password = bcrypt.hashpw(password, salt)
    db.users.update_one({"_id": user["_id"]}, {"$set": {"password": hashed_password}})
    db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": ""}})
    response = make_response("Password reset successful")
    response.set_cookie("uuid", "", expires=0)
    return response


@app.route("/auth/reset-password", methods=["POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]
        user = db.users.find_one({"email": email})
        if not user:
            return jsonify({"message": "User not found", "code": 404})

        db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": generate_uuid()}})

        # send the link in the email

        return jsonify(
            {"message": "Password reset link sent to your email", "code": 200}
        )
