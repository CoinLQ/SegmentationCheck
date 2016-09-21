import React from "react";

class CommentTable extends React.Component {
    render() {
        const {children} = this.props;

        return (
             <div className="box">
              <div className="box-header">
                <h3 className="box-title">编审意见表</h3>
              </div>
              <div className="box-body table-responsive no-padding">
                <table className="table table-hover">
                  <tbody>
                  <tr>
                    <th>ID</th>
                    <th style={{width: '5em'}}>用户</th>
                    <th style={{width: '7em'}}>日期</th>
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
        );
    }
}

export default CommentTable;