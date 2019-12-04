import React from 'react';
import axios from 'axios';
import { connect } from 'react-redux';
import SearchedUserItem from './SearchedUserItem';

class SearchedUsers extends React.Component {
  state = {
    users: []
  }
  componentDidMount() {
    // const url = 'https://www.knownastron.com:6001/api/2.0/getsearchedusers';
    const url = 'http://127.0.0.1:5000/api/2.0/getsearchedusers';
    let self = this;
    axios.post(url, JSON.stringify({
      // 'token': token
      // 'email': this.props.email
      'email': 'knownastron@gmail.com'
    }), {headers: {'Content-Type': 'application/json;charset=UTF-8'}})
    .then(function(response) {
      console.log(response.data.searchedUsers)
      self.setState({users: response.data.searchedUsers})
    })
    .catch(function (error) {
      console.log(error)
    });
  }

  render() {
    return (
      <div className="component-main-div">
        <h2> Searched Users History </h2>
        <div className='center-single'>
          <table className="user-table">
              <tbody>
                <tr>
                  <th className='user-th'>Username</th>
                  <th className='user-th'>Date Searched</th>
                  <th className='user-th'>Location</th>
                  <th className='user-th'>Political Prediction</th>
                </tr>
                {
                  this.state.users.map((user) => (
                    <SearchedUserItem key={user.id} user={user} />
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



export default connect(mapStateToProps, { }) (SearchedUsers);
