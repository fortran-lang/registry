import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  MDBContainer,
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarToggler,
  MDBNavbarNav,
  MDBNavbarItem,
  MDBNavbarLink,
  MDBDropdown,
  MDBDropdownToggle,
  MDBDropdownMenu,
  MDBDropdownItem,
  MDBIcon,
  MDBCollapse,
} from "mdb-react-ui-kit";
import { useDispatch, useSelector } from "react-redux";
import Image from "react-bootstrap/Image";
import { logout } from "../store/actions/authActions";
import { searchPackage, setQuery } from "../store/actions/searchActions";

const Navbar = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [showNavSecond, setShowNavSecond] = useState(false);

  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const username = useSelector((state) => state.auth.username);
  const uuid = useSelector((state) => state.auth.uuid);

  const signOut = () => {
    dispatch(logout(uuid));
  };

  return (
    <MDBNavbar expand="lg" light bgColor="light">
      <MDBContainer>
        <MDBNavbarBrand href="#">
          <Image
            src="https://fortran-lang.org/en/_static/fortran-logo-256x256.png"
            fluid
            width={60}
            height={60}
          />
        </MDBNavbarBrand>

        <MDBNavbarToggler
          aria-expanded="false"
          aria-label="Toggle navigation"
          onClick={() => setShowNavSecond(!showNavSecond)}
        >
          <MDBIcon icon="bars" fas />
        </MDBNavbarToggler>
        <MDBCollapse navbar show={showNavSecond}>
          <MDBNavbarNav className="mr-auto mb-2 mb-lg-0">
            {!isAuthenticated && (
              <MDBNavbarLink onClick={() => navigate("/account/login")}>
                Login
              </MDBNavbarLink>
            )}
            {!isAuthenticated && (
              <MDBNavbarLink onClick={() => navigate("/account/register")}>
                Register
              </MDBNavbarLink>
            )}
            {isAuthenticated && (
              <MDBNavbarItem>
                <MDBDropdown>
                  <MDBDropdownToggle tag="a" className="nav-link" role="button">
                    {username}
                  </MDBDropdownToggle>

                  <MDBDropdownMenu>
                    <MDBDropdownItem
                      className="dropdown-item"
                      onClick={() => {navigate("/package/create");window.location.reload();}}
                    >
                      Create Package
                    </MDBDropdownItem>

                    <MDBDropdownItem
                      className="dropdown-item"
                      onClick={() => {navigate("/manage/projects");window.location.reload();}}
                    >
                      Packages
                    </MDBDropdownItem>
                    <MDBDropdownItem
                      className="dropdown-item"
                      onClick={() => {navigate("/search");window.location.reload();}}
                    >
                      Search
                    </MDBDropdownItem>

                    <MDBDropdownItem
                      className="dropdown-item"
                      onClick={() => {navigate("/manage/account");window.location.reload();}}
                    >
                      Account
                    </MDBDropdownItem>

                    <MDBDropdownItem
                      className="dropdown-item"
                      onClick={signOut}
                    >
                      Logout
                    </MDBDropdownItem>
                  </MDBDropdownMenu>
                </MDBDropdown>
              </MDBNavbarItem>
            )}
          </MDBNavbarNav>
          <SearchBar />
        </MDBCollapse>
      </MDBContainer>
    </MDBNavbar>
  );
};

export default Navbar;

const SearchBar = () => {
  const query = useSelector((state) => state.search.query);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const search = () => {
    if (query.trim().length !== 0) {
      dispatch(searchPackage(query, 0));
      navigate("/search");
    }
  };

  return (
    <div className="d-flex">
      <input
        type="text"
        className="flex-fill form-control"
        placeholder="Search"
        value={query}
        onChange={(event) => dispatch(setQuery(event.target.value))}
      />
      <button className="btn btn-primary" onClick={search}>
        Search
      </button>
    </div>
  );
};
