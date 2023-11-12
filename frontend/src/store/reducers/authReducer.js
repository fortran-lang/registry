import {
  LOGIN_SUCCESS,
  LOGIN_FAILURE,
  SIGNUP_SUCCESS,
  SIGNUP_FAILURE,
  LOGOUT_SUCCESS,
  LOGOUT_FAILURE,
  RESET_ERROR_MESSAGE,
  LOGIN_REQUEST,
  SIGNUP_REQUEST,
  LOGOUT_REQUEST
} from "../actions/authActions";

const initialState = {
  isAuthenticated: false,
  uuid: null,
  error: null,
  username: null,
  isLoading: false,
  message: null,
};

const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOGIN_REQUEST:
      return {
        ...state,
        isLoading: true,
      };
      case LOGOUT_REQUEST:
        return {
          ...state,
          isLoading: true,
        };
      case SIGNUP_REQUEST:
      return {
        ...state,
        isLoading: true,
      };
    case LOGIN_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        uuid: action.payload.uuid,
        username: action.payload.username,
        isLoading: false,
      };

    case LOGIN_FAILURE:
      return {
        ...state,
        isAuthenticated: false,
        error: action.payload.error,
        isLoading: false,
      };

    case LOGOUT_SUCCESS:
      return {
        ...state,
        isAuthenticated: false,
        uuid: null,
        username: null,
        error: null,
        isLoading: false,
      };

    case LOGOUT_FAILURE:
      return {
        ...state,
        error: action.payload.error,
        isLoading: false,
      };

    case SIGNUP_SUCCESS:
      return {
        ...state,
        message: action.payload.message,
        isLoading: false,
      };

    case SIGNUP_FAILURE:
      return {
        ...state,
        isAuthenticated: false,
        error: action.payload.error,
        isLoading: false,
      };
    case RESET_ERROR_MESSAGE:
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
};

export default authReducer;
