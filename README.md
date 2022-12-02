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
└── nginx
    └── nginx.conf

```

## Deploy with docker compose

```
$ sudo chmod 666 /var/run/docker.sock  (for root access)
$ docker compose up -d

After the application starts, navigate to `http://localhost:80` in your web browser or run:

```
$ curl localhost:80
Hello world, Mongo Flask
```

Stop and remove the containers
```
$ docker compose down
```
