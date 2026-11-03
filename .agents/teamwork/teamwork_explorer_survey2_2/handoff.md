# Handoff Report: Investigation of R2 (Folder Unification & Management) & R3 (Quick Access to Full-Screen Reminders)

## 1. Observation

### 1.1 Folder Creation Buttons in the Interface
We searched the entire codebase for folder creation triggers, buttons, and modal openers:
1. **`frontend/index.html` (Lines 76–81)**:
   ```html
   <button id="btn-new-folder" onclick="promptNewFolder()" class="folder-add-icon-btn" data-shortcut-tooltip="new_folder" title="Añadir carpeta (Alt+Shift+N)" aria-label="Añadir carpeta">
     <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
       <line x1="12" y1="5" x2="12" y2="19"></line>
       <line x1="5" y1="12" x2="19" y2="12"></line>
     </svg>
   </button>
   ```
   *Location*: `aside#panel-folders > div.folder-header-row > div.folder-header-actions`.
   *Action*: Calls `promptNewFolder()`, which calls `openFolderModal('create')`.

2. **`frontend/index.html` (Lines 110–115)**:
   ```html
   <button type="button" class="btn-icon-tiny smart-folder-header-btn" onclick="openSmartFolderModal('create')" title="Nueva Carpeta Inteligente (Filtros dinámicos en tiempo real)" style="font-size:11.5px; line-height:1; padding:2px 5px; display:inline-flex; align-items:center; gap:2px;">
     <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
       <circle cx="12" cy="12" r="3"></circle>
       <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
     </svg>
   </button>
   ```
   *Location*: `aside#panel-folders > div#folders-section-header > div`.
   *Action*: Calls `openSmartFolderModal('create')`.

3. **`frontend/index.html` (Lines 116–117)**:
   ```html
   <button type="button" class="btn-icon-tiny" onclick="openFolderModal('create')" title="Nueva carpeta o subcarpeta" style="font-size:13px; line-height:1; padding:1px 5px;">+</button>
   ```
   *Location*: `aside#panel-folders > div#folders-section-header > div`.
   *Action*: Calls `openFolderModal('create')`.

4. **`frontend/app.js` (Line 2062)**:
   ```javascript
   <span class="folder-add-subfolder-hint" onclick="event.stopPropagation(); openSubfolderModal('${safeJsFolder}');" title="Crear subcarpeta dentro de &quot;${safeHtmlDisplayName}&quot;">+</span>
   ```
   *Location*: In individual folder rows in `#folders-list-container` (contextual inline subfolder button).

5. **`frontend/app.js` (Line 4415)**:
   ```javascript
   <button type="button" class="note-folders-new-btn" onclick="closeNoteFoldersPopover(); openFolderModal('create');">+ Nueva carpeta o subcarpeta...</button>
   ```
   *Location*: In the note's multi-folder assignment popover.

---

### 1.2 Permanent Yellow/Amber Styling on Folder Creation Buttons
We directly inspected CSS styling for folder creation buttons in `frontend/styles.css`:
1. **`frontend/styles.css` (Lines 1254–1267)**:
   ```css
   .folder-add-icon-btn {
     width: 25px;
     height: 25px;
     display: inline-flex;
     align-items: center;
     justify-content: center;
     border: 1px solid var(--accent-amber-border);
     background: var(--accent-amber-soft);
     color: var(--accent-amber);
     border-radius: 7px;
     cursor: pointer;
     padding: 0;
     flex-shrink: 0;
     transition: background 0.15s, color 0.15s, border-color 0.15s, transform 0.12s;
   }
   ```
   *Direct Observation*: In default rest state, `.folder-add-icon-btn` is explicitly styled with `background: var(--accent-amber-soft);`, `border: 1px solid var(--accent-amber-border);`, and `color: var(--accent-amber);`.

