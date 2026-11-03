# Handoff Report: Survey Explorer 2 (Requirements R2 & R3)

## 1. Observation

### 1.1 Python Backend & Peewee ORM Data Schema (`models.py`)
- **Note Model (`models.py:61-90`)**:
  ```python
  class Note(BaseModel):
      id = IntegerField(primary_key=True)
      title = CharField(max_length=500, default='Sin título')
      folder = CharField(max_length=120, index=True, default='Personal')
      tags = TextField(default='')
      is_pinned = IntegerField(default=0, index=True)
      content = TextField(default='')
      updated_at = IntegerField(default=0, index=True)
      data_json = TextField(default='{}')
  ```
  `Note.to_dict()` (lines 74-89) deserializes `self.data_json` into dictionary `extra` and overlays `id`, `title`, `folder`, `tags`, `isPinned`, `content`, `updatedAt`. Any custom keys (such as `blocks`) inside `data_json` are preserved.
- **Block Model (`models.py:235-268`)**:
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
  `Block.to_dict()` (lines 253-268) currently deserializes `self.properties` into `props` and returns:
  ```python
  return {
      'id': self.id,
      'noteId': self.note_id,
      'parentId': self.parent_id,
      'type': self.type,
      'properties': props,
      'sortIndex': self.sort_index,
      'createdAt': self.created_at,
      'updatedAt': self.updated_at,
  }
  ```
  Critically, `Block.to_dict()` does **NOT** expose `page_id` or `title` at the top level when `type == 'sub_page'`.
- **Block Sync & Persistence (`models.py:672-716`)**:
  In `sync_blocks_from_note_html_orm(note_id, blocks_data)`:
  ```python
  bid = str(b.get('id') or f"blk-{int(time.time()*1000)}-{len(incoming_ids)}")
  incoming_ids.append(bid)
  btype = str(b.get('type') or 'p')
  parent_id = str(b.get('parentId')) if b.get('parentId') else None
  sort_idx = str(b.get('sortIndex') or 'a0')
  props = json.dumps(b.get('properties') or {})
  ```
  Notice: If an incoming block payload has `{ "type": "sub_page", "id": "uuid", "page_id": "target_note_id", "title": "Título de la nota" }`, `b.get('properties')` is `None` (or `{}`). Therefore, `page_id` and `title` are currently **lost** because they are not copied into `props`.
- **Batch Moves Persistence (`models.py:646`)**:
  In `update_batch_blocks_order_orm(moves)`:
  ```python
  btype = str(m.get('type') or 'p')
  props = json.dumps(m.get('properties') or {})
  ```
  Same vulnerability: top-level `page_id` and `title` are lost if not explicitly saved into `properties`.
- **Note State Signature (`models.py:372-402`)**:
  In `_extract_note_signature(note_obj)`: the signature dictionary checks `title`, `folder`, `tags`, `content`, `emoji`, `hasCover`, `coverStyle`, `showCallout`, `callout`, `showQuote`, `quote`, `showToggle`, `toggleHeader`, `toggleBody`, `showCode`, `code`, `showKanban`, `kanban`, `showTable`, `tableFormula`, `tableRows`, `showChecklist`, `checklists`, `katex`. It does **NOT** currently include `blocks`, which could prevent a history snapshot when only blocks change.
- **Sanitization**:
  There is **no** HTML sanitization or downcasting in `models.py` or `backend.py`. The only regex string cleanup in `models.py` is in `_extract_tags_from_note_dict` (line 1241) and `_extract_mentions_from_note_dict` (line 1260) which strip tags solely for regex mention/tag extraction.

### 1.2 REST API Endpoints & PyWebView Bridge
- **`backend.py`**:
  - `GET /api/notes/<note_id>/blocks` (lines 210-218): invokes `get_note_blocks_orm(note_id)` and returns `{'ok': True, 'noteId': ..., 'blocks': [...]}`.
  - `POST /api/notes/<note_id>/blocks/sync` (lines 486-496): invokes `sync_blocks_from_note_html_orm(note_id, blocks_data)`.
  - `POST /api/blocks/order` (lines 468-476): invokes `update_block_order_orm(...)`.
  - `POST /api/blocks/batch` (lines 479-484): invokes `update_batch_blocks_order_orm(moves)`.
  - `POST /api/notes` (lines 361-366): saves single note with `save_single_note(note_obj)`.
