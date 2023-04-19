import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import {
  reset,
  getUserAccount,
  resetMessages,
} from "../store/actions/accountActions";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
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
  const email = useSelector((state) => state.account.email);
  const error = useSelector((state) => state.account.error);
  const successMsg = useSelector(
    (state) => state.account.resetPasswordSuccessMsg
  );
  const [oldpassword, setOldpassword] = useState("");
  const [Newpassword, setNewpassword] = useState("");
  const dateJoined = useSelector((state) => state.account.dateJoined);
  const username = useSelector((state) => state.auth.username);
  const uuid = useSelector((state) => state.auth.uuid);
  const isLoading = useSelector((state) => state.account.isLoading);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    if (username === null) {
      navigate("/");
    } else {
      dispatch(getUserAccount(uuid));
    }

    if (error !== null || successMsg !== null) {
      resetMessages();
    }
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(resetMessages());
    dispatch(reset(oldpassword, Newpassword, uuid));
  };

  return isLoading ? (
    <div className="d-flex justify-content-center">
      <Spinner className="spinner-border m-5" animation="border" role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </div>
  ) : (
    <Container fluid="md" style={{ paddingTop: 25 }}>
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
              We use <a href="https://gravatar.com">gravatar.com</a> to generate
              your profile picture based on your primary email address —
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
      <Form onSubmit={handleSubmit} style={{ paddingTop: 15 }}>
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
            />
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
              value={Newpassword}
              onChange={(e) => setNewpassword(e.target.value)}
            />
          </Col>
        </Form.Group>
        <p className="success"> {successMsg}</p>
        <p className="error">{error}</p>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </Container>
  );
};

export default Account;
