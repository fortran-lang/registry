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
import { fetchPackageData } from "../store/actions/packageActions";

const PackagePage = () => {
  const [iconsActive, setIconsActive] = useState("readme");
  const { namespace_name, package_name } = useParams();
  const dispatch = useDispatch();
  const statuscode = useSelector((state) => state.package.statuscode);
  const data = useSelector((state) => state.package.data);
  const isLoading = useSelector((state) => state.package.isLoading);
  const navigate = useNavigate();

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
      <p style={{ textAlign: "left", fontSize: 24 }}>{data.name}</p>
      <div style={{ textAlign: "left", fontSize: 16 }}>
        v{data.latest_version_data.version} Published{" "}
        {updatedDays(data.updatedAt)} days ago
      </div>
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
      </MDBTabs>

      <MDBTabsContent sm={4}>
        <MDBTabsPane show={iconsActive === "readme"}>
          <MDBContainer>
            <MDBRow>
              <MDBCol size="9">
                <p style={{ fontSize: 20, textAlign: "left" }}>README</p>

                {data.description}
              </MDBCol>

              {sideBar(data)}
            </MDBRow>
          </MDBContainer>
        </MDBTabsPane>
        <MDBTabsPane show={iconsActive === "dependencies"}>
          <MDBContainer>
            <MDBRow>
              <MDBCol size="9">
                <p style={{ fontSize: 24, textAlign: "left" }}>Dependencies</p>
                <hr></hr>
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
                <MDBTable striped>
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
                    {data.version_history.map((ver) => (
                      <tr key={ver.version}>
                        <td colSpan={3}>
                          <a
                            href={`/packages/${namespace_name}/${package_name}`}
                            style={{ textDecoration: "none" }}
                          >
                            v{ver.version}
                          </a>
                        </td>
                        <td colSpan={3}>
                          {updatedDays(ver.createdAt)} Days ago
                        </td>
                        <td colSpan={3}>
                          {ver.isDeprecated == "true" ? "Yes" : "No"}
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
      </MDBTabsContent>
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

const sideBar = (data) => {
  return (
    <MDBCol size="3">
      {/* TODO: update Package API for url,website,maintainers */}
      <p style={{ fontSize: 16, textAlign: "left" }}>Install</p>
      <code style={{ background: "#ffffff" }}>
        fpm install {data.namespace}/{data.name}
      </code>
      <p style={{ fontSize: 16, textAlign: "left" }}>Repository</p>
      {/* <Container> { data.url }</Container> */}
      <hr></hr>
      <p style={{ fontSize: 16, textAlign: "left" }}>Homepage</p>
      {/* <Container>{ data.website }</Container> */}
      <hr></hr>
      <p style={{ fontSize: 16, textAlign: "left" }}>License</p>
      {data.license}
      <hr></hr>
      <p style={{ fontSize: 16, textAlign: "left" }}>Version</p>
      {data.latest_version_data.version}
      <hr></hr>
      <p style={{ fontSize: 16, textAlign: "left" }}>Last publish</p>
      {updatedDays(data.updatedAt)} days ago
      <hr></hr>
      <p style={{ fontSize: 16, textAlign: "left" }}>Maintainers</p>
      {/* <Container>{{ maintainers }}</Container> */}
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
