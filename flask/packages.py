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
import tarfile
import io
import toml
from flasgger.utils import swag_from
from urllib.parse import unquote
import math
import semantic_version
from license_expression import get_spdx_licensing
# import validate_package


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
        upload_token_doc = next(
            item
            for item in namespace_doc["upload_tokens"]
            if item["token"] == upload_token
        )
        package_doc = db.packages.find_one(
            {"name": package_name, "namespace": namespace_doc["_id"]}
        )

    elif package_doc:
        if package_doc["name"] != package_name:
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

    if not package_doc:
        # User should be either namespace maintainer or namespace admin to upload a package.
        if checkUserUnauthorizedForNamespaceTokenCreation(
            user_id=user["_id"], namespace_doc=namespace_doc
        ):
            return jsonify({"code": 401, "message": "Unauthorized"}), 401
    else:
        # User should be either namespace maintainer or namespace admin or package maintainer to upload a package.
        if checkUserUnauthorized(
            user_id=user["_id"],
            package_namespace=namespace_doc,
            package_doc=package_doc,
        ):
            return jsonify({"message": "Unauthorized", "code": 401}), 401

    package_doc = db.packages.find_one(
        {"name": package_name, "namespace": namespace_doc["_id"]}
    )

    if tarball.content_type not in ["application/gzip", "application/zip","application/octet-stream"]:
        return jsonify({"code": 400, "message": "Invalid file type"}), 400

    tarball_name = "{}-{}.tar.gz".format(package_name, package_version)
    # Upload the tarball to the Grid FS storage.

    # try: TODO: Enable this after Validation is Enabled
    #     zipball, tarball = get_file_object(tarball)
    # except Exception as e:
    #     return jsonify({"code": 400, "message": "Invalid package tarball."}), 400

    # zipfile_object_id = file_storage.put(
    #     zipball, content_type=zipball.content_type, filename=tarball_name + ".zip"
    # )
    # tarfile_object_id = file_storage.put(
    #     tarball, content_type=tarball.content_type, filename=tarball_name + ".tar.gz"
    # )
    file_object_id = file_storage.put(
        tarball, content_type=tarball.content_type, filename=tarball_name
    )

    # Extract the package metadata from the tarball's fpm.toml file.
    try:
        package_data = extract_fpm_toml(tarball)
    except Exception as e:
        return jsonify({"code": 400, "message": "Invalid package tarball."}), 400

    # TODO: Uncomment this when the package validation is enabled
    # validate the package with fpm

    # valid_package = validate_package.validate_package(tarball,"{}-{}".format(package_name, package_version))
    # if not valid_package:
    #     return jsonify({"status": "error", "message": "Invalid package", "code": 400}), 400

    # No previous recorded versions of the package found.
    if not package_doc:
        try:
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
                "copyright": package_data["copyright"],
                "tags": ["fortran", "fpm"],
                "isDeprecated": False,
            }
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

        version_obj = {
            "version": package_version,
            "tarball": tarball_name,
            "dependencies": "Test dependencies",
            "createdAt": datetime.utcnow(),
            "isDeprecated": False,
            # "download_url_zip": f"/tarballs/{zipfile_object_id}",  TODO: Uncomment this when the package validation is enabled
            # "download_url_tar": f"/tarballs/{tarfile_object_id}",
        }

        package_obj["versions"] = []

        # Append the first version document.
        package_obj["versions"].append(version_obj)

        if dry_run:
            return jsonify({"message": "Dry run Successful.", "code": 200})

        db.packages.insert_one(package_obj)

        package = db.packages.find_one(
            {
                "name": package_name,
                "versions.version": package_version,
                "namespace": namespace_doc["_id"],
            }
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
        package_version_doc = db.packages.find_one(
            {
                "name": package_name,
                "namespace": namespace_doc["_id"],
                "versions.version": package_version,
            }
        )

        if package_version_doc:
            return jsonify({"message": "Version already exists", "code": 400}), 400

        new_version = {
            "tarball": tarball_name,
            "version": package_version,
            "dependencies": "Test dependencies",
            "isDeprecated": False,
            "createdAt": datetime.utcnow(),
            "download_url": f"/tarballs/{file_object_id}",
            # "download_url_zip": f"/tarballs/{zipfile_object_id}",
            # "download_url_tar": f"/tarballs/{tarfile_object_id}",
        }

        package_doc["versions"].append(new_version)
        package_doc["versions"] = sorted(
            package_doc["versions"], key=lambda x: x["version"]
        )
        package_doc["updatedAt"] = datetime.utcnow()

        if dry_run:
            return jsonify({"message": "Dry run Successful.", "code": 200}), 200

        db.packages.update_one(
            {"_id": package_doc["_id"]},
            {"$set": package_doc},
        )

        return jsonify({"message": "Package Uploaded Successfully.", "code": 200}), 200


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
@swag_from("documentation/get_tarball.yaml", methods=["GET"])
def serve_gridfs_file(oid):
    try:
        file = file_storage.get(ObjectId(oid))

        # Return the file data as a Flask response object
        return send_file(
            file,
            download_name=file.filename,
            as_attachment=True,
            mimetype=file.content_type,
        )
    except NoFile:
        abort(404)

def check_version(current_version, new_version):
    current_list = list(map(int, current_version.split(".")))
    new_list = list(map(int, new_version.split(".")))
    return new_list > current_list


@app.route("/packages/<namespace_name>/<package_name>", methods=["GET", "POST"])
@swag_from("documentation/get_package.yaml", methods=["GET"])
def get_package(namespace_name, package_name):
    # Get namespace from namespace name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # Check if namespace exists.
    if not namespace:
        return (
            jsonify({"status": "error", "message": "Namespace not found", "code": 404}),
            404,
        )

    # Get package from a package_name and namespace's id.
    package = db.packages.find_one(
        {"name": package_name, "namespace": namespace["_id"]}
    )

    # Check if package is not found.
    if not package:
        return jsonify({"message": "Package not found", "code": 404}), 404

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

 
@app.route("/packages/<namespace_name>/<package_name>/verify", methods=["POST"])
@swag_from("documentation/verify_user_role.yaml", methods=["POST"])
def verify_user_role(namespace_name, package_name):
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized", "code": 401}), 401

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

    if (
        str(user["_id"]) in [str(obj_id) for obj_id in namespace["maintainers"]]
        or str(user["_id"]) in [str(obj_id) for obj_id in namespace["admins"]]
        or str(user["_id"]) in [str(obj_id) for obj_id in package["maintainers"]]
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

        return jsonify({"data": package_response_data, "code": 200}), 200


@app.route("/packages/<namespace_name>/<package_name>/delete", methods=["POST"])
@swag_from("documentation/delete_package.yaml", methods=["POST"])
def delete_package(namespace_name, package_name):
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    # Check if the user is authorized to delete the package.
    if not "admin" in user["roles"]:
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
def delete_package_version(namespace_name, package_name, version):
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"status": "error", "message": "Unauthorized", "code": 401}), 401

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    # Check if the user is authorized to delete the package.
    if not "admin" in user["roles"]:
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
def create_token_upload_token_package(namespace_name, package_name):
    # Verify the uuid.
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401

    # Get the user from uuid.
    user_doc = db.users.find_one({"uuid": uuid})

    if not user_doc:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401

    # Get the namespace from namespace_name.
    namespace_doc = db.namespaces.find_one({"namespace": namespace_name})

    if not namespace_doc:
        return jsonify({"code": 404, "message": "Namespace not found"}), 404

    # Get the package from package_name & namespace_id.
    package_doc = db.packages.find_one(
        {"name": package_name, "namespace": namespace_doc["_id"]}
    )

    if not package_doc:
        return jsonify({"code": 404, "message": "Package not found"}), 404

    # Check if the user is authorized to generate package token.
    # Only package maintainers will have the option to generate tokens for a package.
    if not str(user_doc["_id"]) in [
        str(obj_id) for obj_id in package_doc["maintainers"]
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
        "createdAt": datetime.utcnow(),
        "createdBy": user_doc["_id"],
    }

    db.packages.update_one(
        {"_id": package_doc["_id"]}, {"$addToSet": {"upload_tokens": upload_token_obj}}
    )

    return (
        jsonify(
            {
                "code": 200,
                "message": "Upload token created successfully",
                "uploadToken": upload_token,
            }
        ),
        200,
    )

