import React from 'react'

class SearchedUserItem extends React.Component {
  state = {
    users: []
  }

  componentDidMount() {
    // const url = 'http://127.0.0.1:5000/api/2.0/getsearchedusers';
    // let self = this;
    // axios.post(url, JSON.stringify({
    //   // 'token': token
    //   'email': 'knownastron@gmail.com'
    // }), {headers: {'Content-Type': 'application/json;charset=UTF-8'}})
    // .then(function(response) {
    //   console.log(response.data.searchedUsers)
    //   self.setState({users: response.data.searchedUsers})
    // })
    // .catch(function (error) {
    //   console.log(error)
    // });
  }

  render() {
    return (
      <div className='searched-user-item-div'>
        <a href={'twitterUser/' + this.props.user.screenName}> {this.props.user.screenName} </a><h5>{this.props.user.searchDate} </h5>
      </div>
    )
  }
}

export default SearchedUserItem;
