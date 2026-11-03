# Handoff Report: Survey 2.3 — R5 (Table of Contents Right Column) & R6 (App Icon & Startup Preference)

**Investigator**: Teamwork Explorer  
**Working Directory**: `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey2_3\`  
**Scope**: 
- **R5**: Note Index / Table of Contents outside cover in fixed right column.
- **R6**: Official App Icon update (Imagen 3) & Startup Preference persistence ("Iniciar siempre de cero" vs "Reanudar en la última nota visitada").
- **Automated Test Strategy**: For R5, R6, and cross-cutting requirements R1–R4.

---

## 1. Observation

### 1.1 Visual Reference: Imagen 3 (Official App Icon)
- **Path**: `C:/Users/Joaco/.gemini/antigravity/brain/a7b54704-e486-450a-8698-6616535160da/.user_uploaded/media_1793492278932_da6ebc7c.png`
- **Dimensions & Format**: 192 × 192 pixels, PNG (RGBA, 8-bit/color).
- **Visual Design**: Square icon representing a lined legal notepad / notepad sheet:
  - Top header: Rich amber/yellow gold header bar (#f59e0b / #eab308 tone) with subtle bottom divider line.
  - Perforation: Horizontal row of dark gray perforated circular dots.
  - Paper body: Clean light-gray/off-white ruled paper with alternating horizontal rule lines.
- **Current App Assets**:
  - `public/`: Contains only `assets/aistudio/...` (historical screenshots/PDFs/mp4). No `icon.ico` or `icon.png` exists in `public/` or `frontend/`.
  - `frontend/index.html`: Has no `<link rel="icon">` or `<link rel="shortcut icon">` tags in `<head>`.
  - `desktop_app.py`: `webview.create_window` and `webview.start` do not pass any `icon` argument, and Windows Taskbar AppUserModelID is unconfigured (running as generic Python process).
  - `NoteJS.spec` & `build_exe.bat`: PyInstaller command (`"%PYINSTALLER_EXE%" --noconsole --onefile ... desktop_app.py`) omits `--icon` entirely.

---

### 1.2 Table of Contents / Index (Current Implementation)
1. **Markup (`frontend/index.html`, lines 677–703)**:
   ```html
   <!-- Portada (Cover Banner estilo Notion con Reposicionamiento Vertical) -->
   <div id="notion-cover" class="notion-cover-container" style="background-image: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);">
     <div class="notion-cover-actions">...</div>
     <div id="cover-reposition-bar" ...>...</div>
   </div>

   <!-- Riel Lateral Derecho Fijo: Tabla de Contenidos de Nivel de Página (Sticky TOC) -->
   <aside id="sticky-toc-rail" class="sticky-toc-rail" aria-label="Tabla de contenidos de la página">
     <div id="sticky-toc-bars" class="sticky-toc-rail-bars" title="Índice de encabezados de la página"></div>
     <div class="sticky-toc-popover">
       <div class="sticky-toc-header" style="display:flex; justify-content:space-between; align-items:center;">
         <span>ÍNDICE DE PÁGINA</span>
         <button type="button" class="btn-icon-tiny" onclick="togglePageStickyToc()" title="Ocultar riel de índice">✕</button>
       </div>
       <div id="sticky-toc-list" class="sticky-toc-list"></div>
     </div>
   </aside>
   ```

2. **Styling (`frontend/styles.css`, lines 5357–5424)**:
   ```css
   .sticky-toc-rail {
     position: fixed;
     right: 18px;
     top: 136px;
     width: 26px;
     max-height: calc(100vh - 180px);
     z-index: 95;
     display: flex;
     flex-direction: column;
     align-items: flex-end;
     transition: width 0.18s cubic-bezier(0.22, 1, 0.36, 1);
     pointer-events: auto;
   }
   .sticky-toc-popover {
     position: absolute;
     right: 0;
     top: 0;
     width: 235px;
     max-height: 68vh;
     overflow-y: auto;
     background: var(--bg-elevated);
     border: 1px solid var(--border-subtle);
     border-radius: 11px;
     box-shadow: 0 14px 36px rgba(0, 0, 0, 0.5);
     padding: 10px;
     opacity: 0;
     pointer-events: none;
     transform: translateX(6px);
     transition: opacity 0.16s ease, transform 0.16s ease;
   }
   .sticky-toc-rail:hover .sticky-toc-popover {
     opacity: 1;
     pointer-events: auto;
     transform: translateX(0);
   }
   ```

3. **Layout Collision**:
   - The top banner `.notion-cover-container` has `height: 130px;` and sits directly below the `48px` format bar (plus `~40px` tab/title bar), occupying the vertical space from Y ≈ 88px to Y ≈ 218px.
   - Because `.sticky-toc-rail` has `position: fixed; top: 136px; right: 18px; width: 26px;`, it is placed directly inside / on top of the cover banner image.
   - The index list itself is completely collapsed by default into three 2px bars (`sticky-toc-rail-bars`, width 26px) and only shows on hover.
   - The main editor `.editor-body` has `max-width: 920px; margin: 0 auto;`. In wide screens (>1200px), a huge empty space exists in the right margin beside the editor canvas, completely unused.

4. **Generation & Scripting (`frontend/app.js`, lines 13421–13481)**:
   - `collectEditorHeadings()` extracts H1, H2, H3 elements from `#rich-editor-canvas` and stamps `data-heading-idx`.
   - `refreshPageTableOfContents()` populates `#sticky-toc-bars` and `#sticky-toc-list`.
   - `scrollToHeadingByIndex(idx)` handles smooth scrolling and visual highlight when a heading is clicked.
   - `togglePageStickyToc()` toggles `note.showStickyToc` and adds `.hidden-rail` when disabled.
   - Abort guard for lasso selection in `test_adversarial_challenger.py` already checks `e.target.closest('#sticky-toc-rail')`.

