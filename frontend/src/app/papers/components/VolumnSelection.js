import React from "react";


class VolumnSelection extends React.Component {
    componentDidMount() {
    }


    render() {
        const {children} = this.props;
        return (
            <div {...this.props}>
            <div id="HContents" style={{marginLeft: 46}}>
                <div className="dropdown">
                    <a id="HCteTri" href="javascript:;" className="whiteBackground glow" type="button" data-toggle="dropdown">
                    <span className="text">洪<span className="whiteSpace">
                    </span>武南藏</span><span className="triangle"></span>
                    </a>
                    <ul className="dropdown-menu">
                        <li>
                            <a href="javascript:;">高丽藏</a>
                        </li>
                        <li>
                            <a href="javascript:;">赵城金藏</a>
                        </li>
                        <li className="disabled"><a href="javascript:;">洪武南藏</a></li>
                        <li role="separator" className="divider"></li>
                        <li>
                            <a href="javascript:;">其他</a>
                        </li>
                    </ul>
                </div>
                <div id="HCteVolCt" className="dropdown"><a id="HCteVol" href="javascript:;" className="whiteBackground glow" type="button" data-toggle="dropdown"><span className="text number">17</span><span className="triangle"></span></a><span>册</span>
                    <ul className="dropdown-menu">
                        <li className="disabled"><a href="javascript:;" className="number">17</a></li>
                        <li><a href="javascript:;" className="number">18</a></li>
                        <li><a href="javascript:;" className="number">19</a></li>
                    </ul>
                </div>
            </div>
            </div>
        );
    }
}


export default VolumnSelection;


