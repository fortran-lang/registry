import React, { useState } from "react";
import axios from "axios";
import { Navigate } from "react-router-dom";
import { useCookies } from "react-cookie";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
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
        url: `${process.env.REACT_APP_REGISTRY_API_URL}/auth/signup`,
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
