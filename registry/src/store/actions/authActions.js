import axios from "axios";

export const LOGIN_SUCCESS = "LOGIN_SUCCESS";
export const LOGIN_FAILURE = "LOGIN_FAILURE";

export const login = (email, password) => async (dispatch) => {
  // Make an api call to login
  let formData = new FormData();

  formData.append("email", email);
  formData.append("password", password);

  try {
    let result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/auth/login`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    if (result.data.code === 200) {
      dispatch({
        type: LOGIN_SUCCESS,
        payload: {
          uuid: result.data.uuid,
        },
      });
    } else {
      dispatch({
        type: LOGIN_FAILURE,
        payload: {
          error: result.data.message,
        },
      });
    }
  } catch (error) {
    //on failure
    dispatch({
      type: LOGIN_FAILURE,
      payload: {
        error: error,
      },
    });
  }
};

export const SIGNUP_SUCCESS = "SIGNUP_SUCCESS";
export const SIGNUP_FAILURE = "SIGNUP_FAILURE";

export const signup = (name, email, password) => async (dispatch) => {
  let formData = new FormData();

  formData.append("name", name);
  formData.append("email", email);
  formData.append("password", password);

  console.log("Signup Called");
  // Make the api call to register.
  try {
    let result = await axios({
      method: "post",
      url: `${process.env.REACT_APP_REGISTRY_API_URL}/auth/signup`,
      data: formData,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    console.log(result);

    if (result.data.code === 200) {
      dispatch({
        type: SIGNUP_SUCCESS,
        payload: {
          uuid: result.data.uuid,
        },
      });
    } else {
      dispatch({
        type: SIGNUP_FAILURE,
        payload: {
          error: result.data.message,
        },
      });
    }
  } catch (error) {
    //on failure
    dispatch({
      type: SIGNUP_FAILURE,
      payload: {
        error: error,
      },
    });
  }
};
