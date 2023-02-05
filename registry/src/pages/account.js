import React, { useEffect, useState } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { useCookies } from "react-cookie";
import { fetchPackages } from "../store/actions/dashboardActions";
import { useNavigate } from "react-router-dom";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { MDBIcon } from "mdbreact";
import { MDBBtn } from 'mdb-react-ui-kit';
import Image from "react-bootstrap/Image";
import Table from "react-bootstrap/Table";
import Spinner from "react-bootstrap/Spinner";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

import "@fortawesome/fontawesome-free/css/all.min.css";
import "bootstrap-css-only/css/bootstrap.min.css";
import "mdbreact/dist/css/mdb.css";

const Account = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [cookies, setCookie] = useCookies(["uuid"]);
  const [password, setPassword] = useState("");
  const [oldpassword, setOldpassword] = useState("");
  const [dateJoined, setdateJoined] = useState("");
  const username = useSelector((state) => state.auth.username);
  const uuid = useSelector((state) => state.auth.uuid);
  const packages = useSelector((state) => state.dashboard.packages);
  const isLoading = useSelector((state) => state.dashboard.isLoading);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    if (username === null) {
      navigate("/");
    } else if (packages === null) {
      dispatch(fetchPackages(username));

      let formData = new FormData();
      formData.append("uuid", uuid);

      axios({
        method: "post",
        url: `${process.env.REACT_APP_REGISTRY_API_URL}/users/account`,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
        .then((result) => {
          setEmail(result.data.user.email);
          setdateJoined(result.data.user.createdAt.slice(0, 16));
        })
        .catch((error) => {
          console.log(cookies.uuid);
        });
    }
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append("oldpassword", oldpassword);
    formData.append("password", password);
    formData.append("uuid", uuid);

    axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/auth/reset-password`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
      .then((result) => {
        // console.log(result);
        setError(result.data.message);
      })
      .catch((error) => {
        console.log(error);
        setError(error.response.data.message);
      });
  };
  const handleDelete = async (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append("password", password);
    formData.append("uuid", uuid);

    axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/users/delete`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
      .then((result) => {
        // console.log(result);
        setError(result.data.message);
      })
      .catch((error) => {
        console.log(error);
        setError(error.response.data.message);
      });
  };

  return isLoading ? (
    <Spinner animation="border" role="status">
      <span className="visually-hidden">Loading...</span>
    </Spinner>
  ) : (
    <Container fluid="md">
      <Table>
        <thead>
          <h3>Account Settings</h3>
        </thead>
        <tbody>
          <tr>
            <h5>Profile picture</h5>
          </tr>
          <tr>
            <td>
              <Image
                src={`https://www.gravatar.com/avatar/${username}`}
                alt={`Avatar for ${username} from gravatar.com`}
                title={`Avatar for ${username} from gravatar.com`}
              />
            </td>
            <td>
              We use <a href="gravatar.com">gravatar.com</a> to generate your
              profile picture based on your primary email address —
              <code className="break"> {email} </code>.
            </td>
          </tr>
          <tr>
            <h5>Account details</h5>
          </tr>
          <tr>
            <td>
              <h6>Username</h6>
            </td>
            <td>@{username}</td>
          </tr>
          <tr>
            <td>
              <h6>Date Joined</h6>
            </td>
            <td>{dateJoined}</td>
          </tr>

          <tr>
            <td>
              <h6>Primary Email</h6>
            </td>
            <td>{email}</td>
          </tr>
          <tr>
            <h5>Change Password</h5>
          </tr>
        </tbody>
      </Table>
      <Form onSubmit={handleSubmit}>
        <Form.Group as={Row} className="mb-4">
          <Form.Label column sm="4">
            Old Password
          </Form.Label>
          <Col sm="8">
            <Form.Control
              type="password"
              placeholder="Enter Old Password"
              name="oldpassword"
              value={oldpassword}
              onChange={(e) => setOldpassword(e.target.value)}
            />{" "}
          </Col>
        </Form.Group>

        <Form.Group as={Row} className="mb-4">
          <Form.Label column sm="4">
            New Password
          </Form.Label>
          <Col sm="8">
            <Form.Control
              type="password"
              placeholder="Enter New Password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Col>
        </Form.Group>

        <Button variant="primary" type="submit">
          Submit
        </Button>
        <Form.Text id="error" className="text-muted">
          {error}
        </Form.Text>
      </Form>
      <Container>
        {" "}
        <Table>
          <thead>
            <h3>Delete account</h3>
          </thead>
          <tbody className="text-danger">
            <tr>
              <h5>Proceed with caution!</h5>
            </tr>
            <tr>
              <h5>
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover your account after you delete it
              </h5>
            </tr>
          </tbody>
        </Table>
        <Form onSubmit={handleDelete} className="text-danger">
          <Form.Group as={Row} className="mb-4">
            <Form.Label column sm="4">
              {" "}
              Password
            </Form.Label>
            <Col sm="8">
              <Form.Control
                type="password"
                placeholder="Enter Password"
                name="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />{" "}
            </Col>
          </Form.Group>
          <MDBBtn className='me-1' color='danger' type="submit">
          Delete Account
      </MDBBtn>
          {/* <Button variant="secondary" >
            Delete Account
          </Button> */}
          <Form.Text id="error" className="text-muted">
            {error}
          </Form.Text>
        </Form>
      </Container>
    </Container>
  );
};

export default Account;
