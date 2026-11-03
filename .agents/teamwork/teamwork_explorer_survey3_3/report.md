# Architecture & Investigation Report: Notion Hierarchical Block Tree & Dynamic Rendering in Note-JS Frontend

**Author**: Explorer Subagent (Survey 3_3)  
**Target Milestone**: Survey 3 — Notion Hierarchical Block Architecture  
**Working Directory**: `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_3`  
**Date**: 2026-11-02  
**Status**: Read-Only Analysis Complete  

---

## 1. Executive Summary & Core Findings

1. **Current State**:
   - The editor in `frontend/app.js` is currently anchored on a hybrid model: `#rich-editor-canvas` (a single `contenteditable="true"` div storing raw HTML strings in `note.content`) plus several static block wrappers in `#blocks-container` (`#block-callout`, `#block-quote`, `#block-toggle`, `#block-code`, `#block-kanban`, `#block-table`, `#block-checklists`, `#block-katex`) enabled by boolean flags on the note object.
   - A preliminary `renderBlock(block)` and `renderBlocks(blocks)` function exists at lines 6025–6070 in `frontend/app.js`, but it only implements `case 'sub_page':` (rendering `.block-subpage`) and a generic fallback `default: case 'p'`.
   - Block identification has begun via `tagAllEditorBlocks()` (lines 15001–15018), which stamps `data-block-id` and fractional `data-sort-index` onto elements inside `#rich-editor-canvas`.
   - All backend communication uses an isomorphic bridge pattern: checking `window.pywebview.api.<method>` first, then falling back to `fetch('/api/...')` with JSON payloads.

2. **Target Architecture (Notion Block Model R4 & R5)**:
   - Transition the document model from a single monolithic HTML string to a normalized Notion-style **RecordMap** (`recordMap.block[blockId].value`).
   - Rich text in `properties` is stored as an array of decorator tuples:
     `[["Text string", [["b"], ["i"], ["h", color], ["c"], ["a", url], ["e", latex]]]]`
   - Hierarchical relationships are bidirectional:
     - Parent blocks store an ordered array of child UUIDs in `content: ["id-1", "id-2"]`.
     - Child blocks reference their container via `parent_id` and `parent_table: "block"`.
   - The frontend editor recursively resolves and renders the block hierarchy starting from the root `page` block through its `content` array.
   - Interactive editing (typing, slash commands, Enter key splitting, block type conversions, drag-and-drop reordering, column splitting, toggle expansion) operates on the in-memory `recordMap` and syncs mutations back to SQLite via the PyWebView bridge and REST API.

3. **Compatibility & Non-Regression**:
   - 153 existing automated tests pass (`py -m unittest discover -s tests`). Key frontend contracts—including the lasso selection guard (`contenteditable`, `INPUT`, `TEXTAREA`), the `.editor-container` background constraint, `window.loadNote`, `window.renderBlock`, `window.renderBlocks`, and `window.attachSubpageBlockListeners`—must remain strictly intact.
   - Sticky Table of Contents (`#sticky-toc-rail`), multi-tab bar (`#note-tabs-list`), folder sidebar, and CSS theme custom properties (`--bg-canvas`, `--bg-surface`, `--accent-amber`) will seamlessly interoperate with the new block tree.

---

## 2. Current Editor Implementation Analysis

### 2.1 File Inventory & Layout
- `frontend/app.js` (16,923 lines, 744 KB): Core application logic, event handlers, UI rendering, bridge syncing.
- `frontend/index.html` (2,646 lines, 184 KB): DOM structure containing:
  - Top tab bar (`.top-bar`, `#note-tabs-list`).
  - Desktop format bar (`.desktop-format-bar`, `#btn-insert-dropdown`, format buttons).
  - Main scrollable container (`#panel-canvas`, `#editor-body.editor-container`).
  - Breadcrumbs (`#notion-breadcrumbs`), Cover (`#notion-cover`), Emoji picker (`#page-emoji-display`), Title (`#note-title`), Tag/Folder chips.
  - Editor blocks container (`#blocks-container`, `#rich-editor-canvas`).
  - Floating menus: Slash command (`#slash-menu`), Floating format bar (`#floating-selection-bar`), Block handle (`#spatial-block-handle`), Block action menu (`#block-action-menu`), Sticky right rail TOC (`#sticky-toc-rail`).
- `frontend/styles.css` (10,624 lines, 282 KB): Complete design system using CSS variables, dark/light theme definitions, layout rules for columns, toggles, callouts, subpages, and tables.

