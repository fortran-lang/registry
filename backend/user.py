from app import app
from mongo import db
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from auth import generate_uuid

def user_packages(username):
    #finding a user and all his owned/maintained packages 
    #returns a list of packages
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
    return [package for package in packages]

# @app.route("/users/<username>", methods=["GET"])
# def profile(username):
#     uuid = request.form.get("uuid")
#     # if not uuid:
#     #     packages =  user_packages(username)
#     #     return jsonify({"message": "User found","packages":packages, "code": 200})

#     # else:
#     #     user = db.users.find_one({"uuid": uuid})
#     #     if not user:
#             packages =  user_packages(username)
#             return jsonify({"message": "User found","packages":packages, "code": 200})
#         # this is the user who is logged in
        

#     # return his owned and maintained packages
#     packages = db.packages.find(
#         {"$or": [{"author": user["_id"]}, {"maintainers": user["_id"]}]}
#     )
#     return jsonify({"message": "Password reset successful", "code": 200})


@app.route("/users/delete", methods=["POST"])
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
