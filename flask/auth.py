import os
from dotenv import load_dotenv
from flask import request, jsonify
from datetime import datetime
from uuid import uuid4
from app import app
from mongo import db
import hashlib
from app import swagger
import smtplib
from flasgger.utils import swag_from

load_dotenv()

env_var = dict()

try:
    salt = os.getenv("SALT")
    sudo_password = os.getenv("SUDO_PASSWORD")
    fortran_email = os.getenv("RESET_EMAIL")
    fortran_password = os.getenv("RESET_PASSWORD")
    host = os.getenv("HOST")
    env_var["host"] = host
    env_var["salt"] = salt
    env_var["sudo_password"] = sudo_password
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(fortran_email, fortran_password)

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
    salt = env_var["salt"]
    user_identifier = request.form.get("user_identifier")
    password = request.form.get("password")
    password += salt
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    query = {
        "$and": [
            {"$or": [{"email": user_identifier}, {"username": user_identifier}]},
            {"password": hashed_password},
        ]
    }

    # search for the user both by user name or email
    user = db.users.find_one(query)

    if not user:
        return jsonify({"message": "Invalid email or password", "code": 401}), 401

    if not user["isverified"]:
        return jsonify({"message": "Please verify your email", "code": 401}), 401

    uuid = generate_uuid() if user["loggedCount"] == 0 else user["uuid"]

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
    sudo_password = env_var["sudo_password"]
    salt = env_var["salt"]

    if not uuid:
        uuid = generate_uuid()

    username = request.form.get("username")
    email = request.form.get("email")
    email = email.lower()
    password = request.form.get("password")

    if not username:
        return jsonify({"message": "Username is required", "code": 400}), 400

    if not email:
        return jsonify({"message": "Email is required", "code": 400}), 400

    if not password:
        return jsonify({"message": "Password is required", "code": 400}), 400

    password += salt
    sudo_password += salt
    sudo_hashed_password = hashlib.sha256(sudo_password.encode()).hexdigest()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    registry_user = db.users.find_one(
        {"$or": [{"username": username}, {"email": email}]}
    )

    user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "lastLogout": None,
        "loginAt": datetime.utcnow(),
        "createdAt": datetime.utcnow(),
        "uuid": uuid,
        "loggedCount": 1,
        "isverified": False,
    }

    if not registry_user:
        if hashed_password == sudo_hashed_password:
            user["roles"] = ["admin"]
            forgot_password(email)
        else:
            user["roles"] = ["user"]
        db.users.insert_one(user)
        send_verify_email(email)
        return (
            jsonify(
                {
                    "message": "Signup successful, Please verify your email",
                    "code": 200,
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "message": "A user with this email or username already exists",
                    "code": 400,
                }
            ),
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

    uuid = "" if user["loggedCount"] == 0 else uuid

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

    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401

    if not oldpassword:
        return jsonify({"message": "Please enter old password", "code": 400}), 400

    if not password:
        return jsonify({"message": "Please enter new password", "code": 400}), 400

    user = db.users.find_one({"uuid": uuid})
    salt = env_var["salt"]

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    if not oldpassword:
        password += salt
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        db.users.update_one(
            {"uuid": uuid},
            {"$set": {"password": hashed_password}},
        )
        return jsonify({"message": "Password reset successful", "code": 200}), 200

    oldpassword += salt
    hashed_password = hashlib.sha256(oldpassword.encode()).hexdigest()
    if hashed_password != user["password"]:
        return jsonify({"message": "Invalid password", "code": 401}), 401
    db.users.update_one(
        {"uuid": uuid},
        {"$set": {"password": hashed_password}},
    )
    return jsonify({"message": "Password reset successful", "code": 200}), 200


@app.route("/auth/forgot-password", methods=["POST"])
@swag_from("documentation/forgot_password.yaml", methods=["POST"])
def forgot_password(*email):
    try:
        email = request.form.get("email") if request.form.get("email") else email[0]
    except:
        return jsonify({"message": "Email is required", "code": 400}), 400

    user = db.users.find_one({"email": email})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    if not user["isverified"]:
        return jsonify({"message": "Please verify your email", "code": 401}), 401

    uuid = generate_uuid()
    db.users.update_one({"email": email}, {"$set": {"uuid": uuid, "loggedCount": 1}})

    message = f"""\n
    Dear {user['username']},

    We received a request to reset your password. To reset your password, please copy paste the link below in a new browser window:

    {env_var['host']}/account/reset-password/{uuid}

    Thank you,
    The Fortran-lang Team"""

    message = f"Subject: Password reset link\nTo: {email}\n{message}"

    # sending the mail
    smtp.sendmail(to_addrs=email, msg=message, from_addr=fortran_email)

    return (
        jsonify({"message": "Password reset link sent to your email", "code": 200}),
        200,
    )


def send_verify_email(email):
    user = db.users.find_one({"email": email})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    uuid = user["uuid"]

    message = f"""\n
    Dear {user['username']},

    We received a request to verify your email. To verify your email, please copy paste the link below in a new browser window:

    {env_var['host']}/account/verify/{uuid}

    Thank you,
    The Fortran-lang Team"""

    message = f"Subject: Verify email \nTo: {email}\n{message}"

    # sending the mail
    smtp.sendmail(to_addrs=email, msg=message, from_addr=fortran_email)

    return (
        jsonify({"message": "verification link sent to your email", "code": 200}),
        200,
    )


@app.route("/auth/verify-email", methods=["POST"])
def verify_email():
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    if user["newemail"] != "":
        db.users.update_one(
            {"uuid": uuid}, {"$set": {"email": user["newemail"], "newemail": ""}}
        )

    db.users.update_one({"uuid": uuid}, {"$set": {"isverified": True}})

    return jsonify({"message": "Successfully Verified Email", "code": 200}), 200


@app.route("/auth/change-email", methods=["POST"])
def change_email():
    uuid = request.form.get("uuid")
    new_email = request.form.get("newemail")

    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    if not new_email:
        return jsonify({"message": "Please enter new email", "code": 400}), 400

    used_email = db.users.find_one({"email": new_email})

    if used_email:
        return jsonify({"message": "Email already in use", "code": 400}), 400

    db.users.update_one(
        {"uuid": uuid},
        {"$set": {"newemail": new_email, "isverified": False}},
    )
    send_verify_email(new_email)

    return jsonify({"message": "Please verify your new email.", "code": 200}), 200
