# Handoff Report: R4 (Formatting Bar & Focus Mode Clean-up) & Test Infrastructure

**Agent**: Survey Explorer 3 (`teamwork_explorer_survey_3`)  
**Parent Conversation ID**: `45d1cd46-bf0a-48bd-82de-759226538c42`  
**Date**: 2026-10-30T20:25:00Z  
**Scope**: Requirement R4 (Visual formatting bar styling & Focus mode indicator removal) and Test Infrastructure  

---

## 1. Observation

### 1.1 `.desktop-format-bar` in HTML, JS, and CSS

#### HTML (`frontend/index.html`)
- **Lines 263–658**: The `.desktop-format-bar` container wraps the entire macOS-styled editor formatting toolbar:
  - **Lines 264–545**: `.format-btn-group` (left group):
    - **Lines 270–274**: `<button id="btn-reopen-panels" class="format-bar-btn reopen-panels-btn" onclick="handleReopenPanelsClick()" title="Mostrar paneles laterales" style="display:none;" aria-label="Mostrar paneles laterales">`
    - **Lines 277–284**: 
      ```html
      <div style="position:relative; display:inline-block;">
        <button id="btn-insert-dropdown" class="format-bar-btn insert-dropdown-btn" onmousedown="event.preventDefault()" onclick="toggleInsertDropdown(event)" style="border:1px solid var(--accent-amber-border); color:var(--accent-amber); display:inline-flex; align-items:center; gap:5px; height:28px; padding:0 10px;" title="Insertar bloques, columnas, imágenes, fórmulas y herramientas (Ctrl+Shift+I)">
          <span class="insert-plus-sign" style="display:inline-flex; align-items:center; justify-content:center; font-size:15px; font-weight:700; line-height:1; transform:translateY(-0.5px);" aria-hidden="true">+</span>
          <span style="line-height:1; font-weight:600;">Insertar</span>
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.8; margin-left:1px;">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
      ```
    - **Lines 285–527**: `<div id="insert-blocks-dropdown" class="blocks-dropdown-menu">` (48 block insertion menu options).
    - **Line 530**: `<div class="format-bar-divider"></div>`
    - **Lines 533–544**: Formatting action buttons:
      - Line 533: `<button class="format-bar-btn" onmousedown="event.preventDefault()" onclick="formatDoc('formatBlock', '<h1>')" title="Encabezado Principal (H1)"><span style="font-weight:800; font-size:13.5px;">H1</span></button>`
      - Line 536: `<button class="format-bar-btn" onmousedown="event.preventDefault()" onclick="formatDoc('bold')" data-shortcut-tooltip="format_bold" title="Negrita (Ctrl+B)"><strong style="font-size:14px;">B</strong></button>`
      - Line 539: `<button class="format-bar-btn" onmousedown="event.preventDefault()" onclick="formatDoc('italic')" data-shortcut-tooltip="format_italic" title="Cursiva (Ctrl+I)"><em style="font-size:14px; font-style:italic;">I</em></button>`
      - Line 542: `<button class="format-bar-btn" onmousedown="event.preventDefault()" onclick="formatDoc('underline')" data-shortcut-tooltip="format_underline" title="Subrayado (Ctrl+U)"><u style="font-size:14px;">U</u></button>`
  - **Lines 547–657**: Right group (`display:flex; align-items:center; gap:6px; position:relative;`):
    - **Lines 549–555**: `<button id="btn-in-note-search" class="btn-secondary in-note-find-trigger" style="padding:4px 9px; font-size:11.5px; gap:5px;" onclick="toggleInNoteSearch()" title="Buscar texto en esta nota (F3 / Ctrl+F)" aria-label="Buscar en la nota">`
    - **Lines 558–566**: `<div id="save-status-indicator" class="save-file-indicator synced" title="Guardado en SQLite (notejs.db)">`
    - **Lines 569–574**: `<button class="btn-secondary format-bar-action-icon-btn" onclick="togglePinActiveNote()" id="btn-pin-note" data-shortcut-tooltip="pin_note" title="Fijar / Desfijar nota (Ctrl+Shift+P)" aria-label="Fijar nota">`
    - **Lines 577–584**: `<button class="btn-secondary format-bar-action-icon-btn btn-trash-action" style="color:var(--danger); border-color:var(--danger-soft);" onclick="deleteActiveNote()" data-shortcut-tooltip="delete_note" title="Enviar a la papelera (Ctrl+Shift+Backspace)" aria-label="Enviar a la papelera">`
    - **Lines 588–595**: `<button id="btn-page-appearance" class="btn-secondary page-dots-btn" onclick="togglePageAppearancePopover(event)" title="Opciones de página (•••)" aria-label="Opciones de página">`
    - **Lines 596–655**: `<div id="page-appearance-popover" class="page-appearance-popover" role="dialog" aria-label="Opciones de página">`

