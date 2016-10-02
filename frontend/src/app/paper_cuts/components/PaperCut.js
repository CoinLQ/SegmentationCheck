import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {createSelector} from "reselect";

import actions from "app/actions/collection";
import React from "react";
import {drawSVG, drawLines} from "app/utils/svgHelper";

const selector = createSelector(
    (state) => state.paper_cuts,
    (collection) => {
        return {
            collection,
        };
    }
);

class PaperCut extends React.Component {

    constructor(props) {
        super(props);
        this.state = {listLoaded: false};
    }
    componentDidMount() {
        const {actions, collection, model} = this.props;
        var drawing = drawSVG(model.id.toString(), model.url);
        const Model = collection.get("Model");
        actions.fetchModel({model: new Model({id: model.id})});
        this.setState({drawing});
    }

    componentWillReceiveProps(nextProps) {
        const {model, collection} = nextProps;
    }

    redrawLine = (collection, id) => {
        const paper_cut = collection.models.get(`${id}`);
        if (paper_cut) {
            drawLines(this.state.drawing, paper_cut.line_list);
            //this.setState({drawing: true});
        }
    }

    render() {
        const {collection, model, key} = this.props;
        this.redrawLine(collection, model.id);
        return (
            <div className="svg-wrapper" key={key} id={model.id} >
            </div>
        );
    }
}

const bindActions = (dispatch) => {
    return {actions: bindActionCreators(actions, dispatch)};
};

export default connect(selector, bindActions)(PaperCut);
