from app import app
from mongo import db
from flask import request, jsonify
from app import swagger
from flasgger.utils import swag_from


@app.route("/users/<username>", methods=["GET"])
@swag_from("documentation/user.yaml", methods=["GET"])
def profile(username):
    user = db.users.find_one({"name": username})
    packages = db.packages.find(
        {"$or": [{"author": user["_id"]}, {"maintainers": user["_id"]}]},
        {
            "name": 1,
            "updatedAt": 1,
            "_id": 0,
            "description": {"$substr": ["$description", 0, 80]},
        },
    )
    if packages:
        packages = [package for package in packages]
        return jsonify({"message": "User found", "packages": packages, "code": 200})
    else:
        return jsonify({"message": "User not found", "code": 404})


@app.route("/users/delete", methods=["POST"])
@swag_from("documentation/delete_user.yaml", methods=["POST"])
def delete_user():
    uuid = request.form.get("uuid")
    if not uuid:
        return jsonify({"message": "User not found", "code": 401})
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return "Invalid email or password", 401

    db.users.delete_one({"uuid": uuid})

    return jsonify({"message": "User deleted", "code": 200})
