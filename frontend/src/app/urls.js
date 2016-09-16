import React from "react";
import {IndexRedirect, Route} from "react-router";

import Admin from "app/layouts/Admin";
import RouteNotFound from "app/components/RouteNotFound";
import users from "app/users/urls";
import apps from "app/apps/urls";

const urls = (
    <Route path="/">
        <IndexRedirect to="dashboard"/>
        <Route component={Admin} path="">
            <IndexRedirect to="dashboard"/>
            {apps}
            {users}
            <Route path="*" component={RouteNotFound}/>
        </Route>
    </Route>
);

export default urls;
