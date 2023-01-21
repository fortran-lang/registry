import { Outlet, Link } from "react-router-dom";
import "./layout.css";

const Layout = () => {
  return (
    <>
      <nav>
        <img
          src="https://fortran-lang.org/en/_static/fortran-logo-256x256.png"
          alt="Fortran-lang logo"
          width="80"
          height="80"
        ></img>
        <Link to="/help">Help</Link>
        <Link to="/account/login">Login</Link>
        <Link to="/account/register">Register</Link>
        <Link to="/search">Search</Link>
      </nav>
      <Outlet />
    </>
  );
};

export default Layout;