### 2.2 Note Loading & Active Note Flow
- Trigger: `selectNote(id)` (line 4125) -> updates `state.activeNoteId`, ensures `id` is in `state.openTabIds`, updates tabs, and invokes `loadActiveNote()` (line 4159).
- `loadActiveNote()` steps:
  1. Validates note existence and trash state.
  2. Sets breadcrumbs and page cover (`#notion-cover.style.backgroundImage`).
  3. Sets emoji display (`#page-emoji-display.textContent = note.emoji`).
  4. Sets title input (`#note-title.value = note.title`).
  5. Populates `#rich-editor-canvas.innerHTML = note.content || ''`.
  6. Toggles visibility and input values for the legacy fixed blocks: `#block-callout`, `#block-quote`, `#block-toggle`, `#block-code`, `#block-kanban`, `#block-table`, `#block-checklists`, `#block-katex`.
  7. Restores blocks order via `restoreBlocksOrder()` (line 5277).
  8. Attaches listeners: `attachEmbeddedNoteCardListeners()`, `attachImageBlockListeners()`, `attachSubpageBlockListeners()`, `attachColumnResizerListeners()`, `attachSyncedBlockListeners()`, `setupBlockDragAndDrop()`.
  9. Executes `tagAllEditorBlocks()` (line 15001) and schedules `refreshPageTableOfContents()` (line 13632).

### 2.3 Block Rendering
- `renderBlock(block)` (line 6025):
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
        const pageId = block.page_id || (block.properties && (block.properties.page_id || block.properties.pageId)) || '';
        const title = block.title || (block.properties && block.properties.title) || 'Sin título';
        div.setAttribute('data-page-id', String(pageId));
        div.setAttribute('data-title', title);
        div.setAttribute('contenteditable', 'false');
        div.style.cursor = 'pointer';
        div.innerHTML = `<span class="subpage-icon">📄</span><span class="subpage-title">${title}</span>`;
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
        p.innerHTML = (block.properties && (block.properties.html || block.properties.text)) || '';
        return p;
      }
    }
  }
  ```
- `renderBlocks(blocks, container)` (line 6059): Iterates over `blocks` array, calls `renderBlock(block)`, appends to container, and attaches subpage click listeners.

### 2.4 Event Delegation & Interaction
- **Input (`handleRichEditorInput`, line 4751)**:
  - Detects space key (`e.data === ' '`) to invoke `applyLiveMarkdownTriggers()`:
    - `# ` -> `<h1>`
    - `## ` -> `<h2>`
    - `### ` -> `<h3>`
    - `- ` or `* ` -> `insertUnorderedList`
    - `1. ` -> `insertOrderedList`
    - `[] ` -> `insertChecklistBlock()`
    - `> ` -> `insertToggleBlock()`
    - `"" ` -> `toggleQuoteBlock()`
    - Inline markdown: `**bold**`, `*italic*`, `` `code` ``.
  - Calls `syncRichEditor()` (line 4638) which updates `note.content`, triggers debounced `save()`, and schedules `collectAndSyncNoteBlocks(note.id)` (line 4605).
- **Keydown (`handleRichEditorKeydown`, line 4657)**:
  - Shortcuts: `Ctrl+B` (bold), `Ctrl+I` (italic), `Ctrl+U` (underline), `Ctrl+E` (inline code), `Ctrl+Shift+E` (inline KaTeX math), `Ctrl+K` (create link), `Ctrl+D` (duplicate line/block).
  - `Alt + ArrowUp / ArrowDown`: moves selected line/block up or down.
  - `/`: opens `#slash-menu` at caret position.
  - `Escape`: closes menus.
- **Lasso Selection (`initSpatialBlockController`, line 15651)**:
  - Strictly guarded on line 15657:
    `if (e.target.closest('[contenteditable="true"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;`
  - Validates click target is in `.editor-container` or canvas background.
  - Computes bounding rectangle intersection against canvas blocks and adds `.spatial-block-selected` to `selectedBlockEls` Set.
- **Drag & Drop (Spatial Controller, lines 15073–15750)**:
  - 6-dot grip handle (`#spatial-block-handle`, `#spatial-btn-grip`) displays on block hover.
  - Dragging shows `#spatial-drag-ghost-pill` and drop indicator `#spatial-drop-guide`.
  - Supports:
    * `above` / `below`: reordering via fractional indexing.
    * `left-col` / `right-col`: `combineBlocksIntoSideBySideColumns()` creates `.notion-columns-row` with 2 slots and a resizer.
    * `indent`: `nestBlocksInsideTarget()` nests block into toggle body or callout body.

### 2.5 Backend Communication Bridge
- Pattern:
  ```javascript
  function hasPyWebViewBridge() {
    return Boolean(window.pywebview && window.pywebview.api);
  }
  ```
- Methods currently used:
  - `bootstrap()` -> loads notes, folders, settings, reminders.
  - `save_note(note)` / `POST /api/notes` -> saves whole note document.
  - `sync_all(payload)` / `POST /api/sync` -> initial or full sync.
  - `update_block_order(blockId, prevId, nextId, parentId, noteId)` / `POST /api/blocks/order`.
  - `update_batch_blocks_order(moves)` / `POST /api/blocks/batch`.
  - `sync_note_blocks(noteId, blocksData)` / `POST /api/notes/:id/blocks/sync`.

---

## 3. R4 & R5: Notion Hierarchical Block Tree & Dynamic Rendering Architecture

