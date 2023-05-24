import {
  FETCH_USERS_LIST,
  FETCH_USERS_LIST_SUCCESS,
  FETCH_USERS_LIST_ERROR,
} from "../actions/userListActions";

const initialState = {
  users: null,
  isLoading: true,
};

const userListReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_USERS_LIST:
      return {
        ...state,
        isLoading: true,
      };
    case FETCH_USERS_LIST_SUCCESS:
      return {
        ...state,
        users: action.payload.users,
        isLoading: false,
      };
    case FETCH_USERS_LIST_ERROR:
      return {
        ...state,
        isLoading: false,
      };
    default:
      return state;
  }
};

export default userListReducer;
