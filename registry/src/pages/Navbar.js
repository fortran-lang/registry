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
import Image from "react-bootstrap/Image";

const Navbar = () => {
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
          <NavLink to="/account/login" activeStyle>
            Login
          </NavLink>
          <NavLink to="/account/register" activeStyle>
            Register
          </NavLink>
          <NavLink to="/search" activeStyle>
            Search
          </NavLink>
          <NavLink to="/blogs" activeStyle>
            Blogs
          </NavLink>
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