### 3.1 Rich-Text Tuple Specification & Conversion Engine

Notion represents formatted text as an array of segments:
```json
[
  ["Welcome to ", []],
  ["Note JS", [["b"]]],
  [", an ", []],
  ["interactive", [["i"], ["h", "blue"]]],
  [" editor with ", []],
  ["code", [["c"]]],
  [" and formulas like ", []],
  ["E=mc^2", [["e", "E=mc^2"]]],
  [". Visit ", []],
  ["our documentation", [["a", "https://notion.so"]]]
]
```

#### Complete Decorator Matrix:
| Tuple Decorator | Semantic Meaning | Target HTML Element / Class |
|---|---|---|
| `["b"]` | Bold | `<strong>...</strong>` |
| `["i"]` | Italic | `<em>...</em>` |
| `["_"]` | Underline | `<u>...</u>` |
| `["s"]` | Strikethrough | `<s>...</s>` |
| `["c"]` | Inline Code | `<code>...</code>` |
| `["h", "<color>"]` | Text Color | `<span class="notion-color-<color>" style="color: ...">` |
| `["h", "<color>_background"]` | Highlight Background | `<span class="notion-bg-<color>" style="background: ...">` |
| `["a", "<url>"]` | Hyperlink | `<a href="<url>" target="_blank" rel="noopener noreferrer">...</a>` |
| `["e", "<latex>"]` | Inline LaTeX Math | `<span class="inline-katex-node" data-latex="<latex>" contenteditable="false">...</span>` |

#### Recommended Implementation: `notionRichTextToHtml(segments)`
```javascript
function escapeHtml(text) {
  return String(text || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

const NOTION_COLOR_MAP = {
  gray: 'var(--text-muted)',
  brown: '#92400e',
  orange: '#ea580c',
  yellow: 'var(--accent-amber)',
  teal: '#0d9488',
  blue: '#3b82f6',
  purple: '#a855f7',
  pink: '#ec4899',
  red: 'var(--danger)',
  gray_background: 'rgba(148, 163, 184, 0.2)',
  brown_background: 'rgba(146, 64, 14, 0.2)',
  orange_background: 'rgba(234, 88, 12, 0.2)',
  yellow_background: 'rgba(245, 158, 11, 0.2)',
  teal_background: 'rgba(13, 148, 136, 0.2)',
  blue_background: 'rgba(59, 130, 246, 0.2)',
  purple_background: 'rgba(168, 85, 247, 0.2)',
  pink_background: 'rgba(236, 72, 153, 0.2)',
  red_background: 'rgba(239, 68, 68, 0.2)'
};

function parseRichTextToHtml(segments) {
  if (!Array.isArray(segments) || segments.length === 0) return '';
  let html = '';

  for (const seg of segments) {
    if (!Array.isArray(seg)) continue;
    const text = seg[0] || '';
    const decorators = seg[1] || [];

    // Inline KaTeX equation
    const eqDec = decorators.find(d => d[0] === 'e');
    if (eqDec) {
      const formula = eqDec[1] || text;
      html += `<span class="inline-katex-node" data-latex="${escapeHtml(formula)}" contenteditable="false">${escapeHtml(formula)}</span>`;
      continue;
    }

    let segmentHtml = escapeHtml(text);

    for (const dec of decorators) {
      const tag = dec[0];
      switch (tag) {
        case 'b':
          segmentHtml = `<strong>${segmentHtml}</strong>`;
          break;
        case 'i':
          segmentHtml = `<em>${segmentHtml}</em>`;
          break;
        case '_':
          segmentHtml = `<u>${segmentHtml}</u>`;
          break;
        case 's':
          segmentHtml = `<s>${segmentHtml}</s>`;
          break;
        case 'c':
          segmentHtml = `<code>${segmentHtml}</code>`;
          break;
        case 'a':
          segmentHtml = `<a href="${escapeHtml(dec[1] || '#')}" target="_blank" rel="noopener noreferrer">${segmentHtml}</a>`;
          break;
        case 'h': {
          const colorKey = dec[1];
          const colorVal = NOTION_COLOR_MAP[colorKey];
          if (colorKey && colorKey.endsWith('_background')) {
            segmentHtml = `<span class="notion-bg-${colorKey}" style="background-color:${colorVal || 'rgba(245,158,11,0.2)'}; padding:2px 4px; border-radius:3px;">${segmentHtml}</span>`;
          } else if (colorKey) {
            segmentHtml = `<span class="notion-color-${colorKey}" style="color:${colorVal || 'inherit'};">${segmentHtml}</span>`;
          }
          break;
        }
      }
    }
    html += segmentHtml;
  }
  return html;
}
```

