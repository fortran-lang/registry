import axios from "axios";

export const FETCH_USERS_LIST = "FETCH_USERS_LIST";
export const FETCH_USERS_LIST_SUCCESS = "FETCH_USERS_LIST_SUCCESS";
export const FETCH_USERS_LIST_ERROR = "FETCH_USERS_LIST_ERROR";

export const fetchUserListData = ({
  namespaceAdmins = false,
  namespaceMaintainers = false,
  packageMaintainers = false,
  namespace,
  packageName,
  uuid,
}) => {
  return async (dispatch) => {
    dispatch({ type: FETCH_USERS_LIST });
    let url;
    let formData = new FormData();
    formData.append("uuid", uuid);

    if (namespaceAdmins) {
      url = `${process.env.REACT_APP_REGISTRY_API_URL}/namespaces/${namespace}/admins`;
    } else if (namespaceMaintainers) {
      url = `${process.env.REACT_APP_REGISTRY_API_URL}/namespaces/${namespace}/maintainers`;
    } else if (packageMaintainers) {
      url = `${process.env.REACT_APP_REGISTRY_API_URL}/packages/${namespace}/${packageName}/maintainers`;
    }

    try {
      const result = await axios({
        method: "post",
        url: url,
        data: formData,
      });

      dispatch({
        type: FETCH_USERS_LIST_SUCCESS,
        payload: {
          users: result.data.users,
        },
      });
    } catch (error) {
      console.log(error);
      dispatch({
        type: FETCH_USERS_LIST_ERROR,
        payload: {
          statuscode: error.response.data.code,
          message: error.response.data.message,
        },
      });
    }
  };
};
