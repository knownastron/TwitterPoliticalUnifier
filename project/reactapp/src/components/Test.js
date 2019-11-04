import React from 'react';
import { Auth } from 'aws-amplify';

class Test extends React.Component {
  onClick = (e) => {
    e.preventDefault();
    Auth.currentAuthenticatedUser({
      bypassCache: false
    }).then(user => console.log(user))
    .catch(err => console.log(err));
  }

  render() {
    return (
      <div className="component-main-div">
        <button type="button" onClick={this.onClick}> CLICK</button>
      </ div>
    );
  };
}

export default Test;
