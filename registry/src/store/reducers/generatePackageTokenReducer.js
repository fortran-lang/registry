import {
  GENERATE_PACKAGE_TOKEN_SUCCESS,
  GENERATE_PACKAGE_TOKEN_FAILURE,
} from "../actions/generatePackageTokenActions";
import { RESET_ERROR_MESSAGE } from "../actions/authActions";

const initialState = {
  successMessage: null,
  errorMessage: null,
  uploadToken: null,
};

const generatePackageTokenReducer = (state = initialState, action) => {
  switch (action.type) {
    case GENERATE_PACKAGE_TOKEN_SUCCESS:
      return {
        ...state,
        successMessage: action.payload.message,
        uploadToken: action.payload.uploadToken,
      };
    case GENERATE_PACKAGE_TOKEN_FAILURE:
      return {
        ...state,
        errorMessage: action.payload.message,
      };
    case RESET_ERROR_MESSAGE:
      return {
        ...state,
        successMessage: null,
        errorMessage: null,
      };
    default:
      return state;
  }
};

export default generatePackageTokenReducer;
