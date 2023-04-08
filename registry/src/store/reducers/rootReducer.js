import authReducer from "./authReducer";
import accountReducer from "./accountReducer";
import dashboardReducer from "./dashboardReducer";
import packageReducer from "./packageReducer";
import userReducer from "./userReducer";
import searchReducer from "./searchReducer";
import namespaceReducer from "./namespaceReducer";
import uploadReducer from "./uploadReducer";
import resetPasswordReducer from "./resetPasswordReducer";
import createNamespaceReducer from "./createNamespaceReducer";
import adminReducer from "./adminReducer";
import { combineReducers } from "redux";
import addRemoveMaintainerReducer from "./addRemoveMaintainerReducer";

const rootReducer = combineReducers({
  auth: authReducer,
  dashboard: dashboardReducer,
  account: accountReducer,
  user: userReducer,
  search: searchReducer,
  package: packageReducer,
  namespace: namespaceReducer,
  upload: uploadReducer,
  resetpassword: resetPasswordReducer,
  addRemoveMaintainer: addRemoveMaintainerReducer,
  admin: adminReducer,
  createNamespace: createNamespaceReducer,
});

export default rootReducer;
