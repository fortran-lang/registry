import {
  DELETE_ACCOUNT,
  DELETE_ACCOUNT_ERROR,
  GET_USER_ACCOUNT,
  RESET_PASSWORD_ERROR,
  RESET_PASSWORD,
} from "../actions/accountActions";

const initialState = {
  isAuthenticated: false,
  uuid: null,
  error: null,
  email: "",
  dateJoined: "",
};

const accountReducer = (state = initialState, action) => {
  switch (action.type) {
    case DELETE_ACCOUNT:
      return {
        ...state,
        isAuthenticated: false,
        uuid: null,
        error: null,
        email: "",
        dateJoined: "",
        message: action.payload,
      };
    case DELETE_ACCOUNT_ERROR:
      return {
        ...state,
        error: action.payload,
      };
    case GET_USER_ACCOUNT:
      return {
        ...state,
        email: action.payload.email,
        dateJoined: action.payload.dateJoined,
      };
    case RESET_PASSWORD:
      return {
        ...state,
        error: action.payload,
      };
    case RESET_PASSWORD_ERROR:
      return {
        ...state,
        error: action.payload,
      };
    default:
      return state;
  }
};

export default accountReducer;
