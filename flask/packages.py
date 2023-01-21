from app import app
from mongo import db
from flask import request, jsonify
from datetime import datetime
from auth import generate_uuid
import json

parameters = ['name', 'author', 'createdAt', 'updatedAt',"downloads"]
@app.route("/packages", methods=["GET"])
def search_packages():
    query = request.args.get("query")
    page = request.args.get("page")
    sorted_by = request.args.get("sorted_by")
    sort = request.args.get("sort")
    query = query if query else "fortran"
    sort = -1 if sort == "desc" else 1
    sorted_by = sorted_by if sorted_by in parameters else "name"
    page = int(page) if page else 0

    query = query.strip()
    packages = db.packages.find(
            {
                "$and": [
                    {
                        "$or": [
                            {"name": {"$regex": query}},
                            {"tags": {"$in": [query]}},
                            {"description": {"$regex": query}},
                        ]
                    },
                    {"isDeprecated": False},
                ]
            },
            {
                "_id": 0,
                "name": 1,
                "namespace": 1,
                "author": 1,
                "description": 1,
                "tags": 1,
            },
        ).sort(sorted_by, sort).limit(10).skip(page * 10)
    
    if packages:
        search_packages = []
        for i in packages:
            namespace = db.namespaces.find_one({"_id": i["namespace"]})
            author = db.users.find_one({"_id": i["author"]})
            i["namespace"] = namespace["namespace"]
            i["author"] = author["name"]
            search_packages.append(i)
        return jsonify({"status": 200, "packages": search_packages}), 200
    else:
        return jsonify({"status": "error", "message": "packages not found"}), 404

@app.route("/packages", methods=["POST"])
def upload():
    uuid = request.cookies.get("uuid")
    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    name = request.form.get("name")
    namespace = request.form.get("namespace")
    tarball = request.files["tarball"]
    version = request.form.get("version")
    license = request.form.get("license")
    copyright = request.form.get("copyright")
    description = request.form.get("description")
    namespace_description = request.form.get("namespace_description")
    tags = request.form.get("tags").strip().split(",")
    dependencies = request.form.get("dependencies").strip().split(",")

    # Check if namespace already exists.
    package_namespace = db.namespaces.find_one({"namespace": namespace})

    # If namespace does not exists. Then, create it.
    if package_namespace is None:
        namespace_doc = {
            "namespace": namespace,
            "createdAt": datetime.utcnow(),
            "createdBy": user["_id"],
            "description": namespace_description,
            "tags": tags,
            "authors": user["_id"],
        }

        db.namespaces.insert_one(namespace_doc)
    
    # Get the namespace document.
    namespace = db.namespaces.find_one({"namespace": namespace})

    # Try to get the package with exact same version to be uploaded.
    package = db.packages.find_one(
        {"name": name, "versions.version": version, "namespace": namespace["_id"]}
    )

    # Check if package with particular version number already exits.
    if package is not None:
        return jsonify({"status": "error", "message": "Package already exists"}), 400

    # Get the previous uploaded package.
    package_previously_uploaded = db.packages.find_one({
        "name": name, "namespace": namespace["_id"]
    })

    # TODO: Replace this code with Storage Service.
    tarball_name = "{}-{}.tar.gz".format(name, version)
    tarball.save(tarball_name)

    # If there are no previous versions of package.
    # This means user is trying to upload a new package.
    # There are no previous recorded versions of package present in registry.
    if package_previously_uploaded is None:
        package = {
            "name": name,
            "namespace": namespace["_id"],
            "description": description,
            "license": license,
            "createdAt": datetime.utcnow(),
            "author": user["_id"],
            "maintainers": [user["_id"]],
            "copyright": copyright,
            "tags": list(set(tags)),
        }

        version_document = {    
            "version": version,
            "tarball": tarball_name,
            "dependencies": dependencies
        }

        package["versions"] = []

        # Append the first version document.
        package["versions"].append(version_document)

        db.packages.insert_one(package)
        
        package = db.packages.find_one(
            {"name": name, "versions.version": version, "namespace": namespace["_id"]}
        )

        namespace["packages"] = []

        # Add the package id to the namespace.
        namespace["packages"].append(package["_id"])
        db.namespaces.update_one({"_id": namespace["_id"]}, {"$set": namespace})

        if "authorOf" not in user:
            user["authorOf"] = []
        
        # Current user is the author of the package.
        user["authorOf"].append(package["_id"])
        db.users.update_one({"_id": user["_id"]}, {"$set": user})

        return jsonify({"message": "Package Uploaded Successfully.", "code": 200})     
    else:
        # This block of code runs if there are previous recorded versions of a package present in registry.
        # This means user is uploading a new version of already existing package.
        # Check if the version to be uploaded is valid or not.
        is_valid = check_version(package_previously_uploaded["versions"][-1]["version"], version)

        if not is_valid:
            return jsonify({"status": "error", "message": "Incorrect version"}), 400
            
        new_version = {
            "tarball": tarball_name,
            "version": version,
            "dependencies": dependencies,
        }

        package_previously_uploaded["versions"].append(new_version)
        db.packages.update_one({"_id": package_previously_uploaded["_id"]}, {"$set": package_previously_uploaded})
        
        return jsonify({"message": "Package Uploaded Successfully.", "code": 200})


