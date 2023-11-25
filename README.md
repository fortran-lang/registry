# Registry for Fortran Package Manager

We are currently in the testing phase of this registry.

1. backend APIs are hosted at: https://fpm-registry.vercel.app/
2. frontend is hosted at: https://registry-phi.vercel.app/
3. Documentation for the APIs are available at: https://fpm-registry.vercel.app/apidocs/

**Please note: the current registry is a playground: its database will be fully deleted once its functionality is established. Please do not use it for production yet! more information will follow then.**

The fpm release [0.8.2](https://fortran-lang.discourse.group/t/fpm-version-0-8-2-released-centralized-registry-playground/5792) introduces fpm support for uploading packages to the fpm-registry server directly from the command-line interface, via

```
fpm publish --token <upload-token-here>
```

fpm will now also interact with a web interface that will help to manage the namespaces & packages. detailed information regarding the fpm cli can be found here: [docs](https://fpm.fortran-lang.org/registry/index.html)

## Instructions to Deploy with docker containers

```
$ sudo chmod 666 /var/run/docker.sock  # for root access
```

## Environment variable configuration

set the environment variables in .env file in backend directory or in the docker compose file (compose.yaml). MONGO_URI must be set in the environment to the URL value of the MongoDB to use. For example,If deploying to production, MONGO_URI should be set to mongo container address. set the following env variables in the .env file in the backend folder: 
   - SALT
   - MONGO_URI=MONGO_DB_ATLAS_UR
   - MONGO_DB_NAME
   - SUDO_PASSWORD
   - MONGO_USER_NAME
   - MONGO_PASSWORD
   - HOST
   - RESET_EMAIL 
   - RESET_PASSWORD

#### before building the docker containers, you must configure the environment variables ("RESET_EMAIL" and "RESET_PASSWORD") in the compose.yaml file .

```
$ docker compose -f "compose.yaml" up -d --build
$ cd frontend && REACT_APP_REGISTRY_API_URL="http://127.0.0.1:80"  npm start run
```

After the application starts, navigate to `http://localhost:80` in your web browser or run:

```
$ curl localhost:80
Hello world, Mongo Flask
```

Stop and remove the containers

```
$ docker compose down
```

## Steps to setup mongodump for registry Archives functionality
fpm - registry archives automatically created at weekly intervals by the mongodump command and stored in a tar archives format in the static directory of flask , to support caching and direct rendering of archives without manually fetching the mongodb for each archive request. to reduce the resource used by mongodb , we will only be installing the `mongodb-org-tools` only. the steps to setup mongodump on a Ubuntu linux 22.04 are:

1. Import the public key used by the package management system.

```
 wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
 ```

 2. Create a list file for MongoDB.

 ```
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
 ```

 3. Reload local package database and install the tools:

 ```
  sudo apt-get update
  sudo apt install mongodb-org-tools
 ```

for more details, please refer: [mongodb tools installation docs](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/).