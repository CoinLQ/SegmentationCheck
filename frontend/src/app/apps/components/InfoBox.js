import React from "react";

class InfoBox extends React.Component {
    render() {
        const {children, boxBg, iconClass, textInfo} = this.props;

        return (
            <div className="col-md-3 col-sm-6 col-xs-6">
              <div className="info-box">
                <span className={`info-box-icon ${boxBg}`}><i className={`ion ${iconClass}`}></i></span>
                <div className="info-box-content">
                  <span className="info-box-text">{textInfo}</span>
                  {children}
                </div>
              </div>
            </div>
        );
    }
}

export default InfoBox;