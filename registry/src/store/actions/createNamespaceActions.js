import axios from "axios";

export const CREATE_NAMESPACE = "CREATE_NAMESPACE";
export const CREATE_NAMESPACE_SUCCESS = "CREATE_NAMESPACE_SUCCESS";
export const CREATE_NAMESPACE_ERROR = "CREATE_NAMESPACE_ERROR";

export const createNamespace = (data)  => async (dispatch) => {
  dispatch({
    type: CREATE_NAMESPACE,
  });

    try {
      let result = await axios({
        method: "post",
        url: `${process.env.REACT_APP_REGISTRY_API_URL}/packages`,
        data: new FormData(data),
      });

      if (result.data.code === 200) {
        dispatch({
          type: CREATE_NAMESPACE_SUCCESS,
          payload: {
            message: result.data.message,
            statuscode: result.data.code,
          },
        });
      }
    } catch (error) {
      dispatch({
        type: CREATE_NAMESPACE_ERROR,
        payload: {
          message: error.response.data.message,
          statuscode: error.response.data.code,
        },
      });
    }
  };