- **`desktop_app.py`**:
  - Bridge methods in `PyWebViewBridge` (lines 128-139):
    - `get_note_blocks(note_id)`
    - `update_block_order(...)`
    - `update_batch_blocks_order(moves)`
    - `sync_note_blocks(note_id, blocks_data)`

### 1.3 Frontend Editor & Block Logic (`frontend/app.js`)
- **Note Loading & Navigation (`frontend/app.js:4016-4058`)**:
  - `selectNote(id)` (lines 4016-4040):
    ```javascript
    function selectNote(id) {
      const numericId = Number(id);
      const note = state.notes.find(n => n.id === numericId);
      if (!note) return;
      if (note.isTrashed) {
        showToast('Restaura la nota desde la papelera para abrirla y editarla', '🗑️');
        return;
      }
      if (state.isHomeActive) {
        exitHomeView();
      }
      state.activeNoteId = numericId;
      if (isTrashFolder(state.selectedFolder)) {
        state.selectedFolder = MASTER_ALL_NOTES_FOLDER;
      }
      if (!Array.isArray(state.openTabIds)) state.openTabIds = [];
      if (!state.openTabIds.includes(numericId)) {
        state.openTabIds.push(numericId);
        saveOpenTabsState();
      }
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      loadActiveNote();
    }
    ```
  - `loadNote` function: **Does not exist** anywhere in `frontend/app.js` or the repository. The user request R3 explicitly references `loadNote(block.page_id)`.
  - `loadActiveNote()` (lines 4042-4150):
    Sets `editorCanvas.innerHTML = note.content || '';` (line 4110) and invokes listener attachments `attachEmbeddedNoteCardListeners()`, `attachImageBlockListeners()`, `tagAllEditorBlocks()`.
- **Block Synchronization from Canvas (`frontend/app.js:4479-4499`)**:
  ```javascript
  function collectAndSyncNoteBlocks(noteId) {
    const editor = document.getElementById('rich-editor-canvas');
    if (!editor || !noteId) return;
    const blocks = [];
    Array.from(editor.children).forEach(el => {
      const id = el.getAttribute('data-block-id');
      if (id) {
        blocks.push({
          id: id,
          noteId: noteId,
          parentId: el.getAttribute('data-parent-id') || null,
          sortIndex: el.getAttribute('data-sort-index') || 'a0',
          type: el.tagName.toLowerCase(),
          properties: { text: el.innerText || '', html: el.innerHTML || '' }
        });
      }
    });
    if (blocks.length > 0 && typeof apiSyncNoteBlocks === 'function') {
      apiSyncNoteBlocks(noteId, blocks);
    }
  }
  ```
  `el.tagName.toLowerCase()` sets `type` to `'div'`. If `.block-subpage` is in the editor, its `type` will default to `'div'` instead of `'sub_page'`, unless `getAttribute('data-type')` is read.
- **Existing Subpage Creation (`frontend/app.js:5964-6000`)**:
  `insertSubpageBlock()` currently creates a new note in `state.notes`, but then calls `insertNoteCardAtSelection(newId, savedSelectionRange)` which generates a large vertical `.note-embedded-card` with gradient cover, rather than a `.block-subpage` component.
- **Block Rendering Dispatcher**:
  There is currently **no** function in `frontend/app.js` that iterates over blocks with a `switch` statement (`switch (block.type) { case ... }`).

### 1.4 CSS Styling (`frontend/styles.css`)
- `.block-subpage`: Does not exist in `frontend/styles.css`.
- Theme background and text variables:
  - Dark mode (default): `--bg-elevated: #1e2128;`, `--text-primary: #f3f4f6;`
  - Light mode (`body.light-mode`): `--bg-elevated: #f1f5f9;`, `--text-primary: #0f172a;`
  - Hover states on list items typically use `var(--bg-elevated)` or `rgba(128, 128, 128, 0.12)`.

---

## 2. Logic Chain

1. **R2 Block Schema & SQLite Persistence**:
   - The user requires blocks with schema: `{ "type": "sub_page", "id": "uuid", "page_id": "target_note_id", "title": "Título de la nota" }`.
   - In `models.py:685-695`, `sync_blocks_from_note_html_orm` reads `props = json.dumps(b.get('properties') or {})`. If `page_id` and `title` are top-level properties on `b`, they are dropped because they are not under `'properties'`.
   - Therefore, `sync_blocks_from_note_html_orm` and `update_batch_blocks_order_orm` must be modified to merge top-level `page_id` and `title` into `props_dict` when `btype == 'sub_page'` or when those keys are present.
   - Correspondingly, `Block.to_dict()` (line 253) must unwrap `page_id` and `title` from `props` and expose them as top-level keys in the serialized block dictionary.
   - In `_extract_note_signature(note_obj)`, adding `'blocks'` ensures changes to block lists trigger note version history.

