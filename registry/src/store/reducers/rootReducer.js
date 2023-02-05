import authReducer from "./authReducer";
import accountReducer from "./accountReducer";
import dashboardReducer from "./dashboardReducer";
import { combineReducers } from "redux";

const rootReducer = combineReducers({
  auth: authReducer,
  dashboard: dashboardReducer,
  account: accountReducer,
});

export default rootReducer;
