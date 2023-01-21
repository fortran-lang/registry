import React, { useState } from "react";
import axios from "axios";
import { Navigate } from "react-router-dom";
import { useCookies } from "react-cookie";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [cookies, setCookie] = useCookies(["uuid"]);
  const [navigate, setNavigate] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    if (!cookies.uuid) {
      formData.append("email", email);
      formData.append("password", password);
    } else {
      formData.append("uuid", cookies.uuid);
    }
    var response;
    try {
      response = await axios({
        method: "post",
        url: "http://127.0.0.1:9090/auth/login",
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    } catch (error) {
      setCookie("uuid", "", "100");
      const errorMsg = `${error.response.data}`;
      const errorDiv = document.getElementById("error");
      errorDiv.innerHTML = errorMsg;
    }
    if (response.status === 200) {
      setCookie("uuid", response.data.uuid, { path: "/" });
      setNavigate(true);
    }
  };
  if (navigate) {
    return <Navigate to="/manage/projects" replace={true} />;
  }
  
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
