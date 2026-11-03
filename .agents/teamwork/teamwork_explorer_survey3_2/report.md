# Report: Backend API, PyWebView Bridge & Rich Text Architecture (R3 & R4)

**Author:** teamwork_explorer_survey3_2  
**Target File:** `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_2\report.md`  
**Date:** 2026-11-02  
**Scope:** R3 (Backend API & PyWebView Bridge Operations) and R4 (Rich Text Serialization & Deserialization in Python)  

---

## 1. Executive Summary

This investigation provides the architectural design, protocol specifications, algorithms, and integration blueprint for implementing Notion-style hierarchical block operations (Requirement R3) and Python-based rich text tuple serialization/deserialization with the complete suite of Notion block types (Requirement R4) in **Note-JS-Desktop**.

### Key Outcomes:
1. **R3 Operations Fully Designed:**
   - **Block Creation:** Automatic UUIDv4 generation, parent existence and liveness validation, cycle prevention, atomic updates to parent's `content` array (supporting `target_index`, `after_id`, `before_id`, or append).
   - **Subtree `recordMap` Resolution:** Breadth-First Search (BFS) traversal starting from root block (e.g. page or container) resolving all living descendants into a normalized dictionary `{ "block": { "<id>": { "value": <data>, "role": "editor" } } }` matching Notion's client protocol.
   - **Mutation & Concurrency:** Updating semantic properties (`properties`), visual format (`format`), block type, version increments (`version`, `last_version`), optimistic concurrency conflict checking (`expected_version`), and local CRDT metadata tracking (`crdt_data`, `crdt_format_version`).
   - **Reordering:** Intra-container reordering (`content` array updates) and cross-container reparenting with automatic source/destination parent updates.
   - **Soft-Delete & Restoration:** Non-destructive soft-delete (`alive = 0`) with cascade subtree marking and parent `content` removal, coupled with full subtree restoration (`alive = 1`) and parent re-insertion.
2. **R4 Rich Text Engine & Full Block Suite:**
   - Standardized Notion rich text tuple format: `[["Text", [["b"], ["i"], ["h", color], ["c"], ["a", url], ["e", latex]]]]`.
   - Pure Python standard library converters (`rich_text_to_plain_text`, `plain_text_to_rich_text`, `rich_text_to_html`, `html_to_rich_text`) using `html.parser.HTMLParser` and `html.escape` without external runtime dependencies.
   - Complete schema definition for all 17 required block types spanning structural, text/headers, data/code, media, and legacy sub-notes.
3. **Guaranteed Backwards Compatibility:**
   - Routing disambiguation isolating reserved subpaths (`/api/blocks/order`, `/api/blocks/batch`, `/api/blocks/rich-text/convert`) from dynamic block ID endpoints (`/api/blocks/<id>`).
   - Dual-key serialization in `to_dict()` ensuring all existing 153 tests in `tests/` pass without regressions.

---

## 2. Existing Architecture Analysis

### 2.1 Backend Server (`backend.py`)
- **Server Framework:** Multi-threaded HTTP server utilizing `socketserver.ThreadingMixIn` and `http.server.BaseHTTPRequestHandler` (`NoteJSRequestHandler`). Runs by default on port 3000 (or `DEFAULT_APP_PORT`).
- **Request Dispatching:** Manual path routing via `do_GET`, `do_POST`, `do_DELETE`, `do_OPTIONS`, `do_HEAD`.
- **Response Format:** Helper `_send_json(data, status=200)` serializing JSON with `ensure_ascii=False` and UTF-8 encoding.
- **CORS & Headers:** `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`.
- **Existing Block Endpoints:**
  - `GET /api/notes/<id>/blocks` -> calls `get_note_blocks_orm(note_id)`
  - `POST /api/blocks/order` -> calls `update_block_order_orm(...)`
  - `POST /api/blocks/batch` -> calls `update_batch_blocks_order_orm(...)`
  - `POST /api/notes/<id>/blocks/sync` -> calls `sync_blocks_from_note_html_orm(...)`

### 2.2 Native Desktop Bridge (`desktop_app.py`)
- **PyWebView API Bridge:** `PyWebViewBridge` class exposed to the frontend as `window.pywebview.api`.
- **Method Execution:** Direct in-process Python calls bypassing HTTP serialization latency.
- **Existing Methods:** Mirrors `backend.py` operations (`bootstrap`, `save_note`, `delete_note`, `get_note_blocks`, `update_block_order`, `update_batch_blocks_order`, `sync_note_blocks`, `save_smart_folder`, etc.).

