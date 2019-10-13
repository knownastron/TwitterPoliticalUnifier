import React from 'react'
import './Header.css'

class Header extends React.Component {

  render() {
    return (
      // <header className='header'>Twitter Political Unifier </header>
      <div class="header">
        <img src="epluribusunum.png" id="logo"/>
        <a href="/" class="logo">Twitter Political Unifier</a>

        <div class="header-right">
          <a class="active" href="#home">Home</a>
          <a href="#contact">Contact</a>
          <a href="#about">About</a>
        </div>
      </div>
    );
  }
}

export default Header;
