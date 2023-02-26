import { 
  FETCH_PACKAGE_DATA,
  FETCH_PACKAGE_DATA_SUCCESS,
  FETCH_PACKAGE_DATA_ERROR,

} from '../actions/packageActions'


const initialState = {
statuscode:0,
data:[],
  isLoading: true,
};

const packageReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_PACKAGE_DATA:
      return {
        ...state,
        isLoading: true,
      };
    case FETCH_PACKAGE_DATA_SUCCESS:
      return {
        ...state,
        isLoading: false,
        statuscode: action.payload.statuscode,
        data: action.payload.data,
      };
    case FETCH_PACKAGE_DATA_ERROR:
      return {
        ...state,
        isLoading: false,
        statuscode: action.payload.statuscode,
        data: action.payload.data,
      };
    default:
      return state;
  }
};

export default packageReducer;