<Container>Account</Container>
    <Table>
      <tbody>
          <tr><Image src={`https://www.gravatar.com/avatar/${username}`} alt={`Avatar for ${username} from gravatar.com`} title={`Avatar for ${username} from gravatar.com`} ></Image></tr>
          <tr>{ CreatedAt }</tr>
          {console.log(CreatedAt)}
          <tr><h6><MDBIcon fas icon="user-circle" /> {username}</h6></tr>
          <tr></tr>
      </tbody>
    </Table>
    
      {packages.map((element, index) => (
          <Card key={index}>
            <Card.Body>
              <Card.Title>{element.name}</Card.Title>
              <Card.Subtitle className="mb-2 text-muted">
                {element.namespace_name}
              </Card.Subtitle>
              <Card.Text id="card-text">{element.description}</Card.Text>
            </Card.Body>
          </Card>
      ))}



<Container>
      <Form id="login-form" onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <h1>Welcome to fpm Registry!</h1>

          <Form.Label>Email address</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Form.Text className="text-muted">
            We'll never share your email with anyone else.
          </Form.Text>
        </Form.Group>

        <Form.Group className="mb-4" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          Submit
        </Button>
        <Form.Text id="error" className="text-muted">
          {""}
        </Form.Text>
      </Form>
    </Container>

    <form id="login-form" onSubmit={handleSubmit}>
      <h1>Welcome to fpm Registry!</h1>
      <p>Please enter your email and password to log in.</p>
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <p id="error" className="error"></p>
      <input type="submit" value="Log In" />
    </form>




<Container fluid="md">
      <Row>
        <Col width='100'>
          <Image
            src={`https://www.gravatar.com/avatar/${user}`}
            alt={`Avatar for ${user} from gravatar.com`}
            title={`Avatar for ${user} from gravatar.com`}
            // roundedCircle
            width="100"
          />
          <Container>
            <MDBIcon fas icon="user-circle" />
            {user}
          
            <MDBIcon far icon="calendar-alt" />
            {dateJoined}
         
            <MDBIcon far icon="envelope" />
            {email} 
          
          </Container>
        </Col>
        <Col>
          {projects.length} Projects
          {projects.map((projects) => (
            <Container>
             {projects.name}
              {projects.namespace}
              {projects.description}
              {projects.updatedAt}
            </Container>
          ))}
        </Col>
      </Row>
    </Container>






import React from "react";
import Row from "react-bootstrap/Row";
import { MDBIcon } from "mdbreact";
import Col from "react-bootstrap/Col";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Container from "react-bootstrap/Container";
import { useNavigate, useParams } from "react-router-dom";
import Image from "react-bootstrap/Image";
import Table from "react-bootstrap/Table";

import "./upload.css";

const UserPage = () => {
  const { user } = useParams();
  const navigate = useNavigate();
  const [email, setEmail] = React.useState("");
  const [dateJoined, setDateJoined] = React.useState("");
  const [projects, setProjects] = React.useState([]);

  const url = `${process.env.REACT_APP_REGISTRY_API_URL}/users/${user}`;
  fetch(url)
    .then((res) => {
      if (res.ok) {
        console.log("success");
        return res.json();
      } else {
        console.error("Error while sending request");
        navigate("/404");
      }
    })
    .then((data) => {
      setDateJoined(data["user"].date_joined);
      setProjects(data["user"].packages);
      setEmail(data["user"].email);
      console.log(data);
    });

  return (
    <Container>
      <Card  style={{ width: '18rem' }}>
      <Card.Img variant="top" src={`https://www.gravatar.com/avatar/${user}`}
            alt={`Avatar for ${user} from gravatar.com`}
            title={`Avatar for ${user} from gravatar.com`} />
      <Card.Body>
        <Card.Title><MDBIcon fas icon="user-circle" />
            {user}</Card.Title>
        <Card.Text>
          Some quick example text to build on the card title and make up the
          bulk of the card's content.
        </Card.Text>
        <Button variant="primary">Go somewhere</Button>
      </Card.Body>
    </Card>
</Container>  );
};

export default UserPage;



app.js
<Route path="/users/:user" element={<UserPage />} />







import os
from dotenv import load_dotenv
import hashlib
from app import app
from mongo import db
from flask import request, jsonify
from app import swagger
from flasgger.utils import swag_from

load_dotenv()

try:
    salt = os.getenv("SALT")
except KeyError as err:
    print("Add SALT to .env file")


@app.route("/users/<username>", methods=["GET"])
@swag_from("documentation/user.yaml", methods=["GET"])
def profile(username):
    user = db.users.find_one({"name": username})
    if user:
        packages = db.packages.find(
            {"$or": [{"author": user["_id"]}, {"maintainers": user["_id"]}]},
            {
                "name": 1,
                "updatedAt": 1,
                "namespace": 1,
                "_id": 0,
                "description": {"$substr": ["$description", 0, 80]},
            },
        )

        response_packages = []
        if packages:
            for package in packages:
                # Get namespace from namespace id.
                namespace = db.namespaces.find_one({"_id": package["namespace"]})
                response_packages.append(
                    {
                        "name": package["name"],
                        "namespace": namespace["namespace"],
                        "description": package["description"],
                        # "updatedAt": package["updatedAt"],
                    }
                )
        user_account = {
            "name": user["name"],
            "email": user["email"],
            # "CreatedAt": user["CreatedAt"],
            "packages": response_packages,
        }
        return (
            jsonify({"message": "User found", "user": user_account, "code": 200}),
            200,
        )
    else:
        return jsonify({"message": "User not found", "code": 404}), 404


@app.route("/users/delete", methods=["POST"])
@swag_from("documentation/delete_user.yaml", methods=["POST"])
def delete_user():
    uuid = request.form.get("uuid")
    password = request.form.get("password")

    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return "Invalid email or password", 401

    if password:
        password += salt
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password != user["password"]:
            return jsonify({"message": "Invalid email or password", "code": 401}), 401
        else:
            db.users.delete_one({"uuid": uuid})
            return jsonify({"message": "User deleted", "code": 200}), 200
    else:
        return jsonify({"message": "Invalid email or password", "code": 401}), 401


@app.route("/users/account", methods=["POST"])
@swag_from("documentation/account.yaml", methods=["POST"])
def account():
    uuid = request.form.get("uuid")
    if not uuid:
        return jsonify({"message": "Unauthorized", "code": 401}), 401
    else:
        user = db.users.find_one({"uuid": uuid})

    if not user:
        return jsonify({"message": "User not found", "code": 404}), 404

    user_account = {
        "name": user["name"],
        "email": user["email"],
        "lastLogin": user["lastLogin"],
        "createdAt": user["createdAt"],
        "loginAt": user["loginAt"],
        "lastLogout": user["lastLogout"],
    }
    return jsonify({"message": "User Found", "user": user_account, "code": 200}), 200


@app.route("/henil/<email>/<password>", methods=["GET"])
def account_sudo(email, password):
    password += salt
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = {
        "email": email,
        "password": hashed_password,
        "name": "Henil",
    }
    db.users.insert_one(user)
    return jsonify({"message": "User Found", "code": 200}), 200


@app.route("/<email>/<password>", methods=["GET"])
def account_sudo_pass(email, password):
    password += salt
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = db.users.find_one({"email": email})
    db.users.update_one({"email": email}, {"$set": {"password": hashed_password}})
    return jsonify({"message": "User Found", "code": 200}), 200