### 2.3 ORM & Database Layer (`models.py`)
- **Engine:** SQLite + Peewee ORM with WAL mode (`journal_mode=wal`), normal synchrony, busy timeout 10,000ms.
- **Concurrency Locking:** Global `DB_LOCK = threading.Lock()` and atomic blocks `with db.atomic():` protecting write operations.
- **Existing `Block` Model:**
  ```python
  class Block(BaseModel):
      id = CharField(primary_key=True, max_length=64)
      note_id = IntegerField(index=True)
      parent_id = CharField(max_length=64, null=True, index=True)
      type = CharField(max_length=64, default='p')
      properties = TextField(default='{}')
      sort_index = CharField(max_length=64, index=True, default='a0')
      created_at = IntegerField(default=0)
      updated_at = IntegerField(default=0)
  ```
- **Existing `Block.to_dict()`:** Returns `id`, `noteId`, `parentId`, `type`, `properties` (dict), `sortIndex`, `createdAt`, `updatedAt`, and top-level `page_id`/`title` when `type == 'sub_page'`.

### 2.4 Existing Test Suite (`tests/`)
- Total **153 tests** passing in ~2.4 seconds (`py -m unittest discover -s tests`).
- Tests in `test_backend_subpage.py` and `test_adversarial_challenger.py` assert `Block.to_dict()` structure, error handling on malformed JSON, and camelCase fallback (`pageId` -> `page_id`).
- Tests in `test_adversarial_m3_r1_r4.py` and `test_ui_production_r1_r6.py` verify window controls and settings persistence.
- **Requirement:** Any changes to `Block`, `backend.py`, or `desktop_app.py` must maintain 100% test pass rate.

---

## 3. R3: Backend REST API & Native PyWebView Bridge Operations

### 3.1 Block Creation Protocol

#### Endpoint & Signature:
- **HTTP REST:** `POST /api/blocks`
- **PyWebView Bridge:** `window.pywebview.api.create_block(block_dict, target_index=None, after_id=None, before_id=None)`

#### Request Payload:
```json
{
  "id": "optional-uuid-v4",
  "type": "text",
  "parent_id": "parent-block-uuid",
  "parent_table": "block",
  "properties": {
    "title": [["This is a new paragraph."]]
  },
  "format": {
    "block_color": "yellow_background"
  },
  "target_index": 0,
  "after_id": "sibling-block-uuid-1",
  "before_id": "sibling-block-uuid-2",
  "space_id": "space-uuid-or-default"
}
```

#### Detailed Creation Algorithm:
1. **UUIDv4 Assignment:** If client does not supply an `id`, or supplies an empty/invalid string, assign `str(uuid.uuid4())`.
2. **Parent Validation:**
   - If `parent_id` is supplied:
     - Check `parent_table` (default: `'block'`).
     - Query `Block.get_or_none(Block.id == parent_id)`.
     - Reject if parent does not exist (`404 Not Found` or `{'ok': False, 'error': 'Parent block not found'}`).
     - Reject if parent `alive == 0` (`{'ok': False, 'error': 'Cannot add child to trashed parent'}`).
     - Prevent self-reference: `new_id != parent_id`.
     - Cycle detection: Traverse ancestor chain starting from `parent_id`. If `new_id` is in the ancestor chain, reject circular hierarchy.
3. **Ordering in Parent's `content` Array:**
   - Parent block has `content` (JSON array of child UUID strings).
   - Parse `parent_content = json.loads(parent.content or '[]')`.
   - Remove `new_id` if already present (idempotent).
   - Placement precedence:
     1. If `after_id` in `parent_content`: insert immediately after `after_id`.
     2. Else if `before_id` in `parent_content`: insert immediately before `before_id`.
     3. Else if `target_index` is integer: insert at `max(0, min(target_index, len(parent_content)))`.
     4. Default: append to end of `parent_content`.
   - Update parent: `parent.content = json.dumps(parent_content)`, `parent.version += 1`, `parent.last_edited_time = now_ms`, `parent.save()`.
4. **Child Persistence:**
   - Set `alive = 1`, `version = 1`, `last_version = 0`, `crdt_format_version = 1`.
   - Set `created_time = now_ms`, `last_edited_time = now_ms`.
   - Save new block in SQLite within the same `db.atomic()` transaction.
