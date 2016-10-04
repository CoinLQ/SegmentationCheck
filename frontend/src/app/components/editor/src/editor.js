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
    styleListItem: {},
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

  toggleLine = (id) => {
    var that = this;
    return function(id) {
    };
  }

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
    debugger;
    const { UndoButton, RedoButton } = this.plugins[this.plugins.length-1];
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
                        <a onClick={this.toggleLine(i)} ><li key={i}
                          /></a>
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
                  <UndoButton onChange={ this.onChange } editorState={ this.editorState } />
                  <RedoButton onChange={ this.onChange } editorState={ this.editorState } />
                  </div>
            <button id="CRDrawBtn" className="btn" type="button" data-toggle="popover" data-original-title="" title=""><span className="fa fa-scissors"></span><span className="text">切字</span></button>
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
