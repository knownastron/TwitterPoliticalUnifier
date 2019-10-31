import React from 'react'
import { Auth } from "aws-amplify";
import { Redirect } from 'react-router';


class Verify extends React.Component {
  state = {
    email: '',
    code: '',
    success: false
  };

  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  emailChange = (e) => {
    this.setState({email: e.target.value});
  }

  codeChange = (e) => {
    this.setState({code: e.target.value})
  }

  handleSubmit = async (e) => {
    e.preventDefault();

    Auth.confirmSignUp(this.state.email, this.state.code, {
    // Optional. Force user confirmation irrespective of existing alias. By default set to True.
    }).then(data => {
      console.log(data);
      if (data === 'SUCCESS') {
        alert('Email confirmed, redirecting to dashboard');
        this.setState({success: true})
      }

    })
    .catch(err => console.log(err));
  }

  resendCode = async (e) => {
    if (this.state.email.length == 0) {
      alert("Email/username cannot be empty");
      return
    }
    Auth.resendSignUp(this.state.email)
    .then(() => {
      console.log('code resent successfully');})
    .catch(err => {
      console.log(err);
    });
  }

  render() {
    if (this.state.success === false) {
      return (
        <div className="component-main-div">
          <h2> Verify Email </h2>
          <form onSubmit={this.handleSubmit}>
            <label htmlFor="email">Email</label>
            <input type="text"
              id="emailInput"
              name="email"
              placeholder="Email Address"
              onBlur={this.emailChange}/>

            <label htmlFor="code">Verification Code</label>
            <input type="password"
              id="codeInput"
              name="codeInput"
              placeholder="Verification Code"
              onBlur={this.codeChange}/>
            <input type="submit" value="Submit" />
          </form>
          <p>

            <button className="link" onClick={this.resendCode}>Resend confirmation code</button>
          </p>
        </div>
      );
    } else {
      return (
        <Redirect to="/" />
      )
    }

  }
}

export default Verify;
