import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../store/actions/authActions";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [cookies, setCookie] = useCookies(["uuid"]);
  const navigate = useNavigate();

  const dispatch = useDispatch();

  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const errorMessage = useSelector((state) => state.auth.error);

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/manage/projects");
    } else if (errorMessage !== null) {
      const errorDiv = document.getElementById("error");
      errorDiv.innerHTML = errorMessage;
    }
  }, [isAuthenticated]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(login(email, password));
  };

  return (
    <form id="login-form" onSubmit={handleSubmit}>
      <h1>Welcome to fpm Registry!</h1>
      <p>Please enter your email and password to log in.</p>
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <p id="error" className="error"></p>
      <input type="submit" value="Log In" />
    </form>
  );
};

export default Login;
