export const FETCH_USER_DATA = "FETCH_USER_DATA";
export const FETCH_USER_DATA_SUCCESS = "FETCH_USER_DATA_SUCCESS";
export const FETCH_USER_DATA_ERROR = "FETCH_USER_DATA_ERROR";

export const fetchUserData = (user) => {
  return (dispatch) => {
    dispatch({ type: FETCH_USER_DATA });
    const url = `${process.env.REACT_APP_REGISTRY_API_URL}/users/${user}`;
    fetch(url)
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else {
            console.log("error");
          dispatch({ type: FETCH_USER_DATA_ERROR});
        }
      })
      .then((data) => {
        dispatch({
          type: FETCH_USER_DATA_SUCCESS,
          payload: {
            email: data["user"].email,
            dateJoined: data["user"].createdAt,
            projects: data["user"].packages,
          },
        });
      });
  };
};