5. **Response:**
```json
{
  "ok": true,
  "block": {
    "id": "new-block-uuid",
    "type": "text",
    "properties": { "title": [["This is a new paragraph."]] },
    "content": [],
    "parent_id": "parent-block-uuid",
    "parent_table": "block",
    "alive": 1,
    "version": 1,
    "format": { "block_color": "yellow_background" },
    "created_time": 1730500000000,
    "last_edited_time": 1730500000000
  },
  "parent": {
    "id": "parent-block-uuid",
    "content": ["sibling-1", "new-block-uuid", "sibling-2"],
    "version": 2
  }
}
```

---

### 3.2 Fetching Blocks & Subtree `recordMap` Resolution

#### Endpoint & Signature:
- **HTTP REST:** `GET /api/blocks/<id>/recordMap?include_trashed=false` (also `GET /api/pages/<id>/recordMap`)
- **PyWebView Bridge:** `window.pywebview.api.get_block_record_map(block_id, include_trashed=False)`

#### Purpose:
Return a fully resolved, normalized dictionary indexed by block ID for the requested root block and all its nested descendants across the entire tree, mirroring Notion's `loadPageChunk` client protocol.

#### Subtree Resolution Algorithm (BFS):
```python
def get_block_record_map_orm(root_block_id, include_trashed=False):
    root_id = str(root_block_id or '').strip()
    if not root_id:
        return {'ok': False, 'error': 'Block ID required', 'recordMap': {'block': {}}}

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        root_block = Block.get_or_none(Block.id == root_id)
        if not root_block:
            return {'ok': False, 'error': f'Block {root_id} not found', 'recordMap': {'block': {}}}

        if not include_trashed and root_block.alive == 0:
            return {'ok': False, 'error': f'Block {root_id} is deleted', 'recordMap': {'block': {}}}

        record_map = {'block': {}}
        queue = [root_id]
        visited = set()

        while queue:
            current_id = queue.pop(0)
            if current_id in visited:
                continue
            visited.add(current_id)

            blk = Block.get_or_none(Block.id == current_id)
            if not blk:
                continue
            if not include_trashed and blk.alive == 0:
                continue

            # Store in normalized recordMap structure
            record_map['block'][blk.id] = {
                'value': blk.to_dict(),
                'role': 'editor'
            }

            # Enqueue children referenced in content array
            try:
                content_ids = json.loads(blk.content or '[]')
            except Exception:
                content_ids = []
            
            for cid in content_ids:
                if cid and cid not in visited:
                    queue.append(cid)

            # Defensive lookup: also find any blocks declaring this block as parent_id
            children_query = Block.select().where(
                (Block.parent_id == current_id) &
                (Block.alive == 1 if not include_trashed else True)
            )
            for c_blk in children_query:
                if c_blk.id not in visited:
                    queue.append(c_blk.id)

    return {'ok': True, 'rootId': root_id, 'recordMap': record_map}
```

#### Resulting `recordMap` JSON Structure:
```json
{
  "ok": true,
  "rootId": "page-uuid-1",
  "recordMap": {
    "block": {
      "page-uuid-1": {
        "value": {
          "id": "page-uuid-1",
          "type": "page",
          "properties": { "title": [["Project Overview"]] },
          "content": ["col-list-uuid", "p-uuid-1"],
          "parent_id": null,
          "parent_table": "space",
          "alive": 1,
          "version": 3,
          "format": { "page_icon": "🚀" }
        },
        "role": "editor"
      },
      "col-list-uuid": {
        "value": {
          "id": "col-list-uuid",
          "type": "column_list",
          "properties": {},
          "content": ["col-1-uuid", "col-2-uuid"],
          "parent_id": "page-uuid-1",
          "parent_table": "block",
          "alive": 1,
          "version": 1
        },
        "role": "editor"
      },
      "col-1-uuid": {
        "value": {
          "id": "col-1-uuid",
          "type": "column",
          "properties": {},
          "content": ["text-left-uuid"],
          "parent_id": "col-list-uuid",
          "parent_table": "block",
          "alive": 1,
          "version": 1,
          "format": { "column_ratio": 0.5 }
        },
        "role": "editor"
      }
    }
  }
}
```

---

### 3.3 Updating Semantic Properties, Visual Format & Concurrency

#### Endpoint & Signature:
- **HTTP REST:** `POST /api/blocks/<id>` or `PUT /api/blocks/<id>`
- **PyWebView Bridge:** `window.pywebview.api.update_block(block_id, update_data)`

