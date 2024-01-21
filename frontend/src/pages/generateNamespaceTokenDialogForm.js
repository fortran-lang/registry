import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import {
  generateToken,
  resetMessages,
} from "../store/actions/generateNamespaceTokenActions";

const GenerateNamespaceTokenDialogForm = (props) => {
  const [validationError, setValidationError] = useState("");
  const accessToken = useSelector((state) => state.auth.accessToken);
  const successMessage = useSelector(
    (state) => state.generateNamespaceToken.successMessage
  );
  const errorMessage = useSelector(
    (state) => state.generateNamespaceToken.errorMessage
  );
  const uploadToken = useSelector(
    (state) => state.generateNamespaceToken.uploadToken
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
      generateToken({
        accessToken: accessToken,
        namespace: props.namespace,
      })
    );
  };

  const resetData = () => {
    setValidationError("");
    dispatch(resetMessages());
  };

  const validateForm = () => {
    if (!accessToken) {
      setValidationError("Access token is required");
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
            Generate token
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Generate a namespace token for {props.namespace}
          {validationError && (
            <p id="add-maintainer-error">{validationError}</p>
          )}
          {successMessage && (
            <p id="add-maintainer-success">
              {successMessage}: {uploadToken}
            </p>
          )}
          {errorMessage && <p id="add-maintainer-error">{errorMessage}</p>}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="success" onClick={onSubmit}>
            Generate Token
          </Button>
        </Modal.Footer>
      </Modal>
    </form>
  );
};

export default GenerateNamespaceTokenDialogForm;
