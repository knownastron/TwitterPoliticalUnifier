import React from 'react';
import './App.css';

import Header from './components/Header'
import About from './components/About'
import LabelUser from './components/LabelUser'
import LabelTweet from './components/LabelTweet'
import Login from './components/Login'
import SignUp from './components/SignUp'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom"

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <div className="AppBody">
        <Switch>
          <Route exact path="/">
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


        </Switch>


        </div>
      </div>
    </Router>
  );
}

export default App;
