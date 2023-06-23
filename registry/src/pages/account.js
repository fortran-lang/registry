import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import {
  reset,
  getUserAccount,
  resetMessages,
  change,
} from "../store/actions/accountActions";

import Row from "react-bootstrap/Row";
import Modal from "react-bootstrap/Modal";
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
  const message = useSelector((state) => state.account.message);
  const successMsg = useSelector(
    (state) => state.account.resetPasswordSuccessMsg
  );
  const [oldPassword, setoldPassword] = useState("");
  const [newPassword, setnewPassword] = useState("");
  const [newEmail, setNewEmail] = useState("");
  const [fromValidationErrors, setFormValidationError] = useState({});
  const [show, setShow] = useState(false);
  const dateJoined = useSelector((state) => state.account.dateJoined);
  const username = useSelector((state) => state.auth.username);
  const uuid = useSelector((state) => state.auth.uuid);
  const isLoading = useSelector((state) => state.account.isLoading);
  const isLoadingEmail = useSelector((state) => state.account.isLoadingEmail);
  const messageEmail = useSelector((state) => state.account.message);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    if (username === null) {
      navigate("/");
    } else {
      dispatch(getUserAccount(uuid));
    }

    if (error !== null || successMsg !== null) {
      dispatch(resetMessages());
    }
  });

  const validateForm = () => {
    let errors = {};

    if (!oldPassword) {
      errors.password = "Old Password is required";
    }
    if (!newPassword) {
      errors.password = "Enter New password";
    }

    setFormValidationError(errors);
    return Object.keys(errors).length === 0;
  };

  const validateFormEmail = () => {
    let errors = {};
    setFormValidationError(errors);
    if (!newEmail) {
      errors.email = "New Email is required";
    }
    setFormValidationError(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (validateForm()) {
      dispatch(resetMessages());
      dispatch(reset(oldPassword, newPassword, uuid));
      setnewPassword("");
      setoldPassword("");
    }
    setShow(true);
  };

  const handleSubmitEmail = async (e) => {
    e.preventDefault();

    if (validateFormEmail()) {
      dispatch(change(newEmail, uuid));
      setNewEmail("");
    }
    setShow(true);
  };

  const clearForm = () => {
    setFormValidationError({});
    setNewEmail("");
    setnewPassword("");
    setoldPassword("");
    dispatch(resetMessages());
  };

  const handleCloseModal = () => {
    clearForm();
    setShowModal(false);
  };

  const handleCloseEmailModal = () => {
    clearForm();
    setshowemailModal(false);
  };
  const handleOpenModal = () => {
    setShowModal(true);
  };

  const handleOpenEmailModal = () => {
    setshowemailModal(true);
  };

  const [showModal, setShowModal] = useState(false);
  const [showemailModal, setshowemailModal] = useState(false);

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
              <br />
              <br />
              <a href={`/users/${username}`} style={{ textDecoration: "none" }}>
                @{username}
              </a>
            </td>
            <td>
              We use <a href="https://gravatar.com">gravatar.com</a> to generate
              your profile picture based on your primary email address —
              <code className="break"> {email} </code>.<br />
              <br />
              <Button onClick={handleOpenModal}>Change Password</Button>
              <Button onClick={handleOpenEmailModal}>Change Email</Button>
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
        </tbody>
      </Table>
      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Reset Password</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group as={Row} className="mb-4">
              <Form.Label column sm="4">
                Old Password
              </Form.Label>
              <Col sm="8">
                <Form.Control
                  type="password"
                  placeholder="Enter Old Password"
                  name="oldPassword"
                  value={oldPassword}
                  onChange={(e) => setoldPassword(e.target.value)}
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
                  value={newPassword}
                  onChange={(e) => setnewPassword(e.target.value)}
                />
              </Col>
            </Form.Group>

            {fromValidationErrors.password && (
              <p className="error">{fromValidationErrors.password}</p>
            )}
            <p className={`success ${error ? "error" : ""}`}>
              {error ? error : messageEmail}
            </p>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSubmit}>
          {isLoadingEmail ? "Loading..." : "Submit"}
          </Button>
        </Modal.Footer>
      </Modal>
      <Modal show={showemailModal} onHide={handleCloseEmailModal}>
        <Modal.Header closeButton>
          <Modal.Title>Change Email</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmitEmail}>
            <Form.Group as={Row} className="mb-4">
              <Form.Label column sm="4">
                New Email
              </Form.Label>
              <Col sm="8">
                <Form.Control
                  type="email"
                  placeholder="Enter New Email"
                  name="email"
                  value={newEmail}
                  onChange={(e) => setNewEmail(e.target.value)}
                />
              </Col>
            </Form.Group>

            {fromValidationErrors.email && (
              <p className="error">{fromValidationErrors.email}</p>
            )}
            <p className={`success ${message ? "error" : ""}`}>{message}</p>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseEmailModal}>
            Close
          </Button>
          <Button variant="primary" onClick={handleSubmitEmail}>
            {isLoadingEmail ? "Loading..." : "Submit"}
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default Account;
