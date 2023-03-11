import axios from "axios";

export const ADD_MAINTAINER_REQUEST = "ADD_MAINTAINER_REQUEST";
export const ADD_MAINTAINER_SUCCESS = "ADD_MAINTAINER_SUCCESS";
export const ADD_MAINTAINER_FAILURE = "ADD_MAINTAINER_FAILURE";

export const RESET_MESSAGE = "RESET_ERROR_MESSAGE";

export const addMaintainer = (data, username) => async (dispatch) => {
  let formData = new FormData();
  formData.append("uuid", data.uuid);
  formData.append("username", data.username_to_be_added);
  formData.append("namespace", data.namespace);
  formData.append("package", data.package);

  try {
    dispatch({
      type: ADD_MAINTAINER_REQUEST,
    });

    const result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/${username}/maintainer`,
      data: formData,
    });

    if (result.data.code === 200) {
      dispatch({
        type: ADD_MAINTAINER_SUCCESS,
        payload: {
          message: result.data.message,
        },
      });
    } else {
      dispatch({
        type: ADD_MAINTAINER_FAILURE,
        payload: {
          message: result.data.message,
        },
      });
    }
  } catch (error) {
    dispatch({
      type: ADD_MAINTAINER_FAILURE,
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
