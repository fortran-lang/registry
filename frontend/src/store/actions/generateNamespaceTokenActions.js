import axios from "axios";

export const GENERATE_TOKEN_REQUEST = "GENERATE_TOKEN_REQUEST";
export const GENERATE_TOKEN_SUCCESS = "GENERATE_TOKEN_SUCCESS";
export const GENERATE_TOKEN_FAILURE = "GENERATE_TOKEN_FAILURE";

export const RESET_MESSAGE = "RESET_ERROR_MESSAGE";

export const generateToken = (data) => async (dispatch) => {
  let formData = new FormData();

  formData.append("namespace", data.namespace);

  try {
    dispatch({
      type: GENERATE_TOKEN_REQUEST,
    });

    const result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/namespaces/${data.namespace}/uploadToken`,
      data: formData,
      headers: {
        Authorization: `Bearer ${data.accessToken}`,
      },
    });

    if (result.data.code === 200) {
      dispatch({
        type: GENERATE_TOKEN_SUCCESS,
        payload: {
          message: result.data.message,
          uploadToken: result.data.uploadToken,
        },
      });
    } else {
      dispatch({
        type: GENERATE_TOKEN_FAILURE,
        payload: {
          message: result.data.message,
        },
      });
    }
  } catch (error) {
    dispatch({
      type: GENERATE_TOKEN_FAILURE,
      payload: {
        message: error.response.data.message,
      },
    });
  }
};

export const resetMessages = () => (dispatch) => {
  dispatch({
    type: RESET_MESSAGE,
  });
};
