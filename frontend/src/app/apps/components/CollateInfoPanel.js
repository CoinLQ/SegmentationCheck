import React from "react";

class CollateInfoPanel extends React.Component {
    render() {
        const {children} = this.props;

        return (
             <div className="box">
            <div className="box-header">
              <h3 className="box-title">校勘信息</h3>

              <div className="box-tools">
                <ul className="pagination pagination-sm no-margin pull-right">
                  <li><a href="#">«</a></li>
                  <li><a href="#">1</a></li>
                  <li><a href="#">2</a></li>
                  <li><a href="#">3</a></li>
                  <li><a href="#">»</a></li>
                </ul>
              </div>
            </div>
            <div className="box-body no-padding">
              <table className="table">
                <tbody><tr>
                  <th style={{width: 10}}>#</th>
                  <th>活跃卷</th>
                  <th>负责主编</th>
                  <th>进度</th>
                  <th style={{width: '15%'}}>完成度</th>
                </tr>
                <tr>
                  <td>1.</td>
                  <td>洪武南藏第41册</td>
                  <td>贤三</td>
                  <td>
                    <div className="progress progress-xs">
                      <div className="progress-bar progress-bar-danger" style={{width: '55%'}}></div>
                    </div>
                  </td>
                  <td><span className="badge bg-red">55%</span></td>
                </tr>
                <tr>
                  <td>2.</td>
                  <td>洪武南藏第42册</td>
                  <td>贤四</td>
                  <td>
                    <div className="progress progress-xs">
                      <div className="progress-bar progress-bar-yellow" style={{width: '70%'}}></div>
                    </div>
                  </td>
                  <td><span className="badge bg-yellow">70%</span></td>
                </tr>
                <tr>
                  <td>3.</td>
                  <td>洪武南藏第43册</td>
                  <td>贤五</td>
                  <td>
                    <div className="progress progress-xs progress-striped active">
                      <div className="progress-bar progress-bar-primary" style={{width: '30%'}}></div>
                    </div>
                  </td>
                  <td><span className="badge bg-light-blue">30%</span></td>
                </tr>
                <tr>
                  <td>4.</td>
                  <td>洪武南藏第44册</td>
                  <td>贤六</td>
                  <td>
                    <div className="progress progress-xs progress-striped active">
                      <div className="progress-bar progress-bar-success" style={{width: '90%'}}></div>
                    </div>
                  </td>
                  <td><span className="badge bg-green">90%</span></td>
                </tr>
              </tbody></table>
            </div>
          </div>
        );
    }
}

export default CollateInfoPanel;