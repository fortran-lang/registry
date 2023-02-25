export const UPLOAD_PACKAGE = "UPLOAD_PACKAGE";
export const UPLOAD_PACKAGE_SUCCESS = "UPLOAD_PACKAGE_SUCCESS";
export const UPLOAD_PACKAGE_ERROR = "UPLOAD_PACKAGE_ERROR";

export const uploadPackage = (data) => {
  return (dispatch) => {
    dispatch({ type: UPLOAD_PACKAGE });
    const url = `${process.env.REACT_APP_REGISTRY_API_URL}/packages`;
    const form = new FormData(data);

    fetch(url, {
        method: 'POST',
        body: form,
      })
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else {
            console.log("error");
          dispatch({ type: UPLOAD_PACKAGE_ERROR});
        }
      })
      .then((data) => {
        dispatch({
          type: UPLOAD_PACKAGE_SUCCESS,
          payload: {
            message: data["message"],
          },
        });
      });
  };
};