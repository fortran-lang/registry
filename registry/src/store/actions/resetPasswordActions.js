import axios from "axios";

export const RESET_REQUEST = "RESET_REQUEST";
export const RESET_PASSWORD = "RESET_PASSWORD";

export const RESET_REQUEST_SUCCESS = "RESET_REQUEST_SUCCESS";
export const RESET_REQUEST_FAILURE = "RESET_REQUEST_FAILURE";
export const RESET_SUCCESS = "RESET_SUCCESS";
export const RESET_FAILURE = "RESET_FAILURE";

export const forgot = (email) => async (dispatch) => {
  // Make an api call to request reset password
  let formData = new FormData();

  formData.append("email", email);

  try {
    let result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/auth/forgot-password`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (result.data.code === 200) {
      dispatch({
        type: RESET_REQUEST_SUCCESS,
        payload: {
          statuscode: result.data.code,
          message: result.data.message,
        },
      });
    } else {
      dispatch({
        type: RESET_REQUEST_FAILURE,
        payload: {
            statuscode: result.data.code,
            message: result.data.message,
        },
      });
    }
  } catch (error) {
    //on failure
    console.log(error);
    dispatch({
        type: RESET_REQUEST_FAILURE,
        payload: {
            statuscode: error.response.data.code,
            message: error.response.data.message,
        },
    });
  }
};

export const reset = (password,uuid) => async (dispatch) => {
    // Make an api call to reset password
    let formData = new FormData();
  
    formData.append("password", password);
    formData.append("uuid", uuid);
  
    try {
      let result = await axios({
        method: "post",
        url: `${process.env.REACT_APP_REGISTRY_API_URL}/auth/reset-password`,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      if (result.data.code === 200) {
        dispatch({
          type: RESET_SUCCESS,
          payload: {
            statuscode: result.data.code,
            message: result.data.message,
          },
        });
      } else {
        dispatch({
          type: RESET_FAILURE,
          payload: {
              statuscode: result.data.code,
              message: result.data.message,
          },
        });
      }
    } catch (error) {
      //on failure
      dispatch({
          type: RESET_REQUEST_FAILURE,
          payload: {
            statuscode: error.response.data.code,
            message: error.response.data.message,
          },
      });
    }
  };
