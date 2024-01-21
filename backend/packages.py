from app import app
from mongo import db
from mongo import file_storage
from bson.objectid import ObjectId
from flask import request, jsonify, abort, send_file
from gridfs.errors import NoFile
from datetime import datetime, timedelta
from auth import generate_uuid, IS_VERCEL
from app import swagger
import tarfile
import os
import toml
import shutil
from flasgger.utils import swag_from
from urllib.parse import unquote
import math
import semantic_version
from license_expression import get_spdx_licensing
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.namespace import Namespace
from models.user import User
from models.package import Package
from models.package import Version


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
            {"is_deprecated": False},
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
                "updated_at": 1,
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
            package_obj = Package.from_json(i)

            namespace = db.namespaces.find_one({"_id": package_obj.namespace})
            namespace_obj = Namespace.from_json(namespace)

            author = db.users.find_one({"_id": package_obj.author})
            author_obj = User.from_json(author)
            
            package_obj.namespace = namespace_obj.namespace
            package_obj.author = author_obj.username
            search_packages.append({
                "name": package_obj.name,
                "namespace": package_obj.namespace,
                "author": package_obj.author,
                "description": package_obj.description,
                "tags": package_obj.tags,
                "updated_at": package_obj.updated_at,
            })

        return (
            jsonify(
                {"code": 200, "packages": search_packages, "total_pages": total_pages}
            ),
            200,
        )
    else:
        return (
            jsonify({"status": "error", "message": "packages not found", "code": 404}),
            404,
        )


