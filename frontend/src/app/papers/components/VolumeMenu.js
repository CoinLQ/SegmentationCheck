import React from "react";
import ReactDOM from "react-dom";
import classnames from "classnames";

class VolumeMenu extends React.Component {
    constructor(props) {
        super(props);
        this.state = {expanded: false,
                      volume_lists: [
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
                      selected_volume: 1};
    }

    componentDidMount() {
    }

    ToggleVolume = () => {
       return this.setState({expanded: !this.state.expanded});
    }

    selectVolume = (id) => {
        return function (){
            this.setState({selected_volume: id});
            this.props.volChanged(id)
        }.bind(this);
    }

    closeVolumeMenu = () => {
       return this.setState({expanded: false});
    }

    renderCurrentVolume() {
        const {selected_volume, volume_lists} = this.state;
        const _current = _.find(volume_lists, { 'id': selected_volume });
        if (_current)
            return (
                    <a id="HCteVol" href="javascript:;" className="whiteBackground glow" type="button" data-toggle="dropdown" >
                        <span className="text number">{_current.id}</span><span className="triangle"></span>
                    </a>
                    )
    }

    renderMenu = () => {
        if (this.state.expanded)
            return (<ul className="dropdown-menu">
                {this.state.volume_lists.map(function(volume) {
                 return <li onClick={this.selectVolume(volume.id)}> <a href='javascript:;'>{volume.id}</a></li>
                }.bind(this))}
            </ul>)
    }

    render() {
        const {expanded} = this.state;

        const drop_classNames = classnames({
                "dropdown": true,
                "open": expanded})

        return (
                <div className={drop_classNames} onClick={this.ToggleVolume} mouseOut={ this.closeVolumeMenu }>
                    {this.renderCurrentVolume()}
                    {this.renderMenu()}
                </div>

        );
    }
}


export default VolumeMenu;
