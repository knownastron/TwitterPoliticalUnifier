import { LOGIN_USER_SUCCESS,
         LOGOUT_USER_SUCCESS,
         USER_NOT_CONFIRMED,
         RESET_USER_CONFIRMATION} from './types';
import { Auth } from 'aws-amplify';

export const loginUser = (loginInfo) => async dispatch => {
  await Auth.signIn(
    loginInfo.email,
    loginInfo.password
  ).then(user => {
    console.log(user);
    // console.log(user.signInUserSession.idToken.jwtToken);
    dispatch({
      type: LOGIN_USER_SUCCESS,
      payload: user,
      authenticatedUser: true,
    })
    alert("Logged in");
  }).catch(err => {
    if (err.code === 'UserNotConfirmedException') {
      dispatch({
        type: USER_NOT_CONFIRMED,
        payload: loginInfo,
        confirmationRequired: true
      })
      alert("User has not been confirmed")
      // need error handling redirect to verify page
      return
    }
    console.log(err)
    alert("Invalid username or password");
    return
  });
}

export const logoutUser = () => async dispatch => {
  Auth.signOut()
    .then(data => {
      console.log(data)
      dispatch({
        type: LOGOUT_USER_SUCCESS
      })
      alert('Log out successful')
    })
    .catch(err => console.log(err));
}

export const resetConfirmation = () => dispatch => {
  dispatch({
    type: RESET_USER_CONFIRMATION,
    confirmationRequired: false
  })
}
