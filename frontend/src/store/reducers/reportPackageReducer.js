import {
  REPORT_PACKAGE_REQUEST,
  REPORT_PACKAGE_SUCCESS,
  REPORT_PACKAGE_FAILURE,
  RESET_ERROR_MESSAGE,
} from "../actions/reportPackageActions";

const initialState = {
  isLoading: false,
  error: null,
  message: null,
  statuscode: 0,
};

const reportPackageReducer = (state = initialState, action) => {
  switch (action.type) {
    case REPORT_PACKAGE_REQUEST:
      return {
        ...state,
        isLoading: true,
      };
    case REPORT_PACKAGE_SUCCESS:
      return {
        ...state,
        isLoading: false,
        message: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case REPORT_PACKAGE_FAILURE:
      return {
        ...state,
        isLoading: false,
        message: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case RESET_ERROR_MESSAGE:
      return {
        ...state,
        error: null,
        message: null,
        statuscode: 0,
      };
    default:
      return state;
  }
};

export default reportPackageReducer;