#### CSS (`frontend/styles.css`)
- **Lines 1781–1794**: Base definition:
  ```css
  .desktop-format-bar {
    height: 48px;
    border-bottom: 1px solid var(--border-hairline);
    background: var(--bg-surface);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 14px;
    gap: 8px;
    flex-shrink: 0;
    position: relative;
    overflow: visible;
    z-index: 90;
  }
  ```
- **Lines 1802–1830**: Button styling rule that currently forces ALL format buttons to amber:
  ```css
  .format-bar-btn:not(.btn-trash-action) {
    height: 31px;
    padding: 0 8px;
    background: var(--accent-amber-soft);
    border: 1px solid var(--accent-amber-border);
    border-radius: 6px;
    color: var(--accent-amber);
    font-family: inherit;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;
    transition: background 0.12s, color 0.12s, border-color 0.12s;
  }
  .format-bar-btn:not(.btn-trash-action):hover {
    background: var(--accent-amber);
    color: #090a0d;
    border-color: var(--accent-amber);
  }
  .format-bar-btn:not(.btn-trash-action).active {
    background: var(--accent-amber);
    color: #090a0d;
    border-color: var(--accent-amber);
  }
    border-color: var(--accent-amber-border);
  }
  ```
  *(Note the orphaned `border-color: var(--accent-amber-border); }` at line 1829)*.
- **Lines 454–478**: `.btn-secondary` sets amber styles with `!important`:
  `background: var(--accent-amber-soft) !important; color: var(--accent-amber) !important; border: 1px solid var(--accent-amber-border) !important;`
- **Lines 9685–9689**: Amber unification block includes toolbar buttons with `!important`:
  `#btn-in-note-search, #btn-pin-note, #btn-page-appearance, #btn-reopen-panels, #btn-insert-dropdown`
- **Lines 9715–9719**: Amber hover unification block includes:
  `#btn-in-note-search:hover, #btn-pin-note:hover, #btn-page-appearance:hover, #btn-reopen-panels:hover, #btn-insert-dropdown:hover`
- **Line 9738**: Amber active block includes:
  `.format-bar-btn:not(.btn-trash-action):not([class*="trash"]):not([class*="delete"]).active`

#### JavaScript (`frontend/app.js`)
- **Lines 11878 & 11907**: Toggles format bar display on/off when opening/closing Google Chrome-styled Home view.
- **Line 15255**: Marquee selection handler ignores clicks on `.desktop-format-bar`.
- **Lines 8387, 8402, 8407, 8409, 10229, 10233**: `#btn-insert-dropdown` toggles `.active` class when open.
- **Lines 4096–4104**: In `loadActiveNote()`, inline style injection turns `#btn-pin-note` amber when `note.isPinned`:
  ```javascript
  if (note.isPinned) {
    pinBtn.style.borderColor = 'var(--accent-amber)';
    pinBtn.style.color = 'var(--accent-amber)';
    pinBtn.style.background = 'var(--accent-amber-soft)';
  } else {
    pinBtn.style.borderColor = 'var(--border-hairline)';
    pinBtn.style.color = 'var(--text-secondary)';
    pinBtn.style.background = 'var(--bg-elevated)';
  }
  ```

---

### 1.2 `#focus-mode-indicator` and "Modo concentración"

#### HTML (`frontend/index.html`)
- **Lines 48–50**:
  ```html
  <span id="focus-mode-indicator" style="display:none; color:var(--accent-amber); font-size:12px; font-weight:700; white-space:nowrap;">
    ⚡ Modo Concentración Activo (Presiona ☰ o Ctrl+\ para salir)
  </span>
  ```

