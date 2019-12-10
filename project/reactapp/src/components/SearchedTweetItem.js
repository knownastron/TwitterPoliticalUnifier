import React from 'react';
import {
  Link
} from "react-router-dom";
import ReactTooltip from 'react-tooltip';

class SearchedTweetItem extends React.Component {
  state = {
    tweets: []
  }

  componentDidMount() {

  }

  render() {
    let screen_name = this.props.tweet.screenName;
    let tweetId = this.props.tweet.tweetId
    let date = new Date(this.props.tweet.searchDate)
    let formattedDate = formatDate(date)
    let inProgress = this.props.tweet.inProgress
    return (
        <tr>
          <td className='user-td'><a href={'https://www.twitter.com/' + screen_name} > {'@' + screen_name} </a></td>
          <td className='user-td'><a href={'https://twitter.com/' + screen_name + '/status/' + tweetId}>Go to Tweet</a></td>
          <td className='user-td'>{formattedDate}</td>
          {
            inProgress ?
              <td className='user-td' data-tip="Refresh to check if analysis is finished">
                In progress...
                <ReactTooltip place="top" type="dark" effect="solid"/>
              </td>
            :
            <td className='user-td'>
              <Link to={'/tweetdetails/' + tweetId}>Details</Link>
            </td>
          }
        </tr>
    )
  }
}

function formatDate(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = hours + ':' + minutes + ' ' + ampm;
  let month = date.getMonth()+1
  month = (month < 10 ? '0' + month.toString() : month);
  let day = date.getDate()
  day = (day < 10 ? '0' + day.toString() : day)
  return month + "/" + day + "/" + date.getFullYear() + "  " + strTime;
}



export default SearchedTweetItem;