@app.route("/packages", methods=["POST"])
@swag_from("documentation/package_upload.yaml", methods=["POST"])
@jwt_required()
def upload():
    upload_token = request.form.get("upload_token")
    package_name = request.form.get("package_name")
    package_version = request.form.get("package_version")
    package_license = request.form.get("package_license")
    dry_run = request.form.get("dry_run")
    tarball = request.files["tarball"]

    dry_run = True if dry_run == "true" else False

    if not upload_token:
        return jsonify({"code": 400, "message": "Upload token missing"}), 400

    if not package_name:
        return jsonify({"code": 400, "message": "Package name is missing"}), 400

    if not package_version:
        return jsonify({"code": 400, "message": "Package version is missing"}), 400

    if not package_license:
        return jsonify({"code": 400, "message": "Package license is missing"}), 400

    # Check whether version string is valid or not.
    if package_version == "0.0.0" or not is_valid_version_str(package_version):
        return jsonify({"code": 400, "message": "Version is not valid"}), 400

    # Check whether license identifier is valid or not.
    if not is_valid_license_identifier(license_str=package_license):
        return (
            jsonify(
                {
                    "code": 400,
                    "message": f"Invalid license identifier {package_license}. Please check the SPDX license identifier list.",
                }
            ),
            400,
        )

    # Find the document that contains the upload token.
    namespace_doc = db.namespaces.find_one(
        {"upload_tokens": {"$elemMatch": {"token": upload_token}}}
    )
    package_doc = db.packages.find_one(
        {"upload_tokens": {"$elemMatch": {"token": upload_token}}}
    )

    if not namespace_doc and not package_doc:
        return jsonify({"code": 401, "message": "Invalid upload token"}), 401

    if namespace_doc:
        namespace_obj = Namespace.from_json(namespace_doc)
        upload_token_doc = next(
            item
            for item in namespace_doc["upload_tokens"]
            if item["token"] == upload_token
        )
        package_doc = db.packages.find_one(
            {"name": package_name, "namespace": namespace_obj.id}
        )

    elif package_doc:
        package_obj = Package.from_json(package_doc)
        if package_obj.name != package_name:
            return jsonify({"code": 401, "message": "Invalid upload token"}), 401

        upload_token_doc = next(
            item
            for item in package_doc["upload_tokens"]
            if item["token"] == upload_token
        )
        namespace_doc = db.namespaces.find_one({"_id": package_doc["namespace"]})    

    # Check if the token is expired.
    # Expire the token after one week of it's creation.
    if check_token_expiry(upload_token_created_at=upload_token_doc["createdAt"]):
        return (
            jsonify(
                {
                    "code": 401,
                    "message": "Upload token has been expired. Please generate a new one",
                }
            ),
            401,
        )

    # Get the user connected to the upload token.
    user_id = upload_token_doc["createdBy"]
    user = db.users.find_one({"_id": user_id})

    if not user:
        return jsonify({"code": 404, "message": "User not found"}), 404
    
    user_obj = User.from_json(user)

    if not package_doc:
        # User should be either namespace maintainer or namespace admin to upload a package.
        if checkUserUnauthorizedForNamespaceTokenCreation(
            user_id=user_obj.id, namespace_obj=namespace_obj
        ):
            return jsonify({"code": 401, "message": "Unauthorized"}), 401
    else:
        # User should be either namespace maintainer or namespace admin or package maintainer to upload a package.
        package_obj = Package.from_json(package_doc)
        if checkUserUnauthorized(
            user_id=user_obj.id,
            package_namespace=namespace_obj,
            package_obj=package_obj,
        ):
            return jsonify({"message": "Unauthorized", "code": 401}), 401

    package_doc = db.packages.find_one(
        {"name": package_name, "namespace": namespace_obj.id}
    )

    if tarball.content_type not in [
        "application/gzip",
        "application/zip",
        "application/octet-stream",
        "application/x-tar",
    ]:
        return jsonify({"code": 400, "message": "Invalid file type"}), 400

    tarball_name = "{}-{}.tar.gz".format(package_name, package_version)

    package_data = {
        "repository": "Package Under Verification",
        "description": "Package Under Verification",
        "copyright": "Package Under Verification",
    }

    file_object_id = file_storage.put(
        tarball, content_type=tarball.content_type, filename=tarball_name
    )

    # No previous recorded versions of the package found.
    if not package_doc:
        try:
            package_obj = Package(
                name=package_name,
                namespace=namespace_obj.id,
                description=package_data["description"],
                homepage=package_data["homepage"],
                repository=package_data["repository"],
                copyright=package_data["copyright"],
                license=package_license,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                author=user_obj.id,
                maintainers=[user_obj.id],
                tags=["fortran", "fpm"],
                is_deprecated=False,
                versions=[],
            )
        except KeyError as e:
            return (
                jsonify(
                    {
                        "code": 400,
                        "message": f"Invalid package metadata. {e} is missing",
                    }
                ),
                400,
            )
        
        version_obj = Version(
            version=package_version,
            tarball=tarball_name,
            dependencies="Test dependencies",
            created_at=datetime.utcnow(),
            is_deprecated=False,
            download_url=f"/tarballs/{file_object_id}",
        )

        # Append the first version document.
        package_obj.versions.append(version_obj)

        if dry_run:
            return jsonify({"message": "Dry run Successful.", "code": 200}), 200

        db.packages.insert_one(package_obj.to_json())

        package = db.packages.find_one(
            {
                "name": package_name,
                "versions.version": package_version,
                "namespace": namespace_obj.id,
            }
        )

        # Add the package id to the namespace.
        update_namespace_obj_with_package_id(namespace_obj=namespace_obj, package=package)

        update_user_obj_with_package_id(user_obj, package["_id"])

        return jsonify({"message": "Package Uploaded Successfully.", "code": 200})
    else:
        # Check if version of the package already exists in the backend.
        package_version_doc = db.packages.find_one(
            {
                "name": package_name,
                "namespace": namespace_obj.id,
                "versions.version": package_version,
            }
        )

        if package_version_doc:
            return jsonify({"message": "Version already exists", "code": 400}), 400  

        package_obj = Package.from_json(package_doc)

        new_version = Version(
            version=package_version,
            tarball=tarball_name,
            dependencies="Test dependencies",
            created_at=datetime.utcnow(),
            is_deprecated=False,
            download_url=f"/tarballs/{file_object_id}",
        )


        package_obj.versions.append(new_version)
        
        package_obj.versions = sorted(
            package_obj.versions, key=lambda x: x.version
        )
        package_obj.updatedAt = datetime.utcnow()

        if dry_run:
            return jsonify({"message": "Dry run Successful.", "code": 200}), 200

        db.packages.update_one(
            {"_id": ObjectId(package_obj.id)},
            {"$set": package_obj.to_json()},
        )

        return jsonify({"message": "Package Uploaded Successfully.", "code": 200}), 200

