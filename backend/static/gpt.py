import os
from flask import render_template
from app import app
from mongo import db
import auth
import user
import packages

@app.route("/")
def index():
    return render_template("create.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

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


from app import app
from mongo import db
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from auth import generate_uuid

@app.route('/packages/<package_name>', methods=["GET"])
def search_packages(package_name):
    query = request.args.get('query')
    if query:
        query = query.lower().strip()
        packages = db.packages.find(
            {
                "$or": [
                    {"name": {"$regex": query}},
                    {"tags": {"$in": [query]}},
                    {"description": {"$regex": query}},
                ]
            }
        )
        package = []
        maintainers =[]
        if packages:
            for i in packages:
                for maintainer in i['maintainers']:
                    name = db.users.find_one({"_id": maintainer})
                    maintainers.append(name['name'])
                i['maintainers'] = list(set(maintainers))
                package.append(i)
                del i['_id'] , i['author']
            return jsonify(package)

    if package_name:
        package = db.packages.find_one({"name": package_name})
        if package:
            del package['_id'] , package['author'] , package['maintainers']
            return package
        else:
            return jsonify({"status": "error", "message": "Package not found"}), 404


@app.route("/packages", methods=["POST"])
def upload():
    uuid = request.cookies.get("uuid")
    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    if request.method == "POST":
        name = request.form.get("name")
        namespace = request.form.get("namespace")
        tarball  = request.files['tarball']
        version = request.form.get("version")
        license = request.form.get("license")
        copyright = request.form.get("copyright")
        description = request.form.get("description")
        namespace_description = request.form.get("namespace_description")
        tags = request.form.get("tags").strip().split(",")
        dependencies = request.form.get("dependencies").strip().split(",")
        # for dependency in list(set(dependencies)):
        #     dependencies_id = []
        #     resp = db.packages.find_one({"name": dependency})
        #     if resp:
        #         dependencies_id.append(resp["_id"])

        package = db.packages.find_one({"name": name, "version": version})
        if package is not None:
            return jsonify({"status": "error", "message": "Package already exists"}), 400
        
        tarball_name = "{}-{}.tar.gz".format(name, version)
        tarball.save(tarball_name)

        package = {
            "name": name,
            "namespace": namespace,
            "tarball": tarball_name,
            "version": version,
            "license": license,
            "createdAt": datetime.utcnow(),
            "author": user["_id"],
            "maintainers": [user["_id"]],
            "copyright": copyright,
            "description": description,
            "tags": list(set(tags)),
            "dependencies": dependencies,
        }
        db.packages.insert_one(package)

        namespace_doc = db.namespaces.find_one({"namespace": namespace})
        if namespace_doc:
            namespace_doc["packages"].append(package["_id"])
            db.namespaces.update_one(
                {"_id": namespace_doc["_id"]}, {"$set": namespace_doc}
            )
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

@app.route("/packages/<package_name>", methods=["PUT"])
def update_package():
    uuid = request.cookies.get("uuid")
    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    if request.method == "PUT":
        name = request.form.get("name")
        namespace = request.form.get("namespace")
        tarball  = request.files['tarball']
        version = request.form.get("version")
        license = request.form.get("license")
        copyright = request.form.get("copyright")
        description = request.form.get("description")
        namespace_description = request.form.get("namespace_description")
        tags = request.form.get("tags").strip().split(",")
        dependencies = request.form.get("dependencies").strip().split(",")
        # for dependency in list(set(dependencies)):
        #     dependencies_id = []
        #     resp = db.packages.find_one({"name": dependency})
        #     if resp:
        #         dependencies_id.append(resp["_id"])

        package = db.packages.find_one({"name": name, "version": version})
        if package is not None:
            return jsonify({"status": "error", "message": "Package already exists"}), 400
        
        tarball_name = "{}-{}.tar.gz".format(name, version)
        tarball.save(tarball_name)

        package = {
            "name": name,
            "namespace": namespace,
            "tarball": tarball_name,
            "version": version,
            "license": license,
            "createdAt": datetime.utcnow(),
            "author": user["_id"],
            "maintainers": [user["_id"]],
            "copyright": copyright,
            "description": description,
            "tags": list(set(tags)),
            "dependencies": dependencies,
        }
        db.packages.insert_one(package)
        db.users.update_one({"_id": user["_id"]}, {"$set": user})

        return jsonify({"message": "Package Updated Successfully.", "code": 200})

import os
from dotenv import load_dotenv
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from uuid import uuid4
from app import app
from mongo import db
import hashlib

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
            password+=salt
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


@app.route("/auth/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uuid = request.cookies.get("uuid")
        user = db.users.find_one({"uuid": uuid})
        if not user:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            password+=salt
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = db.users.find_one({"email": email})
            uuid = generate_uuid()
        else:
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


@app.route("/auth/forgot-password", methods=["POST", "GET"])
def forgotpassword():
    if request.method == "POST":
        password = request.form.get("password")
        uuid = request.cookies.get("uuid")
        user = db.users.find_one({"uuid": uuid})
        if not user:
            return jsonify({"message": "User not found", "code": 404})

        password+=salt
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        db.users.update_one({"uuid": uuid}, {"$set": {"password": hashed_password,"uuid": ""}})
        response = make_response("Password reset successful")
        response.set_cookie("uuid", "", expires=0)
        return response
    if request.method == "GET":
        return render_template("change-password.html")


@app.route("/auth/reset-password", methods=["POST", "GET"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = db.users.find({"email": email})
        if not user:
            return jsonify({"message": "User not found", "code": 404})

        uuid = generate_uuid()
        db.users.update_one({"email": email}, {"$set": {"uuid": uuid}})

        # send the uuid link in the email

        return jsonify(
            {"message": "Password reset link sent to your email", "code": 200}
        )
    if request.method == "GET":
        return render_template("reset-password.html")


import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

try:
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
except KeyError as err:
    print("Add MONGO_URI to .env file")

db = client.fpmregistry


