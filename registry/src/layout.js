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

{
  /* <nav class="navbar navbar-default">
<div class="container-fluid">
  <div class="navbar-header">
    <a class="navbar-brand" href="#">WebSiteName</a>
  </div>
  <ul class="nav navbar-nav">
    <li class="active"><a href="#">Home</a></li>
    <li><a href="#">Page 1</a></li>
    <li><a href="#">Page 2</a></li>
    <li><a href="#">Page 3</a></li>
  </ul>
</div>
</nav> */
}
