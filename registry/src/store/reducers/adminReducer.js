import {
  DEPRECATE_PACKAGE_SUCCESS,
  DEPRECATE_PACKAGE_ERROR,
  DELETE_USER_SUCCESS,
  DELETE_USER_ERROR,
  DELETE_NAMESPACE_SUCCESS,
  DELETE_NAMESPACE_ERROR,
  DELETE_RELEASE_SUCCESS,
  DELETE_RELEASE_ERROR,
  ADMIN_AUTH_ERROR,
  ADMIN_AUTH_SUCCESS,
  DELETE_PACKAGE_SUCCESS,
  DELETE_PACKAGE_ERROR,
} from "../actions/adminActions";

const initialState = {
  error: null,
  isAdmin: false,
  message: "",
  statuscode: null,
};

const adminReducer = (state = initialState, action) => {
  switch (action.type) {
    case ADMIN_AUTH_SUCCESS:
      return { ...state, isAdmin: true };
    case ADMIN_AUTH_ERROR:
      return { ...state, isAdmin: false };
    case DELETE_USER_SUCCESS:
      return {
        ...state,
        message: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case DELETE_USER_ERROR:
      return {
        ...state,
        error: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case DELETE_NAMESPACE_SUCCESS:
      return {
        ...state,
        message: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case DELETE_NAMESPACE_ERROR:
      return {
        ...state,
        error: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case DELETE_PACKAGE_SUCCESS:
      return {
        ...state,
        message: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case DELETE_PACKAGE_ERROR:
      return {
        ...state,
        error: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case DELETE_RELEASE_SUCCESS:
      return {
        ...state,
        message: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case DELETE_RELEASE_ERROR:
      return {
        ...state,
        error: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case DEPRECATE_PACKAGE_SUCCESS:
      return {
        ...state,
        message: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    case DEPRECATE_PACKAGE_ERROR:
      return {
        ...state,
        error: action.payload.message,
        statuscode: action.payload.statuscode,
      };
    default:
      return state;
  }
};

export default adminReducer;
