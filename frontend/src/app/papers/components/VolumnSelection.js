import React from "react";
import ReactDOM from "react-dom";
import classnames from "classnames";
import TriMenu from "./TriMenu"
import VolumeMenu from "./VolumeMenu"
class VolumnSelection extends React.Component {
    constructor(props) {
        super(props);
        this.state = { current_tri: 0,
                       current_vol: 0,
                     };
    }

    componentDidMount() {
    }

    triChanged = (id) => {
        this.setState({current_tri: id})
    }

    volChanged = (id) => {
        this.setState({current_vol: id})
    }

    render() {
        return (
            <div {...this.props}>
                <div id="HContents" style={{marginLeft: 40}} ref='area'>
                    <TriMenu triChanged={this.triChanged}/>
                    <VolumeMenu volChanged={this.volChanged}/>
                </div>
                <div id="HColNum">
                <input type="text" className="text number" required="required" pattern="" />
                <a href="javascript:;" className="btn glow" style={{marginTop: -10}} data-tooltip="跳转">
                <span className="text hideText">跳转</span>
                <span className="fa fa-arrow-right" style={{color: 'red'}}></span></a>
            </div>
            </div>
        );
    }
}


export default VolumnSelection;


