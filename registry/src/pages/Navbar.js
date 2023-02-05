import React from "react";
import { Outlet, Link } from "react-router-dom";
import {
  Nav,
  NavLink,
  Bars,
  NavMenu,
  NavBtn,
  NavBtnLink,
  NavIcon,
} from "./NavbarElements";
import { useDispatch, useSelector } from "react-redux";
import Image from "react-bootstrap/Image";
import { logout } from "../store/actions/authActions";

const Navbar = () => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const uuid = useSelector((state) => state.auth.uuid);
  const dispatch = useDispatch();

  const signOut = () => {
    dispatch(logout(uuid));
  };

  return (
    <>
      <Nav>
        <Bars />
        <Image
          src="https://fortran-lang.org/en/_static/fortran-logo-256x256.png"
          fluid
          width={70}
          height={70}
        />
        <NavMenu>
          <NavLink to="/help" activeStyle>
            Help
          </NavLink>
          {!isAuthenticated && (
            <NavLink to="/account/login" activeStyle>
              Login
            </NavLink>
          )}
          {isAuthenticated && (
            <NavLink to="/package/create" activeStyle>
              Create
            </NavLink>
          )}
          {isAuthenticated && (
            <NavLink to="/manage/projects" activeStyle>
              Packages
            </NavLink>
          )}
          {isAuthenticated && (
            <NavLink to="/manage/account" activeStyle>
              Account
            </NavLink>
          )}
          {!isAuthenticated && (
            <NavLink to="/account/register" activeStyle>
              Register
            </NavLink>
          )}
          <NavLink to="/search" activeStyle>
            Search
          </NavLink>
          {isAuthenticated && (
            <NavLink onClick={signOut} activeStyle>
              Logout
            </NavLink>
          )}
          {/* Second Nav */}
          {/* <NavBtnLink to='/sign-in'>Sign In</NavBtnLink> */}
        </NavMenu>
        {/* <NavBtn>
          <NavBtnLink to="/signin">Sign In</NavBtnLink>
        </NavBtn> */}
        <Outlet />
      </Nav>
    </>
  );
};

export default Navbar;
