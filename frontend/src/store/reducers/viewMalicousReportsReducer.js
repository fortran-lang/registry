import {
  FETCH_MALICIOUS_REPORTS,
  FETCH_MALICIOUS_REPORTS_SUCCESS,
  FETCH_MALICIOUS_REPORTS_ERROR,
  RESET_DATA,
} from "../actions/viewMalicousReportActions";

const initialState = {
  reports: [],
  isLoading: false,
  error: null,
};

const viewMalicousReportsReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_MALICIOUS_REPORTS:
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case FETCH_MALICIOUS_REPORTS_SUCCESS:
      return {
        ...state,
        reports: action.payload.reports,
        isLoading: false,
        error: null,
      };
    case FETCH_MALICIOUS_REPORTS_ERROR:
      return {
        ...state,
        isLoading: false,
        error: action.payload.message,
      };
    case RESET_DATA:
      return {
        reports: [],
        isLoading: false,
        error: null,
      };
    default:
      return state;
  }
};

export default viewMalicousReportsReducer;
