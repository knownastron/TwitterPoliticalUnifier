import React from 'react'
import './LabelTweet.css'
import { connect } from 'react-redux';
import { Redirect } from 'react-router';
import axios from 'axios';

class LabelUser extends React.Component {
  state = {
    username: '',
    redirectToLogIn: false,
    redirectToDashboard: false
  };

  submission = (e) => {
    e.preventDefault();

    if (!this.props.isAuthenticated) {
      alert('Please log in to use this feature.');
      this.setState({redirectToLogIn: true})
      return;
    }


    const url = 'https://www.knownastron.com:6001/api/2.0/labeluser';
    // const url = 'http://127.0.0.1:5000/api/2.0/labeluser';

    axios.post(url, JSON.stringify({
      'username': this.state.username,
      'token': this.props.token,
      'email': this.props.email
    }), {headers: {'Content-Type': 'application/json;charset=UTF-8'}})
    .then((response) => {
      this.setState({redirectToDashboard: true})
      console.log(response)
    })
    .catch(function (error) {
      console.log(error)
    });
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
    if (this.state.redirectToLogIn) {
      return (<Redirect to='/login' />);
    } else if (this.state.redirectToDashboard) {
      return (<Redirect to='/dashboard' />);
    }
    return (
      <div className="component-half-div">
        <h2> Twitter User's Political Affiliation </h2>
        <p> Discover a Twitter user's political leanings <br/> based on their tweet history</p>
        <form onSubmit={this.submission}>
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
  token: state.auth.token,
  email: state.auth.email
})

export default connect(mapStateToProps, {})(LabelUser);
