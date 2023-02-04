import {
  LOGIN_SUCCESS,
  LOGIN_FAILURE,
  SIGNUP_SUCCESS,
  SIGNUP_FAILURE,
} from "../actions/authActions";

const initialState = {
  isAuthenticated: false,
  uuid: null,
  error: null,
  username: null,
};

const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOGIN_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        uuid: action.payload.uuid,
        username: action.payload.username,
      };

    case LOGIN_FAILURE:
      return {
        ...state,
        isAuthenticated: false,
        error: action.payload.error,
      };

    case SIGNUP_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        uuid: action.payload.uuid,
        username: action.payload.username,
      };

    case SIGNUP_FAILURE:
      return {
        ...state,
        isAuthenticated: false,
        error: action.payload.error,
      };
    default:
      return state;
  }
};

export default authReducer;
