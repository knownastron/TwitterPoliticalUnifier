import React from 'react';
import axios from 'axios';
import { connect } from 'react-redux';
import SearchedUserItem from './SearchedUserItem';
import { TwitterTweetEmbed } from 'react-twitter-embed'
import config from '../config/config';
import { Map, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

const gop = new L.Icon({
    iconUrl: require('../images/gop.png'),
    iconRetinaUrl: require('../images/gop.png'),
    iconAnchor: null,
    popupAnchor: null,
    shadowUrl: null,
    shadowSize: null,
    shadowAnchor: null,
    iconSize: new L.Point(20, 18),
    className: 'leaflet-div-icon'
});

const dem = new L.Icon({
    iconUrl: require('../images/dem.png'),
    iconRetinaUrl: require('../images/dem.png'),
    iconAnchor: null,
    popupAnchor: null,
    shadowUrl: null,
    shadowSize: null,
    shadowAnchor: null,
    iconSize: new L.Point(20, 20),
    className: 'leaflet-div-icon'
});

const na = new L.Icon({
    iconUrl: require('../images/questionmark.png'),
    iconRetinaUrl: require('../images/questionmark.png'),
    iconAnchor: null,
    popupAnchor: null,
    shadowUrl: null,
    shadowSize: null,
    shadowAnchor: null,
    iconSize: new L.Point(19, 19),
    className: 'leaflet-div-icon'
});

class TweetDetails extends React.Component {
  state = {
    users: [],
    locations: [],
    userInfoWithGeo: [],
    lat: 39.8283,
    lng: -98.5795,
    zoom: 4
  }

  componentDidMount() {
    this.getTwitterUsers()
  }

  getGeoLocations = async (locations) => {
    const codioUrl = 'https://api.geocod.io/v1.4/geocode?';
    return axios.post(codioUrl + 'api_key=' + config.geocodio.KEY,
        JSON.stringify(locations),
        {headers: {'Content-Type': 'application/json;charset=UTF-8'}}
      ).then(function(response) {
        let geo_locations = [];
        response.data.results.forEach(function(geo) {
          if (geo.response.error) {
            geo_locations.push({'error': 'error'})
          } else {
            if (geo.response.results[0]) {
              geo_locations.push(geo.response.results[0].location)
            }
          }
        }
      )
      return geo_locations;
      })
  }

  getTwitterUsers = async () => {
    // const url = 'http://127.0.0.1:5000/api/2.0/gettweetlikes';
    const url = 'https://www.knownastron.com:6001/api/2.0/gettweetlikes';

    await axios.post(url, JSON.stringify({
      'token': this.props.token,
      'tweetId': this.props.match.params.id,
      'email': this.props.email
    }), {headers: {'Content-Type': 'application/json;charset=UTF-8'}})
	  .then((response) => {
	      console.log(response.data.tweetLikes);
	      this.setState({users: response.data.tweetLikes})
	  })
    .catch((error) => {
      console.log(error)
    });

    // gather all the locations and usernames
    let userInfo = []
    let locations = []
    this.state.users.forEach(function(user){
      if (user.location !== '') {
        userInfo.push([user.screenName, user.polLabel])
        locations.push(user.location)
      }
    })

    // get geo location
    let userInfoAndGeo = [];
    await this.getGeoLocations(locations)
      .then(locations => {
        userInfoAndGeo = locations.map((loc, i) => {
          return {screenName: userInfo[i][0],
                   polLabel: userInfo[i][1],
                   coordinates: loc};
        })
      })
    console.log(userInfoAndGeo);
    this.setState({userInfoWithGeo: userInfoAndGeo})
  }



  render() {
    const position = [this.state.lat, this.state.lng];
    return (
      <div className="component-main-div">


        <h1>Tweet Details</h1>
        <div className="tweet-embed">
          <TwitterTweetEmbed tweetId={this.props.match.params.id}/>
        </div>
        <div className='center-single'>
          <table className="tweet-detail-table">
              <tbody>
                <tr>
                  <th className='user-th'>Username</th>
                  <th className='user-th'>Location</th>
                  <th className='user-th'>Political Prediction</th>
                </tr>
                {
                  this.state.users.map((user) => (
                    <SearchedUserItem key={user.id} user={user} />
                  ))
                }
            </tbody>
          </table>
        </div>
        <div className='center-single'>
          <Map className="map" center={position} zoom={this.state.zoom}>
            <TileLayer
              attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
              url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'/>
            {
              this.state.userInfoWithGeo.map((curUser, i) => {
                if (!curUser.coordinates.error) {
                  switch(curUser.polLabel) {
                    case 'conservative':
                      return <Marker key={i} icon={gop} position={[curUser.coordinates.lat, curUser.coordinates.lng]}>
                              {// <Popup>
                              //   <img src='threelinebutton.png'></img>
                              // </Popup>
                              }
                            </Marker>
                    case 'liberal':
                      return <Marker key={i} icon={dem} position={[curUser.coordinates.lat, curUser.coordinates.lng]}>
                              {// <Popup>
                              //   <img src='threelinebutton.png'></img>
                              // </Popup>
                              }
                            </Marker>
                    default:
                      return <Marker key={i} icon={na} position={[curUser.coordinates.lat, curUser.coordinates.lng]}>
                              {// <Popup>
                              //   <img src='threelinebutton.png'></img>
                              // </Popup>
                              }
                            </Marker>
                  }
              } else {
                return null;
              }
            })
            }
          </Map>
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



export default connect(mapStateToProps, { }) (TweetDetails);
