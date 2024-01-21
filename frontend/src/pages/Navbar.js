import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import Image from "react-bootstrap/Image";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import { logout } from "../store/actions/authActions";
import { searchPackage, setQuery } from "../store/actions/searchActions";
import { adminAuth } from "../store/actions/adminActions";

const NavbarComponent = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const location = useLocation();
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const isAdmin = useSelector((state) => state.admin.isAdmin);
  const username = useSelector((state) => state.auth.username);
  const accessToken = useSelector((state) => state.auth.accessToken);

  useEffect(() => {
    dispatch(adminAuth(accessToken));
  }, [isAuthenticated, accessToken]);

  const signOut = () => {
    dispatch(logout(accessToken));
  };

  return (
    <Navbar bg="light" expand="md">
      <Container id="navbar-container">
        <Navbar.Brand
          onClick={() => navigate("/")}
          style={{
            cursor: "pointer",
          }}
        >
          <Image
            src="https://fortran-lang.org/en/_static/fortran-logo-256x256.png"
            fluid
            width={60}
            height={60}
            alt="Fortran-logo"
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse>
          {location.pathname !== "/" ? (
            <div id="search-bar">
              <SearchBar />
            </div>
          ) : null}
          <Nav className="ml-auto">
            {!isAuthenticated && (
              <>
                <Nav.Link onClick={() => navigate("/archives")}>
                  Archives
                </Nav.Link>
                <Nav.Link onClick={() => navigate("/help")}>Help</Nav.Link>
                <Nav.Link onClick={() => navigate("/account/login")}>
                  Login
                </Nav.Link>
                <Nav.Link onClick={() => navigate("/account/register")}>
                  Register
                </Nav.Link>
              </>
            )}
          </Nav>

          {isAuthenticated && (
            <Nav className="ml-auto">
              <NavDropdown title={username} className="d-flex">
                <NavDropdown.Item
                  onClick={() => {
                    navigate("/namespace/create");
                    window.location.reload();
                  }}
                >
                  Create Namespace
                </NavDropdown.Item>

                <NavDropdown.Item
                  onClick={() => {
                    navigate("/manage/projects");
                    window.location.reload();
                  }}
                >
                  Dashboard
                </NavDropdown.Item>

                <NavDropdown.Item
                  onClick={() => {
                    navigate("/manage/account");
                    window.location.reload();
                  }}
                >
                  Account
                </NavDropdown.Item>
                {isAdmin && (
                  <NavDropdown.Item
                    onClick={() => {
                      navigate("/admin");
                      window.location.reload();
                    }}
                  >
                    Admin
                  </NavDropdown.Item>
                )}

                <NavDropdown.Item onClick={signOut}>Logout</NavDropdown.Item>
                <NavDropdown.Item onClick={() => navigate("/help")}>
                  Help
                </NavDropdown.Item>
                <NavDropdown.Item onClick={() => navigate("/archives")}>
                  Archives
                </NavDropdown.Item>
              </NavDropdown>
            </Nav>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavbarComponent;

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

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      search();
    }
  };

  return (
    <div className="d-flex" tabIndex={0} onKeyDown={handleKeyDown}>
      <input
        type="text"
        className="flex-fill form-control"
        placeholder="Search"
        value={query}
        onChange={(event) => dispatch(setQuery(event.target.value))}
        style={{
          borderRadius: "50px",
        }}
      />
      <button className="btn btn-primary" onClick={search}>
        Search
      </button>
    </div>
  );
};
