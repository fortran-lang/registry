import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import {
  removeNamespaceMaintainer,
  resetMessages,
} from "../store/actions/namespaceMaintainersActions";

const RemoveNamespaceMaintainerFormDialog = (props) => {
  const [username, setUsername] = useState("");
  const [validationError, setValidationError] = useState("");
  const currUsername = useSelector((state) => state.auth.username);
  const uuid = useSelector((state) => state.auth.uuid);
  const successMessage = useSelector(
    (state) => state.addRemoveNamespaceMaintainer.successMessage
  );
  const errorMessage = useSelector(
    (state) => state.addRemoveNamespaceMaintainer.errorMessage
  );

  const dispatch = useDispatch();

  const onSubmit = (event) => {
    dispatch(resetMessages());
    event.preventDefault();

    // If the form input is not valid. Do not proceed.
    if (!validateForm()) {
      return;
    }

    dispatch(
      removeNamespaceMaintainer(
        {
          uuid: uuid,
          namespace: props.namespace,
          username_to_be_removed: username,
          package: props.package,
        },
        currUsername
      )
    );
  };

  const resetData = () => {
    setUsername("");
    setValidationError("");
    dispatch(resetMessages());
  };

  const validateForm = () => {
    if (!username) {
      setValidationError("Username is required");
      return false;
    }

    setValidationError("");
    return true;
  };

  return (
    <form id="add-maintainer-form">
      <Modal
        {...props}
        size="md"
        aria-labelledby="contained-modal-title-vcenter"
        centered
        onExit={resetData}
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            Remove namespace maintainer
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
          {validationError && (
            <p id="add-maintainer-error">{validationError}</p>
          )}
          {successMessage && (
            <p id="add-maintainer-success">{successMessage}</p>
          )}
          {errorMessage && <p id="add-maintainer-error">{errorMessage}</p>}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger" onClick={onSubmit}>
            Remove
          </Button>
        </Modal.Footer>
      </Modal>
    </form>
  );
};

export default RemoveNamespaceMaintainerFormDialog;
