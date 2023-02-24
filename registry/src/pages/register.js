import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import { useDispatch, useSelector } from "react-redux";
import { signup, resetErrorMessage } from "../store/actions/authActions";
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [cookies, setCookie] = useCookies(["uuid"]);
  const [fromValidationErrors, setFormValidationError] = useState({});
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const errorMessage = useSelector((state) => state.auth.error);
  const uuid = useSelector((state) => state.auth.uuid);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
      dispatch(signup(username, email, password));
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      setCookie("uuid", uuid);
      navigate("/manage/projects");
      window.location.reload();
    }

    if (errorMessage != null) {
      dispatch(resetErrorMessage());
    }
  }, [isAuthenticated]);

  const validateForm = () => {
    let errors = {};

    if (!username) {
      errors.username = "username is required";
    }

    if (!email) {
      errors.email = "Email is required";
    }

    if (!password) {
      errors.password = "Password is required";
    }

    setFormValidationError(errors);

    return Object.keys(errors).length === 0;
  };

  return (
    <Container style={{ paddingTop: 25 }}>
    <form id="login-form" onSubmit={handleSubmit}>
      <h1>Welcome to fpm Registry!</h1>
      <p>Please enter your details to Sign up.</p>
      <input
        type="text"
        name="username"
        placeholder="username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      {fromValidationErrors.email && (
        <p className="error">{fromValidationErrors.username}</p>
      )}
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
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {fromValidationErrors.email && (
        <p className="error">{fromValidationErrors.password}</p>
      )}
      {errorMessage != null ? <p className="error">{errorMessage}</p> : null}
      <input type="submit" value="Sign Up" />
      <p>
        Already have an account?<Link to="/account/login"> Log in </Link>
      </p>
    </form></Container>
  );
};

export default Register;