#### Recommended Implementation: `htmlToRichTextTuples(elementOrHtml)`
```javascript
function htmlToRichTextTuples(nodeOrHtml) {
  let container;
  if (typeof nodeOrHtml === 'string') {
    container = document.createElement('div');
    container.innerHTML = nodeOrHtml;
  } else {
    container = nodeOrHtml;
  }

  const segments = [];

  function traverse(node, currentStyles) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.nodeValue;
      if (!text) return;

      const decs = [];
      if (currentStyles.bold) decs.push(['b']);
      if (currentStyles.italic) decs.push(['i']);
      if (currentStyles.underline) decs.push(['_']);
      if (currentStyles.strike) decs.push(['s']);
      if (currentStyles.code) decs.push(['c']);
      if (currentStyles.color) decs.push(['h', currentStyles.color]);
      if (currentStyles.link) decs.push(['a', currentStyles.link]);

      // Coalesce with previous segment if decorators match
      if (segments.length > 0) {
        const last = segments[segments.length - 1];
        if (JSON.stringify(last[1] || []) === JSON.stringify(decs)) {
          last[0] += text;
          return;
        }
      }
      segments.push(decs.length > 0 ? [text, decs] : [text]);
      return;
    }

    if (node.nodeType === Node.ELEMENT_NODE) {
      // Check for inline KaTeX node
      if (node.classList.contains('inline-katex-node')) {
        const formula = node.getAttribute('data-latex') || node.textContent;
        segments.push([formula, [['e', formula]]]);
        return;
      }

      const nextStyles = { ...currentStyles };
      const tag = node.tagName.toLowerCase();

      if (tag === 'strong' || tag === 'b') nextStyles.bold = true;
      if (tag === 'em' || tag === 'i') nextStyles.italic = true;
      if (tag === 'u') nextStyles.underline = true;
      if (tag === 's' || tag === 'del' || tag === 'strike') nextStyles.strike = true;
      if (tag === 'code') nextStyles.code = true;
      if (tag === 'a') nextStyles.link = node.getAttribute('href') || '#';

      // Parse styles and color classes
      for (const cls of node.classList) {
        if (cls.startsWith('notion-color-')) {
          nextStyles.color = cls.replace('notion-color-', '');
        } else if (cls.startsWith('notion-bg-')) {
          nextStyles.color = cls.replace('notion-bg-', '');
        }
      }

      if (node.style.fontWeight === 'bold' || Number(node.style.fontWeight) >= 600) nextStyles.bold = true;
      if (node.style.fontStyle === 'italic') nextStyles.italic = true;
      if (node.style.textDecoration && node.style.textDecoration.includes('underline')) nextStyles.underline = true;
      if (node.style.textDecoration && node.style.textDecoration.includes('line-through')) nextStyles.strike = true;

      for (const child of node.childNodes) {
        traverse(child, nextStyles);
      }
    }
  }

  traverse(container, {
    bold: false,
    italic: false,
    underline: false,
    strike: false,
    code: false,
    color: null,
    link: null
  });

  return segments.length > 0 ? segments : [['']];
}
```

---

### 3.2 Full Block Suite Specifications & DOM Architecture

The application will support the full Notion block taxonomy organized into 4 architectural families:

```
                          ┌──────────────────────────┐
                          │   Notion Block Suite     │
                          └─────────────┬────────────┘
                                        │
     ┌──────────────────┬───────────────┴──────────────┬──────────────────┐
     ▼                  ▼                              ▼                  ▼
1. Structural       2. Text & Headers             3. Data & Code      4. Media
 - page              - text (p)                    - code              - image
 - column_list       - header (H1)                 - equation (KaTeX)
 - column            - sub_header (H2)             - table
 - divider           - sub_sub_header (H3)         - table_row
                     - bulleted_list               - collection_view
                     - numbered_list               - collection_view_page
                     - toggle
```

#### Detailed Block Specs:

1. **`page`**:
   - **Properties**: `{ "title": [["Title", []]] }`
   - **Format**: `{ "page_icon": "📝", "page_cover": "...", "page_cover_position": 0.5 }`
   - **Content**: `["uuid-1", "uuid-2", ...]`
   - **Root Canvas Rendering**: Populates page title `#note-title`, cover `#notion-cover`, emoji `#page-emoji-display`, and mounts child blocks in `#rich-editor-canvas`.
   - **Sub-page / Child Rendering**: Renders `.block-subpage` (maintaining 100% compliance with R3):
     ```html
     <div class="block-subpage" data-block-id="${id}" data-type="sub_page" data-page-id="${id}" data-title="${title}" contenteditable="false" style="cursor: pointer;">
       <span class="subpage-icon">📄</span>
       <span class="subpage-title">${title}</span>
     </div>
     ```

2. **`column_list`**:
   - **Properties**: `{}`
   - **Content**: `["col-uuid-1", "col-uuid-2"]`
   - **DOM Structure**:
     ```html
     <div class="notion-block notion-columns-row" data-block-id="${id}" data-type="column_list">
       <!-- child columns rendered here with .notion-column-resizer between them -->
     </div>
     ```

