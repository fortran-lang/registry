import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { createNamespace } from "../store/actions/createNamespaceActions";
import Spinner from "react-bootstrap/Spinner";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { Card } from "react-bootstrap";
import "./upload.css";

const NamespaceForm = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const uuid = useSelector((state) => state.auth.uuid);
  const isLoading = useSelector((state) => state.createNamespace.isLoading);
  const message = useSelector((state) => state.createNamespace.message);
  const statuscode = useSelector((state) => state.createNamespace.statuscode);

  useEffect(() => {
    if (uuid === null) {
      navigate("/");
    }
  }, [uuid]);

  const [data, setData] = useState({
    namespace: "",
    namespace_description: "",
    uuid: uuid,
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setData({ ...data, [name]: value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    dispatch(createNamespace(data));
  };

  return !isLoading ? (
    <Card id="create-namespace-card">
      <h3>Create a namespace</h3>
      <Form onSubmit={handleSubmit}>
        <Form.Group
          className="mb-3"
          controlId="formNamespaceName"
          id="namespace-name-textfield"
        >
          <Form.Label>Namespace:</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter namespace"
            value={data.namespace}
            name="namespace"
            onChange={handleChange}
          />
          <Form.Text className="text-muted">
            Write a unique namespace name.
          </Form.Text>
        </Form.Group>

        <Form.Group
          className="mb-3"
          controlId="formNamespaceDescription"
          id="namespace-description-textfield"
        >
          <Form.Label>Namespace description:</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter namespace description"
            as="textarea"
            name="namespace_description"
            value={data.namespace_description}
            onChange={handleChange}
          />
          <Form.Text className="text-muted">
            Write a brief namespace description.
          </Form.Text>
        </Form.Group>

        <Button variant="primary" type="submit" id="namespace-submit-btn">
          Submit
        </Button>
      </Form>
      {statuscode === 200 ? (
        <p className="success">{message}</p>
      ) : (
        <p className="error">{message}</p>
      )}
    </Card>
  ) : (
    <div className="d-flex justify-content-center">
      <Spinner className="spinner-border m-5" animation="border" role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </div>
  );
};

export default NamespaceForm;
