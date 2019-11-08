import React from 'react'
import './LabelTweet.css'
import { connect } from 'react-redux';

class LabelUser extends React.Component {
  state = {
    email: '',
    username: ''
  };

  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  submission = (e) => {
    let token = this.props.token;
    e.preventDefault();
    console.log('yaaaa');
    if (this.validateEmail(this.state.email)) {

      const url = 'http://127.0.0.1:5000/api/1.0/labeluser';
      const xhr = new XMLHttpRequest();
      xhr.open('POST', url);
      xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      xhr.send(JSON.stringify({...this.state, token}));

      xhr.onload = (e) => {
        console.log(xhr.responseText)
      }

      xhr.onerror = (e) => {
        console.log('error!')
      }


    } else {
      alert('Email error');
    }

  }

  emailChange = (e) => {
    this.setState({email: e.target.value});
  }

  usernameChange = (e) => {
    this.setState({username: e.target.value});
  }

  render() {
    return (
      <div className="component-main-div">
        <h2> Label User </h2>
        <form onSubmit={this.submission}>
          <label htmlFor="email">Email</label>
          <input type="text"
            id="emailInput"
            name="email"
            placeholder="Email Address"
            onBlur={this.emailChange}/>

          <label htmlFor="username">Twitter Username</label>
          <input type="text"
            id="username"
            name="tweeturl"
            placeholder="Twitter handle"
            onBlur={this.usernameChange}/>

          <input type="submit" value="Submit" />
        </form>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated,
  token: state.auth.token
})

export default connect(mapStateToProps, {})(LabelUser);
