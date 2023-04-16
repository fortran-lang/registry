import {
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
  isLoading: true,
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
