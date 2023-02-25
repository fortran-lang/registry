import {
  UPLOAD_PACKAGE,
  UPLOAD_PACKAGE_SUCCESS,
  UPLOAD_PACKAGE_ERROR,
} from "../actions/uploadActions";

const initialState = {
  data: {},
  isLoading: false,
};

const uploadReducer = (state = initialState, action) => {
  switch (action.type) {
    case UPLOAD_PACKAGE:
      return {
        ...state,
        isLoading: true,
      };
    case UPLOAD_PACKAGE_SUCCESS:
      return {
        message: action.payload.message,
        isLoading: false,
      };
    case UPLOAD_PACKAGE_ERROR:
      return {
        ...state,
        message: action.payload.message,
        isLoading: false,
      };
    default:
      return state;
  }
};

export default uploadReducer;