#### JavaScript (`frontend/app.js`)
- **Line 1324**: `const indicator = document.getElementById('focus-mode-indicator');` in `checkFocusModeStateSync()`.
- **Line 1338**: `if (indicator) indicator.style.display = bothCollapsed ? 'inline-block' : 'none';`
- **Lines 10046–10051**: In `refreshAllShortcutTooltipsAndBadges()`:
  ```javascript
  // Actualizar indicador de modo concentración
  const focusInd = document.getElementById('focus-mode-indicator');
  if (focusInd) {
    focusInd.textContent = `⚡ Modo Concentración Activo (Presiona ☰ o ${getShortcutDisplayCombo('toggle_focus')} para salir)`;
  }
  ```

#### CSS (`frontend/styles.css`)
- No CSS rules exist targeting `#focus-mode-indicator` (it used inline style).
- Comments at lines 489, 507, 552 refer to "Modo Concentración" as a general feature concept.
- Line 502 targets `body.is-focus-mode .focus-sidebar-edge-sensor` for the side peek edge sensor.

---

### 1.3 Project Test Infrastructure

1. **System & Executables**:
   - `python`: Direct call fails in Windows PowerShell due to Microsoft Store alias.
   - `py`: Succeeds and points to Python 3.15.2 (`C:\Users\Joaco\AppData\Local\Python\bin\python.exe`).
   - `py -m pytest`: Returns `No module named pytest` (code 1).
   - `node` / `npm`: Not installed or not in PATH (`CommandNotFoundException`).
   - `py -m unittest`: Fully installed and functional (standard library).
2. **Current Test Files**:
   - `firestore.test.js` is the only existing test file in the repository (designed for Firebase emulator with `node:test`, not runnable without node).
   - There are currently NO automated unit tests for backend Python or frontend JavaScript.
3. **Compilation**:
   - `py -m py_compile models.py backend.py desktop_app.py` compiles with exit code 0.
   - `models.py` and `backend.py` import cleanly without runtime errors.

---

## 2. Logic Chain

1. **R4 Formatting Bar Analysis**:
   - Requirement: *Only* `#btn-insert-dropdown` (`.insert-dropdown-btn`) must be yellow/amber; all other buttons must have the canvas/bar background color with neutral hover and active states.
   - Cause of unwanted amber color:
     1. `.format-bar-btn:not(.btn-trash-action)` (lines 1802–1828) defines all buttons with class `.format-bar-btn` (H1, B, I, U, `#btn-reopen-panels`) as `background: var(--accent-amber-soft)` and `color: var(--accent-amber)`.
     2. Global amber unification section (lines 9685–9745) explicitly includes `#btn-in-note-search`, `#btn-pin-note`, `#btn-page-appearance`, `#btn-reopen-panels` and `.btn-secondary` with `!important`.
     3. Active state rule in line 9738 turns active format bar buttons amber with `!important`.
     4. `app.js` lines 4096–4104 injects inline amber styles onto `#btn-pin-note` when pinned.
   - Resolution:
     - Neutralize `.format-bar-btn` default in lines 1802–1828: `background: transparent; border: 1px solid transparent; color: var(--text-secondary);`.
     - Hover/Active states: `background: var(--bg-elevated); color: var(--text-primary); border-color: var(--border-hairline);`.
     - Explicitly define amber styling exclusively for `#btn-insert-dropdown` / `.insert-dropdown-btn`:
       `background: var(--accent-amber-soft) !important; border: 1px solid var(--accent-amber-border) !important; color: var(--accent-amber) !important;`.
     - Exclude `#btn-in-note-search`, `#btn-pin-note`, `#btn-page-appearance`, `#btn-reopen-panels` from lines 9685–9688 and 9715–9718 in `styles.css`.
     - Exclude `.format-bar-btn` from line 9738 active amber styling.
     - Add scoped rule `.desktop-format-bar .btn-secondary:not(.btn-trash-action)` to keep toolbar secondary buttons neutral and prevent them from inheriting the global amber `.btn-secondary` style.
     - In `app.js` (lines 4096–4104), make `#btn-pin-note` active styling neutral (`var(--bg-elevated)`, `var(--text-primary)`, `var(--border-hairline)`).

