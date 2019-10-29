import React from 'react'
import { Auth } from "aws-amplify";


class Login extends React.Component {
  state = {
    email: '',
    password: ''
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

    try {
      await Auth.signIn(this.state.email, this.state.password);
      console.log(e)
      alert("Logged in");
    } catch (e) {
      alert(e.message);
    }
  };

  render() {
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
  }
}

export default Login;
