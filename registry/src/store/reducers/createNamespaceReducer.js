import {
  CREATE_NAMESPACE,
  CREATE_NAMESPACE_SUCCESS,
  CREATE_NAMESPACE_ERROR,
} from "../actions/createNamespaceActions";

const initialState = {
  statuscode: 0,
  message: "",
  isLoading: false,
};

const createNamespaceReducer = (state = initialState, action) => {
  switch (action.type) {
    case CREATE_NAMESPACE:
      return {
        ...state,
        isLoading: true,
        statuscode: 0,
        message: "",
      };
    case CREATE_NAMESPACE_SUCCESS:
      return {
        message: action.payload.message,
        statuscode: action.payload.statuscode,
        isLoading: false,
      };
    case CREATE_NAMESPACE_ERROR:
      return {
        ...state,
        message: action.payload.message,
        statuscode: action.payload.statuscode,
        isLoading: false,
      };
    default:
      return state;
  }
};

export default createNamespaceReducer;
