import React from 'react'
import { connect } from 'react-redux';
import { Redirect } from 'react-router';
import SearchedUsers from './SearchedUsers'
import SearchedTweets from './SearchedTweets'

class Dashboard extends React.Component {

  render() {

    if (this.props.isAuthenticated) {
      return (
        <div>
          <SearchedUsers />
          <SearchedTweets />
        </div>
      );
    } else {
      return (<Redirect to='/login' />)
    }
  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated,
  token: state.auth.token
})

export default connect(mapStateToProps, {}) (Dashboard);
