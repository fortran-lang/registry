import {
    RESET_PASSWORD,
  RESET_REQUEST,
  RESET_REQUEST_SUCCESS,
  RESET_REQUEST_FAILURE,
  RESET_SUCCESS,
  RESET_FAILURE,
} from "../actions/resetPasswordActions";

const initialState = {
  statuscode: 0,
    message: "",
    isLoading: false,
};

const resetPasswordReducer = (state = initialState, action) => {
  switch (action.type) {
    case RESET_REQUEST_SUCCESS:
      return {
        ...state,
        statuscode: action.payload.statuscode,
        message: action.payload.message,
        isLoading: false,
      };

    case RESET_REQUEST_FAILURE:
      return {
        ...state,
        statuscode: action.payload.statuscode,
        message: action.payload.message,
        isLoading: false,
      };

      case RESET_REQUEST:
        return {
          ...state,
          isLoading: true,
        };

        case RESET_PASSWORD:
        return {
          ...state,
          isLoading: true,
        };
        case RESET_SUCCESS:
      return {
        ...state,
        statuscode: action.payload.statuscode,
        message: action.payload.message,
        isLoading: false,
      };

    case RESET_FAILURE:
      return {
        ...state,
        statuscode: action.payload.statuscode,
        message: action.payload.message,
        isLoading: false,
      };

    default:
      return state;
  }
};

export default resetPasswordReducer;
