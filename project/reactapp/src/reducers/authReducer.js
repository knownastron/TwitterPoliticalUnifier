import { LOGIN_USER_SUCCESS,
         LOGOUT_USER_SUCCESS,
         USER_NOT_CONFIRMED,
         RESET_USER_CONFIRMATION } from '../actions/types';

const initialState = {
  curUser : '',
  email : '',
  error: '',
  isAuthenticated : false,
  confirmationRequired: false
}

export default function(state = initialState, action) {
  switch (action.type) {

    case LOGIN_USER_SUCCESS:
      return {
        ...state,
        token: action.payload.signInUserSession.idToken.jwtToken,
        curUser: action.payload,
        email: action.payload.attributes.email,
        isAuthenticated: true
      }

    case LOGOUT_USER_SUCCESS:
      return {
        ...state,
        isAuthenticated: false,
        token: '',
        email: '',
        curUser: ''
      }

    case USER_NOT_CONFIRMED:
      return {
        ...state,
        confirmationRequired: true,
        isAuthenticated: false,
        token: '',
        email: action.payload.email,
        curUser: ''
      }

    case RESET_USER_CONFIRMATION:
      return {
        ...state,
        confirmationRequired: false
      }
    default:
     return state;



  }
}