---

### 1.3 Startup Preference & Settings (Current Implementation)
1. **Settings Organization**:
   - HTML (`frontend/index.html`, lines 1116–1250): Modal `#settings-modal` with left sidebar navigation (`.notion-settings-sidebar`) and content area (`.notion-settings-content`).
   - Active section by default is "Preferencias" (`#notion-sec-preferences`).
   - Setting rows follow standard pattern:
     ```html
     <div class="notion-setting-row" data-search-keys="...">
       <div class="notion-setting-info">
         <div class="notion-setting-title">...</div>
         <div class="notion-setting-desc">...</div>
       </div>
       <div class="notion-setting-control">
         <select id="..." class="notion-select" onchange="...">...</select>
       </div>
     </div>
     ```
2. **Persistence Mechanism**:
   - Multi-tier persistence:
     1. Local cache: `localStorage.getItem('notejs_settings_cache')` for immediate, zero-flicker startup.
     2. SQLite database: Table `Setting` (`key`, `value`) managed via Peewee ORM in `models.py` (`save_settings_dict`, `get_bootstrap_data`).
     3. Bridge: `window.pywebview.api.save_settings(payload)` and REST fallback `POST /api/settings`.
3. **Current Startup Lifecycle Defect**:
   - `frontend/app.js` lines 369–376:
     ```javascript
     activeNoteId: 1,
     openTabIds: (() => {
       try {
         const s = localStorage.getItem('notejs_open_tabs_v1');
         return s !== null ? JSON.parse(s) : [1, 101];
       } catch (_) {
         return [1, 101];
       }
     })(),
     selectedFolder: MASTER_ALL_NOTES_FOLDER,
     ```
   - On fresh startup, Note JS defaults to opening Note 1, opening tabs `[1, 101]`, and selecting folder `'Todas las notas'`.
   - In `initPythonBackendSync()` (lines 1146–1155 and 1186–1197), bootstrap data automatically restores `openTabIds` and calls `loadActiveNote()`.
   - **Violation of R6**: The application currently has no startup behavior toggle and does not start from zero by default.

---

## 2. Logic Chain

