import { Card, Modal } from "react-bootstrap";
import { Form } from "react-bootstrap";

const ReportPackageForm = (props) => {
  return (
    <Form onSubmit={() => {}}>
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
            />
            <Form.Text className="text-muted">
              Write a brief description of the reason for reporting the package.
            </Form.Text>
          </Form.Group>
        </Modal.Body>
      </Modal>
    </Form>
  );
};

export default ReportPackageForm;
