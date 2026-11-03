# Handoff Report: Frontend Investigation & Architecture for Notion Hierarchical Blocks

**Author**: Explorer Subagent (Survey 3_3)  
**Recipient**: Orchestrator Subagent (`194ebf91-bb1a-45d3-84cf-aa5f5ea7f27e`)  
**Working Directory**: `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_3`  
**Report Reference**: `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_3\report.md`  
**Date**: 2026-11-02  

---

## 1. Observation

1. **Test Suite Baseline**:
   - Command: `py -m unittest discover -s tests`
   - Output: `Ran 153 tests in 3.140s - OK`
   - Test contracts in `tests/test_editor_interactions.py`:
     * Line 51: Checks exact guard clause in `frontend/app.js`:
       `if (e.target.closest('[contenteditable="true"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;`
     * Line 57: Requires `<div id="editor-body">` in `frontend/index.html` to include class `'editor-container'`.
     * Line 63: Requires `styles.css` to define `.editor-body, .editor-container {`.
     * Line 79–91: Requires `window.renderBlock = renderBlock`, `window.renderBlocks = renderBlocks`, `window.attachSubpageBlockListeners = attachSubpageBlockListeners`, and `case 'sub_page':` in `renderBlock`.

2. **Current Content Model in `frontend/app.js`**:
   - Line 4235: `loadActiveNote()` currently populates content via:
     `editorCanvas.innerHTML = note.content || '';`
   - Lines 4249–4331: Also toggles display and values for static DOM blocks outside `#rich-editor-canvas`:
     `#block-callout`, `#block-quote`, `#block-toggle`, `#block-code`, `#block-kanban`, `#block-table`, `#block-checklists`, `#block-katex`.
   - Lines 4643–4646: `syncRichEditor()` extracts HTML directly from canvas:
     `note.content = rawHtml.replace(/<mark class="in-note-search-match[^"]*">([\s\S]*?)<\/mark>/gi, '$1');`

3. **Preliminary Block Support in `frontend/app.js`**:
   - Lines 6025–6057:
     ```javascript
     function renderBlock(block) {
       if (!block || !block.type) return null;
       switch (block.type) {
         case 'sub_page': { ... }
         case 'p':
         default: { ... }
       }
     }
     ```
   - Lines 15001–15018: `tagAllEditorBlocks()` iterates `editor.children`, stamping `data-block-id` and fractional `data-sort-index`.
   - Lines 4605–4636: `collectAndSyncNoteBlocks(noteId)` packages children of `#rich-editor-canvas` and sends them via `apiSyncNoteBlocks(noteId, blocks)`.

4. **Event Handling & Drag-and-Drop in `frontend/app.js`**:
   - Lines 15072–15750: `initSpatialBlockController()` provides a 6-dot grip handle (`#spatial-block-handle`), multi-block selection via marquee rectangle (`isMarqueeActive`), and spatial reordering (`reorderBlocksWithFractionalIndexing`, `combineBlocksIntoSideBySideColumns`, `nestBlocksInsideTarget`).
   - Line 15657: Selection conflict guard prevents marquee rectangle initiation inside editable elements.

5. **Backend Communication Pattern**:
   - Lines 1082–1084, 14933–14981: Every backend method checks:
     `if (window.pywebview && window.pywebview.api && window.pywebview.api.<method>) return await window.pywebview.api.<method>(...);`
     falling back to `fetch('/api/...', { method: 'POST', body: JSON.stringify(...) })`.

---

## 2. Logic Chain

1. **From Observation 1 & 3**:
   - The current code already establishes `renderBlock(block)`, `renderBlocks(blocks, container)`, and `attachSubpageBlockListeners()`, but it only handles `sub_page` and falls back to `p`.
   - Because existing automated tests explicitly assert the existence and behavior of `renderBlock(block)`, `renderBlocks`, and `attachSubpageBlockListeners`, the implementation of R4 & R5 must extend `renderBlock(block)` (adding cases for the full block suite: `page`, `column_list`, `column`, `divider`, `text`, `header`, `sub_header`, `sub_sub_header`, `bulleted_list`, `numbered_list`, `toggle`, `code`, `equation`, `table`, `table_row`, `collection_view`, `image`) without removing `case 'sub_page':` or breaking existing exports.

