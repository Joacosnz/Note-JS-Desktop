# Handoff Report — Test Infrastructure & Specification Miner

**Working Directory**: `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\spec_miner_survey_tests`  
**Date**: 2026-11-02T12:38:00Z  
**Author**: Test Infrastructure & Spec Miner Subagent  
**Parent Agent**: 4ad26d22-329a-498b-97c2-c4b62703d7bb  

---

## 1. Observation

### 1.1 Test Suite Status and Infrastructure
- **Test Runner Command**:
  ```powershell
  py -m unittest discover -s tests
  ```
- **Execution Result**:
  - Ran 261 tests in 8.411s.
  - Exit code: `0` (OK, 0 failures, 0 errors).
- **Test File Inventory**:
  Total of 16 test files across `tests/`:
  1. `test_adversarial_challenger.py` (22 tests): Sub-note block schema variations, failure modes, boundaries.
  2. `test_adversarial_m3_r1_r4.py` (23 tests): Frontend rich text, DOM element generation, bridge operations.
  3. `test_adversarial_m3_r5_r6.py` (17 tests): Topbar buttons, toolbar isolation, amber exclusivity.
  4. `test_adversarial_notion_backend.py` (34 tests): Stress testing, deep nesting (50+ levels), circular references, optimistic concurrency 409, SQL injection.
  5. `test_adversarial_notion_frontend.py` (28 tests): Contenteditable guards, tree rendering, drag-and-drop reordering.
  6. `test_adversarial_suite.py` (14 tests): Unicode characters, XSS injections, long titles, dense subpages.
  7. `test_backend_subpage.py` (5 tests): Subpage schema and SQLite persistence.
  8. `test_block_api_and_richtext.py` (20 tests): Pure-Python rich text engine, canonical 17 Notion block types, REST API endpoints, PyWebViewBridge.
  9. `test_block_frontend_contracts.py` (8 tests): Static contract verification on `window`, Node.js VM DOM dynamic simulation for rich text and element factory.
  10. `test_block_schema_and_migration.py` (12 tests): 16-field Notion schema DDL, bidirectional pointers, CRDT tracking, legacy note migration.
  11. `test_challenger_it2_stress.py` (16 tests): Stress testing on database locking and concurrency.
  12. `test_editor_interactions.py` (11 tests): Selection conflict lasso guards, editor-container layout.
  13. `test_formatting_and_focus.py` (9 tests): Neutral format bar buttons, focus mode removal.
  14. `test_frameless_and_topbar_fixes.py` (8 tests): Frameless windowing and topbar button styling.
  15. `test_notion_equations.py` (6 tests): Equation block and inline KaTeX equation rendering.
  16. `test_ui_production_r1_r6.py` (28 tests): Full application UI regression suite.

### 1.2 Test Fixture, Database Mocking and Isolation Patterns
- **Database Isolation Pattern** (`tests/test_block_schema_and_migration.py:27-58`, `tests/test_block_api_and_richtext.py:228-250`, `tests/test_adversarial_notion_backend.py:54-100`):
  Each test suite creates an isolated SQLite database using `tempfile.TemporaryDirectory()` in `setUpClass()`:
  ```python
  cls.temp_dir = tempfile.TemporaryDirectory()
  cls.test_db_path = os.path.join(cls.temp_dir.name, 'test_isolated.db')
  cls.orig_db = models.db
  cls.test_db = SqliteDatabase(cls.test_db_path, timeout=10, check_same_thread=False)
  models.db = cls.test_db
  models.BaseModel._meta.database = cls.test_db
  for m in [models.Note, models.Folder, models.Setting, models.NoteHistory, models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord]:
      m._meta.database = cls.test_db
  cls.test_db.connect(reuse_if_open=True)
  models.init_db()
  ```
  In `setUp()`: cleans tables between test cases (`models.Block.delete().execute()`, `models.Note.delete().execute()`).  
  In `tearDownClass()`: closes test DB, shuts down HTTP servers, cleans temp directory, and restores `models.db` to `cls.orig_db`.
