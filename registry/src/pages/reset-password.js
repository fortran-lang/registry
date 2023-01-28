import React, { useState } from "react";
import axios from "axios";

const resetPassword = ({ setToken }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);
    
    try {
      const response = await axios({
        method: "post",
        url: `${process.env.REACT_APP_REGISTRY_API_URL}/auth/login`,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      if (response.status === 200) {
        //login successful
        console.log(response.data.statusText);

        setToken(response.data.statusText);
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

export default resetPassword;
