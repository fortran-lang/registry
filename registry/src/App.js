import React from "react";
import "./App.css";
import NavbarComponent from "./pages/Navbar";
import Login from "./pages/login";
import Help from "./pages/help";
import Register from "./pages/register";
import Home from "./pages/home";
import Dashboard from "./pages/dashboard";
import PackageForm from "./pages/upload";
import Account from "./pages/account";
import Search from "./pages/search";
import NoPage from "./pages/404";
import UserPage from "./pages/user";
import PackagePage from "./pages/package";
import NamespacePage from "./pages/namespace";
// import Admin from "./pages/admin";
import ForgotPassword from "./pages/forgotpassword";
import ResetPassword from "./pages/resetpassword";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.css";

function App() {
  return (
    <BrowserRouter>
      <NavbarComponent />
      <Routes>
        <Route path="/" exact element={<Home />} />
        <Route path="/account/login" element={<Login />} />
        <Route path="/account/forgot-password" element={<ForgotPassword />} />
        <Route
          path="/account/reset-password/:uuid"
          element={<ResetPassword />}
        />
        <Route path="/account/register" element={<Register />} />
        <Route path="/help" element={<Help />} />
        <Route path="/search" element={<Search />} />
        <Route path="/manage/projects" element={<Dashboard />} />
        <Route path="/manage/account" element={<Account />} />
        <Route path="/package/create" element={<PackageForm />} />
        <Route path="/users/:user" element={<UserPage />} />
        <Route
          path="/packages/:namespace_name/:package_name"
          element={<PackagePage />}
        />
        <Route path="/namespaces/:namespace" element={<NamespacePage />} />
        {/* <Route path="/admin" element={<Admin />} /> */}
        <Route path="*" element={<NoPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
