# Project: Note-JS-Desktop Notion Block System & Transactional Protocol

## Architecture
Note-JS-Desktop implements a local-first desktop workspace with a Notion-compatible block architecture.
- **Backend / Persistence Layer (`models.py`, `backend.py`)**: SQLite database via Peewee ORM with WAL mode, RLock thread-safety, and canonical `Block` model (16 Notion fields, UUIDv4 IDs, JSON-serialized properties/format/content/crdt_data).
- **Transactional Protocol (`models.py`, `backend.py`)**: Atomic block creation executing concurrent `op.set` (block record initialization) and `op.listAfter` (parent container `content` array registration) inside SQLite transactions (`with db.atomic():`).
- **Rich Text & Structural Engine (`rich_text.py`)**: Block taxonomy, canonical schemas, property validation, container vs atomic leaf rules (`content: [UUID, ...]` vs `content: null`), and dynamic toggleable headers (`format.toggleable = true`).
- **Frontend Editor Canvas (`frontend/app.js`, `frontend/styles.css`)**: In-memory `recordMap` store, recursive tree renderer `renderTreeFromRecordMap`, DOM element factory `renderBlock`, bidirectional rich-text serializer (`properties.title`), interactive slash commands, and block action menus.
- **Desktop Bridge (`desktop_app.py`)**: PyWebView bridge communicating between the web frontend and Python backend models/APIs.

## Code Layout
- `models.py`: Database initialization, Peewee models (`Block`, `Note`, etc.), transactional operations (`apply_transaction`, `build_op_set`, `build_op_list_after`), hierarchy manipulation (`add_child_block`, `move_child_block`).
- `rich_text.py`: Notion block types (`ALL_NOTION_BLOCK_TYPES`), canonical schemas (`BLOCK_SCHEMAS`), validation engine (`validate_block`), rich text tuple conversion.
- `backend.py`: REST API endpoints, block CRUD APIs (`create_block_api`, `update_block_api`), transaction endpoints.
- `desktop_app.py`: PyWebView desktop wrapper and API bridge.
- `frontend/app.js`: Client runtime, DOM block rendering, tree mounting, rich text editing, slash menu.
- `frontend/styles.css`: CSS styles for desktop layout, block components, and color themes.
- `tests/`: Automated unit, integration, contract, and adversarial test suites.

## Feature Inventory
Every feature from the Survey phase must appear here with its assigned milestone. No feature may be left unassigned.
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Atomic Block Creation (`op.set` + `op.listAfter`) | Concurrent block record creation and parent `content` insertion within atomic SQLite transaction with rollback | M1 | Survey (Notion runtime module 443756 & 877308) |
| 2 | Pure Leaf Block Structural Rule | Strict enforcement that leaf nodes (`content: null`) cannot receive children; child creation rejected | M1 | Survey (`notion.db` query: 100% leaf nodes have content null) |
| 3 | Container Block Structural Rule | Container blocks maintain ordered list of child UUIDs in `content` | M1 | Survey (`notion.db` & `models.py`) |
| 4 | Toggleable Headers Backend Rule | Headers (`header`, `sub_header`, `sub_sub_header`, `header_4`) dynamically allow children in `content` iff `format.toggleable = true` | M1 | Survey (`notion.db` sub_sub_header toggleable rows) |
| 5 | Block Catalog: `header_4` | Heading 4 block schema with title property and optional toggleable format | M1 | Survey (`notion_block_schemas_extracted.json`) |
| 6 | Block Catalog: `to_do` | Task block with checkbox `properties.checked` and container children capability | M1 | Survey (Notion cache bundle `d2e6fffcbe93e976_0`) |
| 7 | Block Catalog: `quote` | Quotation block container with left accent border and rich-text title | M1 | Survey (Notion cache bundle `d2e6fffcbe93e976_0`) |
| 8 | Block Catalog: `callout` | Highlighted callout box container with icon badge, background tint, and nested children | M1 | Survey (Notion cache bundle `d2e6fffcbe93e976_0`) |
| 9 | Block Catalog: `transclusion_container` | Synced block master container holding shared content | M1 | Survey (Notion cache bundle `d2e6fffcbe93e976_0`) |
| 10 | Block Catalog: `transclusion_reference` | Synced block reference pointer rendering the subtree of a `transclusion_container` | M1 | Survey (Notion cache bundle `d2e6fffcbe93e976_0`) |
| 11 | Block Catalog: Media Leaves (`video`, `audio`, `file`, `pdf`) | Leaf blocks with source property, display format, and atomic `content: null` | M1 | Survey (Notion cache bundle `d2e6fffcbe93e976_0`) |
| 12 | Block Catalog: `bookmark` | Leaf card block with link, title, description, and preview metadata | M1 | Survey (Notion cache bundle `d2e6fffcbe93e976_0`) |
| 13 | Frontend DOM Rendering: Extended Types | Element factory `renderBlock(block)` in `frontend/app.js` generating specialized DOM for all 11 new types | M2 | Survey (`frontend/app.js` survey) |
| 14 | Frontend Toggleable Headers | Rendering collapsible `<details>` with `<summary>` toggle arrow and nested child slot when `format.toggleable = true` | M2 | Survey (`frontend/app.js` survey) |
| 15 | Frontend Rich Text Editing Fidelity | Ensuring bidirectional rich-text editing (`properties.title`) works seamlessly on all new text blocks | M2 | Survey (`frontend/app.js` survey) |
| 16 | Frontend Interactive Controls | Updating slash menu taxonomy (`SLASH_TAXONOMY`) and block conversion actions for new block types | M2 | Survey (`frontend/app.js` survey) |
| 17 | Frontend Component Styling | CSS styling in `frontend/styles.css` for all newly integrated block types and toggleable headers | M2 | Survey (`frontend/styles.css` survey) |
| 18 | E2E & Regression Test Suite | Automated test suite in `tests/` verifying transactions, schemas, container/leaf rules, and 0 regressions | M3 / E2E Track | Survey (`tests/` survey & 261 test baseline) |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Backend Engine, Schemas & Transactional Protocol | Implement `apply_transaction`, `build_op_set`, `build_op_list_after`, update `add_child_block` and `create_block_api`; add 11 new block schemas to `rich_text.py`; enforce container vs leaf (`content: null`) rules; enable toggleable headers dynamic validation. | none | DONE |
| M2 | Frontend Editor & Interactive Block Integration | Add DOM components in `renderBlock`, child rendering in `renderTreeFromRecordMap`, slash menu, block conversion, and CSS styling in `styles.css`. | M1 | DONE |
| M3 | Final Acceptance & Regression Verification | Pass 100% of E2E test suite across Tiers 1-4, execute Tier 5 adversarial coverage hardening, and pass Forensic Audit with 0 regressions. | M2, E2E Track | DONE |

