import React from "react";
import { useSelector } from "react-redux";
import PackageItem from "../components/packageItem";
import { MDBListGroup } from "mdbreact";
import Pagination from "../components/pagination";

const Search = () => {
  const packages = useSelector((state) => state.search.packages);
  const error = useSelector((state) => state.search.error);
  const totalPages = useSelector((state) => state.search.totalPages);
  const currentPage = useSelector((state) => state.search.currentPage);

  return error !== null ? (
    <div className="container">
      <div id="result">{error}</div>
    </div>
  ) : packages !== null ? (
    packages.length === 0 ? (
      <div className="container">
        <div>No packages found.</div>
      </div>
    ) : (
      <div className="container">
        <br />
        <MDBListGroup
          style={{
            alignItems: "center",
          }}
        >
          {packages.map((packageEntity) => (
            <PackageItem
              key={packageEntity.name + packageEntity.namespace}
              packageEntity={packageEntity}
            />
          ))}
          <br />
          <Pagination currentPage={currentPage} totalPages={totalPages} />
        </MDBListGroup>
      </div>
    )
  ) : null;
};

export default Search;
