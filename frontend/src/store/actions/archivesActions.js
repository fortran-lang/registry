export const FETCH_ARCHIVES_DATA = "FETCH_ARCHIVES_DATA";
export const FETCH_ARCHIVES_DATA_SUCCESS = "FETCH_ARCHIVES_DATA_SUCCESS";
export const FETCH_ARCHIVES_DATA_ERROR = "FETCH_ARCHIVES_DATA_ERROR";

export const fetchArchiveData = () => {
  return (dispatch) => {
    dispatch({ type: FETCH_ARCHIVES_DATA });
    const url = `${process.env.REACT_APP_REGISTRY_API_URL}/registry/archives`;
    fetch(url)
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          dispatch({ type: FETCH_ARCHIVES_DATA_ERROR});
        }
      })
      .then((data) => {
        dispatch({
          type: FETCH_ARCHIVES_DATA_SUCCESS,
          payload: {
            archives: data.archives,
            message: data.message,
          },
        });
      });
  };
};