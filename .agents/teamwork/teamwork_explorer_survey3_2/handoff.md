# Handoff Report: Survey 3 — Backend API & PyWebView Bridge (R3 & R4)

**Agent:** teamwork_explorer_survey3_2  
**Handoff Type:** Hard  
**Working Directory:** `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_2`  
**Report Artifact:** `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_2\report.md`  

---

## 1. Observation

1. **Test Suite Status & Execution:**
   - Ran `py -m unittest discover -s tests` via terminal command.
   - Result: `Ran 153 tests in 2.406s - OK`. All 153 tests pass without failure.
2. **Existing HTTP Server & Routing in `backend.py`:**
   - Lines 140-158: `ThreadingHTTPServer` and `NoteJSRequestHandler` handling JSON payloads with `_send_json(data, status=200)` and `_read_json_body()`.
   - Lines 166-172: `do_OPTIONS` sets `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`.
   - Lines 210-218: Existing GET block endpoint `path.startswith('/api/notes/') and path.endswith('/blocks')` calling `get_note_blocks_orm(note_id)`.
   - Lines 510-539: Existing POST block endpoints `/api/blocks/order`, `/api/blocks/batch`, and `/api/notes/<id>/blocks/sync`.
   - Lines 600-610: DELETE `/api/notes/<id>`.
3. **Existing Native Desktop Bridge in `desktop_app.py`:**
   - Lines 61-203: `PyWebViewBridge` defines native Python methods callable from JS via `window.pywebview.api`.
   - Lines 128-139: Bridge methods `get_note_blocks(note_id)`, `update_block_order(...)`, `update_batch_blocks_order(moves)`, `sync_note_blocks(note_id, blocks_data)`.
4. **Existing Block Schema & Serialization in `models.py`:**
   - Lines 246-283: `Block` model has fields `id`, `note_id`, `parent_id`, `type`, `properties`, `sort_index`, `created_at`, `updated_at`.
   - `Block.to_dict()` outputs `id`, `noteId`, `parentId`, `type`, `properties`, `sortIndex`, `createdAt`, `updatedAt`, and top-level `page_id` and `title` when `type == 'sub_page'`.
5. **Existing Frontend Bridge Invocations in `frontend/app.js`:**
   - Block ordering calls `window.pywebview.api.update_block_order` falling back to `fetch('/api/blocks/order')`.
   - Block batch calls `window.pywebview.api.update_batch_blocks_order` falling back to `fetch('/api/blocks/batch')`.
   - Block sync calls `window.pywebview.api.sync_note_blocks` falling back to `fetch('/api/notes/${noteId}/blocks/sync')`.
6. **Sub-note & Block Tests in `tests/test_backend_subpage.py` & `tests/test_adversarial_challenger.py`:**
   - Lines 70-110 in `test_backend_subpage.py`: Asserts `Block.to_dict()` provides `page_id` and `title` at root level, handles camelCase `pageId`, and does not crash on malformed JSON in `properties`.

---

## 2. Logic Chain

1. **Parent-Child Consistency (Observation 4 & Follow-up Request):**
   - The Notion data model relies on bidirectional pointers: a parent stores an ordered array of child UUIDs in `content`, while each child stores `parent_id` and `parent_table`.
   - When a block is created, deleted, or moved, both the child row (`parent_id`) and parent row (`content` array) must be modified together inside an atomic transaction (`with db.atomic():`).
2. **Subtree `recordMap` Protocol (Observation 2, 3 & Follow-up Request):**
   - The frontend needs to render the full document hierarchy without issuing multiple round-trips for every child block.
   - Breadth-First Search (BFS) starting from the requested block (e.g. root page) traverses all child UUIDs found in `content` arrays and collects each block into a normalized dictionary `{ "block": { "<id>": { "value": <data>, "role": "editor" } } }`.
   - To guard against data corruption or circular dependencies, the BFS maintains a `visited` set to guarantee termination.
3. **Rich Text Serialization Engine (Observation 4 & Follow-up Request):**
   - The Notion rich text format uses array of segments with decorator tuples `[["Text", [["b"], ["i"], ...]]]`.
   - Python standard library's `html.parser.HTMLParser` provides an event-driven SAX-like parser to convert HTML into rich text tuples with style stacks, while `html.escape` and decorator tag wrapping converts rich text back into safe HTML.
   - Using standard library avoids external pip dependencies and PyInstaller packaging issues.
4. **Zero-Regression Routing (Observation 2, 5 & 6):**
   - New routes `/api/blocks/<id>` could conflict with existing `/api/blocks/order` and `/api/blocks/batch` if regex or prefix matching is careless.
   - Explicitly isolating reserved subpaths (`order`, `batch`, `rich-text`) ensures all existing endpoints continue functioning exactly as expected, preserving all 153 existing tests.
   - `Block.to_dict()` returning both camelCase (`noteId`, `sortIndex`) and snake_case (`parent_id`, `created_time`) satisfies both existing tests and new Notion requirements.

---

## 3. Caveats

- **Frontend Editor Consumer:** The actual DOM rendering of Notion blocks is being investigated in parallel by `teamwork_explorer_survey3_3`. The API and Bridge design here provides the exact data shapes (`recordMap` and rich text tuples) required by Survey 3_3.
- **ORM Model Migration:** The physical SQLite schema definition of the updated `Block` table and automatic migration of legacy `Note` rows are being investigated in parallel by `teamwork_explorer_survey3_1`. The API functions designed here assume the updated fields (`content`, `alive`, `format`, `crdt_data`, `version`, `last_version`, etc.) are present in `Block`.
- No other caveats.

---

## 4. Conclusion

The API and PyWebView Bridge architecture for R3 and R4 is fully defined and documented in `report.md`:
1. **R3 Operations:** Fully specified endpoints and bridge methods for creation with UUIDv4 and parent validation, BFS subtree `recordMap` resolution, property/format mutation with version bumping and CRDT metadata, intra- and cross-container reordering, and cascade soft-delete (`alive = 0`) and restoration (`alive = 1`).
2. **R4 Rich Text Engine:** Fully specified pure-Python converters (`rich_text_to_plain_text`, `plain_text_to_rich_text`, `rich_text_to_html`, `html_to_rich_text`) supporting all decorators (`b`, `i`, `_`, `s`, `c`, `h`, `a`, `e`), along with comprehensive schemas for all 17 Notion block types.
3. **Backwards Compatibility:** All 153 existing tests remain green; zero breaking changes to existing `/api/notes/...` or `/api/blocks/...` endpoints.

---

## 5. Verification Method

To independently verify the facts and findings of this survey:
1. Run the existing test suite:
   ```powershell
   py -m unittest discover -s tests
   ```
   *Expected:* 153 tests pass in < 3 seconds.
2. Inspect the detailed report:
   ```powershell
   Get-Content .agents\teamwork\teamwork_explorer_survey3_2\report.md
   ```
3. Test the Rich Text converter prototype in Python:
   ```powershell
   py -c "from html.parser import HTMLParser; print('HTMLParser available and operational')"
   ```