2. **`frontend/styles.css` (Lines 9740–9760)**:
   ```css
   .folder-add-icon-btn:not(.sidebar-trash-btn):not([class*="trash"]),
   .sidebar-inline-plus-btn,
   .gallery-search-icon-btn,
   .btn-icon-tiny:not(.btn-danger-tiny):not([class*="trash"]):not([class*="delete"]) {
     background: var(--accent-amber-soft) !important;
     color: var(--accent-amber) !important;
     border: 1px solid var(--accent-amber-border) !important;
     font-weight: 700;
     border-radius: 7px;
     cursor: pointer;
     transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease, transform 0.1s ease, box-shadow 0.15s ease !important;
   }
   ```
   *Direct Observation*: Lines 9749 and 9752 enforce yellow/amber styling on `.folder-add-icon-btn` and `.btn-icon-tiny` with `!important`, making them permanently yellow regardless of any component styling.

---

### 1.3 Folder Modal & Smart Folder Implementation
1. **`frontend/index.html` (Lines 1826–1904)**: Defines `#folder-custom-modal` for standard folders and subfolders. Contains a transition bar at lines 1875–1886 (`#folder-modal-smart-switch-bar`) with a button calling `switchFolderModalToSmart()`.
2. **`frontend/index.html` (Lines 1907–1988)**: Defines `#smart-folder-modal` for creating smart folders with dynamic rules (tags, dates, tasks, logic AND/OR, live preview).
3. **`frontend/app.js` (Lines 7166–7255)**: `openFolderModal(mode, folderName, presetParentFolder)` populates `#folder-parent-select` and manages standard folder creation.
4. **`frontend/app.js` (Lines 7657–7670)**: `switchFolderModalToSmart()` closes `#folder-custom-modal` and opens `#smart-folder-modal`.
5. **`frontend/app.js` (Lines 7672–7725)**: `openSmartFolderModal(mode, folderName, presetName, presetEmoji)` initializes smart folder rules.
6. **`frontend/app.js` (Lines 7396–7485)**: `submitFolderModal()` submits standard folder data to `/api/folders`.
7. **`frontend/app.js` (Lines 7935–8032)**: `submitSmartFolderModal()` saves smart folder configuration to `state.smartFolders` and `/api/smart-folders/save`.
8. **`models.py` (Lines 134–162)**: `Folder` model in SQLite ORM already contains `name`, `parent_name`, `emoji`, `sort_order`, `is_smart`, and `smart_rules_json`.
9. **`backend.py` (Lines 405–415)**: Endpoints `/api/smart-folders/save` and `/api/folders` are already fully implemented.

---

### 1.4 Sidebar Tray Structure & Existing Reminders Engine
1. **`frontend/index.html` (Lines 86–105)**:
   ```html
   <div class="sidebar-notion-quick-nav">
     <button type="button" class="folder-item sidebar-quick-action-btn" onclick="openQuickFindModal()" title="Buscar o ir a una página (Ctrl+K)">...</button>
     <button type="button" class="folder-item sidebar-quick-action-btn" id="fitem-sidebar-home" onclick="navigateToHome()" title="Ir a la página de inicio (Alt+H)">...</button>
   </div>
   ```
2. **`frontend/app.js` (Lines 352–359, 404, 950–992)**:
   - Reminders are loaded into `state.reminders`.
   - Persisted in localStorage (`notejs_calendar_reminders_v1`) and synced via `/api/reminders` and `/api/reminders/sync`.
   - Backend ORM model `ReminderItem` (`models.py` line 274) and endpoints (`backend.py` line 501) are already functional.
3. **`frontend/app.js` (Lines 12015–12078)**:
   `navigateToHome()` sets `state.isHomeActive = true`, applies `.is-home-active` class to `#desktop-scaffold`, hides `.desktop-format-bar`, `#notion-cover`, and `#editor-body`, and displays `#home-page-view`.
