import React from "react";
import {IndexRoute, Route} from "react-router";

import DashBoard from "./views/DashBoard";


const routes = (
        <Route path="app" component={DashBoard}>
        </Route>

);

export default routes;
