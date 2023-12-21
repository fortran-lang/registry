import re
from app import app
from mongo import db
from flask import request, jsonify
from app import swagger
from flasgger.utils import swag_from
from packages import checkUserUnauthorizedForNamespaceTokenCreation
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.namespace import Namespace
from models.user import User

from datetime import datetime
from auth import generate_uuid

# Regular expression pattern for namespace name validation.
NAMESPACE_NAME_PATTERN = r'^[a-zA-Z0-9_-]+$'

@app.route("/namespaces", methods=["POST"])
@swag_from("documentation/create_namespace.yaml", methods=["POST"])
@jwt_required()
def create_namespace():
    uuid = get_jwt_identity()
    
    # Get the user document from the uuid.
    user_doc = db.users.find_one({"uuid": uuid})

    if not user_doc:
        return jsonify({"code":  401, "message": "Unauthorized"}), 401
    
    user_obj = User.from_json(user_doc)
    
    namespace_name = request.form.get("namespace")
    namespace_description = request.form.get("namespace_description")

    if not namespace_name:
        return jsonify({"code": 400, "message": "Please enter namespace name"}), 400
    
    if not namespace_description:
        return jsonify({"code": 400, "message": "Please enter namespace description"}), 400

    # Make sure namespace name only contains [a-z], [A-Z], [0-9], - and _ characters.
    if not re.match(NAMESPACE_NAME_PATTERN, namespace_name):
        return jsonify({"code": 400, "message": "Namespace name can only include (a-z), (A-Z), (0-9), - and _"}), 400

    # Get the namespace document from the namespace name.
    # To check if already a namespace exists by this name.
    namespace_doc = db.namespaces.find_one({"namespace": namespace_name})

    # Check if namespace already exists.
    if namespace_doc:
        return jsonify({"code": 400, "message": "Namespace already exists"}), 400
    
    namespace_obj = Namespace(
        namespace=namespace_name,
        description=namespace_description,
        author=user_obj.id,
        maintainers=[user_obj.id],
        admins=[user_obj.id],
        packages=[],
    ).to_json()

    db.namespaces.insert_one(namespace_obj)

    return jsonify({"code": 200, "message": "Namespace created successfully"}), 200

@app.route("/namespaces/<namespace_name>/uploadToken", methods=["POST"])
@swag_from("documentation/create_namespace_upload_token.yaml", methods=["POST"])
@jwt_required()
def create_upload_token(namespace_name):
    uuid = get_jwt_identity()

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    user_doc = db.users.find_one({"uuid": uuid})

    if not user_doc:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    user_obj = User.from_json(user_doc)
    
    # Get the namespace from namespace_name.
    namespace_doc = db.namespaces.find_one({"namespace": namespace_name})

    if not namespace_doc:
        return jsonify({"code": 404, "message": "Namespace not found"}), 404
    
    namespace_obj = Namespace.from_json(namespace_doc)
    
    # Only namespace maintainers or admins can generate an upload token for now.
    if checkUserUnauthorizedForNamespaceTokenCreation(user_id=user_obj.id, namespace_obj=namespace_obj):
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    # Generate an upload token for upload packages to the namespace.
    upload_token = generate_uuid()
    
    upload_token_obj = {
        "token": upload_token,
        "createdAt": datetime.utcnow(),
        "createdBy": user_obj.id
    }

    db.namespaces.update_one(
        {"namespace": namespace_name},
        {"$addToSet": {"upload_tokens": upload_token_obj}}
    )

    return jsonify({"code": 200, "message": "Upload token created", "uploadToken": upload_token})

@app.route("/namespace/<namespace_name>/delete", methods=["POST"])
@swag_from("documentation/delete_namespace.yaml", methods=["POST"])
@jwt_required()
def delete_namespace(namespace_name):
    uuid = get_jwt_identity()

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401

    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"code": 404, "message": "User not found"}), 404
    
    user_obj = User.from_json(user)

    # Check if the user is authorized to delete the package.
    if not "admin" in user_obj.roles:
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
    
    namespace_obj = Namespace.from_json(namespace)

    namespace_deleted = db.namespaces.delete_one({"namespace": namespace_obj.id})

    if namespace_deleted.deleted_count > 0:
        return jsonify({"message": "Namespace deleted successfully","code":200}), 200
    else:
        return jsonify({"message": "Internal Server Error", "code": 500}),200
    

@app.route("/namespace/<namespace>", methods=["GET"])
@swag_from("documentation/get_namespace_packages.yaml", methods=["GET"])
def namespace_packages(namespace):
    namespace_document = db.namespaces.find_one({"namespace": namespace})

    if not namespace_document:
        return jsonify({"code": 404, "message": "Namespace not found"}), 404

    namespace_obj = Namespace.from_json(namespace_document)

    packages = []
    for i in namespace_obj.packages:
        package = db.packages.find_one(
            {"_id": i},
            {
                "_id": 0,
                "name": 1,
                "description": 1,
                "author": 1,
                "updatedAt": 1,
            },
        )
        
        # Get the package author name.
        author = db.users.find_one({"_id": package["author"]})

        author_obj = User.from_json(author)
        
        packages.append({
            "namespace" : namespace,
            "name": package["name"],
            "description": package["description"],
            "author": author_obj.username,
            "updatedAt": package["updatedAt"],
        })
            
    return (
        jsonify(
            {
                "code": 200,
                "packages": packages,
                "createdAt": namespace_obj.createdAt,
            }
        ),
        200,
    )

@app.route("/namespaces/<namespace>/admins", methods=["POST"])
@swag_from("documentation/get_namespace_admins.yaml", methods=["POST"])
@jwt_required()
def namespace_admins(namespace):
    uuid = get_jwt_identity()

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"code": 404, "message": "User not found"}), 404
    
    user_obj = User.from_json(user)

    namespace_doc = db.namespaces.find_one({"namespace": namespace})

    if not namespace_doc:
        return jsonify({"code": 404, "message": "Namespace not found"}), 404  

    namespace_obj = Namespace.from_json(namespace_doc)
    
    if not user_obj.id in namespace_obj.admins and not user_obj.id in namespace_obj.maintainers:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    admins = []

    for i in namespace_obj.admins:
        admin = db.users.find_one({"_id": i}, {"_id": 1, "username": 1})
        admin_obj = User.from_json(admin)
        admins.append({
            "id": str(admin_obj.id),
            "username": admin_obj.username
        })
    
    return jsonify({"code": 200, "users": admins}), 200

@app.route("/namespaces/<namespace>/maintainers", methods=["POST"])
@swag_from("documentation/get_namespace_maintainers.yaml", methods=["POST"])
@jwt_required()
def namespace_maintainers(namespace):
    uuid = get_jwt_identity()

    if not uuid:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401
    
    user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"code": 404, "message": "User not found"}), 404

    namespace_doc = db.namespaces.find_one({"namespace": namespace})

    if not namespace_doc:
        return jsonify({"code": 404, "message": "Namespace not found"}), 404
    
    namespace_obj = Namespace.from_json(namespace_doc)
    user_obj = User.from_json(user)
    
    if not user_obj.id in namespace_obj.admins and not user_obj.id in namespace_obj.maintainers:
        return jsonify({"code": 401, "message": "Unauthorized"}), 401    
    
    maintainers = []

    for i in namespace_obj.maintainers:
        maintainer = db.users.find_one({"_id": i}, {"_id": 1, "username": 1})
        maintainer_obj = User.from_json(maintainer)
        maintainers.append({
            "id": str(maintainer_obj.id),
            "username": maintainer_obj.username
        })

    return jsonify({"code": 200, "users": maintainers}), 200