### 2.1 Logic Chain for R5 (Note Index / Table of Contents Right Column)
1. **Observation**: `#sticky-toc-rail` is currently hardcoded with `position: fixed; top: 136px; right: 18px; width: 26px;` inside `#panel-canvas`. When a cover banner is enabled, Y=136px is inside the cover banner boundaries (88px to 218px).
2. **Requirement**: "el índice (tabla de contenidos) debe ubicarse fuera de la portada/banner y situarse en una columna o barra lateral fija en el costado derecho del editor, aprovechando el espacio libre disponible."
3. **Layout Solution**:
   - `#panel-canvas` is `position: relative`. Position `#sticky-toc-rail` with `position: absolute; right: 20px;`.
   - **Outside Cover Banner**:
     - When cover is NOT shown (default or `.notion-cover-container` hidden): `top: 60px` (directly below the 48px format bar).
     - When cover IS shown (`.notion-cover-container.has-cover ~ .sticky-toc-rail`): `top: 194px` (48px format bar + 130px cover + 16px margin).
     - In both scenarios, the TOC starts strictly **below and outside** the cover banner.
   - **Fixed Column Beside Editor**:
     - Change width from 26px to a full right-side column: `width: 220px;` (max-height `calc(100% - 210px)`, `overflow-y: auto`).
     - Instead of hiding the popover (`opacity: 0`) and requiring a hover over the 3 small bars, the popover is flattened into the column surface (`position: static; opacity: 1; pointer-events: auto; box-shadow: none; background: transparent; border: none; padding: 0;`).
     - Display the title header ("ÍNDICE DE PÁGINA") with an optional hide/collapse button, followed directly by the navigable heading items (`#sticky-toc-list`).
     - Responsive behavior: When viewport/canvas is narrower than 1100px or when `.is-full-width` is active, apply safe right padding or gracefully collapse into the compact bar icon to prevent overlapping editor text.

---

### 2.2 Logic Chain for R6 Part 1 (App Icon Replacement)
1. **Observation**: Imagen 3 is a 192x192 PNG lined notepad graphic. PyInstaller, PyWebView, and HTML head currently specify no icon.
2. **Strategy**:
   - Generate standard multi-resolution Windows ICO file containing 16x16, 32x32, 48x48, 64x64, 128x128, 192x192 sizes from Imagen 3.
   - Windows natively supports `.NET` `System.Drawing` (already available via installed `pythonnet`) or Pillow to write `icon.ico` and copy `icon.png`.
   - Place assets at:
     - `public/icon.png` and `public/icon.ico`
     - Root `icon.ico`
     - `frontend/icon.png` and `frontend/favicon.ico`
   - Wire into:
     - `frontend/index.html`: `<link rel="icon" type="image/png" href="/icon.png">` and `<link rel="shortcut icon" href="/favicon.ico">`.
     - `desktop_app.py`: Set Windows Taskbar AppUserModelID:
       ```python
       if sys.platform == 'win32':
           try:
               import ctypes
               ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('NoteJS.Desktop.App.v2')
           except Exception:
               pass
       ```
       Pass `icon=icon_path` to `webview.start(debug=False, icon=icon_path)`.
     - `NoteJS.spec`: Set `exe = EXE(..., icon='public/icon.ico')`.
     - `build_exe.bat`: Add `--icon="public\icon.ico"` to PyInstaller compilation command.

---

### 2.3 Logic Chain for R6 Part 2 (Startup Preference Persistence)
1. **Observation**: Current initial state has `activeNoteId: 1`, `openTabIds: [1, 101]`, `selectedFolder: MASTER_ALL_NOTES_FOLDER`.
2. **Requirement**:
   - Settings toggle:
     1. "Iniciar siempre de cero" (sin notas abiertas, sin pestañas abiertas y sin carpetas seleccionadas).
     2. "Reanudar en la última nota visitada".
   - Factory default must strictly be "Iniciar siempre de cero".
   - Persisted in settings and applied strictly at each launch.
