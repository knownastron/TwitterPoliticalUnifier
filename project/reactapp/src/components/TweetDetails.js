import React from 'react';
import axios from 'axios';
import { connect } from 'react-redux';
import SearchedUserItem from './SearchedUserItem';
import { TwitterTweetEmbed } from 'react-twitter-embed'

class TweetDetails extends React.Component {
  state = {
    users: []
  }
  componentDidMount() {
    const url = 'http://127.0.0.1:5000/api/2.0/gettweetlikes';
    let self = this;
    axios.post(url, JSON.stringify({
      // 'token': token
      // 'email': this.props.email
      'tweetId': this.props.match.params.id,
      'email': 'knownastron@gmail.com'
    }), {headers: {'Content-Type': 'application/json;charset=UTF-8'}})
    .then(function(response) {
      console.log(response.data.searchedUsers)
      self.setState({users: response.data.tweetLikes})
    })
    .catch(function (error) {
      console.log(error)
    });
  }

  render() {
    return (

      <div className="component-main-div">

        <h1>Tweet Details for:</h1>
          <div style={{display:'flex',justifyContent:'center'}}>
            <TwitterTweetEmbed tweetId={this.props.match.params.id}/>
          </div>
          <table className="tweet-detail-table">
              <tbody>
                <tr>
                  <th className='user-th'>Username</th>
                  <th className='user-th'>Location</th>
                  <th className='user-th'>Political Prediction</th>
                </tr>
                {
                  this.state.users.map((user) => (
                    <SearchedUserItem key={user.id} user={user} />
                  ))
                }
            </tbody>
          </table>

      </div>
    )
  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated,
  email: state.auth.email,
  token: state.auth.token
})



export default connect(mapStateToProps, { }) (TweetDetails);
