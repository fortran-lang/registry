import os
import hashlib
from flask import Flask
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from pymongo import MongoClient
import re
from uuid import uuid4

app = Flask(__name__)

client = MongoClient("mongo:27017")
db = client.fpmregistry


@app.route("/")
def index():
    return render_template("login.html")


def generate_uuid():
    uuid = uuid4().hex
    user = db.users.find_one({"uuid": uuid})
    while user:
        uuid = uuid4().hex
        user = db.users.find_one({"uuid": uuid})
    return uuid


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uuid = request.cookies.get("uuid")
        if not uuid:
            email = request.form.get("email")
            password = request.form.get("password")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uuid = request.cookies.get("uuid")
        if not uuid:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
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
            "uuid": "",
        }
        db.users.insert_one(user)
        db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": uuid}})

        response = make_response("Signup successful")
        response.set_cookie("uuid", uuid)
        return response
    else:
        return render_template("login.html")

@app.route("/logout", methods=["POST"])
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


@app.route("/forgotpassword/", methods=["POST"])
def forgotpassword():
    password = request.form.get("password")
    uuid = request.form.get("uuid")
    user = db.users.find_one({"uuid": uuid})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    db.users.update_one({"_id": user["_id"]}, {"$set": {"password": hashed_password}})
    db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": ""}})
    response = make_response("Password reset successful")
    response.set_cookie("uuid", "", expires=0)
    return response


@app.route("/reset-password", methods=["POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]
        user = db.users.find_one({"email": email})
        if not user:
            return jsonify({"message": "User not found", "code": 404})

        db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": generate_uuid()}})

        # send the link in the email

        return jsonify({"message": "Password reset link sent to your email", "code": 200})


@app.route("/<username>/", methods=["GET"])
def profile(username):
    uuid = request.cookies.get("uuid")
    if not uuid:
        return render_template("login.html")

    user = db.users.find_one({"uuid": uuid})

    if not user or user["name"] != username:
        return render_template("login.html")

    # return his owned and maintained packages
    packages = db.packages.find({"$or": [{"author": user["_id"]}, {"maintainers": user["_id"]}]})

    return render_template("profile.html", user=user, packages=[package for package in packages])


@app.route("/<username>/upload", methods=["GET", "POST"])
def upload(username):
    uuid = request.cookies.get("uuid")
    if not uuid:
        return render_template("login.html")

    user = db.users.find_one({"uuid": uuid})

    if not user or user["name"] != username:
        return render_template("login.html")

    if request.method == "POST":
        name = request.form.get("name")
        namespace = request.form.get("namespace")
        tarball = request.form.get("tarball")
        version = request.form.get("version")
        license = request.form.get("license")
        copyright = request.form.get("copyright")
        description = request.form.get("description")
        namespace_description = request.form.get("namespace_description")
        tags = request.form.get("tags").split(",")
        dependencies = request.form.get("dependencies").trim().split(",")
        for dependency in dependencies:
            dependencies_id=[]
            if dependency == "":
                dependencies.remove(dependency)
            resp = db.packages.find_one({"name": dependency})
            if resp:
                dependencies_id.append(resp['_id'])
            
        package = {
            "name": name,
            "namespace": namespace,
            "tarball": tarball,
            "version": version,
            "license": license,
            "createdAt": datetime.utcnow(),
            "author": user["_id"],
            "maintainers": [user["_id"]],
            "copyright": copyright,
            "description": description,
            "tags": tags,
            "dependencies": dependencies,
        }
        db.packages.insert_one(package)

        namespace_doc = db.namespaces.find_one({"namespace": namespace})
        if namespace_doc:
            namespace_doc["packages"].append(package["_id"])
            db.namespaces.update_one({"_id": namespace_doc["_id"]}, {"$set": namespace_doc})
        else:
            namespace_doc = {
                "namespace": namespace,
                "createdAt": datetime.utcnow(),
                "createdBy": user["_id"],
                "description": namespace_description,
                "tags": tags,
                "authors": user["_id"],
                "packages": [package["_id"]],
            }
            db.namespaces.insert_one(namespace_doc)

        user["authorOf"].append(package["_id"])
        db.users.update_one({"_id": user["_id"]}, {"$set": user})

        return jsonify({"message": "Package Uploaded Successfully.", "code": 200})

    else:
        return render_template("upload.html")


@app.route("/search/<query>", methods=["GET"])
def search_packages(query):
    packages = db.packages.find(
        {
            "$or": [
                {"name": {"$regex": query}},
                {"tags": {"$in": [query]}},
                {"description": {"$regex": query}},
            ]
        }
    )

    return jsonify([package for package in packages])

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
