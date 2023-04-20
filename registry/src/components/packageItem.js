import { MDBListGroupItem } from "mdb-react-ui-kit";
import { Row, Col, Image } from "react-bootstrap";

const PackageItem = ({ packageEntity }) => {
  function formatDate(timestamp) {
    const now = new Date();
    const date = new Date(timestamp);

    // Check if the date is less than 12 hours ago
    const diff = (now.getTime() - date.getTime()) / 1000;
    if (diff < 43200) {
      // 12 hours = 43,200 seconds
      // Calculate minutes or hours ago
      const minutes = Math.floor(diff / 60);
      if (minutes < 60) {
        return `${minutes} minutes ago`;
      } else {
        const hours = Math.floor(minutes / 60);
        return `${hours} hours ago`;
      }
    } else {
      // Format date in "YYYY-MM-DD" format
      const year = date.getUTCFullYear();
      const month = String(date.getUTCMonth() + 1).padStart(2, "0");
      const monthName = new Date(Date.UTC(year, month, 1)).toLocaleString(
        "en-US",
        { month: "long" }
      );
      const day = String(date.getUTCDate()).padStart(2, "0");

      return `${monthName} ${day},  ${year}`;
    }
  }

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
            <h5 id="list-item-package-name">
              <a
                href={`/packages/${packageEntity.namespace}/${packageEntity.name}`}
                style={{ textDecoration: "none" }}
              >
                {packageEntity.name}
              </a>
            </h5>
          </div>
          <h6 className="mb-2 text-muted">
            Namespace {packageEntity.namespace}
          </h6>
          <label className="mb-2 text-muted">{packageEntity.description}</label>
        </Col>
        <Col md={1} style={{ flex: 1, textAlign: "right" }}>
          <h6>By {packageEntity.author}</h6>
          <label>{formatDate(packageEntity.updatedAt)}</label>
        </Col>
      </Row>
    </MDBListGroupItem>
  );
};

export default PackageItem;
