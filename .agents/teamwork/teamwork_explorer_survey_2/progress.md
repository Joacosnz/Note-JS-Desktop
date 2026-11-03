# Progress — Survey Explorer 2 (R2 & R3)

Last visited: 2026-10-30T20:23:00Z

## Status
- Completed in-depth investigation of Requirements R2 & R3.
- Investigated `models.py` (Peewee ORM models Note, Block, upsert_note_orm, sync_blocks_from_note_html_orm, to_dict).
- Investigated `backend.py` REST API routes (`/api/notes`, `/api/notes/<id>/blocks`, `/api/notes/<id>/blocks/sync`, `/api/blocks/order`, `/api/blocks/batch`).
- Investigated `desktop_app.py` PyWebView bridge methods.
- Investigated `frontend/app.js` (rich-editor-canvas, selectNote, loadActiveNote, collectAndSyncNoteBlocks, insertSubpageBlock, generateEmbeddedNoteCardHtml).
- Verified that `loadNote` and `renderBlock` with `case 'sub_page':` are currently missing and must be introduced.
- Identified styling requirements for `.block-subpage` in `frontend/styles.css`.
- Compiling findings into handoff report in `handoff.md`.
