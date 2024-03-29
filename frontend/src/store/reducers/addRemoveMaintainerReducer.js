import {
  ADD_MAINTAINER_SUCCESS,
  ADD_MAINTAINER_FAILURE,
  REMOVE_MAINTAINER_SUCCESS,
  REMOVE_MAINTAINER_FAILURE,
} from "../actions/addRemoveMaintainerActions";
import { RESET_ERROR_MESSAGE } from "../actions/authActions";

const initialState = {
  successMessage: null,
  errorMessage: null,
};

const addRemoveMaintainerReducer = (state = initialState, action) => {
  switch (action.type) {
    case ADD_MAINTAINER_SUCCESS:
      return {
        ...state,
        successMessage: action.payload.message,
      };
    case ADD_MAINTAINER_FAILURE:
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
    case REMOVE_MAINTAINER_SUCCESS:
      return {
        ...state,
        successMessage: action.payload.message,
      };
    case REMOVE_MAINTAINER_FAILURE:
      return {
        ...state,
        errorMessage: action.payload.message,
      };
    default:
      return state;
  }
};

export default addRemoveMaintainerReducer;
