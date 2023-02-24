import os
from dotenv import load_dotenv
import hashlib
from app import app
from mongo import db
from flask import request, jsonify
from app import swagger
from flasgger.utils import swag_from

load_dotenv()

try:
    salt = os.getenv("SALT")
except KeyError as err:
    print("Add SALT to .env file")

@app.route("/users/<username>", methods=["GET"])
@swag_from("documentation/user.yaml", methods=["GET"])
def profile(username):
    user = db.users.find_one({"username": username})
    if user:
        packages = db.packages.find(
            {"$or": [{"author": user["_id"]}, {"maintainers": user["_id"]}]},
        )

        response_packages = []
        if packages:
            for package in packages:
                # Get namespace from namespace id.
                namespace = db.namespaces.find_one({"_id": package["namespace"]})
                user = db.users.find_one({"_id": package["author"]})
                namespace = db.namespaces.find_one({"_id": package["namespace"]})
                response_packages.append(
                    {
                        "name": package["name"],
                        "namespace": namespace["namespace"],
                        "description": package["description"],
                        "updatedAt": package["updatedAt"],
                        "author": user["username"],
                    }
                )
        user_account = {
            "username": user["username"],
            "email": user["email"],
            "createdAt": user["createdAt"],
            "packages": response_packages,
        }
        return (
            jsonify(
                {
                    "message": "User found",
                    "user": user_account,
                    "packages": response_packages,
                    "code": 200,
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "User not found", "code": 404}), 404


@app.route("/users/delete", methods=["POST"])
@swag_from("documentation/delete_user.yaml", methods=["POST"])
def delete_user():
    uuid = request.form.get("uuid")
    password = request.form.get("password")

    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return "Invalid email or password", 401

    if password:
        password += salt
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password != user["password"]:
            return jsonify({"message": "Invalid email or password", "code": 401}), 401
        else:
            db.users.delete_one({"uuid": uuid})
            return jsonify({"message": "User deleted", "code": 200}), 200
    else:
        return jsonify({"message": "Invalid email or password", "code": 401}), 401


@app.route("/users/account", methods=["POST"])
@swag_from("documentation/account.yaml", methods=["POST"])
def account():
    uuid = request.form.get("uuid")
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    user_account = {
        "username": user["username"],
        "email": user["email"],
        "createdAt": user["createdAt"],
        "loginAt": user["loginAt"],
        "lastLogout": user["lastLogout"],
    }
    return jsonify({"message": "User Found", "user": user_account, "code": 200}), 200