@app.route("/packages", methods=["PUT"])
def update_package():
    uuid = request.cookies.get("uuid")
    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    name = request.form.get("name")
    version = request.form.get("version")
    namespace = request.form.get("namespace")
    isDeprecated = request.form.get("isDeprecated")
    namespace = db.namespaces.find_one({"namespace": namespace})

    package = db.packages.find_one(
        {"name": name, "version": version, "namespace": namespace["_id"]}
    )
    if package is None:
        return jsonify({"status": "error", "message": "Package doesn't exist"}), 404
    
    isDeprecated = True if isDeprecated == "true" else False
    package["isDeprecated"] = isDeprecated
    db.packages.update_one({"_id": package["_id"]}, {"$set": package})
    return jsonify({"message": "Package Updated Successfully.", "code": 200})


def check_version(current_version, new_version):
    current_list = list(map(int, current_version.split(".")))
    new_list = list(map(int, new_version.split(".")))
    return (new_list > current_list)
    
@app.route("/packages/<namespace_name>/<package_name>", methods=["GET"])
def get_package(namespace_name, package_name):
    # Get namespace from namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Get package from a package_name and namespace's id.
    package = db.packages.find_one({
        "name": package_name, "namespace": namespace["_id"]
    })

    # Check if package is not found.
    if not package:
        return jsonify({"message": "Package not found", "code": 404})

    else:
        # Get the package author from id. 
        package_author = db.users.find_one({"_id": package["author"]})

        # Only latest version of the package will be sent as a response.
        package_response_data = {
            "name": package["name"],
            "namespace": namespace["namespace"],
            "latest_version_data": package["versions"][-1],
            "author": package_author["name"],
            "tags": package["tags"],
            "license": package["license"],
            "createdAt": package["createdAt"],
            "version_history": package["versions"]
        }

        return jsonify({"data": package_response_data, "code": 200})

@app.route("/packages/<namespace_name>/<package_name>/<version>", methods=["GET"])
def get_package_from_version(namespace_name, package_name, version):
    # Get namespace from namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Get package from a package_name, namespace's id and version.
    package = db.packages.find_one({"name": package_name, "namespace": namespace["_id"], "versions.version": version})

    # Check if package is not found.
    if not package:
        return jsonify({"message": "Package not found", "code": 404})

    else:
        # Get the package author from id. 
        package_author = db.users.find_one({"_id": package["author"]})

        # Extract version data from the list of versions.
        version_history = package["versions"]
        version_data = next(filter(lambda obj: obj['version'] == version, version_history), None)
        
        # Only queried version should be sent as response.
        package_response_data = {
            "name": package["name"],
            "namespace": namespace["namespace"],
            "author": package_author["name"],
            "tags": package["tags"],
            "license": package["license"],
            "createdAt": package["createdAt"],
            "version_data": version_data
        }

        return jsonify({"data": package_response_data, "code": 200})
