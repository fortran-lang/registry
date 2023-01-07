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

        # user["authorOf"].append(package["_id"])
        db.users.update_one({"_id": user["_id"]}, {"$set": user})

        return jsonify({"message": "Package Uploaded Successfully.", "code": 200})

@app.route("/packages/<username>/<namespace_name>/<package_name>/delete", methods=["GET", "POST"])
def delete_package(username, namespace_name, package_name):
    uuid = request.cookies.get("uuid")
    if not uuid:
        return render_template("login.html")

    user = db.users.find_one({"uuid": uuid})

    # If user is null or username does not matches with the username in the route.
    if not user or user["name"] != username:
        return render_template("login.html")

    # Find package using package_name and namespace_name.
    package = db.packages.find_one({"name": package_name, "namespace": namespace_name})

    # If package is not found related to the package_id. Return 404.
    if not package:
        return jsonify({"message": "Package not found", "code": 404})

    # Check if the user is authorized to delete the package.
    if user["_id"] != package["author"] and user["_id"] not in package["maintainers"]:
        return jsonify({"message": "User is not authorized to delete the package", "code": 401})

    package_deleted = db.packages.delete_one({"name": package_name, "namespace": namespace_name})

    if package_deleted.deleted_count > 0:
        return jsonify({"message": "Package deleted successfully", "code": 200})
    else:
        return jsonify({"message": "Package not found", "code": 404})