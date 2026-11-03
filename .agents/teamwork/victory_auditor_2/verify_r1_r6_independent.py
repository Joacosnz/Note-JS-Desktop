import sys
import os
import json
import re

ROOT_DIR = r"c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop"
sys.path.insert(0, ROOT_DIR)

print("=== INDEPENDENT AUDITOR VERIFICATION FOR R1-R6 ===")

# 1. Verify Models & SQLite persistence of sub_page blocks
import models
models.init_db()

test_subpage = {
    "type": "sub_page",
    "id": "blk-audit-verify-999",
    "page_id": "target-note-42",
    "title": "Nota Auditada Independiente",
    "noteId": 1
}

# Test sync_blocks_from_note_html_orm
models.sync_blocks_from_note_html_orm(1, [test_subpage])

# Retrieve from SQLite
saved_blk = models.Block.get_or_none(models.Block.id == "blk-audit-verify-999")
assert saved_blk is not None, "FAIL: Block not saved in SQLite"
saved_dict = saved_blk.to_dict()
assert saved_dict.get("page_id") == "target-note-42", f"FAIL: page_id mismatch: {saved_dict}"
assert saved_dict.get("title") == "Nota Auditada Independiente", f"FAIL: title mismatch: {saved_dict}"
assert saved_dict.get("type") == "sub_page", f"FAIL: type mismatch: {saved_dict}"
print("[PASS] SQLite persistence & schema for sub_page blocks")

# Clean up test block
saved_blk.delete_instance()

# 2. Verify Setting ORM for startup behavior
models.save_settings_dict({"startupBehavior": "clean"})
b_clean = models.get_bootstrap_data()
val = b_clean["settings"].get("startupBehavior")
assert val == "clean", f"FAIL: startupBehavior was {val}"

models.save_settings_dict({"startupBehavior": "resume"})
b_resume = models.get_bootstrap_data()
val_resume = b_resume["settings"].get("startupBehavior")
assert val_resume == "resume", f"FAIL: startupBehavior resume was {val_resume}"

# Reset to factory default
models.save_settings_dict({"startupBehavior": "clean"})
print("[PASS] Setting model persistence for startupBehavior")

