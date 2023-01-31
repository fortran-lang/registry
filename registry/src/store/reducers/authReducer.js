import { LOGIN_SUCCESS, LOGIN_FAILURE } from "../actions/authActions";

const initialState = {
  isAuthenticated: false,
  uuid: null,
  error: null,
  isLoading: false,
};

const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOGIN_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        uuid: action.payload.uuid,
      };

    case LOGIN_FAILURE:
      return {
        ...state,
        isAuthenticated: false,
        error: action.payload.error,
      };

    default:
      return state;
  }
};

export default authReducer;
