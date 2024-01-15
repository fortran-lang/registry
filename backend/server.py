import os
from flask import jsonify
from app import app
from auth import is_ci
import auth
import user
import packages
import namespaces


@app.route("/")
def index():
    return jsonify({"message": "Python flask mongo", "code": 200})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Page not found", "code": 404})

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"message": "Internal server error", "code": 500})


debug = True if is_ci != "true" else False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=debug)
