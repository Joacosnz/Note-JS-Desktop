# Technical Investigation Report: Tab Bar Styles, Window Controls & Format Bar / Settings (R1 & R4)

## Executive Summary
This investigation covers Requirement 1 (Tab Bar Styles & Window Controls) and Requirement 4 (Formatting Bar & Settings Button) based on the project requirements and visual references:
- **Image 1** (`media_1793492072447_291e97ff.png`): Pill-shaped tabs with icon, text, and close '✕'; minimalist '+' new tab button; right-aligned window controls (menu/chevron `⌄`, minimize `—`, maximize/restore `▢`, close `✕`).
- **Image 2** (`media_1793492163191_1126a933.png`): Formatting toolbar where `+ Insertar` is the exclusive amber accent element, '+' is vertically centered with "Insertar", all other format buttons are neutral, and the settings button is exclusively a gear icon without text.

---

## 1. Observation

### 1.1 Reference Images Inspection
- **Image 1 (`media_1793492072447_291e97ff.png`)**:
  - The top bar is a sleek dark titlebar header.
  - On the left: a floating rounded pill tab (`border-radius: 9999px` / ~20px) containing:
    1. A small circular icon on the left (notebook / note icon).
    2. Note title label ("Nueva pestaña").
    3. A clean close '✕' button on the right inside the pill.
  - Active tab state shows a subtle warm amber border outline (`border-color: var(--accent-amber)` / subtle glow), but NOT a heavy solid amber fill.
  - Immediately to the right of the tab pill is an unadorned, neutral `+` button (no solid yellow background or heavy border).
  - On the far right: four window control buttons:
    1. Down chevron `⌄` (menu / options).
    2. Minimize `—`.
    3. Maximize / Restore `▢`.
    4. Close `✕`.
  - There is no separate yellow home button ("casita") or text buttons like "Atajos" cluttering the top bar.

- **Image 2 (`media_1793492163191_1126a933.png`)**:
  - The toolbar contains `[+ Insertar ⌵]` as the sole highlighted amber action button.
  - The `+` glyph is vertically centered with the "Insertar" label.
  - Buttons like `H1`, `B`, `/`, `U`, `Buscar (F3)`, `Pin`, `Trash`, `•••` should have neutral backgrounds and borders matching the container, NOT permanent yellow borders.

### 1.2 Current Codebase State

#### Tab Bar & Permanent Yellow Elements (`frontend/styles.css` & `frontend/index.html`)
- In `frontend/styles.css` lines 9801–9818:
  ```css
  /* 4. Botones Circulares del Top Bar */
  .chrome-home-btn,
  .note-tab-action-btn,
  #btn-new-tab,
  #btn-tab-picker {
    background: var(--accent-amber-soft) !important;
    color: var(--accent-amber) !important;
    border: 1px solid var(--accent-amber-border) !important;
  }
  ```
  These buttons are permanently painted in amber background and border, directly violating the requirement that tab bar buttons must not have permanent yellow styling.
- In `frontend/styles.css` lines 139–208, the `.note-tab-item` is styled as a Chrome-style trapezoid fused to the bottom border (`border-radius: 9px 9px 0 0; border-bottom: none; box-shadow: 0 -2px 0 0 var(--accent-amber);`), rather than the floating rounded pill in Image 1.
- In `frontend/index.html` lines 19–52:
  ```html
  <header class="top-bar chrome-tabs-bar">
    <button id="btn-top-home" class="chrome-home-btn" ...>...</button>
    <div class="note-tabs-bar-wrapper" id="note-tabs-bar-wrapper">...</div>
    <div class="top-actions">
      <button id="btn-open-shortcuts" class="top-shortcuts-btn" ...>Atajos</button>
    </div>
  </header>
  ```
  There are NO window control buttons (menu/chevron, minimize, maximize, close) in `top-bar`.

