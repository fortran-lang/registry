import { FETCH_NAMESPACE_DATA, FETCH_NAMESPACE_DATA_SUCCESS, FETCH_NAMESPACE_DATA_ERROR } from "../actions/namespaceActions";
  
  const initialState = {
    dateJoined: "",
    projects: [],
    isLoading: true,
    notFound: false,
  };
  
  const namespaceReducer = (state = initialState, action) => {
    switch (action.type) {
      case FETCH_NAMESPACE_DATA:
        return {
          ...state,
          isLoading: true,
          notFound: false,
        };
      case FETCH_NAMESPACE_DATA_SUCCESS:
        return {
          dateJoined: action.payload.dateJoined,
          projects: action.payload.projects,
          isLoading: false,
          notFound: false,
        };
      case FETCH_NAMESPACE_DATA_ERROR:
        return {
          ...state,
          isLoading: false,
          notFound: true,
        };
      default:
        return state;
    }
  };
  
  export default namespaceReducer;
  