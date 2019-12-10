import React from 'react'
import './Header.css'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux';
import { logoutUser } from '../actions/authActions';
import { Dropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';


class Header extends React.Component {
  state = {
    selectedOption: null,
    dropDownValue: 'Select action',
    dropdownOpen: false
  };

  onLogout = (e) => {
    console.log(this.props.isAuthenticated);
    this.props.logoutUser();
  }

  toggle = (e) =>{
        this.setState({
            dropdownOpen: !this.state.dropdownOpen
        });
    }


  render() {
    return (
      <div className={["header", "clearfix"].join(' ')}>
        <div id="header-content">
          <img src={require("../images/epluribusunum.png")} id="logo" alt=''/>
          <h3 className="title">Twitter Political Unifier</h3>

          <div className="header-right">
            <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggle}>
              <DropdownToggle style={{backgroundColor: '#323232', border: 'none'}}>
                <img src={require("../images/threelinebutton.png")} id='three-line' alt=''/>
              </DropdownToggle>
              <DropdownMenu right>
                <DropdownItem><Link className="dropdown-item" to="/home">Home</Link></DropdownItem>
                <DropdownItem><Link className="dropdown-item" to="/dashboard">Dashboard</Link></DropdownItem>
                <DropdownItem><Link className="dropdown-item" to="/about">About</Link></DropdownItem>
                <DropdownItem>{
                  this.props.isAuthenticated ?
                  <Link className="dropdown-item" to="/" onClick={this.onLogout}>Logout</Link>
                  : <Link className="dropdown-item" to="/login">Login/Register</Link>
                }</DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated
})

export default connect(mapStateToProps, { logoutUser })(Header);
