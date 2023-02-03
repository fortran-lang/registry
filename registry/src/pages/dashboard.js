import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useCookies } from "react-cookie";
import { fetchPackages } from "../store/actions/dashboardActions";
import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Spinner from "react-bootstrap/Spinner";
import Container from "react-bootstrap/Container";

const Dashboard = () => {
  const [cookies, setCookie] = useCookies(["uuid"]);
  const username = useSelector((state) => state.auth.username);
  const packages = useSelector((state) => state.dashboard.packages);
  const isLoading = useSelector((state) => state.dashboard.isLoading);
  const dispatch = useDispatch();

  useEffect(() => {
    if (packages === null) {
      dispatch(fetchPackages(username));
    }
  });

  return isLoading ? (
    <Spinner animation="border" role="status">
      <span className="visually-hidden">Loading...</span>
    </Spinner>
  ) : (
    <Container>
      <Row>
        {packages.map((element, index) => (
          <Col key={element.name + element.namespace_name} xs={6} md={4}>
            <Card>
              <Card.Body>
                <Card.Title>{element.name}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">
                  {element.namespace_name}
                </Card.Subtitle>
                <Card.Text id="card-text">{element.description}</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default Dashboard;
