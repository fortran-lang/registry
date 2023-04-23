import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { login, resetErrorMessage } from "../store/actions/authActions";
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";

const Login = () => {
  const [user_identifier, setUser_identifier] = useState("");
  const [password, setPassword] = useState("");
  const [fromValidationErrors, setFormValidationError] = useState({});
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const errorMessage = useSelector((state) => state.auth.error);

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/manage/projects");
      window.location.reload();
    }

    if (errorMessage !== null) {
      dispatch(resetErrorMessage());
    }
  }, [isAuthenticated]);

  const validateForm = () => {
    let errors = {};

    if (!user_identifier) {
      errors.user_identifier = "Email is required";
    }

    if (!password) {
      errors.password = "Password is required";
    }

    setFormValidationError(errors);

    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
      dispatch(login(user_identifier, password));
    }
  };

  return (
    <Container style={{ paddingTop: 25 }}>
      <form id="login-form" onSubmit={handleSubmit}>
        <h1>Welcome to fpm Registry!</h1>
        <p>Please enter your username/email and password to log in.</p>
        <input
          type="user_identifier"
          name="user_identifier"
          placeholder="Email"
          value={user_identifier}
          onChange={(e) => setUser_identifier(e.target.value)}
        />
        {fromValidationErrors.user_identifier && (
          <p className="error">{fromValidationErrors.user_identifier}</p>
        )}
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {fromValidationErrors.password && (
          <p className="error">{fromValidationErrors.password}</p>
        )}
        {errorMessage != null ? <p className="error">{errorMessage}</p> : null}
        <input type="submit" value="Log In" />
        <p>
          Don't have an account?<Link to="/account/register"> Sign up </Link>
        </p>
        <p>
          <Link to="/account/forgot-password"> Forgot password </Link>
        </p>
      </form>
    </Container>
  );
};

export default Login;
