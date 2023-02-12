import React, { useState } from "react";
import { Outlet, Link } from "react-router-dom";
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

const Navbar = () => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const username = useSelector((state) => state.auth.username);
  const uuid = useSelector((state) => state.auth.uuid);
  const [showNavSecond, setShowNavSecond] = useState(false);
  const dispatch = useDispatch();

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
              <MDBNavbarLink href="/account/login">Login</MDBNavbarLink>
            )}
            {!isAuthenticated && (
              <MDBNavbarLink href="/account/register">Register</MDBNavbarLink>
            )}
            {isAuthenticated && (
              <MDBNavbarItem>
                <MDBDropdown>
                  <MDBDropdownToggle tag="a" className="nav-link" role="button">
                    {username}
                  </MDBDropdownToggle>

                  <MDBDropdownMenu>
                    <MDBDropdownItem link="/package/create">
                      Create Package
                    </MDBDropdownItem>
                    <MDBDropdownItem link="/manage/projects">
                      Packages
                    </MDBDropdownItem>
                    <MDBDropdownItem link="/manage/account">
                      Account
                    </MDBDropdownItem>
                    <MDBDropdownItem link onClick={signOut}>
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

  function SearchBar() {
    return (
      <div className="d-flex">
        <input
          type="text"
          className="flex-fill form-control"
          placeholder="Search"
        />
        <button className="btn btn-primary">Search</button>
      </div>
    );
  }
};

export default Navbar;
