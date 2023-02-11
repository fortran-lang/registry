import React from "react";
import { MDBIcon } from "mdbreact";
import { useNavigate, useParams } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import "./upload.css";

const UserPage = () => {
  const { user } = useParams();
  const navigate = useNavigate();
  const [email, setEmail] = React.useState("");
  const [dateJoined, setDateJoined] = React.useState("");
  const [projects, setProjects] = React.useState([]);

  const url = `${process.env.REACT_APP_REGISTRY_API_URL}/users/${user}`;
  fetch(url)
    .then((res) => {
      if (res.ok) {
        console.log("success");
        return res.json();
      } else {
        console.error("Error while sending request");
        navigate("/404");
      }
    })
    .then((data) => {
      setDateJoined(data["user"].date_joined);
      setProjects(data["user"].packages);
      setEmail(data["user"].email);
      console.log(data);
    });

  return (
    <Container>
      <Card className="user-card" style={{ width: '18rem' }}>
        <Card.Img 
          variant="top" 
          src={`https://www.gravatar.com/avatar/${user}`}
          alt={`Avatar for ${user} from gravatar.com`}
          title={`Avatar for ${user} from gravatar.com`}
        />
        <Card.Body>
          <Card.Title>
            <MDBIcon fas icon="user-circle" />
            {user}
          </Card.Title>
          <Card.Text>
            Some quick example text to build on the card title and make up the
            bulk of the card's content.
          </Card.Text>
          <Button variant="primary">Go somewhere</Button>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default UserPage;