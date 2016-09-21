import {Map, Record} from "immutable";

import isFilterActive from "app/utils/isFilterActive";
import constants from "./constants";

class PageComment extends Record({
    id: "",
    user: Map(),
    tripitaka: Map({'items': []}),
    page: Map(),
    constants,
    opage: Map(),
    _errors: Map(),
}){

    apiUrl() {
       return '/api/page_comments/';
    }

    toString() {
        return "ok";
    }
}

class Collection extends Record({
    apiUrl: 'PageComment',
    constants,
    Model: PageComment,
    isLoading: false,
    models: Map({'default': new PageComment()}),
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
        return "/page_comments";
    }

}

export {
    PageComment,
    Collection
};
