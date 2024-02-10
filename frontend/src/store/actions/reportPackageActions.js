import axios from "axios";

export const REPORT_PACKAGE_REQUEST = "REPORT_PACKAGE_REQUEST";
export const REPORT_PACKAGE_SUCCESS = "REPORT_PACKAGE_SUCCESS";
export const REPORT_PACKAGE_FAILURE = "REPORT_PACKAGE_FAILURE";

export const RESET_ERROR_MESSAGE = "RESET_ERROR_MESSAGE";

export const reportPackage = (data, access_token) => async (dispatch) => {
  let formData = new FormData();
  formData.append("reason", data.reason);

  let package_name = data.package;
  let namespace_name = data.namespace;

  try {
    dispatch({
      type: REPORT_PACKAGE_REQUEST,
    });

    const result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/report/${namespace_name}/${package_name}`,
      data: formData,
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    });

    dispatch({
      type: REPORT_PACKAGE_SUCCESS,
      payload: {
        message: result.data.message,
        statuscode: result.data.code,
      },
    });
  } catch (error) {
    dispatch({
      type: REPORT_PACKAGE_FAILURE,
      payload: {
        message: error.response.data.message,
        statuscode: error.response.data.code,
      },
    });
  }
};

export const resetErrorMessage = () => (dispatch) => {
  dispatch({
    type: RESET_ERROR_MESSAGE,
  });
};