#### PyWebView Window Controls Integration (`desktop_app.py` & `backend.py`)
- In `desktop_app.py` lines 198–209:
  ```python
  window = webview.create_window(
      title='Note JS — PC Desktop (PyWebView + SQLite & Peewee ORM)',
      url=url,
      js_api=bridge,
      width=1360,
      height=860,
      min_size=(940, 620),
      background_color='#0f1115',
      text_select=True,
      confirm_close=False,
  )
  ```
  `desktop_app.py` exposes `PyWebViewBridge` via `js_api=bridge`.
- Running inspection on Python 3.15 with PyWebView 6.2.1:
  `webview.Window` natively provides `minimize()`, `maximize()`, `restore()`, and `destroy()`.
- However, `PyWebViewBridge` in `desktop_app.py` currently has NO methods exposed for window minimization, maximization/restoration, or closing.
- In `backend.py` lines 145–450, there are no HTTP endpoints to control window actions.

#### Format Bar & Settings Button (`frontend/index.html` & `frontend/styles.css`)
- In `frontend/index.html` lines 275–281:
  ```html
  <button id="btn-insert-dropdown" class="format-bar-btn insert-dropdown-btn" onmousedown="event.preventDefault()" onclick="toggleInsertDropdown(event)" style="border:1px solid var(--accent-amber-border); color:var(--accent-amber); display:inline-flex; align-items:center; gap:5px; height:28px; padding:0 10px;" title="Insertar bloques, columnas, imágenes, fórmulas y herramientas (Ctrl+Shift+I)">
    <span class="insert-plus-sign" style="display:inline-flex; align-items:center; justify-content:center; font-size:15px; font-weight:700; line-height:1; transform:translateY(-0.5px);" aria-hidden="true">+</span>
    <span style="line-height:1; font-weight:600;">Insertar</span>
    ...
  </button>
  ```
  The `+` character has an ad-hoc inline transform `transform:translateY(-0.5px);` which can misalign depending on rendering zoom/DPI.
- In `frontend/index.html` lines 142–149:
  ```html
  <!-- Botón de engranaje (Ajustes) anclado en la parte inferior -->
  <button class="btn-settings-bottom" onclick="openSettingsModal()" data-shortcut-tooltip="open_settings" title="Ajustes (Ctrl+,)">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="3"></circle>
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82..."></path>
    </svg>
    <span style="flex:1; text-align:left;">Ajustes</span>
    <kbd class="ui-kbd-badge" data-shortcut-badge="open_settings">Ctrl+,</kbd>
  </button>
  ```
  The settings button currently includes text `<span>Ajustes</span>` and a keyboard badge `<kbd>Ctrl+,</kbd>`, directly violating the requirement that it must consist exclusively of the gear icon.

---

## 2. Logic Chain

1. **Tab Bar Color Normalization**:
   - Observations 1.1 and 1.2 show that `styles.css:9801-9818` forces `background: var(--accent-amber-soft) !important` on top bar buttons.
   - Therefore, removing this forced rule and setting the default state of `#btn-top-home`, `#btn-new-tab`, `#btn-tab-picker`, and tab items to neutral backgrounds and borders (`transparent` or `var(--bg-elevated)` and `var(--border-hairline)`) will satisfy the acceptance criteria that tabs and buttons display neutral backgrounds by default.
   - Adding `:hover` and `.active` selectors that apply amber styling (`color: var(--accent-amber); border-color: var(--accent-amber);`) ensures amber highlighting is only applied on hover or active/pressed state.

2. **Tab Pill Appearance Matching Image 1**:
   - Image 1 shows discrete floating pills with `border-radius: 9999px` (or `20px`), height ~30px, an icon on the left, note title in the center, and a close '✕' icon button on the right.
   - In `styles.css`, refactoring `.note-tab-item` from Chrome tab bottom-docked styles (`border-radius: 9px 9px 0 0`) to pill styling (`border-radius: 20px; border: 1px solid var(--border-hairline); margin: 0 3px; align-self: center;`) matches Image 1.
   - The close button `.note-tab-close` should be styled as a clean circular target with hover brightening.
   - The `+` new tab button (`#btn-new-tab`) should sit directly next to the tab pills with neutral styling, clean plus icon, and subtle hover highlight.

