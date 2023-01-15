import os
from flask import render_template,jsonify
from app import app
from mongo import db
import auth
import user
import packages

@app.route("/")
def index():
    return jsonify({"message": "Python flask mongo", "code": 200})

@app.route("/account/login", methods=["GET"])
def login_UI():
    return render_template("login.html")

@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html")

@app.route("/account/register", methods=["GET"])
def register_UI():
    return render_template("signup.html")

@app.route("/account/reset-password", methods=["GET"])
def render_reset():
    return render_template("reset.html")

@app.route("/account/update-password", methods=["GET"])
def update_password():
    return render_template("update.html")

@app.route("/manage/projects/", methods=["GET"])
def manage_projects():
    return render_template("account.html")

@app.route("/manage/account/", methods=["GET"])
def manage_accounts():
    return render_template("account.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
