import React from "react";
import drawSVG from "app/utils/svgHelper"
import PaperCut from "app/paper_cuts/components/PaperCut"

class PaperContainer extends React.Component {
    componentDidMount() {
    }


    render() {
        const {children, model, key} = this.props;
        return (
            <div {...this.props}>
            <PaperCut key={key} model={model} />
            </div>
        );
    }
}


export default PaperContainer;