def update_namespace_obj_with_package_id(namespace_obj, package):
    namespace_obj.packages.append(package["_id"])
    namespace_obj.updatedAt = datetime.utcnow()
    
    db.namespaces.update_one({"_id": namespace_obj.id}, {"$set": namespace_obj.to_json()})

def update_user_obj_with_package_id(user_obj, package_id):
    # Current user is the author of the package.
    user_obj.authorOf.append(package_id)

    db.users.update_one({"_id": user_obj.id}, {"$set": user_obj.to_json()})

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


@app.route("/tarballs/<oid>", methods=["GET"])
@swag_from("documentation/get_tarball.yaml", methods=["GET"])
def serve_gridfs_file(oid):
    try:
        file = file_storage.get(ObjectId(oid))

        package_version_doc = db.packages.update_one(
            {
                "versions.oid": oid,
            },
            {
                "$inc": {
                    f"downloads_stats.versions.{oid}": 1,
                    "downloads_stats.total_downloads": 1,
                    f"downloads_stats.dates.{str(datetime.now())[:10]}.{oid}": 1,
                    f"downloads_stats.dates.{str(datetime.now())[:10]}.total_downloads": 1,
                }
            },
        )
        if package_version_doc.modified_count > 0:
            # Return the file data as a Flask response object
            return send_file(
                file,
                download_name=file.filename,
                as_attachment=True,
                mimetype=file.content_type,
            )
        return jsonify({"message": "Package version not found", "code": 404}), 404

    except NoFile:
        abort(404)


def check_version(current_version, new_version):
    current_list = list(map(int, current_version.split(".")))
    new_list = list(map(int, new_version.split(".")))
    return new_list > current_list


@app.route("/packages/<namespace_name>/<package_name>", methods=["GET"])
@swag_from("documentation/get_package.yaml", methods=["GET"])
def get_package(namespace_name, package_name):
    # Get namespace from namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})
    namespace_obj = Namespace.from_json(namespace)

    # Check if namespace exists.
    if not namespace:
        return (
            jsonify({"status": "error", "message": "Namespace not found", "code": 404}),
            404,
        )

    # Get package from a package_name and namespace's id.
    package = db.packages.find_one(
        {"name": package_name, "namespace": namespace_obj.id}
    )

    # Check if package is not found.
    if not package:
        return jsonify({"message": "Package not found", "code": 404}), 404
    
    package_obj = Package.from_json(package)

    # Get the package author from id.
    package_author = db.users.find_one({"_id": package_obj.author})
    package_author_obj = User.from_json(package_author)

    # Only latest version of the package will be sent as a response.
    package_response_data = {
        "name": package_obj.name,
        "namespace": namespace_obj.namespace,
        "latest_version_data": package_obj.versions[-1].to_json(),
        "author": package_author_obj.username,
        "tags": package_obj.tags,
        "license": package_obj.license,
        "created_at": package_obj.created_at,
        "version_history": package_obj.to_json()["versions"],
        "updated_at": package_obj.updated_at,
        "description": package_obj.description,
        "ratings": round(sum(package_obj.ratings['users'].values())/len(package_obj.ratings['users']),3),
        "downloads": package_obj.downloads_stats,
    }

    return jsonify({"data": package_response_data, "code": 200})


@app.route("/packages/<namespace_name>/<package_name>/verify", methods=["POST"])
@swag_from("documentation/verify_user_role.yaml", methods=["POST"])
@jwt_required()
def verify_user_role(namespace_name, package_name):
    uuid = get_jwt_identity()

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"status": "error", "message": "Unauthorized", "code": 401}), 401

    namespace = db.namespaces.find_one({"namespace": namespace_name})

    if not namespace:
        return (
            jsonify({"status": "error", "message": "Namespace not found", "code": 404}),
            404,
        )

    package = db.packages.find_one(
        {"name": package_name, "namespace": namespace["_id"]}
    )

    if not package:
        return (
            jsonify({"status": "error", "message": "Package not found", "code": 404}),
            404,
        )
    
    user_obj = User.from_json(user)
    package_obj = Package.from_json(package)
    namespace_obj = Namespace.from_json(namespace)

    if (
        str(user_obj.id) in [str(obj_id) for obj_id in namespace_obj.maintainers]
        or str(user_obj.id) in [str(obj_id) for obj_id in namespace_obj.admins]
        or str(user_obj.id) in [str(obj_id) for obj_id in package_obj.maintainers]
    ):
        return jsonify({"status": "success", "code": 200, "isVerified": True}), 200
    else:
        return jsonify({"status": "error", "code": 401, "isVerified": False}), 401


