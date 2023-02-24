from app import app
from mongo import db
from flask import request, jsonify
from datetime import datetime
from auth import generate_uuid
from app import swagger
from flasgger.utils import swag_from
from urllib.parse import unquote
import json
import math

parameters = {
    "name": "name",
    "author": "author",
    "createdat": "createdAt",
    "updatedat": "updatedAt",
    "downloads": "downloads",
}


@app.route("/packages", methods=["GET"])
@swag_from("documentation/search_packages.yaml", methods=["GET"])
def search_packages():
    query = request.args.get("query")
    page = request.args.get("page")
    sorted_by = request.args.get("sorted_by")
    sort = request.args.get("sort")
    sorted_by = sorted_by.lower() if sorted_by else "name"
    query = query if query else "fortran"
    sort = -1 if sort == "desc" else 1
    sorted_by = (
        parameters[sorted_by.lower()]
        if sorted_by.lower() in parameters.keys()
        else "name"
    )
    page = int(page) if page else 0
    query = unquote(query.strip().lower())
    packages_per_page = 10

    mongo_db_query = {
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
    }

    packages = (
        db.packages.find(
            mongo_db_query,
            {
                "_id": 0,
                "name": 1,
                "namespace": 1,
                "author": 1,
                "description": 1,
                "tags": 1,
                "updatedAt": 1,
            },
        )
        .sort(sorted_by, -1)
        .limit(packages_per_page)
        .skip(page * packages_per_page)
    )

    if packages:
        # Count the number of documents in the database related to query.
        total_documents = db.packages.count_documents(mongo_db_query)

        total_pages = math.ceil(total_documents / packages_per_page)

        search_packages = []
        for i in packages:
            namespace = db.namespaces.find_one({"_id": i["namespace"]})
            author = db.users.find_one({"_id": i["author"]})
            i["namespace"] = namespace["namespace"]
            i["author"] = author["username"]
            search_packages.append(i)
        return (
            jsonify(
                {"status": 200, "packages": search_packages, "total_pages": total_pages}
            ),
            200,
        )
    else:
        return jsonify({"status": "error", "message": "packages not found"}), 404


@app.route("/namespace/<namespace>", methods=["GET"])
def namespace_packages(namespace):
    namespace_packages = db.namespaces.find_one({"namespace": namespace})
    packages = []
    for i in namespace_packages["packages"]:
        package = db.packages.find(
            {"_id": i},
            {
                "_id": 0,
                "name": 1,
                "description": 1,
                "author": 1,
                "updatedAt": 1,
            },
        )
        for p in package:
            p["namespace"] = namespace
            author = db.users.find_one({"_id": p["author"]})
            p["author"] = author["username"]
            packages.append(p)

    return (
        jsonify(
            {
                "status": 200,
                "packages": packages,
                "createdAt": namespace_packages["createdAt"],
            }
        ),
        200,
    )

@app.route("/packages", methods=["POST"])
def upload():
    uuid = request.form.get("uuid")
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
            "updatedAt": datetime.utcnow(),
            "createdBy": user["_id"],
            "description": namespace_description,
            "tags": tags,
            "authors": user["_id"],
            "isDeprecated": False,
        }

        db.namespaces.insert_one(namespace_doc)

    # Get the namespace document.
    namespace = db.namespaces.find_one({"namespace": namespace})

    # Try to get the package with exact same version to be uploaded.
    package = db.packages.find_one(
        {"name": name, "versions.version": version, "namespace": namespace["_id"]}
    )

    # Check if package with particular version number already exists.
    if package is not None:
        return jsonify({"status": "error", "message": "Package already exists"}), 400

    # Get the previous uploaded package.
    package_previously_uploaded = db.packages.find_one(
        {"name": name, "namespace": namespace["_id"]}
    )

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
            "updatedAt": datetime.utcnow(),
            "author": user["_id"],
            "maintainers": [user["_id"]],
            "copyright": copyright,
            "tags": list(set(tags)),
            "isDeprecated": False,
        }

        version_document = {
            "version": version,
            "tarball": tarball_name,
            "dependencies": dependencies,
            "isDeprecated": False,
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
        namespace["updatedAt"] = datetime.utcnow()
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
        is_valid = check_version(
            package_previously_uploaded["versions"][-1]["version"], version
        )

        if not is_valid:
            return jsonify({"status": "error", "message": "Incorrect version"}), 400

        new_version = {
            "tarball": tarball_name,
            "version": version,
            "dependencies": dependencies,
            "isDeprecated": False,
        }

        package_previously_uploaded["versions"].append(new_version)
        package_previously_uploaded["updatedAt"] = datetime.utcnow()
        db.packages.update_one(
            {"_id": package_previously_uploaded["_id"]},
            {"$set": package_previously_uploaded},
        )

        return jsonify({"message": "Package Uploaded Successfully.", "code": 200})


@app.route("/packages", methods=["PUT"])
def update_package():
    uuid = request.form.get("uuid")
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
    package["updatedAt"] = datetime.utcnow()
    db.packages.update_one({"_id": package["_id"]}, {"$set": package})
    return jsonify({"message": "Package Updated Successfully.", "code": 200})


def check_version(current_version, new_version):
    current_list = list(map(int, current_version.split(".")))
    new_list = list(map(int, new_version.split(".")))
    return new_list > current_list


@app.route("/packages/<namespace_name>/<package_name>", methods=["GET"])
@swag_from("documentation/get_package.yaml", methods=["GET"])
def get_package(namespace_name, package_name):
    # Get namespace from namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Get package from a package_name and namespace's id.
    package = db.packages.find_one(
        {"name": package_name, "namespace": namespace["_id"]}
    )

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
            "version_history": package["versions"],
            "updatedAt": package["updatedAt"],
            "description": package["description"],
        }

        return jsonify({"data": package_response_data, "code": 200})


