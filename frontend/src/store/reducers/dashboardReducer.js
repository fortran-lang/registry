import {
    REQUEST_PACKAGES,
    REQUEST_PACKAGES_SUCCESS,
    REQUEST_PACKAGES_FAILURE,
} from "../actions/dashboardActions";

const initialState = {
    packages: null,
    namespaces: null,
    isLoading: true, 
    error: null,
}

const dashboardReducer = (state = initialState, action) => {
    switch (action.type) {
        case REQUEST_PACKAGES:
            return {
                ...state,
                isLoading: true,
            }

        case REQUEST_PACKAGES_SUCCESS:
            
            return {
                ...state, 
                isLoading: false,
                packages: action.payload.packages,
                namespaces: action.payload.namespaces,
            }

        case REQUEST_PACKAGES_FAILURE:
            return  {
                ...state,
                isLoading: false, 
            }
    
        default:
            return state
    }
}

export default dashboardReducer;
