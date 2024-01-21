from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "fpm-registry-secret-key"     #TODO: Please change this.
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 90 * 24 * 60 * 60   # 90 days
CORS(app)                                                    #TODO: Please restrict to only the frontend domain.
JWTManager(app)

swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {"title": "Backend Registry APIs", "version": "1.0"},
    },
)
