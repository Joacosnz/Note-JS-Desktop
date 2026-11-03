# Scope: Milestone 1 — Backend Core: Database Schema, Bidirectional Persistence & Legacy Migration

## Architecture
- Module: `models.py`
- Database: SQLite (`notejs.db`) via Peewee ORM
- Core Entity: `Block` with full Notion DDL schema:
  `id`, `space_id`, `version`, `last_version`, `type`, `properties`, `content`, `parent_id`, `parent_table`, `alive`, `format`, `crdt_format_version`, `crdt_data`, `created_time`, `last_edited_time`, `permissions`
- Compatibility Layer: SQLite view `blocks`, attributes `note_id`, `sort_index`, `created_at`, `updated_at`, dual keys in `to_dict()`.
- Migration: `migrate_legacy_notes_to_blocks()` run in `init_db()`.
- Bidirectional consistency: atomic helper methods for add, move, reorder, soft delete.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | Notion Block Schema DDL & Peewee Model (R1) | Implement `Block` model with all 16 Notion fields and compatibility attributes. | M1 | Survey 3_1 |
| F2 | Bidirectional Pointers & Consistency (R1) | Container `content` UUID array <-> child `parent_id`/`parent_table` pointers maintained on add, move, reorder, delete. | M1 | Survey 3_1 |
| F3 | Soft Deletion & Local CRDT Versioning (R1) | Soft delete (`alive = 0`), version bump, mutation vector in `crdt_data`. | M1 | Survey 3_1 |
| F4 | Automatic Legacy Note Migration (R2) | Startup migration in `init_db()` converting existing `notes` to root `page` blocks and child `text` blocks in `content`. | M1 | Survey 3_1 |
| F5 | Zero-Regression Legacy Compatibility (R2) | Retain existing `notes` table intact, dual keys in `to_dict()`, 153 existing tests pass. | M1 | Survey 3_1 |

## Interface Contracts
### Notion Block Model (`models.py`)
- Peewee ORM `Block` (`table_name = 'block'`):
  - `id`: CharField primary_key (UUIDv4)
  - `space_id`: CharField default 'default_space'
  - `version`: IntegerField default 1
  - `last_version`: IntegerField default 1
  - `type`: CharField
  - `properties`: TextField default '{}'
  - `content`: TextField default '[]'
  - `parent_id`: CharField null=True
  - `parent_table`: CharField default 'block'
  - `alive`: IntegerField default 1
  - `format`: TextField default '{}'
  - `crdt_format_version`: IntegerField default 1
  - `crdt_data`: TextField default '{}'
  - `created_time`: BigIntegerField
  - `last_edited_time`: BigIntegerField
  - `permissions`: TextField default '[]'
  - Backwards-compatibility fields: `note_id` (IntegerField null=True), `sort_index` (CharField default 'a0'), `created_at` (DateTimeField), `updated_at` (DateTimeField).
- View: `CREATE VIEW IF NOT EXISTS blocks AS SELECT * FROM block;`
- Methods:
  - `add_child_block(parent_id, child_data, index=None)`
  - `move_child_block(child_id, new_parent_id, index=None)`
  - `reorder_children(parent_id, new_content_order)`
  - `soft_delete_block(block_id)`
  - `restore_block(block_id)`
  - `resolve_subtree_record_map(root_id)`
- Migration:
  - `migrate_legacy_notes_to_blocks()`:
    Reads `Note.select()`. For each note, creates root `page` block (if not exists), sets `properties.title = [[note.title]]`, splits content into `text` blocks, populates `page.content`.
- Tests:
  - `tests/test_block_schema_and_migration.py`
  - Full suite `py -m unittest discover -s tests` must pass (153 existing + new tests).
