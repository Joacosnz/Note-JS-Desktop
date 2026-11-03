# Backend Architecture Survey & REA Transaction Analysis — Handoff Report

## 1. Observation

### 1.1 Backend Core Files and Data Layer Architecture
- **Database & Storage Layer**:
  - SQLite database located at `notejs.db` (or resolved dynamically via `get_data_dir()` in `models.py:33-52` to handle frozen PyInstaller paths and `%APPDATA%/NoteJS`).
  - Database Pragmas (`models.py:56-67`):
    ```python
    db = SqliteDatabase(
        DB_PATH,
        pragmas={
            'journal_mode': 'wal',
            'cache_size': -64000,  # 64MB cache
            'foreign_keys': 1,
            'synchronous': 1,
            'busy_timeout': 10000, # 10s busy timeout
        },
        timeout=15,
        check_same_thread=False,
    )
    ```
  - Thread safety lock (`models.py:53`): `DB_LOCK = threading.RLock()`.
  - ORM: Peewee ORM (`peewee.py`), with `BaseModel(Model)` inheriting `database = db` (`models.py:70-73`).

### 1.2 Canonical Block Model Schema (`models.py:249-396`)
- Model definition: `class Block(BaseModel):` mapped to SQLite table `block` (`models.py:279`).
- Compatibility view: `_ensure_block_table_and_view()` in `models.py:661-732` creates a SQLite `VIEW blocks AS SELECT * FROM block;` so that both `block` and `blocks` table queries resolve seamlessly.
- **16 Notion canonical fields**:
  1. `id`: `CharField(primary_key=True, max_length=64)` (stores UUIDv4 string).
  2. `space_id`: `CharField(max_length=64, default='default_space', index=True)`.
  3. `version`: `IntegerField(default=1)`.
  4. `last_version`: `IntegerField(default=1)`.
  5. `type`: `CharField(max_length=64, default='text', index=True)`.
  6. `properties`: `TextField(default='{}')` (stores JSON dictionary of property arrays, e.g. rich-text tuples `{"title": [["text", [["b"]]]]}`).
  7. `content`: `TextField(default='[]')` (stores JSON array of child UUID strings in visual render order).
  8. `parent_id`: `CharField(max_length=64, null=True, index=True)`.
  9. `parent_table`: `CharField(max_length=64, default='block')`.
  10. `alive`: `IntegerField(default=1, index=True)` (1 for active, 0 for soft-deleted).
  11. `format`: `TextField(default='{}')` (stores JSON dictionary for visual formatting properties).
  12. `crdt_format_version`: `IntegerField(default=1)`.
  13. `crdt_data`: `TextField(default='{}')` (stores mutation vector log and vector clock JSON).
  14. `created_time`: `BigIntegerField(default=lambda: int(time.time() * 1000))`.
  15. `last_edited_time`: `BigIntegerField(default=lambda: int(time.time() * 1000), index=True)`.
  16. `permissions`: `TextField(default='[]')`.
- **4 Backwards-compatible legacy fields**:
  `note_id` (IntegerField null=True, default=0), `sort_index` (CharField(64), default='a0'), `created_at` (DateTimeField), `updated_at` (DateTimeField).
- `Block.to_dict()` (`models.py:281-396`): Deserializes JSON fields (`properties`, `content`, `format`, `crdt_data`, `permissions`) and outputs both canonical Notion keys and legacy keys (`noteId`, `parentId`, `sortIndex`, `createdAt`, `updatedAt`, `page_id`, `title`).

### 1.3 Existing Block Creation, Reordering & Hierarchy Operations
- **ID Generation**: `uuid.uuid4()` is generated as a standard 36-character string (`backend.py:296`, `models.py:1011`).
- **Parent/Child Relationships**:
  - Container blocks maintain an ordered JSON list of child UUID strings in `content`: e.g. `'["uuid-1", "uuid-2"]'`.
  - Child blocks store `parent_id = str(parent_id)` and `parent_table = 'block'`.
