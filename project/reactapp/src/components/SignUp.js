import React from 'react'
import { Auth } from 'aws-amplify';
import { Link } from "react-router-dom";
import { Redirect } from "react-router"
import Verify from "./Verify"

class SignUp extends React.Component {
  state = {
    email: '',
    password1: '',
    password2: '',
    toVerify: false,
    code : '',
    success: false
  };

  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  emailChange = (e) => {
    this.setState({email: e.target.value.toLowerCase()});
  }

  passwordChange1 = (e) => {
    this.setState({password1: e.target.value});
  }

  passwordChange2 = (e) => {
    this.setState({password2: e.target.value});
  }

  codeChange = (e) => {
    this.setState({code: e.target.value});
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
      this.setState({toVerify: true})
      console.log(data)
    })
    .catch((err) => {
      if (err.code === 'UsernameExistsException') {
        alert('Email/username already exists');
      }

    });
  }

  handleVerifySubmit = async (e) => {
    e.preventDefault();
    Auth.confirmSignUp(this.state.email, this.state.code, {
    // Optional. Force user confirmation irrespective of existing alias. By default set to True.
    }).then(data => {
      console.log(data);
      if (data === 'SUCCESS') {
        alert('Email confirmed, redirecting to dashboard');
        this.setState({success: true});
      }

    })
    .catch(err => console.log(err));
  }

  render() {
    if (this.state.toVerify === false) {
      if (this.state.success) {
        return (<Redirect to="/" />);
      }
      return (
        <div className="component-main-div">
          <h2> Register New User </h2>
          <form onSubmit={this.handleNewSubmit}>
            <label htmlFor="email">Email</label>
            <input type="text"
              id="emailInput"
              name="email"
              placeholder="Email Address"
              onChange={this.emailChange}/>

            <label htmlFor="password1">Password</label>
            <input type="password"
              id="passwordInput1"
              name="passwordInput1"
              placeholder="Password"
              onChange={this.passwordChange1}/>

          <label htmlFor="password2">Re-enter Password</label>
          <input type="password"
            id="passwordInput2"
            name="passwordInput2"
            placeholder="Re-enter Password"
            onChange={this.passwordChange2}/>
          <input type="submit" value="Submit"  />
        </form>
        </div>
      );
    } else {
      return (
        <Redirect to='/Verify' />
        // <div className="component-main-div">
        //   <h2>Verify email</h2>
        //   <form onSubmit={this.handleVerifySubmit}>
        //   <label htmlFor="code">Verification Code</label>
        //     <input type="password"
        //       id="codeInput"
        //       name="codeInput"
        //       placeholder="Verification Code"
        //       onBlur={this.codeChange}/>
        //     <input type="submit" value="Submit" />
        //   </form>
        //   <p>
        //     <button class="link">Resend confirmation code</button>
        //   </p>
        // </div>
      )
    }
  }
}

//.userConfirmed

export default SignUp;
