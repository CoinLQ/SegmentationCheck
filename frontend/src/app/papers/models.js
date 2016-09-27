import {Map, Record} from "immutable";

import isFilterActive from "app/utils/isFilterActive";
import constants from "./constants";


class ChangeSet extends Record({
    first_name: "",
    last_name: "",
    email: "",
    _errors: Map()
}){}


class Paper extends Record({
    id: "",
    constants,
    ChangeSet,
    url: "",
}) {
    appUrl() {
        return `/papers/${this.id}`;
    }

    tabUrl(tab = "details") {
        return `${this.appUrl()}/${tab}`;
    }

    apiUrl() {
        return `${window.django.urls.users}${this.id}/`;
    }

    toString() {
        return "-";
    }
}

class Collection extends Record({
    apiUrl: '/api/v1/papers',
    constants,
    ChangeSet,
    isLoading: false,
    Model: Paper,
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
    routeId: "paper",
    title: "页面校勘",
    titleSingular: "Paper"
}){
    appUrl() {
        return "/papers";
    }

    isFilterActive() {
        return isFilterActive(this.query);
    }
}

export {
    Collection,
    Paper
};
