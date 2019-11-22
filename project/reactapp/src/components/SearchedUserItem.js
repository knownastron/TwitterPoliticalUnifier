import React from 'react'

class SearchedUserItem extends React.Component {
  state = {
    users: []
  }

  componentDidMount() {

  }

  render() {
    let screen_name = this.props.user.screenName;
    let date = new Date(this.props.user.searchDate)
    let location = this.props.user.location
    let formattedDate = formatDate(date)
    return (
        <tr>
          <td className='user-td'><a href={'https://www.twitter.com/' + screen_name} > {'@' + screen_name} </a></td>
          <td className='user-td'>{formattedDate}</td>
          <td className='user-td'>{location}</td>
          <td className='user-td'>{this.props.user.polLabel}</td>
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



export default SearchedUserItem;
