import React from "react";
import {Col, Row} from "react-bootstrap";

import {Box} from "adminlte";
import LinkedListGroup from "app/components/LinkedListGroup";
import Pagination from "app/components/Pagination";
import RefreshButton from "app/components/RefreshButton";
import SearchBox from "app/components/SearchBox";
import Slider from 'react-slick'
import PaperContainer from 'app/papers/components/PaperContainer'
import { DZJEditor } from 'app/components/editor/DZJEditor';
import Example  from 'app/components/editor/wysiwyg/container.js'
class Container extends React.Component {
    componentWillMount() {
        const {actions, collection} = this.props;
        const query = collection.get("query");
        actions.fetchCollectionIfEmpty({collection, query});
    }
    componentDidMount() {
    }

    render() {
        const {children, collection, rowOneWidth = 7, rowTwoWidth = 5} = this.props;
        const settings = {
            dots: false,
            vertical: false,
            adaptiveHeight: true,
            infinite: false,
            slidesToShow: 1,
            slidesToScroll: 1,
            swipe:false,
        }

        return (
                <div>
                <Box.Wrapper>
                    <Box.Header>
                        <Box.Title>{collection.title}</Box.Title>
                        <div className="inline-wrap">
                        <span className="h4">H-V00017P00232B2</span></div>
                        <Box.Tools>
                            <div className="combo-buttons">
                                <a href="#aboutModal" data-toggle="modal" data-target="#myModal" className="btn btn-circle-micro btn-primary">
                                    <span className="fa fa-server"></span>
                                </a>
                                <a href="#aboutModal" data-toggle="modal" data-target="#myModal" className="btn btn-circle-micro btn-primary">
                                    <span className="fa fa-bell-o"></span>
                                </a>
                                <a href="#aboutModal" data-toggle="modal" data-target="#myModal" className="btn btn-circle-micro btn-primary">
                                    <span className="fa fa-cog"></span>
                                </a>
                                <a href="#aboutModal" data-toggle="modal" data-target="#myModal" className="btn btn-circle-micro btn-primary">
                                    <span className="fa fa-question"></span>
                                </a>
                            </div>
                        </Box.Tools>
                    </Box.Header>
                </Box.Wrapper>
                <Row>
                    <Col sm={rowOneWidth} className="container">

                                 {collection.models.size != 0 && <Slider {...settings}>
                                    {collection.models.toList().map((model, key) =>
                                        <PaperContainer key={key} model={model}/>
                                    )}
                                </Slider>
                                }

                    </Col>
                    <Col sm={rowTwoWidth}>
                         <Example />
                        {children}
                    </Col>
                </Row>
                </div>


        );
    }
}

export default Container;