3. **Architecture & Implementation**:
   - Setting Key: `startupBehavior` with values `'clean'` (default) or `'resume'`.
   - Companion Key: `lastVisitedNoteId` (integer note ID).
   - **UI in Settings (`frontend/index.html`)**:
     Add inside `#notion-sec-preferences`:
     ```html
     <div class="notion-settings-group">
       <div class="notion-group-heading">Inicio de la aplicación</div>
       <div class="notion-setting-row" data-search-keys="inicio arrancar empezar reanudar cero abrir">
         <div class="notion-setting-info">
           <div class="notion-setting-title">Al iniciar Note JS</div>
           <div class="notion-setting-desc">Elige el estado inicial de la interfaz al abrir la aplicación</div>
         </div>
         <div class="notion-setting-control">
           <select id="setting-startup-behavior" class="notion-select" onchange="handleStartupBehaviorChange(this.value)">
             <option value="clean">Iniciar siempre de cero</option>
             <option value="resume">Reanudar en la última nota visitada</option>
           </select>
         </div>
       </div>
     </div>
     ```
   - **Factory Default Enforcement (`frontend/app.js`)**:
     - Default `startupBehavior = state.settings?.startupBehavior || 'clean'`.
     - If `startupBehavior === 'clean'`:
       - `state.openTabIds = []`
       - `state.activeNoteId = null`
       - `state.selectedFolder = null`
       - `state.isHomeActive = true`
       - Do not restore tabs from localStorage or backend.
       - Display Google Chrome Home page (`navigateToHome()`).
       - Folders panel shows no selected/active folder.
     - If `startupBehavior === 'resume'`:
       - Read `lastVisitedNoteId = state.settings?.lastVisitedNoteId || localStorage.getItem('notejs_last_visited_note')`.
       - If valid note exists, set `state.activeNoteId = Number(lastVisitedNoteId)`.
       - Ensure `state.openTabIds = [state.activeNoteId]`.
       - Set `state.isHomeActive = false`.
       - Call `loadActiveNote()`.
     - Note visit tracking: In `loadNote(id)` and `loadActiveNote()`, whenever a note is actively loaded, update `localStorage.setItem('notejs_last_visited_note', String(id))` and persist `{ lastVisitedNoteId: id }` via `save_settings`.

---

## 3. Caveats

1. **Backwards Compatibility with Existing Databases**:
   - Existing databases (`notejs.db`) may have rows in `Setting` table or existing tabs saved. The startup logic must prioritize the explicit `startupBehavior` key. If `startupBehavior` is absent in SQLite, the factory default **MUST BE `'clean'`**, ensuring a clean start unless the user explicitly toggles to "Reanudar".
2. **Empty Folder Selection State**:
   - In `frontend/app.js`, `renderFolders()` highlights folders based on `state.selectedFolder`. If `state.selectedFolder === null`, none of the folder rows will have the `.active` class. The implementation must ensure `renderNotesList()` and `renderFolders()` handle `state.selectedFolder === null` gracefully without defaulting back to `'Todas las notas'`.
3. **Lasso Selection Abort Guard Preservation**:
   - Existing test suites (`test_adversarial_challenger.py`, `test_challenger_it2_stress.py`) verify `e.target.closest('#sticky-toc-rail')` aborts lasso selection. Keeping the ID `#sticky-toc-rail` intact on the new right column ensures zero regressions.
4. **PyInstaller Environment Differences**:
   - `build_exe.bat` uses `%PYINSTALLER_EXE%`. Adding `--icon="public\icon.ico"` requires `public\icon.ico` to exist before the build script runs. The conversion script must be executed during build/setup.

---

## 4. Conclusion & Recommended File Touches

### Summary of Actions Required

