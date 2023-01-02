from app import app
from mongo import db
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from auth import generate_uuid

@app.route("/users/<username>/", methods=["GET"])
def profile(username):
    uuid = request.cookies.get("uuid")
    if not uuid:
        return render_template("login.html")

    user = db.users.find_one({"uuid": uuid})

    if not user or user["name"] != username:
        return render_template("login.html")

    # return his owned and maintained packages
    packages = db.packages.find(
        {"$or": [{"author": user["_id"]}, {"maintainers": user["_id"]}]}
    )

    return render_template(
        "profile.html", user=user, packages=[package for package in packages]
    )
