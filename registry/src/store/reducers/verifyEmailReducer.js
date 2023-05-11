import {
  VERIFY_REQUEST_SUCCESS,
  VERIFY_REQUEST_FAILURE,
  VERIFY_REQUEST,
} from "../actions/verifyEmailActions";

const initialState = {
  statuscode: 0,
    message: "",
};

const verifyEmailReducer = (state = initialState, action) => {
  switch (action.type) {
    case VERIFY_REQUEST_SUCCESS:
      return {
        ...state,
        statuscode: action.payload.statuscode,
        message: action.payload.message,
      };

    case VERIFY_REQUEST_FAILURE:
      return {
        ...state,
        statuscode: action.payload.statuscode,
        message: action.payload.message,
      };

      case VERIFY_REQUEST:
        return {
          ...state,
        };
        
    default:
      return state;
  }
};

export default verifyEmailReducer;
