import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Card, Container, Modal, Spinner } from "react-bootstrap";
import {
  fetchMalicousReports,
  resetData,
} from "../store/actions/viewMalicousReportActions";

const ViewMalicousReports = (props) => {
  const accessToken = useSelector((state) => state.auth.accessToken);
  const reports = useSelector((state) => state.malicousReport.reports);
  const loading = useSelector((state) => state.malicousReport.isLoading);
  const dispatch = useDispatch();

  useEffect(() => {
    if (!props.show) {
      return;
    }

    dispatch(fetchMalicousReports(accessToken));
  }, [props.show]);

  const onExit = () => {
    dispatch(resetData());
  };

  return (
    <Modal show={props.show} onHide={props.onHide} onExit={onExit}>
      <Modal.Header closeButton>
        <Modal.Title>View Malicious Reports</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {loading && (
          <div className="d-flex justify-content-center">
            <Spinner
              animation="border"
              role="status"
              style={{ alignItems: "center" }}
            >
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          </div>
        )}
        {reports.map((report, index) => {
          return (
            <Card key={index}>
              <Card.Body>
                <h5>Namespace - {report.namespace}</h5>
                <h6>Package - {report.package}</h6>
                <p style={{ textAlign: "left" }}>{report.reason}</p>
              </Card.Body>
            </Card>
          );
        })}
      </Modal.Body>
    </Modal>
  );
};

export default ViewMalicousReports;
