# Registry for Fortran package manager

Currently for the testing phase :
1. backend APIs are hosted at:  http://registry-apis.vercel.app/
2. frontend is hosted at: https://registry-frontend.vercel.app/
3. Documentation for the APIs are available at: https://registry-apis.vercel.app/apidocs/

**Please note: the current registry is a playground: its database will be fully deleted once its functionality is established. Please do not use it for production yet! more information will follow then.**

The fpm release [0.8.2](https://fortran-lang.discourse.group/t/fpm-version-0-8-2-released-centralized-registry-playground/5792) introduces fpm support for uploading packages to the fpm-registry server directly from the command-line interface, via

```
fpm publish --token <token-here>
```

fpm will now interact with a web interface that will help to manage the namespaces & packages.


## fpm - registry : Python Flask app with Nginx and Mongo database

backend Project structure:
```
.
├── compose.yaml
├── flask
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
|   └── app.py
|   └── auth.py
|   └── mongo.py
|   └── .env
└── nginx
    └── nginx.conf

```

## Instructions for Deploy with docker compose

```
$ sudo chmod 666 /var/run/docker.sock  (for root access)
$ docker compose up -d
$ REACT_APP_REGISTRY_API_URL="http://127.0.0.1:9090"  npm start run
```

After the application starts, navigate to `http://localhost:80` in your web browser or run:

```
$ curl localhost:80
Hello world, Mongo Flask
```

set MONGO_URI=MONGO_DB_ATLAS_URL (in .env file in flask directory)
The MONGO_URI must be set in the environment (or, alternatively, in the .env file in the flask directory) to the URL value of the MongoDB to use. For example,If deploying to production, MONGO_URI should be set to mongo container address.
set the following env variables in the .env file in the flask folder: 
   - SALT
   - MONGO_URI
   - MONGO_DB_NAME
   - SUDO_PASSWORD
   - MONGO_USER_NAME
   - MONGO_PASSWORD
   - HOST
   - RESET_EMAIL 
   - RESET_PASSWORD

Stop and remove the containers

```
$ docker compose down
```
