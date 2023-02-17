import { SEARCH_SUCCESS, SEARCH_FAILURE } from "../actions/searchActions";

const initialState = {
  packages: null,
  totalPages: null,
  error: null,
};

const searchReducer = (state = initialState, action) => {
  switch (action.type) {
    case SEARCH_SUCCESS:
      return {
        ...state,
        packages: action.payload.packages,
        totalPages: action.payload.totalPages,
      };

    case SEARCH_FAILURE:
      return {
        ...state,
        packages: null,
        totalPages: action.payload.totalPages,
        error: action.payload.error,
      };

    default:
      return state;
  }
};

export default searchReducer;
