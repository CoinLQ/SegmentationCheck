import React from "react";
import {Col, Row} from "react-bootstrap";
import InfoBox from "app/apps/components/InfoBox";
import TopFPanel from "app/apps/components/TopFPanel";
import CollateInfoPanel from "app/apps/components/CollateInfoPanel";
import CommentTable from "app/apps/components/CommentTable";


class Container extends React.Component {
    componentWillMount() {
        const {actions, collection} = this.props;
        const Model = collection.get("Model");
        actions.fetchModel({model: new Model()});
    }

    render() {
        const {children, collection, rowOneWidth = 6, rowTwoWidth = 6} = this.props;

        const dashboard = collection.models.get('default');
        debugger;
        return (
            <Row className='content'>
              <InfoBox boxBg='bg-aqua' iconClass='ion-ios-folder'
                  textInfo='藏经数'>
                  <span className='info-box-number'>{dashboard.tripitaka.count}<small>部</small></span>
              </InfoBox>
              <InfoBox boxBg='bg-red' iconClass='ion-ios-paper-outline'
                  textInfo='待处理文件数'>
                  <span className='info-box-number'>{dashboard.page.count}</span>
              </InfoBox>
              <InfoBox boxBg='bg-green' iconClass='ion-ios-paper'
                  textInfo='已处理文件数'>
                  <span className='info-box-number'>{dashboard.page.approved}</span>
              </InfoBox>
              <InfoBox boxBg='bg-yellow' iconClass='ion-ios-people-outline'
                  textInfo='校勘用户数'>
                  <span className='info-box-number'>{dashboard.user.count}</span>
              </InfoBox>
              <Col sm={rowOneWidth}>
                  <TopFPanel tripitakas={dashboard.tripitaka.items || []}></TopFPanel>
              </Col>
              <Col sm={rowTwoWidth}>
                  <CollateInfoPanel/>
              </Col>

              <Col sm={12}>
                  <CommentTable/>
              </Col>
            </Row>
        );
    }
}

export default Container;
