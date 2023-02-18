import { MDBListGroupItem } from "mdb-react-ui-kit";
import { Row, Col, Image } from "react-bootstrap";

const PackageItem = ({ packageEntity }) => {
  return (
    <MDBListGroupItem id="list-item">
      <Row>
        <Col md={1}>
          <Image
            src="https://fortran-lang.org/en/_static/fortran-logo-256x256.png"
            fluid
            width={60}
            height={60}
          />
        </Col>
        <Col md={4}>
          <div>
            <h5 id="list-item-package-name">{packageEntity.name}</h5>
          </div>
          <h6 className="mb-2 text-muted">{packageEntity.description}</h6>
          <h6 className="mb-2 text-muted">
            Namespace {packageEntity.namespace}
          </h6>
        </Col>
        <Col md={1} style={{ flex: 1 }}>
          <h6
            style={{
              textAlign: "right",
            }}
          >
            By {packageEntity.author}
          </h6>
        </Col>
      </Row>
    </MDBListGroupItem>
  );
};

export default PackageItem;
