import axios from "axios";
export const FETCH_PACKAGE_DATA = "FETCH_PACKAGE_DATA";
export const FETCH_PACKAGE_DATA_SUCCESS = "FETCH_PACKAGE_DATA_SUCCESS";
export const FETCH_PACKAGE_DATA_ERROR = "FETCH_PACKAGE_DATA_ERROR";

export const fetchPackageData =
  (namespace_name, package_name) => async (dispatch) => {
    dispatch({
      type: FETCH_PACKAGE_DATA,
    });
    try {
      let result = await axios({
        method: "get",
        url: `${process.env.REACT_APP_REGISTRY_API_URL}/packages/${namespace_name}/${package_name}`,
      });

      if (result.data.code === 200) {
        dispatch({
          type: FETCH_PACKAGE_DATA_SUCCESS,
          payload: {
            statuscode: result.data.code,
            data: result.data.data,
          },
        });
        console.log(result.data.data);
      }
    } catch (error) {
      dispatch({
        type: FETCH_PACKAGE_DATA_ERROR,
        payload: {
          statuscode: error.data.code,
          data: error.data.data,
        },
      });
    }
  };
