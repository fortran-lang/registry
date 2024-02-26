import authReducer from "./authReducer";
import accountReducer from "./accountReducer";
import dashboardReducer from "./dashboardReducer";
import packageReducer from "./packageReducer";
import userReducer from "./userReducer";
import searchReducer from "./searchReducer";
import namespaceReducer from "./namespaceReducer";
import resetPasswordReducer from "./resetPasswordReducer";
import createNamespaceReducer from "./createNamespaceReducer";
import archivesReducer from "./archivesReducer";
import adminReducer from "./adminReducer";
import { combineReducers } from "redux";
import addRemoveMaintainerReducer from "./addRemoveMaintainerReducer";
import generateNamespaceTokenReducer from "./generateNamespaceTokenReducer";
import generatePackageTokenReducer from "./generatePackageTokenReducer";
import addRemoveNamespaceMaintainerReducer from "./namespaceMaintainersReducer";
import addRemoveNamespaceAdminReducer from "./namespaceAdminReducer";
import verifyEmailReducer from "./verifyEmailReducer";
import userListReducer from "./userListReducer";
import reportPackageReducer from "./reportPackageReducer";
import viewMalicousReportsReducer from "./viewMalicousReportsReducer";

const rootReducer = combineReducers({
  auth: authReducer,
  dashboard: dashboardReducer,
  account: accountReducer,
  user: userReducer,
  search: searchReducer,
  package: packageReducer,
  namespace: namespaceReducer,
  resetpassword: resetPasswordReducer,
  addRemoveMaintainer: addRemoveMaintainerReducer,
  generateNamespaceToken: generateNamespaceTokenReducer,
  generatePackageToken: generatePackageTokenReducer,
  admin: adminReducer,
  createNamespace: createNamespaceReducer,
  addRemoveNamespaceMaintainer: addRemoveNamespaceMaintainerReducer,
  addRemoveNamespaceAdmin: addRemoveNamespaceAdminReducer,
  verifyEmail: verifyEmailReducer,
  userList: userListReducer,
  archives: archivesReducer,
  reportPackage: reportPackageReducer,
  malicousReport: viewMalicousReportsReducer,
});

export default rootReducer;
