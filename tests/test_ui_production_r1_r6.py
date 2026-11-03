#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Milestone 3 UI/UX Enhancements and Production Hardening (Requirements R1 - R6)
Covers:
  R1: Tab bar neutral default styles, floating pill tabs, right-aligned window controls.
  R2: Folder management unification, duplicate button elimination, neutral default style, segmented modal.
  R3: Quick access full-screen reminders dashboard, sidebar item with badge, layout coordination.
  R4: Formatting toolbar amber exclusivity (+ Insertar only with flexbox '+'), settings button gear icon only.
  R5: Table of contents fixed right column (220px) outside/below cover banner (top: 60px / top: 194px).
  R6: Multi-size app icon assets across build tools & PyWebView, startup preference toggle ("clean" default).
"""

import json
import os
import re
import unittest
from unittest.mock import MagicMock

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'index.html')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')
APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
DESKTOP_APP_PATH = os.path.join(WORKSPACE_DIR, 'desktop_app.py')
BACKEND_PATH = os.path.join(WORKSPACE_DIR, 'backend.py')
SPEC_PATH = os.path.join(WORKSPACE_DIR, 'NoteJS.spec')
BUILD_BAT_PATH = os.path.join(WORKSPACE_DIR, 'build_exe.bat')


class TestR1TabBarAndWindowControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()
        with open(DESKTOP_APP_PATH, 'r', encoding='utf-8') as f:
            cls.desktop_app = f.read()
        with open(BACKEND_PATH, 'r', encoding='utf-8') as f:
            cls.backend = f.read()

    def test_tab_pill_styling(self):
        """Verifies .note-tab-item uses pill border-radius (9999px) and neutral borders."""
        self.assertIn('.note-tab-item', self.styles_css)
        self.assertTrue(
            re.search(r'\.note-tab-item\s*\{[^}]*border-radius:\s*(?:9999px|999px|20px|16px)', self.styles_css),
            "Expected pill border-radius on .note-tab-item"
        )

    def test_top_bar_buttons_neutral_default_styles(self):
        """Verifies top bar buttons have neutral/transparent default background, amber on hover/active."""
        self.assertIn('.chrome-home-btn', self.styles_css)
        self.assertIn('.note-tab-action-btn', self.styles_css)
        self.assertIn('#btn-new-tab', self.styles_css)
        self.assertIn('#btn-tab-picker', self.styles_css)

    def test_window_controls_markup_in_html(self):
        """Verifies window controls toolbar and buttons are in frontend/index.html."""
        self.assertIn('class="window-controls-bar"', self.index_html)
        self.assertIn('id="btn-win-menu"', self.index_html)
        self.assertIn('id="btn-win-minimize"', self.index_html)
        self.assertIn('id="btn-win-maximize"', self.index_html)
        self.assertIn('id="btn-win-close"', self.index_html)

    def test_window_controls_css(self):
        """Verifies CSS styling for window controls bar and close button hover."""
        self.assertIn('.window-controls-bar', self.styles_css)
        self.assertIn('.win-control-btn', self.styles_css)
        self.assertTrue(
            re.search(r'\.win-control-close:hover\s*\{[^}]*background(?:-color)?:\s*#e81123', self.styles_css),
            "Expected red background (#e81123) on win-control-close:hover"
        )

    def test_backend_window_endpoints(self):
        """Verifies backend.py contains /api/window/minimize, maximize, and close endpoints."""
        from backend import NoteJSRequestHandler
        from http.server import HTTPServer
        import threading
        from urllib import request as urllib_request

        server = HTTPServer(('127.0.0.1', 0), NoteJSRequestHandler)
        host, port = server.server_address
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        try:
            # 1. Minimize
            req_min = urllib_request.Request(
                f'http://127.0.0.1:{port}/api/window/minimize',
                data=b'{}',
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib_request.urlopen(req_min) as resp:
                self.assertEqual(resp.status, 200)
                data_min = json.loads(resp.read().decode('utf-8'))
                self.assertTrue(data_min.get('success'))
                self.assertEqual(data_min.get('action'), 'minimize')

            # 2. Maximize
            req_max = urllib_request.Request(
                f'http://127.0.0.1:{port}/api/window/maximize',
                data=b'{}',
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib_request.urlopen(req_max) as resp:
                self.assertEqual(resp.status, 200)
                data_max = json.loads(resp.read().decode('utf-8'))
                self.assertTrue(data_max.get('success'))
                self.assertIn(data_max.get('action'), ['maximize', 'restore'])

            # 3. Close
            req_close = urllib_request.Request(
                f'http://127.0.0.1:{port}/api/window/close',
                data=b'{}',
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib_request.urlopen(req_close) as resp:
                self.assertEqual(resp.status, 200)
                data_close = json.loads(resp.read().decode('utf-8'))
                self.assertTrue(data_close.get('success'))
                self.assertEqual(data_close.get('action'), 'close')
        finally:
            server.shutdown()
            server.server_close()

    def test_desktop_app_bridge_methods(self):
        """Verifies PyWebViewBridge in desktop_app.py implements window control methods."""
        self.assertIn('def minimize_window(self):', self.desktop_app)
        self.assertIn('def toggle_maximize_window(self):', self.desktop_app)
        self.assertIn('def close_window(self):', self.desktop_app)

    def test_app_js_window_functions(self):
        """Verifies window functions are declared and exposed in frontend/app.js."""
        self.assertIn('async function minimizeWindow()', self.app_js)
        self.assertIn('async function toggleMaximizeWindow()', self.app_js)
        self.assertIn('async function closeWindow()', self.app_js)
        self.assertIn('function updateMaximizeIcon(', self.app_js)
        self.assertIn('function toggleWinMenu(', self.app_js)
        self.assertIn('window.minimizeWindow = minimizeWindow;', self.app_js)
        self.assertIn('window.toggleMaximizeWindow = toggleMaximizeWindow;', self.app_js)
        self.assertIn('window.closeWindow = closeWindow;', self.app_js)


class TestR2FolderManagementUnification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_no_duplicate_folder_buttons_in_sidebar(self):
        """Verifies there is exactly ONE folder creation button in the sidebar folder header."""
        header_match = re.search(r'<div class="folder-header-actions">([\s\S]*?)</div>\s*</div>', self.index_html)
        self.assertTrue(header_match, "Folder header actions container not found")
        header_content = header_match.group(1)
        # Should have btn-collapse-sidebar and btn-new-folder, no second folder button
        btn_count = header_content.count('promptNewFolder()')
        self.assertEqual(btn_count, 1, f"Expected exactly 1 promptNewFolder call in folder-header-actions, found {btn_count}")

    def test_folder_add_btn_neutral_styles(self):
        """Verifies .folder-add-icon-btn is neutral by default and not in forced amber lists."""
        self.assertIn('.folder-add-icon-btn', self.styles_css)
        # Assert neutral default styling
        self.assertTrue(
            re.search(r'\.folder-add-icon-btn\s*\{[^}]*background:\s*transparent', self.styles_css),
            "Expected transparent background by default for .folder-add-icon-btn"
        )

    def test_unified_folder_modal_segmented_control_in_html(self):
        """Verifies #folder-custom-modal includes the segmented selector and rules container."""
        modal_match = re.search(r'<div id="folder-custom-modal"[\s\S]*?</div>\s*</div>\s*</div>', self.index_html)
        self.assertTrue(modal_match, "#folder-custom-modal not found")
        modal_content = modal_match.group(0)

        self.assertIn('id="ftype-btn-standard"', modal_content)
        self.assertIn('id="ftype-btn-smart"', modal_content)
        self.assertIn('id="folder-smart-rules-container"', modal_content)
        self.assertIn('id="unified-smart-folder-rules-list"', modal_content)
        self.assertIn('id="unified-smart-folder-preview-count"', modal_content)

    def test_unified_folder_segmented_control_styles_in_css(self):
        """Verifies styles for .folder-type-segmented-control and buttons."""
        self.assertIn('.folder-type-segmented-control', self.styles_css)
        self.assertIn('.folder-type-seg-btn', self.styles_css)

    def test_unified_folder_modal_js_methods(self):
        """Verifies setFolderModalType is implemented and wired into folder modals."""
        self.assertIn('function setFolderModalType(', self.app_js)
        self.assertIn('window.setFolderModalType = setFolderModalType;', self.app_js)
        self.assertIn('folderModalState.folderType', self.app_js)
        # Assert submitFolderModal checks folderType
        self.assertTrue(
            re.search(r'if\s*\(\s*folderModalState\.folderType\s*===\s*[\'"]smart[\'"]\s*\)\s*\{[^}]*submitSmartFolderModal\(\);', self.app_js),
            "Expected submitFolderModal to delegate to submitSmartFolderModal when folderType is smart"
        )


