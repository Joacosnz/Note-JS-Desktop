## 2026-11-02T02:11:51Z
You are a Worker subagent for Milestone 2 (Backend API & Native Bridge, Rich Text Engine & Full Block Suite).
Working directory: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_worker_m2
Original request path: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\ORIGINAL_REQUEST.md
Scope document: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\PROJECT.md
Explorer findings report: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_2\report.md

You MUST read ORIGINAL_REQUEST.md first, as well as PROJECT.md and the explorer report.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

File ownership:
You exclusively own:
- `backend.py`
- `desktop_app.py`
- `rich_text.py` (or helper modules for rich text and block types)
- `tests/test_block_api_and_richtext.py`
Do NOT edit other files in this milestone.

Your Mission:
1. Implement pure-Python Rich Text & Block Type Engine in `rich_text.py` (or imported helper):
   - Pure standard library (`html.parser.HTMLParser`, `html.escape`):
     * `rich_text_to_plain_text(tuples)`: extracts clean text from Notion tuple structure `[["Text", [["b"], ...]], ...]`.
     * `plain_text_to_rich_text(text)`: wraps plain text into Notion rich text tuples `[[text, []]]`.
     * `rich_text_to_html(tuples)`: converts decorator tuples into styled HTML (`<strong>`, `<em>`, `<u>`, `<s>`, `<code>`, `<mark style="...">`, `<a href="...">`, `<span class="inline-equation" data-latex="...">`).
     * `html_to_rich_text(html_str)`: parses HTML back into Notion rich text tuples with style stacks.
     * Support decorators: bold (`["b"]`), italic (`["i"]`), underline (`["_"]`), strikethrough (`["s"]`), inline code (`["c"]`), highlight/color (`["h", color]`), link (`["a", url]`), inline equation (`["e", latex]`).
   - Define canonical schemas and validation for all 17 Notion block types:
     * Structural: `page`, `column_list`, `column`, `divider`.
     * Text & Headers: `text`, `header`, `sub_header`, `sub_sub_header`, `bulleted_list`, `numbered_list`, `toggle`.
     * Data & Code: `code` (with `language`), `equation` (LaTeX), `table` (with `table_row`, `table_block_column_order`, format headers), `collection_view` / `collection_view_page`.
     * Media: `image` (width, source).
     * Navigation: `sub_page`.
2. Implement REST Endpoints in `backend.py`:
   - Disambiguate reserved paths so `/api/blocks/order`, `/api/blocks/batch`, `/api/blocks/rich-text/convert` are NOT treated as `<id>` endpoints.
   - `POST /api/blocks`: create block (UUIDv4, validates parent, adds to parent's `content` array with support for `target_index`, `after_id`, `before_id`, or append).
   - `GET /api/blocks/<id>`: get block by ID. If query param `?resolve=true` or `resolve_tree=true`, returns subtree recordMap.
   - `GET /api/blocks/<id>/recordMap` and `GET /api/notes/<id>/recordMap`: BFS resolution returning normalized `{ "block": { "<id>": { "value": <data>, "role": "editor" } } }`.
   - `PUT /api/blocks/<id>`: update properties, format, type, crdt_data, incrementing version and checking `expected_version` concurrency.
   - `POST /api/blocks/<id>/reorder`: intra-parent child reordering or moving between parents.
   - `DELETE /api/blocks/<id>`: soft-delete (`alive = 0`, removed from parent `content`).
   - `POST /api/blocks/<id>/restore`: restore (`alive = 1`, re-inserted into parent `content`).
   - `POST /api/blocks/rich-text/convert`: converts between HTML and rich text tuples.
3. Implement Native PyWebView Bridge in `desktop_app.py`:
   - Expose in `PyWebViewBridge`:
     * `create_block(block_dict, target_index=None, after_id=None, before_id=None)`
     * `get_block(block_id, resolve_tree=False)`
     * `get_record_map(root_id)`
     * `update_block(block_id, updates, expected_version=None)`
     * `reorder_block_children(parent_id, content_array)`
     * `soft_delete_block(block_id)`
     * `restore_block(block_id)`
     * `convert_rich_text(payload)`
4. Create automated test suite `tests/test_block_api_and_richtext.py`:
   - Test rich text tuple conversions (decorators, nesting, HTML round-trip, plain text).
   - Test block validation across all 17 block types.
   - Test all HTTP REST endpoints using urllib/http client in test runner.
   - Test PyWebViewBridge native methods.
   - Test reserved subpath disambiguation (`/api/blocks/order`, `/api/blocks/batch`).
   - Run verification:
     * `py -m unittest tests.test_block_api_and_richtext -v`
     * `py -m unittest discover -s tests -p "test_*.py"`
     * Ensure all 165 existing tests + new tests pass with 0 errors.
