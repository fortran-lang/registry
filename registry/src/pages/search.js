import React, { useState } from "react";
import { useSelector } from "react-redux";
import PackageItem from "../components/packageItem";
import { MDBListGroup } from "mdbreact";

const Search = () => {
  const packages = useSelector((state) => state.search.packages);
  const error = useSelector((state) => state.search.error);
  const totalPages = useSelector((state) => state.search.totalPages);

  console.log(totalPages);

  return error !== null ? (
    <div className="container">
      <div id="result">{error}</div>
    </div>
  ) : packages !== null ? (
    packages.length === 0 ? (
      <div className="container">
        <div id="result">No packages found.</div>
      </div>
    ) : (
      <div className="container">
        <br />
        <MDBListGroup
          id="result"
          style={{
            alignItems: "center",
          }}
        >
          {packages.map((packageEntity) => PackageItem(packageEntity))}
        </MDBListGroup>
      </div>
    )
  ) : null;
};

export default Search;
