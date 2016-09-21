import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {createSelector} from "reselect";

import actions from "app/actions/collection";
import Container from "app/components/dashboard/Container";
import WidgetGroup from "app/apps/components/WidgetGroup";

const selector = createSelector(
    (state) => state.apps,
    (collection) => {
        return {
            collection,
            WidgetGroup
        };
    }
);

const bindActions = (dispatch) => {
    return {actions: bindActionCreators(actions, dispatch)};
};

export default connect(selector, bindActions)(Container);
