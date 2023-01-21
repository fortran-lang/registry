from app import app
from mongo import db
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from auth import generate_uuid

@app.route("/users/<username>", methods=["GET"])
def profile(username):
    uuid = request.form.get("uuid")
    if not uuid:
        user = db.users.find_one({"name": username})
        #write code to return user profile for not logged in 
    else:
        user = db.users.find_one({"uuid": uuid})
        if not user:
            return jsonify({"message": "User not found", "code": 401})
        print(user)
        #write code to return user profile for logged in user

    # if not user or user["name"] != username:
    #     return jsonify({"message": "User not found", "code": 401})

    # return his owned and maintained packages
    packages = db.packages.find(
        {"$or": [{"author": user["_id"]}, {"maintainers": user["_id"]}]}
    )

    user ={}
    # user['']                   
    return jsonify({"message": "Password reset successful", "code": 200})


@app.route("/users/delete", methods=["POST"])
def delete_user():
    uuid = request.form.get("uuid")
    if not uuid:
        return jsonify({"message": "User not found", "code": 401})
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return "Invalid email or password", 401

    db.users.delete_one({'uuid': uuid})

    return jsonify({"message": "User deleted", "code": 200})
