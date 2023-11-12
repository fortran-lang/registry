import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { reset } from "../store/actions/resetPasswordActions";
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";

const ResetPassword = () => {
  const { uuid } = useParams();
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [fromValidationErrors, setFormValidationError] = useState({});
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const message = useSelector((state) => state.resetpassword.message);
  const statuscode = useSelector((state) => state.resetpassword.statuscode);

  const validateForm = () => {
    let errors = {};

    if (!password) {
      errors.password = "Password is required";
    }
    if (password !== confirmPassword) {
      errors.password = "Enter same password";
    }

    setFormValidationError(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
      dispatch(reset(password, uuid));
    }
  };

  return (
    <Container style={{ paddingTop: 25 }}>
      <form id="login-form" onSubmit={handleSubmit}>
        <h1>Welcome to fpm Registry!</h1>
        <p>Please enter your new Password</p>
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="password"
          name="confirm password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
        {fromValidationErrors.password && (
          <p className="error">{fromValidationErrors.password}</p>
        )}
        {message &&
          (statuscode !== 200 ? (
            <p className="error">{message}</p>
          ) : (
            <p className="success">{message}</p>
          ))}
        <input type="submit" value="Reset Password" />
        <p>
          Already have an account?<Link to="/account/login"> Login </Link>
        </p>
      </form>
    </Container>
  );
};

export default ResetPassword;