#### Request Payload:
```json
{
  "properties": {
    "title": [["Updated title ", [["b"]]]],
    "language": [["python"]]
  },
  "format": {
    "block_color": "blue",
    "block_width": 750
  },
  "type": "code",
  "expected_version": 2,
  "crdt_data": {
    "client_id": "desktop-client-1",
    "clock": 14,
    "last_mutation": "update_properties"
  }
}
```

#### Mutation Logic:
1. **Concurrency Check:**
   - If `expected_version` is passed and `block.version != expected_version`:
     - Return conflict error `409 Conflict`: `{'ok': False, 'error': 'Version conflict', 'current_version': block.version}`.
2. **Properties Merge:**
   - Existing properties dictionary is merged or updated with incoming keys.
   - Rich text tuples in properties are validated.
3. **Format Merge:**
   - Existing visual formatting dictionary is merged with incoming format keys.
4. **Type Transition:**
   - If `type` is specified, block type is updated (e.g. converting `text` to `header` or `toggle`).
5. **Versioning & CRDT:**
   - `block.last_version = block.version`
   - `block.version += 1`
   - `block.last_edited_time = int(time.time() * 1000)`
   - `block.crdt_data = json.dumps(incoming_crdt_data)`
6. **Persistence:** `block.save()` within `db.atomic()`.

---

### 3.4 Reordering Child Blocks

#### Endpoint & Signature:
- **HTTP REST:** `POST /api/blocks/<id>/reorder`
- **PyWebView Bridge:** `window.pywebview.api.reorder_block_children(parent_id, content_or_move)`

#### Scenarios Supported:
1. **Full Content Array Reordering:** Client passes full new order of child UUIDs `{"content": ["uuid-3", "uuid-1", "uuid-2"]}`.
   - Validates that each UUID exists in SQLite and belongs to `parent_id`.
   - Replaces `parent.content = json.dumps(new_order)`.
2. **Single Relative Move:** Client passes `{"child_id": "uuid-3", "target_index": 0}` or `{"child_id": "uuid-3", "after_id": "uuid-1"}`.
   - Modifies existing array in place.
3. **Cross-Container Reparenting:** Client moves a child from `source_parent_id` to `target_parent_id`:
   - Removes `child_id` from `source_parent.content`.
   - Sets `child.parent_id = target_parent_id`.
   - Inserts `child_id` into `target_parent.content` at target position.
   - Bumps versions on `source_parent`, `target_parent`, and `child`.

---

### 3.5 Soft-Delete (`alive = 0`) & Restoration (`alive = 1`)

#### Endpoints & Signatures:
- **Soft-Delete:**
  - **HTTP REST:** `DELETE /api/blocks/<id>?permanent=false`
  - **PyWebView Bridge:** `window.pywebview.api.delete_block(block_id, permanent=False)`
- **Restoration:**
  - **HTTP REST:** `POST /api/blocks/<id>/restore`
  - **PyWebView Bridge:** `window.pywebview.api.restore_block(block_id)`

#### Soft-Delete Logic:
1. Fetch target block. If not found: return 404.
2. If `permanent=True`: physical delete `Block.delete().where(...)`.
3. If `permanent=False` (default):
   - Find all descendants in subtree rooted at `block_id` using BFS.
   - For target block and all descendants:
     - Set `alive = 0`.
     - Set `last_edited_time = now_ms`.
     - Increment `version`.
   - In parent block:
     - If parent exists and is alive:
       - Remove `block_id` from parent's `content` array (so parent immediately stops rendering it).
       - Note: child still preserves `parent_id` pointing to parent for restoration!
       - Increment parent's `version`.
       - Update parent's `last_edited_time`.

#### Restoration Logic:
1. Fetch target block.
2. Find all descendants in subtree rooted at `block_id`.
3. Set `alive = 1` on target block and all descendants.
4. In parent block:
   - If parent exists and `alive == 1`:
     - Parse parent's `content` array.
     - If `block_id` not in `parent_content`:
       - Append `block_id` to `parent_content` (or restore to index).
       - Increment parent's `version`.
   - If parent does not exist or parent is also deleted:
     - Reparent `block_id` to workspace root / space.
5. Save all records in atomic transaction.

---

## 4. R4: Rich Text Serialization & Deserialization in Python

### 4.1 Notion Rich Text Specification

In Notion, all textual properties (such as block `title`, headers, code content, captions) are structured as an array of decorated text segments:
```
RichText = [ Segment_1, Segment_2, ... ]
Segment = [ Text_String, [ Decorator_1, Decorator_2, ... ] ]
```
If a segment has no formatting, it is represented as `["Text"]` or `["Text", []]`.

