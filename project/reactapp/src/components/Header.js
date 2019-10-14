import React from 'react'
import './Header.css'

class Header extends React.Component {

  render() {
    return (
      <div className="header">
        <img src="epluribusunum.png" id="logo" alt=''/>
        <h3 className="title">Twitter Political Unifier</h3>

        <div className="header-right">
          <a className="active" href="#home">Home</a>
          <a href="#contact">Contact</a>
          <a href="#about">About</a>
        </div>
      </div>
    );
  }


}

export default Header;
