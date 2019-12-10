import React from 'react'
import LabelTweet from './LabelTweet';
import LabelUser from './LabelUser'
import { connect } from 'react-redux';
import { Redirect } from 'react-router';

class Home extends React.Component {

  render() {
      return (
          <div className="home">
              <LabelTweet />
              <LabelUser />
          </div>
      );
  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated,
  token: state.auth.token
})

export default connect(mapStateToProps, {}) (Home);