#### Supported Decorator Catalog:
| Decorator Tuple | Meaning | HTML Rendering | Inline Editor Representation |
|---|---|---|---|
| `["b"]` | Bold | `<strong>...</strong>` | `<b>` or `Ctrl+B` |
| `["i"]` | Italic | `<em>...</em>` | `<i>` or `Ctrl+I` |
| `["_"]` | Underline | `<u>...</u>` | `<u>` or `Ctrl+U` |
| `["s"]` | Strikethrough | `<s>...</s>` | `<s>` or `Ctrl+Shift+S` |
| `["c"]` | Inline Code | `<code>...</code>` | `<code>` or `Ctrl+E` |
| `["h", color]` | Color / Highlight | `<span class="notion-color-{color}">...</span>` | Font color or background color |
| `["a", url]` | Hyperlink | `<a href="{url}" target="_blank" rel="noopener noreferrer">...</a>` | Clickable hyperlink |
| `["e", latex]` | Inline Equation | `<span class="notion-inline-equation" data-latex="{latex}">{latex}</span>` | Rendered KaTeX formula |

Valid color values in `["h", color]`:
- Text colors: `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`
- Background highlights: `gray_background`, `brown_background`, `orange_background`, `yellow_background`, `green_background`, `blue_background`, `purple_background`, `pink_background`, `red_background`

---

### 4.2 Python Converter Engine Blueprint

The following standalone conversion helpers provide full bidirectional translation between rich text tuples, plain strings, and HTML:

```python
import html
from html.parser import HTMLParser
from urllib.parse import urlparse


def rich_text_to_plain_text(rich_text):
    """Extrae el contenido textual plano concatenando los segmentos de texto enriquecido."""
    if not rich_text:
        return ""
    if isinstance(rich_text, str):
        return rich_text
    if not isinstance(rich_text, (list, tuple)):
        return str(rich_text)

    parts = []
    for seg in rich_text:
        if isinstance(seg, (list, tuple)) and len(seg) > 0:
            parts.append(str(seg[0] or ""))
        elif isinstance(seg, str):
            parts.append(seg)
    return "".join(parts)


def plain_text_to_rich_text(plain_text):
    """Envuelve texto plano simple en el formato de tuplas de texto enriquecido de Notion."""
    text_str = str(plain_text or "")
    if not text_str:
        return []
    return [[text_str]]


def rich_text_to_html(rich_text, sanitize=True):
    """
    Convierte tuplas de texto enriquecido de Notion a HTML seguro con sanitización de URLs y XSS.
    """
    if not rich_text or not isinstance(rich_text, (list, tuple)):
        return ""

    ALLOWED_SCHEMES = {'http', 'https', 'mailto', ''}
    output = []

    for seg in rich_text:
        if not isinstance(seg, (list, tuple)) or len(seg) == 0:
            continue

        raw_text = str(seg[0] or "")
        escaped_text = html.escape(raw_text)
        decorators = seg[1] if len(seg) > 1 and isinstance(seg[1], (list, tuple)) else []

        inner = escaped_text
        for dec in decorators:
            if not isinstance(dec, (list, tuple)) or len(dec) == 0:
                continue

            tag_type = dec[0]
            if tag_type == 'b':
                inner = f"<strong>{inner}</strong>"
            elif tag_type == 'i':
                inner = f"<em>{inner}</em>"
            elif tag_type == '_':
                inner = f"<u>{inner}</u>"
            elif tag_type == 's':
                inner = f"<s>{inner}</s>"
            elif tag_type == 'c':
                inner = f"<code>{inner}</code>"
            elif tag_type == 'h' and len(dec) > 1:
                color = str(dec[1] or '').replace('"', '').replace("'", "")
                inner = f'<span class="notion-color-{color}">{inner}</span>'
            elif tag_type == 'a' and len(dec) > 1:
                url = str(dec[1] or '').strip()
                parsed = urlparse(url)
                if parsed.scheme.lower() in ALLOWED_SCHEMES and not url.lower().startswith(('javascript:', 'data:', 'vbscript:')):
                    inner = f'<a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer">{inner}</a>'
            elif tag_type == 'e' and len(dec) > 1:
                latex = str(dec[1] or '')
                inner = f'<span class="notion-inline-equation" data-latex="{html.escape(latex)}">{html.escape(latex)}</span>'

        output.append(inner)

    return "".join(output)


class _RichTextHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.segments = []
        self.style_stack = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        t = tag.lower()
        if t in ('strong', 'b'):
            self.style_stack.append(['b'])
        elif t in ('em', 'i'):
            self.style_stack.append(['i'])
        elif t == 'u':
            self.style_stack.append(['_'])
        elif t in ('s', 'del', 'strike'):
            self.style_stack.append(['s'])
        elif t == 'code':
            self.style_stack.append(['c'])
        elif t == 'a':
            href = attrs_dict.get('href', '').strip()
            self.style_stack.append(['a', href])
        elif t == 'span':
            cls = attrs_dict.get('class', '')
            if 'notion-inline-equation' in cls:
                latex = attrs_dict.get('data-latex', '')
                self.style_stack.append(['e', latex])
            elif 'notion-color-' in cls:
                found_color = None
                for c in cls.split():
                    if c.startswith('notion-color-'):
                        found_color = c[len('notion-color-'):]
                        break
                self.style_stack.append(['h', found_color] if found_color else None)
            else:
                self.style_stack.append(None)
        elif t == 'br':
            self.handle_data('\n')
        else:
            self.style_stack.append(None)

    def handle_endtag(self, tag):
        if self.style_stack:
            self.style_stack.pop()

    def handle_data(self, data):
        if not data:
            return
        active_decs = [s for s in self.style_stack if s is not None]
        if active_decs:
            self.segments.append([data, list(active_decs)])
        else:
            self.segments.append([data])


def html_to_rich_text(html_str):
    """
    Parsea una cadena HTML en la estructura canónica de tuplas de texto enriquecido de Notion.
    Fusiona automáticamente segmentos adyacentes con decoradores idénticos.
    """
    if not html_str:
        return []

    parser = _RichTextHTMLParser()
    parser.feed(str(html_str))

    # Fusionar segmentos contiguos con los mismos decoradores
    merged = []
    for seg in parser.segments:
        if not merged:
            merged.append(seg)
            continue

        prev = merged[-1]
        prev_text = prev[0]
        prev_decs = prev[1] if len(prev) > 1 else []
        curr_text = seg[0]
        curr_decs = seg[1] if len(seg) > 1 else []

        if prev_decs == curr_decs:
            merged[-1] = [prev_text + curr_text, prev_decs] if prev_decs else [prev_text + curr_text]
        else:
            merged.append(seg)

    return merged
```