2. **R3 DOM Rendering & Navigation**:
   - Requirement R3 states: "En la función que renderiza el DOM iterando los bloques, añadir el caso `case 'sub_page':`. Generar un componente HTML (un `div` con clase `.block-subpage`) que muestre un ícono de documento (📄) seguido del título. Aplicar `cursor: pointer` y estilos de hover (fondo gris claro). Asignar un manejador de eventos `onclick` que dispare la función de navegación (ej. `loadNote(block.page_id)`) para abrir esa sub-nota..."
   - Because no `renderBlock` or `switch (block.type)` exists in `frontend/app.js`, we must introduce:
     - `renderBlock(block)` containing `switch (block.type) { case 'sub_page': ... default: ... }`.
     - `renderBlocks(blocks, container)` to iterate and append rendered blocks.
     - `attachSubpageBlockListeners()` to bind `onclick` handlers on `.block-subpage` elements loaded into `#rich-editor-canvas`.
   - `loadNote(pageId)` must be implemented globally on `window`:
     - Checks if `pageId` is missing/null/empty -> shows warning toast `showToast('ID de nota inválido', '⚠️')`, returns `false`.
     - Finds note in `state.notes` matching `String(n.id) === String(pageId) || Number(n.id) === Number(pageId)`.
     - If not found -> `showToast('Nota no encontrada', '⚠️')`, returns `false`.
     - If in trash -> `showToast('Restaura la nota desde la papelera para abrirla y editarla', '🗑️')`, returns `false`.
     - If valid -> calls `selectNote(note.id)` and returns `true`.

3. **Styling `.block-subpage`**:
   - Add `.block-subpage` styles to `frontend/styles.css`:
     - `display: flex; align-items: center; gap: 8px;`
     - `cursor: pointer;`
     - `padding: 6px 10px; border-radius: 6px;`
     - Light gray hover: `background: rgba(128, 128, 128, 0.12);` (in dark mode) and `background: #e5e7eb;` (in `body.light-mode`).
     - Display `📄` in `.subpage-icon` and title in `.subpage-title`.

---

## 3. Caveats

- **Existing `.note-embedded-card`**: The application previously had a large visual card format for shortcuts (`.note-embedded-card`). The new `.block-subpage` is a clean inline Notion-style block row (`📄 Title`). We should ensure both can coexist without breaking existing notes that already contain `.note-embedded-card` in `content`.
- **String vs Number IDs**: `note.id` in `Note` is an integer (e.g. `1` or timestamp `1730310000000`), but block IDs and `page_id` in the prompt can be UUID strings or string IDs. `loadNote` must compare both via `String(n.id) === String(pageId)` and `Number(n.id) === Number(pageId)`.
- **Read-Only Scope**: This report contains investigation and design recommendations only; source code was not modified.

---

## 4. Conclusion & Concrete Recommendations

### 4.1 Backend Recommendations (`models.py`)

1. **`Block.to_dict()` (`models.py:253-268`)**:
   Update to expose `page_id` and `title` at the top level:
   ```python
   def to_dict(self):
       try:
           props = json.loads(self.properties or '{}')
       except Exception:
           props = {}
       data = {
           'id': self.id,
           'noteId': self.note_id,
           'parentId': self.parent_id,
           'type': self.type,
           'properties': props,
           'sortIndex': self.sort_index,
           'createdAt': self.created_at,
           'updatedAt': self.updated_at,
       }
       if self.type == 'sub_page' or 'page_id' in props:
           data['page_id'] = props.get('page_id') or props.get('pageId')
           data['title'] = props.get('title') or ''
       return data
   ```

