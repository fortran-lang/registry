import {
  MARK_PACKAGE_DEPRECATED,
  MARK_PACKAGE_DEPRECATED_SUCCESS,
  MARK_PACKAGE_DEPRECATED_ERROR,
  CREATE_NEW_RELEASE,
  CREATE_NEW_RELEASE_SUCCESS,
  CREATE_NEW_RELEASE_ERROR,
  ADMIN_AUTH_ERROR,
  ADMIN_AUTH_SUCCESS,
} from "../actions/adminActions";

const initialState = {
  packages: [],
  error: null,
  isAdmin: false,
};

const adminReducer = (state = initialState, action) => {
  switch (action.type) {
    case ADMIN_AUTH_SUCCESS:
      return { ...state, isAdmin: true };
    case ADMIN_AUTH_ERROR:
      return { ...state, isAdmin: false };
    case FETCH_PACKAGES:
      return { ...state, packages: [] };
    case FETCH_PACKAGES_SUCCESS:
      return { ...state, packages: action.payload };
    case FETCH_PACKAGES_ERROR:
      return { ...state, error: action.payload };
    case MARK_PACKAGE_DEPRECATED:
      return { ...state, packages: [] };
    case MARK_PACKAGE_DEPRECATED_SUCCESS:
      return { ...state, packages: action.payload };
    case MARK_PACKAGE_DEPRECATED_ERROR:
      return { ...state, error: action.payload };
    case CREATE_NEW_RELEASE:
      return { ...state, packages: [] };
    case CREATE_NEW_RELEASE_SUCCESS:
      return { ...state, packages: action.payload };
    case CREATE_NEW_RELEASE_ERROR:
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

export default adminReducer;
