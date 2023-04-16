import axios from "axios";

export const RESET_SUCCESS = "RESET_SUCCESS";
export const RESET_FAILURE = "RESET_FAILURE";
export const GET_USER_ACCOUNT = "GET_USER_ACCOUNT";
export const GET_USER_ACCOUNT_FAILURE = "GET_USER_ACCOUNT_FAILURE";
// export const DELETE_ACCOUNT = "DELETE_ACCOUNT";
// export const DELETE_ACCOUNT_ERROR = "DELETE_ACCOUNT_ERROR";
export const RESET_PASSWORD = "RESET_PASSWORD";
export const RESET_PASSWORD_ERROR = "RESET_PASSWORD_ERROR";


export const getUserAccount = (uuid) => async (dispatch) => {
  const formData = new FormData();
  formData.append("uuid", uuid);

  axios({
    method: "post",
    url: `${process.env.REACT_APP_REGISTRY_API_URL}/users/account`,
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  })
    .then((result) => {
      dispatch({
        type: GET_USER_ACCOUNT,
        payload: {
          email: result.data.user.email,
          dateJoined: result.data.user.createdAt.slice(0, 16),
        },
      });
    })
    .catch((error) => {
      dispatch({
        type: GET_USER_ACCOUNT_FAILURE,
        payload: error.response.message,
      });
    });
};

export const reset = (oldpassword, password, uuid) => {
  return (dispatch) => {
    let formData = new FormData();
    formData.append("oldpassword", oldpassword);
    formData.append("password", password);
    formData.append("uuid", uuid);

    axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/auth/reset-password`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
      .then((result) => {
        dispatch({ type: RESET_PASSWORD, payload: result.data.message });
      })
      .catch((error) => {
        console.log(error);
        dispatch({
          type: RESET_PASSWORD_ERROR,
          payload: error.response.data.message,
        });
      });
  };
};
