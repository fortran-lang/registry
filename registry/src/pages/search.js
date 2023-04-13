import React, { useEffect } from "react";
import Spinner from "react-bootstrap/Spinner";
import { useSelector, useDispatch } from "react-redux";
import PackageItem from "../components/packageItem";
import { MDBListGroup } from "mdbreact";
import Pagination from "../components/pagination";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import { searchPackage, setOrderBy } from "../store/actions/searchActions";

const Search = () => {
  const dispatch = useDispatch();
  const packages = useSelector((state) => state.search.packages);
  const error = useSelector((state) => state.search.error);
  const totalPages = useSelector((state) => state.search.totalPages);
  const currentPage = useSelector((state) => state.search.currentPage);
  const orderBy = useSelector((state) => state.search.orderBy);
  const query = useSelector((state) => state.search.query);
  const isLoading = useSelector((state) => state.search.isLoading);

  const dropdownOptions = ["None", "Date last updated"];

  const onDropDownSelect = (option) => {
    dispatch(setOrderBy(option));
    dispatch(searchPackage(query, 0, option));
  };

  if (isLoading) {
    return (
      <div class="d-flex justify-content-center">
        <Spinner
          className="spinner-border m-5"
          animation="border"
          role="status"
        >
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  if (error !== null) {
    return (
      <div className="container">
        <div id="result">{error}</div>
      </div>
    );
  }

  if (packages !== null) {
    if (packages.length === 0) {
      return (
        <div
          className="container alert alert-secondary"
          style={{
            marginTop: "1em",
          }}
          role="alert"
        >
          No package found.
        </div>
      );
    } else {
      return (
        <div className="container">
          <br />
          <div className="d-flex justify-content-end" id="dropdown-orderby">
            <label>Order by</label>
            <DropdownSortBy
              orderBy={orderBy}
              dropdownOptions={dropdownOptions}
              onDropDownSelect={onDropDownSelect}
            />
          </div>
          <ListView
            packages={packages}
            currentPage={currentPage}
            totalPages={totalPages}
          />
        </div>
      );
    }
  }
};

export default Search;

const ListView = ({ packages, currentPage, totalPages }) => {
  return (
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
  );
};

const DropdownSortBy = ({ orderBy, dropdownOptions, onDropDownSelect }) => {
  return (
    <DropdownButton title={orderBy}>
      {dropdownOptions.map((option) => (
        <Dropdown.Item key={option} onClick={() => onDropDownSelect(option)}>
          {option}
        </Dropdown.Item>
      ))}
    </DropdownButton>
  );
};
