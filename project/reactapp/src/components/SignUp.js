import React from 'react'
import { Auth } from 'aws-amplify';
import { Redirect } from "react-router";


class SignUp extends React.Component {
  state = {
    email: '',
    password1: '',
    password2: '',
    toVerify: false,
  };

  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  onChange = (e) => {
    this.setState({[e.target.name] : e.target.value})
  }

  handleNewSubmit = async (e) => {
    e.preventDefault();

    if (this.state.password1 !== this.state.password2) {
      alert("Passwords do not match");
      return;
    }

    if (this.state.password1.length < 8) {
      alert("Password must be at least 8 characters long");
      return;
    }

    if (!this.validateEmail(this.state.email)) {
      alert("Invalid email");
      return;
    }

    await Auth.signUp(
      this.state.email,
      this.state.password1
    )
    .then(data => {
      this.setState({toVerify: true});
      // console.log(data)
    })
    .catch((err) => {
      if (err.code === 'UsernameExistsException') {
        alert('Email/username already exists');
      }
    });
  }

  render() {
    if (this.state.toVerify === false) {
      return (
        <div className="component-main-div">
          <h2> Register New User </h2>
          <form onSubmit={this.handleNewSubmit}>
            <label htmlFor="email">Email</label>
            <input type="text"
              id="emailSignupInput"
              name="email"
              placeholder="Email Address"
              onChange={this.onChange}/>

            <label htmlFor="password1">Password</label>
            <input type="password"
              id="passwordInput1"
              name="password1"
              placeholder="Password"
              onChange={this.onChange}/>

          <label htmlFor="password2">Re-enter Password</label>
          <input type="password"
            id="passwordInput2"
            name="password2"
            placeholder="Re-enter Password"
            onChange={this.onChange}/>
          <input type="submit" value="Submit"  />
        </form>
        </div>
      );
    } else {
      return (
        (<Redirect to='/verify'/>)
      )
    }
  }
}

export default SignUp;
