# Scope: Note-JS-Desktop UI, Navigation & Startup Configuration (R1 - R6)

## Architecture
- **Desktop Runtime**: Windows desktop application using Python runtime (`desktop_app.py`, `backend.py`, `models.py`) serving static frontend UI (`frontend/index.html`, `frontend/styles.css`, `frontend/app.js`).
- **PyWebView Window Bridge**: Desktop window actions (minimize, maximize/restore, close) wired via `PyWebViewBridge` in `desktop_app.py` and fallback HTTP endpoints in `backend.py`.
- **Styling Architecture**: Theme tokens and CSS variables in `frontend/styles.css`, governing hover/active states, pill-shaped tabs, neutral button surfaces, format bar amber exclusivity, and right-column TOC.
- **Database & Settings**: SQLite database via Peewee ORM (`models.py`) managing `Folder`, `ReminderItem`, `Setting`, and `Note` entities with strict persistence of `startupBehavior`.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F6 | Tab Bar Rounded Pills & Window Controls (R1) | Neutral default styling on tab buttons (amber only on hover/active); pill-shaped tabs with icon, title, close '✕' button; adjacent '+' button; right-aligned window controls (`#btn-win-menu`, `#btn-win-minimize`, `#btn-win-maximize`, `#btn-win-close`) wired to PyWebViewBridge and `/api/window/*` fallback endpoints matching Image 1. | M3 | Survey E1 |
| F7 | Folder Management Unification & Duplicate Elimination (R2) | Eliminate duplicate folder creation buttons in sidebar; remove permanent yellow styling from `.folder-add-icon-btn` (amber only on hover/active); merge standard and smart folder creation into a single unified modal with segmented selector (`[📁 Estándar | ⚙️ Inteligente]`). | M3 | Survey E2 |
| F8 | Quick Access to Full-Screen Reminders (R3) | Add dedicated `#fitem-sidebar-reminders` in folder tray `sidebar-notion-quick-nav` with calendar icon and pending count badge; implement full-screen reminders view (`#reminders-page-view`) replacing main content area, with calendar and interactive reminders dashboard. | M3 | Survey E2 |
| F9 | Format Bar Amber Exclusivity, Vertically Centered Plus & Gear-Only Settings Button (R4) | In `.desktop-format-bar`, ensure `#btn-insert-dropdown` is the sole amber accent button; vertically align and center '+' with "Insertar" label via flexbox; render settings button at bottom of sidebar solely as gear SVG icon without text or shortcut badge matching Image 2. | M3 | Survey E1 |
| F10 | Table of Contents Right Fixed Column Outside Cover (R5) | Reposition `#sticky-toc-rail` outside/below cover banner (top: 60px without cover, top: 194px with cover) as a fixed right-side column (width ~220px) beside the editor, rendering open navigable headings list without requiring hover. | M3 | Survey E3 |
| F11 | Official App Icon Replacement & Startup Preference Strict Persistence (R6) | Convert Imagen 3 notepad graphic into multi-size `.ico` and `.png` assets in `public/` and `frontend/`; configure Windows Taskbar AppUserModelID and `icon` in `desktop_app.py`, `index.html`, `build_exe.bat`, and `NoteJS.spec`; add startup preference toggle in Settings ("Iniciar siempre de cero" vs "Reanudar en la última nota visitada"), strictly persisting to SQLite and defaulting to factory "Iniciar siempre de cero" (0 tabs, 0 open notes, null folder, Home view). | M3 | Survey E3 |
| F12 | Automated Test Suites & Regression Verification | Comprehensive automated tests in `tests/` validating R1-R6 requirements, persistence, layout rules, and cross-cutting editor interactions. | M3, M4 | Survey E1, E2, E3 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 3 | Full Implementation of R1-R6 & Automated Test Suites | Implement F6 (R1), F7 (R2), F8 (R3), F9 (R4), F10 (R5), F11 (R6), and F12 (Automated Test Suites). Run full test suite and verify 0 regressions. | Phase 0 Survey (Complete) | DONE (105 tests pass) |
| 4 | Verification, Dual Independent Review, Adversarial Challenge & Forensic Audit | Run full test suite, conduct dual independent reviews, dual adversarial challenger verification, and forensic integrity audit. | M3 | DONE (Gate PASS: Dual Review APPROVE, Dual Challenge APPROVE, Audit CLEAN, 145 tests pass) |

