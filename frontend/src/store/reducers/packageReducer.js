import {
  FETCH_PACKAGE_DATA,
  FETCH_PACKAGE_DATA_SUCCESS,
  FETCH_PACKAGE_DATA_ERROR,
  VERIFY_USER_ROLE_SUCCESS,
  VERIFY_USER_ROLE_ERROR,
  VERIFY_USER_ROLE,
} from "../actions/packageActions";

const initialState = {
  statuscode: 0,
  data: [],
  isLoading: true,
  isVerified: null,
};

const packageReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_PACKAGE_DATA:
      return {
        ...state,
        isLoading: true,
      };
    case FETCH_PACKAGE_DATA_SUCCESS:
      return {
        ...state,
        isLoading: false,
        statuscode: action.payload.statuscode,
        data: action.payload.data,
      };
    case FETCH_PACKAGE_DATA_ERROR:
      return {
        ...state,
        isLoading: false,
        statuscode: action.payload.statuscode,
        data: action.payload.data,
      };
    case VERIFY_USER_ROLE_SUCCESS:
      return {
        ...state,
        isVerified: action.payload.data.isVerified,
      };
    case VERIFY_USER_ROLE_ERROR:
      return {
        ...state,
        isVerified: false,
      };
    case VERIFY_USER_ROLE:
      return {
        ...state,
        isVerified: null,
      };
    default:
      return state;
  }
};

export default packageReducer;
