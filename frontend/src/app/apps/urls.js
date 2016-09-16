import React from "react";
import {IndexRedirect, Route} from "react-router";

import DashBoard from "./views/DashBoard";


const routes = (
      <Route path="dashboard" component={DashBoard}/>

);

export default routes;
