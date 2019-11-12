import React from 'react';
import axios from 'axios';
import SearchedUserItem from './SearchedUserItem';

class SearchedUsers extends React.Component {
  state = {
    users: []
  }
  componentDidMount() {
    const url = 'http://127.0.0.1:5000/api/2.0/getsearchedusers';
    let self = this;
    axios.post(url, JSON.stringify({
      // 'token': token
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
        <h1> Searched Users History </h1>
        {
          this.state.users.map((user) => (
            <SearchedUserItem key={user.id} user={user} />
            // <h3 key={user.id}> {user.screenName} , {user.searchDate} </h3>
          ))
        }
      </div>
    )
  }
}

export default SearchedUsers;