4. **`frontend/styles.css` (Lines 7254–7263)**:
   ```css
   .desktop-main-scaffold.is-home-active #panel-gallery,
   .desktop-main-scaffold.is-home-active #splitter-gallery-editor {
     display: none !important;
   }
   .desktop-main-scaffold.is-home-active #panel-canvas {
     flex: 1 1 auto;
     width: 100%;
   }
   ```
   When Home is active, the notes gallery panel is hidden, and `#panel-canvas` expands to take up 100% of the main content space beside the folders sidebar.

---

## 2. Logic Chain

### 2.1 Duplication Elimination Reasoning (R2)
- **Premise 1**: In `panel-folders`, there are two separate buttons that create a standard folder:
  1. `#btn-new-folder` at line 76 in `folder-header-row` (`promptNewFolder()`).
  2. The `+` button at line 116 in `folders-section-header` (`openFolderModal('create')`).
- **Premise 2**: In `folders-section-header`, there is an additional button: the gear icon button at line 110 (`openSmartFolderModal('create')`), which creates an artificial separation between regular folder creation and smart folder creation.
- **Deduction**:
  - The interface contains 3 folder creation buttons in the same left panel within 40 pixels of each other.
  - Requirement R2 mandates:
    1. Eliminate duplicate folder creation buttons.
    2. Unify "crear carpeta" and "crear carpeta inteligente" into a single button and single dialog/form where smart folder is a toggleable option.
  - **Resolution**:
    - Remove the duplicate button. Keep `#btn-new-folder` as the primary folder creation button in the panel.
    - Remove the separate `smart-folder-header-btn` from `folders-section-header`.
    - Remove the redundant `+` button from `folders-section-header` (or designate `#btn-new-folder` at the section header and remove it from `folder-header-row`).
    - The remaining single button triggers the unified folder creation flow.

### 2.2 Styling Rectification Reasoning (R2)
- **Premise**: `ORIGINAL_REQUEST.md` states:
  *"Los botones de crear carpeta no deben ser amarillos de forma permanente; solo deben mostrar color amarillo al hacer hover o al pulsarlos."*
- **Premise**: In `frontend/styles.css`, `.folder-add-icon-btn` is styled with permanent yellow/amber backgrounds and borders both in its base rule (lines 1260–1262) and in the forced rule with `!important` (line 9749, line 9752 for `.btn-icon-tiny`).
- **Deduction**:
  - In default rest state, folder creation buttons must display a neutral theme color matching the surface (transparent or `var(--bg-surface)` background, hairline or transparent border, and `var(--text-secondary)` color).
  - Amber highlighting (`var(--accent-amber)`) must only be applied on `:hover` and `:active`.
  - Lines 9749 and 9752 must be adjusted to exclude folder creation buttons from the permanent amber background.

### 2.3 Unification of Folder Creation Flow (R2)
- **Premise**: Currently, standard folders and smart folders exist in two separate modals (`#folder-custom-modal` and `#smart-folder-modal`) with two separate handlers (`submitFolderModal` and `submitSmartFolderModal`).
- **Premise**: Requirement R2 requires merging them into a single action and dialog/form where smart folder is a selectable/toggleable option.
- **Deduction**:
  - Add a toggle control (e.g. Segmented Pill or Radio Toggle) at the top of `#folder-custom-modal`:
    `[ 📁 Carpeta Estándar ]   [ ⚙️ Carpeta Inteligente ]`
  - When **Carpeta Estándar** is selected:
    - Display the parent folder select group (`#folder-parent-select-group`).
    - Hide the smart rules builder.
    - Submit button: `+ Crear carpeta`.
  - When **Carpeta Inteligente** is selected:
    - Hide the parent folder select group (since smart folders in Note-JS/Apple Notes are always root-level dynamic queries).
    - Display the smart rules builder (match mode AND/OR, dynamic rule rows, live matching notes preview).
    - Default emoji becomes `⚙️`.
    - Submit button: `⚙️ Guardar Carpeta Inteligente`.
  - Submission handler: Inside `submitFolderModal()`, evaluate the selected type. If smart, execute the smart folder validation and persistence to SQLite; if standard, execute the standard folder persistence.

