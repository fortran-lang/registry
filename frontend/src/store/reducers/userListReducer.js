import {
  FETCH_USERS_LIST,
  FETCH_USERS_LIST_SUCCESS,
  FETCH_USERS_LIST_ERROR,
} from "../actions/userListActions";

const initialState = {
  users: null,
  isLoading: true,
  error: null,
};

const userListReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_USERS_LIST:
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case FETCH_USERS_LIST_SUCCESS:
      return {
        ...state,
        users: action.payload.users,
        isLoading: false,
        error: null,
      };
    case FETCH_USERS_LIST_ERROR:
      return {
        ...state,
        isLoading: false,
        error: action.payload.message,
      };
    default:
      return state;
  }
};

export default userListReducer;
