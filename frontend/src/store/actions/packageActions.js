import axios from "axios";
export const FETCH_PACKAGE_DATA = "FETCH_PACKAGE_DATA";
export const FETCH_PACKAGE_DATA_SUCCESS = "FETCH_PACKAGE_DATA_SUCCESS";
export const FETCH_PACKAGE_DATA_ERROR = "FETCH_PACKAGE_DATA_ERROR";
export const VERIFY_USER_ROLE = "VERIFY_USER_ROLE";
export const VERIFY_USER_ROLE_SUCCESS = "VERIFY_USER_ROLE_SUCCESS";
export const VERIFY_USER_ROLE_ERROR = "VERIFY_USER_ROLE_ERROR";

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

export const verifyUserRole =
  (namespace_name, package_name, uuid) => async (dispatch) => {
    const formData = new FormData();
    formData.append("uuid", uuid);

    dispatch({
      type: VERIFY_USER_ROLE,
    });

    try {
      let result = await axios({
        method: "post",
        url: `${process.env.REACT_APP_REGISTRY_API_URL}/packages/${namespace_name}/${package_name}/verify`,
        data: formData,
      });

      dispatch({
        type: VERIFY_USER_ROLE_SUCCESS,
        payload: {
          data: result.data,
        },
      });
    } catch (error) {
      dispatch({
        type: VERIFY_USER_ROLE_ERROR,
        payload: {
          data: error.data,
        },
      });
    }
  };