@app.route("/packages/<namespace_name>/<package_name>/<version>", methods=["GET"])
@swag_from("documentation/get_version.yaml", methods=["GET"])
def get_package_from_version(namespace_name, package_name, version):
    # Get namespace from namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Check if namespace does not exists.
    if not namespace:
        return jsonify({"message": "Namespace not found", "code": 404}), 404
    
    namespace_obj = Namespace.from_json(namespace)

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
        return jsonify({"message": "Package not found", "code": 404}), 404

    else:
        package_obj = Package.from_json(package)

        # Get the package author from id.
        package_author = db.users.find_one({"_id": package_obj.author})

        package_author_obj = User.from_json(package_author)

        # Extract version data from the list of versions.
        version_history = package_obj.versions
        version_data = next(
            filter(lambda obj: obj.version == version, version_history), None
        )

        # Only queried version should be sent as response.
        package_response_data = {
            "name": package_obj.name,
            "namespace": namespace_obj.namespace,
            "author": package_author_obj.username,
            "tags": package_obj.tags,
            "license": package_obj.license,
            "created_at": package_obj.created_at,
            "version_data": version_data.to_json(),
            "updatedAt": package_obj.updated_at,
            "description": package_obj.description,
        }

        return jsonify({"data": package_response_data, "code": 200}), 200


@app.route("/packages/<namespace_name>/<package_name>/delete", methods=["POST"])
@swag_from("documentation/delete_package.yaml", methods=["POST"])
@jwt_required()
def delete_package(namespace_name, package_name):
    uuid = get_jwt_identity()

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404
    
    user_obj = User.from_json(user)

    # Check if the user is authorized to delete the package.
    if not "admin" in user_obj.roles:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "User is not authorized to delete the package",
                    "code": 401,
                }
            ),
            401,
        )

    # Get the namespace from the namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    if not namespace:
        return jsonify({"message": "Namespace not found", "code": 404}), 404

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
        return jsonify({"message": "Internal Server Error", "code": 500}), 500


@app.route(
    "/packages/<namespace_name>/<package_name>/<version>/delete", methods=["POST"]
)
@swag_from("documentation/delete_package_version.yaml", methods=["POST"])
@jwt_required()
def delete_package_version(namespace_name, package_name, version):
    uuid = get_jwt_identity()

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404
    
    user_obj = User.from_json(user)

    # Check if the user is authorized to delete the package.
    if not "admin" in user_obj.roles:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "User is not authorized to delete the package",
                    "code": 401,
                }
            ),
            401,
        )

    # Get the namespace from the namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Check if namespace does not exists.
    if not namespace:
        return jsonify({"message": "Namespace does not found", "code": 404}), 404

    # Perform the pull operation.
    result = db.packages.update_one(
        {"name": package_name, "namespace": namespace["_id"]},
        {"$pull": {"versions": {"version": version}}},
    )

    if result.matched_count:
        return jsonify({"message": "Package version deleted successfully"}), 200
    else:
        return (
            jsonify(
                {"status": "error", "message": "Package version not found", "code": 404}
            ),
            404,
        )


@app.route("/packages/<namespace_name>/<package_name>/uploadToken", methods=["POST"])
@swag_from("documentation/create_package_upload_token.yaml", methods=["POST"])
@jwt_required()
def create_token_upload_token_package(namespace_name, package_name):
    uuid = get_jwt_identity()

    # Get the user from uuid.
    user_doc = db.users.find_one({"uuid": uuid})

    if not user_doc:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401

    # Get the namespace from namespace_name.
    namespace_doc = db.namespaces.find_one({"namespace": namespace_name})

    if not namespace_doc:
        return jsonify({"code": 404, "message": "Namespace not found"}), 404
    
    namespace_obj = Namespace.from_json(namespace_doc)

    # Get the package from package_name & namespace_id.
    package_doc = db.packages.find_one(
        {"name": package_name, "namespace": namespace_obj.id}
    )

    if not package_doc:
        return jsonify({"code": 404, "message": "Package not found"}), 404
    
    package_obj = Package.from_json(package_doc)
    user_obj = User.from_json(user_doc)

    # Check if the user is authorized to generate package token.
    # Only package maintainers will have the option to generate tokens for a package.
    if not str(user_obj.id) in [
        str(obj_id) for obj_id in package_obj.maintainers
    ]:
        return (
            jsonify(
                {"code": 401, "message": "Only package maintainers can create tokens"}
            ),
            401,
        )

    # Generate the token.
    upload_token = generate_uuid()

    upload_token_obj = {
        "token": upload_token,
        "created_at": datetime.utcnow(),
        "created_by": user_doc["_id"],
    }

    db.packages.update_one(
        {"_id": package_obj.id}, {"$addToSet": {"upload_tokens": upload_token_obj}}
    )

    return (
        jsonify(
            {
                "code": 200,
                "message": "Upload token created successfully",
                "upload_token": upload_token,
            }
        ),
        200,
    )