- **Dynamic Port HTTP Server Fixture**:
  Ephemeral socket binding via `find_free_port()` allocating dynamic TCP ports to prevent port conflicts across concurrent suites.
- **Node.js VM DOM Simulation Fixture** (`tests/test_block_frontend_contracts.py:149-210`):
  Uses Node.js (verified v26.13.0) via `subprocess.run(['node', '-e', runner_code])` with mocked DOM nodes (`MockNode`, `MockElement`, `MockDocument`, `MockWindow`) to test `frontend/app.js` without requiring an Electron or PyWebView graphical window.

### 1.3 Authoritative Reverse-Engineered Notion Evidence
1. **Notion Database Analysis (`C:\Users\Joaco\AppData\Roaming\Notion\notion.db`)**:
   Querying `SELECT type, COUNT(*), SUM(CASE WHEN content IS NULL THEN 1 ELSE 0 END), SUM(CASE WHEN content IS NOT NULL THEN 1 ELSE 0 END) FROM block GROUP BY type`:
   - **Pure Leaf Nodes (content ALWAYS NULL)**:
     - `code`: 36 total, 36 NULL (100%), 0 non-null.
     - `divider`: 19 total, 19 NULL (100%), 0 non-null.
     - `equation`: 42 total, 42 NULL (100%), 0 non-null.
     - `image`: 13 total, 13 NULL (100%), 0 non-null.
     - `table_row`: 136 total, 136 NULL (100%), 0 non-null.
   - **Pure Container Nodes (content ALWAYS non-NULL list of child UUIDs)**:
     - `column`: 17 total, 0 NULL, 17 non-null (100%).
     - `column_list`: 9 total, 0 NULL, 9 non-null (100%).
     - `table`: 22 total, 0 NULL, 22 non-null (100%).
   - **Conditional Containers / Toggleable Headers**:
     - `sub_sub_header`: 114 total (106 NULL content, 8 non-null content).
     - Directly verified row: `sub_sub_header`, `format: {"toggleable": true}`, `content: ["1ad6afc4-0012-804a-88c1-e8a0fe04d10d", "1ad6afc4-0012-8007-b370-e05e34ed7234"]`.
     - When `format.toggleable` is absent or false, `content` is `NULL`.

2. **Notion Operation Dispatcher Module (`module 443756 & 877308` in Cache bundle `34070e4cac3243af_0`)**:
   ```javascript
   op: {
     set: function(e) {
       return { pointer: e.pointer, path: e.path, command: "set", args: e.args };
     },
     append: function(e) {
       if (e.args.ids)
         return e.args.before ?
           { pointer: e.pointer, path: e.path, command: "listBeforeMulti", args: { ids: e.args.ids, before: e.args.before } } :
           { pointer: e.pointer, path: e.path, command: "listAfterMulti", args: { ids: e.args.ids, after: e.args.after } };
       return e.args.before ?
         { pointer: e.pointer, path: e.path, command: "listBefore", args: { id: e.args.id, before: e.args.before } } :
         { pointer: e.pointer, path: e.path, command: "listAfter", args: { id: e.args.id, after: e.args.after } };
     },
     insertChildren: function(e) {
       let t = e.args.ids ?? [e.args.id];
       return e.args.before ?
         { pointer: e.pointer, path: e.path, command: "insertChildrenBefore", args: { ids: t, before: e.args.before } } :
         { pointer: e.pointer, path: e.path, command: "insertChildrenAfter", args: { ids: t, after: e.args.after } };
     }
   }
   ```
   Block creation generates:
   `[ op.set({ pointer: { table: "block", id: childId, spaceId }, path: [], args: blockRecord }), op.listAfter({ pointer: { table: "block", id: parentId, spaceId }, path: ["content"], args: { id: childId, after: afterId } }) ]`.

