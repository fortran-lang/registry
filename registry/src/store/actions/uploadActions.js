import axios from "axios";

export const UPLOAD_PACKAGE = "UPLOAD_PACKAGE";
export const UPLOAD_PACKAGE_SUCCESS = "UPLOAD_PACKAGE_SUCCESS";
export const UPLOAD_PACKAGE_ERROR = "UPLOAD_PACKAGE_ERROR";

export const uploadPackage = (data)  => async (dispatch) => {
  dispatch({
    type: UPLOAD_PACKAGE,
  });

    try {
      let result = await axios({
        method: "post",
        url: `${process.env.REACT_APP_REGISTRY_API_URL}/packages`,
        data: new FormData(data),
      });

      if (result.data.code === 200) {
        console.log(result.data.message);
        dispatch({
          type: UPLOAD_PACKAGE_SUCCESS,
          payload: {
            message: result.message,
          },
        });
      }
    } catch (error) {
      console.log(error.response.data.message);
      dispatch({
        type: UPLOAD_PACKAGE_ERROR,
        payload: {
          message: error.response.data.message,
        },
      });
    }
  };