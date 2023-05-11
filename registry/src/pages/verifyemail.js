import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { verify } from "../store/actions/verifyEmailActions";
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";

const VerifyEmail = () => {
  const { uuid } = useParams();
  const dispatch = useDispatch();
  const message = useSelector((state) => state.verifyemail.message);
  const statuscode = useSelector((state) => state.verifyemail.statuscode);

  const handleSubmit = async (e) => {
    e.preventDefault();
      dispatch(verify(uuid));
  };

  return (
    <Container style={{ paddingTop: 25 }} onLoad={handleSubmit}>
      <form id="login-form" onSubmit={handleSubmit}>
        <h1>Welcome to fpm Registry!</h1>
        <h3>Verify your email</h3>
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
