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

@app.route("/users/<username>/<package_name>/delete", methods=["GET", "POST"])
def delete_package(username, package_name):
    uuid = request.cookies.get("uuid")
    if not uuid:
        return render_template("login.html")

    user = db.users.find_one({"uuid": uuid})

    # If user is null or username does not matches with the username in the route.
    if not user or user["name"] != username:
        return render_template("login.html")

    package = db.packages.find_one({"name": package_name})

    # If package is not found related to the package_id. Return 404.
    if not package:
        return jsonify({"message": "Package not found", "code": 404})

    # Check if the user is authorized to delete the package.
    if user["_id"] != package["author"] and user["_id"] not in package["maintainers"]:
        return jsonify({"message": "User is not authorized to delete the package", "code": 401})

    package_deleted = db.packages.delete_one({"name": package_name})

    if package_deleted.deleted_count == 1:
        return jsonify({"message": "Package deleted successfully", "code": 200})
    else:
        return jsonify({"message": "Package not found", "code": 400})
