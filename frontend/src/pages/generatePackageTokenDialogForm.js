import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import {
  generatePackageToken,
  resetMessages,
} from "../store/actions/generatePackageTokenActions";

const GeneratePackageTokenDialogForm = (props) => {
  const [validationError, setValidationError] = useState("");
  const uuid = useSelector((state) => state.auth.uuid);
  const successMessage = useSelector(
    (state) => state.generatePackageToken.successMessage
  );
  const errorMessage = useSelector(
    (state) => state.generatePackageToken.errorMessage
  );
  const uploadToken = useSelector(
    (state) => state.generatePackageToken.uploadToken
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
      generatePackageToken({
        uuid: uuid,
        namespace: props.namespace,
        package: props.package,
      })
    );
  };

  const resetData = () => {
    setValidationError("");
    dispatch(resetMessages());
  };

  const validateForm = () => {
    if (!uuid) {
      setValidationError("uuid is required");
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
          Generate a package token for {props.package}
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

export default GeneratePackageTokenDialogForm;
