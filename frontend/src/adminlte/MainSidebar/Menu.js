import React from "react";
import _ from "lodash";
import {Link} from "react-router";


const allLinks = [
    {
        permission: "user.view_users",
        text: "Users",
        to: "/users",
        icon: "fa fa-users"
    },
    {
        permission: "segmentation.add_page",
        text: "页面校勘",
        to: "/papers",
        icon: "fa fa-edit"
    }
];

const userLinks = _.filter(allLinks, (link) => {
    return window.django.user.permissions.has(link.permission);
});


export default class Menu extends React.Component {
    render() {
        return (
            <section className="sidebar">
                <ul className="sidebar-menu">
                    <li className="header text-center">MENU</li>
                    {_.map(userLinks, (link, key) =>
                        <li key={key}>
                            <Link to={link.to}>
                                <i className={link.icon}/>
                                <span>{link.text}</span>
                            </Link>
                        </li>
                    )}
                </ul>
            </section>
        );
    }
}
