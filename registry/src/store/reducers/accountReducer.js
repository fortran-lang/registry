import {
  GET_USER_ACCOUNT,
  RESET_PASSWORD_ERROR,
  RESET_PASSWORD,
  RESET_MESSAGES,
  CHANGE_EMAIL_SUCCESS,
  CHANGE_EMAIL_FAILURE,
  CHANGE_EMAIL,
  RESET_PASSWORD_SUCCESS,
} from "../actions/accountActions";

const initialState = {
  isAuthenticated: false,
  uuid: null,
  error: null,
  email: "",
  dateJoined: "",
  isLoading: true,
  isLoadingEmail: false,
  isLoadingPassword: false,
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
        isLoadingPassword: true,
      };
    case CHANGE_EMAIL_SUCCESS:
      return {
        ...state,
        message: action.payload,
        isLoadingEmail: false,
      };
    case CHANGE_EMAIL:
      return {
        ...state,
        message: action.payload,
        isLoadingEmail: true,
      };
    case CHANGE_EMAIL_FAILURE:
      return {
        ...state,
        message: action.payload,
        isLoadingEmail: false,
      };
    case RESET_PASSWORD_SUCCESS:
      return {
        ...state,
        message: action.payload,
        isLoadingPassword: false,
      };
    case RESET_PASSWORD_ERROR:
      return {
        ...state,
        error: action.payload,
        isLoadingPassword: false,
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
