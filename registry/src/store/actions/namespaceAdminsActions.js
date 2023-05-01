import axios from "axios";

export const ADD_NAMESPACE_ADMIN_REQUEST = "ADD_NAMESPACE_ADMIN_REQUEST";
export const ADD_NAMESPACE_ADMIN_SUCCESS = "ADD_NAMESPACE_ADMIN_SUCCESS";
export const ADD_NAMESPACE_ADMIN_FAILURE = "ADD_NAMESPACE_ADMIN_FAILURE";

export const REMOVE_NAMESPACE_ADMIN_REQUEST = "REMOVE_NAMESPACE_ADMIN_REQUEST";
export const REMOVE_NAMESPACE_ADMIN_SUCCESS = "REMOVE_NAMESPACE_ADMIN_SUCCESS";
export const REMOVE_NAMESPACE_ADMIN_FAILURE = "REMOVE_NAMESPACE_ADMIN_FAILURE";

export const RESET_ERROR_MESSAGE = "RESET_ERROR_MESSAGE";

export const addNamespaceAdmin = (data, username) => async (dispatch) => {
  let formData = new FormData();
  formData.append("uuid", data.uuid);
  formData.append("username", data.username_to_be_added);
  formData.append("namespace", data.namespace);

  try {
    dispatch({
      type: ADD_NAMESPACE_ADMIN_REQUEST,
    });

    const result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/${username}/namespace/admin`,
      data: formData,
    });

    if (result.data.code === 200) {
      dispatch({
        type: ADD_NAMESPACE_ADMIN_SUCCESS,
        payload: {
          message: result.data.message,
        },
      });
    } else {
      dispatch({
        type: ADD_NAMESPACE_ADMIN_FAILURE,
        payload: {
          message: result.data.message,
        },
      });
    }
  } catch (error) {
    dispatch({
      type: ADD_NAMESPACE_ADMIN_FAILURE,
      payload: {
        message: error.response.data.message,
      },
    });
  }
};

export const removeNamespaceAdmin = (data, username) => async (dispatch) => {
  let formData = new FormData();
  formData.append("uuid", data.uuid);
  formData.append("username", data.username_to_be_removed);
  formData.append("namespace", data.namespace);

  try {
    dispatch({
      type: REMOVE_NAMESPACE_ADMIN_REQUEST,
    });

    const result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/${username}/namespace/admin/remove`,
      data: formData,
    });

    if (result.data.code === 200) {
      dispatch({
        type: REMOVE_NAMESPACE_ADMIN_SUCCESS,
        payload: {
          message: result.data.message,
        },
      });
    } else {
      dispatch({
        type: REMOVE_NAMESPACE_ADMIN_FAILURE,
        payload: {
          message: result.data.message,
        },
      });
    }
  } catch (error) {
    dispatch({
      type: REMOVE_NAMESPACE_ADMIN_FAILURE,
      payload: {
        message: error.response.data.message,
      },
    });
  }
};

export const resetMessages = () => (dispatch) => {
  dispatch({
    type: RESET_ERROR_MESSAGE,
  });
};
