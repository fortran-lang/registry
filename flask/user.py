from app import app
from mongo import db
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from auth import generate_uuid

@app.route("/users/<username>", methods=["GET"])
def profile(username):
    uuid = request.cookies.get("uuid")
    if not uuid:
        return jsonify({"message": "only info", "code": 401})

    user = db.users.find_one({"uuid": uuid})
    if not user or user["name"] != username:
        return jsonify({"message": "only info", "code": 401})

    # return his owned and maintained packages
    packages = db.packages.find(
        {"$or": [{"author": user["_id"]}, {"maintainers": user["_id"]}]}
    )

    user ={}
    # user['']                   
    return jsonify({"message": "Password reset successful", "code": 200})

    # return render_template(
    #     "profile.html", user=user, packages=[package for package in packages]
    # )