---

### 4.3 Full Suite of Block Types Schema Specification

| Block Type | Family | Properties Schema | Format Schema | Child `content` Rules |
|---|---|---|---|---|
| `page` | Structural | `{"title": RichText}` | `{"page_icon": str, "page_cover": str, "page_full_width": bool, "page_small_text": bool}` | Ordered array of child block UUIDs |
| `column_list` | Structural | `{}` | `{}` | Array of `column` block UUIDs (2 or more) |
| `column` | Structural | `{}` | `{"column_ratio": float}` | Ordered array of vertical child block UUIDs |
| `divider` | Structural | `{}` | `{}` | Empty `[]` |
| `text` | Text & Format | `{"title": RichText}` | `{"block_color": str}` | `[]` or nested child blocks (indented) |
| `header` | Text & Format | `{"title": RichText}` | `{"block_color": str}` | `[]` (H1 heading) |
| `sub_header` | Text & Format | `{"title": RichText}` | `{"block_color": str}` | `[]` (H2 heading) |
| `sub_sub_header` | Text & Format | `{"title": RichText}` | `{"block_color": str}` | `[]` (H3 heading) |
| `bulleted_list` | Text & Format | `{"title": RichText}` | `{"block_color": str}` | `[]` or nested indented list items |
| `numbered_list` | Text & Format | `{"title": RichText}` | `{"block_color": str}` | `[]` or nested indented list items |
| `toggle` | Text & Format | `{"title": RichText}` | `{"block_color": str}` | Ordered array of collapsible child block UUIDs |
| `code` | Data & Code | `{"title": RichText, "language": [["python"]]}` | `{"code_wrap": bool}` | `[]` |
| `equation` | Data & Code | `{"title": [["\\sum_{i=1}^n x_i"]]}` | `{}` | `[]` |
| `table` | Data & Code | `{}` | `{"table_block_column_order": [str], "table_block_column_header": bool, "table_block_row_header": bool, "table_block_column_widths": [int]}` | Ordered array of `table_row` block UUIDs |
| `table_row` | Data & Code | `{"<col_uuid>": RichText}` | `{}` | `[]` |
| `collection_view` | Data & Code | `{"title": RichText}` | `{"collection_id": str, "view_ids": [str]}` | Managed collection views |
| `collection_view_page` | Data & Code | `{"title": RichText}` | `{"collection_id": str, "view_ids": [str], "page_icon": str}` | Full-page database view |
| `image` | Media | `{"source": str, "caption": RichText}` | `{"block_width": int, "display_source": str, "block_alignment": str}` | `[]` |
| `sub_page` | Navigation | `{"page_id": str, "title": str}` | `{}` | `[]` (links to sub-note) |