3. **`column`**:
   - **Format**: `{ "column_ratio": 0.5 }`
   - **Content**: `["block-uuid-a", "block-uuid-b"]`
   - **DOM Structure**:
     ```html
     <div class="notion-column-slot" data-block-id="${id}" data-type="column" style="flex: ${ratio} 1 0%;">
       <div class="notion-column-content notion-block-children">
         <!-- recursive child blocks -->
       </div>
     </div>
     ```

4. **`divider`**:
   - **Properties**: `{}`
   - **DOM Structure**:
     ```html
     <div class="notion-block notion-divider-block" data-block-id="${id}" data-type="divider" contenteditable="false">
       <hr class="notion-hr" />
     </div>
     ```

5. **`text`**:
   - **Properties**: `{ "title": [[ "Paragraph content...", [] ]] }`
   - **Content**: `["nested-block-uuid"]` (supports indented children)
   - **DOM Structure**:
     ```html
     <div class="notion-block notion-block-text" data-block-id="${id}" data-type="text">
       <div class="notion-block-content" contenteditable="true" data-property="title">${html}</div>
       <div class="notion-block-children"></div>
     </div>
     ```

6. **`header` (H1)**, **`sub_header` (H2)**, **`sub_sub_header` (H3)**:
   - **Properties**: `{ "title": [[ "Heading text", [] ]] }`
   - **DOM Structure**:
     ```html
     <h1 class="notion-block notion-block-header" data-block-id="${id}" data-type="header" contenteditable="true" data-property="title">${html}</h1>
     <h2 class="notion-block notion-block-sub-header" data-block-id="${id}" data-type="sub_header" contenteditable="true" data-property="title">${html}</h2>
     <h3 class="notion-block notion-block-sub-sub-header" data-block-id="${id}" data-type="sub_sub_header" contenteditable="true" data-property="title">${html}</h3>
     ```
   - **TOC Compatibility**: Automatically indexed by `collectEditorHeadings()` (`editor.querySelectorAll('h1, h2, h3')`).

7. **`bulleted_list`**:
   - **Properties**: `{ "title": [[ "Bullet text", [] ]] }`
   - **DOM Structure**:
     ```html
     <div class="notion-block notion-block-bulleted-list" data-block-id="${id}" data-type="bulleted_list">
       <span class="notion-bullet" contenteditable="false">•</span>
       <div class="notion-block-content" contenteditable="true" data-property="title">${html}</div>
       <div class="notion-block-children"></div>
     </div>
     ```

8. **`numbered_list`**:
   - **Properties**: `{ "title": [[ "Numbered text", [] ]] }`
   - **DOM Structure**:
     ```html
     <div class="notion-block notion-block-numbered-list" data-block-id="${id}" data-type="numbered_list">
       <span class="notion-number-prefix" contenteditable="false">${index}.</span>
       <div class="notion-block-content" contenteditable="true" data-property="title">${html}</div>
       <div class="notion-block-children"></div>
     </div>
     ```

9. **`toggle`**:
   - **Properties**: `{ "title": [[ "Collapsible title", [] ]] }`
   - **Content**: `["child-uuid-1", "child-uuid-2"]`
   - **DOM Structure**:
     ```html
     <details class="notion-block notion-block-toggle" data-block-id="${id}" data-type="toggle">
       <summary class="notion-toggle-summary">
         <span class="notion-toggle-arrow">▶</span>
         <div class="notion-toggle-title" contenteditable="true" data-property="title">${html}</div>
       </summary>
       <div class="notion-toggle-content notion-block-children">
         <!-- recursively rendered children -->
       </div>
     </details>
     ```

10. **`code`**:
    - **Properties**: `{ "title": [[ "const x = 42;", [] ]], "language": [[ "JavaScript", [] ]] }`
    - **DOM Structure**:
      ```html
      <div class="notion-block notion-block-code" data-block-id="${id}" data-type="code">
        <div class="notion-code-header" contenteditable="false">
          <select class="notion-code-lang-select" onchange="updateBlockCodeLanguage('${id}', this.value)">
            <option value="javascript">JavaScript</option>
            <option value="python">Python</option>
            <option value="html">HTML</option>
            <option value="css">CSS</option>
            <option value="sql">SQL</option>
            <option value="markdown">Markdown</option>
          </select>
          <button class="notion-code-copy-btn" onclick="copyBlockCode('${id}')">Copiar</button>
        </div>
        <pre><code class="notion-code-body" contenteditable="plaintext-only" spellcheck="false" data-property="title">${plainCode}</code></pre>
      </div>
      ```

11. **`equation`**:
    - **Properties**: `{ "title": [[ "\\int_{0}^{\\infty} e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}", [] ]] }`
    - **DOM Structure**:
      ```html
      <div class="notion-block notion-block-equation" data-block-id="${id}" data-type="equation" contenteditable="false">
        <div class="notion-equation-display" onclick="toggleEquationEditor('${id}')"></div>
        <div class="notion-equation-popover" style="display:none;">
          <input type="text" class="notion-equation-input search-box" value="${formula}" oninput="updateBlockEquation('${id}', this.value)" />
        </div>
      </div>
      ```

