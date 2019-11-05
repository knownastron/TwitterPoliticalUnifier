import { LOGIN_USER_SUCCESS, LOGOUT_USER_SUCCESS} from '../actions/types';

const initialState = {
  curUser : '',
  email : '',
  error: '',
  isAuthenticated : false
}

export default function(state = initialState, action) {
  // let newState = {};
  switch (action.type) {
    // let newState = {};

    case LOGIN_USER_SUCCESS:
      console.log('reducer')
      // newState = {
      //   curUser : action.payload,
      //   email: action.email,
      //   isAuthenticated : true
      // };
      return {
        ...state,
        curUser: action.payload,
        email: action.payload.attributes.email,
        isAuthenticated: true
      }
      // return Object.assign({}, state, newState);

    case LOGOUT_USER_SUCCESS:
      return {
        ...state,
        isAuthenticated: false
      }
    default:
     return state;
  }
}
