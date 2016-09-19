import React from "react";
import {Col, Row} from "react-bootstrap";



class Container extends React.Component {
    componentWillMount() {
        const {actions, collection} = this.props;
        const query = collection.get("query");
        actions.fetchCollectionIfEmpty({collection, query});
    }

    render() {
        const {children, rowOneWidth = 6, rowTwoWidth = 6} = this.props;

        return (
            <Row className='content'>
        <div className="col-md-3 col-sm-6 col-xs-12">
          <div className="info-box">
            <span className="info-box-icon bg-aqua"><i className="ion ion-ios-folder"></i></span>

            <div className="info-box-content">
              <span className="info-box-text">藏经数</span>
              <span className="info-box-number"><big>2</big><small>部</small></span>
            </div>
          </div>
        </div>
        <div className="col-md-3 col-sm-6 col-xs-12">
          <div className="info-box">
            <span className="info-box-icon bg-red"><i className="fa ion-ios-paper-outline"></i></span>

            <div className="info-box-content">
              <span className="info-box-text">待处理文件数</span>
              <span className="info-box-number"><big>30</big></span>
            </div>
          </div>
        </div>

        <div className="clearfix visible-sm-block"></div>

        <div className="col-md-3 col-sm-6 col-xs-12">
          <div className="info-box">
            <span className="info-box-icon bg-green"><i className="ion ion-ios-paper"></i></span>

            <div className="info-box-content">
              <span className="info-box-text">已处理文件数</span>
              <span className="info-box-number">460</span>
            </div>
          </div>
        </div>
        <div className="col-md-3 col-sm-6 col-xs-12">
          <div className="info-box">
            <span className="info-box-icon bg-yellow"><i className="ion ion-ios-people-outline"></i></span>

            <div className="info-box-content">
              <span className="info-box-text">校勘用户数</span>
              <span className="info-box-number">2,000</span>
            </div>
          </div>
        </div>

        <Col sm={rowOneWidth}>
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
                <tr>
                  <td>1.</td>
                  <td>龙藏</td>
                  <td>
                    <div className="progress progress-xs progress-striped active">
                      <div className="progress-bar progress-bar-success" style={{width: '90%'}}></div>
                    </div>
                  </td>
                  <td><span className="badge bg-green">90%</span></td>
                </tr>
                <tr>
                  <td>2.</td>
                  <td>洪武南藏</td>
                  <td>
                    <div className="progress progress-xs">
                      <div className="progress-bar progress-bar-yellow" style={{width: '70%'}}></div>
                    </div>
                  </td>
                  <td><span className="badge bg-yellow">70%</span></td>
                </tr>
                <tr>
                  <td>3.</td>
                  <td>赵城金藏</td>
                  <td>
                    <div className="progress progress-xs">
                      <div className="progress-bar progress-bar-danger" style={{width: '55%'}}></div>
                    </div>
                  </td>
                  <td><span className="badge bg-red">55%</span></td>
                </tr>

                <tr>
                  <td>4.</td>
                  <td>乾隆大正藏</td>
                  <td>
                    <div className="progress progress-xs progress-striped active">
                      <div className="progress-bar progress-bar-primary" style={{width: '30%'}}></div>
                    </div>
                  </td>
                  <td><span className="badge bg-light-blue">30%</span></td>
                </tr>

              </tbody></table>
            </div>
          </div>
        </Col>
        <Col sm={rowTwoWidth}>
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
        </Col>

        <Col sm={12}>
            <div className="box">
              <div className="box-header">
                <h3 className="box-title">编审意见表</h3>
              </div>
              <div className="box-body table-responsive no-padding">
                <table className="table table-hover">
                  <tbody><tr>
                    <th>ID</th>
                    <th>用户</th>
                    <th>日期</th>
                    <th>状态</th>
                    <th>缘由</th>
                    <th>处理人</th>
                    <th>处理情况</th>
                  </tr>
                  <tr>
                    <td>H-V20P183</td>
                    <td>贤二</td>
                    <td>9-17-2016</td>
                    <td><span className="label label-success">Approved</span></td>
                    <td>原图弯曲</td>
                    <td>admin</td>
                    <td>已替换原图</td>
                  </tr>
                  <tr>
                    <td>H-V20P293</td>
                    <td>贤二</td>
                    <td>9-17-2016</td>
                    <td><span className="label label-warning">Pending</span></td>
                    <td>缺上10页283-292</td>
                  </tr>
                  <tr>
                    <td>H-V20P657</td>
                    <td>贤二</td>
                    <td>9-17-2016</td>
                    <td><span className="label label-success">Approved</span></td>
                    <td>原图模糊</td>
                    <td>admin</td>
                    <td>已替换原图</td>
                  </tr>
                  <tr>
                    <td>H-V21P175</td>
                    <td>贤二</td>
                    <td>9-17-2016</td>
                    <td><span className="label label-danger">Denied</span></td>
                    <td>缺损，右边界文字丢失。文件稿对应差异较大。</td>
                    <td>admin</td>
                    <td>已替换原图，文字稿有待重新校对</td>
                  </tr>
                </tbody></table>
              </div>
            </div>
        </Col>
            </Row>
        );
    }
}

export default Container;