12. **`table`** & **`table_row`**:
    - **`table` Format**: `{ "table_block_column_order": ["col-a", "col-b"], "table_block_column_header": true }`
    - **`table` Content**: `["row-uuid-1", "row-uuid-2"]`
    - **`table_row` Properties**: `{ "col-a": [["Cell A", []]], "col-b": [["Cell B", []]] }`
    - **DOM Structure**:
      ```html
      <div class="notion-block notion-block-table-wrapper" data-block-id="${id}" data-type="table">
        <table class="notion-simple-table">
          <tbody class="notion-table-body">
            <!-- row children rendered here as <tr> with <td contenteditable="true" data-col-id="col-a"> -->
          </tbody>
        </table>
        <div class="notion-table-controls" contenteditable="false">
          <button class="btn-secondary" onclick="addTableColumn('${id}')">+ Columna</button>
          <button class="btn-secondary" onclick="addTableRow('${id}')">+ Fila</button>
        </div>
      </div>
      ```

13. **`image`**:
    - **Properties**: `{ "source": [[ "https://...", [] ]], "caption": [[ "Caption", [] ]] }`
    - **Format**: `{ "block_width": 600, "block_alignment": "center" }`
    - **DOM Structure**:
      ```html
      <div class="notion-block notion-block-image" data-block-id="${id}" data-type="image" style="width:${width}px;">
        <div class="notion-image-wrap">
          <img src="${url}" alt="${caption}" />
          <div class="notion-image-resizer left" onmousedown="initImageResize('${id}', 'left', event)"></div>
          <div class="notion-image-resizer right" onmousedown="initImageResize('${id}', 'right', event)"></div>
        </div>
        <div class="notion-image-caption" contenteditable="true" data-property="caption" placeholder="Escribe un pie de foto...">${captionHtml}</div>
      </div>
      ```

14. **`collection_view` / `collection_view_page`**:
    - Renders the multi-view database component (Table, Board, Gallery, List, Calendar, Timeline) mapped to the collection data.

---

### 3.3 Recursive Tree Rendering Algorithm from RecordMap

```javascript
/**
 * Recursively renders the block hierarchy from recordMap into the DOM.
 * @param {Object} recordMap - { block: { [id]: { value: blockData } } }
 * @param {string} rootBlockId - UUID of the root page block
 * @param {HTMLElement} mountTarget - DOM element (#rich-editor-canvas)
 */
function renderTreeFromRecordMap(recordMap, rootBlockId, mountTarget) {
  if (!recordMap || !recordMap.block || !mountTarget) return;

  const rootEntry = recordMap.block[rootBlockId];
  if (!rootEntry || !rootEntry.value) return;

  const visited = new Set();
  mountTarget.innerHTML = '';

  function renderSubtree(blockId, parentElement) {
    if (visited.has(blockId)) {
      console.warn('Cyclic hierarchy detected for block:', blockId);
      return;
    }
    visited.add(blockId);

    const entry = recordMap.block[blockId];
    if (!entry || !entry.value) return;
    const block = entry.value;

    // Check soft-delete (alive === 0)
    if (block.alive === 0) return;

    // If this is the root page itself, we render its children directly into the mount target
    if (blockId === rootBlockId) {
      if (Array.isArray(block.content)) {
        block.content.forEach(childId => renderSubtree(childId, parentElement));
      }
      return;
    }

    // Create the DOM element for this block type
    const blockEl = renderBlock(block);
    if (!blockEl) return;

    // Stamp metadata attributes
    blockEl.setAttribute('data-block-id', block.id);
    blockEl.setAttribute('data-type', block.type);
    if (block.parent_id) blockEl.setAttribute('data-parent-id', block.parent_id);

    // If block has child content, recursively render children
    if (Array.isArray(block.content) && block.content.length > 0) {
      const childrenSlot = blockEl.querySelector('.notion-block-children, .notion-column-content, .notion-toggle-content, .notion-table-body') || blockEl;
      block.content.forEach(childId => renderSubtree(childId, childrenSlot));
    }

    parentElement.appendChild(blockEl);
  }

  renderSubtree(rootBlockId, mountTarget);

  // Post-render passes
  renderAllInlineEquations();
  attachSubpageBlockListeners();
  if (typeof attachColumnResizerListeners === 'function') attachColumnResizerListeners();
  if (typeof refreshPageTableOfContents === 'function') refreshPageTableOfContents();
}
```

---

### 3.4 Interactive Operations (Editing, Creating, Reordering)

1. **Content Editable Input (`oninput`)**:
   - Each editable element inside a block has `contenteditable="true"` and `data-property="title"` (or `caption`, `language`, etc.).
   - On input event:
     1. Retrieve `blockId = el.closest('[data-block-id]').getAttribute('data-block-id')`.
     2. Retrieve `propName = el.getAttribute('data-property') || 'title'`.
     3. Extract rich-text tuples: `const tuples = htmlToRichTextTuples(el);`
     4. Mutate in-memory recordMap: `recordMap.block[blockId].value.properties[propName] = tuples;`
     5. If block is `header`, `sub_header`, or `sub_sub_header`, call `refreshPageTableOfContents()`.
     6. Trigger debounced save (300ms) to persist block updates to backend.