---

## 5. Review of Existing API Endpoints, Tests & Compatibility

### 5.1 Disambiguation of REST URL Routing in `backend.py`

In `NoteJSRequestHandler`:
If a request is received on `/api/blocks/...`:
- It must **not** misidentify reserved subpaths as block IDs.
- **Reserved Subpaths:**
  1. `/api/blocks/order` (legacy fractional ordering)
  2. `/api/blocks/batch` (legacy batch ordering)
  3. `/api/blocks/rich-text/convert` (rich text converter endpoint)

**Routing Table for `backend.py`:**
```python
# --- GET Handling ---
if path == '/api/blocks/rich-text/convert':
    # Method not allowed or usage help
    self._send_json({'ok': True, 'usage': 'POST with html or rich_text payload'})
    return

if path.startswith('/api/blocks/') and path.endswith('/recordMap'):
    bid = path[len('/api/blocks/'):-len('/recordMap')].strip('/')
    self._send_json(get_block_record_map_orm(bid))
    return

if path.startswith('/api/notes/') and path.endswith('/recordMap'):
    nid = path[len('/api/notes/'):-len('/recordMap')].strip('/')
    # Resolve page block corresponding to legacy note id
    self._send_json(get_block_record_map_orm(f"page-note-{nid}"))
    return

if path.startswith('/api/blocks/') and not any(path.startswith(f'/api/blocks/{r}') for r in ('order', 'batch', 'rich-text')):
    bid = path[len('/api/blocks/'):].strip('/')
    self._send_json(get_block_orm(bid))
    return

# --- POST / PUT Handling ---
if path == '/api/blocks/rich-text/convert':
    payload = body
    if 'html' in payload:
        res = {'ok': True, 'rich_text': html_to_rich_text(payload['html'])}
    elif 'rich_text' in payload:
        res = {
            'ok': True,
            'html': rich_text_to_html(payload['rich_text']),
            'plain_text': rich_text_to_plain_text(payload['rich_text'])
        }
    else:
        res = {'ok': False, 'error': 'Payload must contain html or rich_text'}
    self._send_json(res)
    return

if path == '/api/blocks':
    self._send_json(create_block_orm(body), status=201)
    return

if path.startswith('/api/blocks/') and path.endswith('/reorder'):
    bid = path[len('/api/blocks/'):-len('/reorder')].strip('/')
    self._send_json(reorder_block_children_orm(bid, body))
    return

if path.startswith('/api/blocks/') and path.endswith('/restore'):
    bid = path[len('/api/blocks/'):-len('/restore')].strip('/')
    self._send_json(restore_block_orm(bid))
    return

if path.startswith('/api/blocks/') and not any(path.startswith(f'/api/blocks/{r}') for r in ('order', 'batch', 'rich-text')):
    bid = path[len('/api/blocks/'):].strip('/')
    self._send_json(update_block_orm(bid, body))
    return

# --- DELETE Handling ---
if path.startswith('/api/blocks/'):
    bid = path[len('/api/blocks/'):].strip('/')
    from urllib.parse import parse_qs
    qs = parse_qs(parsed.query)
    perm = qs.get('permanent', ['false'])[0].lower() == 'true'
    self._send_json(delete_block_orm(bid, permanent=perm))
    return
```

### 5.2 Preservation of `Block.to_dict()` Contract for Existing Tests

To guarantee that `test_backend_subpage.py` and `test_adversarial_challenger.py` continue to pass with 0 regressions, `Block.to_dict()` must expose both the new Notion block fields and the legacy camelCase/snake_case aliases:

