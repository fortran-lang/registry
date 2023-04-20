import axios from "axios";

export const SEARCH_PACKAGE = "SEARCH_PACKAGE";
export const SEARCH_SUCCESS = "SEARCH_SUCCESS";
export const SEARCH_FAILURE = "SEARCH_FAILURE";

const sortedByMap = new Map()
  .set("Date last updated", "updatedat")
  .set("None", "");

export const searchPackage =
  (query, page, sortedBy = "") =>
  async (dispatch) => {
    if (sortedBy.length !== 0) {
      sortedBy = sortedByMap.get(sortedBy);
    }

    const url = `${
      process.env.REACT_APP_REGISTRY_API_URL
    }/packages?query=${encodeURIComponent(query)}&page=${encodeURIComponent(
      page
    )}&sorted_by=${encodeURIComponent(sortedBy)}`;

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
          currentPage: page,
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

export const SET_QUERY = "SET_QUERY";

export const setQuery = (query) => (dispatch) => {
  dispatch({
    type: SET_QUERY,
    payload: {
      query: query,
    },
  });
};

export const SET_ORDER_BY = "SET_ORDER_BY";

export const setOrderBy = (orderBy) => (dispatch, getState) => {
  dispatch({
    type: SET_ORDER_BY,
    payload: {
      orderBy: orderBy,
    },
  });
};
