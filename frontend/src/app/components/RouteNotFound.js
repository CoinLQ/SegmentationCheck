import React from "react";

import history from "app/history";


class RouteNotFound extends React.Component {
    render() {
        return(
            <div className="error-page">
                <h2 className="headline text-yellow"> 404</h2>
                <div className="error-content">
                    <h3><i className="fa fa-warning text-yellow"></i> Oops! 该页面不存在.</h3>

                    <p className="text-center">
                        很遗憾，您所访问的页面我们还没找到。
                    </p>

                    <a
                        className="btn btn-default cursor-pointer"
                        onClick={history.goBack}
                    >
                        返回
                    </a>
                </div>
            </div>
        );
    }
}

export default RouteNotFound;
