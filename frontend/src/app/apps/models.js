import {Map, Record} from "immutable";

import isFilterActive from "app/utils/isFilterActive";
import constants from "./constants";

class DashBoard extends Record({
    id: "",
    user: Map(),
    tripitaka: Map({'items': []}),
    page: Map(),
    constants,
    opage: Map(),
    _errors: Map(),
}){

    apiUrl() {
       return '/api/v1/dashboard/';
    }

    toString() {
        return "ok";
    }
}

class Collection extends Record({
    apiUrl: 'dashboard',
    constants,
    Model: DashBoard,
    isLoading: false,
    models: Map({'default': new DashBoard()}),
    pagination: Map({
        end_index: 0,
        page: 0,
        start_index: 0,
        total_pages: 0
    }),
    query: Map({
        page: 1,
        search: ""
    }),
}){
    appUrl() {
        return "/volumes";
    }

    dashboard() {
       return this.models.get('default');
    }
}

export {
    DashBoard,
    Collection
};