### 2.4 Quick Access to Full-Screen Reminders View (R3)
- **Premise**: Requirement R3 requires:
  1. A visible quick-access button/item in the folder tray/sidebar to open reminders.
  2. Replacing the main content area (canvas/editor) with a full-screen dedicated reminders view.
- **Premise**: The folder tray (`aside#panel-folders`) already features `sidebar-notion-quick-nav` (lines 86–105) holding quick-access buttons for "Buscar" (`openQuickFindModal()`) and "Inicio" (`navigateToHome()`).
- **Premise**: The main content area (`main#panel-canvas`) already hosts `#home-page-view` which replaces the editor when `.desktop-main-scaffold.is-home-active` is applied.
- **Deduction**:
  - Add `#fitem-sidebar-reminders` in `sidebar-notion-quick-nav` with calendar/bell icon and a badge displaying the count of uncompleted reminders.
  - Add `#reminders-page-view` directly in `main#panel-canvas` alongside `#home-page-view`.
  - Implement `navigateToReminders()`:
    - Sets `state.isRemindersActive = true`, `state.isHomeActive = false`.
    - Applies `.is-reminders-active` to `#desktop-scaffold` (hiding `#panel-gallery` and `#splitter-gallery-editor`, expanding `#panel-canvas` to 100%).
    - Hides the format bar, cover, and editor body; displays `#reminders-page-view`.
    - Highlights `#fitem-sidebar-reminders` as `.active`.
    - Invokes `renderRemindersPageView()` to render the full-screen view (interactive calendar, filtered reminder cards, category chips, checkboxes, "+ Nuevo recordatorio" action).
  - Implement `exitRemindersView()`: Invoked upon navigating to a note or home, cleaning up the active state.

---

## 3. Caveats
1. **No Backend Model Changes Needed**: Both `models.py` (`Folder`, `ReminderItem`) and `backend.py` (`/api/folders`, `/api/smart-folders/save`, `/api/reminders`, `/api/reminders/sync`) already fully support all required data attributes. No schema migrations or backend modifications are required.
2. **Keyboard Shortcuts**: `Alt+Shift+N` (id: `new_folder`) in `frontend/app.js:9883` currently calls `promptNewFolder()`. Merging the modal preserves this shortcut without any disruption. We also recommend assigning `Alt+R` as a shortcut for `navigateToReminders()`.
3. **Subfolder inline hints**: The inline `+` hint (`.folder-add-subfolder-hint`) appearing on folder hover is not a top-level folder creation button, but a subfolder shortcut. It already has neutral styling (hidden until hover, amber only on button hover).
4. **Production write restriction**: In accordance with the teamwork explorer instructions, no production source code has been modified during this investigation.

---

## 4. Conclusion & Recommendations

### 4.1 Summary of Changes Needed
| Requirement | Action | Target Files |
|-------------|--------|--------------|
| **R2: Eliminate duplicate buttons** | Remove duplicate folder creation button and separate smart folder button in sidebar. Keep one single unified button. | `frontend/index.html` (lines 76-81, 107-118) |
| **R2: Folder button styling** | Change `.folder-add-icon-btn` default styling to neutral background/border; remove from lines 9749 & 9752; apply amber only on `:hover` and `:active`. | `frontend/styles.css` (lines 1254-1276, 9749, 9752) |
| **R2: Unified folder creation modal** | Integrate standard folder modal and smart folder modal into a single modal with a segmented type selector (`[📁 Estándar | ⚙️ Inteligente]`). | `frontend/index.html` (lines 1826-1988), `frontend/app.js` (lines 7166-7255, 7396-7485, 7657-7725) |
| **R3: Reminders quick-access in tray** | Add `#fitem-sidebar-reminders` inside `.sidebar-notion-quick-nav` with calendar icon and count badge; toggle `.active` state. | `frontend/index.html` (lines 86-105), `frontend/app.js` (lines 1957-2000) |
| **R3: Full-screen reminders view** | Add `#reminders-page-view` inside `#panel-canvas`; add `.is-reminders-active` CSS; implement `navigateToReminders()` & `renderRemindersPageView()`. | `frontend/index.html` (lines 255-258), `frontend/styles.css` (lines 7254-7264), `frontend/app.js` (lines 12015-12080) |

