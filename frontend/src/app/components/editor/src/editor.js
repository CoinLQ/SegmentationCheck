import React, {Component} from 'react';
import {EditorState, convertToRaw, convertFromRaw} from 'draft-js';
import Editor from 'draft-js-plugins-editor-wysiwyg';
import {DefaultDraftBlockRenderMap} from 'draft-js';
import createPlugins from './create-plugins';
import {Map} from 'immutable';

class WysiwygEditor extends Component {


  static defaultProps = {
    style: {},
    styleEditor: {},
    styleList: {},
    styleListItem: {}
  }

  constructor(props) {
    super(props);
    this.batch = batch(200);
    this.plugins = createPlugins(props);
    this.editorState = props.value
      ? EditorState.push(EditorState.createEmpty(), convertFromRaw(props.value))
      : EditorState.createEmpty();

    this.blockRenderMap = DefaultDraftBlockRenderMap.merge(
      this.customBlockRendering(props)
    );

    this.state = {};
  }

  componentWillUnmount(){
    this.unmounted = true;
  }

  shouldComponentUpdate(props, state) {
    if (this.props.value !== props.value && this._raw !== props.value) {
      this.editorState = !props.value
        ? EditorState.createEmpty()
        : EditorState.push(this.editorState, convertFromRaw(props.value));
      return true;
    } else if (this.state.active !== state.active
      || this.state.readOnly !== state.readOnly
      || this.state.editorState !== state.editorState) {
      return true;
    } else if (this.props.readOnly !== props.readOnly
      || this.props.fileDrag !== props.fileDrag
      || this.props.uploading !== props.uploading
      || this.props.percent !== props.percent) {
      return true;
    }
    return false;
  }

  onChange = (editorState) => {
    if (this.unmounted) return;
    this.editorState = editorState;
    this.setState({editorState: Date.now()});

    if (this.props.onChange) {
      this.batch(() => {
        this._raw = convertToRaw(editorState.getCurrentContent());
        this.props.onChange(this._raw, editorState);
      });
    }
  };

  focus = () => {
    this.refs.editor.focus();
  };

  blockRendererFn = contentBlock => {
    const {blockTypes} = this.props;
    const type = contentBlock.getType();
    return blockTypes && blockTypes[type] ? {
      component: blockTypes[type]
    } : undefined;
  }

  customBlockRendering = props => {
    const {blockTypes} = props;
    var newObj = {
      'paragraph': {
        element: 'div',
      },
      'unstyled': {
        element: 'div',
      },
      'block-image': {
        element: 'div',
      },
      'block-table': {
        element: 'div',
      }
    };
    for (var key in blockTypes) {
      newObj[key] = {
        element: 'div'
      };
    }
    return Map(newObj);
  }

  render() {
    const {editorState} = this;
    const {isDragging, progress, readOnly} = this.props;

    return (
      <div style={Object.assign(this.props.style, {
          display: 'flex'
        })}>
        <ol {...this.props.list}
          style={Object.assign(this.props.styleList, {
            margin: 0,
            padding: 0
          })}>
          {[...Array((this.editorState || EditorState.createEmpty()).getCurrentContent().getBlockMap().size)].map((x, i) =>
            <li key={i}
              {...this.props.listItem}
              style={Object.assign(this.props.styleListItem, {
                listStylePosition: 'inside'
              })} />
          )}
        </ol>
        <div style={{flex: 1}}>
      <Editor readOnly={readOnly} editorState={editorState}
              plugins={this.plugins}
              blockRenderMap={this.blockRenderMap}
              blockRendererFn={this.blockRendererFn}
              onChange={this.onChange}
              ref="editor"
      />
      </div>
      </div>
    );
  }
}

export default WysiwygEditor;

const batch = (limit=500) => {
  var _callback = null;
  return (callback) => {
    _callback = callback;
    setTimeout(() => {
      if (_callback === callback) {
        callback();
      }
    }, limit);
  }
}
