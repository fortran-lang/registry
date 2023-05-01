import {
  ADD_NAMESPACE_ADMIN_SUCCESS,
  ADD_NAMESPACE_ADMIN_FAILURE,
  REMOVE_NAMESPACE_ADMIN_SUCCESS,
  REMOVE_NAMESPACE_ADMIN_FAILURE,
  RESET_ERROR_MESSAGE,
} from "../actions/namespaceAdminsActions";

const initialState = {
  successMessage: null,
  errorMessage: null,
};

const addRemoveNamespaceAdminReducer = (state = initialState, action) => {
  switch (action.type) {
    case ADD_NAMESPACE_ADMIN_SUCCESS:
      return {
        ...state,
        successMessage: action.payload.message,
      };
    case ADD_NAMESPACE_ADMIN_FAILURE:
      return {
        ...state,
        errorMessage: action.payload.message,
      };
    case REMOVE_NAMESPACE_ADMIN_SUCCESS:
      return {
        ...state,
        successMessage: action.payload.message,
      };
    case REMOVE_NAMESPACE_ADMIN_FAILURE:
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

export default addRemoveNamespaceAdminReducer;
