import React from "react";
import ReactDOM from "react-dom";
import classnames from "classnames";

class TriMenu extends React.Component {
    constructor(props) {
        super(props);
        this.state = {expanded: false,
                      tri_lists: [
                      {
                        id: 1,
                        name: '高丽藏'
                      },
                      {
                        id: 2,
                        name: '赵城金藏'
                      },
                      {
                        id: 3,
                        name: '洪武南藏'
                      }],
                      selected_tri: 1};
    }

    componentDidMount() {
    }

    ToggleTri = () => {
       return this.setState({expanded: !this.state.expanded});
    }

    selectTri = (id) => {
        return function (){
            this.setState({selected_tri: id})
            this.props.triChanged(id);
        }.bind(this);
    }

    closeTriMenu = () => {
       return this.setState({expanded: false});
    }

    renderCurrentTri() {
        const {selected_tri, tri_lists} = this.state;
        const _current = _.find(tri_lists, { 'id': selected_tri });
        if (_current)
            return (
                    <a id="HCteTri" href="javascript:;" className="whiteBackground glow" type="button" data-toggle="dropdown" >
                        <span className="text">{_current.name[0]}<span className="whiteSpace">
                        </span>{_current.name.slice(1)}</span><span className="triangle"></span>
                    </a>
                    )
    }

    renderMenu = () => {
        if (this.state.expanded)
            return (<ul className="dropdown-menu">
                {this.state.tri_lists.map(function(tri) {
                 return <li onClick={this.selectTri(tri.id)}> <a href='javascript:;'>{tri.name}</a></li>
                }.bind(this))}
            </ul>)
    }

    render() {
        const {expanded} = this.state;

        const drop_classNames = classnames({
                "dropdown": true,
                "open": expanded})

        return (
                <div className={drop_classNames} onClick={this.ToggleTri} mouseOut={ this.closeTriMenu }>
                    {this.renderCurrentTri()}
                    {this.renderMenu()}
                </div>

        );
    }
}


export default TriMenu;
