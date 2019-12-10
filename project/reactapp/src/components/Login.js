import React from 'react';
import { Redirect } from 'react-router';
import { connect } from 'react-redux';
import { loginUser } from '../actions/authActions';


class Login extends React.Component {
  state = {
    email: '',
    password: '',
    toConfirm: false,
    isLoggedIn: false,
    createNewUser: false
  };

  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  onChange = (e) => {
    this.setState({[e.target.name] : e.target.value})
  }

  handleSubmit = async (e) => {
    e.preventDefault();
    const loginInfo = {
      email: this.state.email,
      password: this.state.password
    }

    this.props.loginUser(loginInfo);
  }

  ya = e => {
    e.preventDefault();
    console.log(this.props.isAuthenticated);
  }

  newAccount = e => {
    e.preventDefault();
    this.setState({createNewUser: true})
  }

  render() {
    if (this.props.isAuthenticated) {
      return (< Redirect to="/dashboard" />)
    } else if (this.props.confirmationRequired) {
      return (< Redirect to="/verify" />)
    } else if (this.state.createNewUser) {
      return (<Redirect to="/register" />)
    } else if (!this.state.toConfirm) {
      return (
        <div className="component-main-div">
          <h2> Login </h2>
          <form onSubmit={this.handleSubmit}>
            <label htmlFor="email">Email</label>
            <input type="text"
              id="emailLoginInput"
              name="email"
              placeholder="Email Address"
              onChange={this.onChange}/>


            <label htmlFor="password">Password</label>
            <input type="password"
              id="passwordInput"
              name="password"
              placeholder="Password"
              onChange={this.onChange}/>
            <input type="submit" value="Submit" />
            <p>
              <button className="link" onClick={this.newAccount}>Don't have an account? Create one now.</button>
            </p>
          </form>
        </div>
      );
    }


  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated,
  confirmationRequired: state.auth.confirmationRequired
})

export default connect(mapStateToProps, { loginUser })(Login);