3. **Window Controls Integration**:
   - In desktop mode, windows require minimize, maximize/restore, and close capabilities.
   - Since PyWebView 6.2.1 is running the app, `desktop_app.py`'s `PyWebViewBridge` can expose:
     - `minimize_window()` calling `webview.windows[0].minimize()`
     - `toggle_maximize_window()` toggling `win.restore()` and `win.maximize()`
     - `close_window()` calling `webview.windows[0].destroy()`
   - In `backend.py`, mirroring these actions at `POST /api/window/minimize`, `POST /api/window/maximize`, and `POST /api/window/close` provides an API fallback and enables automated test validation without a GUI display.
   - In `frontend/index.html`, adding `.window-controls-bar` on the right of `.top-bar` with:
     - Menu/chevron (`#btn-win-menu`)
     - Minimize (`#btn-win-minimize`)
     - Maximize/Restore (`#btn-win-maximize`)
     - Close (`#btn-win-close`)
   - In `frontend/app.js`, handlers call `window.pywebview.api.*` or fallback to `/api/window/*`.
   - On close hover, Windows convention styles the button with red accent (`background: #e81123; color: white`).

4. **Format Bar Amber Exclusivity & Plus Centering (R4)**:
   - In `.desktop-format-bar`, ensure `#btn-insert-dropdown` is the ONLY element with amber accent.
   - The plus glyph `.insert-plus-sign` within `#btn-insert-dropdown` should use flexbox centering (`display: inline-flex; align-items: center; justify-content: center; line-height: 1; vertical-align: middle;`) alongside `span` with `line-height: 1;` so it is vertically centered with "Insertar".
   - Non-insert buttons (`H1`, `B`, `I`, `U`, `#btn-in-note-search`, `#btn-pin-note`, `#btn-page-appearance`) are styled with neutral container background (`transparent` or `var(--bg-surface)`) and subtle border.

5. **Settings Button Refactoring (R4)**:
   - In `frontend/index.html`, remove `<span>Ajustes</span>` and `<kbd class="ui-kbd-badge">Ctrl+,</kbd>` from `.btn-settings-bottom`.
   - In `frontend/styles.css`, update `.btn-settings-bottom` from full-width button to a sleek square icon button (`width: 34px; height: 34px; display: inline-flex; justify-content: center; align-items: center; border-radius: 8px;`).

---

## 3. Caveats

- **Frameless Window vs Standard Window**:
  If `frameless=True` is enabled in `webview.create_window()`, WebView2 on Windows removes the native OS title bar and allows the top bar to serve as the application title bar. Titlebar dragging in Chromium WebView2 is achieved with `-webkit-app-region: drag;` on `.top-bar` and `-webkit-app-region: no-drag;` on tabs and buttons. If running in a regular web browser, window controls gracefully emulate or no-op via the backend endpoints.
- **Maximized State Tracking**:
  When maximizing or restoring, tracking `_is_maximized` in `PyWebViewBridge` and updating the `#btn-win-maximize` icon (single square vs overlapping squares) maintains parity with Windows desktop conventions.

---

## 4. Conclusion & Recommendations

1. **R1 Tab Bar**:
   - Clean up `frontend/styles.css` rules (lines 9801–9818) that force amber backgrounds on `.chrome-home-btn`, `.note-tab-action-btn`, `#btn-new-tab`, `#btn-tab-picker`.
   - Refactor `.note-tab-item` to rounded pills (`border-radius: 20px` / `border-radius: 9999px`) with neutral dark background, subtle border, note icon, title, and close '✕'.
   - Add amber highlight only on `:hover` or `.active`.
   - Add `.window-controls-bar` to `.top-bar` with menu/chevron `⌄`, minimize `—`, maximize `▢`, and close `✕`.

