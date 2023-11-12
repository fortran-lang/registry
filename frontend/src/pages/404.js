import React from "react";
import "./404.css";

const NoPage = () => {
  return (
    <div class="container">
      <br></br>
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>
        The Page you are looking for doesn't exist or an other error occured. Go
        to <a href="/">Home Page.</a>
      </p>
    </div>
  );
};

export default NoPage;
