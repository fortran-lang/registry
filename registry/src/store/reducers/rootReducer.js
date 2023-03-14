import authReducer from "./authReducer";
import accountReducer from "./accountReducer";
import dashboardReducer from "./dashboardReducer";
import packageReducer from "./packageReducer";
import userReducer from "./userReducer";
import searchReducer from "./searchReducer";
import namespaceReducer from "./namespaceReducer";
import uploadReducer from "./uploadReducer";
import resetPasswordReducer from "./resetPasswordReducer";
import { combineReducers } from "redux";
import addMaintainerReducer from "./addMaintainerReducer";

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
  addMaintainer: addMaintainerReducer,
});

export default rootReducer;
