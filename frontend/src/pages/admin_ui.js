import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useCookies } from "react-cookie";
import { useNavigate } from "react-router-dom";
import {
  reset,
  getUserAccount,
  deleteAccount,
} from "../store/actions/accountActions";
// import { fetchPackages } from "../store/actions/dashboardActions";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { MDBIcon } from "mdbreact";
import {
  MDBInputGroup,MDBInput
} from 'mdb-react-ui-kit';
import Table from "react-bootstrap/Table";
import Container from "react-bootstrap/Container";
import { Spinner } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";


const Admin = () => {
  const email = useSelector((state) => state.account.email);
  const error = useSelector((state) => state.account.error);
  const [password, setPassword] = useState("");
  const [oldpassword, setOldpassword] = useState("");
  const [Newpassword, setNewpassword] = useState("");
  const [show, setShow] = useState(false);
  const dateJoined = useSelector((state) => state.account.dateJoined);
  // const username = useSelector((state) => state.auth.username);
  const uuid = useSelector((state) => state.auth.uuid);
  const packages = useSelector((state) => state.dashboard.packages);
  const isLoading = useSelector((state) => state.dashboard.isLoading);
  // const user = useSelector((state) => state.account.user);
  const [username, setUsername] = useState("");
  const [packagename, setPackagename] = useState("");
  const [namespace, setNamespace] = useState("");
  const [release, setRelease] = useState("");

  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    if (username === null) {
      navigate("/");
    } else if (packages === null) {
      dispatch(getUserAccount(uuid));
    }
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(reset(oldpassword, Newpassword, uuid));
    setShow(true);
  };

  const handleDelete = async (e) => {
    e.preventDefault();
    dispatch(deleteAccount(password, uuid));
  };

  return !isLoading ? (
    <Spinner animation="border" role="status">
      <span className="visually-hidden">Loading...</span>
    </Spinner>
  ) : (
    <Container fluid="md" style={{ paddingTop: 25 }}>
      <h2 style ={{textAlign:left}}>Admin Settings</h2>
      <Container>
        <Table style={{ paddingTop: 15 }}>
          <thead>
            <h3>Delete User account</h3>
          </thead>
          <tbody className="text-danger"> 
            <tr>
              <h5>Proceed with caution!</h5>
            </tr>
            <tr>
              <h5>
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover {username} account after you delete it.
              </h5>
            </tr>
          </tbody>
        </Table>
        <Form onSubmit={handleDelete}>
          <Form.Group as={Row} className="mb-6">
            <Form.Label column sm="4">
              Username
            </Form.Label>
            <Col sm="8">
              <Form.Control
                type="text"
                placeholder="Enter username"
                name="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </Col>
          </Form.Group>
          <Button type="submit"> Delete User</Button>
          <Form.Text id="error" className="text-muted">
            {!show && error}
          </Form.Text>
        </Form>
      </Container>
      <Container>
        <Table style={{ paddingTop: 15 }}>
          <thead>
            <h3>Delete Package</h3>
          </thead>
          <tbody className="text-danger">
            <tr>
              <h5>Proceed with caution!</h5>
            </tr>
            <tr>
              <h5>
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover {packagename} after you delete it.
              </h5>
            </tr>
          </tbody>
        </Table>
      {/* <Form onSubmit={handleDelete} className="mb-4">
          <Form.Group as={Row} >
            <label>
              Package name
            </label>
        
            
              <
                type="text"
                placeholder="Enter Package name"
                name="package"
                value={packagename}
                onChange={(e) => setPackagename(e.target.value)}
              />
            
          </Form.Group>
          <MDBInputGroup noBorder textBefore='@'>
        <input className='form-control' type='text' placeholder='Username' />
      </MDBInputGroup>
      

          <Button type="submit">Delete Package</Button>
          <Form.Text id="error" className="text-muted">
            {!show && error}
          </Form.Text>
        </Form>  */}
        <form onSubmit={handleDelete}>
  <div className="row">
    <div className="col-4">
      <label>Name</label>
    </div>
    <div className="col-6">
      <MDBInput id='typeText' type='text' />
    </div>
  </div>
  <Button type="submit">Delete Package</Button>
  <Form.Text id="error" className="text-muted">
    {!show && error}
  </Form.Text>
</form>

      </Container>
      <Container>
        <Table style={{ paddingTop: 15 }}>
          <thead>
            <h3>Delete Package Release Version</h3>
          </thead>
          <tbody className="text-danger">
            <tr>
              <h5>Proceed with caution!</h5>
            </tr>
            <tr>
              <h5>
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover {release} after you delete it.
              </h5>
            </tr>
          </tbody>
        </Table>
        <Form onSubmit={handleDelete} >
          <Form.Group as={Row} className="mb-6">
            <Form.Label column sm="4">
              Release Version
            </Form.Label>
            <Col sm="8">
              <Form.Control
                type="text"
                placeholder="Enter Release Version"
                name="release"
                value={release}
                onChange={(e) => setRelease(e.target.value)}
              />{" "}
            </Col>
          </Form.Group>
      <Button type="submit">Delete Release</Button>
          <Form.Text id="error" className="text-muted">
            {!show && error}
          </Form.Text>
        </Form>
      </Container>
      <Container>
        <Table style={{ paddingTop: 15 }}>
          <thead>
            <h3>Delete Namespace</h3>
          </thead>
          <tbody className="text-danger">
            <tr>
              <h5>Proceed with caution!</h5>
            </tr>
            <tr>
              <h5>
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover {namespace} after you delete it.   </h5>
            </tr>
          </tbody>
        </Table>
        <Form onSubmit={handleDelete}>
          <Form.Group as={Row} className="mb-8">
            <Form.Label column>
              Namespace
            </Form.Label>
            <Col sm="8">
              <Form.Control column
                type="text"
                placeholder="Enter namespace"
                name="namespace"
                value={namespace}
                onChange={(e) => setNamespace(e.target.value)}
              />{" "}
            </Col>
          </Form.Group>
          <Button type="submit">Delete Namespace</Button>

          <Form.Text id="error" className="text-muted">
            {!show && error}
          </Form.Text>
        </Form>
      </Container>
    </Container>
  );
};

export default Admin;

 