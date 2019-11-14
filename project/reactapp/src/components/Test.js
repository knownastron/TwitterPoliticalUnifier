import React from 'react';
import { Auth } from 'aws-amplify';
import { TwitterTweetEmbed } from 'react-twitter-embed'

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
      <div id="test-div">
        <TwitterTweetEmbed options={
            {
              width: 300,
              cards: 'hidden'
            }
          }
          tweetId={'1000000245584072704'}
        />
        <TwitterTweetEmbed
          tweetId={'1194120382413803520'}
          options={
              {
                width: 300,
                cards: 'hidden'
              }
            }
        />
      </div>
    );
  };
}

var muh_style = {'height': '100px'}

export default Test;