## Interface Contracts

### Transaction Operations Contract (`models.py` & `backend.py`)
```python
# op.set: Initializes a block row with full canonical fields
op_set = {
    'pointer': {'table': 'block', 'id': str(block_id)},
    'path': [],
    'command': 'set',
    'args': block_dict  # contains id, type, properties, format, content, parent_id, parent_table, alive, etc.
}

# op.listAfter: Inserts child UUID into parent's content array immediately after after_id (or index 0 if after_id is None)
op_list_after = {
    'pointer': {'table': 'block', 'id': str(parent_id)},
    'path': ['content'],
    'command': 'listAfter',
    'args': {'id': str(child_id), 'after': after_id_or_none}
}

# Transaction runner:
# apply_transaction(operations: list[dict]) -> dict: {'ok': True, 'results': [...]}
```

### Container vs Leaf Contract (`rich_text.py` & `models.py`)
```python
CONTAINER_BLOCK_TYPES = {
    'page', 'column_list', 'column', 'text', 'to_do',
    'bulleted_list', 'numbered_list', 'toggle', 'quote',
    'callout', 'table', 'transclusion_container'
}

LEAF_BLOCK_TYPES = {
    'equation', 'divider', 'code', 'image', 'video',
    'audio', 'file', 'pdf', 'bookmark', 'table_row',
    'transclusion_reference', 'sub_page'
}

TOGGLEABLE_HEADER_TYPES = {'header', 'sub_header', 'sub_sub_header', 'header_4'}

def is_container_block(block_type: str, format_dict: dict | None = None) -> bool:
    if block_type in CONTAINER_BLOCK_TYPES:
        return True
    if block_type in TOGGLEABLE_HEADER_TYPES and format_dict and bool(format_dict.get('toggleable')):
        return True
    return False
```

### Frontend Block Rendering Contract (`frontend/app.js`)
```javascript
// Every newly rendered block element must satisfy:
// 1. blockEl.id = block.id;
// 2. blockEl.dataset.blockId = block.id;
// 3. blockEl.dataset.type = block.type;
// 4. Any editable rich text segment must have [contenteditable="true"] and data-property="title" (or "caption").
// 5. Container blocks must contain a child slot matching:
//    '.notion-block-children, .block-toggle-content, .notion-synced-body, .block-quote-children, .block-callout-children, .block-to-do-children'
```