@app.route("/packages/<namespace>/<package>/maintainers", methods=["GET"])
@swag_from("documentation/package_maintainers.yaml", methods=["GET"])
@jwt_required()
def package_maintainers(namespace, package):
    uuid = get_jwt_identity()
    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    user_obj = User.from_json(user)

    namespace_doc = db.namespaces.find_one({"namespace": namespace})

    if not namespace_doc:
        return jsonify({"message": "Namespace not found", "code": 404})
    
    namespace_obj = Namespace.from_json(namespace_doc)

    package_doc = db.packages.find_one(
        {"name": package, "namespace": namespace_obj.id}
    )

    if not package_doc:
        return jsonify({"message": "Package not found", "code": 404})
    
    package_obj = Package.from_json(package_doc)

    maintainers = []

    for i in package_obj.maintainers:
        maintainer = db.users.find_one({"_id": ObjectId(i)}, {"_id": 1, "username": 1})
        maintainer_obj = User.from_json(maintainer)
        maintainers.append(
            {"id": str(maintainer_obj.id), "username": maintainer_obj.username}
        )

    return jsonify({"code": 200, "users": maintainers}), 200


def sort_versions(versions):
    """
    Sorts the list of version in the reverse order. Such that the latest version comes at
    0th index.
    """
    return sorted(versions, key=lambda x: [int(i) for i in x.split(".")], reverse=True)


# This function checks if user is authorized to upload/update a package in a namespace.
def checkUserUnauthorized(user_id, package_namespace, package_obj):
    admins_id_list = [str(obj_id) for obj_id in package_namespace.admins]
    maintainers_id_list = [str(obj_id) for obj_id in package_namespace.maintainers]
    pkg_maintainers_id_list = [str(obj_id) for obj_id in package_obj.maintainers]
    str_user_id = str(user_id)
    return (
        str_user_id not in admins_id_list
        and str_user_id not in maintainers_id_list
        and str_user_id not in pkg_maintainers_id_list
    )


def checkUserUnauthorizedForNamespaceTokenCreation(user_id, namespace_obj):
    admins_id_list = [str(obj_id) for obj_id in namespace_obj.admins]
    maintainers_id_list = [str(obj_id) for obj_id in namespace_obj.maintainers]
    str_user_id = str(user_id)
    return str_user_id not in admins_id_list and str_user_id not in maintainers_id_list


