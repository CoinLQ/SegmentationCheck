import { Entity, Modifier, EditorState, SelectionState } from 'draft-js';

function _update(editorState, setEditorState, content, key, begin, end ) {
  var new_selection = new SelectionState({
        anchorKey: key,
        anchorOffset: begin,
        focusKey: key,
        focusOffset: end
      })
  let ReplacedContent = Modifier.replaceText(
                              editorState.getCurrentContent(),
                              new_selection,
                              content,
                              null
                            );
  const newEditorState = EditorState.push(editorState,
          ReplacedContent,
          'none');
  setEditorState(EditorState.acceptSelection(newEditorState, ReplacedContent.getSelectionAfter()));
  return newEditorState;
}
export function replaceContent(editorState, setEditorState, start, end='') {
  const _select = editorState.getSelection();
  const currentContent = editorState.getCurrentContent();
  const anchorKey = _select.getAnchorKey();
  const focusKey = _select.getFocusKey();
  const anchorBlock = currentContent.getBlockForKey(anchorKey);
  const focusBlock = currentContent.getBlockForKey(focusKey);
  if (focusKey == anchorKey)
  {
    const l = _select.anchorOffset;
    const r = _select.focusOffset;
    var blockText;
    if (_select.getIsBackward()) {
      blockText = anchorBlock.getText().slice(r,l);
    }
    else {
      blockText = anchorBlock.getText().slice(l,r);
    }
    var new_content = `${start}${blockText}${end}`;
    _update(editorState, setEditorState, new_content, anchorKey, _select.getStartOffset(), _select.getEndOffset());
  }
  else{
    const l = _select.anchorOffset;
    const r = _select.focusOffset;
    var anchorText;
    var focusText;
    if (!_select.getIsBackward()) {
      anchorText = anchorBlock.getText().slice(l);
      var anchor_content = `${start}${anchorText}`
      console.log(anchor_content);
      var newEditorState = _update(editorState, setEditorState, anchor_content, anchorKey, l, anchorBlock.getText().length);
      focusText = focusBlock.getText().slice(0,r);
      let focus_content = `${focusText}${end}`;
      _update(newEditorState, setEditorState, focus_content, focusKey, 0, r);
    }else{
      anchorText = anchorBlock.getText().slice(0, l);
      var anchor_content = `${anchorText}${end}`
      console.log(anchor_content);
      var newEditorState = _update(editorState, setEditorState, anchor_content, anchorKey, 0, l);
      focusText = focusBlock.getText().slice(r);
      let focus_content = `${begin}${focusText}`;
      _update(newEditorState, setEditorState, focus_content, focusKey, r, focusBlock.getText().length);

    }
  }
}

export default {
    replaceContent,
};