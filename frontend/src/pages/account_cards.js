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
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import Spinner from "react-bootstrap/Spinner";

import "@fortawesome/fontawesome-free/css/all.min.css";
import "bootstrap-css-only/css/bootstrap.min.css";
import "mdbreact/dist/css/mdb.css";

const Account = () => {
  const email = useSelector((state) => state.account.email);
  const error = useSelector((state) => state.account.error);
  const successMsg = useSelector(
    (state) => state.account.resetPasswordSuccessMsg
  );
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [formValidationErrors, setFormValidationErrors] = useState({});
  const [show, setShow] = useState(false);
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
      dispatch(resetMessages());
    }
  }, [dispatch, navigate, successMsg, error, username, uuid]);

  const validateForm = () => {
    let errors = {};

    if (!oldPassword) {
      errors.oldPassword = "Old Password is required";
    }
    if (!newPassword) {
      errors.newPassword = "Enter New password";
    }

    setFormValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (validateForm()) {
      dispatch(resetMessages());
      dispatch(reset(oldPassword, newPassword, uuid));
    }
    setShow(true);
  };

  return isLoading ? (
    <div className="d-flex justify-content-center">
      <Spinner className="spinner-border m-5" animation="border" role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </div>
  ) : (
    <Container fluid style={{ paddingTop: 25 }}>
      <Row>
        <Col md={4}>
          <Card className="mb-4" style={{ backgroundColor: "#734f96" }}>
            <Card.Header className="text-white">
              <h3>Profile Settings</h3>
            </Card.Header>
            <Card.Body style={{ backgroundColor: "#ffffff" }}>
              <Card.Title className="text-white">Profile Picture</Card.Title>
                <Card.Img
                  src={`https://www.gravatar.com/avatar/${username}`}
                  alt={`Avatar for ${username} from gravatar.com`}
                  title={`Avatar for ${username} from gravatar.com`}
                  style={{ width: 150, height: 150 }}
                />
              <Card.Text className="text-black">
                We use{" "}
                <a href="https://gravatar.com" >
                  gravatar.com
                </a>{" "}
                to generate your profile picture based on your primary email
                address — <code>{email}</code>.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={8}>
          <Card className="mb-4" style={{ backgroundColor: "#734f96" }}>
            <Card.Header className="text-white">
              <h3>Account Details</h3>
            </Card.Header>
            <ListGroup variant="flush" className="text-black">
              <ListGroup.Item>
                <h6 >Username</h6>
                <span >@{username}</span>
              </ListGroup.Item>
              <ListGroup.Item>
                <h6 >Date Joined</h6>
                <span >{dateJoined}</span>
              </ListGroup.Item>
              <ListGroup.Item>
                <h6 >Primary Email</h6>
                <span >{email}</span>
              </ListGroup.Item>
            </ListGroup>
          </Card>
        </Col>
      </Row>

      <Card className="mt-4" style={{ backgroundColor: "#734f96" }}>
        <Card.Header className="text-white">
          <h5>Change Password</h5>
        </Card.Header>
        <Card.Body style={{ backgroundColor: "#ffffff" }}>
          <Form onSubmit={handleSubmit}>
            {/* Password change form */}
          </Form>
        </Card.Body>
      </Card>

      <Card className="mt-4" style={{ backgroundColor: "#734f96" }}>
        <Card.Header className="text-white">
          <h5>Change Email</h5>
        </Card.Header>
        <Card.Body style={{ backgroundColor: "#ffffff" }}>
          {/* Email change form */}
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Account;



























// email change form


 {/* <Form onSubmit={handleSubmit} style={{ paddingTop: 15 }}>
        <Form.Group as={Row} className="mb-4">
          <Form.Label column sm="4">
            New Email
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
        <Button variant="primary" type="submit">
          Submit
        </Button>
        {fromValidationErrors.password && (
          <p className="error">{fromValidationErrors.password}</p>
        )}
        <p className={`success ${error ? "error" : ""}`}>
          {error ? error : successMsg}
        </p>
        <Form.Text id="error" className="text-muted">
          {show && error}
        </Form.Text>
      </Form> */}



// password change form

<Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>New Email</Modal.Title>
        </Modal.Header>
        <Modal.Body>
<Form onSubmit={handleSubmit} style={{ paddingTop: 15 }}>
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
  {error ? error : successMsg}
</p>
<Button variant="primary" type="submit">
  Submit
</Button>
<Form.Text id="error" className="text-muted">
  {show && error}
</Form.Text>
</Form> </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Close
          </Button>
          <Button variant="primary" type="submit" onClick={handleSubmit}>
            Submit
          </Button>
        </Modal.Footer>
      </Modal>

































<Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>New Email</Modal.Title>
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
                  onChange={(e) => setnewEmail(e.target.value)}
                />
              </Col>
            </Form.Group>
            {fromValidationErrors.password && (
              <p className="error">{fromValidationErrors.password}</p>
            )}
          </Form>
          <p className={`success ${error ? "error" : ""}`}>
            {error ? error : successMsg}
          </p>
          <Form.Text id="error" className="text-muted">
            {show && error}
          </Form.Text>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Close
          </Button>
          <Button variant="primary" type="submit" onClick={handleSubmit}>
            Submit
          </Button>
        </Modal.Footer>
      </Modal>






