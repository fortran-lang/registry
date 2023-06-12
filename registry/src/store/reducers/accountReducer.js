import {
  GET_USER_ACCOUNT,
  RESET_PASSWORD_ERROR,
  RESET_PASSWORD,
  RESET_MESSAGES,CHANGE_EMAIL_SUCCESS,CHANGE_EMAIL_FAILURE
} from "../actions/accountActions";

const initialState = {
  isAuthenticated: false,
  uuid: null,
  error: null,
  email: "",
  dateJoined: "",
  isLoading: true,
  message: null,
  resetPasswordSuccessMsg: null,
};

const accountReducer = (state = initialState, action) => {
  switch (action.type) {
    case GET_USER_ACCOUNT:
      return {
        ...state,
        email: action.payload.email,
        dateJoined: action.payload.dateJoined,
        isLoading: false,
      };
    case RESET_PASSWORD:
      return {
        ...state,
        resetPasswordSuccessMsg: action.payload,
      };
    case CHANGE_EMAIL_SUCCESS:
      return {
        ...state,
        message: action.payload,
      };
      case CHANGE_EMAIL_FAILURE:
        return {
          ...state,
          message: action.payload,
        };
    case RESET_PASSWORD_ERROR:
      return {
        ...state,
        error: action.payload,
      };
    case RESET_MESSAGES:
      return {
        error: null,
        resetPasswordSuccessMsg: null,
      };
    default:
      return state;
  }
};

export default accountReducer;