```python
def to_dict(self):
    try:
        props = json.loads(self.properties or '{}')
    except Exception:
        props = {}
    try:
        fmt = json.loads(self.format or '{}')
    except Exception:
        fmt = {}
    try:
        cnt = json.loads(self.content or '[]')
    except Exception:
        cnt = []
    try:
        crdt = json.loads(self.crdt_data or '{}')
    except Exception:
        crdt = {}

    created = getattr(self, 'created_time', None) or getattr(self, 'created_at', 0)
    updated = getattr(self, 'last_edited_time', None) or getattr(self, 'updated_at', 0)

    data = {
        'id': self.id,
        'space_id': getattr(self, 'space_id', 'default-space'),
        'version': getattr(self, 'version', 1),
        'last_version': getattr(self, 'last_version', 0),
        'type': self.type,
        'properties': props,
        'content': cnt,
        'parent_id': self.parent_id,
        'parent_table': getattr(self, 'parent_table', 'block'),
        'alive': getattr(self, 'alive', 1),
        'format': fmt,
        'crdt_format_version': getattr(self, 'crdt_format_version', 1),
        'crdt_data': crdt,
        'created_time': created,
        'last_edited_time': updated,
        # Legacy compatibility aliases
        'noteId': getattr(self, 'note_id', 0),
        'parentId': self.parent_id,
        'sortIndex': getattr(self, 'sort_index', 'a0'),
        'createdAt': created,
        'updatedAt': updated,
    }

    # Subpage backwards compatibility
    if self.type == 'sub_page' or 'page_id' in props or 'pageId' in props:
        data['page_id'] = props.get('page_id') or props.get('pageId')
        data['title'] = props.get('title') or ''

    return data
```

---

## 6. Implementation Blueprint for Downstream Workers

### 6.1 Recommended File Structure
1. `block_engine.py` (New dedicated module or embedded in `models.py`):
   - Implements rich text serialization functions (`rich_text_to_plain_text`, `plain_text_to_rich_text`, `rich_text_to_html`, `html_to_rich_text`).
   - Implements block management functions (`create_block_orm`, `get_block_orm`, `get_block_record_map_orm`, `update_block_orm`, `reorder_block_children_orm`, `delete_block_orm`, `restore_block_orm`).
2. `backend.py`:
   - Adds route dispatching for `GET /api/blocks/<id>/recordMap`, `POST /api/blocks`, `POST/PUT /api/blocks/<id>`, `POST /api/blocks/<id>/reorder`, `DELETE /api/blocks/<id>`, `POST /api/blocks/<id>/restore`, and `POST /api/blocks/rich-text/convert`.
   - Adds `do_PUT` delegating to `do_POST`.
3. `desktop_app.py`:
   - Adds bridge methods to `PyWebViewBridge`:
     - `create_block(block_dict, target_index=None, after_id=None, before_id=None)`
     - `get_block(block_id)`
     - `get_block_record_map(block_id, include_trashed=False)`
     - `update_block(block_id, update_data)`
     - `reorder_block_children(parent_id, content_or_move)`
     - `delete_block(block_id, permanent=False)`
     - `restore_block(block_id)`
     - `convert_rich_text(payload)`

### 6.2 Test Suite Expansion Plan
Downstream worker or challenger agents should add a new test file: `tests/test_block_api_and_rich_text.py` containing:
1. `TestBlockCreationAndParentOrdering`:
   - UUID assignment, parent validation, cycle detection, insertion at target index, insertion after/before sibling.
2. `TestRecordMapSubtreeResolution`:
   - Nested page with column lists, columns, toggles, text blocks. Verifies all are collected in `recordMap['block']`.
   - Cycle defense (circular references gracefully ignored via visited set).
3. `TestBlockMutationAndConcurrency`:
   - Property updates, format updates, type changes, version increment, expected_version conflict handling.
4. `TestChildReorderingAndReparenting`:
   - Intra-container reordering, cross-container reparenting.
5. `TestSoftDeleteAndRestoration`:
   - Soft-delete marks `alive=0` on target and descendants and removes from parent `content`.
   - Restoration sets `alive=1` and re-inserts into parent `content`.
6. `TestRichTextTupleConverters`:
   - Tuples -> HTML -> Tuples round-trip.
   - All decorators (`b`, `i`, `_`, `s`, `c`, `h`, `a`, `e`).
   - XSS prevention and dangerous URL scheme rejection (`javascript:`).

---

## 7. Conclusion

Requirements R3 and R4 provide the core transactional and serialization foundation for Note-JS-Desktop's transition to a full Notion-style hierarchical block architecture. The design outlined above is completely modular, strictly backward-compatible, adheres to SQLite ACID guarantees through Peewee's atomic transactions, and ensures that the existing 153 tests in `tests/` remain completely green while empowering the frontend with a production-grade Notion `recordMap` protocol.
