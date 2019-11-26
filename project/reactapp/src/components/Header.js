import React from 'react'
import './Header.css'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux';
import { logoutUser } from '../actions/authActions';

class Header extends React.Component {
  onLogout = (e) => {
    console.log(this.props.isAuthenticated);
    this.props.logoutUser();
    // Auth.signOut()
    //   .then(data => console.log(data))
    //   .catch(err => console.log(err));
  }

  render() {
    return (
      <div className="header">
        <div id="header-content">
          <img src="epluribusunum.png" id="logo" alt=''/>
          <h3 className="title">Twitter Political Unifier</h3>

          <div className="header-right">
            <Link to="/home">Home</Link>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/contact">Contact</Link>
            <Link to="/about">About</Link>
            {
              this.props.isAuthenticated ?
              <Link to="/" onClick={this.onLogout}>Logout</Link>
              : <Link to="/login">Login</Link>
            }
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated
})

export default connect(mapStateToProps, { logoutUser })(Header);