@app.route("/ratings/<namespace>/<package>", methods=["POST"])
@swag_from("documentation/post_rating.yaml", methods=["POST"])
@jwt_required()
def post_ratings(namespace, package):
    uuid = get_jwt_identity()
    rating = request.form.get("rating")

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401

    if not rating:
        return jsonify({"code": 400, "message": "Rating is missing"}), 400

    if int(rating) < 1 or int(rating) > 5:
        return (
            jsonify({"code": 400, "message": "Rating should be between 1 and 5"}),
            400,
        )

    user = db.users.find_one({"uuid": uuid})
    namespace_doc = db.namespaces.find_one({"namespace": namespace})
    package_doc = db.packages.find_one(
        {"name": package, "namespace": namespace_doc["_id"]}
    )

    if not user or not namespace_doc or not package_doc:
        error_message = {
            "user": "User not found" if not user else None,
            "namespace": "Namespace not found" if not namespace_doc else None,
            "package": "Package not found" if not package_doc else None,
            "code": 404
        }
        return jsonify({"message": error_message}), 404

    if user["_id"] in package_doc["ratings"]["users"] and package_doc["ratings"][
        "users"
    ][user["_id"]] == int(rating):
        return jsonify({"message": "Ratings Submitted Successfully", "code": 200}), 200

    if user["_id"] in package_doc["ratings"]["users"] and package_doc["ratings"][
        "users"
    ][user["_id"]] != int(rating):
        package_version_doc = db.packages.update_one(
            {"name": package, "namespace": namespace_doc["_id"]},
            {
                "$set": {
                    f"ratings.users.{user['_id']}": int(rating),
                },
            },
        )
        return jsonify({"message": "Ratings Updated Successfully", "code": 200}), 200

    package_version_doc = db.packages.update_one(
        {"name": package, "namespace": namespace_doc["_id"]},
        {
            "$set": {
                f"ratings.users.{user['_id']}": int(rating),
            },
            "$inc": {
                "ratings.total_count": 1,
            },
        },
    )
    return jsonify({"message": "Ratings Submitted Successfully", "code": 200}), 200


@app.route("/report/<namespace>/<package>", methods=["POST"])
@swag_from("documentation/post_malicious.yaml", methods=["POST"])
@jwt_required()
def post_malicious(namespace, package):
    uuid = get_jwt_identity()
    reason = request.form.get("reason")

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401

    if not reason:
        return jsonify({"code": 400, "message": "Reason is missing"}), 400
    
    reason = reason.strip()

    if len(reason) < 10:
        return (
            jsonify({"code": 400, "message": "Reason should atleast be 10 characters"}),
            400,
        )

    user = db.users.find_one({"uuid": uuid})
    namespace_doc = db.namespaces.find_one({"namespace": namespace})
    package_doc = db.packages.find_one(
        {"name": package, "namespace": namespace_doc["_id"]}
    )

    if not user or not namespace_doc or not package_doc:
        error_message = {
            "user": "User not found" if not user else None,
            "namespace": "Namespace not found" if not namespace_doc else None,
            "package": "Package not found" if not package_doc else None,
            "code": 404
        }
        return jsonify({"message": error_message}), 404

    if user["_id"] in package_doc["malicious_report"]["users"] and package_doc["malicious_report"][
        "users"
    ][user["_id"]]['reason'] == str(reason):
        return jsonify({"message": "Malicious Report Submitted Successfully", "code": 200}), 200

    if user["_id"] in package_doc["malicious_report"]["users"] and package_doc["malicious_report"][
        "users"
    ][user["_id"]]['reason'] != str(reason):
        package_version_doc = db.packages.update_one(
            {"name": package, "namespace": namespace_doc["_id"]},
            {
                "$set": {
                    f"malicious_report.users.{user['_id']}": { 'reason': str(reason), 'isViewed': False },
                    "malicious_report.isViewed": False,

                },
            },
        )
        return jsonify({"message": "Malicious Report Updated Successfully", "code": 200}), 200

    package_version_doc = db.packages.update_one(
        {"name": package, "namespace": namespace_doc["_id"]},
        {
            "$set": {
                f"malicious_report.users.{user['_id']}": { 'reason': str(reason), 'isViewed': False },
                "malicious_report.isViewed": False,
            }
        },
    )
    return jsonify({"message": "Malicious Report Submitted Successfully", "code": 200}), 200

@app.route("/report/view", methods=["GET"])
@swag_from("documentation/view_report.yaml", methods=["GET"])
@jwt_required()
def view_report():
    uuid = get_jwt_identity()

    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        user = db.users.find_one({"uuid": uuid})

    if "admin" in user["roles"]:
        non_viewed_reports = list()
        malicious_reports = db.packages.find({"malicious_reports.isViewed": False})
        for package in list(malicious_reports):
            for user_id, report in package.get("malicious_report", {}).get("users", {}).items():
                if not report.get("isViewed", False):
                    report['name'] = db.users.find_one({"_id": ObjectId(user_id)}, {"username": 1})["username"]
                    del report["isViewed"]
                    non_viewed_reports.append(report)

        return jsonify({"message": "Malicious Reports fetched Successfully", "code": 200, "reports": non_viewed_reports}), 200


    return jsonify({"message": "Unauthorized", "code": 401}), 401

