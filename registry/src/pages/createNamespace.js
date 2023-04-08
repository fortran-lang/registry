import React, { useState } from "react";
import { useCookies } from "react-cookie";
import { Navigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { createNamespace } from "../store/actions/createNamespaceActions";
import Container from "react-bootstrap/Container";
import Spinner from "react-bootstrap/Spinner";
import "./upload.css";

const NamespaceForm = () => {
  const [cookies, setCookie] = useCookies(["uuid"]);
  const dispatch = useDispatch();
  const isLoading = useSelector((state) => state.upload.isLoading);
  const message = useSelector((state) => state.upload.message);
  const statuscode = useSelector((state) => state.upload.statuscode);

  const [data, setData] = useState({
    namespace: "",
    namespace_description: "",
    uuid: cookies.uuid,
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setData({ ...data, [name]: value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    dispatch(createNamespace(event.target));
  };


    return !isLoading ? (
        <Container style={{padding:20}}>
        <h2>Create a Namespace</h2>
        <form id="package-form" onSubmit={handleSubmit}>
          <label htmlFor="namespace">Namespace:</label>
          <input
            type="text"
            id="namespace"
            name="namespace"
            value={data.namespace}
            onChange={handleChange}
          />
          <br />
      
          <label htmlFor="namespace_description">Namespace Description:</label>
          <textarea
            id="namespace_description"
            name="namespace_description"
            value={data.namespace_description}
            onChange={handleChange}
          />
          <br />
      
          <input
            type="hidden"
            id="uuid"
            name="uuid"
            value={cookies.uuid}
            onChange={handleChange}
          />
          <br />
          {statuscode === 200 ? (
            <Container className="success">{message}</Container>
          ) : (
            <Container className="error">{message}</Container>
          )}
          <button type="submit">Create Namespace</button>
        </form>
</Container>    ) : (
      <Container style={{ margin: "200px" }}>
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </Container>
    );
  }

export default NamespaceForm;
