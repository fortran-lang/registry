import axios from 'axios';

export const MARK_PACKAGE_DEPRECATED = "MARK_PACKAGE_DEPRECATED";
export const MARK_PACKAGE_DEPRECATED_SUCCESS = "MARK_PACKAGE_DEPRECATED_SUCCESS";
export const MARK_PACKAGE_DEPRECATED_ERROR = "MARK_PACKAGE_DEPRECATED_ERROR";

export const DELETE_USER_SUCCESS = "DELETE_USER_SUCCESS";
export const DELETE_USER_ERROR = "DELETE_USER_ERROR";

export const DELETE_NAMESPACE_SUCCESS = "DELETE_NAMESPACE_SUCCESS";
export const DELETE_NAMESPACE_ERROR = "DELETE_NAMESPACE_ERROR";

export const DELETE_RELEASE_SUCCESS = "DELETE_RELEASE_SUCCESS";
export const DELETE_RELEASE_ERROR = "DELETE_RELEASE_ERROR";

export const ADMIN_AUTH_ERROR = "ADMIN_AUTH_ERROR";
export const ADMIN_AUTH_SUCCESS = "ADMIN_AUTH_SUCCESS";
export const DELETE_PACKAGE_SUCCESS = "DELETE_PACKAGE_SUCCESS";
export const DELETE_PACKAGE_ERROR = "DELETE_PACKAGE_ERROR";


export const adminAuth = (uuid) => async (dispatch) => {
  // Make an api call to authenticate admin
  let formData = new FormData();
  formData.append("uuid", uuid);

  try {
    let result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/users/admin`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (result.data.code === 200) {
      dispatch({
        type: ADMIN_AUTH_SUCCESS,
        payload: {
          statuscode: result.data.code,
          message: result.data.message,
        },
      });
    } else {
      dispatch({
        type: ADMIN_AUTH_ERROR,
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
        type: ADMIN_AUTH_ERROR,
        payload: {
            statuscode: error.response.data.code,
            message: error.response.data.message,
        },
    });
  }
};


export const deleteUser = (username,uuid) => async (dispatch) => {
  // Make an api call to request reset password
  let formData = new FormData();

  formData.append("uuid", uuid);
  formData.append("username", username);

  try {
    let result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/users/delete`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (result.data.code === 200) {
      dispatch({
        type: DELETE_USER_SUCCESS,
        payload: {
          statuscode: result.data.code,
          message: result.data.message,
        },
      });
    } else {
      dispatch({
        type: DELETE_USER_ERROR,
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
        type: DELETE_USER_ERROR,
        payload: {
            statuscode: error.response.data.code,
            message: error.response.data.message,
        },
    });
  }
};


export const deleteNamespace = (namespace,uuid) => async (dispatch) => {
  // Make an api call to request reset password
  let formData = new FormData();

  formData.append("uuid", uuid);

  try {
    let result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/packages/${namespace}/delete`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (result.data.code === 200) {
      dispatch({
        type: DELETE_NAMESPACE_SUCCESS,
        payload: {
          statuscode: result.data.code,
          message: result.data.message,
        },
      });
    } else {
      dispatch({
        type: DELETE_NAMESPACE_ERROR,
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
        type: DELETE_NAMESPACE_ERROR,
        payload: {
            statuscode: error.response.data.code,
            message: error.response.data.message,
        },
    });
  }
};


export const deletePackage = (namespace,package,uuid) => async (dispatch) => {
  // Make an api call to request reset password
  let formData = new FormData();

  formData.append("uuid", uuid);

  try {
    let result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/packages/${namespace}/delete`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (result.data.code === 200) {
      dispatch({
        type: DELETE_PACKAGE_SUCCESS,
        payload: {
          statuscode: result.data.code,
          message: result.data.message,
        },
      });
    } else {
      dispatch({
        type: DELETE_PACKAGE_ERROR,
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
        type: DELETE_PACKAGE_ERROR,
        payload: {
            statuscode: error.response.data.code,
            message: error.response.data.message,
        },
    });
  }
};

export const deleteRelease = (release,uuid) => async (dispatch) => {
    // Make an api call to request reset password
    let formData = new FormData();
  
    formData.append("uuid", uuid);
  
    try {
      let result = await axios({
        method: "post",
        url: `${process.env.REACT_APP_REGISTRY_API_URL}/packages/${namespace}/delete`,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      if (result.data.code === 200) {
        dispatch({
          type: DELETE_PACKAGE_SUCCESS,
          payload: {
            statuscode: result.data.code,
            message: result.data.message,
          },
        });
      } else {
        dispatch({
          type: DELETE_PACKAGE_ERROR,
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
          type: DELETE_PACKAGE_ERROR,
          payload: {
              statuscode: error.response.data.code,
              message: error.response.data.message,
          },
      });
    }
  };