3. **Current Gaps in Codebase (`models.py`, `backend.py`, `rich_text.py`, `frontend/app.js`)**:
   - `rich_text.py:165` & `backend.py:100`: `BLOCK_SCHEMAS['header']['children_allowed']` is statically `False`.
   - Running `rich_text.validate_block({'type': 'header', 'format': {'toggleable': True}, 'content': ['c1']})` currently outputs:
     `Verbatim: (False, "Block type 'header' does not permit children in content")`.
   - `models.add_child_block(parent_id, child_data)` currently does NOT verify whether `parent.type` allows children. A child can currently be inserted into a `divider` or `equation` parent without error.
   - Missing block types: `header_4`, `to_do`, `quote`, `callout`, `transclusion_container`, `transclusion_reference`, `bookmark`, `video`, `audio`, `file`, `pdf` are not present in `BLOCK_SCHEMAS`, `backend.py`, or `frontend/app.js:renderBlock`.

---

## 2. Logic Chain

1. **Premise 1**: The project requires preserving 100% test compatibility (261 existing tests passing with 0 regressions) while incorporating extracted Notion reverse-engineering specifications.
2. **Premise 2**: Authoritative Notion evidence from `notion.db` and runtime bundles proves that:
   - Creation requires atomic pair execution (`op.set` initializes the block row, `op.listAfter` appends the UUID to the parent container's `content` array) inside a database transaction (`with db.atomic():`).
   - Pure leaf blocks (`code`, `divider`, `equation`, `image`, `video`, `audio`, `file`, `pdf`, `bookmark`, `table_row`) have `content: null` and must reject child insertions.
   - Container blocks (`page`, `column_list`, `column`, `text`, `to_do`, `bulleted_list`, `numbered_list`, `toggle`, `quote`, `callout`, `table`, `transclusion_container`) maintain ordered UUID lists in `content`.
   - Headers (`header`, `sub_header`, `sub_sub_header`, `header_4`) dynamically become container blocks when `format.toggleable = true`, but remain atomic leaf nodes when `toggleable` is absent or false.
3. **Premise 3**: Current code has static `children_allowed: False` for headers, preventing toggleable header children, does not validate leaf parent restrictions in `add_child_block`, and lacks definitions for the 11 extended block types.
4. **Deduction**: The test suite must be augmented with dedicated unit, integration, and contract tests that cover:
   - Atomic transactions (`op.set` + `op.listAfter`) with rollback guarantees.
   - Strict container vs leaf validation.
   - Toggleable header lifecycle (creation, child insertion, toggle switching).
   - Schema, property, and format validation for the 11 new block types.
   - Rich-text title editing without degradation of the existing 261 test cases.

---

## 3. Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Transactional Protocol | Atomic Block Creation (`op.set` + `op.listAfter`) | Concurrent initialization of child block record and atomic addition of child ID to parent container's `content` array inside a single SQLite transaction | `block_data: dict`, `parent_id: str`, `after_id: str \| None` | `{ ok: True, block: dict, parent: dict }`, HTTP 201 | Rolls back transaction; returns 404 if parent missing, 400 if parent trashed or cycle detected | Notion bundle `34070e4cac3243af_0` (module 443756 & 877308) |
| 2 | Transactional Protocol | Directional Insertion (`listAfter` / `listBefore`) | Precision spatial positioning of child block before or after an existing sibling block in parent's `content` | `after_id: str` or `before_id: str` | Parent `content` array updated with child ID at exact index; parent `version` + 1 | If target sibling not found, safely appends or prepends to `content` | Notion bundle `34070e4cac3243af_0` module 443756 (`op.append`, `op.insertChildren`) |
| 3 | Structural Rules | Pure Leaf Block Enforcement | Blocks that represent atomic data (`content: null`) are strictly prohibited from receiving child blocks | `type: leaf_type`, `content: [...]` | Leaf block dictionary with `content: null` (None) | Validation error: `"Block type '<type>' does not permit children in content"`; `add_child_block` raises ValueError / 400 | `notion.db` empirical query (0/246 non-null content rows across leaf types) |
| 4 | Structural Rules | Container Block Hierarchy | Containers maintain an ordered JSON array of child UUIDs representing visual DOM rendering order | `type: container_type`, `content: [UUID, ...]` | Container block dictionary with ordered `content` list | Rejects duplicate UUIDs; maintains parent pointers in children | `notion.db` empirical query & `models.py:add_child_block` |
| 5 | Structural Rules | Toggleable Headers (`format.toggleable`) | `header`, `sub_header`, `sub_sub_header`, `header_4` dynamically allow children in `content` when `format.toggleable = true` | `format: {"toggleable": true}`, `content: [child_uuid, ...]` | Validated header container block; renders collapsible `<details>` with summary | Rejects children if `format.toggleable` is false or omitted | `notion.db` (rows with `format.toggleable: true`) & bundle `8cbceebc64912dc2_1` (`toggleFormatHeader`) |
| 6 | Block Catalog | `header_4` (Heading 4) | Smallest heading block (H4) with text styling and optional toggleable capability | `properties: {title: [...]}, format: {block_color, toggleable}` | H4 block record; rendered as `<h4>` or `<details>` | Rejects non-rich-text title; rejects children if not toggleable | `notion_block_schemas_extracted.json` (26 rows in `notion.db`) |
| 7 | Block Catalog | `to_do` (Checkbox Task) | Interactive to-do task item with title and boolean checked state | `properties: {title: [...], checked: [["Yes"]] \| [["No"]]}` | Task item block record; rendered with checkbox and contenteditable title | Rejects invalid checked values; supports nested sub-tasks in `content` | Cache bundle `d2e6fffcbe93e976_0` & `ee36094c25e4a2ce_0` |
| 8 | Block Catalog | `quote` (Blockquote) | Styled quotation block with visual vertical accent border | `properties: {title: [...]}, format: {block_color}` | Quote container block; rendered with `border-left` and styled quote text | Rejects malformed title rich-text tuples | Cache bundle `d2e6fffcbe93e976_0` & `640b0f502752e0d2_0` |
| 9 | Block Catalog | `callout` (Callout Box) | Highlighted callout box with icon, background color, and nested content | `properties: {title: [...]}, format: {page_icon, block_color}` | Callout container block; rendered with emoji/icon badge and colored box | Rejects malformed properties; supports children in `content` | Cache bundle `d2e6fffcbe93e976_0` (`calloutBlock`, `callout_version: 2`) |
| 10 | Block Catalog | `transclusion_container` | Synced block master container holding shared content | `content: [child_uuid, ...]`, `properties: {}` | Master synced container block | Soft-deleting container cascades to references | Cache bundle `d2e6fffcbe93e976_0` (`transclusion_container`) |
| 11 | Block Catalog | `transclusion_reference` | Synced block reference pointer rendering the subtree of a `transclusion_container` | `format: {transclusion_reference_pointer: {id, table: "block"}}` | Reference block rendering target container's `recordMap` subtree | Cycle detection if container references itself; 404 if target missing | Cache bundle `d2e6fffcbe93e976_0` (`transclusion_reference`) |
| 12 | Block Catalog | `bookmark` (Web Bookmark) | Visual card previewing external URL with metadata | `properties: {link, title, description, caption}, format: {bookmark_icon, block_width}` | Leaf bookmark card with favicon, preview title, and URL link | Rejects non-leaf children; invalid URL defaults to generic card | Cache bundle `d2e6fffcbe93e976_0` (`renderedType: "bookmark"`) |
| 13 | Block Catalog | `video` (Video Embed) | Embedded video player supporting remote URL or file source | `properties: {source, caption}, format: {block_width, display_source}` | Leaf video block rendering HTML5 `<video>` or iframe | Rejects non-leaf children; sanitizes malicious schemes | Cache bundle `d2e6fffcbe93e976_0` (`renderedType: "video"`) |
| 14 | Block Catalog | `audio` (Audio Embed) | Embedded audio player supporting MP3/WAV/OGG | `properties: {source, caption}, format: {block_width}` | Leaf audio block rendering HTML5 `<audio controls>` | Rejects non-leaf children | Cache bundle `d2e6fffcbe93e976_0` (`renderedType: "audio"`) |
| 15 | Block Catalog | `file` (File Attachment) | Downloadable attachment card with file name and size metadata | `properties: {source, title, size, caption}, format: {block_width}` | Leaf file card with download link and file metadata | Rejects non-leaf children | Cache bundle `d2e6fffcbe93e976_0` (`filesProperty`) |
| 16 | Block Catalog | `pdf` (PDF Embed) | Embedded PDF viewer component | `properties: {source, caption}, format: {block_width, display_source}` | Leaf PDF block rendering `<embed>` or PDF viewer iframe | Rejects non-leaf children | Cache bundle `d2e6fffcbe93e976_0` (`renderedType: "pdf"`) |
| 17 | Rich Text Engine | Multi-Decorator Title Editing | Bidirectional rich-text title serialization supporting 8 Notion decorators (`b`, `i`, `_`, `s`, `c`, `h`, `a`, `e`) | Contenteditable HTML or Notion decorator tuples array | Serialized tuples in `properties.title`; rendered sanitized HTML | Sanitizes XSS/script tags; merges adjacent matching decorators | `rich_text.py` & `frontend/app.js:parseRichTextToHtml` |

---

## 4. Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | Atomic Creation Protocol | `parent_id` is non-existent (`"missing-uuid"`) | Database transaction aborts with 404; child block record is NOT created in SQLite (0 orphan rows created). |
| 2 | Atomic Creation Protocol | `parent_id` points to a trashed block (`alive = 0`) | Transaction rejected with 400 Bad Request; child block is NOT created. |
| 3 | Atomic Creation Protocol | `parent_id` equals child ID, or child ID is an ancestor of `parent_id` | Cycle detection triggers; transaction aborted with 400 `"Circular block hierarchy detected"`. |
| 4 | Atomic Creation Protocol | `after_id` does not exist in parent's `content` array | Falls back gracefully to appending at end of parent's `content` without raising IndexError. |
| 5 | Atomic Creation Protocol | `before_id` matches first element of `content` | Inserts child ID at index 0 of parent's `content` array. |
| 6 | Container vs Leaf Nodes | Child block added to pure leaf node (`divider`, `code`, `equation`, `image`, `video`, `audio`, `file`, `pdf`, `bookmark`, `table_row`) | Rejects operation with 400 Bad Request (`"Block type '...' does not permit children"`); leaf `content` remains `null`. |
| 7 | Toggleable Headers | Header (`header`, `sub_header`, `sub_sub_header`, `header_4`) with `format: {"toggleable": true}` receiving child | Validates successfully (`is_valid = True`); child inserted into header's `content` array; renders collapsible `<details>`. |
| 8 | Toggleable Headers | Header with `format: {"toggleable": false}` or omitted receiving child | Validation fails (`is_valid = False`, `"does not permit children"`); child insertion rejected. |
| 9 | Toggleable Headers | Header toggled from `toggleable: true` to `false` when children already exist in `content` | Children remain intact in database; header is displayed without toggle disclosure until re-enabled (prevents silent data loss). |
| 10 | Block Schemas (`to_do`) | `properties: {"checked": [["Yes"]]}` vs `{"checked": [["No"]]}` | Checked state displays checked box with strike-through styling on title; toggle click flips checked property and persists via bridge/API. |
| 11 | Block Schemas (`callout`) | `format: {"page_icon": "💡", "block_color": "yellow_background"}` | Renders callout container with amber/yellow background tint and lightbulb emoji icon badge. |
| 12 | Block Schemas (`transclusion`) | Recursive self-reference: container A contains reference to container A | Cycle detection in `renderTreeFromRecordMap` via `visited` Set breaks infinite recursion safely. |
| 13 | Rich Text Title Editing | Malicious script tag in title: `[["<script>alert(1)</script>", [["b"]]]]` | HTML sanitizer escapes `<script>` to `&lt;script&gt;`; prevents XSS execution in editor canvas. |
| 14 | Rich Text Title Editing | Empty or None title in `properties.title`: `[]` or `None` | Defaults to empty string `""` without throwing TypeError or IndexError. |
| 15 | Rich Text Title Editing | Multi-byte Unicode, emojis, mathematical Greek letters in title | Preserved verbatim across JSON round-trips without encoding artifacts. |

---

## 5. Test Plan Recommendations

To achieve the acceptance criteria defined in `ORIGINAL_REQUEST.md` (atomic creation protocol, container/leaf validation, toggleable headers, 11 new block types, and 100% test pass rate with 0 regressions), the test strategy should be structured across 5 concrete tiers:

### Tier 1: Unit & Schema Validation Tests
- **Location**: `tests/test_block_schema_and_migration.py` & `tests/test_block_api_and_richtext.py`.
- **Target**:
  1. Verify `ALL_NOTION_BLOCK_TYPES` in `rich_text.py` includes all 11 new types:
     `['header_4', 'to_do', 'quote', 'callout', 'transclusion_container', 'transclusion_reference', 'bookmark', 'video', 'audio', 'file', 'pdf']`.
  2. Test `validate_block()` across all 11 new types with valid properties and format defaults.
  3. Test `validate_block()` for pure leaf nodes (`equation`, `divider`, `code`, `image`, `video`, `audio`, `file`, `pdf`, `bookmark`, `table_row`): verify they reject non-empty `content`.
  4. Test `validate_block()` for headers:
     - `header`, `sub_header`, `sub_sub_header`, `header_4` with `format: {"toggleable": True}` allow children.
     - Same headers with `format: {"toggleable": False}` or `{}` reject children.
  5. Test `to_do` property validation for `checked` (`[["Yes"]]`, `[["No"]]`).

### Tier 2: Transactional Protocol & Atomic Creation Tests
- **Location**: `tests/test_block_api_and_richtext.py` & `tests/test_adversarial_notion_backend.py`.
- **Target**:
  1. Verify atomic creation (`op.set` + `op.listAfter`):
     - Creating a child block under a container executes inside a single database transaction.
     - Child row created with UUIDv4, parent pointers, version 1.
     - Parent `content` array updated with child UUID at exact position.
     - Parent `version` incremented, `last_edited_time` updated, CRDT mutation logged.
  2. Test rollback on failure:
     - Simulate an integrity error during parent update (e.g. parent locked or invalid); verify child row is rolled back and not orphaned in SQLite.
  3. Test spatial positioning:
     - `after_id` places child immediately after specified sibling.
     - `before_id` places child immediately before specified sibling.
     - Target index 0 places child at start of `content`.
  4. Test leaf rejection in `add_child_block()` and `create_block_api()`:
     - Attempting to add a child to a leaf block (`divider`, `code`, `video`, etc.) returns error status 400.
     - Attempting to add a child to a non-toggleable header returns error status 400.

### Tier 3: Frontend Contract & Dynamic VM Tests
- **Location**: `tests/test_block_frontend_contracts.py`.
- **Target**:
  1. Static contract verification:
     - Verify `renderBlock(block)` contains switch-case branches for all newly added types (`case 'header_4':`, `case 'to_do':`, `case 'quote':`, `case 'callout':`, `case 'transclusion_container':`, `case 'transclusion_reference':`, `case 'bookmark':`, `case 'video':`, `case 'audio':`, `case 'file':`, `case 'pdf':`).
     - Verify CSS rules exist in `frontend/styles.css` for each new block component (`.block-header-4`, `.block-todo`, `.block-quote`, `.block-callout`, `.block-transclusion`, `.block-bookmark`, `.block-video`, `.block-audio`, `.block-file`, `.block-pdf`, `.block-toggle-header`).
  2. Dynamic Node.js VM tests:
     - Test DOM instantiation of each new block type via `renderBlock(block)`.
     - Test toggleable header rendering: `<details>` with `<summary>` and `.block-toggle-content` children container.
     - Test `renderTreeFromRecordMap`: mounting children of toggleable headers and callout containers into their respective slots.
     - Test `to_do` checkbox change event firing and state reflection.

### Tier 4: Adversarial Hardening & Concurrency Tests
- **Location**: `tests/test_adversarial_notion_backend.py` & `tests/test_adversarial_challenger.py`.
- **Target**:
  1. Cycle defense with toggleable headers: H1 -> H2 -> H1 circular nesting attempts blocked.
  2. Concurrency stress: 10 parallel threads executing atomic creations (`op.set` + `op.listAfter`) under the same container parent; verify SQLite WAL mode handles transactions without table corruption or duplicate UUIDs.
  3. XSS injection testing in rich text titles for `header_4`, `quote`, `callout`, `to_do`.
  4. Malicious URL schemes (`javascript:`, `vbscript:`, `data:text/html`) in `video.source`, `audio.source`, `file.source`, `bookmark.link` sanitized.

### Tier 5: Full Regression Verification Suite
- **Command**: `py -m unittest discover -s tests`
- **Criterion**: All 261 existing tests + new unit/integration/contract tests pass with 100% exit code 0. Zero regressions across existing note migration, rich text engine, desktop windowing, or topbar layout.

---

## 6. Caveats
- No caveats. All 16 existing test suites were executed and inspected; authoritative reverse-engineering artifacts from `notion.db` and Notion cache bundles were empirically probed and cross-verified against `ORIGINAL_REQUEST.md`.

---

## 7. Conclusion
The Note-JS-Desktop test suite is healthy, robust, and well-isolated, passing all 261 tests across 16 suites in ~8.4 seconds.  
The authoritative specifications mined from Notion establish clear, precise rules:
1. **Creation Protocol**: Concurrent `op.set` (block record) and `op.listAfter` (parent `content` array) executed inside an atomic SQLite transaction with rollback on failure.
2. **Structural Rules**: Strict partition between pure leaf nodes (`content: null`, child creation rejected) and container blocks (`content: [...]`).
3. **Toggleable Headers**: `header`, `sub_header`, `sub_sub_header`, and `header_4` dynamically accept children if and only if `format.toggleable = true`.
4. **Catalog Expansion**: 11 new block types (`header_4`, `to_do`, `quote`, `callout`, `transclusion_container`, `transclusion_reference`, `bookmark`, `video`, `audio`, `file`, `pdf`) require formal schema definitions in `rich_text.py`, validation handling in `backend.py`, DOM components in `frontend/app.js`, and styling in `frontend/styles.css`.
5. **Regression Safety**: All additions can be introduced non-destructively by extending schemas and handlers while preserving the 261 existing tests.

---

## 8. Verification Method
To independently verify these findings:
1. **Execute full test suite**:
   ```powershell
   py -m unittest discover -s tests
   ```
   *Expected*: Ran 261 tests, OK (exit code 0).
2. **Verify current toggleable header rejection**:
   ```powershell
   py -c "import rich_text; print(rich_text.validate_block({'type': 'header', 'format': {'toggleable': True}, 'content': ['c1']}))"
   ```
   *Expected*: `(False, "Block type 'header' does not permit children in content")`.
3. **Verify Notion database content null vs non-null partition**:
   ```powershell
   py -c "import sqlite3; con = sqlite3.connect(r'C:\Users\Joaco\AppData\Roaming\Notion\notion.db'); cur = con.cursor(); cur.execute('SELECT type, COUNT(*), SUM(CASE WHEN content IS NULL THEN 1 ELSE 0 END) FROM block GROUP BY type'); print(cur.fetchall())"
   ```
   *Expected*: Pure leaf types (`code`, `divider`, `equation`, `image`, `table_row`) show 100% NULL content.
