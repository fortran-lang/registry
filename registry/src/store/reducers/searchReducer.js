import { SEARCH_SUCCESS, SEARCH_FAILURE } from "../actions/searchActions";

const initialState = {
  packages: null,
  error: null,
};

const searchReducer = (state = initialState, action) => {
  switch (action.type) {
    case SEARCH_SUCCESS:
      return {
        ...state,
        packages: action.payload.packages,
      };

    case SEARCH_FAILURE:
      return {
        ...state,
        packages: null,
        error: action.payload.error,
      };

    default:
      return state;
  }
};

export default searchReducer;