- **Block Creation Flow**:
  - `backend.py:287-414` (`create_block_api`):
    - Validates block via `rich_text.validate_block(bdata)` (`backend.py:302`).
    - If `parent_id` is supplied: validates parent exists, is active (`alive == 1`), not self-parenting, and walks up ancestors to detect circular references (`backend.py:328-337`).
    - Determines insertion index from `after_id`, `before_id`, or `target_index` (`backend.py:347-356`).
    - Calls `models.add_child_block(parent_id, child_dict, index=idx)` (`backend.py:371`).
    - If no `parent_id` (root block): creates record via `Block.create(...)` within `with db.atomic():` (`backend.py:380-412`).
  - `models.py:984-1110` (`add_child_block`):
    - Operates inside `with db.atomic():`.
    - Inserts the new block record with `parent_id=parent_id`, `parent_table='block'`.
    - Loads `parent.content` (deserializing JSON array).
    - Inserts `child_id` at `index` (or appends to end).
    - Serializes `parent.content` back to JSON.
    - Increments `parent.version += 1`, updates timestamps.
    - Appends mutation record to `parent.crdt_data['mutations']`:
      `{'op': 'add_child', 'child_id': child_id, 'index': index, 'timestamp': now_ms, 'version': parent.version}`.
    - Saves `parent`.
- **Moving & Reordering**:
  - `models.move_child_block(child_id, new_parent_id, index=None)` (`models.py:1112-1293`): Removes `child_id` from old parent's `content`, inserts into new parent's `content`, updates child's `parent_id` and records CRDT mutations.
  - `models.reorder_children(parent_id, new_content_order)` (`models.py:1295-1341`): Directly overwrites parent's `content` array with new list of UUID strings.
- **Soft Deletion & Restoration**:
  - `models.soft_delete_block(block_id)` (`models.py:1343-1444`): Sets `alive = 0`, removes `child_id` from parent's `content`, and cascades `alive = 0` recursively to all descendants.
  - `models.restore_block(block_id)` (`models.py:1446-1525`): Sets `alive = 1`, and if parent is alive, appends `block_id` back into parent's `content`.

### 1.4 Notion Transaction Operations Extracted from Cache Bundle
- Direct inspection of Notion's production JavaScript bundle (`34070e4cac3243af_0`, modules 789680 and 455472) reveals:
  ```javascript
  // Module 789680: Transaction operations for content array
  function s(e) {
      return {
          pointer: { table: "block", id: e.blockParentId },
          path: ["content"],
          command: "insertChildrenAfter",
          args: { ids: [e.recordId], after: e.afterId }
      };
  }
  function l(e) {
      return {
          pointer: { table: "block", id: e.blockParentId },
          path: ["content"],
          command: "removeChild",
          args: { id: e.recordId }
      };
  }
  // List command dispatch in client bundle:
  command: "listAfter", args: { id: e.args.id, after: e.args.after }
  command: "listBefore", args: { id: e.args.id, before: e.args.before }
  command: "set", pointer: f, path: [], args: (0, r(455472).hA)(n)
  ```
- In Notion, atomic block creation consists of two concurrent operations executed in a single atomic transaction:
  1. `op.set`: initializes the block record with UUIDv4, type, parent pointers, properties, format, alive=1, space_id, version=1, crdt_data.
  2. `op.listAfter` (or `op.insertChildrenAfter`): registers the new block's UUID in the `content` array of the parent container block immediately after `afterId` (or at the beginning if after is empty/None).
- **Current Project Status**: Neither `op.set`, `op.listAfter`, nor an operation dispatcher exists in `models.py` or `backend.py`. The project uses procedural Peewee ORM calls (`add_child_block`) instead of an operation-based transaction protocol.

### 1.5 Container Blocks vs Leaf Nodes & `format.toggleable` (Notion DB Evidence)
- Empirical query on extracted `notion.db` (`1656` blocks total across 20 types):
  ```
  bulleted_list: has_content=32, no_content=226
  code:          has_content=0,  no_content=36
  column:        has_content=17, no_content=0
  column_list:   has_content=9,  no_content=0
  divider:       has_content=0,  no_content=19
  equation:      has_content=0,  no_content=42
  header:        has_content=0,  no_content=10
  header_4:      has_content=0,  no_content=26
  image:         has_content=0,  no_content=13
  numbered_list: has_content=2,  no_content=53
  page:          has_content=26, no_content=14
  sub_header:    has_content=0,  no_content=49
  sub_sub_header:has_content=8,  no_content=106
  table:         has_content=22, no_content=0
  table_row:     has_content=0,  no_content=136
  text:          has_content=5,  no_content=763
  toggle:        has_content=28, no_content=2
  ```
