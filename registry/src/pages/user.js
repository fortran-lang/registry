import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchUserData } from "../store/actions/userActions";
import { MDBIcon } from "mdbreact";
import { useNavigate, useParams } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Figure from "react-bootstrap/Figure";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Spinner from "react-bootstrap/Spinner";
import PackageItem from "../components/packageItem";

const UserPage = () => {
  const { user } = useParams();
  const navigate = useNavigate();
  const email = useSelector((state) => state.user.email);
  const dateJoined = useSelector((state) => state.user.dateJoined);
  const projects = useSelector((state) => state.user.projects);
  const notFound = useSelector((state) => state.user.notFound);
  const isLoading = useSelector((state) => state.user.isLoading);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchUserData(user));
  }, [user, notFound]);

  if (notFound) {
    navigate("/404");
  }

  return !isLoading ? (
    <Container>
      <Row>
        <Col sm={4}>
          <Row style={{ marginLeft: "10px", marginTop: "20px" }}>
            <Figure>
              <Figure.Image
                width={171}
                height={180}
                alt={`Avatar for ${user} from gravatar.com`}
                src={`https://www.gravatar.com/avatar/${user}`}
              />
            </Figure>
          </Row>
          <Row
            style={{ marginLeft: "10px", marginTop: "10px", fontSize: "20px" }}
          >
            <MDBIcon style={{ marginTop: "5px" }} far icon="user-circle">
              {" " + user}
            </MDBIcon>
            <MDBIcon style={{ marginTop: "5px" }} far icon="calendar-alt">
              {" Joined " + Date(dateJoined).slice(4, 15)}
            </MDBIcon>

            <MDBIcon style={{ marginTop: "5px" }} far icon="envelope">
              {" " + email}
            </MDBIcon>
          </Row>
        </Col>
        <Col sm={8}>
          <Row style={{ fontSize: 24, marginTop: "20px" }}>
            {projects.length === 0
              ? "0 projects"
              : projects.length + " projects"}
          </Row>
          {projects.map((packageEntity) => (
        <PackageItem
          key={packageEntity.name + packageEntity.namespace}
          packageEntity={packageEntity}
        />
      ))}
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

export default UserPage;
