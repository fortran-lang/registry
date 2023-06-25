import React, { useEffect } from "react";
import Spinner from "react-bootstrap/Spinner";
import { useDispatch, useSelector } from "react-redux";
import Container from "react-bootstrap/Container";
import { fetchArchiveData } from "../store/actions/archivesActions";

const Archives = () => {
  const archives = useSelector((state) => state.archives.archives);
  const dispatch = useDispatch();
  const isLoading = useSelector((state) => state.archives.isLoading);

  useEffect(() => {
    dispatch(fetchArchiveData());
  }, []);

  const containerStyle = {
    textAlign: "left",
    fontFamily: "Arial, sans-serif",
    fontSize: "18px",
    lineHeight: "1.5",
    paddingLeft: "30px",
    paddingTop: "20px",
    paddinBottom: "20px",
    color: "#333",
    paddingRight: "30px",
  };

  const h2Style = {
    textAlign: "left",
    alignContent: "left",
    fontSize: "26px",
  };

  return !isLoading ? (
    <div style={containerStyle}>
      <h1>Archives</h1>
      <br></br>
      <h2 style={h2Style}>fpm - registry Archives</h2>
      <div>
        Here, you will find a collection of registry archives created at weekly
        intervals, showcasing the weekly snapshots of our registry. These
        archives serve as a valuable resource for tracking the evolution of our
        registry over time.
      </div>
      <br></br>
      <div>
        Each week, An archive is automatically compiled and stores a snapshot of our registry,
        capturing the state of namespaces, packages, and tarballs of the fpm - registry. These
        archives provide a comprehensive record of the changes and updates made
        to our registry.
      </div>
      <br></br>
      <ul>
        {archives.map((archive) => (
          <li>
            <a
              href={`${process.env.REACT_APP_REGISTRY_API_URL}/static/${archive}`}
            >
              {archive}
            </a>
          </li>
        ))}
      </ul>
    </div>
  ) : (
    <Container style={{ margin: "200px" }}>
      <Spinner animation="border" role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </Container>
  );
};

export default Archives;