2. **`sync_blocks_from_note_html_orm()` (`models.py:672-716`)**:
   Ensure top-level `page_id` and `title` are preserved in `props`:
   ```python
   for b in blocks_data:
       bid = str(b.get('id') or f"blk-{int(time.time()*1000)}-{len(incoming_ids)}")
       incoming_ids.append(bid)
       btype = str(b.get('type') or 'p')
       parent_id = str(b.get('parentId')) if b.get('parentId') else None
       sort_idx = str(b.get('sortIndex') or 'a0')
       raw_props = b.get('properties')
       props_dict = dict(raw_props) if isinstance(raw_props, dict) else {}
       if btype == 'sub_page' or 'page_id' in b or 'pageId' in b:
           if 'page_id' in b:
               props_dict['page_id'] = b.get('page_id')
           elif 'pageId' in b:
               props_dict['page_id'] = b.get('pageId')
           if 'title' in b:
               props_dict['title'] = b.get('title')
       props = json.dumps(props_dict, ensure_ascii=False)
   ```

3. **`update_batch_blocks_order_orm()` (`models.py:646`)**:
   Same mapping for `moves`:
   ```python
   btype = str(m.get('type') or 'p')
   raw_props = m.get('properties')
   props_dict = dict(raw_props) if isinstance(raw_props, dict) else {}
   if btype == 'sub_page' or 'page_id' in m or 'pageId' in m:
       if 'page_id' in m:
           props_dict['page_id'] = m.get('page_id')
       elif 'pageId' in m:
           props_dict['page_id'] = m.get('pageId')
       if 'title' in m:
           props_dict['title'] = m.get('title')
   props = json.dumps(props_dict, ensure_ascii=False)
   ```

4. **`_extract_note_signature()` (`models.py:372-402`)**:
   Add `'blocks': note_obj.get('blocks') or []` to the signature dictionary.

5. **`firebase-blueprint.json`**:
   Add `SubPageBlock` definition in the schema entity definitions for formal schema validation.

### 4.2 Frontend Recommendations (`frontend/app.js`)

1. **Implement `loadNote(pageId)`**:
   ```javascript
   function loadNote(pageId) {
     if (!pageId && pageId !== 0) {
       showToast('ID de nota inválido', '⚠️');
       return false;
     }
     const note = state.notes.find(n => String(n.id) === String(pageId) || Number(n.id) === Number(pageId));
     if (!note) {
       showToast('Nota no encontrada', '⚠️');
       return false;
     }
     if (note.isTrashed) {
       showToast('Restaura la nota desde la papelera para abrirla y editarla', '🗑️');
       return false;
     }
     selectNote(note.id);
     return true;
   }
   window.loadNote = loadNote;
   ```

2. **Implement `renderBlock(block)` & `renderBlocks(blocks, container)`**:
   ```javascript
   function renderBlock(block) {
     if (!block || !block.type) return null;
     switch (block.type) {
       case 'sub_page': {
         const div = document.createElement('div');
         div.className = 'block-subpage';
         div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
         div.setAttribute('data-block-id', div.id);
         div.setAttribute('data-type', 'sub_page');
         const pageId = block.page_id || (block.properties && block.properties.page_id) || '';
         const title = block.title || (block.properties && block.properties.title) || 'Sin título';
         div.setAttribute('data-page-id', String(pageId));
         div.setAttribute('data-title', title);
         div.setAttribute('contenteditable', 'false');
         div.innerHTML = `<span class="subpage-icon">📄</span><span class="subpage-title">${escapeHtmlAttr(title)}</span>`;
         div.onclick = function(e) {
           e.preventDefault();
           e.stopPropagation();
           loadNote(pageId);
         };
         return div;
       }
       case 'p':
       default: {
         const p = document.createElement('p');
         if (block.id) p.id = block.id;
         p.innerHTML = (block.properties && block.properties.html) || (block.properties && block.properties.text) || '';
         return p;
       }
     }
   }

   function renderBlocks(blocks, container = null) {
     const target = container || document.getElementById('rich-editor-canvas');
     if (!target || !Array.isArray(blocks)) return;
     target.innerHTML = '';
     blocks.forEach(block => {
       const el = renderBlock(block);
       if (el) target.appendChild(el);
     });
     attachSubpageBlockListeners();
   }
   ```

3. **Implement `attachSubpageBlockListeners()`**:
   ```javascript
   function attachSubpageBlockListeners() {
     const canvas = document.getElementById('rich-editor-canvas');
     if (!canvas) return;
     canvas.querySelectorAll('.block-subpage').forEach(el => {
       if (!el.dataset.subpageListenerAttached) {
         el.dataset.subpageListenerAttached = 'true';
         el.setAttribute('contenteditable', 'false');
         const pageId = el.getAttribute('data-page-id');
         el.onclick = function(e) {
           e.preventDefault();
           e.stopPropagation();
           loadNote(pageId);
         };
       }
     });
   }
   ```
   Call `attachSubpageBlockListeners()` inside `loadActiveNote()` at line 4120.