@app.route("/packages/<namespace>/<package>/maintainers", methods=["GET"])
@swag_from("documentation/package_maintainers.yaml", methods=["GET"])
def package_maintainers(namespace, package):
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401

    namespace_doc = db.namespaces.find_one({"namespace": namespace})

    if not namespace_doc:
        return jsonify({"message": "Namespace not found", "code": 404})

    package_doc = db.packages.find_one(
        {"name": package, "namespace": namespace_doc["_id"]}
    )

    if not package_doc:
        return jsonify({"message": "Package not found", "code": 404})

    maintainers = []

    for i in package_doc["maintainers"]:
        maintainer = db.users.find_one({"_id": i}, {"_id": 1, "username": 1})
        maintainers.append(
            {"id": str(maintainer["_id"]), "username": maintainer["username"]}
        )

    return jsonify({"code": 200, "users": maintainers}), 200


def sort_versions(versions):
    """
    Sorts the list of version in the reverse order. Such that the latest version comes at
    0th index.
    """
    return sorted(versions, key=lambda x: [int(i) for i in x.split(".")], reverse=True)


# This function checks if user is authorized to upload/update a package in a namespace.
def checkUserUnauthorized(user_id, package_namespace, package_doc):
    admins_id_list = [str(obj_id) for obj_id in package_namespace["admins"]]
    maintainers_id_list = [str(obj_id) for obj_id in package_namespace["maintainers"]]
    pkg_maintainers_id_list = [str(obj_id) for obj_id in package_doc["maintainers"]]
    str_user_id = str(user_id)
    return (
        str_user_id not in admins_id_list
        and str_user_id not in maintainers_id_list
        and str_user_id not in pkg_maintainers_id_list
    )


