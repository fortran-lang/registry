import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";

const AddMaintainerFormDialog = (props) => {
  const [username, setUsername] = useState("");
  const [validationError, setValidationError] = useState("");

  console.log(!validationError);

  useEffect(() => {
    if (validationError.length !== 0 && username.length !== 0) {
      validateForm(username);
    }
  }, []);

  const checkValidity = (event) => {
    event.preventDefault();

    // If the form input is not valid. Do not proceed.
    if (!validateForm(username)) {
      return;
    }
  };

  const validateForm = (username) => {
    if (!username) {
      setValidationError("Username is required");
    } else {
      setValidationError("");
    }

    return validationError === "";
  };

  return (
    <form id="add-matainer-form" onSubmit={checkValidity}>
      <Modal
        {...props}
        size="sm"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            Add maintainers
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <label>Enter username</label>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={username}
            id="add-maintainer-input"
            onChange={(e) => setUsername(e.target.value)}
          />
          <p className="error">{validationError}</p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="success" onClick={checkValidity}>
            Add
          </Button>
        </Modal.Footer>
      </Modal>
    </form>
  );
};

export default AddMaintainerFormDialog;
