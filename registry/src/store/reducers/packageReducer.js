import { 
  FETCH_PACKAGE_DATA,
  FETCH_PACKAGE_DATA_SUCCESS,
  FETCH_PACKAGE_DATA_ERROR,

} from '../actions/packageActions'


const initialState = {
  author: '',
  tags: [],
  license: '',
  createdAt: '',
  versionData: {},
  updatedAt: '',
  description: '',
  notFound: false,
  isLoading: false
};

const packageReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_PACKAGE_DATA:
      return {
        ...state,
        isLoading: true
      };
    case FETCH_PACKAGE_DATA_SUCCESS:
      return {
        ...state,
        isLoading: false,
        author: action.payload.author,
        tags: action.payload.tags,
        license: action.payload.license,
        createdAt: action.payload.createdAt,
        versionData: action.payload.versionData,
        updatedAt: action.payload.updatedAt,
        description: action.payload.description
      };
    case FETCH_PACKAGE_DATA_ERROR:
      return {
        ...state,
        isLoading: false,
        notFound: true
      };
    default:
      return state;
  }
};

export default packageReducer;