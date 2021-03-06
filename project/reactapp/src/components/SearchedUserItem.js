import React from 'react'
import ReactTooltip from 'react-tooltip'

class SearchedUserItem extends React.Component {
  state = {
    users: []
  }

  componentDidMount() {

  }

  render() {
    let screen_name = this.props.user.screenName;
    let formattedDate = null
    if (this.props.user.searchDate) {
      let date = new Date(this.props.user.searchDate)
      formattedDate = formatDate(date)
    }
    let location = this.props.user.location
    let inProgress = this.props.user.inProgress

    if (inProgress) {
      return (
        <tr>
          <td className='user-td'><a href={'https://www.twitter.com/' + screen_name}> {'@' + screen_name} </a></td>
          {
            formattedDate ? <td className='user-td'>{formattedDate}</td> : null
          }

          <td className='user-td'>{location}</td>
          {
            <td className='user-td' data-tip="Refresh to check if analysis is finished">
              In progress...
              <ReactTooltip place="top" type="dark" effect="solid"/>
            </td>
          }
        </tr>
      )
    } else {
      return (
        <tr>
          <td className='user-td'><a href={'https://www.twitter.com/' + screen_name}> {'@' + screen_name} </a></td>
          {
            formattedDate ? <td className='user-td'>{formattedDate}</td> : null
          }

          <td className='user-td'>{location}</td>
          {
            this.props.user.polLabel === 'N/A' ?
                <td className='user-td' data-tip="User does not have any tweets">
                  {this.props.user.polLabel}
                  <ReactTooltip place="top" type="dark" effect="solid"/>
                </td>
              : <td className='user-td'>{this.props.user.polLabel}</td>
          }
        </tr>
      )
    }
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
