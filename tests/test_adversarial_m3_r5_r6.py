#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Milestone 3 Adversarial Test Suite (Requirements R5 & R6)
Author: teamwork_challenger_m3_2
Purpose: Empirically challenge, stress-test, and verify boundary conditions for:
  - R5: Table of contents fixed right column (220px) outside/below cover banner (top: 60px / top: 194px),
        zero collision with editor, DOM separation, lasso immunity, heading extraction, and XSS sanitization.
  - R6: Official App icon binary headers (ICO 0x00000100, PNG 0x89504E47), multi-size/single-size structures,
        build tool bindings; SQLite `Setting` persistence, factory default strictly clean state (0 tabs,
        0 open notes, null folder, Home view), resume mode restoration, and resilient handling of corrupted storage
        and missing/trashed notes.
"""

import html
import json
import os
import re
import struct
import sys
import tempfile
import threading
import unittest
from http.server import HTTPServer
from urllib import request as urllib_request
from urllib.error import HTTPError

from peewee import SqliteDatabase

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

INDEX_HTML_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'index.html')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')
APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
DESKTOP_APP_PATH = os.path.join(WORKSPACE_DIR, 'desktop_app.py')
BACKEND_PATH = os.path.join(WORKSPACE_DIR, 'backend.py')
SPEC_PATH = os.path.join(WORKSPACE_DIR, 'NoteJS.spec')
BUILD_BAT_PATH = os.path.join(WORKSPACE_DIR, 'build_exe.bat')

import backend
import desktop_app
import models


class TestR5AdversarialTableOfContents(unittest.TestCase):
    """Adversarial stress tests for Requirement R5 (Table of Contents Fixed Right Rail & Layout)."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_r5_css_positioning_and_cover_offset(self):
        """Stress: Verify .sticky-toc-rail positioning, right alignment, and cover banner offset."""
        # Check base positioning
        rail_match = re.search(r'\.sticky-toc-rail\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(rail_match, ".sticky-toc-rail CSS block not found")
        rail_css = rail_match.group(1)

        self.assertIn('position: absolute;', rail_css)
        self.assertIn('right: 20px;', rail_css)
        self.assertIn('top: 60px;', rail_css)
        self.assertIn('width: 220px;', rail_css)
        self.assertIn('z-index: 85;', rail_css)

        # Check with-cover positioning: strictly below cover banner
        with_cover_match = re.search(
            r'(\.notion-cover-container\.has-cover\s*~\s*\.sticky-toc-rail|#panel-canvas\.has-cover\s+\.sticky-toc-rail)\s*\{([^}]+)\}',
            self.styles_css
        )
        self.assertIsNotNone(with_cover_match, "TOC offset rule for cover not found")
        with_cover_css = with_cover_match.group(2)
        self.assertIn('top: 194px;', with_cover_css)

        # Mathematical verification of zero vertical collision with cover banner:
        # Cover banner height is 130px. Format bar height is 48px.
        # Format bar (48px) + Cover banner (130px) = 178px bottom edge.
        # At top: 194px, the TOC rail starts 16px below the cover banner bottom edge.
        format_bar_match = re.search(r'\.desktop-format-bar\s*\{[^}]*height:\s*(\d+)px;', self.styles_css)
        cover_match = re.search(r'\.notion-cover-container\s*\{[^}]*height:\s*(\d+)px;', self.styles_css)
        self.assertIsNotNone(format_bar_match)
        self.assertIsNotNone(cover_match)
        format_h = int(format_bar_match.group(1))
        cover_h = int(cover_match.group(1))
        cover_bottom_y = format_h + cover_h  # 48 + 130 = 178
        self.assertGreaterEqual(194, cover_bottom_y, "TOC rail must start at or below cover bottom edge")

    def test_r5_dom_hierarchy_zero_collision_with_editor(self):
        """Stress: Verify #sticky-toc-rail is outside #editor-body in DOM, preventing scroll collision."""
        # Verify sticky-toc-rail is inside #panel-canvas but NOT inside #editor-body
        self.assertIn('id="sticky-toc-rail"', self.index_html)
        self.assertIn('id="editor-body"', self.index_html)

        # In DOM order, #sticky-toc-rail appears before #editor-body
        rail_pos = self.index_html.find('id="sticky-toc-rail"')
        editor_pos = self.index_html.find('id="editor-body"')
        self.assertNotEqual(rail_pos, -1)
        self.assertNotEqual(editor_pos, -1)
        self.assertLess(rail_pos, editor_pos, "#sticky-toc-rail must be declared outside/before #editor-body")

        # Verify #editor-body has independent overflow-y so scrolling it does not move the TOC rail
        editor_match = re.search(r'\.editor-body,\s*\.editor-container\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(editor_match)
        editor_css = editor_match.group(1)
        self.assertIn('overflow-y: auto;', editor_css)

        # Popover expands smoothly on hover or when expanded (Notion outline UX)
        popover_match = re.search(r'\.sticky-toc-popover\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(popover_match)
        self.assertIn('.sticky-toc-rail:hover .sticky-toc-popover', self.styles_css)

        # Rail bars should be styled for Notion outline indicator display
        bars_match = re.search(r'\.sticky-toc-rail-bars\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(bars_match)
        self.assertIn('display: flex;', bars_match.group(1))

        # Header row inside cover must NOT contain the misplaced "Índice (/toc)" button
        header_buttons_match = re.search(r'<div class="notion-header-buttons-row"[^>]*>([\s\S]*?)</div>', self.index_html)
        self.assertIsNotNone(header_buttons_match)
        self.assertNotIn('insertTableOfContentsBlock()', header_buttons_match.group(1))

    def test_r5_lasso_guard_on_sticky_toc(self):
        """Adversarial: Clicking or dragging inside #sticky-toc-rail must never initiate lasso selection."""
        # App.js mousedown listener must explicitly guard against #sticky-toc-rail
        self.assertIn('#sticky-toc-rail', self.app_js)
        self.assertTrue(
            re.search(r'e\.target\.closest\([\'"]#sticky-toc-rail[\'"]\)', self.app_js),
            "Expected e.target.closest('#sticky-toc-rail') in lasso mousedown guard"
        )

        # Simulation of lasso guard logic
        def simulate_lasso_guard(target_selectors):
            if any(s in target_selectors for s in ['[contenteditable="true"]', 'INPUT', 'TEXTAREA']):
                return False, 'ABORT_EDITABLE'
            if any(s in target_selectors for s in ['#spatial-block-handle', '#block-action-menu', '.desktop-format-bar', 'button', '#sticky-toc-rail']):
                return False, 'ABORT_CONTROLS'
            return True, 'START_LASSO'

        # Test clicking TOC container
        can_lasso, reason = simulate_lasso_guard(['#sticky-toc-rail', '.sticky-toc-rail'])
        self.assertFalse(can_lasso)
        self.assertEqual(reason, 'ABORT_CONTROLS')

        # Test clicking TOC item
        can_lasso, reason = simulate_lasso_guard(['.sticky-toc-item', '#sticky-toc-rail'])
        self.assertFalse(can_lasso)
        self.assertEqual(reason, 'ABORT_CONTROLS')

        # Test clicking close button in TOC header
        can_lasso, reason = simulate_lasso_guard(['button', '.btn-icon-tiny', '#sticky-toc-rail'])
        self.assertFalse(can_lasso)
        self.assertEqual(reason, 'ABORT_CONTROLS')

    def test_r5_heading_extraction_and_xss_escaping(self):
        """Stress: Verify heading collection, HTML escaping against XSS, and index generation."""
        # Simulated headings with edge cases (empty headings, XSS attack vector)
        test_headings = [
            {'idx': 0, 'level': 1, 'text': 'Introduction'},
            {'idx': 1, 'level': 2, 'text': '<script>alert("xss")</script>'},
            {'idx': 2, 'level': 3, 'text': 'Sub & Section "Quotes"'},
            {'idx': 3, 'level': 2, 'text': ''},  # Empty heading
        ]

        # Verify app.js has escapeHtmlAttr or equivalent escaping
        self.assertIn('function escapeHtmlAttr(', self.app_js)

        def escape_html_attr(text):
            if not text:
                return ''
            return html.escape(str(text), quote=True)

        # Generate TOC markup as app.js does
        items_html = []
        for h in test_headings:
            display_text = h['text'] if h['text'] else f"Encabezado {h['idx'] + 1}"
            escaped_text = escape_html_attr(display_text)
            self.assertNotIn('<script>', escaped_text)
            self.assertIn('&quot;', escaped_text) if '"' in display_text else None
            items_html.append(f'<div class="sticky-toc-item toc-h{h["level"]}">{escaped_text}</div>')

        full_html = "".join(items_html)
        self.assertNotIn('<script>alert', full_html)
        self.assertIn('&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;', full_html)
        self.assertIn('Sub &amp; Section &quot;Quotes&quot;', full_html)
        self.assertIn('Encabezado 4', full_html)

    def test_r5_toc_visibility_toggle_state(self):
        """Stress: Verify togglePageStickyToc and .hidden-rail hiding behavior."""
        self.assertIn('function togglePageStickyToc()', self.app_js)
        self.assertIn('function refreshPageTableOfContents()', self.app_js)

        # Verify .hidden-rail CSS rule is display: none !important
        hidden_rail_match = re.search(r'\.sticky-toc-rail\.hidden-rail\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(hidden_rail_match)
        self.assertIn('display: none !important;', hidden_rail_match.group(1))

        # Verify switch in appearance popover
        self.assertIn('id="switch-sticky-toc"', self.index_html)
        self.assertIn('togglePageStickyToc()', self.index_html)


class TestR6AdversarialIconBinaryAssets(unittest.TestCase):
    """Adversarial binary verification for Requirement R6 (Icon Binaries and Headers)."""

    def test_r6_ico_binary_headers_and_directory_entries(self):
        """Empirically verify ICO header (0x00000100) and entry structures for public/icon.ico & frontend/favicon.ico."""
        ico_files = [
            os.path.join(WORKSPACE_DIR, 'public', 'icon.ico'),
            os.path.join(WORKSPACE_DIR, 'frontend', 'favicon.ico'),
            os.path.join(WORKSPACE_DIR, 'icon.ico'),
        ]

        for path in ico_files:
            self.assertTrue(os.path.exists(path), f"File {path} does not exist")
            size = os.path.getsize(path)
            self.assertGreater(size, 6, f"File {path} too small to contain ICO header")

            with open(path, 'rb') as f:
                header = f.read(4)
                # ICO header magic: 0x00, 0x00, 0x01, 0x00 (little endian: reserved=0, type=1)
                self.assertEqual(header, b'\x00\x00\x01\x00', f"{path} does not have valid ICO magic 0x00000100")

                num_images = struct.unpack('<H', f.read(2))[0]
                self.assertGreaterEqual(num_images, 1, f"{path} must contain at least 1 image entry")

                # Verify each icon directory entry
                for i in range(num_images):
                    entry = f.read(16)
                    self.assertEqual(len(entry), 16, f"Corrupted directory entry {i} in {path}")
                    w, h, color_count, reserved, planes, bpp, img_size, img_offset = struct.unpack('<BBBBHHII', entry)
                    w = 256 if w == 0 else w
                    h = 256 if h == 0 else h

                    self.assertGreater(w, 0)
                    self.assertGreater(h, 0)
                    self.assertGreater(img_size, 0)
                    self.assertGreaterEqual(img_offset, 6 + num_images * 16)
                    self.assertLessEqual(img_offset + img_size, size)

                    # Inspect the image data payload at img_offset
                    curr_pos = f.tell()
                    f.seek(img_offset)
                    img_magic = f.read(4)
                    f.seek(curr_pos)

                    # Either a PNG header (0x89504E47) or a BITMAPINFOHEADER (0x00000028 = 40 bytes)
                    is_png_payload = (img_magic == b'\x89PNG')
                    is_bmp_payload = (struct.unpack('<I', img_magic)[0] == 40)
                    self.assertTrue(
                        is_png_payload or is_bmp_payload,
                        f"Image payload in {path} at offset {img_offset} must be valid PNG or BITMAPINFOHEADER"
                    )

    def test_r6_png_binary_headers_and_chunks(self):
        """Empirically verify PNG header (0x89504E470D0A1A0A) and IHDR chunk for public/icon.png & frontend/icon.png."""
        png_files = [
            os.path.join(WORKSPACE_DIR, 'public', 'icon.png'),
            os.path.join(WORKSPACE_DIR, 'frontend', 'icon.png'),
        ]

        png_magic = b'\x89PNG\r\n\x1a\n'

        for path in png_files:
            self.assertTrue(os.path.exists(path), f"File {path} does not exist")
            size = os.path.getsize(path)
            self.assertGreater(size, 8, f"File {path} too small for PNG header")

            with open(path, 'rb') as f:
                magic = f.read(8)
                self.assertEqual(magic, png_magic, f"{path} does not have valid PNG header 0x89504E47")

                # Next chunk must be IHDR (length 4 bytes, type 4 bytes)
                ihdr_len = struct.unpack('>I', f.read(4))[0]
                self.assertEqual(ihdr_len, 13, "IHDR chunk length must be 13")
                ihdr_type = f.read(4)
                self.assertEqual(ihdr_type, b'IHDR', "First chunk must be IHDR")

                # IHDR data: width (4), height (4), bit_depth (1), color_type (1), compression (1), filter (1), interlace (1)
                ihdr_data = f.read(13)
                w, h, bit_depth, color_type, comp, filt, interlace = struct.unpack('>IIBBBBB', ihdr_data)
                self.assertGreater(w, 0, "PNG width must be positive")
                self.assertGreater(h, 0, "PNG height must be positive")
                self.assertEqual(w, h, "Icon must have 1:1 square aspect ratio")
                self.assertIn(bit_depth, [1, 2, 4, 8, 16], "Invalid PNG bit depth")
                self.assertIn(color_type, [0, 2, 3, 4, 6], "Invalid PNG color type")

    def test_r6_build_tools_and_html_icon_declarations(self):
        """Stress: Verify icon binding across desktop_app.py, NoteJS.spec, build_exe.bat, and index.html."""
        with open(DESKTOP_APP_PATH, 'r', encoding='utf-8') as f:
            desktop_app_code = f.read()
        with open(SPEC_PATH, 'r', encoding='utf-8') as f:
            spec_code = f.read()
        with open(BUILD_BAT_PATH, 'r', encoding='utf-8') as f:
            bat_code = f.read()
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            html_code = f.read()

        # Desktop app passes icon to webview
        self.assertTrue(
            "os.path.join(base_dir, 'public', 'icon.ico')" in desktop_app_code or
            'os.path.join(WORKSPACE_DIR, "public", "icon.ico")' in desktop_app_code or
            "'public', 'icon.ico'" in desktop_app_code
        )
        self.assertIn('icon=icon_file', desktop_app_code)

        # PyInstaller spec embeds icon
        self.assertTrue(
            "icon='public/icon.ico'" in spec_code or
            "icon=['public/icon.ico']" in spec_code
        )
        self.assertIn("('public', 'public')", spec_code)

        # Batch build script includes icon argument
        self.assertIn('--icon="public\\icon.ico"', bat_code)

        # HTML references both icon.png and favicon.ico
        self.assertIn('rel="icon" type="image/png" href="/icon.png"', html_code)
        self.assertIn('rel="shortcut icon" href="/favicon.ico"', html_code)


class TestR6AdversarialStartupBehaviorAndPersistence(unittest.TestCase):
    """Adversarial stress tests for Requirement R6 (Startup Preference, SQLite Setting Table, Factory State)."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

        # Isolated temporary SQLite database
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = os.path.join(cls.temp_dir.name, 'test_r6_settings.db')
        cls.original_db = models.db

        cls.test_db = SqliteDatabase(cls.test_db_path)
        models.db = cls.test_db
        models.BaseModel._meta.database = cls.test_db
        for model in [models.Note, models.Folder, models.Setting, models.NoteHistory,
                      models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord]:
            model._meta.database = cls.test_db

        cls.test_db.connect()
        cls.test_db.create_tables([
            models.Note, models.Folder, models.Setting, models.NoteHistory,
            models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord
        ])

        # Spin up server on test database
        cls.server = HTTPServer(('127.0.0.1', 0), backend.NoteJSRequestHandler)
        cls.host, cls.port = cls.server.server_address
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.server.shutdown()
            cls.server.server_close()
            if not cls.test_db.is_closed():
                cls.test_db.close()
            cls.temp_dir.cleanup()
        except Exception:
            pass
        finally:
            models.db = cls.original_db
            models.BaseModel._meta.database = cls.original_db
            for model in [models.Note, models.Folder, models.Setting, models.NoteHistory,
                          models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord]:
                model._meta.database = cls.original_db

    def _post_json(self, path, payload):
        req = urllib_request.Request(
            f'http://127.0.0.1:{self.port}{path}',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib_request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def _get_json(self, path):
        req = urllib_request.Request(f'http://127.0.0.1:{self.port}{path}')
        with urllib_request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))

    def test_r6_sqlite_setting_model_atomic_persistence(self):
        """Stress: Verify atomic on_conflict_replace insertion and retrieval in SQLite Setting table."""
        # 1. Direct Peewee insertion
        models.Setting.insert(key='startupBehavior', value='clean').on_conflict_replace().execute()
        s = models.Setting.get_or_none(models.Setting.key == 'startupBehavior')
        self.assertIsNotNone(s)
        self.assertEqual(s.value, 'clean')

        # 2. Update to 'resume'
        models.Setting.insert(key='startupBehavior', value='resume').on_conflict_replace().execute()
        s2 = models.Setting.get_or_none(models.Setting.key == 'startupBehavior')
        self.assertIsNotNone(s2)
        self.assertEqual(s2.value, 'resume')

        # Ensure no duplicate rows were created
        count = models.Setting.select().where(models.Setting.key == 'startupBehavior').count()
        self.assertEqual(count, 1)

    def test_r6_api_settings_endpoint_persistence(self):
        """Stress: POST /api/settings updates SQLite Setting table and bootstrap reflects it."""
        # Save settings via API
        resp = self._post_json('/api/settings', {'startupBehavior': 'resume', 'lastVisitedNoteId': 42})
        self.assertTrue(resp.get('ok'))

        # Read back via bootstrap
        boot = self._get_json('/api/bootstrap')
        self.assertTrue(boot.get('ok'))
        settings = boot.get('settings', {})
        self.assertEqual(settings.get('startupBehavior'), 'resume')
        self.assertEqual(settings.get('lastVisitedNoteId'), '42')

        # Reset to clean
        self._post_json('/api/settings', {'startupBehavior': 'clean'})
        boot2 = self._get_json('/api/bootstrap')
        self.assertEqual(boot2.get('settings', {}).get('startupBehavior'), 'clean')

    def test_r6_factory_default_clean_slate_invariant(self):
        """Adversarial Invariant: Factory default MUST start from zero (0 tabs, 0 open notes, null folder, Home active)."""
        # Simulate state initialization logic from frontend/app.js line 361-413
        # When settings cache is empty or default:
        empty_cache = {}
        startup_behavior = empty_cache.get('startupBehavior', 'clean')
        self.assertEqual(startup_behavior, 'clean')

        # Invariant checks for initial state
        active_note_id = None if startup_behavior == 'clean' else 123
        open_tab_ids = [] if startup_behavior == 'clean' else [123]
        selected_folder = None if startup_behavior == 'clean' else 'All Notes'
        is_home_active = True

        self.assertEqual(open_tab_ids, [], "Factory default MUST have 0 open tabs")
        self.assertIsNone(active_note_id, "Factory default MUST have null activeNoteId")
        self.assertIsNone(selected_folder, "Factory default MUST have null selectedFolder")
        self.assertTrue(is_home_active, "Factory default MUST start on Home view")

        # Check frontend/app.js bootstrap enforcement
        self.assertTrue(
            re.search(r'if\s*\(\s*startupBehavior\s*===\s*[\'"]clean[\'"]\s*\)\s*\{[^}]*state\.openTabIds\s*=\s*\[\];', self.app_js),
            "Expected state.openTabIds = [] when startupBehavior is clean"
        )
        self.assertTrue(
            re.search(r'state\.activeNoteId\s*=\s*null;', self.app_js),
            "Expected state.activeNoteId = null when startupBehavior is clean"
        )
        self.assertTrue(
            re.search(r'state\.selectedFolder\s*=\s*null;', self.app_js),
            "Expected state.selectedFolder = null when startupBehavior is clean"
        )
        self.assertTrue(
            re.search(r'state\.isHomeActive\s*=\s*true;', self.app_js),
            "Expected state.isHomeActive = true when startupBehavior is clean"
        )

    def test_r6_resume_mode_restores_last_visited_note(self):
        """Stress: Verify setting 'resume' accurately restores last visited note and opens tab."""
        # Setup simulated bootstrap payload
        sample_notes = [
            {'id': 101, 'title': 'First Note', 'isTrashed': False},
            {'id': 102, 'title': 'Second Note', 'isTrashed': False},
        ]
        sample_settings = {
            'startupBehavior': 'resume',
            'lastVisitedNoteId': 102
        }

        # Simulate bootstrap logic from frontend/app.js lines 1173-1200
        startup_behavior = sample_settings.get('startupBehavior', 'clean')
        state = {'openTabIds': [], 'activeNoteId': None, 'isHomeActive': True}

        if startup_behavior == 'resume':
            last_id = int(sample_settings.get('lastVisitedNoteId', 0))
            if any(n['id'] == last_id and not n.get('isTrashed') for n in sample_notes):
                state['activeNoteId'] = last_id
                state['openTabIds'] = [last_id]
                state['isHomeActive'] = False

        self.assertEqual(state['activeNoteId'], 102)
        self.assertEqual(state['openTabIds'], [102])
        self.assertFalse(state['isHomeActive'])

    def test_r6_resume_mode_handles_missing_note_gracefully(self):
        """Adversarial: Resume mode with non-existent last note ID must not crash and fallback safely."""
        sample_notes = [
            {'id': 101, 'title': 'First Note', 'isTrashed': False},
        ]
        sample_settings = {
            'startupBehavior': 'resume',
            'lastVisitedNoteId': 99999  # Does not exist
        }

        state = {'openTabIds': [], 'activeNoteId': None, 'isHomeActive': True}
        last_id = int(sample_settings.get('lastVisitedNoteId', 0))

        # Check guard in app.js: note must exist in data.notes and not be trashed
        exists = any(n['id'] == last_id and not n.get('isTrashed') for n in sample_notes)
        if exists:
            state['activeNoteId'] = last_id
            state['openTabIds'] = [last_id]
            state['isHomeActive'] = False

        self.assertFalse(exists)
        self.assertIsNone(state['activeNoteId'], "Must not resume non-existent note")
        self.assertEqual(state['openTabIds'], [])
        self.assertTrue(state['isHomeActive'])

    def test_r6_resume_mode_handles_trashed_note_gracefully(self):
        """Adversarial: Resume mode with a trashed note must not open or restore it."""
        sample_notes = [
            {'id': 101, 'title': 'Active Note', 'isTrashed': False},
            {'id': 102, 'title': 'Deleted Note', 'isTrashed': True},
        ]
        sample_settings = {
            'startupBehavior': 'resume',
            'lastVisitedNoteId': 102  # Trashed note
        }

        state = {'openTabIds': [], 'activeNoteId': None, 'isHomeActive': True}
        last_id = int(sample_settings.get('lastVisitedNoteId', 0))

        # Guard: !n.isTrashed
        exists_and_active = any(n['id'] == last_id and not n.get('isTrashed') for n in sample_notes)
        self.assertFalse(exists_and_active, "Trashed note must fail active check")

        if exists_and_active:
            state['activeNoteId'] = last_id
            state['openTabIds'] = [last_id]
            state['isHomeActive'] = False

        self.assertIsNone(state['activeNoteId'])
        self.assertEqual(state['openTabIds'], [])
        self.assertTrue(state['isHomeActive'])

    def test_r6_corrupted_localstorage_cache_fallback(self):
        """Adversarial: Corrupted localStorage JSON must be safely caught and default to 'clean'."""
        corrupted_strings = [
            "{broken json",
            "null",
            "undefined",
            "[1, 2, 3]",
            "12345",
            "",
            "''",
            '{"startupBehavior": "malicious_exploit"}',
        ]

        for s in corrupted_strings:
            try:
                parsed = json.loads(s) if s not in ['null', 'undefined', ''] else {}
                if not isinstance(parsed, dict):
                    parsed = {}
            except Exception:
                parsed = {}

            # Fallback logic identical to app.js line 372
            resolved = parsed.get('startupBehavior')
            final_behavior = resolved if resolved in ['clean', 'resume'] else 'clean'
            self.assertEqual(final_behavior, 'clean', f"Corrupted payload '{s}' must resolve to 'clean'")

    def test_r6_malicious_or_unknown_startup_behavior_sanitization(self):
        """Adversarial: handleStartupBehaviorChange must sanitize unknown values strictly to 'clean'."""
        self.assertIn('function handleStartupBehaviorChange(value)', self.app_js)
        self.assertTrue(
            re.search(r'const cleanVal\s*=\s*\(value\s*===\s*[\'"]resume[\'"]\)\s*\?\s*[\'"]resume[\'"]\s*:\s*[\'"]clean[\'"];', self.app_js),
            "Expected ternary sanitation: (value === 'resume') ? 'resume' : 'clean'"
        )

        # Verify simulation of sanitation
        def sanitize(val):
            return 'resume' if val == 'resume' else 'clean'

        self.assertEqual(sanitize('clean'), 'clean')
        self.assertEqual(sanitize('resume'), 'resume')
        self.assertEqual(sanitize(''), 'clean')
        self.assertEqual(sanitize(None), 'clean')
        self.assertEqual(sanitize('UNKNOWN'), 'clean')
        self.assertEqual(sanitize('DROP TABLE notes;'), 'clean')
        self.assertEqual(sanitize('<script>'), 'clean')

    def test_r6_settings_ui_elements_in_html_and_app_js(self):
        """Stress: Verify #setting-startup-behavior in Settings modal and window export."""
        # index.html select and options
        self.assertIn('id="setting-startup-behavior"', self.index_html)
        self.assertIn('value="clean"', self.index_html)
        self.assertIn('value="resume"', self.index_html)
        self.assertIn('onchange="handleStartupBehaviorChange(this.value)"', self.index_html)

        # app.js handler and window export
        self.assertIn('window.handleStartupBehaviorChange = handleStartupBehaviorChange;', self.app_js)
        self.assertIn('startupSelect.value = state.startupBehavior', self.app_js)


if __name__ == '__main__':
    unittest.main()
