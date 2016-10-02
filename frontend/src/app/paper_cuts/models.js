import {Map, List, Record} from "immutable";

import isFilterActive from "app/utils/isFilterActive";
import constants from "./constants";


class ChangeSet extends Record({
    first_name: "",
    last_name: "",
    email: "",
    _errors: Map()
}){}


class PaperCut extends Record({
    id: "",
    constants,
    ChangeSet,
    paper_id: "",
    line_list: Map()
}) {
    appUrl() {
        return `/bars/${this.id}`;
    }


    apiUrl() {
        return `/api/v1/bars/${this.id}`;
    }

    toString() {
        return "-";
    }
}

class Collection extends Record({
    apiUrl: '/api/v1/bars',
    constants,
    ChangeSet,
    isLoading: false,
    Model: PaperCut,
    models: Map(),
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
    routeId: "papercut",
    title: "页面",
    titleSingular: "PaperCut"
}){
    appUrl() {
        return "/paper_cuts";
    }

    isFilterActive() {
        return isFilterActive(this.query);
    }
}

export {
    Collection,
    PaperCut
};