---

## 5. File Touches & Concrete Implementation Blueprint

### File 1: `frontend/index.html`

#### Change A: Sidebar Header & Folders Section Header (Eliminating Duplicate Buttons)
In `aside#panel-folders`:
- In `folder-header-row` (line 76): keep `#btn-new-folder` as the primary folder creation button with title `"Nueva carpeta (Alt+Shift+N)"`.
- In `folders-section-header` (lines 107–118): remove `smart-folder-header-btn` and the duplicate `+` button.
```html
<!-- BEFORE (lines 107-118): -->
<div id="folders-section-header" class="folder-section-title" style="margin-top:10px; display:flex; align-items:center; justify-content:space-between; padding-right:8px;" title="Arrastra una subcarpeta aquí para convertirla en carpeta principal">
  <span>CARPETAS</span>
  <div style="display:inline-flex; align-items:center; gap:3px;">
    <button type="button" class="btn-icon-tiny smart-folder-header-btn" onclick="openSmartFolderModal('create')" title="Nueva Carpeta Inteligente (Filtros dinámicos en tiempo real)" style="font-size:11.5px; line-height:1; padding:2px 5px; display:inline-flex; align-items:center; gap:2px;">
      <svg ...></svg>
    </button>
    <button type="button" class="btn-icon-tiny" onclick="openFolderModal('create')" title="Nueva carpeta o subcarpeta" style="font-size:13px; line-height:1; padding:1px 5px;">+</button>
  </div>
</div>

<!-- AFTER: -->
<div id="folders-section-header" class="folder-section-title" style="margin-top:10px; display:flex; align-items:center; justify-content:space-between; padding-right:8px;" title="Arrastra una subcarpeta aquí para convertirla en carpeta principal">
  <span>CARPETAS</span>
</div>
```

#### Change B: Quick Access Item in Folder Tray (`sidebar-notion-quick-nav`)
In lines 86–105:
```html
<!-- AFTER (appended after fitem-sidebar-home): -->
<button type="button" class="folder-item sidebar-quick-action-btn" id="fitem-sidebar-reminders" onclick="navigateToReminders()" title="Ver recordatorios a pantalla completa (Alt+R)">
  <span class="folder-item-left">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0; opacity:0.8;">
      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
      <line x1="16" y1="2" x2="16" y2="6"></line>
      <line x1="8" y1="2" x2="8" y2="6"></line>
      <line x1="3" y1="10" x2="21" y2="10"></line>
    </svg>
    <span>Recordatorios</span>
  </span>
  <span class="folder-item-right">
    <span id="sidebar-reminders-count-badge" class="folder-count">0</span>
  </span>
</button>
```

#### Change C: Full-Screen Reminders View Container
In `<main id="panel-canvas" class="panel-canvas">` (line 257):
```html
<!-- AFTER: -->
<div id="home-page-view" class="home-page-view" style="display:none;"></div>
<div id="reminders-page-view" class="reminders-page-view" style="display:none;"></div>
```

