import React from 'react';
import './App.css';

import Header from './components/Header'
import About from './components/About'
import Login from './components/Login'
import SignUp from './components/SignUp'
import Verify from './components/Verify'
import Test from './components/Test'
import Dashboard from './components/Dashboard'
import TweetDetails from './components/TweetDetails'
import LandingPage from './components/LandingPage'
import Home from './components/Home'
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
              <Home />
            </Route>
            <Route path="/about">
              <About />
            </Route>
            <Route path="/login">
              <Login />
            </Route>
            <Route path="/register">
              <SignUp />
            </Route>
            <Route path="/verify" component={Verify}>
            </Route>
            <Route path="/test">
              <Test/>
            </Route>
            <Route path="/dashboard">
              <Dashboard />
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
