import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { forgot } from "../store/actions/resetPasswordActions";
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [fromValidationErrors, setFormValidationError] = useState({});
  const dispatch = useDispatch();
  const message = useSelector((state) => state.resetpassword.message);
  const statuscode = useSelector((state) => state.resetpassword.statuscode);

  const validateForm = () => {
    let errors = {};

    if (!email) {
      errors.email = "Email is required";
    }
    setFormValidationError(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
      dispatch(forgot(email));
    }
  };

  return (
    <Container style={{ paddingTop: 25 }}>
      <form id="login-form" onSubmit={handleSubmit}>
        <h1>Welcome to fpm Registry!</h1>
        <p>Please enter your email to Reset Password</p>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {fromValidationErrors.email && (
          <p className="error">{fromValidationErrors.email}</p>
        )}
       {message && (statuscode !== 200 ? (
          <p className="error">{message}</p>
        ) : (
          <p className="success">{message}</p>
        ))}
        <input type="submit" value="Forgot Password" />
        <p>
          Already have an account?<Link to="/account/login"> Login </Link>
        </p>
      </form>
    </Container>
  );
};

export default ForgotPassword;