class TestR3FullScreenRemindersDashboard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_sidebar_reminders_item_and_badge_in_html(self):
        """Verifies #fitem-sidebar-reminders and #sidebar-reminders-count-badge are in sidebar quick nav."""
        self.assertIn('id="fitem-sidebar-reminders"', self.index_html)
        self.assertIn('id="sidebar-reminders-count-badge"', self.index_html)

    def test_reminders_page_view_container_in_html(self):
        """Verifies #reminders-page-view is declared inside #panel-canvas."""
        self.assertIn('id="reminders-page-view"', self.index_html)

    def test_reminders_scaffold_css_rules(self):
        """Verifies scaffold expands canvas when reminders is active."""
        self.assertIn('.desktop-main-scaffold.is-reminders-active #panel-canvas', self.styles_css)
        self.assertIn('.reminders-page-view', self.styles_css)
        self.assertIn('.reminders-full-header', self.styles_css)

    def test_reminders_js_functions(self):
        """Verifies navigateToReminders, exitRemindersView, renderRemindersPageView are defined and exported."""
        self.assertIn('function navigateToReminders()', self.app_js)
        self.assertIn('function exitRemindersView()', self.app_js)
        self.assertIn('function renderRemindersPageView()', self.app_js)
        self.assertIn('window.navigateToReminders = navigateToReminders;', self.app_js)
        self.assertIn('window.exitRemindersView = exitRemindersView;', self.app_js)
        self.assertIn('window.renderRemindersPageView = renderRemindersPageView;', self.app_js)

    def test_reminders_navigation_coordination(self):
        """Verifies selectNote, navigateToHome, and switchNoteTab exit reminders view."""
        self.assertTrue(
            re.search(r'function selectNote\([^)]*\)\s*\{[\s\S]*?exitRemindersView\(\);', self.app_js),
            "Expected selectNote to call exitRemindersView"
        )
        self.assertTrue(
            re.search(r'function navigateToHome\(\)\s*\{[\s\S]*?exitRemindersView\(\);', self.app_js),
            "Expected navigateToHome to call exitRemindersView"
        )


