import React from 'react'


class About extends React.Component {

  render() {
    return (
      <div className="component-main-div">
        <div style={{'width': '50%',
                      'justify-content': 'center',
                      'display': 'inline-block'}}>
          <p> Political polarization has increased to concerning levels in
          America today. A striking 91% of people said in a PRRI survey that the
          country is divided over politics. </p>
          <p> The effects of polarization can be seen in federal government where
          compromise is rare leading to deadlock in Washington. The effects can
          also be seen in our steets where political violence is becoming more
          frequent. </p>
          <p> Americans needs hear messages that can unite, rather than the much
          more common messages intended to divide. Use Twitter Political Unifier
          to discover messages that can appeal to Americans across the poltical
          landscape. </p>
        <br />
        <h3><i>"E Pluribus Unum" - "From many, One"</i></h3>
        </div>
      </div>
    );
  }
}

export default About;
