import React from "react";
import _ from "lodash";
import classnames from "classnames";

class TopFPanel extends React.Component {
    render() {
        const {children, tripitakas} = this.props;

        const percent = (tripitaka) => {
          return (tripitaka.completed_count  * 100/tripitaka.volumes_count).toFixed(0);
        }

        const mystyle = (tripitaka) => {
          var _style = "";
          if (percent(tripitaka) < 30) {
            _style = "bg-blue";
          }else if (percent(tripitaka) >= 30 && percent(tripitaka)< 60){
            _style = "bg-red";
          }else if (percent(tripitaka) >= 60 && percent(tripitaka)< 80){
            _style = "bg-yellow";
          }else if (percent(tripitaka) >= 80){
            _style = "bg-green";
          }
          return _style;
        }

        return (
            <div className="box">
            <div className="box-header">
              <h3 className="box-title">藏经完善度Top 5</h3>
            </div>
            <div className="box-body no-padding">
              <table className="table table-striped">
                <tbody><tr>
                  <th style={{width: 30}}>#</th>
                  <th>藏经名称</th>
                  <th style={{width: '30%'}}>进度</th>
                  <th style={{width: '15%'}}>完成度</th>
                </tr>
                {_.map(tripitakas, (tripitaka, key) =>
                        <tr key={key}>
                          <td>{tripitaka.id }</td>
                          <td>{tripitaka.name}</td>
                          <td>
                            <div className="progress progress-xs progress-striped">
                              <div className={"progress-bar " + mystyle(tripitaka)} style={{width: (percent(tripitaka) +'%')}}></div>
                            </div>
                          </td>
                          <td><span className={"badge " + mystyle(tripitaka)}>{ percent(tripitaka)}%</span></td>
                        </tr>
                    )}
                </tbody>
              </table>
            </div>
          </div>
        );
    }
}

export default TopFPanel;