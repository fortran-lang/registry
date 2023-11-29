import axios from "axios";

export const VERIFY_REQUEST = "VERIFY_REQUEST";

export const VERIFY_REQUEST_SUCCESS = "VERIFY_REQUEST_SUCCESS";
export const VERIFY_REQUEST_FAILURE = "VERIFY_REQUEST_FAILURE";

export const verify = (uuid) => async (dispatch) => {
  // Make an api call to request to verify email
  dispatch({
    type: VERIFY_REQUEST,
  });
  let formData = new FormData();

  formData.append("uuid", uuid);

  try {
    let result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/auth/verify-email`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (result.data.code === 200) {
      dispatch({
        type: VERIFY_REQUEST_SUCCESS,
        payload: {
          statuscode: result.data.code,
          message: result.data.message,
        },
      });
    } else {
      dispatch({
        type: VERIFY_REQUEST_FAILURE,
        payload: {
          statuscode: result.data.code,
          message: result.data.message,
        },
      });
    }
  } catch (error) {
    //on failure
    // console.log(error);
    dispatch({
      type: VERIFY_REQUEST_FAILURE,
      payload: {
        statuscode: error.response.data.code,
        message: error.response.data.message,
      },
    });
  }
};
