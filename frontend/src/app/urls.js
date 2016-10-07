import React from "react";
import {IndexRoute, Route} from "react-router";

import Admin from "app/layouts/Admin";
import RouteNotFound from "app/components/RouteNotFound";
import users from "app/users/urls";
import papers from "app/papers/urls";
import DashBoard from "app/apps/views/DashBoard";

const urls = (
    <Route path="/">

        <Route component={Admin} path="" >
            <IndexRoute components={{main: DashBoard}} />
            {users}
            {papers}
            <Route path="*" component={RouteNotFound}/>
        </Route>
    </Route>
);

export default urls;