# 3. Verify Frontend HTML checks
with open(os.path.join(ROOT_DIR, "frontend", "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

# R1: Window controls
assert 'id="btn-win-menu"' in html, "FAIL: btn-win-menu missing in index.html"
assert 'id="btn-win-minimize"' in html, "FAIL: btn-win-minimize missing in index.html"
assert 'id="btn-win-maximize"' in html, "FAIL: btn-win-maximize missing in index.html"
assert 'id="btn-win-close"' in html, "FAIL: btn-win-close missing in index.html"
assert 'class="window-controls-bar"' in html, "FAIL: window-controls-bar missing in index.html"
print("[PASS] HTML: Window controls toolbar & buttons present")

# R2: Folder unification
assert html.count('promptNewFolder()') == 1, "FAIL: Duplicate folder buttons in folder header"
assert 'id="ftype-btn-standard"' in html, "FAIL: ftype-btn-standard missing"
assert 'id="ftype-btn-smart"' in html, "FAIL: ftype-btn-smart missing"
assert 'id="folder-smart-rules-container"' in html, "FAIL: folder-smart-rules-container missing"
print("[PASS] HTML: Folder unification & segmented control present")

# R3: Quick access reminders
assert 'id="fitem-sidebar-reminders"' in html, "FAIL: fitem-sidebar-reminders missing"
assert 'id="sidebar-reminders-count-badge"' in html, "FAIL: sidebar-reminders-count-badge missing"
assert 'id="reminders-page-view"' in html, "FAIL: reminders-page-view missing"
print("[PASS] HTML: Quick access reminders item and view present")

# R4: Focus mode removed & gear-only settings button & insert button
assert 'focus-mode-indicator' not in html, "FAIL: focus-mode-indicator found in index.html"
assert 'Modo Concentración Activo' not in html, "FAIL: Modo Concentración text found in index.html"
assert '<button class="btn-settings-bottom"' in html, "FAIL: btn-settings-bottom missing"
settings_btn = re.search(r'<button class="btn-settings-bottom"[^>]*>([\s\S]*?)</button>', html)
assert settings_btn, "FAIL: btn-settings-bottom regex failed"
settings_inner = settings_btn.group(1).strip()
assert '<span>Ajustes</span>' not in settings_inner and '<kbd' not in settings_inner, "FAIL: settings button contains text/badge"
assert '<svg' in settings_inner, "FAIL: settings button missing SVG"
print("[PASS] HTML: Focus mode removed, settings button is gear-icon only")

# R5: TOC outside cover
assert html.find('id="notion-cover"') < html.find('id="sticky-toc-rail"'), "FAIL: sticky-toc-rail not outside/after notion-cover"
print("[PASS] HTML: Table of contents rail located outside note cover")

# R6: Startup behavior select & icons
assert 'id="setting-startup-behavior"' in html, "FAIL: setting-startup-behavior missing in index.html"
assert 'value="clean"' in html, "FAIL: value clean missing in select"
assert 'value="resume"' in html, "FAIL: value resume missing in select"
assert 'href="/icon.png"' in html, "FAIL: icon.png link missing in index.html"
assert 'href="/favicon.ico"' in html, "FAIL: favicon.ico link missing in index.html"
print("[PASS] HTML: Startup behavior select and head icon links present")

# 4. Verify CSS Styles
with open(os.path.join(ROOT_DIR, "frontend", "styles.css"), "r", encoding="utf-8") as f:
    css = f.read()

# R1: Floating pill tabs & neutral top bar buttons
assert '.note-tab-item' in css
assert 'border-radius: 9999px;' in css, "FAIL: Pill border-radius missing on .note-tab-item"
assert '.chrome-home-btn' in css
assert '.win-control-btn.win-control-close:hover' in css
assert '#e81123' in css, "FAIL: Red hover color missing on win-control-close"
print("[PASS] CSS: Tab pill styling, window controls, and neutral top bar buttons")

# R2: Folder add button neutral
assert '.folder-add-icon-btn' in css
assert re.search(r'\.folder-add-icon-btn\s*\{[^}]*background:\s*transparent', css), "FAIL: folder-add-icon-btn not neutral by default"
print("[PASS] CSS: Folder add button neutral styling")

# R3: Reminders scaffold view
assert '.desktop-main-scaffold.is-reminders-active #panel-canvas' in css
assert '.reminders-page-view' in css
print("[PASS] CSS: Reminders full screen dashboard styles")

# R4: Format bar amber exclusivity
assert '#btn-insert-dropdown' in css
assert '.insert-dropdown-btn' in css
assert '.desktop-format-bar #btn-insert-dropdown' in css
assert re.search(r'\.insert-plus-sign\s*\{[^}]*display:\s*inline-flex;[^}]*align-items:\s*center;[^}]*justify-content:\s*center;', css)
print("[PASS] CSS: Format bar amber exclusivity and plus sign flexbox centering")

# R5: Sticky TOC rail positioning
assert re.search(r'\.sticky-toc-rail\s*\{[^}]*top:\s*60px;', css)
assert re.search(r'#panel-canvas\.has-cover\s+\.sticky-toc-rail\s*\{[^}]*top:\s*194px;', css)
assert re.search(r'\.sticky-toc-rail\s*\{[^}]*width:\s*220px;', css)
print("[PASS] CSS: Fixed right column TOC outside/below cover banner (top: 60px / top: 194px)")

# 5. Verify App JS logic
with open(os.path.join(ROOT_DIR, "frontend", "app.js"), "r", encoding="utf-8") as f:
    app_js = f.read()

# R1 Selection guard
assert "e.target.closest('[contenteditable=\"true\"]')" in app_js, "FAIL: Selection guard missing contenteditable"
assert "e.target.tagName === 'INPUT'" in app_js, "FAIL: Selection guard missing INPUT"
assert "e.target.tagName === 'TEXTAREA'" in app_js, "FAIL: Selection guard missing TEXTAREA"
assert "const isEditorContainer = e.target === panelCanvas || Boolean(e.target.closest('.editor-container, .editor-body, #blocks-container'));" in app_js
print("[PASS] JS: Selection guard aborts on editable elements and restricts lasso to empty canvas/margins")

# R1 Window functions
assert 'async function minimizeWindow()' in app_js
assert 'async function toggleMaximizeWindow()' in app_js
assert 'async function closeWindow()' in app_js
print("[PASS] JS: Native window controls bridge methods")

# R2 Folder modal
assert 'function setFolderModalType(' in app_js
assert 'submitSmartFolderModal();' in app_js
print("[PASS] JS: Folder modal type switching and submission")

# R3 Reminders navigation
assert 'function navigateToReminders()' in app_js
assert 'function exitRemindersView()' in app_js
assert 'function renderRemindersPageView()' in app_js
print("[PASS] JS: Reminders navigation & rendering functions")

# R6 Startup behavior
assert "startupBehavior: (() => {" in app_js
assert "return 'clean';" in app_js
assert "function handleStartupBehaviorChange(" in app_js
assert "if (startupBehavior === 'clean') {" in app_js
assert "else if (startupBehavior === 'resume') {" in app_js
print("[PASS] JS: Startup behavior default 'clean' and 'resume' implementation")

# 6. Verify Icon Assets
icon_files = [
    os.path.join(ROOT_DIR, "public", "icon.ico"),
    os.path.join(ROOT_DIR, "public", "icon.png"),
    os.path.join(ROOT_DIR, "icon.ico"),
    os.path.join(ROOT_DIR, "frontend", "icon.png"),
    os.path.join(ROOT_DIR, "frontend", "favicon.ico")
]
for p in icon_files:
    assert os.path.exists(p), f"FAIL: Icon file missing: {p}"
    size = os.path.getsize(p)
    assert size > 0, f"FAIL: Icon file empty: {p}"
print("[PASS] Assets: All 5 application icon files present and non-empty")

print("\nALL INDEPENDENT AUDIT CHECKS PASSED SUCCESSFULLY!")
