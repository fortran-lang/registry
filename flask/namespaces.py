from app import app
from mongo import db
from flask import request, jsonify
from app import swagger
from flasgger.utils import swag_from

@app.route("/namespace/<namespace_name>/delete", methods=["POST"])
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