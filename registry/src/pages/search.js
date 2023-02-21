import React from "react";
import { useSelector, useDispatch } from "react-redux";
import PackageItem from "../components/packageItem";
import { MDBListGroup } from "mdbreact";
import Pagination from "../components/pagination";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import { searchPackage, setOrderBy } from "../store/actions/searchActions";

const Search = () => {
  const packages = useSelector((state) => state.search.packages);
  const error = useSelector((state) => state.search.error);
  const totalPages = useSelector((state) => state.search.totalPages);
  const currentPage = useSelector((state) => state.search.currentPage);
  const orderBy = useSelector((state) => state.search.orderBy);
  const query = useSelector((state) => state.search.query);

  const dropdownOptions = ["None", "Date last updated"];

  const dispatch = useDispatch();

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
        <div className="d-flex justify-content-end" id="dropdown-orderby">
          <label>Order by</label>
          <DropdownButton title={orderBy}>
            {dropdownOptions.map((option) => (
              <Dropdown.Item
                key={option}
                onClick={() => {
                  dispatch(setOrderBy(option));
                  dispatch(searchPackage(query, 0, option));
                }}
              >
                {option}
              </Dropdown.Item>
            ))}
          </DropdownButton>
        </div>
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