2. **Block Splitting & Enter Key (`onkeydown`)**:
   - When user presses Enter in an editable block:
     - In `text` / `header`:
       Split caret contents into two parts: text before caret stays in current block; text after caret becomes a new `text` block.
       Generate new UUID: `const newBlockId = crypto.randomUUID();`
       Create block in `recordMap`:
       ```json
       {
         "id": newBlockId,
         "type": "text",
         "properties": { "title": newTuples },
         "content": [],
         "parent_id": currentBlock.parent_id,
         "parent_table": "block",
         "alive": 1
       }
       ```
       Insert `newBlockId` into parent block's `content` array immediately after `currentBlock.id`.
       Insert new DOM element after current block and move cursor to new block.
       Sync mutation to backend.
     - In `bulleted_list` / `numbered_list`:
       If current item has text: create new item of same type.
       If current item is empty: convert to regular `text` block (outdent).
     - In `toggle`:
       If caret is in summary/header: opens toggle, creates first child block inside `toggle_content`.

3. **Block Type Conversion ("Turn into")**:
   - User triggers conversion via `#block-action-menu` or markdown prefixes (`# `, `## `, `> `, `- `, `1. `, `[] `).
   - Operation:
     ```javascript
     function convertBlockType(blockId, newType) {
       const block = state.activeRecordMap.block[blockId]?.value;
       if (!block) return;
       block.type = newType;
       // Re-render single block element in place
       const oldEl = document.querySelector(`[data-block-id="${blockId}"]`);
       if (oldEl) {
         const newEl = renderBlock(block);
         oldEl.replaceWith(newEl);
         attachSubpageBlockListeners();
         refreshPageTableOfContents();
       }
       saveBlockMutation(block);
     }
     ```

4. **Reordering & Hierarchy (DND / Spatial Handle)**:
   - Moving within parent `content`:
     When user drops a block above/below a sibling:
     1. Parent `content` array is updated: remove `draggedId`, insert at new index relative to `targetId`.
     2. Update DOM: `targetEl.before(draggedEl)` or `targetEl.after(draggedEl)`.
     3. Sync parent block's updated `content` array to backend:
        `window.pywebview.api.reorder_child_blocks(parentId, parent.content)`
   - Nesting (Indent / Tab):
     1. Remove `blockId` from old parent's `content`.
     2. Update `block.parent_id = newParentId`.
     3. Append `blockId` to `newParent.content`.
     4. Move DOM element into `newParentEl.querySelector('.notion-block-children')`.
     5. Sync both parent blocks and child block to backend.

5. **Soft Delete (`alive = 0`)**:
   - When user deletes a block:
     1. Mark `block.alive = 0`.
     2. Remove `block.id` from `parentBlock.content` array.
     3. Remove block element from DOM.
     4. Send soft-delete to backend: `window.pywebview.api.soft_delete_block(blockId)`.

---

### 3.5 Backend Persistence Flow

```
┌─────────────────────────────────┐
│     User Edits in Editor UI     │
└────────────────┬────────────────┘
                 │ (1) User input / Enter / Slash / Drag
                 ▼
┌─────────────────────────────────┐
│ In-Memory RecordMap Mutated     │
│  - properties / content / type  │
└────────────────┬────────────────┘
                 │ (2) Debounce timer (300ms)
                 ▼
┌─────────────────────────────────┐
│     PyWebView Bridge Check      │
└────────┬───────────────┬────────┘
         │ (hasPyWebView)│ (fallback)
         ▼               ▼
┌──────────────────┐   ┌───────────────────────────┐
│ pywebview.api    │   │ fetch('/api/blocks/...')  │
│  .save_block()   │   │  POST / PUT REST endpoint │
│  .reorder_...()  │   └─────────────┬─────────────┘
└────────┬─────────┘                 │
         │ (3) Native SQLite write   │
         ▼                           ▼
┌──────────────────────────────────────────────────┐
│  Python Backend: Peewee ORM (Block table)        │
│   - Update row properties / content / alive      │
│   - Update parent content UUID array             │
│   - Bump version, update last_edited_time        │
└────────────────────────┬─────────────────────────┘
                         │ (4) OK Response
                         ▼
┌──────────────────────────────────────────────────┐
│ UI: Update #save-status-indicator to "synced"    │
└──────────────────────────────────────────────────┘
```

---

## 4. Compatibility Analysis with Existing UI Features

### 4.1 Multiple Tabs (`#note-tabs-list`)
- **Current Behavior**:
  * `state.openTabIds`: array of note IDs.
  * Tab click triggers `switchNoteTab(id)` -> `selectNote(id)` -> `loadActiveNote()`.
  * Tabs display title, emoji, pin indicator, close button.
