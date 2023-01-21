import React from "react";
import { Navigate } from "react-router-dom";
import { useCookies } from 'react-cookie';


const Dashboard = () => {
  const [cookies, setCookie] = useCookies(['uuid']);
  if (!cookies.uuid) {
    return <Navigate to="/account/login" replace={true} />;
  }
  return <p>Dashboard</p>;
};

export default Dashboard;
