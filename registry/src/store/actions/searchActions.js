import axios from "axios";

export const SEARCH_PACKAGE = "SEARCH_PACKAGE";
export const SEARCH_SUCCESS = "SEARCH_SUCCESS";
export const SEARCH_FAILURE = "SEARCH_FAILURE";

export const searchPackage = (query) => async (dispatch) => {
  const url = `${
    process.env.REACT_APP_REGISTRY_API_URL
  }/packages?query=${encodeURIComponent(query)}`;

  dispatch({
    type: SEARCH_PACKAGE,
  });

  try {
    let result = await axios({
      method: "get",
      url: url,
    });

    dispatch({
      type: SEARCH_SUCCESS,
      payload: {
        packages: result.data["packages"],
        totalPages: result.data["total_pages"],
      },
    });
  } catch (error) {
    dispatch({
      type: SEARCH_FAILURE,
      payload: {
        error: error.response.data.message,
      },
    });
  }
};
