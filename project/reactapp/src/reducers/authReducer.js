import { LOGIN_USER_SUCCESS, LOGOUT_USER_SUCCESS, IS_LOGGED_IN } from '../actions/types';

const initialState = {
  curUser : '',
  email : '',
  error: '',
  isAuthenticated : false
}

export default function(state = initialState, action) {
  let newState = {};
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