2. **From Observation 2 & Notion Model Requirements**:
   - Storing a monolithic HTML string in `note.content` does not support Notion's hierarchical block tree or rich-text decorator tuples.
   - To achieve full Notion fidelity:
     * Notes must be loaded as a root `page` block pointing to child block UUIDs in its `content` array.
     * The document must be backed by an in-memory `recordMap` structure (`recordMap.block[uuid].value`).
     * The editor must recursively traverse `content` arrays from the root `page` block, instantiating each block via `renderBlock(block)`.
     * Editing text in `contenteditable` elements must be serialized into decorator tuples `[["Text", [["b"], ...]]]` stored in `block.properties.title`.

3. **From Observation 4**:
   - The editor already includes an advanced spatial block controller with 6-dot grip handles (`⋮⋮`), column combination, and nesting capabilities.
   - Transitioning this controller to update the parent block's `content` array (rather than merely reordering DOM elements and calculating fractional strings) aligns spatial DND with Notion's bidirectional tree model.

4. **From Observation 5**:
   - Because both `window.pywebview.api` and REST `fetch('/api/...')` endpoints exist in parallel, all new block operations (`save_block`, `update_block_order`, `sync_record_map`, `soft_delete_block`) must follow the existing isomorphic check pattern so that desktop execution (PyWebView) and web/headless modes remain 100% functional.

---

## 3. Caveats

1. **Backend Dependency**:
   - The frontend implementation of `renderTreeFromRecordMap` and `saveBlockMutation` relies on backend endpoints (`backend.py` / `desktop_app.py`) being updated by survey 3_1 and 3_2 to return and accept `recordMap` dictionaries and block DDL fields (`id`, `parent_id`, `parent_table`, `content`, `properties`, `format`, `alive`).
   - A client-side fallback/adapter should convert legacy `note.content` HTML into an in-memory `recordMap` if the backend has not yet completed migration for a given note.
2. **KaTeX Library**:
   - Equation rendering depends on `window.katex`. If `window.katex` is not loaded, equations should display LaTeX source text in monospace rather than failing.
3. **No Code Modification During Survey**:
   - In accordance with the Explorer subagent instructions, no source code files (`app.js`, `index.html`, `styles.css`) were modified during this investigation. All designs and code snippets are presented as architecture proposals in `report.md`.

---

## 4. Conclusion

The frontend architecture for Notion hierarchical block tree rendering and editing is fully designed and documented in `report.md`. Key deliverables prepared for the implementers:
1. **Rich-text conversion module**: `parseRichTextToHtml(tuples)` and `htmlToRichTextTuples(dom)` supporting bold, italic, underline, strike, code, colors, highlights, links, and inline equations.
2. **Full block suite element factory**: Extended `renderBlock(block)` specifications for structural (`page`, `column_list`, `column`, `divider`), text/headers (`text`, `header`, `sub_header`, `sub_sub_header`, `bulleted_list`, `numbered_list`, `toggle`), data/code (`code`, `equation`, `table`, `table_row`, `collection_view`), and media (`image`).
3. **Recursive RecordMap renderer**: `renderTreeFromRecordMap(recordMap, pageId, container)` with cycle prevention and post-render listener attachments.
4. **Interactive editing engine**: Caret splitting on Enter, block conversion via slash commands and action menu, hierarchy DND, and debounced bridge persistence.
5. **Full compatibility**: Seamless interoperation with tabs, right-rail TOC, folder sidebar, dark/light themes, and 100% preservation of the 153 passing tests.

---

## 5. Verification Method

1. **Automated Unit Testing**:
   Run the full project test suite in powershell:
   ```powershell
   py -m unittest discover -s tests
   ```
   *Expected result*: All 153 tests pass with 0 failures and 0 errors.

2. **Frontend Contract Inspection**:
   Inspect `frontend/app.js` to ensure the following identifiers are exported and functional:
   - `window.renderBlock`
   - `window.renderBlocks`
   - `window.attachSubpageBlockListeners`
   - `window.loadNote`
   - Guard clause at line 15657:
     `if (e.target.closest('[contenteditable="true"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;`

3. **Report Artifact Inspection**:
   Review the comprehensive architecture report at:
   `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_3\report.md`