#### Change D: Unified Folder Creation Modal (`#folder-custom-modal`)
At lines 1850–1875 of `frontend/index.html`:
Replace `#folder-modal-smart-switch-bar` with a segmented selector right above or below the name input:
```html
<!-- Selector de Tipo de Carpeta: Estándar vs Inteligente -->
<div class="folder-type-segmented-wrap" style="margin-bottom:12px;">
  <div class="folder-type-segmented-control" role="radiogroup" aria-label="Tipo de Carpeta">
    <button type="button" id="ftype-btn-standard" class="folder-type-seg-btn active" onclick="setFolderModalType('standard')">
      📁 Carpeta Estándar
    </button>
    <button type="button" id="ftype-btn-smart" class="folder-type-seg-btn" onclick="setFolderModalType('smart')">
      ⚙️ Carpeta Inteligente (Filtro Dinámico)
    </button>
  </div>
</div>
```
And embed the smart rules container directly inside `#folder-custom-modal` (conditionally displayed when `smart` is selected):
```html
<div id="folder-smart-rules-container" style="display:none;">
  <!-- Selector AND/OR, Lista de reglas con + Añadir filtro, y Live Preview Box -->
</div>
```

---

### File 2: `frontend/styles.css`

#### Change A: Fix Folder Button Permanent Yellow Background/Border
Lines 1254–1276:
```css
/* BEFORE: */
.folder-add-icon-btn {
  width: 25px;
  height: 25px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--accent-amber-border);
  background: var(--accent-amber-soft);
  color: var(--accent-amber);
  border-radius: 7px;
  cursor: pointer;
  padding: 0;
  flex-shrink: 0;
  transition: background 0.15s, color 0.15s, border-color 0.15s, transform 0.12s;
}

/* AFTER: */
.folder-add-icon-btn {
  width: 25px;
  height: 25px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-secondary);
  border-radius: 7px;
  cursor: pointer;
  padding: 0;
  flex-shrink: 0;
  transition: background 0.15s, color 0.15s, border-color 0.15s, transform 0.12s;
}
.folder-add-icon-btn:hover {
  background: var(--accent-amber);
  color: #121316;
  border-color: var(--accent-amber);
}
.folder-add-icon-btn:active {
  transform: scale(0.95);
  background: var(--accent-amber);
  color: #121316;
}
```

#### Change B: Remove Forced Amber Rules
In lines 9740–9760:
Remove `.folder-add-icon-btn:not(.sidebar-trash-btn):not([class*="trash"])` and `.btn-icon-tiny:not(...)` from the forced amber block so they are NOT permanently yellow.

#### Change C: Layout & Full-Screen Reminders View Styles
Around line 7260:
```css
/* Soporte de pantalla completa para Recordatorios */
.desktop-main-scaffold.is-reminders-active #panel-gallery,
.desktop-main-scaffold.is-reminders-active #splitter-gallery-editor {
  display: none !important;
}
.desktop-main-scaffold.is-reminders-active #panel-canvas {
  flex: 1 1 auto;
  width: 100%;
}
.reminders-page-view {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  height: 100%;
  overflow-y: auto;
  padding: 24px 32px;
  background: var(--bg-canvas);
  color: var(--text-primary);
}
```

#### Change D: Segmented Type Selector for Unified Folder Modal
```css
.folder-type-segmented-control {
  display: flex;
  background: var(--bg-surface);
  border: 1px solid var(--border-hairline);
  border-radius: 8px;
  padding: 3px;
  gap: 4px;
}
.folder-type-seg-btn {
  flex: 1;
  padding: 6px 12px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}
.folder-type-seg-btn.active {
  background: var(--accent-amber);
  color: #090a0d;
}
```

---

### File 3: `frontend/app.js`

#### Change A: Sidebar Rendering (`renderFolders`)
Update `renderFolders()` to toggle active state on `#fitem-sidebar-reminders` and refresh `#sidebar-reminders-count-badge`:
```javascript
const remindersBtn = document.getElementById('fitem-sidebar-reminders');
const remindersBadge = document.getElementById('sidebar-reminders-count-badge');
if (remindersBtn) {
  remindersBtn.classList.toggle('active', Boolean(state.isRemindersActive));
}
if (remindersBadge) {
  const pendingCount = (state.reminders || []).filter(r => !r.completed).length;
  remindersBadge.textContent = String(pendingCount);
}
```