2. **R1 Window Controls Integration**:
   - Add `minimize_window()`, `toggle_maximize_window()`, and `close_window()` to `PyWebViewBridge` in `desktop_app.py`.
   - Add matching endpoints `POST /api/window/minimize`, `POST /api/window/maximize`, `POST /api/window/close` in `backend.py`.
   - Implement `minimizeWindow()`, `toggleMaximizeWindow()`, `closeWindow()` in `frontend/app.js`.

3. **R4 Format Bar & Settings**:
   - Guarantee `+ Insertar` is the only amber button in `.desktop-format-bar`.
   - Vertically center the `+` sign with `Insertar` using flexbox alignment in `styles.css`.
   - Strip label text and shortcut badge from `.btn-settings-bottom` in `frontend/index.html` so it renders solely as a gear icon button.

### Proposed File Touches

| File | Changes Needed |
|------|----------------|
| `desktop_app.py` | Add `minimize_window`, `toggle_maximize_window`, `close_window` methods to `PyWebViewBridge`. Optional `frameless=True` with shadow. |
| `backend.py` | Add `POST /api/window/minimize`, `POST /api/window/maximize`, `POST /api/window/close` to `NoteJSRequestHandler`. |
| `frontend/index.html` | 1. Add `.window-controls-bar` inside `header.top-bar`.<br>2. Remove text `Ajustes` and `<kbd>` badge from `.btn-settings-bottom`.<br>3. Verify `.insert-plus-sign` structure in `#btn-insert-dropdown`. |
| `frontend/styles.css` | 1. Neutralize tab bar buttons by default; apply amber only on hover/active.<br>2. Style `.note-tab-item` as rounded pills matching Image 1.<br>3. Style `.window-controls-bar` and `.win-control-btn` (with red hover on close).<br>4. Center `.insert-plus-sign` in `#btn-insert-dropdown`.<br>5. Style `.btn-settings-bottom` as a compact icon-only button. |
| `frontend/app.js` | 1. Implement `minimizeWindow()`, `toggleMaximizeWindow()`, `closeWindow()`.<br>2. Update `renderNoteTabs()` to render pill tabs matching Image 1. |
| `tests/test_tabs_and_window_controls.py` | New comprehensive test suite validating R1 & R4 criteria. |

---

## 5. Verification Method

1. **Automated Unit & Integration Tests**:
   - Run `py -3.15 -m unittest discover tests` to ensure all 77 existing tests pass.
   - Run new tests in `tests/test_tabs_and_window_controls.py` verifying:
     - Neutral default background and border for all tab bar buttons (`#btn-new-tab`, `#btn-tab-picker`, `.chrome-home-btn`, `.note-tab-item`).
     - Amber styling present on `:hover` and `.active` for tabs.
     - Presence of window controls (`btn-win-menu`, `btn-win-minimize`, `btn-win-maximize`, `btn-win-close`) in `frontend/index.html`.
     - Presence of window control endpoints `/api/window/minimize`, `/api/window/maximize`, `/api/window/close` in `backend.py`.
     - Presence of bridge methods `minimize_window`, `toggle_maximize_window`, `close_window` on `PyWebViewBridge` in `desktop_app.py`.
     - Exclusivity of amber styling for `#btn-insert-dropdown` in `.desktop-format-bar`.
     - Settings button `.btn-settings-bottom` containing ONLY the SVG gear icon and no text.

2. **Manual / Visual Inspection**:
   - Compare running top bar against Image 1: pill-shaped tabs, adjacent '+' button, and right-aligned window controls.
   - Compare format bar against Image 2: only `+ Insertar` has amber accent, '+' is vertically centered with "Insertar", and settings button at the bottom of panel-folders is solely a gear icon.

3. **Invalidation Conditions**:
   - Any tab button displaying a yellow background or border when not hovered or active.
   - Settings button rendering text "Ajustes" or badge "Ctrl+,".
   - Any format bar button besides `+ Insertar` having yellow background or yellow border.
   - Window control buttons failing to trigger PyWebView minimize, maximize/restore, or close actions.
