import React from 'react';
import './App.css';
import Header from './components/Header'
import About from './components/About'
import LabelUser from './components/LabelUser'
import TweetInputForm from './components/TweetInputForm'
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
          <Route path="/about">
            <About />
          </Route>
          <Route path="/">
            <TweetInputForm />
            <LabelUser />
          </Route>

        </Switch>


        </div>
      </div>
    </Router>
  );
}

export default App;
