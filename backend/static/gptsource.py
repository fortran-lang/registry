import os
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from uuid import uuid4
import bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)


load_dotenv()
try:
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
except KeyError as err:
    print("Add MONGO_URI to .env file")

db = client.fpmregistry

@app.route("/")
def index():
    return render_template("login.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)



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

@app.route('/packages', methods=["GET"])
def search_packages():
    query = request.args.get('query')
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

@app.route("/packages", methods=["POST"])
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
            dependencies_id = []
            if dependency == "":
                dependencies.remove(dependency)
            resp = db.packages.find_one({"name": dependency})
            if resp:
                dependencies_id.append(resp["_id"])

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
            hashed_password = bcrypt.hashpw(password, salt)
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
        if not uuid:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            hashed_password = bcrypt.hashpw(password, salt)
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


@app.route("/auth/forgot-password", methods=["POST"])
def forgotpassword():
    password = request.form.get("password")
    uuid = request.form.get("uuid")
    user = db.users.find_one({"uuid": uuid})
    if not user:
        return jsonify({"message": "User not found", "code": 404})

    hashed_password = bcrypt.hashpw(password, salt)
    db.users.update_one({"_id": user["_id"]}, {"$set": {"password": hashed_password}})
    db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": ""}})
    response = make_response("Password reset successful")
    response.set_cookie("uuid", "", expires=0)
    return response


@app.route("/auth/reset-password", methods=["POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]
        user = db.users.find_one({"email": email})
        if not user:
            return jsonify({"message": "User not found", "code": 404})

        db.users.update_one({"_id": user["_id"]}, {"$set": {"uuid": generate_uuid()}})

        # send the link in the email

        return jsonify(
            {"message": "Password reset link sent to your email", "code": 200}
        )


@app.route('/users/<username>/maintainer/', methods=['GET', 'POST'])
def manage_maintainers(username):
    # Check if user is logged in
    uuid = request.cookies.get('uuid')
    if not uuid:
        return render_template('login.html')

    # Retrieve user from database
    user = db.users.find_one({'uuid': uuid})

    # Return login page if user is not found or username does not match
    if not user or user['name'] != username:
        return render_template('login.html')

    # Only allow maintainers or admins to access this route
    if 'maintainer' in user['roles'] or 'admin' in user['roles']:
        if request.method == 'POST':
            # Handle request to approve or reject maintainer requests
            package_name = request.form.get('package_name')
            package = db.packages.find_one({'name': package_name})
            if package:
                action = request.form.get('action')
                if action == 'approve':
                    package['maintainers'].append(user['_id'])
                    db.packages.update_one({'_id': package['_id']}, {'$set': package})
                    return jsonify({'status': 'success'})
                elif action == 'reject':
                    return jsonify({'status': 'success'})
                else:
                    return jsonify({'error': 'Invalid action'}), 400
            else:
                return jsonify({'error': 'Package not found'}), 404
        else:
            # Return a list of packages with pending maintainer requests
            packages = db.packages.find(
                {'maintainers_pending': user['_id']}
            )
            return render_template(
                'manage_maintainers.html', packages=[package for package in packages]
            )
    else:
        return render_template('unauthorized.html'), 403


