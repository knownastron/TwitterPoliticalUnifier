import React from 'react'
import './TweetInputForm.css'

class TweetInputForm extends React.Component {
  state = {
    email: '',
    tweeturl: ''
  };


  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  submission = (e) => {
    console.log('yaaaa');
    if (this.validateEmail(this.state.email)) {
      alert('Email validated');
    } else {
      alert('Email error');
    }
    e.preventDefault();
  }

  emailChange = (e) => {
    this.setState({email: e.target.value});
  }

  render() {
    return (
      <div className="form-parent">
        <form onSubmit={this.submission}>
          <label htmlFor="email">Email</label>
          <input type="text"
            id="emailInput"
            name="email"
            placeholder="your email address"
            onBlur={this.emailChange}/>

          <label htmlFor="tweeturl">Tweet URL</label>
          <input type="text" id="tweet-url" name="tweeturl" placeholder="ex) https://twitter.com/username/status/1183390085993119749" />

          <input type="submit" value="Submit" />
        </form>
      </div>
    );
  }
}

export default TweetInputForm;
