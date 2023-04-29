import {
  ADD_NAMESPACE_MAINTAINER_SUCCESS,
  ADD_NAMESPACE_MAINTAINER_FAILURE,
  RESET_ERROR_MESSAGE,
  REMOVE_NAMESPACE_MAINTAINER_SUCCESS,
  REMOVE_NAMESPACE_MAINTAINER_FAILURE,
} from "../actions/namespaceMaintainersActions";

const initialState = {
  successMessage: null,
  errorMessage: null,
};

const addRemoveNamespaceMaintainerReducer = (state = initialState, action) => {
  switch (action.type) {
    case ADD_NAMESPACE_MAINTAINER_SUCCESS:
      return {
        ...state,
        successMessage: action.payload.message,
      };
    case ADD_NAMESPACE_MAINTAINER_FAILURE:
      return {
        ...state,
        errorMessage: action.payload.message,
      };
    case REMOVE_NAMESPACE_MAINTAINER_SUCCESS:
      return {
        ...state,
        successMessage: action.payload.message,
      };
    case REMOVE_NAMESPACE_MAINTAINER_FAILURE:
      return {
        ...state,
        errorMessage: action.payload.message,
      };
    case RESET_ERROR_MESSAGE:
      return {
        ...state,
        successMessage: null,
        errorMessage: null,
      };
    default:
      return state;
  }
};

export default addRemoveNamespaceMaintainerReducer;
