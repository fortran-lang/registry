import os
from flask import render_template, jsonify
from app import app
from mongo import db
from auth import is_ci
import logging
import auth
import user
import packages
import namespaces
import val_test
# import validate_package  # TODO: Uncomment this when the package validation is enabled

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


@app.route("/")
def index():
    return jsonify({"message": "Python flask mongo", "code": 200})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Page not found", "code": 404})

@app.errorhandler(500)
def internal_server_error(e):
    logging.error("Server Error: %s", str(e))
    return jsonify({"message": "Internal server error", "code": 500})


# Log all unhandled exceptions
def log_exception(sender, exception, **extra):
    sender.logger.error(
        "An exception occurred: %s", str(exception), exc_info=(exception)
    )


app.register_error_handler(Exception, log_exception)

debug = True if is_ci != "true" else False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=debug)
