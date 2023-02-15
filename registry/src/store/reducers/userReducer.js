import {
  FETCH_USER_DATA,
  FETCH_USER_DATA_SUCCESS,
  FETCH_USER_DATA_ERROR,
} from "../actions/userActions";

const initialState = {
  email: "",
  dateJoined: "",
  projects: [],
  isLoading: true,
  notFound: false,
};

const userReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_USER_DATA:
      return {
        ...state,
        isLoading: true,
        notFound: false,
      };
    case FETCH_USER_DATA_SUCCESS:
      return {
        email: action.payload.email,
        dateJoined: action.payload.dateJoined,
        projects: action.payload.projects,
        isLoading: false,
        notFound: false,
      };
    case FETCH_USER_DATA_ERROR:
      return {
        ...state,
        isLoading: false,
        notFound: true,
      };
    default:
      return state;
  }
};

export default userReducer;
