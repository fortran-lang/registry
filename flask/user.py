import os
from dotenv import load_dotenv
import hashlib
from app import app
from mongo import db
from flask import request, jsonify
from app import swagger
from flasgger.utils import swag_from
from auth import forgot_password

load_dotenv()

try:
    salt = os.getenv("SALT")
except KeyError as err:
    print("Add SALT to .env file")


@app.route("/users/<username>", methods=["GET"])
@swag_from("documentation/user.yaml", methods=["GET"])
def profile(username):
    user = db.users.find_one({"username": username})
    if user:
        packages = db.packages.find(
            {"$or": [{"author": user["_id"]}, {"maintainers": user["_id"]}]},
        )

        response_packages = []
        if packages:
            for package in packages:
                # Get namespace from namespace id.
                namespace = db.namespaces.find_one({"_id": package["namespace"]})
                user = db.users.find_one({"_id": package["author"]})
                namespace = db.namespaces.find_one({"_id": package["namespace"]})
                response_packages.append(
                    {
                        "name": package["name"],
                        "namespace": namespace["namespace"],
                        "description": package["description"],
                        "updatedAt": package["updatedAt"],
                        "author": user["username"],
                    }
                )
        user_account = {
            "username": user["username"],
            "email": user["email"],
            "createdAt": user["createdAt"],
            "packages": response_packages,
        }
        return (
            jsonify(
                {
                    "message": "User found",
                    "user": user_account,
                    "packages": response_packages,
                    "code": 200,
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "User not found", "code": 404}), 404


@app.route("/users/delete", methods=["POST"])
@swag_from("documentation/delete_user.yaml", methods=["POST"])
def delete_user():
    uuid = request.form.get("uuid")
    password = request.form.get("password")
    username = request.form.get("username")

    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return "Invalid email or password", 401

    if password:
        password += salt
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password != user["password"]:
            return jsonify({"message": "Invalid email or password", "code": 401}), 401
        else:
            db.users.delete_one({"uuid": uuid})
            return jsonify({"message": "User deleted", "code": 200}), 200

    elif username and "admin" in user["roles"]:
        delete_user = db.users.find_one({"username": username})
        if delete_user:
            db.users.delete_one({"username": username})
            return jsonify({"message": "User deleted", "code": 200}), 200
        else:
            return jsonify({"message": "User not found", "code": 404}), 404

    else:
        return jsonify({"message": "Unauthorized", "code": 401}), 401


@app.route("/users/account", methods=["POST"])
@swag_from("documentation/account.yaml", methods=["POST"])
def account():
    uuid = request.form.get("uuid")
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    user_account = {
        "username": user["username"],
        "email": user["email"],
        "createdAt": user["createdAt"],
        "loginAt": user["loginAt"],
        "lastLogout": user["lastLogout"],
    }
    return jsonify({"message": "User Found", "user": user_account, "code": 200}), 200


@app.route("/users/admin", methods=["POST"])
@swag_from("documentation/admin.yaml", methods=["POST"])
def admin():
    uuid = request.form.get("uuid")
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404
    
    if "admin" not in user["roles"]:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        return (
            jsonify({"message": "User is admin", "isAdmin": "true", "code": 200}),
            200,
        )


@app.route("/users/admin/transfer", methods=["POST"])
@swag_from("documentation/admin.yaml", methods=["POST"])
def transfer_account():
    uuid = request.form.get("uuid")
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    if "admin" not in user["roles"]:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        old_user = request.form.get("old_username")
        new_user = request.form.get("new_username")
        new_email = request.form.get("new_email")
        db.users.update_one(
            {"username": old_user},
            {
                "$set": {
                    "email": new_email,
                    "username": new_user,
                    "uuid": "",
                    "loggedCount": 0,
                    "loginAt": None,
                    "lastLogout": None,
                }
            },
        )
        forgot_password(new_email)
        return (
            jsonify(
                {
                    "message": "Account Transfer Successful and Password reset request sent.",
                    "code": 200,
                }
            ),
            200,
        )

@app.route("/<username>/maintainer", methods=["POST"])
def add_maintainers_to_package(username):
    uuid = request.form.get("uuid")
    username_to_be_added = request.form.get("username")
    package = request.form.get("package")
    namespace = request.form.get("namespace")

    # Validating the data coming with request.
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    if not username_to_be_added:
        return jsonify({"message": "Please enter the username to be added", "code": 400}), 400
    
    if not package:
        return jsonify({"message": "Please enter the package name", "code": 400}), 400
    
    if not namespace:
        return jsonify({"message": "Please enter the namespace name", "code": 400}), 400
    
    # Get the user from the database using uuid.
    user = db.users.find_one({"uuid": uuid})

    # Check if current user is authorized to access this API.
    if not user or user["username"] != username:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    # Get the namespace from the database.
    package_namespace = db.namespaces.find_one({"namespace": namespace})

    # Check if namespace does not exists.
    if not package_namespace:
        return jsonify({"message": "Namespace not found", "code": 404}), 404
    
    # Get the package in the namespace.
    curr_package = db.packages.find_one({"name": package, "namespace": package_namespace["_id"]})

    # Check if the package does not exists.
    if not curr_package:
        return jsonify({"message": "Package not found", "code": 404}), 404

    # Check if the current user has authority to add maintainers.
    if not checkIsMaintainer(user_id=user["_id"], package=curr_package) and not checkIsNamespaceAdmin(user_id=user["_id"], namespace=package_namespace):
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    # Get the user to be added using the username received in the request body.
    user_to_be_added = db.users.find_one({"username": username_to_be_added})

    if not user_to_be_added:
        return jsonify({"message": "Username to be added as a maintainer not found", "code": 404})

    # Update the document only if the user_to_be_added["_id"] is not already in the maintainers list.
    result = db.packages.update_one(
        {"name": package, "namespace": package_namespace["_id"]},
        {"$addToSet": {"maintainers": user_to_be_added["_id"]}}
    )

    # package_id gets added to the maintainerOf list in user document.
    db.users.update_one(
        {"username": username_to_be_added}, 
        {"$addToSet": {"maintainerOf": curr_package["_id"]}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Maintainer added successfully", "code": 200}), 200
    else:
        return jsonify({"message": "Maintainer already added", "code": 200}), 200
    
@app.route("/<username>/maintainer/remove", methods=["POST"])
def remove_maintainers_from_package(username):
    uuid = request.form.get("uuid")
    username_to_be_removed = request.form.get("username")
    package = request.form.get("package")
    namespace = request.form.get("namespace")

    # Validating the data coming with request.
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    if not username_to_be_removed:
        return jsonify({"message": "Please enter the username to be removed", "code": 400}), 400
    
    if not package:
        return jsonify({"message": "Please enter the package name", "code": 400}), 400
    
    if not namespace:
        return jsonify({"message": "Please enter the namespace name", "code": 400}), 400
    
    # Get the user from the database using uuid.
    user = db.users.find_one({"uuid": uuid})

    # Check if current user is authorized to access this API.
    if not user or user["username"] != username:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    # Get the namespace from the database.
    package_namespace = db.namespaces.find_one({"namespace": namespace})

    # Check if namespace does not exists.
    if not package_namespace:
        return jsonify({"message": "Namespace not found", "code": 404}), 404
    
    # Get the package in the namespace.
    curr_package = db.packages.find_one({"name": package, "namespace": package_namespace["_id"]})

    # Check if the package does not exists.
    if not curr_package:
        return jsonify({"message": "Package not found", "code": 404}), 404

    # Check if the current user has authority to remove maintainers.
    if not checkIsNamespaceAdmin(user_id=user["_id"], namespace=package_namespace):
        return jsonify({"message": "User is not authorized to remove maintainers", "code": 401}), 401
    
    # Get the user to be removed using the username received in the request body.
    user_to_be_removed = db.users.find_one({"username": username_to_be_removed})

    if not user_to_be_removed:
        return jsonify({"message": "Username to be removed as a maintainer not found", "code": 404})

    # Update the document only if the user_to_be_added["_id"] is not already in the maintainers list.
    result = db.packages.update_one(
        {"name": package, "namespace": package_namespace["_id"]},
        {"$pull": {"maintainers": user_to_be_removed["_id"]}}
    )

    # package_id gets added to the maintainerOf list in user document.
    db.users.update_one(
        {"username": username_to_be_removed}, 
        {"$pull": {"maintainerOf": curr_package["_id"]}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Maintainer removed successfully", "code": 200}), 200
    else:
        return jsonify({"message": "Package maintainer not found", "code": 200}), 200
    
@app.route("/<username>/namespace/maintainer", methods=["POST"])
def add_maintainers_to_namespace(username):
    uuid = request.form.get("uuid")
    username_to_be_added = request.form.get("username")
    namespace = request.form.get("namespace")
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    # Validating the data coming with request.
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    if not username_to_be_added:
        return jsonify({"message": "Please enter the username to be added", "code": 400}), 400
    
    if not namespace:
        return jsonify({"message": "Please enter the namespace name", "code": 400}), 400

    # Get the user from the database using uuid.
    user = db.users.find_one({"uuid": uuid})

    # Check if current user is authorized to access this API.
    if not user or user["username"] != username:
        return jsonify({"message": "Unauthorized", "code": 401}), 401

    # Get the namespace from the database.
    namespace_doc = db.namespaces.find_one({"namespace": namespace})

    # Check if namespace does not exists.
    if not namespace_doc:
        return jsonify({"message": "Namespace not found", "code": 404}), 404

    # Check if the current user has authority to add maintainers.
    # Only namespace maintainers or namespace admins can add new maintainers to the namespace.
    if not checkIsNamespaceAdmin(user_id=user["_id"], namespace=namespace_doc) and not checkIfNamespaceMaintainer(user_id=user["_id"], namespace=namespace_doc):
        return jsonify({"message": "User is not authorized to add namespace maintainers", "code": 401}), 401

    # Get the user to be added using the username received in the request body.
    user_to_be_added = db.users.find_one({"username": username_to_be_added})

    if not user_to_be_added:
        return jsonify({"message": "Username to be added as a maintainer not found", "code": 404})

     # Update the document only if the user_to_be_added["_id"] is not already in the admins list.
    result =  db.namespaces.update_one(
        {"namespace": namespace, 'maintainers': {'$ne': user_to_be_added["_id"]}}, 
        {"$addToSet": {"maintainers": user_to_be_added["_id"]}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Maintainer added successfully", "code": 200}), 200
    else:
        return jsonify({"message": "Maintainer already added", "code": 200}), 200
    
@app.route("/<username>/namespace/maintainer/remove", methods=["POST"])
def remove_maintainers_from_namespace(username):
    uuid = request.form.get("uuid")
    username_to_be_removed = request.form.get("username")
    namespace = request.form.get("namespace")

    # Validating the data coming with request.
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    if not username_to_be_removed:
        return jsonify({"message": "Please enter the username to be removed", "code": 400}), 400
    
    if not namespace:
        return jsonify({"message": "Please enter the namespace name", "code": 400}), 400
    
    # Get the user from the database using uuid.
    user = db.users.find_one({"uuid": uuid})

    # Check if current user is authorized to access this API.
    if not user or user["username"] != username:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    # Get the namespace from the database.
    namespace_doc = db.namespaces.find_one({"namespace": namespace})

    # Check if namespace does not exists.
    if not namespace_doc:
        return jsonify({"message": "Namespace not found", "code": 404}), 404

    # Check if the current user has authority to remove maintainers.
    if not checkIsNamespaceAdmin(user_id=user["_id"], namespace=namespace_doc):
        return jsonify({"message": "User is not authorized to remove maintainers", "code": 401}), 401
    
    # Get the user to be removed using the username received in the request body.
    user_to_be_removed = db.users.find_one({"username": username_to_be_removed})

    if not user_to_be_removed:
        return jsonify({"message": "Username to be removed as a maintainer not found", "code": 404})

    # Update the document only if the user_to_be_added["_id"] is not already in the maintainers list.
    result = db.namespaces.update_one(
        {"namespace": namespace},
        {"$pull": {"maintainers": user_to_be_removed["_id"]}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Maintainer removed successfully", "code": 200}), 200
    else:
        return jsonify({"message": "Namespace maintainer not found", "code": 200}), 200
    
# This function checks if user is a maintainer of a namespace.
def checkIfNamespaceMaintainer(user_id, namespace):
    maintainers_id_list = [str(obj_id) for obj_id in namespace["maintainers"]]
    str_user_id = str(user_id)
    return str_user_id in maintainers_id_list
    
# This function checks if user is a maintainer of a package.
def checkIsMaintainer(user_id, package):
    maintainers_id_list = [str(obj_id) for obj_id in package["maintainers"]]
    str_user_id = str(user_id)
    return str_user_id in maintainers_id_list

# This function checks if user is an admin of the namespace.
def checkIsNamespaceAdmin(user_id, namespace):
    admins_id_list = [str(obj_id) for obj_id in namespace["admins"]]
    str_user_id = str(user_id)
    return str_user_id in admins_id_list