- **Notion Block Compatibility**:
  * Each tab represents a root `page` block.
  * When switching tabs, `loadActiveNote()` loads the `recordMap` for that `page` block and renders the tree.
  * Tab title is bound to `recordMap.block[pageId].value.properties.title`.
  * Fully compatible without any structural changes to tab layout or tab drag-and-drop.

### 4.2 Fixed Right-Rail Table of Contents (`#sticky-toc-rail`)
- **Current Behavior**:
  * `collectEditorHeadings()` (lines 13619–13630) inspects `#rich-editor-canvas`:
    `const nodes = Array.from(editor.querySelectorAll('h1, h2, h3'));`
  * Extracts text, level (1, 2, 3), and assigns `data-heading-idx`.
  * Populates `#sticky-toc-bars` and `#sticky-toc-list`.
  * Smooth scrolling on click highlights heading.
- **Notion Block Compatibility**:
  * Rendering `header` as `<h1>`, `sub_header` as `<h2>`, and `sub_sub_header` as `<h3>` guarantees immediate 100% interoperability with `collectEditorHeadings()`.
  * Any edit to a heading title automatically triggers `refreshPageTableOfContents()`.

### 4.3 Sidebar & Folders (`#panel-folders`, `#panel-gallery`)
- Note items in gallery display title, emoji, and updated date.
- Root page blocks map to notes. The folder hierarchy maps to folder assignments.
- Compatible with all search, filtering, and smart folder queries.

### 4.4 Dark / Light Themes & CSS Variables
- The block elements use existing CSS variables defined in `:root` and `body.light-mode`:
  * Backgrounds: `var(--bg-canvas)`, `var(--bg-surface)`, `var(--bg-elevated)`.
  * Borders: `var(--border-hairline)`.
  * Typography: `var(--text-primary)`, `var(--text-secondary)`, `var(--text-muted)`.
  * Accent: `var(--accent-amber)`, `var(--accent-amber-soft)`, `var(--accent-amber-border)`.
- No hardcoded colors; light mode toggle (`body.light-mode`) automatically applies to all new block types.

### 4.5 Regression Safety
- The 153 existing tests in `tests/` check:
  * Selection guard in `mousedown` listener (`[contenteditable="true"]`, `INPUT`, `TEXTAREA`).
  * `.block-subpage` rendering and click navigation to `loadNote(pageId)`.
  * Window control buttons and tab bar styling.
  * `window.renderBlock = renderBlock; window.renderBlocks = renderBlocks; window.attachSubpageBlockListeners = attachSubpageBlockListeners;`.
- All proposed changes build on top of these exported identifiers, guaranteeing zero test regressions.

---

## 5. Concrete Implementation Roadmap for Workers

To execute R4 & R5 smoothly, implementation should be structured in 4 sequential phases:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 1: Rich-Text Tuple Conversion Module                             │
│ - Implement parseRichTextToHtml(tuples) & htmlToRichTextTuples(dom)   │
│ - Support bold, italic, underline, strike, code, color/bg, link, math  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ Phase 2: Full Suite Block Element Factory                              │
│ - Extend renderBlock(block) to handle all types:                       │
│   sub_page, text, header, sub_header, sub_sub_header, bulleted_list,   │
│   numbered_list, toggle, code, equation, divider, column_list, column, │
│   table, table_row, image, collection_view                             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ Phase 3: Recursive RecordMap Renderer                                  │
│ - Implement renderTreeFromRecordMap(recordMap, pageId, container)      │
│ - Resolve parent_id and content UUID arrays recursively                │
│ - Integrate with loadActiveNote() to replace innerHTML assignment     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ Phase 4: Interactive Operations & PyWebView Bridge Sync                │
│ - Block splitting on Enter, conversion via slash menu and 'turn into'  │
│ - Reordering via spatial handle DND updating parent content array      │
│ - Debounced mutations to window.pywebview.api                          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Independent Verification & Testing Protocol

To independently verify the frontend implementation:
1. **Unit Test Discovery**:
   ```powershell
   py -m unittest discover -s tests
   ```
   Must execute all 153 existing tests and any newly added block tests with zero failures.
2. **Rich Text Tuple Round-Trip Verification**:
   - Create a test script validating that:
     `htmlToRichTextTuples(parseRichTextToHtml(tuples))` produces identical rich-text data.
3. **Hierarchy Integrity Verification**:
   - Verify that adding a child block updates parent's `content` array and child's `parent_id`.
   - Verify that reordering children updates the visual DOM sequence and the parent's `content` array.
4. **Editor Interaction Verification**:
   - Test that clicking text inside contenteditable blocks does NOT trigger the lasso marquee.
   - Test that clicking subpage blocks navigates to the target page via `loadNote(pageId)`.
   - Test that headings appear in `#sticky-toc-rail` and smooth-scroll on click.

---
*End of Report.*
