export const FETCH_PACKAGE_DATA = "FETCH_PACKAGE_DATA";
export const FETCH_PACKAGE_DATA_SUCCESS = "FETCH_PACKAGE_DATA_SUCCESS";
export const FETCH_PACKAGE_DATA_ERROR = "FETCH_PACKAGE_DATA_ERROR";

export const fetchPackageData = (namespace_name,package_name) => {
  return (dispatch) => {
    dispatch({ type: FETCH_PACKAGE_DATA });
    const url = `${process.env.REACT_APP_REGISTRY_API_URL}/packages/${namespace_name}/${package_name}`;
    fetch(url)
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else {
            console.log("error");
          dispatch({ type: FETCH_PACKAGE_DATA_ERROR});
        }
      })
      .then((data) => {
        dispatch({
          type: FETCH_PACKAGE_DATA_SUCCESS,
          payload: {
            name: data.data.name,
            namespace: data.data.namespace,
            author: data.data.author,
            tags:data.data.tags,
            license: data.data.license,
            createdAt: data.data.createdAt,
            version_data: data.data.version_data,
            updatedAt: data.data.updatedAt,
            description: data.data.description
          },
        });
      });
  };
};