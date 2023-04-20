import {
  GENERATE_TOKEN_SUCCESS,
  GENERATE_TOKEN_FAILURE,
} from "../actions/generateNamespaceTokenActions";
import { RESET_ERROR_MESSAGE } from "../actions/authActions";

const initialState = {
  successMessage: null,
  errorMessage: null,
  uploadToken: null,
};

const generateNamespaceTokenReducer = (state = initialState, action) => {
  switch (action.type) {
    case GENERATE_TOKEN_SUCCESS:
      return {
        ...state,
        successMessage: action.payload.message,
        uploadToken: action.payload.uploadToken,
      };
    case GENERATE_TOKEN_FAILURE:
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

export default generateNamespaceTokenReducer;
