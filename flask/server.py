import os
from flask import render_template,jsonify
from app import app
from mongo import db
import auth
import user
import packages
import namespaces

@app.route("/")
def index():
    return jsonify({"message": "Python flask mongo", "code": 200})

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
