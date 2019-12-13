import React from 'react';
import { Auth } from 'aws-amplify';
import { Map, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css';
// import 'leaflet/dist/leaflet.css';
// const { MLeafletMap, TileLayer, Marker, Popup } = ReactLeaflet
import L from 'leaflet';
import SearchedTweets from './SearchedTweets';
import LabelUser from './LabelUser'
import ReactTooltip from 'react-tooltip'

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

class Test extends React.Component {
  constructor() {
    super()
    this.state = {
      lat: 39.8283,
      lng: -98.5795,
      zoom: 4
    }
  }

  render() {
    const position = [this.state.lat, this.state.lng];
    return (
      <div>
        <table className="main-table">
            <tbody>
              <tr>
                <th className='user-th'>Username</th>
                <th className='user-th'>Date Searched</th>
                <th className='user-th'>Location</th>
                <th className='user-th'>Political Prediction</th>
              </tr>
            <tr>
              <td><a>duhhello1</a></td>
              {
                <td className='user-td'>date</td>
              }

              <td className='user-td'>location</td>
                <td className='user-td' data-tip="React-tooltip">duuhello</ td>
                <ReactTooltip place="top" type="dark" effect="solid"/>

            </tr>
          </tbody>
        </ table>
      </div>
    );
  }
}

var muh_style = {'height': '400px', width: '100%'}

export default Test;
