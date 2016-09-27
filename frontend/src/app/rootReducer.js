import {combineReducers} from "redux";

import adminlte from "adminlte/reducers";
import alerts from "app/reducers/alerts";
import users from "app/users/reducers";
import apps from "app/apps/reducers";
import papers from "app/papers/reducers";

export default combineReducers({
    adminlte,
    alerts,
    users,
    apps,
    papers,
});
