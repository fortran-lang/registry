import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
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
import AddNamespaceMaintainerFormDialog from "./addNamespaceMaintainerDialogForm";
import RemoveNamespaceMaintainerFormDialog from "./removeNamespaceMaintainerDialogForm";

const Dashboard = () => {
  const [addMaintainerDialogState, setAddMaintainerDialogState] = useState({});
  const [showGenerateTokenDialog, setshowGenerateTokenDialog] = useState({});
  const [removeMaintainerDialogState, setRemoveMaintainerDialogState] =
    useState({});
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

  const handleAddMaintainerDialog = (itemId, value) => {
    setAddMaintainerDialogState((prevState) => ({
      ...prevState,
      [itemId]: value,
    }));
  };

  const handleRemoveMaintainerDialog = (itemId, value) => {
    setRemoveMaintainerDialogState((prevState) => ({
      ...prevState,
      [itemId]: value,
    }));
  };

  const handleGenerateTokenDialog = (itemId, value) => {
    setshowGenerateTokenDialog((prevState) => ({
      ...prevState,
      [itemId]: value,
    }));
  };

  return isLoading ? (
    <div className="d-flex justify-content-center">
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
          <Col key={element.id} xs={6} md={4}>
            <Card id="dashboard-card">
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
                <div
                  className="border border-success rounded-pill chip-action"
                  onClick={() => handleAddMaintainerDialog(element.id, true)}
                >
                  Add Maintainers
                </div>
                <AddMaintainerFormDialog
                  package={element.name}
                  namespace={element.namespace}
                  show={addMaintainerDialogState[element.id]}
                  onHide={() => handleAddMaintainerDialog(element.id, false)}
                />
                {element.isNamespaceMaintainer ? (
                  <div
                    className="border border-danger rounded-pill chip-action"
                    onClick={() =>
                      handleRemoveMaintainerDialog(element.id, true)
                    }
                  >
                    Remove Maintainers
                  </div>
                ) : null}
                <RemoveMaintainerFormDialog
                  package={element.name}
                  namespace={element.namespace}
                  show={removeMaintainerDialogState[element.id]}
                  onHide={() => handleRemoveMaintainerDialog(element.id, false)}
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
            <Card id="dashboard-card">
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
                <div
                  className="border border-success rounded-pill chip-action"
                  onClick={() => handleGenerateTokenDialog(element.id, true)}
                >
                  Generate Token
                </div>
                <GenerateNamespaceTokenDialogForm
                  namespace={element.name}
                  show={showGenerateTokenDialog[element.id]}
                  onHide={() => handleGenerateTokenDialog(element.id, false)}
                />
                <div
                  className="border border-success rounded-pill chip-action"
                  onClick={() => handleAddMaintainerDialog(element.id, true)}
                >
                  Add maintainers
                </div>
                <AddNamespaceMaintainerFormDialog
                  namespace={element.name}
                  show={addMaintainerDialogState[element.id]}
                  onHide={() => handleAddMaintainerDialog(element.id, false)}
                />
                {element.isNamespaceAdmin ? (
                  <div
                    className="border border-danger rounded-pill chip-action"
                    onClick={() =>
                      handleRemoveMaintainerDialog(element.id, true)
                    }
                  >
                    Remove maintainers
                  </div>
                ) : null}

                <RemoveNamespaceMaintainerFormDialog
                  namespace={element.name}
                  show={removeMaintainerDialogState[element.id]}
                  onHide={() => handleRemoveMaintainerDialog(element.id, false)}
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
