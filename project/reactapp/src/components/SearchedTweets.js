import React from 'react';
import axios from 'axios';
import { connect } from 'react-redux';
import SearchedTweetItem from './SearchedTweetItem';

class SearchedTweets extends React.Component {
  state = {
    tweets: []
  }

  componentDidMount() {
    const url = 'https://www.knownastron.com:6001/api/2.0/getsearchedtweets';
    //const url = 'http://127.0.0.1:5000/api/2.0/getsearchedtweets';

    let self = this;
    axios.post(url, JSON.stringify({
      'token': this.props.token,
      'email': this.props.email
    }), {headers: {'Content-Type': 'application/json;charset=UTF-8'}})
    .then(function(response) {
      if (response.data.statusCode === 401) {
        alert(response.data.message)
      }
      self.setState({tweets: response.data.searchedTweets})
    })
    .catch(function (error) {
      console.log(error)
      alert('Something went wrong. Please try again')
    });


  }

  render() {
    return (
      <div className="component-main-div">
        <h2> Searched Tweet History </h2>
        <div className='center-single'>
          <table className="main-table">
              <tbody>
                <tr>
                  <th className='user-th'>Author</th>
                  <th className='user-th'>Tweet</th>
                  <th className='user-th'>Date Searched</th>
                  <th className='user-th'>Status</th>
                </tr>
                {
                  this.state.tweets.map((tweet) => (
                    <SearchedTweetItem key={tweet.id} tweet={tweet} />
                  ))
                }
            </tbody>
          </ table>
      </div>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated,
  email: state.auth.email,
  token: state.auth.token
})



export default connect(mapStateToProps, { }) (SearchedTweets);
