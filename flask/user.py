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
@swag_from("documentation/get_user_profile.yaml", methods=["GET"])
def profile(username):
    user_doc = db.users.find_one({"username": username})
    if user_doc:
        # Get all the packages user is maintainer of.
        packages = db.packages.find(
            {"$or": [{"author": user_doc["_id"]}, {"maintainers": user_doc["_id"]}]},
        )

        # Get all the namespaces user is maintainer/admin of.
        # A namespace maintainer / admin will be maintainer of all the packages under that namespace.
        namespaces = db.namespaces.find(
            {"$or": [{"author": user_doc["_id"]}, {"maintainers": user_doc["_id"]}, {"admins": user_doc["_id"]}]},
        )

        response_packages = []
        response_namespaces = []
        
        # Check if there are any namespaces user is maintainer of.
        if namespaces:
            # Iterate over all the namespaces and add it to the response_namespace.
            for namespace in namespaces:
                isNamespaceAdmin = False
                isNamespaceMaintainer = False

                # Check if the user is admin of the namespace.
                if user_doc["_id"] in namespace["admins"]:
                    isNamespaceAdmin = True

                # Check if the user is maintainer of the namespace.
                if user_doc["_id"] in namespace["maintainers"]:
                    isNamespaceMaintainer = True

                response_namespaces.append({
                    "id": str(namespace["_id"]),
                    "name": namespace["namespace"],
                    "description": namespace["description"],
                    "isNamespaceAdmin": isNamespaceAdmin,
                    "isNamespaceMaintainer": isNamespaceMaintainer,
                })

                # Iterate over all the packages in the namespace.
                # User is maintainer of all these packages.
                # Add these packages to the response_packages.
                for package_id in namespace["packages"]:
                    package_doc = db.packages.find_one({"_id": package_id})

                    isPackageMaintainer = False

                    # Check if the user is maintainer of the package.
                    if user_doc["_id"] in package_doc["maintainers"]:
                        isPackageMaintainer = True

                    response_packages.append({
                        "id": str(package_doc["_id"]),
                        "name": package_doc["name"],
                        "namespace": namespace["namespace"],
                        "description": package_doc["description"],
                        "updatedAt": package_doc["updatedAt"],
                        "isNamespaceMaintainer": isNamespaceMaintainer,
                        "isNamespaceAdmin": isNamespaceAdmin,
                        "isPackageMaintainer": isPackageMaintainer,
                    })

        # Check for the packages that user is maintainer of individually but not as namespace maintainer.
        # If these packages are already not in the response then add it to the response_packages else skip the 
        # duplicates.
        if packages:
            for package in packages:
                isDuplicate = False

                # Check if that package is already under a namespace.
                # response_packages will contain a list of packages that user is maintainer of under a namespace.
                for pkg in response_packages:
                    
                    if pkg["id"] == str(package["_id"]):
                        isDuplicate = True
                        break
                
                # Skip the duplicates.
                if isDuplicate:
                    continue
                
                # Get namespace from namespace id.
                namespace = db.namespaces.find_one({"_id": package["namespace"]})
                
                isNamespaceMaintainer = False
                isPackageMaintainer = False

                if user_doc["_id"] in namespace["maintainers"]:
                    isNamespaceMaintainer = True

                if user_doc["_id"] in package["maintainers"]:
                    isPackageMaintainer = True

                response_packages.append(
                    {   
                        "id": str(package["_id"]),
                        "name": package["name"],
                        "namespace": namespace["namespace"],
                        "description": package["description"],
                        "updatedAt": package["updatedAt"],
                        "isNamespaceMaintainer": isNamespaceMaintainer,
                        "isPackageMaintainer": isPackageMaintainer,
                    }
                )
                
        
        user_account = {
            "username": user_doc["username"],
            "email": user_doc["email"],
            "createdAt": user_doc["createdAt"],
        }
        return (
            jsonify(
                {
                    "message": "User found",
                    "user": user_account,
                    "packages": response_packages,
                    "namespaces": response_namespaces,
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
    username = request.form.get("username")

    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
       return jsonify({"message": "Unauthorized", "code": 401}), 401

    if username and "admin" in user["roles"]:
        delete_user = db.users.find_one({"username": username})
        if delete_user:
            db.users.delete_one({"username": username})
            return jsonify({"message": "User deleted", "code": 200}), 200
        else:
            return jsonify({"message": "User not found", "code": 404}), 404

    else:
        return jsonify({"message": "Unauthorized", "code": 401}), 401


@app.route("/users/account", methods=["POST"])
@swag_from("documentation/get_user_account.yaml", methods=["POST"])
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
@swag_from("documentation/check_admin_user.yaml", methods=["POST"])
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
@swag_from("documentation/transfer_account.yaml", methods=["POST"])
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
@swag_from("documentation/add_package_maintainer.yaml", methods=["POST"])
def add_maintainers_to_package(username):
    uuid = request.form.get("uuid")
    username_to_be_added = request.form.get("username")
    package = request.form.get("package")
    namespace = request.form.get("namespace")

    # Validating the data coming with request.
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401

    if not username_to_be_added:
        return (
            jsonify({"message": "Please enter the username to be added", "code": 400}),
            400,
        )

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
    curr_package = db.packages.find_one(
        {"name": package, "namespace": package_namespace["_id"]}
    )

    # Check if the package does not exists.
    if not curr_package:
        return jsonify({"message": "Package not found", "code": 404}), 404

    # Check if the current user has authority to add maintainers.
    # Package maintainer, Namespace maintainer or Namespace admin has the authority to add package maintainers.
    if not checkIsMaintainer(
        user_id=user["_id"], package=curr_package
    ) and not checkIsNamespaceAdmin(user_id=user["_id"], namespace=package_namespace
        ) and not checkIfNamespaceMaintainer(user_id=user["_id"], namespace=package_namespace):
        return jsonify({"message": "Unauthorized", "code": 401}), 401

    # Get the user to be added using the username received in the request body.
    user_to_be_added = db.users.find_one({"username": username_to_be_added})

    if not user_to_be_added:
        return jsonify(
            {"message": "Username to be added as a maintainer not found", "code": 404}
        )

    # Update the document only if the user_to_be_added["_id"] is not already in the maintainers list.
    result = db.packages.update_one(
        {"name": package, "namespace": package_namespace["_id"]},
        {"$addToSet": {"maintainers": user_to_be_added["_id"]}},
    )

    # package_id gets added to the maintainerOf list in user document.
    db.users.update_one(
        {"username": username_to_be_added},
        {"$addToSet": {"maintainerOf": curr_package["_id"]}},
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
        return (
            jsonify(
                {"message": "Please enter the username to be removed", "code": 400}
            ),
            400,
        )

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
    curr_package = db.packages.find_one(
        {"name": package, "namespace": package_namespace["_id"]}
    )

    # Check if the package does not exists.
    if not curr_package:
        return jsonify({"message": "Package not found", "code": 404}), 404

    # Check if the current user has authority to remove maintainers.
    # Package maintainer, Namespace maintainer or Namespace admin has the authority to remove package maintainers.
    if not checkIsNamespaceAdmin(user_id=user["_id"], namespace=package_namespace
        ) and not checkIfNamespaceMaintainer(user_id=user["_id"], namespace=package_namespace):
        return (
            jsonify(
                {"message": "User is not authorized to remove maintainers", "code": 401}
            ),
            401,
        )

    # Get the user to be removed using the username received in the request body.
    user_to_be_removed = db.users.find_one({"username": username_to_be_removed})

    if not user_to_be_removed:
        return jsonify(
            {"message": "Username to be removed as a maintainer not found", "code": 404}
        )

    # Update the document only if the user_to_be_added["_id"] is not already in the maintainers list.
    result = db.packages.update_one(
        {"name": package, "namespace": package_namespace["_id"]},
        {"$pull": {"maintainers": user_to_be_removed["_id"]}},
    )

    # package_id gets added to the maintainerOf list in user document.
    db.users.update_one(
        {"username": username_to_be_removed},
        {"$pull": {"maintainerOf": curr_package["_id"]}},
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

    # Validating the data coming with request.
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401

    if not username_to_be_added:
        return (
            jsonify({"message": "Please enter the username to be added", "code": 400}),
            400,
        )

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
    if not checkIsNamespaceAdmin(
        user_id=user["_id"], namespace=namespace_doc
    ) and not checkIfNamespaceMaintainer(user_id=user["_id"], namespace=namespace_doc):
        return (
            jsonify(
                {
                    "message": "User is not authorized to add namespace maintainers",
                    "code": 401,
                }
            ),
            401,
        )

    # Get the user to be added using the username received in the request body.
    user_to_be_added = db.users.find_one({"username": username_to_be_added})

    if not user_to_be_added:
        return jsonify(
            {"message": "Username to be added as a maintainer not found", "code": 404}
        )

    # Update the document only if the user_to_be_added["_id"] is not already in the admins list.
    result = db.namespaces.update_one(
        {"namespace": namespace, "maintainers": {"$ne": user_to_be_added["_id"]}},
        {"$addToSet": {"maintainers": user_to_be_added["_id"]}},
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
        return (
            jsonify(
                {"message": "Please enter the username to be removed", "code": 400}
            ),
            400,
        )

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
        return (
            jsonify(
                {"message": "User is not authorized to remove maintainers", "code": 401}
            ),
            401,
        )

    # Get the user to be removed using the username received in the request body.
    user_to_be_removed = db.users.find_one({"username": username_to_be_removed})

    if not user_to_be_removed:
        return jsonify(
            {"message": "Username to be removed as a maintainer not found", "code": 404}
        )

    # Check if the user is trying to remove admins from the namespace.
    # Namespace admins cannot be remove from the namespace maintainers role.
    if checkIsNamespaceAdmin(user_id=user_to_be_removed["_id"], namespace=namespace_doc):
        return (
            jsonify(
                {
                    "message": "Admins cannot be removed from the namespace maintainer role",
                    "code": 401,
                }
            ),
            401,
        )

    # Update the document only if the user_to_be_added["_id"] is not already in the maintainers list.
    result = db.namespaces.update_one(
        {"namespace": namespace}, {"$pull": {"maintainers": user_to_be_removed["_id"]}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Maintainer removed successfully", "code": 200}), 200
    else:
        return jsonify({"message": "Namespace maintainer not found", "code": 200}), 200
    
@app.route("/<username>/namespace/admin", methods=["POST"])
def add_admins_to_namespace(username):
    uuid = request.form.get("uuid")
    username_to_be_added = request.form.get("username")
    namespace = request.form.get("namespace")

    # Validating the data coming with request.
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    if not username_to_be_added:
        return (
            jsonify(
                {"message": "Please enter the username to be added", "code": 400}
            ),
            400,
        )
    
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
    
    # Only namespace admins can add new admins to the namespace or namespace authors have the authority to add admins.
    if not checkIsNamespaceAdmin(user_id=user["_id"], namespace=namespace_doc) and not checkIfNamespaceAuthor(user_id=user["_id"], namespace=namespace_doc):
        return (
            jsonify(
                {"message": "User is not authorized to add namespace admins", "code": 401}
            ),
            401,
        )
    
    # Get the user to be added using the username received in the request body.
    username_to_be_added = db.users.find_one({"username": username_to_be_added})

    if not username_to_be_added:
        return jsonify(
            {"message": "Username to be added as a admin not found", "code": 404}
        )
    
    # Update the document only if the user_to_be_added["_id"] is not already in the admins list.
    result = db.namespaces.update_one(
        {"namespace": namespace, "admins": {"$ne": username_to_be_added["_id"]}},
        {"$addToSet": {"admins": username_to_be_added["_id"]}},
    )

    if result.modified_count > 0:
        return jsonify({"message": "Admin added successfully", "code": 200}), 200
    else:
        return jsonify({"message": "Admin already added", "code": 200}), 200
    
@app.route("/<username>/namespace/admin/remove", methods=["POST"])
def remove_admins_from_namespace(username):
    uuid = request.form.get("uuid")
    username_to_be_removed = request.form.get("username")
    namespace = request.form.get("namespace")

    # Validating the data coming with request.
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    
    if not username_to_be_removed:
        return (
            jsonify(
                {"message": "Please enter the username to be removed", "code": 400}
            ),
            400,
        )
    
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
    
    # Check if the current user has authority to remove admins.
    # Only namespace authors or admins can remove namespace admins.
    if not checkIsNamespaceAdmin(user_id=user["_id"], namespace=namespace_doc) and not checkIfNamespaceAuthor(user_id=user["_id"], namespace=namespace_doc):
        return (
            jsonify(
                {"message": "User is not authorized to remove admins", "code": 401}
            ),
            401,
        )
    
    # Get the user to be removed using the username received in the request body.
    username_to_be_removed = db.users.find_one({"username": username_to_be_removed})

    if not username_to_be_removed:
        return jsonify(
            {"message": "Username to be removed as a admin not found", "code": 404}
        )

    # Check if a user is trying to remove original namespace author from admin role.
    # Do not allow users to remove original namespace authors from admin role.
    if str(namespace_doc["author"]) == str(username_to_be_removed["_id"]):
        return jsonify({"code": 401, "message": "Namespace owners cannot be removed from admins"})

    # Update the document only if the user_to_be_added["_id"] is not already in the admins list.
    result = db.namespaces.update_one(
        {"namespace": namespace, "admins": username_to_be_removed["_id"]},
        {"$pull": {"admins": username_to_be_removed["_id"]}},
    )

    if result.modified_count > 0:
        return jsonify({"message": "Admin removed successfully", "code": 200}), 200
    else:
        return jsonify({"message": "Admin already removed", "code": 200}), 200


# This function checks if user is an author of a namespace.
def checkIfNamespaceAuthor(user_id, namespace):
    author_id = namespace["author"]
    return user_id == author_id

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
