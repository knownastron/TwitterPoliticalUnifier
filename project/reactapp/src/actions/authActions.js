import { LOGIN_USER_SUCCESS, LOGOUT_USER_SUCCESS } from './types';
import { Auth } from 'aws-amplify';

export const loginUser = (loginInfo) => async dispatch => {
  // console.log("LOGININFO", loginInfo);
  await Auth.signIn(
    loginInfo.email,
    loginInfo.password
  ).then(user => {
    // console.log(user);
    dispatch({
      type: LOGIN_USER_SUCCESS,
      payload: user,
      authenticatedUser: true,
    })
    alert("Logged in");
  }).catch(err => {
    if (err.code === 'UserNotConfirmedException') {
      alert("User has not been confirmed")
      // need error handling
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
// export function loginUser(loginInfo) {
//   console.log("LOGIN ACTION called", loginInfo);
//   return async function(dispatch, loginInfo) {
//
//
//   }
// }
