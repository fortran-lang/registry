export const FETCH_NAMESPACE_DATA = "FETCH_NAMESPACE_DATA";
export const FETCH_NAMESPACE_DATA_SUCCESS = "FETCH_NAMESPACE_DATA_SUCCESS";
export const FETCH_NAMESPACE_DATA_ERROR = "FETCH_NAMESPACE_DATA_ERROR";

export const fetchNamespaceData = (namespace) => {
  return (dispatch) => {
    dispatch({ type: FETCH_NAMESPACE_DATA });
    const url = `${process.env.REACT_APP_REGISTRY_API_URL}/namespace/${namespace}`;
    fetch(url)
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else {
            console.log("error");
          dispatch({ type: FETCH_NAMESPACE_DATA_ERROR});
        }
      })
      .then((data) => {
        dispatch({
          type: FETCH_NAMESPACE_DATA_SUCCESS,
          payload: {
            projects: data["packages"],
            dateJoined: data["createdAt"],
          },
        });
      });
  };
};