| Requirement | Affected Files | Core Changes |
|---|---|---|
| **R5 (TOC Right Column)** | `frontend/styles.css`<br>`frontend/index.html`<br>`frontend/app.js` | Redesign `#sticky-toc-rail` from fixed hovering popover into a 220px right-side column positioned outside/below `#notion-cover` (`top: 60px` or `top: 194px`). Show headings list directly instead of only on hover. Add safety padding for wide/full-width editors. |
| **R6 (App Icon)** | `public/icon.png`<br>`public/icon.ico`<br>`frontend/icon.png`<br>`frontend/favicon.ico`<br>`desktop_app.py`<br>`build_exe.bat`<br>`NoteJS.spec`<br>`frontend/index.html` | Convert Imagen 3 to multi-size `.ico` and `.png`. Add `<link rel="icon">` in HTML `<head>`, pass `icon` to `webview.start`, configure Windows AppUserModelID in `desktop_app.py`, and add `--icon` to PyInstaller commands. |
| **R6 (Startup Preference)** | `frontend/index.html`<br>`frontend/app.js`<br>`models.py` | Add startup behavior `<select>` in Settings modal. Enforce factory default `'clean'` (0 tabs, 0 open notes, null folder, Home view). Track `lastVisitedNoteId` when set to `'resume'`. Persist via `Setting` table in SQLite. |

---

### Concrete Code Proposals

#### 1. R5: CSS in `frontend/styles.css`
```css
/* --- R5: Tabla de Contenidos en Columna Derecha Fija (Fuera de Portada) --- */
.sticky-toc-rail {
  position: absolute;
  right: 20px;
  top: 60px; /* Debajo de la barra de formato (48px) cuando no hay portada */
  width: 220px;
  max-height: calc(100% - 80px);
  z-index: 85;
  display: flex;
  flex-direction: column;
  pointer-events: auto;
  transition: top 0.2s cubic-bezier(0.2, 0, 0, 1), opacity 0.15s ease;
}

/* Cuando la portada está visible, ubicar el índice estrictamente debajo de ella */
.notion-cover-container.has-cover ~ .sticky-toc-rail {
  top: 194px; /* 48px formato + 130px portada + 16px margen */
  max-height: calc(100% - 215px);
}

.sticky-toc-rail.hidden-rail {
  display: none !important;
}

/* Contenedor principal de la columna de índice */
.sticky-toc-popover {
  position: static;
  width: 100%;
  max-height: 100%;
  overflow-y: auto;
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 0;
  opacity: 1;
  pointer-events: auto;
  transform: none;
}

.sticky-toc-header {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border-hairline);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sticky-toc-rail-bars {
  display: none; /* Ocultar las barritas compactas para mostrar la columna completa */
}

/* Espaciado de seguridad en el lienzo del editor para evitar solapamiento */
@media (min-width: 1200px) {
  .editor-body:not(.is-full-width) {
    margin-right: calc((100% - 920px) / 2);
  }
  .editor-body.is-full-width {
    padding-right: 260px !important;
  }
}
```

#### 2. R6: Asset Generation Script & Registration
```python
# scripts/generate_app_icons.py
import os
import clr
clr.AddReference('System.Drawing')
from System.Drawing import Bitmap, Icon
from System.IO import FileStream, FileMode

source_png = r'C:\Users\Joaco\.gemini\antigravity\brain\a7b54704-e486-450a-8698-6616535160da\.user_uploaded\media_1793492278932_da6ebc7c.png'
workspace = r'c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop'

bmp = Bitmap(source_png)
# Guardar PNGs
bmp.Save(os.path.join(workspace, 'public', 'icon.png'))
bmp.Save(os.path.join(workspace, 'frontend', 'icon.png'))

# Guardar ICOs
hicon = bmp.GetHicon()
ico = Icon.FromHandle(hicon)
for target in [os.path.join(workspace, 'public', 'icon.ico'),
               os.path.join(workspace, 'icon.ico'),
               os.path.join(workspace, 'frontend', 'favicon.ico')]:
    fs = FileStream(target, FileMode.Create)
    ico.Save(fs)
    fs.Close()
```

#### 3. R6: `desktop_app.py`
```python
# Configurar AppUserModelID para icono en barra de tareas de Windows 11
if sys.platform == 'win32':
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('NoteJS.Desktop.App.v2')
    except Exception:
        pass

# En launch_pywebview_app():
icon_file = os.path.join(os.path.dirname(__file__), 'public', 'icon.ico')
if not os.path.exists(icon_file):
    icon_file = os.path.join(os.path.dirname(__file__), 'icon.ico')

webview.start(debug=False, icon=icon_file if os.path.exists(icon_file) else None)
```