4. **Update `collectAndSyncNoteBlocks()` (`frontend/app.js:4479-4499`)**:
   Check if `el.classList.contains('block-subpage')` or `el.getAttribute('data-type') === 'sub_page'`. When true:
   ```javascript
   const isSubpage = el.classList.contains('block-subpage') || el.getAttribute('data-type') === 'sub_page';
   const btype = isSubpage ? 'sub_page' : (el.getAttribute('data-type') || el.tagName.toLowerCase());
   const blockObj = {
     id: id,
     noteId: noteId,
     parentId: el.getAttribute('data-parent-id') || null,
     sortIndex: el.getAttribute('data-sort-index') || 'a0',
     type: btype,
     properties: { text: el.innerText || '', html: el.innerHTML || '' }
   };
   if (isSubpage) {
     const pageId = el.getAttribute('data-page-id');
     const title = el.getAttribute('data-title') || el.querySelector('.subpage-title')?.innerText || '';
     blockObj.page_id = pageId;
     blockObj.title = title;
     blockObj.properties.page_id = pageId;
     blockObj.properties.title = title;
   }
   blocks.push(blockObj);
   ```

5. **Update `insertSubpageBlock()` (`frontend/app.js:5964-6000`)**:
   When creating a subpage, generate a `.block-subpage` element or HTML:
   ```html
   <div class="block-subpage" data-block-id="blk-${Date.now()}" data-page-id="${newId}" data-type="sub_page" contenteditable="false"><span class="subpage-icon">📄</span><span class="subpage-title">${escapeHtmlAttr(subpage.title)}</span></div>
   ```
   Insert it at selection in `rich-editor-canvas`, invoke `attachSubpageBlockListeners()`, and trigger `syncRichEditor()`.

### 4.3 Styling Recommendations (`frontend/styles.css`)

Add to `frontend/styles.css`:
```css
/* Sub-note Block Component */
.block-subpage {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  margin: 4px 0;
  border-radius: 6px;
  cursor: pointer;
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.5;
  transition: background 0.15s ease, transform 0.05s ease;
  user-select: none;
  border: 1px solid transparent;
}
.block-subpage:hover {
  background: rgba(128, 128, 128, 0.12); /* light gray hover effect */
}
body.light-mode .block-subpage:hover {
  background: #e5e7eb; /* clean light gray hover in light theme */
}
.block-subpage:active {
  transform: scale(0.99);
}
.block-subpage .subpage-icon {
  font-size: 16px;
  line-height: 1;
  flex-shrink: 0;
}
.block-subpage .subpage-title {
  flex: 1;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-decoration: underline;
  text-underline-offset: 3px;
  text-decoration-color: rgba(128, 128, 128, 0.4);
}
.block-subpage:hover .subpage-title {
  text-decoration-color: var(--text-primary);
}
```

---

## 5. Verification Method

1. **Python Database & Model Test**:
   Execute unit test using the installed Python binary:
   ```powershell
   & 'C:\Users\Joaco\AppData\Local\Python\bin\python.exe' -m unittest discover -s tests -p "test_*.py"
   ```
   Specific test script to verify:
   - Call `sync_blocks_from_note_html_orm(note_id, [{ "type": "sub_page", "id": "test-uuid-1", "page_id": "note-999", "title": "Subnota de prueba" }])`.
   - Call `get_note_blocks_orm(note_id)`.
   - Assert block returns `'type': 'sub_page'`, `'page_id': 'note-999'`, `'title': 'Subnota de prueba'` without data loss or downcasting.

2. **Frontend DOM & Navigation Verification**:
   - Verify `window.loadNote` is defined as a function.
   - Verify calling `window.loadNote(null)` or `window.loadNote('invalid-id')` displays toast and returns `false` without crashing.
   - Verify calling `renderBlock({ type: 'sub_page', id: 'b1', page_id: '1', title: 'Subnota' })` returns an `HTMLDivElement` with class `.block-subpage`, containing `📄` and `Subnota`.
   - Verify clicking `.block-subpage` triggers `loadNote(block.page_id)` and switches the active note in `state.activeNoteId`.

3. **Visual Inspection**:
   - Inspect `.block-subpage` in browser developer tools: verify `cursor: pointer` is computed and hovering displays the light gray background.
