import React from "react";
import drawSVG from "app/utils/svgHelper"

class PaperCut extends React.Component {
    componentDidMount() {
        const {model} = this.props;
        drawSVG(model.id.toString(), model.url);
    }


    render() {
        const {children, model, key} = this.props;
        return (
            <div {...this.props}>
            <div className="svg-wrapper" key={key} id={model.id} >
            </div>
            </div>
        );
    }
}


export default PaperCut;
