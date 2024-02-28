import axios from "axios";

export const FETCH_MALICIOUS_REPORTS = "FETCH_MALICIOUS_REPORTS";
export const FETCH_MALICIOUS_REPORTS_SUCCESS =
  "FETCH_MALICIOUS_REPORTS_SUCCESS";
export const FETCH_MALICIOUS_REPORTS_ERROR = "FETCH_MALICIOUS_REPORTS_ERROR";
export const RESET_DATA = "RESET_DATA";

export const fetchMalicousReports = (accessToken) => {
  return async (dispatch) => {
    dispatch({ type: FETCH_MALICIOUS_REPORTS });
    try {
      const result = await axios({
        method: "get",
        url: `${process.env.REACT_APP_REGISTRY_API_URL}/report/view`,
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      dispatch({
        type: FETCH_MALICIOUS_REPORTS_SUCCESS,
        payload: {
          reports: result.data.reports,
        },
      });
    } catch (error) {
      dispatch({
        type: FETCH_MALICIOUS_REPORTS_ERROR,
        payload: {
          statuscode: error.response.data.code,
          message: error.response.data.message,
        },
      });
    }
  };
};

export const resetData = () => (dispatch) => {
  dispatch({
    type: RESET_DATA,
  });
};
