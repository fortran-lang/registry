import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { verify } from "../store/actions/verifyEmailActions";
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";

const VerifyEmail = () => {
  const { uuid } = useParams();
  const dispatch = useDispatch();
  const message = useSelector((state) => state.verifyEmail.message);
  const statuscode = useSelector((state) => state.verifyEmail.statuscode);
  const isLoading = useSelector((state) => state.verifyEmail.isLoading);

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(verify(uuid));
  };

  return (
    <Container style={{ paddingTop: 25 }}>
      <form id="login-form" onSubmit={handleSubmit}>
        <h1>Welcome to fpm Registry!</h1>
        <input type="submit" value={isLoading ? "Loading..." : "Verify Email"} />
        {message &&
          (statuscode !== 200 ? (
            <p className="error">{message}</p>
          ) : (
            <p className="success">{message}</p>
          ))}
        <p>
          Already have an account?<Link to="/account/login"> Login </Link>
        </p>
      </form>
    </Container>
  );
};

export default VerifyEmail;
