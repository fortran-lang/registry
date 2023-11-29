import axios from "axios";

export const REQUEST_PACKAGES = "REQUEST_PACKAGES";
export const REQUEST_PACKAGES_SUCCESS = "REQUEST_PACKAGES_SUCCESS";
export const REQUEST_PACKAGES_FAILURE = "REQUEST_PACKAGES_FAILURE";

export const fetchPackages = (username) => async (dispatch) => {
  dispatch({
    type: REQUEST_PACKAGES,
  });

  try {
    let result = await axios({
      method: "get",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/users/${username}`,
    });

    if (result.data.code === 200) {
      dispatch({
        type: REQUEST_PACKAGES_SUCCESS,
        payload: {
          packages: result.data.packages,
          namespaces: result.data.namespaces,
        },
      });
    } else {
      dispatch({
        type: REQUEST_PACKAGES_FAILURE,
      });
    }
  } catch (error) {
    dispatch({
      type: REQUEST_PACKAGES_FAILURE,
    });
  }
};
