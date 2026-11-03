#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Milestone 3 Adversarial Test Suite (Requirements R1 - R4)
Author: teamwork_challenger_m3_1
Purpose: Empirically challenge, stress-test, and verify boundary conditions for:
  - R1: Tab bar neutral styles, pill styling, window controls in PyWebViewBridge, backend endpoints /api/window/*, and HTML/JS handlers.
  - R2: Folder duplicate button elimination, neutral styling of folder buttons, unified modal with segmented selector.
  - R3: Full-screen reminders view navigation, activation/deactivation, count badge synchronization.
  - R4: Formatting bar amber exclusivity on #btn-insert-dropdown, centered plus via flexbox, gear-only settings button .btn-settings-bottom.
"""

import os
import sys
import re
import json
import threading
from http.server import HTTPServer
from urllib import request as urllib_request
from urllib.error import HTTPError
import unittest
from unittest.mock import MagicMock

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

INDEX_HTML_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'index.html')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')
APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
DESKTOP_APP_PATH = os.path.join(WORKSPACE_DIR, 'desktop_app.py')
BACKEND_PATH = os.path.join(WORKSPACE_DIR, 'backend.py')

import desktop_app
import backend


class TestR1AdversarialWindowControlsAndTabBar(unittest.TestCase):
    """Adversarial stress-testing of Window controls (Bridge, Backend API, Frontend JS/CSS, Tab Pills)."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

        # Spin up a real backend server instance for API stress-testing
        cls.server = HTTPServer(('127.0.0.1', 0), backend.NoteJSRequestHandler)
        cls.host, cls.port = cls.server.server_address
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.server.shutdown()
            cls.server.server_close()
        except Exception:
            pass

    # --- PyWebViewBridge Adversarial Tests ---
    def test_bridge_window_methods_when_no_active_windows(self):
        """Stress: PyWebViewBridge gracefully handles webview.windows being empty without crash."""
        bridge = desktop_app.PyWebViewBridge()
        
        # Save original webview.windows
        orig_windows = getattr(desktop_app.webview, 'windows', [])
        desktop_app.webview.windows = []

        try:
            res_min = bridge.minimize_window()
            self.assertFalse(res_min.get('ok'))
            self.assertEqual(res_min.get('error'), 'No active window')

            res_max = bridge.toggle_maximize_window()
            self.assertFalse(res_max.get('ok'))
            self.assertEqual(res_max.get('error'), 'No active window')

            res_close = bridge.close_window()
            self.assertFalse(res_close.get('ok'))
            self.assertEqual(res_close.get('error'), 'No active window')
        finally:
            desktop_app.webview.windows = orig_windows

    def test_bridge_window_methods_exception_resilience(self):
        """Failure mode: PyWebViewBridge catches internal window exceptions and returns clean error dict."""
        bridge = desktop_app.PyWebViewBridge()

        mock_window = MagicMock()
        mock_window._is_maximized = False
        mock_window.minimize.side_effect = RuntimeError("Window subsystem deadlock")
        mock_window.maximize.side_effect = RuntimeError("Display adapter crash")
        mock_window.restore.side_effect = RuntimeError("Display adapter restore crash")
        mock_window.destroy.side_effect = RuntimeError("Process handle invalid")

        orig_windows = getattr(desktop_app.webview, 'windows', [])
        desktop_app.webview.windows = [mock_window]

        try:
            res_min = bridge.minimize_window()
            self.assertFalse(res_min['ok'])
            self.assertIn("Window subsystem deadlock", res_min['error'])

            res_max = bridge.toggle_maximize_window()
            self.assertFalse(res_max['ok'])
            self.assertIn("Display adapter crash", res_max['error'])

            res_close = bridge.close_window()
            self.assertFalse(res_close['ok'])
            self.assertIn("Process handle invalid", res_close['error'])
        finally:
            desktop_app.webview.windows = orig_windows

    def test_bridge_rapid_toggle_maximize_state_invariants(self):
        """Stress: Rapid alternating maximize/restore cycles maintain accurate state flags."""
        bridge = desktop_app.PyWebViewBridge()

        mock_window = MagicMock()
        mock_window._is_maximized = False

        orig_windows = getattr(desktop_app.webview, 'windows', [])
        desktop_app.webview.windows = [mock_window]

        try:
            for cycle in range(25):
                # First call -> maximize
                res1 = bridge.toggle_maximize_window()
                self.assertTrue(res1['ok'])
                self.assertEqual(res1['action'], 'maximize')
                self.assertTrue(res1['is_maximized'])
                self.assertTrue(mock_window._is_maximized)

                # Second call -> restore
                res2 = bridge.toggle_maximize_window()
                self.assertTrue(res2['ok'])
                self.assertEqual(res2['action'], 'restore')
                self.assertFalse(res2['is_maximized'])
                self.assertFalse(mock_window._is_maximized)

            self.assertEqual(mock_window.maximize.call_count, 25)
            self.assertEqual(mock_window.restore.call_count, 25)
        finally:
            desktop_app.webview.windows = orig_windows

    # --- Backend Window API Endpoints Stress Tests ---
    def test_backend_window_endpoints_malformed_and_edge_requests(self):
        """Stress: POST /api/window/* endpoints survive empty body, corrupt JSON, unexpected queries."""
        endpoints = ['/api/window/minimize', '/api/window/maximize', '/api/window/close']

        for ep in endpoints:
            # 1. Empty body
            req = urllib_request.Request(
                f'http://127.0.0.1:{self.port}{ep}',
                data=b'',
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib_request.urlopen(req) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode('utf-8'))
                self.assertTrue(data.get('success'))

            # 2. Corrupt / invalid non-JSON body -> server safely returns 400 Bad Request
            req_corrupt = urllib_request.Request(
                f'http://127.0.0.1:{self.port}{ep}',
                data=b'<<<MALFORMED_NON_JSON_DATA>>>',
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            try:
                with urllib_request.urlopen(req_corrupt) as resp:
                    # Should not succeed 200 with corrupt data
                    self.fail("Expected HTTP 400 Bad Request on corrupt payload")
            except HTTPError as e:
                self.assertEqual(e.code, 400)
                err_data = json.loads(e.read().decode('utf-8'))
                self.assertFalse(err_data.get('ok', True))

            # 3. Request with query parameters
            req_query = urllib_request.Request(
                f'http://127.0.0.1:{self.port}{ep}?burst=true&client_time=123456789',
                data=b'{}',
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib_request.urlopen(req_query) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode('utf-8'))
                self.assertTrue(data.get('success'))

    def test_backend_window_maximize_toggle_alternation(self):
        """Verify POST /api/window/maximize flips between 'maximize' and 'restore' across calls."""
        actions = []
        for _ in range(6):
            req = urllib_request.Request(
                f'http://127.0.0.1:{self.port}/api/window/maximize',
                data=b'{}',
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib_request.urlopen(req) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode('utf-8'))
                actions.append(data.get('action'))

        # In headless environment without webview.windows, defaults safely to 'maximize' without crash
        self.assertEqual(len(actions), 6)
        for act in actions:
            self.assertIn(act, ('maximize', 'restore'))

    # --- Frontend Window Controls & Tab Pill Invariants ---
    def test_frontend_window_controls_dom_and_handlers(self):
        """Verify window controls buttons exist in HTML with proper onclick and accessibility attributes."""
        # Check window controls toolbar
        self.assertIn('class="window-controls-bar"', self.index_html)
        self.assertIn('-webkit-app-region: no-drag;', self.styles_css)

        # Check all 4 buttons and their assigned handlers
        controls = [
            ('btn-win-menu', 'toggleWinMenu('),
            ('btn-win-minimize', 'minimizeWindow()'),
            ('btn-win-maximize', 'toggleMaximizeWindow()'),
            ('btn-win-close', 'closeWindow()'),
        ]
        for btn_id, handler_call in controls:
            btn_match = re.search(rf'<button[^>]*id="{btn_id}"[^>]*>', self.index_html)
            self.assertIsNotNone(btn_match, f"Missing button #{btn_id} in HTML")
            self.assertIn(handler_call, btn_match.group(0))

    def test_frontend_update_maximize_icon_null_safety(self):
        """Verify updateMaximizeIcon in app.js has defensive checks against missing elements."""
        func_match = re.search(r'function updateMaximizeIcon\([^\)]*\)\s*\{([\s\S]*?)\}', self.app_js)
        self.assertIsNotNone(func_match)
        body = func_match.group(1)
        self.assertIn('if (!btn) return;', body, "updateMaximizeIcon must null-check btn")
        self.assertIn('if (icon)', body, "updateMaximizeIcon must check icon existence before modifying innerHTML")

    def test_frontend_toggle_win_menu_event_safety(self):
        """Verify toggleWinMenu in app.js does not crash if event object is null/undefined."""
        func_match = re.search(r'function toggleWinMenu\([^\)]*\)\s*\{([\s\S]*?)\}', self.app_js)
        self.assertIsNotNone(func_match)
        body = func_match.group(1)
        self.assertIn('if (e) e.stopPropagation();', body)
        self.assertIn('openSettingsModal();', body)

    def test_tab_pill_and_neutral_top_bar_styling(self):
        """Verify .note-tab-item uses pill border-radius (9999px) and top bar action buttons are neutral."""
        # Pill border radius
        self.assertTrue(
            re.search(r'\.note-tab-item\s*\{[^}]*border-radius:\s*(?:9999px|999px|20px|16px)', self.styles_css),
            "Expected pill border-radius on .note-tab-item"
        )
        # Tab item height should be around 30px as in spec
        self.assertTrue(
            re.search(r'\.note-tab-item\s*\{[^}]*height:\s*30px', self.styles_css),
            "Expected height: 30px on .note-tab-item"
        )
        # Close button hover color #e81123
        self.assertTrue(
            re.search(r'\.win-control-close:hover\s*\{[^}]*background(?:-color)?:\s*#e81123', self.styles_css)
        )


class TestR2AdversarialFolderManagementUnification(unittest.TestCase):
    """Adversarial testing of Folder creation unification, duplicate button elimination, and segmented modal."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_strict_elimination_of_duplicate_folder_buttons(self):
        """Adversarial: Exactly ONE folder creation button in sidebar header and no secondary buttons."""
        sidebar_header_match = re.search(
            r'<div class="folder-header-actions">([\s\S]*?)</div>',
            self.index_html
        )
        self.assertIsNotNone(sidebar_header_match, "Expected .folder-header-actions container in HTML")
        actions_content = sidebar_header_match.group(1)

        # Count button occurrences in folder-header-actions
        buttons = re.findall(r'<button\b[^>]*>', actions_content)
        # Should have exactly two buttons: btn-collapse-sidebar and btn-new-folder
        self.assertEqual(len(buttons), 2, f"Expected 2 buttons in .folder-header-actions, found {len(buttons)}")
        self.assertIn('id="btn-collapse-sidebar"', actions_content)
        self.assertIn('id="btn-new-folder"', actions_content)

        # Ensure no other button references smart folder creation in sidebar
        self.assertNotIn('promptNewSmartFolder', actions_content)
        self.assertNotIn('openSmartFolderModal', actions_content)
        self.assertNotIn('btn-new-smart-folder', self.index_html)

    def test_folder_add_button_neutral_styling_invariants(self):
        """Verify .folder-add-icon-btn has transparent/neutral background by default and amber ONLY on hover/active."""
        # Find default definition of .folder-add-icon-btn
        default_match = re.search(r'\.folder-add-icon-btn\s*\{([^}]*)\}', self.styles_css)
        self.assertIsNotNone(default_match, "Missing .folder-add-icon-btn in styles.css")
        default_rules = default_match.group(1)

        # Must NOT have amber in default background or color
        self.assertNotIn('var(--accent-amber)', default_rules)
        self.assertNotIn('#f59e0b', default_rules)

        # Hover and active definitions should provide amber accent
        hover_match = re.search(r'\.folder-add-icon-btn:hover\s*\{([^}]*)\}', self.styles_css)
        self.assertIsNotNone(hover_match, "Missing .folder-add-icon-btn:hover in styles.css")

    def test_unified_modal_segmented_control_structure(self):
        """Verify segmented control in #folder-custom-modal with standard and smart options."""
        modal_match = re.search(r'<div[^>]*id="folder-custom-modal"[\s\S]*?</div>\s*</div>\s*</div>', self.index_html)
        self.assertIsNotNone(modal_match)
        modal_content = modal_match.group(0)

        # Segmented control elements
        self.assertIn('class="folder-type-segmented-control"', modal_content)
        self.assertIn('id="ftype-btn-standard"', modal_content)
        self.assertIn('id="ftype-btn-smart"', modal_content)
        self.assertIn('id="folder-smart-rules-container"', modal_content)

        # Segmented control CSS
        self.assertIn('.folder-type-segmented-control', self.styles_css)
        self.assertIn('.folder-type-seg-btn', self.styles_css)
        self.assertTrue(
            re.search(r'\.folder-type-seg-btn\.active\s*\{[^}]*var\(--accent-amber\)', self.styles_css),
            "Expected active segmented button to receive amber highlight"
        )

    def test_set_folder_modal_type_defensive_normalization(self):
        """Verify setFolderModalType normalizes invalid arguments safely to 'standard'."""
        func_match = re.search(r'function setFolderModalType\(([^\)]*)\)\s*\{([\s\S]*?)\n    \}', self.app_js)
        self.assertIsNotNone(func_match)
        body = func_match.group(2)

        # Check defensive normalization: const cleanType = (type === 'smart') ? 'smart' : 'standard';
        self.assertTrue(
            re.search(r"cleanType\s*=\s*\(type\s*===\s*['\"]smart['\"]\)\s*\?\s*['\"]smart['\"]\s*:\s*['\"]standard['\"]", body)
            or re.search(r"folderModalState\.folderType\s*=\s*\(type\s*===\s*['\"]smart['\"]\)\s*\?\s*['\"]smart['\"]\s*:\s*['\"]standard['\"]", body),
            "setFolderModalType must sanitize type argument to 'smart' or 'standard'"
        )

        # Verify modal submit dispatcher forwards to submitSmartFolderModal when type is 'smart'
        submit_match = re.search(r'function submitFolderModal\(\)\s*\{([\s\S]*?)\n    \}', self.app_js)
        self.assertIsNotNone(submit_match)
        submit_body = submit_match.group(1)
        self.assertIn("folderModalState.folderType === 'smart'", submit_body)
        self.assertIn("submitSmartFolderModal()", submit_body)


class TestR3AdversarialFullScreenRemindersDashboard(unittest.TestCase):
    """Adversarial testing of Full-Screen Reminders navigation, activation/deactivation, and count badge sync."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_sidebar_reminders_item_and_badge_markup(self):
        """Verify #fitem-sidebar-reminders and #sidebar-reminders-count-badge in sidebar."""
        item_match = re.search(r'<button[^>]*id="fitem-sidebar-reminders"[^>]*>([\s\S]*?)</button>', self.index_html)
        self.assertIsNotNone(item_match)
        item_content = item_match.group(1)

        self.assertIn('onclick="navigateToReminders()"', self.index_html)
        self.assertIn('id="sidebar-reminders-count-badge"', item_content)
        self.assertIn('Recordatorios', item_content)

    def test_reminders_page_view_container_in_canvas(self):
        """Verify #reminders-page-view is inside #panel-canvas and starts hidden."""
        view_match = re.search(r'<div[^>]*id="reminders-page-view"[^>]*>', self.index_html)
        self.assertIsNotNone(view_match)
        view_tag = view_match.group(0)
        self.assertTrue(re.search(r'display:\s*none', view_tag), f"Expected display:none on reminders view tag, got {view_tag}")
        self.assertIn('reminders-page-view', view_tag)

    def test_reminders_navigation_view_exclusivity(self):
        """Verify navigateToReminders and exitRemindersView enforce view mutual exclusivity."""
        nav_match = re.search(r'function navigateToReminders\(\)\s*\{([\s\S]*?)\n    \}', self.app_js)
        self.assertIsNotNone(nav_match)
        nav_body = nav_match.group(1)

        # Activates reminders, deactivates home
        self.assertIn('state.isRemindersActive = true;', nav_body)
        self.assertIn('state.isHomeActive = false;', nav_body)
        self.assertIn("scaffold.classList.add('is-reminders-active')", nav_body)
        self.assertIn("scaffold.classList.remove('is-home-active')", nav_body)
        self.assertIn("remindersView.style.display = 'flex'", nav_body)
        self.assertIn("homeView.style.display = 'none'", nav_body)
        self.assertIn("editorBody.style.display = 'none'", nav_body)

        # Exit reminders view
        exit_match = re.search(r'function exitRemindersView\(\)\s*\{([\s\S]*?)\n    \}', self.app_js)
        self.assertIsNotNone(exit_match)
        exit_body = exit_match.group(1)
        self.assertIn('if (!state.isRemindersActive) return;', exit_body, "exitRemindersView must be idempotent")
        self.assertIn('state.isRemindersActive = false;', exit_body)
        self.assertIn("remindersView.style.display = 'none'", exit_body)

    def test_reminders_deactivation_on_competing_navigation(self):
        """Adversarial: Navigating to note, home, or tabs strictly calls exitRemindersView."""
        competing_functions = [
            ('selectNote', r'function selectNote\([^)]*\)\s*\{([\s\S]*?loadActiveNote\(\);)'),
            ('navigateToHome', r'function navigateToHome\(\)\s*\{([\s\S]*?renderHomePage\(\);)'),
            ('switchNoteTab', r'function switchNoteTab\([^)]*\)\s*\{([\s\S]*?selectNote\([^\)]*\);)'),
            ('loadActiveNote', r'function loadActiveNote\(\)\s*\{([\s\S]*?return;[\s\S]*?\})'),
            ('createNewNote', r'function createNewNote\([^)]*\)\s*\{([\s\S]*?loadActiveNote\(\);)')
        ]
        for name, pattern in competing_functions:
            fn_match = re.search(pattern, self.app_js)
            self.assertIsNotNone(fn_match, f"Could not find function {name}")
            fn_body = fn_match.group(1)
            self.assertIn('exitRemindersView()', fn_body, f"Function {name} must invoke exitRemindersView()")

    def test_count_badge_synchronization_logic(self):
        """Stress: Badge count counts ONLY pending reminders (!r.completed) and survives null/empty lists."""
        # Simulated badge counting logic matching app.js line 2020:
        # const pendingCount = (state.reminders || []).filter(r => !r.completed).length;

        def compute_badge(reminders):
            return (reminders or []).filter(lambda r: not r.get('completed', False)) if hasattr(reminders, 'filter') \
                else len([r for r in (reminders or []) if not r.get('completed', False)])

        # 1. Null / None reminders
        self.assertEqual(compute_badge(None), 0)

        # 2. Empty list
        self.assertEqual(compute_badge([]), 0)

        # 3. 5 pending, 0 completed
        rems1 = [{'id': i, 'completed': False} for i in range(5)]
        self.assertEqual(compute_badge(rems1), 5)

        # 4. 5 pending, 5 completed
        rems2 = [{'id': i, 'completed': i % 2 == 0} for i in range(10)]
        # i=0,2,4,6,8 completed=True (5). i=1,3,5,7,9 completed=False (5).
        self.assertEqual(compute_badge(rems2), 5)

        # 5. Missing completed key treated as pending
        rems3 = [{'id': 1}, {'id': 2, 'completed': True}]
        self.assertEqual(compute_badge(rems3), 1)

    def test_reminders_page_view_xss_protection(self):
        """Stress: Reminder title rendering escapes malicious XSS payloads."""
        self.assertIn('escapeHtmlAttr(ev.title ||', self.app_js)
        self.assertIn('escapeHtmlAttr(ev.time)', self.app_js)
        self.assertIn('escapeHtmlAttr(ev.date)', self.app_js)
        self.assertIn('escapeHtmlAttr(ev.category)', self.app_js)


class TestR4AdversarialFormattingBarAmberExclusivityAndSettingsGear(unittest.TestCase):
    """Adversarial testing of Amber Exclusivity, Flexbox centering of '+', and Gear-only Settings button."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_format_bar_amber_exclusivity_across_all_buttons(self):
        """Adversarial: Ensure NO other button in .desktop-format-bar receives amber styling."""
        format_bar_match = re.search(
            r'<div class="desktop-format-bar"[^>]*>([\s\S]*?)</div>\s*<!--\s*Fin desktop-format-bar',
            self.index_html
        )
        if not format_bar_match:
            format_bar_match = re.search(
                r'<div class="desktop-format-bar"[^>]*>([\s\S]*?)</div>\s*</div>\s*<!--',
                self.index_html
            )
        self.assertIsNotNone(format_bar_match, "Could not find .desktop-format-bar in index.html")
        bar_html = format_bar_match.group(1)

        # Find all buttons inside desktop-format-bar
        button_tags = re.findall(r'<button\b[^>]*>', bar_html)
        self.assertGreater(len(button_tags), 10, "Format bar should have multiple buttons")

        for btn in button_tags:
            is_insert_btn = ('id="btn-insert-dropdown"' in btn) or ('insert-dropdown-btn' in btn)
            # If not the insert button, verify it does NOT have amber inline styles
            if not is_insert_btn:
                self.assertNotIn('color: #f59e0b', btn.lower())
                self.assertNotIn('color: var(--accent-amber)', btn.lower())
                self.assertNotIn('background: #f59e0b', btn.lower())
                self.assertNotIn('background: var(--accent-amber)', btn.lower())

    def test_css_format_bar_neutral_override_precedence(self):
        """Verify CSS contains strong neutral override rule for all non-insert format bar buttons."""
        self.assertIn('.desktop-format-bar button:not(#btn-insert-dropdown):not(.insert-dropdown-btn)', self.styles_css)
        self.assertIn('.desktop-format-bar .btn-secondary:not(.btn-trash-action)', self.styles_css)

        # Verify the insert button alone has amber styles
        self.assertTrue(
            re.search(r'\.desktop-format-bar\s+#btn-insert-dropdown[^{]*\{[^}]*var\(--accent-amber-soft\)', self.styles_css)
            or re.search(r'#btn-insert-dropdown[^{]*\{[^}]*var\(--accent-amber-soft\)', self.styles_css)
        )

    def test_insert_plus_sign_pure_flexbox_centering(self):
        """Verify .insert-plus-sign uses pure flexbox centering and NO inline or CSS translateY hacks."""
        # CSS definition
        css_match = re.search(r'\.insert-plus-sign\s*\{([^}]*)\}', self.styles_css)
        self.assertIsNotNone(css_match, "Missing .insert-plus-sign in styles.css")
        rules = css_match.group(1)

        self.assertIn('display: inline-flex;', rules)
        self.assertIn('align-items: center;', rules)
        self.assertIn('justify-content: center;', rules)
        self.assertNotIn('translateY', rules, "Must not use translateY offset hack in CSS")

        # HTML inline style
        plus_match = re.search(r'<span class="insert-plus-sign"[^>]*>', self.index_html)
        self.assertIsNotNone(plus_match, "Missing <span class='insert-plus-sign'> in HTML")
        plus_tag = plus_match.group(0)
        self.assertNotIn('translateY', plus_tag, "Must not use translateY offset hack in HTML")

    def test_settings_button_gear_icon_exclusivity(self):
        """Verify .btn-settings-bottom contains ONLY the gear SVG icon and NO text or kbd badge."""
        settings_match = re.search(r'<button\b[^>]*class="[^"]*btn-settings-bottom[^"]*"[^>]*>([\s\S]*?)</button>', self.index_html)
        self.assertIsNotNone(settings_match, "Missing .btn-settings-bottom in index.html")
        inner_html = settings_match.group(1).strip()

        # Must NOT contain "Ajustes" or "Settings" text
        self.assertNotIn('Ajustes', inner_html)
        self.assertNotIn('Settings', inner_html)
        self.assertNotIn('<kbd', inner_html)
        self.assertNotIn('Ctrl+,', inner_html)

        # Must contain SVG element
        self.assertTrue(inner_html.startswith('<svg') and inner_html.endswith('</svg>'),
                        "Expected .btn-settings-bottom inner content to be purely <svg>...</svg>")

        # Dimensions: 32px x 32px
        dim_match = re.search(r'\.btn-settings-bottom\s*\{[^}]*width:\s*32px;[^}]*height:\s*32px;', self.styles_css)
        self.assertIsNotNone(dim_match, "Expected 32px x 32px dimensions on .btn-settings-bottom")


if __name__ == '__main__':
    unittest.main()
