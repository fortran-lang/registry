from app import app
from mongo import db
from mongo import file_storage
from bson.objectid import ObjectId
from flask import request, jsonify, abort, send_file
from gridfs.errors import NoFile
from datetime import datetime, timedelta
from auth import generate_uuid
from app import swagger
import zipfile
import toml
from flasgger.utils import swag_from
from urllib.parse import unquote
import math
import semantic_version
from license_expression import get_spdx_licensing
# from validate_package import validate_package

parameters = {
    "name": "name",
    "author": "author",
    "createdat": "createdAt",
    "updatedat": "updatedAt",
    "downloads": "downloads",
}

def is_valid_version_str(version_str):
    """
    Function to verify whether the version string is valid or not.

    Parameters:
    version_str: The version string to be validated.

    Returns:
    bool: True if the version_str is valid.
    """

    try:
        semantic_version.Version(version_str)
        return True
    except:
        return False

def is_valid_license_identifier(license_str):
    """
    Function to check whether the license string is a valid identifier or not.

    Parameters:
    license_str (str): The SPDX license identifier string to be validated.

    Returns:
    bool: True if the string is a valid SPDX license identifier, False otherwise.
    """
    try:
        licensing = get_spdx_licensing()
        licensing.parse(license_str, validate=True)
        return True
    except:
        return False

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
        return jsonify({"code": 200, "packages": search_packages, "total_pages": total_pages}), 200
    else:
        return jsonify({"status": "error", "message": "packages not found", "code": 404}), 404

@app.route("/packages", methods=["POST"])
def upload():
    upload_token = request.form.get("upload_token")
    package_name = request.form.get("package_name")
    package_version = request.form.get("package_version")
    package_license = request.form.get("package_license")
    dry_run = request.form.get("dry_run")
    tarball = request.files["tarball"]

    dry_run = True if dry_run == "true" else False

    if not upload_token:
        return jsonify({"code": 400, "message": "Upload token missing"})
    
    if not package_name:
        return jsonify({"code": 400, "message": "Package name is missing"})
    
    if not package_version:
        return jsonify({"code": 400, "message": "Package version is missing"})
    
    if not package_license:
        return jsonify({"code": 400, "message": "Package license is missing"})
    
    # Check whether version string is valid or not.
    if package_version == "0.0.0" or not is_valid_version_str(package_version):
        return jsonify({"code": 400, "message": "Version is not valid"})
    
    # Check whether license identifier is valid or not.
    if not is_valid_license_identifier(license_str=package_license):
        return jsonify({"code": 400, "message": f"Invalid license identifier {package_license}. Please check the SPDX license identifier list."})
    
    # Find the document that contains the upload token.
    namespace_doc = db.namespaces.find_one({"upload_tokens": {"$elemMatch": {"token": upload_token}}})

    # Check if there is a namespace connected to the given upload_token:
    if not namespace_doc:
        return jsonify({"code": 401, "message": "Invalid upload token"})
    
    # Get the matching subdocument from the upload_token array
    upload_token_doc = next(item for item in namespace_doc['upload_tokens'] if item['token'] == upload_token)

    # Check if the token is expired.
    # Expire the token after one week of it's creation.
    if check_token_expiry(upload_token_created_at=upload_token_doc['createdAt']):
        return jsonify({"code": 401, "message": "Upload token has been expired. Please generate a new one"})

    # Get the user connected to the upload token.
    user_id = upload_token_doc["createdBy"]
    user = db.users.find_one({"_id": user_id})

    if not user:
        return jsonify({"code": 404, "message": "User not found"})
    
    # User should be either namespace maintainer or namespace admin to upload a package.
    if checkUserUnauthorized(user_id=user["_id"], package_namespace=namespace_doc):
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    package_doc = db.packages.find_one({"name": package_name, "namespace": namespace_doc["_id"]})

    tarball_name = "{}-{}.tar.gz".format(package_name, package_version)
    # Upload the tarball to the Grid FS storage.
    file_object_id = file_storage.put(tarball, content_type="application/gzip", filename=tarball_name)



    # Extract the package metadata from the tarball's fpm.toml file.
    package_data = extract_fpm_toml(tarball_name)

    # TODO: Uncomment this when the package validation is enabled

    # validate the package
    # valid_package = validate_package(tarball_name, tarball_name)
    # if not valid_package:
    #     return jsonify({"status": "error", "message": "Invalid package", "code": 400}), 400


    # No previous recorded versions of the package found.
    if not package_doc:
        package_obj = {
            "name": package_name,
            "namespace": namespace_doc["_id"],
            "description": package_data["description"],
            "homepage": package_data["homepage"],
            "repository": package_data["repository"],
            "license": package_license,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
            "author": user["_id"],
            "maintainers": [user["_id"]],
            "copyright": "Test copyright",
            "tags": ["fortran", "fpm"],
            "isDeprecated": False,
        }

        version_obj = {
            "version": package_version,
            "tarball": tarball_name,
            "dependencies": "Test dependencies",
            "createdAt": datetime.utcnow(),
            "isDeprecated": False,
            "download_url": f"/tarballs/{file_object_id}"
        }

        package_obj["versions"] = []

        # Append the first version document.
        package_obj["versions"].append(version_obj)
        db.packages.insert_one(package_obj)

        package = db.packages.find_one(
            {"name": package_name, "versions.version": package_version, "namespace": namespace_doc["_id"]}
        )

        # Add the package id to the namespace.
        namespace_doc["packages"].append(package["_id"])
        namespace_doc["updatedAt"] = datetime.utcnow()
        db.namespaces.update_one({"_id": namespace_doc["_id"]}, {"$set": namespace_doc})

        if "authorOf" not in user:
            user["authorOf"] = []

        # Current user is the author of the package.
        user["authorOf"].append(package["_id"])
        db.users.update_one({"_id": user["_id"]}, {"$set": user})

        return jsonify({"message": "Package Uploaded Successfully.", "code": 200})
    else:
        # Check if version of the package already exists in the backend.
        package_version_doc = db.packages.find_one({
            "name": package_name, "namespace": namespace_doc["_id"], "versions.version": package_version
        })

        if package_version_doc:
            return jsonify({"message": "Version already exists", "code": 400}), 400

        new_version = {
            "tarball": tarball_name,
            "version": package_version,
            "dependencies": "Test dependencies",
            "isDeprecated": False,
            "createdAt": datetime.utcnow(),
            "download_url": f"/tarballs/{file_object_id}"
        }

        package_doc["versions"].append(new_version)
        package_doc["versions"] = sorted(package_doc["versions"], key=lambda x: x['version'])
        package_doc["updatedAt"] = datetime.utcnow()

        if dry_run:
            return jsonify({"message": "Dry run Successful.", "code": 200})
        
        db.packages.update_one(
            {"_id": package_doc["_id"]},
            {"$set": package_doc},
        )

        return jsonify({"message": "Package Uploaded Successfully.", "code": 200})

