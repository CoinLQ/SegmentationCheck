import React from "react";
import {IndexRedirect, Route} from "react-router";

import Edit from "./views/Edit";
import List from "./views/List";
import Tabs from "./views/Tabs";
import VolumnSelection from "./components/VolumnSelection"

const routes = (
    <Route path="papers" components={{children: List, navbar: VolumnSelection}}>
        <Route path=":paper" component={Tabs}>
            <IndexRedirect to="edit"/>
            <Route path="edit" component={Edit} />
        </Route>
    </Route>
);

export default routes;
