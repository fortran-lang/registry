import authReducer from "./authReducer";
import accountReducer from "./accountReducer";
import dashboardReducer from "./dashboardReducer";
import packageReducer from "./packageReducer";
import userReducer from "./userReducer";
import { combineReducers } from "redux";

const rootReducer = combineReducers({
  auth: authReducer,
  dashboard: dashboardReducer,
  account: accountReducer,
  user: userReducer,
  package:packageReducer,
});

export default rootReducer;
