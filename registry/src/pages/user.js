import React from "react";
import { MDBIcon } from "mdbreact";
import { useNavigate, useParams } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Card from "react-bootstrap/Card";
import Image from "react-bootstrap/Image";
import Figure from "react-bootstrap/Figure";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import "./upload.css";

const UserPage = () => {
  const { user } = useParams();
  const navigate = useNavigate();
  const [email, setEmail] = React.useState("");
  const [dateJoined, setDateJoined] = React.useState("");
  const [projects, setProjects] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);

  const url = `${process.env.REACT_APP_REGISTRY_API_URL}/users/${user}`;

  if (isLoading) {
    fetch(url)
      .then((res) => {
        if (res.ok) {
          console.log("success");
          return res.json();
        } else {
          console.error("Error while sending request");
          setIsLoading(false);
          navigate("/404");
        }
      })
      .then((data) => {
        setDateJoined(data["user"].createdAt);
        setProjects(data["user"].packages);
        setEmail(data["user"].email);
        console.log(data);
        setIsLoading(false);
      });
  }

  return (
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
          {projects.map((element, index) => (
            <Row
              className="mb-2"
              key={element.name + element.namespace_name}
              xs={8}
              md={8}
            >
              <Card>
                {" "}
                <Card.Link
                  style={{ textDecoration: "none" }}
                  href={`/packages/${element.namespace_name}/${element.name}`}
                >
                  <Card.Body>
                    <Card.Title>{element.name}</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">
                      {element.namespace_name} / {element.name}{" "}
                    </Card.Subtitle>

                    <Card.Text id="card-text">
                      <div>Last released {element.updatedAt}</div>
                      <div> {element.description.slice(0, 40)}</div>
                    </Card.Text>
                  </Card.Body>
                </Card.Link>
              </Card>
            </Row>
          ))}
        </Col>
      </Row>
    </Container>
  );
};

export default UserPage;
