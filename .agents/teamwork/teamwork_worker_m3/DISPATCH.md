## 2026-11-02T02:27:01Z

You are a Worker subagent for Milestone 3 (Frontend Dynamic Rendering, Rich Text & Interactive Editor).
Working directory: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_worker_m3
Original request path: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\ORIGINAL_REQUEST.md
Scope document: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\PROJECT.md
Explorer findings report: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_3\report.md

You MUST read ORIGINAL_REQUEST.md first, as well as PROJECT.md and the explorer report.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File ownership:
You exclusively own:
- `frontend/app.js`
- `frontend/styles.css`
- `frontend/index.html`
- `tests/test_block_frontend_contracts.py`
Do NOT edit other files in this milestone.

Your Mission:
1. Implement in `frontend/app.js`:
   - Rich Text Tuple Engine:
     * `parseRichTextToHtml(tuples)`: transforms Notion rich-text tuple format `[["Text", [["b"], ["i"], ["h", color], ["c"], ["a", url], ["e", latex]]]]` into formatted HTML.
     * `htmlToRichTextTuples(domElement)`: converts formatted contenteditable HTML back into canonical Notion rich-text tuples.
     * Full decorator support: bold (`["b"]`), italic (`["i"]`), underline (`["_"]`), strikethrough (`["s"]`), inline code (`["c"]`), highlight/color (`["h", color]`), link (`["a", url]`), inline equation (`["e", latex]`).
   - Extended Element Factory `renderBlock(block)`:
     * Extend `renderBlock(block)` to support the full 17 Notion block types + `sub_page`:
       - Structural: `page`, `column_list`, `column` (flexbox side-by-side layout with ratio support), `divider` (<hr>).
       - Text & Headers: `text`, `header` (H1), `sub_header` (H2), `sub_sub_header` (H3), `bulleted_list` (li bullet), `numbered_list` (numbered item), `toggle` (collapsible `<details>`/toggle with disclosure arrow and nested child container).
       - Data & Code: `code` (with language badge/selector), `equation` (LaTeX formula block and inline equations with KaTeX/fallback), `table` & `table_row` (multi-column editable grid based on `table_block_column_order`, format headers), `collection_view` / `collection_view_page`.
       - Media: `image` (width control, source display).
       - Navigation: Preserve `case 'sub_page':` (`.block-subpage` with 📄 icon and `loadNote(block.page_id)`).
     * Global exports: `window.renderBlock = renderBlock`, `window.renderBlocks = renderBlocks`, `window.attachSubpageBlockListeners = attachSubpageBlockListeners`, `window.loadNote = loadNote`, `window.parseRichTextToHtml = parseRichTextToHtml`, `window.htmlToRichTextTuples = htmlToRichTextTuples`, `window.renderTreeFromRecordMap = renderTreeFromRecordMap`.
   - Recursive RecordMap Tree Renderer:
     * `renderTreeFromRecordMap(recordMap, rootId, container)`:
       - Follows `content` UUID arrays from root page block.
       - Resolves blocks from `recordMap.block[id].value` (skipping `alive === 0`).
       - Cycle prevention via `visited` Set.
       - Recursively renders container blocks (`column_list` -> `column` -> children; `toggle` -> children; `table` -> `table_row`).
       - Attaches event listeners and spatial drag handles.
   - Interactive Editing & Bridge Persistence:
     * Enter key on editable blocks splits text or inserts a new block below.
     * Backspace on empty block converts to paragraph or removes block.
     * Block type switching from format bar or slash commands.
     * Spatial controller (6-dot handle) drag-and-drop updates parent `content` array and triggers bridge / REST reorder.
     * Debounced persistence calling `window.pywebview.api.update_block` with fallback to `fetch('/api/blocks/<id>', { method: 'PUT', ... })`.
     * In `loadActiveNote(noteId)`, fetch `recordMap` via bridge `get_record_map(noteId)` / `fetch('/api/notes/${noteId}/recordMap')` and render with `renderTreeFromRecordMap`.
2. Implement CSS styling in `frontend/styles.css`:
   - Comprehensive styling for all Notion block components (`.notion-block`, `.block-column-list`, `.block-column`, `.block-toggle`, `.block-toggle-summary`, `.block-toggle-content`, `.block-code`, `.block-equation`, `.block-table`, `.block-table-row`, `.block-table-cell`, `.block-image`, `.block-divider`, inline formatting styles).
   - Ensure columns display side-by-side flexbox layout (`display: flex; gap: 16px; width: 100%;`).
3. Preserve Existing UI Contracts:
   - Floating pill tabs (`border-radius: 9999px`) and neutral controls.
   - Fixed right-column TOC outside/below cover banner.
   - Lasso selection guard: `if (e.target.closest('[contenteditable="true"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;`
   - Settings gear-only button.
4. Create automated test suite `tests/test_block_frontend_contracts.py`:
   - Test `renderBlock` coverage across all 17 Notion block types + `sub_page`.
   - Test rich text tuple parser and serializer algorithms.
   - Test `renderTreeFromRecordMap` structural hierarchy and cycle prevention.
   - Test exported globals and selection guard clauses.
   - Run verification:
     * `py -m unittest tests.test_block_frontend_contracts -v`
     * `py -m unittest discover -s tests -p "test_*.py"`
     * Ensure all 185 existing tests + new tests pass with 0 errors.
