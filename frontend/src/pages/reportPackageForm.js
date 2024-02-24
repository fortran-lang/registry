import React, { useEffect, useState } from "react";
import { Form, Button, Modal, Spinner } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import {
  reportPackage,
  resetErrorMessage,
} from "../store/actions/reportPackageActions";
import { toast, ToastContainer } from "react-toastify";
import { reset } from "../store/actions/accountActions";

const ReportPackageForm = (props) => {
  const dispatch = useDispatch();
  const [reason, setReason] = useState("");
  const accessToken = useSelector((state) => state.auth.accessToken);
  const isLoading = useSelector((state) => state.reportPackage.isLoading);
  const statusCode = useSelector((state) => state.reportPackage.statuscode);
  const message = useSelector((state) => state.reportPackage.message);

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(
      reportPackage(
        { reason: reason, namespace: props.namespace, package: props.package },
        accessToken
      )
    );
  };

  useEffect(() => {
    if (statusCode === 200) {
      toast.success(message);
    } else {
      toast.error(message);
    }

    dispatch(resetErrorMessage());
  }, [statusCode]);

  return (
    <Form onSubmit={handleSubmit}>
      <Modal {...props} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Report Package</Modal.Title>
        </Modal.Header>
        <ToastContainer
          position="top-center"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          pauseOnHover
          theme="light"
        />
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
          {!isLoading ? (
            <Button variant="primary" type="submit" onClick={handleSubmit}>
              Submit
            </Button>
          ) : (
            <div style={{ margin: 0 }}>
              <Spinner
                className="spinner-border m-3"
                animation="border"
                role="status"
              >
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            </div>
          )}
        </Modal.Footer>
      </Modal>
    </Form>
  );
};

export default ReportPackageForm;