#### 4. R6: Startup Logic in `frontend/app.js`
```javascript
// En función init() o inicialización de estado:
function getEffectiveStartupBehavior() {
  const cached = JSON.parse(localStorage.getItem('notejs_settings_cache') || '{}');
  return state.settings?.startupBehavior || cached.startupBehavior || 'clean';
}

function applyStartupPreference() {
  const behavior = getEffectiveStartupBehavior();
  if (behavior === 'clean') {
    state.openTabIds = [];
    state.activeNoteId = null;
    state.selectedFolder = null;
    state.isHomeActive = true;
    localStorage.removeItem('notejs_open_tabs_v1');
    navigateToHome();
  } else if (behavior === 'resume') {
    const cached = JSON.parse(localStorage.getItem('notejs_settings_cache') || '{}');
    const lastNoteId = Number(state.settings?.lastVisitedNoteId || cached.lastVisitedNoteId || localStorage.getItem('notejs_last_visited_note'));
    if (lastNoteId && state.notes.some(n => n.id === lastNoteId)) {
      state.activeNoteId = lastNoteId;
      state.openTabIds = [lastNoteId];
      state.isHomeActive = false;
      loadActiveNote();
    } else {
      navigateToHome();
    }
  }
}
```

---

## 5. Verification Method

### 5.1 Test Execution Command
Run the test suite using the project Python runtime:
```powershell
& "C:\Users\Joaco\AppData\Local\Python\bin\python.exe" -m unittest discover -s tests -p "test_*.py"
```

### 5.2 Plan for New Automated Tests (`tests/test_toc_and_startup.py`)
1. **R5 TOC Layout Verification**:
   - `test_toc_rail_exists_and_contains_list`: Asserts `#sticky-toc-rail`, `#sticky-toc-list`, and `#sticky-toc-header` are defined.
   - `test_toc_rail_css_positioning_outside_cover`: Asserts `styles.css` positions `.sticky-toc-rail` outside cover (does not contain `top: 136px` hardcoded; contains rule `.notion-cover-container.has-cover ~ .sticky-toc-rail` with `top >= 190px`).
   - `test_toc_rail_column_width`: Asserts `.sticky-toc-rail` has column width (`200px` to `240px`).
   - `test_toc_headings_dynamic_update`: Verifies headings collection logic in JS correctly parses H1, H2, H3 and assigns `data-heading-idx`.
2. **R6 App Icon Verification**:
   - `test_icon_files_exist`: Asserts `public/icon.ico`, `public/icon.png`, `frontend/icon.png`, and `frontend/favicon.ico` exist and are valid image files.
   - `test_html_head_contains_favicons`: Asserts `index.html` contains `<link rel="icon"` and `<link rel="shortcut icon"`.
   - `test_pywebview_icon_registered`: Asserts `desktop_app.py` passes `icon` to `webview.start` and sets `AppUserModelID`.
   - `test_build_exe_spec_contains_icon`: Asserts `build_exe.bat` and `NoteJS.spec` include the `--icon` parameter.
3. **R6 Startup Preference Verification**:
   - `test_settings_html_contains_startup_toggle`: Asserts `#setting-startup-behavior` select exists in `#notion-sec-preferences` with options `clean` and `resume`.
   - `test_factory_default_is_clean`: Asserts that when settings are empty or default, `startupBehavior` defaults strictly to `'clean'` with 0 tabs, 0 active notes, and null folder.
   - `test_resume_behavior_restores_last_note`: Asserts that setting `startupBehavior = 'resume'` restores the note recorded in `lastVisitedNoteId`.
   - `test_sqlite_settings_persistence`: Asserts `Setting` table persists and loads `startupBehavior` and `lastVisitedNoteId`.
4. **Cross-Requirement Verification (R1–R4)**:
   - Run regression assertions against format bar neutral styles, sub-page blocks, and lasso abort guards to ensure zero breaking changes.
