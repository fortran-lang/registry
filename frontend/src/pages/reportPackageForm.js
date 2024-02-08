import React, { useState } from "react";
import { Form, Button, Modal } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { reportPackage } from "../store/actions/reportPackageActions";

const ReportPackageForm = (props) => {
  const dispatch = useDispatch();
  const [reason, setReason] = useState("");
  const accessToken = useSelector((state) => state.auth.accessToken);

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(
      reportPackage(
        { reason: reason, namespace: props.namespace, package: props.package },
        accessToken
      )
    );
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Modal {...props} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Report Package</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group
            className="mb-3"
            controlId="formReportPackage"
            id="namespace-description-textfield"
          >
            <Form.Label>Reason for reporting package</Form.Label>
            <Form.Control
              type="text"
              placeholder="Describe the reason for reporting the package"
              as="textarea"
              name="report_description"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            />
            <Form.Text className="text-muted">
              Write a brief description of the reason for reporting the package.
            </Form.Text>
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" type="submit" onClick={handleSubmit}>
            Submit
          </Button>
        </Modal.Footer>
      </Modal>
    </Form>
  );
};

export default ReportPackageForm;