@app.route("/packages/<namespace_name>/<package_name>/<version>", methods=["GET"])
@swag_from("documentation/get_version.yaml", methods=["GET"])
def get_package_from_version(namespace_name, package_name, version):
    # Get namespace from namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Get package from a package_name, namespace's id and version.
    package = db.packages.find_one(
        {
            "name": package_name,
            "namespace": namespace["_id"],
            "versions.version": version,
        }
    )

    # Check if package is not found.
    if not package:
        return jsonify({"message": "Package not found", "code": 404})

    else:
        # Get the package author from id.
        package_author = db.users.find_one({"_id": package["author"]})

        # Extract version data from the list of versions.
        version_history = package["versions"]
        version_data = next(
            filter(lambda obj: obj["version"] == version, version_history), None
        )

        # Only queried version should be sent as response.
        package_response_data = {
            "name": package["name"],
            "namespace": namespace["namespace"],
            "author": package_author["name"],
            "tags": package["tags"],
            "license": package["license"],
            "createdAt": package["createdAt"],
            "version_data": version_data,
            "updatedAt": package["updatedAt"],
            "description": package["description"],
        }

        return jsonify({"data": package_response_data, "code": 200})


@app.route("/packages/<namespace_name>/<package_name>/delete", methods=["POST"])
def delete_package(namespace_name, package_name):
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    user = db.users.find_one({"uuid": uuid})

    # Check if the user is authorized to delete the package.
    if not "admin" in user["roles"]:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "User is not authorized to delete the package",
                }
            ),
            401,
        )

    # Get the namespace from the namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Find package using package_name & namespace_name.
    package = db.packages.find_one(
        {"name": package_name, "namespace": namespace["_id"]}
    )

    # If package is not found. Return 404.
    if not package:
        return jsonify({"message": "Package not found", "code": 404})

    package_deleted = db.packages.delete_one(
        {"name": package_name, "namespace": namespace["_id"]}
    )

    if package_deleted.deleted_count > 0:
        return jsonify({"message": "Package deleted successfully"}), 200
    else:
        return jsonify({"message": "Internal Server Error", "code": 500})


@app.route(
    "/packages/<namespace_name>/<package_name>/<version>/delete", methods=["POST"]
)
def delete_package_version(namespace_name, package_name, version):
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    user = db.users.find_one({"uuid": uuid})

    # Check if the user is authorized to delete the package.
    if not "admin" in user["roles"]:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "User is not authorized to delete the package",
                }
            ),
            401,
        )

    # Get the namespace from the namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Perform the pull operation.
    result = db.packages.update_one(
        {"name": package_name, "namespace": namespace["_id"]},
        {"$pull": {"versions": {"version": version}}},
    )

    if result.matched_count:
        return jsonify({"message": "Package version deleted successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Package version not found"}), 404


@app.route("/packages/list", methods=["GET"])
def get_packages():
    page = int(request.args.get("page", 0))

    packages = db.packages.find().limit(10).skip(page * 10)
    response_packages = []
    for package in packages:
        # Get the namespace id of the package.
        namespace_id = package["namespace"]

        # Get the namespace document from namespace id.
        namespace = db.namespaces.find_one({"_id": namespace_id})

        response_packages.append(
            {
                "package_name": package["name"],
                "namespace_name": namespace["namespace"],
                "description": package["description"],
            }
        )

    return jsonify({"packages": response_packages})


def sort_versions(versions):
    """
    Sorts the list of version in the reverse order. Such that the latest version comes at
    0th index.
    """
    return sorted(versions, key=lambda x: [int(i) for i in x.split(".")], reverse=True)


@app.route("/packages/<namespace_name>/<package_name>/checkversion", methods=["GET"])
@swag_from("documentation/compare_version_registry.yaml", methods=["GET"])
def compare_version_local_registry(namespace_name, package_name):
    """
    API for checking whether the latest version of a particular package
    is already there in local registry or not.
    """
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Check if namespace exists.
    if not namespace:
        return jsonify({"status": "error", "message": "Namespace not found"}), 404

    package = db.packages.find_one(
        {
            "name": package_name,
            "namespace": namespace["_id"],
        }
    )

    # Check if package exists.
    if not package:
        return jsonify({"status": "error", "message": "Package not found"}), 404

    versions = request.get_json()["versions"]

    # Sort the versions received in request body.
    sorted_versions = sort_versions(versions)

    # Get the latest version stored in the backend database.
    latest_version_backend = package["versions"][-1]["version"]

    # Get the latest version that is in the registry for that package.
    latest_version_local_registry = sorted_versions[0]

    latest_version_backend_list = list(map(int, latest_version_backend.split(".")))
    latest_version_local_registry_list = list(
        map(int, latest_version_local_registry.split("."))
    )

    # Check if the local registry already has the latest version.
    if latest_version_backend_list <= latest_version_local_registry_list:
        return (
            jsonify({"message": "Latest version is already there in local registry"}),
            200,
        )

    # If local registry does not have the latest version. Then send it from the backend.
    package = {
        "name": package["name"],
        "namespace": namespace["namespace"],
        "description": package["description"],
        "latest_version": {
            "version": package["versions"][-1]["version"],
            "tarball": package["versions"][-1]["tarball"],
        },
    }

    return jsonify({"package": package}), 200
