import React, { useState } from "react";
import { useCookies } from "react-cookie";
import { Navigate } from "react-router-dom";
import "./upload.css";

const UserPage = () => {
  const [cookies, setCookie] = useCookies(["uuid"]);
  const responseDiv = document.getElementById("error");

  const [data, setData] = useState({
    name: "",
    namespace: "",
    tarball: "",
    version: "",
    license: "",
    copyright: "",
    description: "",
    namespace_description: "",
    tags: "",
    dependencies: "",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setData({ ...data, [name]: value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch(`${process.env.REACT_APP_REGISTRY_API_URL}/packages`, {
      method: "POST",
      body: new FormData(event.target),
    }).then((res) => {
      if (res.ok) {
        console.log("created");
      } else {
        console.error("Error while sending request");
      }
      console.log(res);

      responseDiv.innerHTML = `${res.data}`;
    });
  };
  if (!cookies.uuid) {
    return <Navigate to="/account/login" replace={true} />;
  } else {
    return (
      <div className="container">
        <h2>Create a Package</h2>
        <form id="package-form" onSubmit={handleSubmit}>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={data.name}
            onChange={handleChange}
          />
          <br />
          <label htmlFor="namespace">Namespace:</label>
          <input
            type="text"
            id="namespace"
            name="namespace"
            value={data.namespace}
            onChange={handleChange}
          />
          <br />
          <label htmlFor="tarball">Tarball:</label>
          <input
            type="file"
            id="tarball"
            name="tarball"
            value={data.tarball}
            onChange={handleChange}
          />
          <br />
          <label htmlFor="version">Version:</label>
          <input
            type="text"
            id="version"
            name="version"
            value={data.version}
            onChange={handleChange}
          />
          <br />
          <label htmlFor="license">License:</label>
          <input
            type="text"
            id="license"
            name="license"
            value={data.license}
            onChange={handleChange}
          />
          <br />
          <label htmlFor="copyright">Copyright:</label>
          <input
            type="text"
            id="copyright"
            name="copyright"
            value={data.copyright}
            onChange={handleChange}
          />
          <br />
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            name="description"
            value={data.description}
            onChange={handleChange}
          />
          <br />
          <label htmlFor="namespace_description">Namespace Description:</label>
          <textarea
            id="namespace_description"
            name="namespace_description"
            value={data.namespace_description}
            onChange={handleChange}
          />
          <br />
          <label htmlFor="tags">Tags (comma separated):</label>
          <input
            type="text"
            id="tags"
            name="tags"
            value={data.tags}
            onChange={handleChange}
          />
          <br />
          <label htmlFor="dependencies">Dependencies (comma separated):</label>
          <input
            type="text"
            id="dependencies"
            name="dependencies"
            value={data.dependencies}
            onChange={handleChange}
          />
          <input
            type="hidden"
            id="uuid"
            name="uuid"
            value={cookies.uuid}
            onChange={handleChange}
          />
          <br />
          <p id="error" className="error"></p>
          <button type="submit">Add Package</button>
        </form>
      </div>
    );
  }
};

export default UserPage;
