import React, { useState } from "react";
import axios from "axios";
import { Navigate } from "react-router-dom";
import { useCookies } from 'react-cookie';

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [cookies, setCookie] = useCookies(['uuid']);


  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("password", password);

    try {
      const response = await axios({
        method: "post",
        url: "http://127.0.0.1:9090/auth/signup",
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      if (response.status === 200) {
        //login successful
        console.log(response.data.uuid);
        setCookie('uuid', response.data.uuid, { path: '/' });
        // setCookie("uuid", response.data.uuid, "100");
        return <Navigate to="/search" replace={true} />;
      }
    } catch (error) {
      console.log(error.response.data);
      console.log(error.response.status);
      console.log(error.response.statusText);

      const responseText = error.response.data;
      const errorMsg = `${responseText}`;
      const errorDiv = document.getElementById("error");
      errorDiv.innerHTML = errorMsg;
    }
  };
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