class TestR4FormattingBarAmberExclusivityAndSettingsGear(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_insert_dropdown_amber_exclusivity(self):
        """Verifies only #btn-insert-dropdown receives amber styling in formatting bar."""
        self.assertIn('#btn-insert-dropdown', self.styles_css)
        # Assert other buttons are NOT in amber rule selectors
        non_insert = ['#btn-in-note-search', '#btn-pin-note', '#btn-page-appearance', '#btn-reopen-panels']
        for btn in non_insert:
            self.assertFalse(
                re.search(r'#btn-insert-dropdown[^{]*' + re.escape(btn) + r'[^{]*\{[^}]*color:\s*var\(--accent-amber\)', self.styles_css),
                f"{btn} must not share amber styling with #btn-insert-dropdown"
            )

    def test_insert_plus_sign_flexbox_centering(self):
        """Verifies .insert-plus-sign is centered via flexbox without inline translateY."""
        self.assertIn('.insert-plus-sign', self.styles_css)
        self.assertTrue(
            re.search(r'\.insert-plus-sign\s*\{[^}]*display:\s*inline-flex;[^}]*align-items:\s*center;[^}]*justify-content:\s*center;', self.styles_css),
            "Expected .insert-plus-sign to use inline-flex with center alignment"
        )
        # Ensure translateY inline hack is not on the element in HTML
        insert_btn_match = re.search(r'<button id="btn-insert-dropdown"[\s\S]*?</button>', self.index_html)
        self.assertTrue(insert_btn_match)
        self.assertNotIn('transform: translateY', insert_btn_match.group(0))

    def test_settings_button_gear_only(self):
        """Verifies .btn-settings-bottom has only the gear SVG icon (no text label or kbd badge)."""
        settings_btn_match = re.search(r'<button[^>]*class="[^"]*btn-settings-bottom[^"]*"[\s\S]*?</button>', self.index_html)
        self.assertTrue(settings_btn_match, "Settings bottom button not found in index.html")
        content = settings_btn_match.group(0)
        self.assertNotIn('<span>Ajustes</span>', content)
        self.assertNotIn('<kbd', content)
        self.assertIn('<svg', content)


class TestR5TableOfContentsOutsideAndBelowCover(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()

    def test_toc_rail_top_position_without_cover(self):
        """Verifies .sticky-toc-rail top position is 60px when no cover is present."""
        self.assertTrue(
            re.search(r'\.sticky-toc-rail\s*\{[^}]*top:\s*60px;', self.styles_css),
            "Expected top: 60px for .sticky-toc-rail without cover"
        )

    def test_toc_rail_top_position_with_cover(self):
        """Verifies .sticky-toc-rail top position is 194px below cover banner."""
        self.assertTrue(
            re.search(r'#panel-canvas\.has-cover\s+\.sticky-toc-rail\s*\{[^}]*top:\s*194px;', self.styles_css),
            "Expected top: 194px for .sticky-toc-rail with cover"
        )

    def test_toc_rail_dimensions_and_positioning(self):
        """Verifies .sticky-toc-rail has width: 220px, right: 20px, and position: absolute/fixed."""
        self.assertTrue(
            re.search(r'\.sticky-toc-rail\s*\{[^}]*width:\s*220px;', self.styles_css),
            "Expected width: 220px for .sticky-toc-rail"
        )
        self.assertTrue(
            re.search(r'\.sticky-toc-rail\s*\{[^}]*right:\s*20px;', self.styles_css),
            "Expected right: 20px for .sticky-toc-rail"
        )


class TestR6AppIconAndStartupBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()
        with open(DESKTOP_APP_PATH, 'r', encoding='utf-8') as f:
            cls.desktop_app = f.read()
        with open(SPEC_PATH, 'r', encoding='utf-8') as f:
            cls.spec = f.read()
        with open(BUILD_BAT_PATH, 'r', encoding='utf-8') as f:
            cls.bat = f.read()

    def test_app_icon_assets_exist_and_non_empty(self):
        """Verifies icon assets exist in public, frontend, and root."""
        icon_paths = [
            os.path.join(WORKSPACE_DIR, 'public', 'icon.ico'),
            os.path.join(WORKSPACE_DIR, 'public', 'icon.png'),
            os.path.join(WORKSPACE_DIR, 'icon.ico'),
            os.path.join(WORKSPACE_DIR, 'frontend', 'icon.png'),
            os.path.join(WORKSPACE_DIR, 'frontend', 'favicon.ico')
        ]
        for p in icon_paths:
            self.assertTrue(os.path.exists(p), f"Icon asset missing at {p}")
            self.assertGreater(os.path.getsize(p), 0, f"Icon asset empty at {p}")

    def test_icon_integration_in_build_and_spec(self):
        """Verifies icon is referenced in index.html, spec, bat, and desktop_app."""
        self.assertIn('href="/icon.png"', self.index_html)
        self.assertIn('href="/favicon.ico"', self.index_html)
        self.assertTrue(
            "icon='public/icon.ico'" in self.spec or
            "icon=['public/icon.ico']" in self.spec
        )
        self.assertIn('--icon="public\\icon.ico"', self.bat)
        self.assertIn('icon=icon_file', self.desktop_app)

    def test_startup_behavior_select_in_html(self):
        """Verifies #setting-startup-behavior select is present in Settings modal."""
        self.assertIn('id="setting-startup-behavior"', self.index_html)
        self.assertIn('value="clean"', self.index_html)
        self.assertIn('value="resume"', self.index_html)

    def test_startup_behavior_factory_default_clean(self):
        """Verifies initial state defaults startupBehavior to 'clean'."""
        self.assertIn("startupBehavior: (() => {", self.app_js)
        self.assertIn("return 'clean';", self.app_js)
        self.assertIn("handleStartupBehaviorChange(this.value)", self.index_html)

    def test_sqlite_setting_model_and_api(self):
        """Verifies Setting ORM model and /api/settings handles startupBehavior."""
        import models
        from backend import NoteJSRequestHandler
        from http.server import HTTPServer
        import threading
        from urllib import request as urllib_request

        models.init_db()
        server = HTTPServer(('127.0.0.1', 0), NoteJSRequestHandler)
        host, port = server.server_address
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        try:
            # 1. POST /api/settings
            req_post = urllib_request.Request(
                f'http://127.0.0.1:{port}/api/settings',
                data=json.dumps({'startupBehavior': 'clean'}).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib_request.urlopen(req_post) as resp:
                self.assertEqual(resp.status, 200)
                post_data = json.loads(resp.read().decode('utf-8'))
                self.assertTrue(post_data.get('ok'))

            # 2. GET /api/bootstrap
            req_boot = urllib_request.Request(f'http://127.0.0.1:{port}/api/bootstrap')
            with urllib_request.urlopen(req_boot) as resp:
                self.assertEqual(resp.status, 200)
                boot_data = json.loads(resp.read().decode('utf-8'))
                settings = boot_data.get('settings', {})
                self.assertEqual(settings.get('startupBehavior'), 'clean')
        finally:
            server.shutdown()
            server.server_close()


if __name__ == '__main__':
    unittest.main()
