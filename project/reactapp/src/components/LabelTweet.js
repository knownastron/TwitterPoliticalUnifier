import React from 'react'
import './LabelTweet.css'
import { connect } from 'react-redux';
import { Redirect } from 'react-router';
import axios from 'axios';

class LabelTweet extends React.Component {
  state = {
    tweeturl: '',
    redirectToLogIn: false,
    redirectToDashboard: false
  };

  onChange = (e) => {
    this.setState({[e.target.name] : e.target.value})
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
    if (!this.props.isAuthenticated) {
      this.setState({redirectToLogIn: true})
      alert('Please log in to use this feature.');
      return;
    }
    if (!this.validateTweetUrl(this.state.tweeturl)) {
      alert('Invalid tweet url');
    }

    // const url = 'https://www.knownastron.com:6001/api/2.0/labeltweet';
    const url = 'http://127.0.0.1:5000/api/2.0/labeltweet';

    axios.post(url, JSON.stringify({
        ...this.state,
        token: this.props.token,
        email: this.props.email,
        tweetId: this.state.tweeturl.split('/')[5]
    }), {headers: {'Content-Type': 'application/json;charset=UTF-8'}})
    .then((response) => {
      this.setState({redirectToDashboard: true})
      console.log(response);
    })
  }

  render() {
    if (this.state.redirectToLogIn) {
      return (<Redirect to='/login' />);
    } else if (this.state.redirectToDashboard) {
      return (<Redirect to='/dashboard' />);
    }
    return (
      <div className="component-half-div">
        <h2> Tweet Polarization </h2>
        <p> Discover a Tweet's polarization based on the users who liked the tweet</p>
        <form onSubmit={this.submission}>

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
  token: state.auth.token,
  email: state.auth.email
})

export default connect(mapStateToProps, {}) (LabelTweet);
