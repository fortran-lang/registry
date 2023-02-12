import authReducer from "./authReducer";
import accountReducer from "./accountReducer";
import dashboardReducer from "./dashboardReducer";
import userReducer from "./userReducer";
import { combineReducers } from "redux";

const rootReducer = combineReducers({
  auth: authReducer,
  dashboard: dashboardReducer,
  account: accountReducer,
  user: userReducer,
});

export default rootReducer;
