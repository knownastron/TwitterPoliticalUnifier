import React from 'react';
import { Auth } from "aws-amplify";
import { Redirect } from "react-router";

class Login extends React.Component {
  state = {
    email: '',
    password: '',
    toConfirm: false,
    cuser: '',
  };

  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  emailChange = (e) => {
    this.setState({email: e.target.value});
  }

  passwordChange = (e) => {
    this.setState({password: e.target.value});
  }

  handleSubmit = async (e) => {
    e.preventDefault();

    await Auth.signIn(
      this.state.email,
      this.state.password
    ).then(user => {
      console.log(user);
      this.setState({curUser : user})
      this.setState({toConfirm: true})
      alert("Logged in");
    }).catch(err => {
      if (err.code === 'UserNotConfirmedException') {
        alert("User has not been confirmed")
        this.setState({toConfirm: true});
      }
      console.log(err)
      alert("Invalid username or password");
    });

  };

  render() {
    if (!this.state.toConfirm) {
      return (
        <div className="component-main-div">
          <h2> Login </h2>
          <form onSubmit={this.handleSubmit}>
            <label htmlFor="email">Email</label>
            <input type="text"
              id="emailInput"
              name="email"
              placeholder="Email Address"
              onBlur={this.emailChange}/>

            <label htmlFor="password">Password</label>
            <input type="password"
              id="passwordInput"
              name="passwordInput"
              placeholder="Password"
              onBlur={this.passwordChange}/>
            <input type="submit" value="Submit" />
          </form>
        </div>
      );
    } else {
      return (<Redirect to="/" />)

    }
  }
}

export default Login;
