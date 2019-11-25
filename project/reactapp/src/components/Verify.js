import React from 'react'
import { Auth } from "aws-amplify";
import { Redirect } from 'react-router';
import { connect } from 'react-redux';
import { resetConfirmation } from '../actions/authActions'


class Verify extends React.Component {
  state = {
    email: '',
    code: '',
    success: false
  };

  componentDidMount() {
    // reset user_not_confirmed
    this.props.resetConfirmation()
  }

  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  onChange = (e) => {
    this.setState({[e.target.name] : e.target.value})
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
    if (this.state.email.length === 0) {
      alert("Email/username cannot be empty");
      return
    }

    if (!this.validateEmail(this.state.email)) {
      alert("Invalid email");
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
              value={this.props.email}
              onChange={this.onChange}/>

            <label htmlFor="code">Verification Code</label>
            <input type="password"
              id="codeInput"
              name="code"
              placeholder="Verification Code"
              onChange={this.onChange}/>
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

const mapStateToProps = state => ({
  email: state.auth.email
})

export default connect(mapStateToProps, { resetConfirmation })(Verify);
