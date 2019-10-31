import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import config from './config/config';
import Amplify from 'aws-amplify';


Amplify.configure({
  Auth: {
    mandatorySignIn: true,
    region: config.cognito.REGION,
    userPoolId: config.cognito.USER_POOL_ID,
    identityPoolId: config.cognito.IDENTITY_POOL_ID,
    userPoolWebClientId: config.cognito.APP_CLIENT_ID
  }
});

ReactDOM.render(<App />, document.getElementById('root'));
