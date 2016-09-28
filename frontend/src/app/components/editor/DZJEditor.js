import React, { Component, PropTypes } from 'react';
import { EditorState, RichUtils} from 'draft-js';
import Editor from 'draft-js-plugins-editor'; // eslint-disable-line import/no-unresolved
import createCounterPlugin from 'draft-js-counter-plugin'; // eslint-disable-line import/no-unresolved
import createToolbarPlugin, { ToolbarDecorator } from 'draft-js-toolbar-plugin';

// Creates an Instance. At this step, a configuration object can be passed in
// as an argument.
const counterPlugin = createCounterPlugin();

// Extract a counter from the plugin.
const { CharCounter, LineCounter } = counterPlugin;



export class DZJEditor extends Component {
  static defaultProps = {
    style: {},
    styleEditor: {},
    styleList: {},
    styleListItem: {}
  }

  constructor(props) {
    super(props);
    this.state = {editorState: props.editorState || EditorState.createEmpty()};
  }

  onChange = (editorState) => {
    this.setState({
      editorState,
    });
  };

  setEditorState(editorState) {
    this.setState({
      editorState,
    });

  }

  render() {

    return (
      <div style={Object.assign(this.props.style, {
          display: 'flex'
        })}>
        <ol {...this.props.list}
          style={Object.assign(this.props.styleList, {
            margin: 0,
            padding: 0
          })}>
          {[...Array(this.state.editorState.getCurrentContent().getBlockMap().size)].map((x, i) =>
            <li key={i}
              {...this.props.listItem}
              style={Object.assign(this.props.styleListItem, {
                listStylePosition: 'inside'
              })} />
          )}
        </ol>
        <div style={{flex: 1}}>
          <Editor {...this.props.editor}
            style={this.props.styleEditor}
            editorState={this.state.editorState}
            onChange={this.onChange}
            plugins={[counterPlugin]}
            ref="editor"/>
          <CharCounter editorState={this.state.editorState} limit={200} />
          <LineCounter editorState={this.state.editorState} limit={200} />
        </div>
      </div>
    );
  }
}
