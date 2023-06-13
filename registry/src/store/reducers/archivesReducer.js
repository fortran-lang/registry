import {
  FETCH_ARCHIVES_DATA,
  FETCH_ARCHIVES_DATA_SUCCESS,
  FETCH_ARCHIVES_DATA_ERROR,
} from "../actions/archivesActions";

const initialState = {
  archives: [],
  message:null,
  isLoading: true,
};

const archivesReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_ARCHIVES_DATA:
      return {
        ...state,
        isLoading: true,
      };
    case FETCH_ARCHIVES_DATA_SUCCESS:
      return {
        archives: action.payload.archives,
        message: action.payload.message,
        isLoading: false,
      };
    case FETCH_ARCHIVES_DATA_ERROR:
      return {
        ...state,
        isLoading: false,
      };
    default:
      return state;
  }
};

export default archivesReducer;
