import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchPackageData } from "../store/actions/packageActions";
import { useNavigate, useParams } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Spinner from "react-bootstrap/Spinner";

const PackagePage = () => {
  const { namespace_name, package_name } = useParams();
  const navigate = useNavigate();
  const author = useSelector((state) => state.package.author);
  const tags = useSelector((state) => state.package.tags);
  const license = useSelector((state) => state.package.license);
  const createdAt = useSelector((state) => state.package.createdAt);
  const versionData = useSelector((state) => state.package.versionData);
  const updatedAt = useSelector((state) => state.package.updatedAt);
  const description = useSelector((state) => state.package.description);
  const notFound = useSelector((state) => state.package.notFound);
  const isLoading = useSelector((state) => state.package.isLoading);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchPackageData(namespace_name, package_name));
  }, [namespace_name, package_name]);

  if (notFound) {
    navigate("/404");
  }

  return !isLoading ? (
    <Container>
      <Row>
        <Col>
          <Card>
            <Card.Body>
              {/*    WIP - Psckage Description Page
               <Card.Title>{package_name}</Card.Title>
              <Card.Subtitle>{namespace_name} / {package_name}</Card.Subtitle>
              <Card.Text>
                <p>Author: {author}</p>    
                <p>Tags: {tags.join(",")}</p>
                <p>License: {license}</p>
                <p>Created At: {createdAt}</p>
                <p>Version Data: {versionData.join(",")}</p>
                <p>Updated At: {updatedAt}</p>
                <p>{description}</p>
              </Card.Text> */}
              <Button variant="primary" href={`/download/${namespace_name}/${package_name}`}>
                Download
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  ) : (
    <Container style={{ margin: "200px" }}>
      <Spinner animation="border" role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </Container>
  );
};

export default PackagePage;