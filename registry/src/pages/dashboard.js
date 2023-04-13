import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useCookies } from "react-cookie";
import { fetchPackages } from "../store/actions/dashboardActions";
import { useNavigate } from "react-router-dom";
import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Spinner from "react-bootstrap/Spinner";
import Container from "react-bootstrap/Container";
import AddMaintainerFormDialog from "./addMaintainerDialogForm";
import RemoveMaintainerFormDialog from "./removeMaintainerDialogForm";
import GenerateNamespaceTokenDialogForm from "./generateNamespaceTokenDialogForm";

const Dashboard = () => {
  const [cookies, setCookie] = useCookies(["uuid"]);
  const [showAddMaintainerDialog, setShowAddMaintainerDialog] = useState(false);
  const [showGenerateTokenDialog, setshowGenerateTokenDialog] = useState(false);
  const [showRemoveMaintainerDialog, setShowRemoveMaintainerDialog] =
    useState(false);
  const username = useSelector((state) => state.auth.username);
  const packages = useSelector((state) => state.dashboard.packages);
  const namespaces = useSelector((state) => state.dashboard.namespaces);
  const isLoading = useSelector((state) => state.dashboard.isLoading);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    if (!packages) {
      dispatch(fetchPackages(username));
    }

    if (username === null) {
      navigate("/");
    }
  }, [packages, username]);

  return isLoading ? (
    <div class="d-flex justify-content-center">
      <Spinner className="spinner-border m-5" animation="border" role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </div>
  ) : (
    <Container style={{ paddingTop: 25 }}>
      <p style={{ textAlign: "left", fontSize: 24, padding: 5 }}>Namespaces</p>
      {Namespaces()}
      <p style={{ textAlign: "left", fontSize: 24, padding: 5 }}>Packages</p>
      {Packages()}
    </Container>
  );

  function Packages() {
    return packages.length === 0 ? (
      <div className="alert alert-secondary" role="alert">
        You are not a maintainer of any package yet.
      </div>
    ) : (
      <Row>
        {packages.map((element, index) => (
          <Col key={element.name + element.namespace} xs={6} md={4}>
            <Card>
              <Card.Body>
                <Card.Title>
                  <a
                    href={`/packages/${element.namespace}/${element.name}`}
                    style={{ textDecoration: "none", color: "black" }}
                  >
                    {element.name}
                  </a>
                </Card.Title>
                <Card.Subtitle className="mb-2 text-muted">
                  {element.namespace}
                </Card.Subtitle>
                <Card.Text id="card-text">{element.description}</Card.Text>
                <p style={{ textAlign: "left", fontSize: 16 }}>
                  <a
                    href={`/package/create`}
                    style={{ textDecoration: "none" }}
                  >
                    Create New Release
                  </a>
                </p>
                <span
                  style={{ textAlign: "left", fontSize: 16 }}
                  onClick={() => setShowAddMaintainerDialog(true)}
                >
                  Add Maintainers
                </span>
                <AddMaintainerFormDialog
                  package={element.name}
                  namespace={element.namespace}
                  show={showAddMaintainerDialog}
                  onHide={() => setShowAddMaintainerDialog(false)}
                />
                <span
                  style={{ textAlign: "left", fontSize: 16 }}
                  onClick={() => setShowRemoveMaintainerDialog(true)}
                >
                  Remove Maintainers
                </span>
                <RemoveMaintainerFormDialog
                  package={element.name}
                  namespace={element.namespace}
                  show={showRemoveMaintainerDialog}
                  onHide={() => setShowRemoveMaintainerDialog(false)}
                />
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    );
  }

  function Namespaces() {
    return namespaces.length === 0 ? (
      <div className="alert alert-secondary" role="alert">
        You are not a maintainer of any namespace yet.
      </div>
    ) : (
      <Row>
        {namespaces.map((element, index) => (
          <Col key={element.name} xs={6} md={4}>
            <Card>
              <Card.Body>
                <Card.Title>
                  <a
                    href={`/namespaces/${element.name}`}
                    style={{ textDecoration: "none", color: "black" }}
                  >
                    {element.name}
                  </a>
                </Card.Title>
                <Card.Text id="card-text">{element.description}</Card.Text>
                <span
                  style={{ textAlign: "left", fontSize: 16 }}
                  onClick={() => setshowGenerateTokenDialog(true)}
                >
                  Generate Token
                </span>
                <GenerateNamespaceTokenDialogForm
                  namespace={element.name}
                  show={showGenerateTokenDialog}
                  onHide={() => setshowGenerateTokenDialog(false)}
                />
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    );
  }
};

export default Dashboard;
