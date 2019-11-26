import React from 'react';
import './App.css';

import Header from './components/Header'
import About from './components/About'
import LabelUser from './components/LabelUser'
import LabelTweet from './components/LabelTweet'
import Login from './components/Login'
import SignUp from './components/SignUp'
import Verify from './components/Verify'
import Test from './components/Test'
import SearchedUsers from './components/SearchedUsers'
import SearchedTweets from './components/SearchedTweets'
import TweetDetails from './components/TweetDetails'
import LandingPage from './components/LandingPage'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  // Link
} from "react-router-dom"
import { Provider } from 'react-redux';
import store from './store'

function App() {
  return (
    <Provider store = {store}>
      <Router>
        <div className="App">
          <Header />
          <div className="AppBody">
          <Switch>
            <Route exact path="/">
              <LandingPage />
            </Route>
            <Route path="/home">
              <LabelTweet />
              <LabelUser />
            </Route>
            <Route path="/about">
              <About />
            </Route>
            <Route path="/login">
              <Login />
              <SignUp />
            </Route>
            <Route path="/verify">
              <Verify />
            </Route>
            <Route path="/test">
              <Test/>
            </Route>
            <Route path="/dashboard">
              <SearchedUsers />
              <SearchedTweets />
            </Route>
            <Route path="/tweetdetails/:id" component={TweetDetails} />
          </Switch>
          </div>
        </div>
      </Router>
    </Provider>
  );
}

export default App;