- **Toggleable Headers Evidence**:
  In `notion.db`:
  `('sub_sub_header', '{"toggleable":true}', '["1ad6afc4-0012-804a-88c1-e8a0fe04d10d","1ad6afc4-0012-8007-b370-e05e34ed7234"]')`
  When `format.toggleable = true`, headers (`header`, `sub_header`, `sub_sub_header`, `header_4`) become container blocks containing child UUIDs in their `content` array.
- **Current Project Status**:
  In `rich_text.py:416-439`, `header`, `sub_header`, `sub_sub_header` have `'children_allowed': False` hardcoded, and `allowed_format` is limited to `{'block_color'}`.
  `validate_block` (`rich_text.py:639-640`) rejects any header that has items in `content`.
  Furthermore, `header_4` does not exist in `BLOCK_SCHEMAS`.

### 1.6 Current Test Suite Baseline
- Command: `py -m unittest discover -s tests`
- Result: `Ran 261 tests in 10.016s — OK` (100% passing, 0 errors, 0 regressions).

---

## 2. Logic Chain

1. **Transaction Protocol Gap**:
   - *Observation*: Notion bundle analysis establishes that Notion client operations emit `op.set` (to create the block record) and `op.listAfter` / `op.insertChildrenAfter` (to append/insert the child UUID into parent's `content`).
   - *Observation*: Note-JS-Desktop currently creates blocks via `add_child_block` in `models.py` which imperatively modifies the parent row and inserts a child row within `with db.atomic():`.
   - *Inference*: To satisfy R1, `models.py` requires a formal operation schema and executor:
     - Operation dictionary structures matching Notion: `op.set`, `op.listAfter`, `op.listBefore`, `op.listRemove`, `op.update`.
     - Transaction runner `apply_transaction(operations)` / `execute_transaction(operations)` that atomically executes `op.set` + `op.listAfter` inside SQLite `with db.atomic():`.
     - Creation helper `build_atomic_block_creation_ops(...)` that builds the `[op.set, op.listAfter]` list and executes it.
     - Integration into `backend.py:create_block_api` and `desktop_app.py:PyWebViewBridge`.

2. **Container vs Atomic Leaf Node Rules**:
   - *Observation*: In Notion, container blocks (`page`, `column_list`, `column`, `text`, `to_do`, `bulleted_list`, `numbered_list`, `toggle`, `quote`, `callout`, `table`, `transclusion_container`) have `content: [UUID, ...]`. Atomic leaf blocks (`equation`, `divider`, `code`, `image`, `video`, `audio`, `file`, `pdf`, `bookmark`, `table_row`, `transclusion_reference`) have `content: null` (None in Python).
   - *Observation*: In `rich_text.py`, `BLOCK_SCHEMAS` only defines 17 types. Container definitions miss `to_do`, `quote`, `callout`, `transclusion_container`. Leaf definitions miss `video`, `audio`, `file`, `pdf`, `bookmark`, `transclusion_reference`.
   - *Inference*: The schema must be updated with:
     - `CONTAINER_BLOCK_TYPES`: `{'page', 'column_list', 'column', 'text', 'to_do', 'bulleted_list', 'numbered_list', 'toggle', 'quote', 'callout', 'table', 'transclusion_container'}`.
     - `LEAF_BLOCK_TYPES`: `{'equation', 'divider', 'code', 'image', 'video', 'audio', 'file', 'pdf', 'bookmark', 'table_row', 'transclusion_reference', 'sub_page'}`.
     - `TOGGLEABLE_HEADER_TYPES`: `{'header', 'sub_header', 'sub_sub_header', 'header_4'}`.
     - Container rule: A block is a container iff:
       `(type in CONTAINER_BLOCK_TYPES) or (type in TOGGLEABLE_HEADER_TYPES and format.get('toggleable') is True)`.
     - Leaf rule: If a block is not a container, `content` must either be `None` (`null`) or empty `[]`. Non-empty `content` on a leaf block fails validation.

3. **Toggleable Headers Handling**:
   - *Observation*: Currently `header`, `sub_header`, `sub_sub_header` in `rich_text.py` have `'children_allowed': False` and `allowed_format = {'block_color'}`.
   - *Observation*: In Notion, `header_4` also exists as Heading 4, and all 4 heading levels can be toggled via `format.toggleable = True`.
   - *Inference*:
     - Add `header_4` to `BLOCK_SCHEMAS`.
     - Add `'toggleable'` to `allowed_format` for `header`, `sub_header`, `sub_sub_header`, `header_4`.
     - Update `rich_text.validate_block` to dynamically evaluate container status using the rule:
       `children_allowed = schema['children_allowed'] or (btype in TOGGLEABLE_HEADER_TYPES and bool(fmt.get('toggleable')))`
     - When `toggleable` is True, `content` may contain child UUIDs and `add_child_block` can append children under the header.

4. **Missing Block Catalog Schemas (R2)**:
   - *Observation*: Notion bundle analysis and `notion_block_schemas_extracted.json` provide explicit properties and formats for `header_4`, `to_do`, `quote`, `callout`, `transclusion_container`, `transclusion_reference`, `video`, `audio`, `file`, `pdf`, `bookmark`.
   - *Inference*: Defining canonical schemas for each of these in `rich_text.BLOCK_SCHEMAS` will complete the backend block catalog while maintaining rich-text tuple compatibility in `properties.title`.

5. **Backward Compatibility Preservation (R4)**:
   - *Observation*: All 261 existing tests verify existing block types, REST endpoints, bridge calls, and database operations.
   - *Inference*: The transactional creation operations (`op.set`, `op.listAfter`) must directly integrate into `create_block_api` and `add_child_block` in a manner that preserves their return formats (`{'ok': True, 'block': ...}`).

---

## 3. Caveats

1. **Frontend Rendering Scope**: This investigation focused strictly on backend storage, ORM, schemas, transaction operations, and validation. Frontend rendering in `frontend/app.js` and styling in `frontend/styles.css` will be surveyed and implemented by the frontend specialist.
2. **CRDT Text Merging**: While the local vector clock (`clock`) and mutation vector (`mutations`) in `crdt_data` are fully tracked and maintained in SQLite, multi-user real-time operational transformation (OT/CRDT) over WebSockets is not currently part of Note-JS-Desktop's single-user local architecture.
3. **No Caveats on Database Migrations**: SQLite table `block` has dynamic column addition via `_ensure_block_table_and_view()`, so schema additions do not require destructive table recreations.

---

## 4. Conclusion

### 4.1 Required Backend Changes Summary

| Target File | Area | Proposed Modification |
|---|---|---|
| `models.py` | Transaction Protocol | Implement `build_op_set`, `build_op_list_after`, `apply_operation`, and `apply_transaction(operations)` executing atomic `[op.set, op.listAfter]` within SQLite transactions (`with db.atomic():`). Update `add_child_block` to execute via this protocol. |
| `models.py` | Content Null Handling | In `Block.to_dict()` and `Block` model, distinguish container `content: [...]` from atomic leaf `content: null`. |
| `rich_text.py` | Block Types | Add `header_4`, `to_do`, `quote`, `callout`, `transclusion_container`, `transclusion_reference`, `video`, `audio`, `file`, `pdf`, `bookmark` to `ALL_NOTION_BLOCK_TYPES`. |
| `rich_text.py` | Block Schemas | Populate `BLOCK_SCHEMAS` with exact properties, format definitions, and container flags for all new block types. |
| `rich_text.py` | Dynamic Container Validation | Update `validate_block` to allow children in `header`, `sub_header`, `sub_sub_header`, and `header_4` when `format.toggleable = True`, and reject children on leaf nodes. |
| `backend.py` | REST API & Bridge | Refactor `create_block_api` to execute atomic block creation using `op.set` + `op.listAfter` transactional operations. Add optional endpoint `POST /api/transactions`. |
| `desktop_app.py` | PyWebView Bridge | Expose `apply_transaction` / `create_block_transactional` to `PyWebViewBridge`. |

### 4.2 Proposed Canonical Schema Specifications for New Block Types

```python
NEW_BLOCK_SCHEMAS = {
    'header_4': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color', 'toggleable'},
        'children_allowed': False,  # True dynamically when format.toggleable == True
        'default_properties': {'title': []},
        'default_format': {},
    },
    'to_do': {
        'family': 'text',
        'allowed_properties': {'title', 'checked'},
        'allowed_format': {'block_color'},
        'children_allowed': True,
        'default_properties': {'title': [], 'checked': [['No', []]]},
        'default_format': {},
    },
    'quote': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {},
    },
    'callout': {
        'family': 'text',
        'allowed_properties': {'title'},
        'allowed_format': {'block_color', 'page_icon'},
        'children_allowed': True,
        'default_properties': {'title': []},
        'default_format': {'page_icon': '💡', 'block_color': 'gray_background'},
    },
    'transclusion_container': {
        'family': 'structural',
        'allowed_properties': set(),
        'allowed_format': set(),
        'children_allowed': True,
        'default_properties': {},
        'default_format': {},
    },
    'transclusion_reference': {
        'family': 'structural',
        'allowed_properties': set(),
        'allowed_format': {'transclusion_reference_pointer'},
        'children_allowed': False,
        'default_properties': {},
        'default_format': {'transclusion_reference_pointer': {}},
    },
    'video': {
        'family': 'media',
        'allowed_properties': {'source', 'caption'},
        'allowed_format': {'block_width', 'block_alignment', 'display_source'},
        'children_allowed': False,
        'default_properties': {'source': [['', []]], 'caption': []},
        'default_format': {'block_width': 700, 'block_alignment': 'center'},
    },
    'audio': {
        'family': 'media',
        'allowed_properties': {'source'},
        'allowed_format': {'block_width', 'block_alignment'},
        'children_allowed': False,
        'default_properties': {'source': [['', []]]},
        'default_format': {},
    },
    'file': {
        'family': 'media',
        'allowed_properties': {'source', 'title', 'size'},
        'allowed_format': {'block_color'},
        'children_allowed': False,
        'default_properties': {'source': [['', []]], 'title': [['', []]], 'size': [['', []]]},
        'default_format': {},
    },
    'pdf': {
        'family': 'media',
        'allowed_properties': {'source'},
        'allowed_format': {'block_width', 'block_height', 'block_alignment'},
        'children_allowed': False,
        'default_properties': {'source': [['', []]]},
        'default_format': {'block_width': 700, 'block_height': 500, 'block_alignment': 'center'},
    },
    'bookmark': {
        'family': 'media',
        'allowed_properties': {'link', 'title', 'description', 'caption'},
        'allowed_format': {'bookmark_icon', 'bookmark_cover'},
        'children_allowed': False,
        'default_properties': {'link': [['', []]], 'title': [], 'description': [], 'caption': []},
        'default_format': {},
    },
}
```

---

## 5. Verification Method

1. **Automated Test Suite Execution**:
   Run the full project test suite in powershell:
   ```powershell
   py -m unittest discover -s tests
   ```
   *Expected*: All existing 261 tests must pass with 0 failures and 0 errors.

2. **Schema and Validation Verification**:
   Verify via python CLI that `is_valid_block_type` returns `True` for each of the new block types and that `validate_block` permits children for headers when `format={'toggleable': True}` and forbids them when `format={'toggleable': False}`:
   ```powershell
   py -c "import rich_text; print(all(rich_text.is_valid_block_type(t) for t in ['header_4', 'to_do', 'quote', 'callout', 'transclusion_container', 'transclusion_reference', 'video', 'audio', 'file', 'pdf', 'bookmark']))"
   ```

3. **Transactional Operation Protocol Verification**:
   Inspect `models.py` and `backend.py` to confirm that:
   - `build_op_set(...)` generates `{pointer: {table: 'block', id: ...}, command: 'set', args: ...}`.
   - `build_op_list_after(...)` generates `{pointer: {table: 'block', id: ...}, path: ['content'], command: 'listAfter', args: ...}`.
   - `apply_transaction(...)` applies both in a single atomic SQLite commit.

4. **Invalidation Conditions**:
   The findings would be invalidated if:
   - Any of the 261 existing tests break.
   - Leaf blocks with `content: null` cause unhandled JSON parsing exceptions in existing frontend or API serialization code.
   - The transaction system fails to reject circular parent references.