def check_token_expiry(upload_token_created_at):
    """
    Function to verify whether the upload token is expired or not.

    Parameters:
    upload_token_created_at (datetime): The creation date of upload token.

    Returns:
    bool: True if token is expired (older than 1 week). False otherwise.
    """
    datetime_now = datetime.utcnow()

    # Calculate the time difference between the current time and the `createdAt` time
    time_diff = datetime_now - upload_token_created_at

    # Check if the time difference is greater than 1 week
    if time_diff > timedelta(weeks=1):
        return True
    
    return False
    
@app.route('/tarballs/<oid>', methods=["GET"])
def serve_gridfs_file(oid):
    try:
        file = file_storage.get(ObjectId(oid))

        # Return the file data as a Flask response object
        return send_file(file, download_name=file.filename, as_attachment=True, mimetype=file.content_type)
    except NoFile:
        abort(404)


@app.route("/packages", methods=["PUT"])
def update_package():
    uuid = request.form.get("uuid")
    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized", "code": 401}), 401

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"status": "error", "message": "Unauthorized", "code": 401}), 401

    name = request.form.get("name")
    namespace = request.form.get("namespace")
    isDeprecated = request.form.get("isDeprecated")

    # Get the package namespace.
    package_namespace = db.namespaces.find_one({"namespace": namespace})

    if checkUserUnauthorized(user_id=user["_id"], package_namespace=package_namespace):
        return jsonify({"status": "error", "message": "Unauthorized", "code": 401}), 401

    package = db.packages.find_one(
        {"name": name, "namespace": package_namespace["_id"]}
    )
    if package is None:
        return jsonify({"status": "error", "message": "Package doesn't exist", "code": 404}), 404

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

    # Check if namespace exists.
    if not namespace:
        return jsonify({"status": "error", "message": "Namespace not found", "code": 404}), 404

    # Get package from a package_name and namespace's id.
    package = db.packages.find_one(
        {"name": package_name, "namespace": namespace["_id"]}
    )

    # Check if package is not found.
    if not package:
        return jsonify({"message": "Package not found", "code": 404})

    if request.method == "GET":
        # Get the package author from id.
        package_author = db.users.find_one({"_id": package["author"]})

        # Only latest version of the package will be sent as a response.
        package_response_data = {
            "name": package["name"],
            "namespace": namespace["namespace"],
            "latest_version_data": package["versions"][-1],
            "author": package_author["username"],
            "tags": package["tags"],
            "license": package["license"],
            "createdAt": package["createdAt"],
            "version_history": package["versions"],
            "updatedAt": package["updatedAt"],
            "description": package["description"],
        }

        return jsonify({"data": package_response_data, "code": 200})

    elif request.method == "POST":
        """
        API for checking whether the latest version of a particular package
        is already there in local registry or not.
        """
        versions = request.get_json()["cached_versions"]

        # Versions should not be empty array.
        if len(versions) == 0:
            return jsonify({"message": "cached versions list is empty", "code": 400})

        # Sort the versions received in request body.
        sorted_versions = sort_versions(versions)

        # Get the latest version stored in the backend database.
        latest_version_backend = package["versions"][-1]["version"]

        # Get the latest version that is in the local registry for that package.
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
            "repository": package["repository"],
            "homepage": package["homepage"],
            "latest_version_data": {
                "dependencies": package["versions"][-1]["dependencies"],
                "version": package["versions"][-1]["version"],
                "tarball": package["versions"][-1]["tarball"],
                "isDeprecated": package["versions"][-1]["isDeprecated"],
            }
        }

        return jsonify({"data": package, "code": 200}), 200
        

