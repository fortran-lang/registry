import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import {
  MDBIcon,
  MDBTabs,
  MDBTabsItem,
  MDBTabsLink,
  MDBTabsContent,
  MDBTabsPane,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBTable,
  MDBTableBody,
  MDBTableHead,
} from "mdb-react-ui-kit";
import Container from "react-bootstrap/Container";
import Spinner from "react-bootstrap/Spinner";
import {
  fetchPackageData,
  verifyUserRole,
} from "../store/actions/packageActions";
import ShowUserListDialog from "./showUserListDialog";
import ReportPackageForm from "./reportPackageForm";
import { Button } from "react-bootstrap";
import PackageRatingGraph from "./packageRatingGraph";

const PackagePage = () => {
  const [iconsActive, setIconsActive] = useState("readme");
  const { namespace_name, package_name } = useParams();
  const dispatch = useDispatch();
  const statuscode = useSelector((state) => state.package.statuscode);
  const data = useSelector((state) => state.package.data);
  const isLoading = useSelector((state) => state.package.isLoading);
  const navigate = useNavigate();
  const [togglePackageMaintainersDialog, settogglePackageMaintainersDialog] =
    useState(false);
  const [showReportForm, setShowReportForm] = useState(false);

  const handleIconsClick = (value) => {
    if (value === iconsActive) {
      return;
    }

    setIconsActive(value);
  };

  useEffect(() => {
    dispatch(fetchPackageData(namespace_name, package_name));
    if (statuscode === 404) {
      navigate("/404");
    }
  }, [namespace_name, package_name]);

  return !isLoading ? (
    <Container style={{ paddingTop: 25 }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <p style={{ textAlign: "left", fontSize: 24 }}>{data.name}</p>

        <ViewPackageMaintainersButton
          namespace_name={namespace_name}
          package_name={package_name}
          settogglePackageMaintainersDialog={settogglePackageMaintainersDialog}
        />

        <ShowUserListDialog
          packagemaintainers={true}
          show={togglePackageMaintainersDialog}
          onHide={() => settogglePackageMaintainersDialog(false)}
          package={package_name}
          namespace={namespace_name}
        />
      </div>

      <p style={{ textAlign: "left", fontSize: 16 }}>
        v{data.latest_version_data.version} Published{" "}
        {updatedDays(data.updated_at)} days ago
      </p>
      <p>
      </p>
      <MDBTabs className="mb-3">
        <MDBTabsItem>
          <MDBTabsLink
            onClick={() => handleIconsClick("readme")}
            active={iconsActive === "readme"}
          >
            <MDBIcon fab icon="readme" className="me-2" /> Readme
          </MDBTabsLink>
        </MDBTabsItem>
        <MDBTabsItem>
          <MDBTabsLink
            onClick={() => handleIconsClick("dependencies")}
            active={iconsActive === "dependencies"}
          >
            <MDBIcon fas icon="boxes" className="me-2" /> {" Dependencies"}
          </MDBTabsLink>
        </MDBTabsItem>
        <MDBTabsItem>
          <MDBTabsLink
            onClick={() => handleIconsClick("versions")}
            active={iconsActive === "versions"}
          >
            <MDBIcon fas icon="tag" className="me-2" /> Versions
          </MDBTabsLink>
        </MDBTabsItem>
        <MDBTabsItem>
          <MDBTabsLink
            onClick={() => handleIconsClick("stats")}
            active={iconsActive === "stats"}
          >
            <MDBIcon fas icon="chart-bar" className="me-2" /> Stats
          </MDBTabsLink>
        </MDBTabsItem>
      </MDBTabs>

      <MDBTabsContent sm={4}>
        <MDBTabsPane show={iconsActive === "readme"}>
          <MDBContainer>
            <MDBRow>
              <MDBCol size="9">{data.description}</MDBCol>

              {sideBar(data, setShowReportForm)}
            </MDBRow>
          </MDBContainer>
        </MDBTabsPane>
        <MDBTabsPane show={iconsActive === "dependencies"}>
          <MDBContainer>
            <MDBRow>
              <MDBCol size="9">
                <p style={{ fontSize: 24, textAlign: "left" }}>Dependencies</p>
                <hr />

                <br />
              </MDBCol>
              {sideBar(data)}
            </MDBRow>
          </MDBContainer>
        </MDBTabsPane>
        <MDBTabsPane show={iconsActive === "versions"}>
          <MDBContainer>
            <MDBRow>
              <MDBCol size="9">
                <p style={{ fontSize: 24, textAlign: "left" }}>
                  Version History
                </p>
                <hr></hr>
                <MDBTable hover>
                  <MDBTableHead>
                    <tr>
                      <th scope="col" colSpan={3}>
                        Version
                      </th>
                      <th scope="col" colSpan={3}>
                        Published
                      </th>
                      <th scope="col" colSpan={3}>
                        Deprecated
                      </th>
                    </tr>
                  </MDBTableHead>
                  <MDBTableBody>
                    {sortedVersions(data.version_history).map((ver) => (
                      <tr key={ver.version}>
                        <td colSpan={3}>
                          <a
                            href={`${process.env.REACT_APP_REGISTRY_API_URL}${ver.download_url}`}
                            style={{ textDecoration: "none" }}
                          >
                            v{ver.version}
                          </a>
                        </td>
                        <td colSpan={3}>
                          {updatedDays(ver.created_at)} Days ago
                        </td>
                        <td colSpan={3}>
                          {ver.isDeprecated === "true" ? "Yes" : "No"}
                        </td>
                      </tr>
                    ))}
                  </MDBTableBody>
                </MDBTable>
              </MDBCol>
              {sideBar(data)}
            </MDBRow>
          </MDBContainer>
        </MDBTabsPane>
        <MDBTabsPane show={iconsActive === "stats"}>
          <MDBContainer>
            <PackageRatingGraph data={data.ratings_count} />
          </MDBContainer>
        </MDBTabsPane>
      </MDBTabsContent>
      <ReportPackageForm
        namespace={namespace_name}
        package={package_name}
        show={showReportForm}
        onHide={() => setShowReportForm(false)}
      />
    </Container>
  ) : (
    <Container style={{ margin: "200px" }}>
      <Spinner animation="border" role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </Container>
  );
};

export default PackagePage;

const ViewPackageMaintainersButton = ({
  namespace_name,
  package_name,
  settogglePackageMaintainersDialog,
}) => {
  const dispatch = useDispatch();
  const uuid = useSelector((state) => state.auth.uuid);
  const isVerified = useSelector((state) => state.package.isVerified);

  useEffect(() => {
    // Only make the API request when the user is logged in.
    if (uuid) {
      dispatch(verifyUserRole(namespace_name, package_name, uuid));
    }
  }, []);

  return (
    <React.Fragment>
      {isVerified && (
        <p
          className="border border-success"
          style={{
            padding: "8px",
            borderRadius: "25px",
            fontSize: "14px",
            color: "green",
            cursor: "pointer",
          }}
          onClick={() => settogglePackageMaintainersDialog(true)}
        >
          View Package Maintainers
        </p>
      )}
    </React.Fragment>
  );
};

const sideBar = (data, setShowReportForm) => {
  return (
    <MDBCol size="3">
      <p style={{ fontSize: 16, textAlign: "left" }}>Install (add to fpm.toml)</p>
      <p style={{ fontSize: 16, textAlign: "left" }}><code>{data.name} = {"{"}{"'namespace'"}: {"'"}{data.namespace}{"'}"}</code> </p>
      <hr></hr>
      <p style={{ fontSize: 16, textAlign: "left" }}>Repository</p>
      <Container> {data.repository}</Container>
      <hr></hr>
      <p style={{ fontSize: 16, textAlign: "left" }}>Homepage</p>
      <Container>{data.homepage}</Container>
      <hr></hr>
      <p style={{ fontSize: 16, textAlign: "left" }}>License</p>
      {data.license}
      <hr></hr>
      <p style={{ fontSize: 16, textAlign: "left" }}>Version</p>
      {data.latest_version_data.version}
      <hr></hr>
      <p style={{ fontSize: 16, textAlign: "left" }}>Last publish</p>
      {updatedDays(data.updated_at)} days ago
      <hr></hr>
      <Button
        variant="danger"
        style={{ margin: 0 }}
        onClick={() => setShowReportForm(true)}
      >
        Report
      </Button>
    </MDBCol>
  );
};

const updatedDays = (date) => {
  var updatedDate = new Date(date);
  var currentDate = new Date();
  var updatedTime = currentDate.getTime() - updatedDate.getTime();
  var updatedDays = Math.ceil(updatedTime / (1000 * 60 * 60 * 24));
  return updatedDays;
};

const sortedVersions = (version) => {
  let sortedVersions = [...version];
  return sortedVersions.sort((a, b) => {
    const [aMajor, aMinor, aPatch] = a.version.split(".").map(Number);
    const [bMajor, bMinor, bPatch] = b.version.split(".").map(Number);

    if (aMajor === bMajor) {
      if (aMinor === bMinor) {
        return bPatch - aPatch;
      } else {
        return bMinor - aMinor;
      }
    } else {
      return bMajor - aMajor;
    }
  });
};
