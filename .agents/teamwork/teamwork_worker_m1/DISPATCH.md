## 2026-11-02T01:54:51Z
You are a Worker subagent for Milestone 1 (Backend Core: Database Schema, Bidirectional Persistence & Legacy Migration).
Working directory: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_worker_m1
Original request path: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\ORIGINAL_REQUEST.md
Scope document: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\PROJECT.md
Explorer findings report: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_1\report.md

You MUST read ORIGINAL_REQUEST.md first, as well as PROJECT.md and the explorer report.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File ownership:
You exclusively own:
- `models.py`
- `tests/test_block_schema_and_migration.py`
Do NOT edit other files in this milestone.

Your Mission:
1. Implement in `models.py`:
   - Update `Block` model class with `table_name = 'block'`:
     * Fields: `id` (CharField primary_key UUID string), `space_id` (CharField default 'default_space'), `version` (IntegerField default 1), `last_version` (IntegerField default 1), `type` (CharField), `properties` (TextField default '{}'), `content` (TextField default '[]'), `parent_id` (CharField null=True), `parent_table` (CharField default 'block'), `alive` (IntegerField default 1), `format` (TextField default '{}'), `crdt_format_version` (IntegerField default 1), `crdt_data` (TextField default '{}'), `created_time` (BigIntegerField epoch ms), `last_edited_time` (BigIntegerField epoch ms), `permissions` (TextField default '[]').
     * Retain compatibility columns with defaults: `note_id` (IntegerField null=True), `sort_index` (CharField default 'a0'), `created_at` (DateTimeField default datetime.now), `updated_at` (DateTimeField default datetime.now).
     * Update `Block.to_dict()`: return both full Notion keys (`id`, `space_id`, `version`, `last_version`, `type`, `properties`, `content`, `parent_id`, `parent_table`, `alive`, `format`, `crdt_format_version`, `crdt_data`, `created_time`, `last_edited_time`, `permissions`) AND legacy keys (`noteId`, `parentId`, `sortIndex`, `createdAt`, `updatedAt`, `page_id`, `title`) so existing frontend code and test suites work seamlessly.
   - In `init_db()`:
     * Create table `block`.
     * Check if table `blocks` exists as a regular table; if so, rename to `block` or migrate safely.
     * Create compatibility view: `CREATE VIEW IF NOT EXISTS blocks AS SELECT * FROM block;`.
     * Trigger `migrate_legacy_notes_to_blocks()` during initialization.
   - Implement bidirectional consistency and hierarchy helper functions in `models.py`:
     * `add_child_block(parent_id, child_data, index=None)`: creates child block, sets `parent_id` and `parent_table='block'`, inserts child ID into parent's ordered `content` JSON array, increments `parent.version`, records local CRDT mutation in `crdt_data`.
     * `move_child_block(child_id, new_parent_id, index=None)`: atomic move removing from old parent's `content`, inserting into new parent's `content`, updating child's `parent_id`.
     * `reorder_children(parent_id, new_content_order)`: validates child IDs and updates parent's `content` array in place.
     * `soft_delete_block(block_id)`: sets `alive = 0`, removes `block_id` from parent's `content` array, updates parent's version and child's `last_edited_time`. Row remains in database.
     * `restore_block(block_id)`: sets `alive = 1`, re-adds `block_id` into parent's `content` array.
     * `resolve_subtree_record_map(root_id)`: BFS traversal returning `{ "block": { "<id>": { "value": <data>, "role": "editor" } } }` with cycle detection.
   - Implement `migrate_legacy_notes_to_blocks()` in `models.py`:
     * Inspect all rows in `notes` table.
     * For each note, check if root `page` block already exists (id = str(note.id)).
     * If not, create root `page` block with `id = str(note.id)`, `properties = {"title": [[note.title or "", []]]}`, `format` storing icon/cover if present, parse note content/HTML into child `text` blocks, link child IDs in `page.content`, set `alive = 1`.
     * Idempotent (does not duplicate).
     * `notes` table remains 100% intact.
2. Create automated test suite in `tests/test_block_schema_and_migration.py`:
   - Test full 16-field DDL schema on `Block`.
   - Test bidirectional consistency (add, reorder, move between parents).
   - Test soft deletion (`alive = 0`) keeping rows in SQLite and removing from parent's `content`.
   - Test restoration (`alive = 1`).
   - Test CRDT fields mutation tracking and version increments.
   - Test automatic legacy note migration preserving note title and text content.
   - Test legacy `Block` compatibility (legacy fields, `to_dict()`, `blocks` view).
3. Verification:
   - Run: `py -m unittest tests.test_block_schema_and_migration -v`
   - Run full test suite: `py -m unittest discover -s tests -p "test_*.py"`
   - Ensure all 153 existing tests continue to pass (now 153 + new tests).

Write your completion report and handoff to:
`c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_worker_m1\handoff.md`
Send a message when complete with test results and report path. Remember to update your `progress.md` after each meaningful step.
