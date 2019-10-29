import React from 'react'

class SignUp extends React.Component {
  state = {
    email: '',
    password1: '',
    password2: ''
  };

  validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  }

  emailChange = (e) => {
    this.setState({email: e.target.value});
  }

  passwordChange1 = (e) => {
    this.setState({password1: e.target.value});
  }

  passwordChange2 = (e) => {
    this.setState({password2: e.target.value});
  }

  submission = (e) => {
    if (this.password1 !== this.password2) {
      alert("Passwords do not match");
    }

    if (!this.validateEmail(this.email)) {
      alert("Invalid email");
    }

    e.preventDefault();
  }

  render() {
    return (
      <div className="component-main-div">
        <h2> Register User </h2>
        <form onSubmit={this.submission}>
          <label htmlFor="email">Email</label>
          <input type="text"
            id="emailInput"
            name="email"
            placeholder="Email Address"
            onBlur={this.emailChange}/>

          <label htmlFor="password1">Password</label>
          <input type="password"
            id="passwordInput1"
            name="passwordInput1"
            placeholder="Password"
            onBlur={this.passwordChange1}/>

        <label htmlFor="password2">Re-enter Password</label>
        <input type="password"
          id="passwordInput2"
          name="passwordInput2"
          placeholder="Re-enter Password"
          onBlur={this.passwordChange2}/>
        <input type="submit" value="Submit"  />
      </form>
      </div>
    );
  }
}

export default SignUp;