2. **R4 Focus Mode Indicator Removal**:
   - Requirement: Completely remove the `#focus-mode-indicator` element and its "Modo concentración" text from DOM and styles.
   - Resolution:
     - Remove lines 48–50 from `frontend/index.html`.
     - In `frontend/app.js`, remove references at lines 1324, 1338, and lines 10046–10051.
     - Verify no lingering styles or DOM references remain.

3. **Test Infrastructure Strategy**:
   - Since `py -m unittest` is natively available without dependencies, the team can create a dedicated `tests/` directory with test suites:
     - `tests/test_backend_subpage.py`: Tests Peewee ORM SQLite model serialization, block retrieval, and REST endpoints for `sub_page` blocks (Requirement R2).
     - `tests/test_dom_and_styles_r4.py`: Tests DOM elements, CSS rules, and JS references for `#focus-mode-indicator` removal and formatting bar styling (Requirement R4).
     - `tests/test_frontend_code_guards.py`: Verifies mousedown guard clause for R1 and subpage rendering DOM logic for R3.
   - Commands to execute tests: `py -m unittest discover -s tests -p "test_*.py"`.

---

## 3. Caveats

1. **Pytest & Node Availability**: Neither `pytest` nor `node` is available in PATH. Any test suite developed by the team must use Python's built-in `unittest` runner executed via `py -m unittest` to ensure 100% reproducible execution in this environment.
2. **Global `.btn-secondary` Impact**: `.btn-secondary` is globally styled amber in `styles.css` (lines 454–478 and 9673). Because `#btn-in-note-search`, `#btn-pin-note`, and `#btn-page-appearance` use `.btn-secondary`, specific scoped rules targeting `.desktop-format-bar .btn-secondary:not(.btn-trash-action)` must be used to ensure toolbar buttons remain neutral without unintentionally altering modal dialog buttons elsewhere in the app.
3. **Trash Action Button**: The trash button in `.desktop-format-bar` (`.btn-trash-action`) is explicitly danger-red and must remain red/transparent, never receiving amber or plain text colors.

---

## 4. Conclusion

- **Requirement R4 is clearly defined and localized**:
  1. `frontend/index.html`: Delete lines 48–50 (`#focus-mode-indicator`).
  2. `frontend/app.js`: Remove lines 1324, 1338, and 10046–10051 (indicator lookup and text update); update lines 4096–4104 so `#btn-pin-note` does not set amber inline styles.
  3. `frontend/styles.css`: Fix lines 1802–1830 to neutralize `.format-bar-btn` and eliminate syntax error at line 1829; remove format bar buttons from lines 9685–9688 and 9715–9718; remove `.format-bar-btn` from line 9738; add scoped `.desktop-format-bar` rules ensuring only `#btn-insert-dropdown` is amber.
- **Test Infrastructure is ready**:
  - Python standard library `unittest` via `py -m unittest` is fully functional and can independently validate backend ORM persistence (R2), REST endpoints, and static HTML/CSS/JS structural rules (R1, R3, R4).

---

## 5. Verification Method

### 5.1 Verification Commands
Run the following commands using PowerShell:
```powershell
# 1. Verify Python and Peewee compilation
py -m py_compile models.py backend.py desktop_app.py

# 2. Run Python unittest suite (once test files are created in tests/)
py -m unittest discover -s tests -p "test_*.py" -v
```

### 5.2 Independent Inspection Checks for R4
1. **Focus Mode Indicator Removal**:
   ```powershell
   # Must return 0 matches
   Select-String -Path "frontend/index.html" -Pattern "focus-mode-indicator"
   Select-String -Path "frontend/index.html" -Pattern "Modo Concentración Activo"
   ```
2. **Formatting Bar Amber Styling Exclusivity**:
   - Inspect `.desktop-format-bar` buttons in `frontend/styles.css`:
     - `#btn-insert-dropdown` has amber colors (`var(--accent-amber)`, `var(--accent-amber-soft)`).
     - `#btn-reopen-panels`, H1, B, I, U, `#btn-in-note-search`, `#btn-pin-note`, `#btn-page-appearance` have `background: transparent` or `var(--bg-surface)` and neutral hover (`var(--bg-elevated)`).
     - No format bar buttons other than `#btn-insert-dropdown` appear in the amber unification list (around lines 9685–9725).