#### Change B: Full-Screen Reminders Navigation (`navigateToReminders`, `exitRemindersView`)
```javascript
function navigateToReminders() {
  state.isRemindersActive = true;
  state.isHomeActive = false;

  const scaffold = document.getElementById('desktop-scaffold');
  if (scaffold) {
    scaffold.classList.remove('is-home-active');
    scaffold.classList.add('is-reminders-active');
  }

  const homeBtn = document.getElementById('btn-top-home');
  if (homeBtn) {
    homeBtn.classList.remove('active');
    homeBtn.setAttribute('aria-pressed', 'false');
  }

  const remindersView = document.getElementById('reminders-page-view');
  const homeView = document.getElementById('home-page-view');
  const formatBar = document.querySelector('.desktop-format-bar');
  const notionCover = document.getElementById('notion-cover');
  const editorBody = document.getElementById('editor-body');

  if (remindersView) remindersView.style.display = 'flex';
  if (homeView) homeView.style.display = 'none';
  if (formatBar) formatBar.style.display = 'none';
  if (notionCover) notionCover.style.display = 'none';
  if (editorBody) editorBody.style.display = 'none';

  renderFolders();
  renderNoteTabs();
  renderRemindersPageView();
}

function exitRemindersView() {
  if (!state.isRemindersActive) return;
  state.isRemindersActive = false;

  const scaffold = document.getElementById('desktop-scaffold');
  if (scaffold) {
    scaffold.classList.remove('is-reminders-active');
  }

  const remindersView = document.getElementById('reminders-page-view');
  if (remindersView) remindersView.style.display = 'none';

  renderFolders();
}
```
In `loadNote()` and `navigateToHome()`, call `exitRemindersView()`.

#### Change C: Unified Modal State & Submission
In `folderModalState`:
Add `folderType: 'standard'` (`'standard'` | `'smart'`).
Implement `setFolderModalType(type)`:
- Sets `folderModalState.folderType = type`.
- Toggles active class on `#ftype-btn-standard` and `#ftype-btn-smart`.
- Shows/hides `#folder-parent-select-group` vs `#folder-smart-rules-container`.
- Switches default emoji between `📁` and `⚙️`.
- Updates submit button text.
In `submitFolderModal()`:
If `folderModalState.folderType === 'smart'`, run the smart folder rules validation, save to `state.smartFolders`, and persist to SQLite via `/api/smart-folders/save`. Otherwise, run the standard folder logic.

---

## 6. Verification Method

To independently verify these findings:

1. **Button Duplication Verification**:
   - Inspect `frontend/index.html` lines 76–81 and lines 107–118.
   - Confirm that line 76 (`#btn-new-folder`) and line 116 (`+` in section header) both invoke `openFolderModal('create')`.
   - Confirm line 110 (`smart-folder-header-btn`) opens `openSmartFolderModal('create')`.

2. **Styling Verification**:
   - Inspect `frontend/styles.css` lines 1260–1262 and lines 9749, 9752.
   - Confirm `.folder-add-icon-btn` has `background: var(--accent-amber-soft); border: 1px solid var(--accent-amber-border);` in its base rule and is forced amber via `!important` at line 9749.

3. **Backend Readiness Verification**:
   - Inspect `models.py` line 134 (`class Folder`) and line 274 (`class ReminderItem`).
   - Run Python test suite:
     ```powershell
     python -m unittest discover -s tests -v
     ```
   - Verify all existing backend subpage, persistence, and ORM tests pass cleanly.

4. **Reminders Structure Verification**:
   - Inspect `frontend/app.js` lines 352, 950–992, and 12310–12790 to verify `state.reminders`, `toggleHomeReminder`, `deleteHomeReminder`, and `openNewEventModal`.
   - Inspect `backend.py` lines 501–545 to confirm existing `/api/reminders` endpoints.
