import re
from app import app
from mongo import db
from flask import request, jsonify
from app import swagger
from flasgger.utils import swag_from
from packages import checkUserUnauthorized

from datetime import datetime
from auth import generate_uuid

@app.route("/namespaces", methods=["POST"])
def create_namespace():
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    # Get the user document from the uuid.
    user_doc = db.users.find_one({"uuid": uuid})

    if not user_doc:
        return jsonify({"code":  401, "message": "Unauthorized"}), 401
    
    namespace_name = request.form.get("namespace")

    if not namespace_name:
        return jsonify({"code": 400, "message": "Please enter namespace name"}), 400
    
    pattern = r'^[a-zA-Z0-9_-]+$'

    # Make sure namespace name only contains [a-z], [A-Z], [0-9], - and _ characters.
    if not re.match(pattern, namespace_name):
        return jsonify({"code": 400, "message": "Namespace name can only include (a-z), (A-Z), (0-9), - and _"}), 400

    # Get the namespace document from the namespace name.
    # To check if already a namespace exists by this name.
    namespace_doc = db.namespaces.find_one({"namespace": namespace_name})

    # Check if namespace already exists.
    if namespace_doc:
        return jsonify({"code": 400, "message": "Namespace already exists"}), 400

    namespace_obj = {
        "namespace": namespace_name,
        "createdAt": datetime.utcnow(),
        "author": user_doc["_id"],
        "maintainers": [user_doc["_id"]],
        "admins": [user_doc["_id"]]
    }

    db.namespaces.insert_one(namespace_obj)

    return jsonify({"code": 200, "message": "Namespace created successfully"}), 200

@app.route("/namespaces/<namespace_name>/uploadToken", methods=["POST"])
def create_upload_token(namespace_name):
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    user_doc = db.users.find_one({"uuid": uuid})

    if not user_doc:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    # Get the namespace from namespace_name.
    namespace_doc = db.namespaces.find_one({"namespace": namespace_name})

    if not namespace_doc:
        return jsonify({"code": 404, "message": "Namespace not found"}), 404
    
    # Only namespace maintainers or admins can generate an upload token for now.
    if checkUserUnauthorized(user_id=user_doc["_id"], package_namespace=namespace_doc):
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    # Generate an access token for accessing the namespace.
    upload_token = generate_uuid()
    
    upload_token_obj = {
        "token": upload_token,
        "createdAt": datetime.utcnow(),
        "createdBy": user_doc["_id"]
    }

    db.namespaces.update_one(
        {"namespace": namespace_name},
        {"$addToSet": {"upload_tokens": upload_token_obj}}
    )

    return jsonify({"code": 200, "message": "Upload token created", "uploadToken": upload_token})

@app.route("/packages/<namespace_name>/delete", methods=["POST"])
def delete_namespace(namespace_name):
    uuid = request.form.get("uuid")

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401

    user = db.users.find_one({"uuid": uuid})

    # Check if the user is authorized to delete the package.
    if not "admin" in user["roles"]:
        return (
            jsonify(
                {
                    "code": 401,
                    "message": "User is not authorized to delete the namespace",
                }
            ),
            401,
        )

    # Get the namespace from the namespace_name.
    namespace = db.namespaces.find_one({"namespace": namespace_name})

    # If namespace is not found. Return 404.
    if not namespace:
        return jsonify({"message": "Namespace not found", "code": 404})

    namespace_deleted = db.namespaces.delete_one({"namespace": namespace["_id"]})

    if namespace_deleted.deleted_count > 0:
        return jsonify({"message": "Namespace deleted successfully","code":200}), 200
    else:
        return jsonify({"message": "Internal Server Error", "code": 500}),200
    

@app.route("/namespace/<namespace>", methods=["GET"])
def namespace_packages(namespace):
    namespace_document = db.namespaces.find_one({"namespace": namespace})

    if not namespace_document:
        return jsonify({"code": 404, "message": "Namespace not found"}), 404

    packages = []
    for i in namespace_document["packages"]:
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
                "createdAt": namespace_document["createdAt"],
            }
        ),
        200,
    )