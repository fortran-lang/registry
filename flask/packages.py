from app import app
from mongo import db
from flask import request, jsonify
from datetime import datetime


@app.route("/packages", methods=["GET"])
def search_packages():
    query = request.args.get("query")
    page = request.args.get("page")
    sort = request.args.get("sorted_by")
    query = query if query else "fortran"
    sort = -1 if sort == "desc" else 1
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
        ).sort("name", sort).limit(10).skip(page * 10)
    
    if packages:
        search_packages = []
        for i in packages:
            namespace = db.namespaces.find_one({"_id": i["namespace"]})
            author = db.users.find_one({"_id": i["author"]})
            i["namespace"] = namespace["namespace"]
            i["author"] = author["name"]
            search_packages.append(i)
        return jsonify({"status": "success", "packages": search_packages}), 200
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
    # for dependency in list(set(dependencies)):
    #     dependencies_id = []
    #     resp = db.packages.find_one({"name": dependency})
    #     if resp:
    #         dependencies_id.append(resp["_id"])

    namespace = db.namespaces.find_one({"namespace": namespace})
    package = db.packages.find_one(
        {"name": name, "version": version, "namespace": namespace["_id"]}
    )
    if package is not None:
        return jsonify({"status": "error", "message": "Package already exists"}), 400

    tarball_name = "{}-{}.tar.gz".format(name, version)
    tarball.save(tarball_name)

    package = {
        "name": name,
        "namespace": namespace["_id"],
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

    package = db.packages.find_one(
        {"name": name, "version": version, "namespace": namespace["_id"]}
    )
    if namespace:
        namespace["packages"].append(package["_id"])
        db.namespaces.update_one({"_id": namespace["_id"]}, {"$set": namespace})
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


@app.route("/packages/<namespace>/<package_name>", methods=["PUT"])
def update_package(namespace, package_name):
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
        return jsonify({"status": "error", "message": "Package doesn't exist"}), 400

    if isDeprecated == True or isDeprecated == False:
        package["isDeprecated"] = isDeprecated
        db.packages.update_one({"_id": package["_id"]}, {"$set": package})
        return jsonify({"message": "Package Updated Successfully.", "code": 200})
    else:
        return jsonify({"status": "error", "message": "Invalid Request"}), 500