@app.route("/packages/<namespace_name>/<package_name>/<version>", methods=["GET"])
@swag_from("documentation/get_version.yaml", methods=["GET"])
def get_package_from_version(namespace_name, package_name, version):
    # Get namespace from namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Check if namespace does not exists.
    if not namespace:
        return jsonify({"message": "Namespace not found", "code": 404})

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
            "author": package_author["username"],
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
                    "code": 401
                }
            ),
            401,
        )

    # Get the namespace from the namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    if not namespace:
        return jsonify({"message": "Namespace not found", "code": 404})

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
        return jsonify({"message": "Package deleted successfully", "code": 200}), 200
    else:
        return jsonify({"message": "Internal Server Error", "code": 500})


@app.route(
    "/packages/<namespace_name>/<package_name>/<version>/delete", methods=["POST"]
)
def delete_package_version(namespace_name, package_name, version):
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized", "code": 401}), 401

    user = db.users.find_one({"uuid": uuid})

    # Check if the user is authorized to delete the package.
    if not "admin" in user["roles"]:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "User is not authorized to delete the package",
                    "code": 401
                }
            ),
            401,
        )

    # Get the namespace from the namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Check if namespace does not exists.
    if not namespace:
        return jsonify({"message": "Namespace does not found", "code": 404})

    # Perform the pull operation.
    result = db.packages.update_one(
        {"name": package_name, "namespace": namespace["_id"]},
        {"$pull": {"versions": {"version": version}}},
    )

    if result.matched_count:
        return jsonify({"message": "Package version deleted successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Package version not found", "code": 404}), 404


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

        # Check if namespace does not exists.
        if not namespace:
            return jsonify({"message": "Namespace does not found", "code": 404})

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

# This function checks if user is authorized to upload/update a package in a namespace.
def checkUserUnauthorized(user_id, package_namespace):
    admins_id_list = [str(obj_id) for obj_id in package_namespace["admins"]]
    maintainers_id_list = [str(obj_id) for obj_id in package_namespace["maintainers"]]
    str_user_id = str(user_id)
    return str_user_id not in admins_id_list and str_user_id not in maintainers_id_list

def extract_fpm_toml(file_obj):
    with zipfile.ZipFile(file_obj, 'r') as zip_ref:
        zip_ref.extract("fpm.toml")
        with open("fpm.toml", 'r') as file:
            data = toml.load(file)
            
    return data