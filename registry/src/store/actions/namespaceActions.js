import axios from "axios";

export const FETCH_NAMESPACE_DATA = "FETCH_NAMESPACE_DATA";
export const FETCH_NAMESPACE_DATA_SUCCESS = "FETCH_NAMESPACE_DATA_SUCCESS";
export const FETCH_NAMESPACE_DATA_ERROR = "FETCH_NAMESPACE_DATA_ERROR";

export const fetchNamespaceData = (namespace) => {
  return async (dispatch) => {
    dispatch({ type: FETCH_NAMESPACE_DATA });
    const url = `${process.env.REACT_APP_REGISTRY_API_URL}/namespace/${namespace}`;

    try {
      const result = await axios({
        method: "get",
        url: url,
      });

      dispatch({
        type: FETCH_NAMESPACE_DATA_SUCCESS,
        payload: {
          projects: result.data["packages"],
          dateJoined: result.data["createdAt"],
        },
      });
    } catch (error) {
      dispatch({ type: FETCH_NAMESPACE_DATA_ERROR });
    }
  };
};
