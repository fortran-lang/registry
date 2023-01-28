from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Backend Registry APIs",
        "version": "1.0"
    }
})