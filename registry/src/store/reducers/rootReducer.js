import authReducer from "./authReducer";
import dashboardReducer from "./dashboardReducer";
import { combineReducers } from "redux";

const rootReducer = combineReducers({
  auth: authReducer,
  dashboard: dashboardReducer,
});

export default rootReducer;
