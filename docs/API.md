# Backend Overview

## Server

The code to actually run the server is in *flask/server.py*. This is where most of the pieces of the system are instantiated and configured, and can be thought of as the "entry point" to fpm-registry.


## Routes

The API URLs that the server responds to (aka "routes") are defined in
*flask/`*`.py*.

All of the routes are mounted under the `/` path (see the lines that look like `@app.route("/path")`

Each API route definition looks like this:

```python
@app.route('/auth/logout', methods=["POST"])
```

This line defines a route that responds to a POST request made to
`/auth/logout` with the 


## Code having to do with running a web application

This is Flask application with routes for fpm-registry. The code is using MongoDB as the backend database.

### The `auth` module

The following routes are defined:

* `/auth/login`: This route allows a user to log in to the application. It accepts both GET and POST requests. If a POST request is received, the route will attempt to log the user in by checking their email and password against the database. If the email and password are valid, the user's loginAt field in the database will be updated and a cookie containing a unique user identifier (UUID) will be set in the response. If the email and password are not valid, a 401 status code will be returned. If a GET request is received, the route will return a rendered template for the login form.

Request : 
```bash
curl --location --request POST 'http://127.0.0.1:9090/auth/login' \
--form 'email="john"' \
--form 'password="doe"'
```

* `/auth/signup`: This route allows a user to sign up for the application. It accepts both GET and POST requests. If a POST request is received, the route will attempt to create a new user in the database with the provided name, email, and password. If a user with the same email already exists, a 400 status code will be returned. If the signup is successful, a cookie containing a unique UUID will be set in the response. If a GET request is received, the route will return a rendered template for the signup form.

* `/auth/logout`: This route allows a user to log out of the application. It only accepts POST requests. If a valid cookie containing a UUID is found in the request, the user's lastLogout field in the database will be updated and the cookie will be removed from the response. If the cookie is not found, a 404 status code will be returned.

* `/auth/forgot-password`: This route allows a user to send an password reset email. It only accepts POST requests. If a valid email is found, Then new UUID is generated and a email is sent with uuid link to reset password.

* `/auth/reset-password`: This route allows a user to reset password.  It only accepts GET requests. If a valid UUID is found, Then password is changed and returns json `Password reset successful`, else it returns  `User not found`.