def checkUserUnauthorizedForNamespaceTokenCreation(user_id, namespace_doc):
    admins_id_list = [str(obj_id) for obj_id in namespace_doc["admins"]]
    maintainers_id_list = [str(obj_id) for obj_id in namespace_doc["maintainers"]]
    str_user_id = str(user_id)
    return str_user_id not in admins_id_list and str_user_id not in maintainers_id_list


def extract_fpm_toml(file_obj):
    tar = tarfile.open(fileobj=file_obj, mode='r')

    fpm_toml_file = None
    for file in tar.getmembers():
        if file.name == 'fpm.toml':
            fpm_toml_file = file
            break

    if fpm_toml_file is None:
        raise ValueError("fpm.toml file not found in the tarball.")

    extracted_file = tar.extractfile(fpm_toml_file)
    toml_data = extracted_file.read()
    tar.close()
    parsed_toml = toml.loads(toml_data)
    return parsed_toml

def convert_zip_to_tar(zip_file):
    tar_file = io.BytesIO()
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        with tarfile.open(fileobj=tar_file, mode='w') as tar_ref:
            for file_name in zip_ref.namelist():
                file_data = zip_ref.read(file_name)
                tar_info = tarfile.TarInfo(name=file_name)
                tar_info.size = len(file_data)
                tar_ref.addfile(tar_info, fileobj=io.BytesIO(file_data))
    
    tar_file.seek(0)  # Reset the file position for reading    
    return tar_file


def convert_to_zip(file_obj):
    with tarfile.open(file_obj, "r:gz") as tar:
        tar.extractall()
        with zipfile.ZipFile("package.zip", "w") as zip_ref:
            zip_ref.write("fpm.toml")
            zip_ref.write("package")
    return zip_ref


def get_file_object(file_obj):
    if file_obj.content_type == "application/zip":
        return file_obj, convert_zip_to_tar(file_obj)
    elif file_obj.content_type == "application/gzip":
        return convert_to_zip(file_obj), file_obj
    else:
        raise Exception("Invalid file type")
