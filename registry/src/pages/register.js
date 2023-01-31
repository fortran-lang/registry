import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";
import { useDispatch, useSelector } from "react-redux";
import { signup } from "../store/actions/authActions";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [cookies, setCookie] = useCookies(["uuid"]);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const errorMessage = useSelector((state) => state.auth.error);
  const uuid = useSelector((state) => state.auth.uuid);

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(signup(name, email, password));
  };

  useEffect(() => {
    if (isAuthenticated) {
      setCookie("uuid", uuid);
      navigate("/manage/projects");
    } else if (errorMessage !== null) {
      const errorDiv = document.getElementById("error");
      errorDiv.innerHTML = errorMessage;
    }
  }, [isAuthenticated, errorMessage]);

  return (
    <form id="login-form" onSubmit={handleSubmit}>
      <h1>Welcome to fpm Registry!</h1>
      <p>Please enter your details to Sign up.</p>
      <input
        type="text"
        name="name"
        placeholder="name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
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
      <input type="submit" value="Sign Up" />
    </form>
  );
};

export default Register;
