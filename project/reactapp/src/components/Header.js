import React from 'react'
import './Header.css'
import { Link } from 'react-router-dom'

class Header extends React.Component {
  // Remove this later, just for testing purposes
  test_state = {
    ya: true 
  }
  render() {
    return (
      <div className="header">
        <img src="epluribusunum.png" id="logo" alt=''/>
        <h3 className="title">Twitter Political Unifier</h3>

        <div className="header-right">
          <Link to="/">Home</Link>
          <Link to="/contact">Contact</Link>
          <Link to="/about">About</Link>
          { this.test_state.ya
            ? <Link to="/login">Login</Link>
            : <Link to="/">Logout</Link>
          }
        </div>
      </div>
    );
  }
}

export default Header;
