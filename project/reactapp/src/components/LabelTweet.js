import React from 'react'
import './LabelTweet.css'
import { connect } from 'react-redux';
import axios from 'axios';

class LabelTweet extends React.Component {
  state = {
    email: '',
    tweeturl: ''
  };

  onChange = (e) => {
    this.setState({[e.target.name] : e.target.value})
  }

  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  validateTweetUrl = (tweeturl) => {
    // must have twitter.com, username, status, and a number
    var isnum = /^\d+$/;
    let splitUrl = this.state.tweeturl.split('/')
    if (splitUrl[0] === 'https:' &&
      splitUrl[2] === 'twitter.com' &&
      splitUrl[4] === 'status' && isnum.test(splitUrl[5])) {
        return true;
      }
    return false;
  }

  submission = (e) => {
    e.preventDefault()
    if (!this.validateTweetUrl(this.state.tweeturl)) {
      alert('Invalid tweet url')
    }

    if (!this.validateEmail(this.state.email)) {
      alert('Invalid email')
    }

    let token = this.props.token;
    const url = 'http://127.0.0.1:5000/api/2.0/labeltweet';

    axios.post(url, JSON.stringify({
        ...this.state,
        token: token,
        username: this.state.email,
        tweetId: this.state.tweeturl.split('/')[5]
    }), {headers: {'Content-Type': 'application/json;charset=UTF-8'}})
    .then(function(response) {
      console.log(response)
    })
  }

  emailChange = (e) => {
    this.setState({email: e.target.value});
  }

  render() {
    return (
      <div className="component-main-div">
        <h2> Label Tweet </h2>
        <form onSubmit={this.submission}>
          <label htmlFor="email">Email</label>
          <input type="text"
            id="emailInput"
            name="email"
            placeholder="your email address"
            onChange={this.onChange}/>

          <label htmlFor="tweeturl">Tweet URL</label>
          <input type="text"
            id="tweet-url"
            name="tweeturl"
            placeholder="ex) https://twitter.com/username/status/1183390085993119749"
            onChange={this.onChange}/>

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

export default connect(mapStateToProps, {}) (LabelTweet);
