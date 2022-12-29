# registry
Registry for Fortran package manager

## Python Flask app with Nginx and  Mongo database

Project structure:
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

## Deploy with docker compose

```
$ sudo chmod 666 /var/run/docker.sock  (for root access)
$ docker compose up -d
```

After the application starts, navigate to `http://localhost:80` in your web browser or run:

```
$ curl localhost:80
Hello world, Mongo Flask
```

set MONGO_URI=MONGO_DB_ATLAS_URL (in .env file in flask directory)
The MONGO_URI must be set in the environment (or, alternatively, in the .env file in the flask directory) to the URL value of the MongoDB to use. For example,If deploying to production, MONGO_URI should be set to mongo container address.

Stop and remove the containers

```
$ docker compose down
```
