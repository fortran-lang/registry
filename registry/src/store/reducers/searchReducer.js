import {
  SEARCH_SUCCESS,
  SEARCH_FAILURE,
  SET_QUERY,
  SET_ORDER_BY,
  SEARCH_LOADING,
} from "../actions/searchActions";

const initialState = {
  packages: null,
  totalPages: null,
  error: null,
  currentPage: 0,
  query: "",
  orderBy: "None",
  isLoading: true,
};

const searchReducer = (state = initialState, action) => {
  switch (action.type) {
    case SEARCH_LOADING:
      return {
        ...state,
        isLoading: true,
        packages: null,
      };
    case SEARCH_SUCCESS:
      return {
        ...state,
        isLoading: false,
        packages: action.payload.packages,
        totalPages: action.payload.totalPages,
        currentPage: action.payload.currentPage,
      };

    case SEARCH_FAILURE:
      return {
        ...state,
        isLoading: false,
        packages: null,
        totalPages: action.payload.totalPages,
        error: action.payload.error,
      };

    case SET_QUERY:
      return {
        ...state,
        query: action.payload.query,
      };

    case SET_ORDER_BY:
      return {
        ...state,
        orderBy: action.payload.orderBy,
      };

    default:
      return state;
  }
};

export default searchReducer;
