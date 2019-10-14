import React from 'react';
import './App.css';
import Header from './components/Header'
import TweetInputForm from './components/TweetInputForm'

function App() {
  return (
    <div className="App">
      <Header />
      <div className="AppBody">

      <TweetInputForm />
      </div>
    </div>
  );
}

export default App;
