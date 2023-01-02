from app import app
from mongo import db
from flask import render_template
from flask import request, make_response, jsonify
from datetime import datetime
from auth import generate_uuid

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

