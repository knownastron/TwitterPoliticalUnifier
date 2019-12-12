import React from 'react'
import { Auth } from "aws-amplify";
import { Redirect } from 'react-router';
import { connect } from 'react-redux';
import { resetConfirmation } from '../actions/authActions';
import axios from 'axios';


class Verify extends React.Component {
  state = {
    email: '',
    code: '',
    success: false
  };

  componentDidMount() {
    // reset user_not_confirmed
    if (this.props.location.state) {
      this.setState({email: this.props.location.state.email})
    }
    this.props.resetConfirmation();
  }

  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  onChange = (e) => {
    this.setState({[e.target.name] : e.target.value})
  }

  handleSubmit = async (e) => {
    e.preventDefault();

    await Auth.confirmSignUp(this.state.email, this.state.code, {
    // Optional. Force user confirmation irrespective of existing alias. By default set to True.
    }).then(data => {
      console.log(data);
      if (data === 'SUCCESS') {
        this.createNewUser(this.state.email);
        this.setState({success: true});
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

  createNewUser = async (email) => {
    //const url = 'http://127.0.0.1:5000/api/2.0/createnewuser';
    const url = 'https://www.knownastron.com:6001/api/2.0/createnewuser';

    await axios.post(url, JSON.stringify({
      email: this.state.email,
    }), {headers: {'Content-Type': 'application/json;charset=UTF-8'}})
    .then((response) => {
      // console.log(response)
    })
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
              value={this.state.email}
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
        <Redirect to="/home" />
      )
    }
  }
}

const mapStateToProps = state => ({
  email: state.auth.email
})

export default connect(mapStateToProps, { resetConfirmation })(Verify);