## Interface Contracts
### Window Controls Contract (`desktop_app.py` & `backend.py`)
- **PyWebViewBridge**:
  - `minimize_window()` -> minimizes active pywebview window
  - `toggle_maximize_window()` -> toggles maximize/restore
  - `close_window()` -> destroys/closes pywebview window
- **HTTP Endpoints**:
  - `POST /api/window/minimize` -> `{"success": true, "action": "minimize"}`
  - `POST /api/window/maximize` -> `{"success": true, "action": "maximize"}`
  - `POST /api/window/close` -> `{"success": true, "action": "close"}`

### Unified Folder Modal Contract (`frontend/app.js` & `frontend/index.html`)
- **Segmented Control**: `setFolderModalType(type)` where `type` is `'standard'` or `'smart'`.
- When `'standard'`: displays `#folder-parent-select-group`, hides `#folder-smart-rules-container`, submits to `/api/folders`.
- When `'smart'`: hides parent folder select, displays `#folder-smart-rules-container`, saves smart rules to `state.smartFolders` and `/api/smart-folders/save`.

### Full-Screen Reminders Contract (`frontend/app.js` & `frontend/index.html`)
- **Navigation Function**: `navigateToReminders()`
  - Activates `.is-reminders-active` on `#desktop-scaffold`.
  - Hides `#panel-gallery`, `#splitter-gallery-editor`, format bar, cover, and editor body.
  - Displays `#reminders-page-view` at 100% canvas width.
  - Renders interactive calendar, categorized task cards, and "+ Nuevo recordatorio".
- **Exit Function**: `exitRemindersView()` called when selecting a note, folder, or home.

### Table of Contents Right Column Contract (`frontend/styles.css`)
- **Selector**: `.sticky-toc-rail`
- Position: `position: absolute; right: 20px; width: 220px; z-index: 85;`
- Offset without cover: `top: 60px;` (below format bar)
- Offset with cover: `.notion-cover-container.has-cover ~ .sticky-toc-rail { top: 194px; }`
- Open display: `.sticky-toc-popover { position: static; width: 100%; max-height: 100%; overflow-y: auto; background: transparent; border: none; box-shadow: none; padding: 0; opacity: 1; pointer-events: auto; transform: none; }`

### Startup Preference Contract (`frontend/app.js`, `models.py`)
- **Setting Key**: `startupBehavior` with values `'clean'` (factory default) or `'resume'`.
- When `'clean'`: `openTabIds = []`, `activeNoteId = null`, `selectedFolder = null`, `isHomeActive = true`, open Home page.
- When `'resume'`: reads `lastVisitedNoteId`, restores that note and opens tab if valid.
- Persistence: Stored in SQLite `Setting` table and localStorage cache.

## Code Layout
- `desktop_app.py`: PyWebView window bridge methods, AppUserModelID, icon setup.
- `backend.py`: Window control HTTP fallback endpoints, server static routing.
- `frontend/index.html`: Window controls markup, unified folder modal segmented selector, reminders full-screen view container, settings startup preference select, icon favicon links, gear-only settings button.
- `frontend/styles.css`: Tab pill styles, neutral top bar button styles with hover/active amber, window controls styling, folder button neutral styling, full-screen reminders styling, TOC right column styling, format bar amber exclusivity and plus alignment.
- `frontend/app.js`: Window controls handlers, unified folder modal controller, reminders full-screen navigation and rendering, startup preference enforcement and note visit tracking.
- `public/icon.ico`, `public/icon.png`, `frontend/icon.png`, `frontend/favicon.ico`: Application icon assets generated from Imagen 3.
- `NoteJS.spec`, `build_exe.bat`: PyInstaller icon configurations.
- `tests/test_ui_production_r1_r6.py`: Comprehensive automated tests for R1-R6 (28 tests).
- `tests/test_adversarial_m3_r1_r4.py`: Adversarial empirical verification tests for R1-R4 (23 tests).
- `tests/test_adversarial_m3_r5_r6.py`: Adversarial empirical verification tests for R5-R6 (17 tests).
