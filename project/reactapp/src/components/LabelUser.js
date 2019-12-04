import React from 'react'
import './LabelTweet.css'
import { connect } from 'react-redux';
import axios from 'axios';

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

    if (this.validateEmail(this.state.email)) {

      // const url = 'https://www.knownastron.com:6001/api/2.0/labeluser';
      const url = 'http://127.0.0.1:5000/api/2.0/labeluser';

      axios.post(url, JSON.stringify({
        ...this.state,
        'token': token
      }), {headers: {'Content-Type': 'application/json;charset=UTF-8'}})
      .then(function(response) {
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      });

    } else {
      alert('Email error');
    }

  }

  emailChange = (e) => {
    this.setState({email: e.target.value});
  }

  usernameChange = (e) => {
    let new_username = e.target.value;
    if (new_username.charAt(0) === '@') {
      new_username = new_username.slice(1)
    }
    this.setState({username: new_username});
  }

  render() {
    return (
      <div className="component-main-div">
        <h2> Twitter User's Political Affiliation </h2>
        <p> Discover a Twitter user's political leanings <br/> based on their tweet history</p>
        <form onSubmit={this.submission}>
          <label htmlFor="email">Email</label>
          <input type="text"
            id="emailInput"
            name="email"
            placeholder="Email Address"
            onChange={this.emailChange}/>
          <label htmlFor="username">Twitter Username</label>
          <input type="text"
            id="username"
            name="tweeturl"
            placeholder="ex) @realdonaldtrump"
            onChange={this.usernameChange}/>
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
