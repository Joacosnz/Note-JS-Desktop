#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adversarial Stress Test Suite - Empirical Challenger Verification
Validates:
1. R2 Backend SQLite Persistence:
   - Extremely long titles (10,000+ characters)
   - Special characters, SQL injection syntax, XSS payloads, whitespace, newlines, null chars
   - Unicode, CJK, RTL, and complex composite emojis
   - Missing attributes, null values, type variations (int/str page_id, pageId vs page_id)
   - Batch moves with mixed blocks and property preservation
   - High density subpages per note (100 subpages)
   - Re-sync idempotence and state isolation
2. R1 Frontend Selection Conflict:
   - Event target resolution simulation for deeply nested editable elements
   - Input and Textarea event resolution
   - Empty canvas, editor container margins, and non-editable block resolution
   - Marquee activation rules validation
3. R4 Formatting Bar Amber Exclusivity & Focus Mode Removal:
   - AST / regex audit of styles.css for amber styling on all toolbar buttons
   - Zero occurrences of #focus-mode-indicator or 'Modo concentración' in DOM elements and styles
   - CSS cascade specificity check exposing whether line 9749 overrides scoped formatting bar rules
"""

import os
import re
import sys
import json
import time
import shutil
import tempfile
import unittest
from html.parser import HTMLParser

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WORKSPACE_DIR)

import models
from peewee import SqliteDatabase


class TestAdversarialBackendSubpagePersistence(unittest.TestCase):
    """Adversarial stress testing for Backend SQLite persistence of sub_page blocks."""

    def setUp(self):
        # Create a fresh isolated test database
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, 'test_adversarial.db')
        self.test_db = SqliteDatabase(self.db_path)

        # Patch models.db and bind
        self.original_db = models.db
        models.db = self.test_db
        models.Block._meta.database = self.test_db
        models.Note._meta.database = self.test_db

        self.test_db.connect()
        self.test_db.create_tables([models.Note, models.Block], safe=True)

        # Create a base note
        self.base_note = models.Note.create(
            id=1001,
            title="Adversarial Test Note",
            folder="Work",
            category="Work",
            pinned=0,
            is_trashed=0,
            has_cover=0,
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000)
        )

    def tearDown(self):
        if not self.test_db.is_closed():
            self.test_db.close()
        models.db = self.original_db
        models.Block._meta.database = self.original_db
        models.Note._meta.database = self.original_db
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_subpage_extremely_long_title(self):
        """Stress test: 10,000 character title in sub_page block."""
        long_title = "A" * 10000
        payload = [{
            "type": "sub_page",
            "id": "blk-long-title",
            "page_id": "target-note-999",
            "title": long_title
        }]
        res = models.sync_blocks_from_note_html_orm(self.base_note.id, payload)
        self.assertTrue(res.get('ok'), f"Sync failed: {res}")

        # Retrieve and verify
        blk = models.Block.get_or_none(models.Block.id == "blk-long-title")
        self.assertIsNotNone(blk)
        data = blk.to_dict()
        self.assertEqual(data['type'], 'sub_page')
        self.assertEqual(data['page_id'], 'target-note-999')
        self.assertEqual(data['title'], long_title)
        self.assertEqual(len(data['title']), 10000)

    def test_subpage_special_characters_sql_injection_and_xss(self):
        """Adversarial input: SQL injection syntax, quotes, slashes, HTML/script tags."""
        malicious_inputs = [
            "'; DROP TABLE blocks; --",
            "\" OR \"1\"=\"1",
            "<script>alert('XSS')</script>",
            "Title with \\ and / and \n and \r\n and \t and \0 null",
            "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?`~",
            "JSON payload: {\"evil\": true, \"null\": null, \"list\": [1,2,3]}"
        ]
        payload = []
        for idx, title_sample in enumerate(malicious_inputs):
            payload.append({
                "type": "sub_page",
                "id": f"blk-vuln-{idx}",
                "page_id": f"page-{idx}",
                "title": title_sample
            })

        res = models.sync_blocks_from_note_html_orm(self.base_note.id, payload)
        self.assertTrue(res.get('ok'))

        # Verify all survived with exact character integrity
        for idx, expected_title in enumerate(malicious_inputs):
            blk = models.Block.get(models.Block.id == f"blk-vuln-{idx}")
            data = blk.to_dict()
            self.assertEqual(data['type'], 'sub_page')
            self.assertEqual(data['page_id'], f"page-{idx}")
            self.assertEqual(data['title'], expected_title)

    def test_subpage_unicode_cjk_rtl_and_complex_emojis(self):
        """Adversarial input: Multi-byte UTF-8 characters, CJK, Arabic, Hebrew, and composite emojis."""
        unicode_titles = [
            "中文标题测试 — 高级笔记",
            "日本語のサブページタイトルです",
            "한국어 서브페이지 제목 테스트",
            "عنوان الصفحة الفرعية باللغة العربية",
            "כותרת דף משנה בעברית",
            "Complex Emojis: 👨‍👩‍👧‍👦 🏳️‍🌈 🦀 📄 🚀 💻 📝",
            "Accents: áéíóú, àèìòù, äëïöü, âêîôû, ñ, ç, ß"
        ]
        payload = [
            {
                "type": "sub_page",
                "id": f"blk-uni-{i}",
                "page_id": f"uni-page-{i}",
                "title": title
            }
            for i, title in enumerate(unicode_titles)
        ]
        res = models.sync_blocks_from_note_html_orm(self.base_note.id, payload)
        self.assertTrue(res.get('ok'))

        for i, expected_title in enumerate(unicode_titles):
            blk = models.Block.get(models.Block.id == f"blk-uni-{i}")
            data = blk.to_dict()
            self.assertEqual(data['title'], expected_title)

    def test_subpage_missing_attributes_and_type_coercion(self):
        """Edge cases: missing page_id, missing title, null values, integer page_id, alternative 'pageId' key."""
        edge_cases = [
            # 1. Missing page_id
            ({"type": "sub_page", "id": "blk-edge-1", "title": "No page_id"}, None, "No page_id"),
            # 2. Missing title
            ({"type": "sub_page", "id": "blk-edge-2", "page_id": "page-2"}, "page-2", ""),
            # 3. None for both
            ({"type": "sub_page", "id": "blk-edge-3", "page_id": None, "title": None}, None, ""),
            # 4. Integer page_id
            ({"type": "sub_page", "id": "blk-edge-4", "page_id": 4242, "title": "Integer ID"}, 4242, "Integer ID"),
            # 5. Alternative camelCase pageId
            ({"type": "sub_page", "id": "blk-edge-5", "pageId": "camel-page", "title": "Camel Case"}, "camel-page", "Camel Case"),
            # 6. Completely empty attributes
            ({"type": "sub_page", "id": "blk-edge-6"}, None, "")
        ]

        payload = [case[0] for case in edge_cases]
        res = models.sync_blocks_from_note_html_orm(self.base_note.id, payload)
        self.assertTrue(res.get('ok'))

        for case, exp_page_id, exp_title in edge_cases:
            blk = models.Block.get(models.Block.id == case["id"])
            data = blk.to_dict()
            self.assertEqual(data['type'], 'sub_page')
            self.assertEqual(data.get('page_id'), exp_page_id)
            self.assertEqual(data.get('title'), exp_title)

    def test_subpage_batch_moves_and_reordering(self):
        """Stress test: update_batch_blocks_order_orm with interleaved subpages and standard blocks."""
        # Initial setup: 5 blocks
        initial_blocks = [
            {"id": "blk-p1", "type": "p", "properties": {"text": "Intro paragraph"}},
            {"id": "blk-sub1", "type": "sub_page", "page_id": "p-10", "title": "Subpage 1"},
            {"id": "blk-p2", "type": "p", "properties": {"text": "Middle paragraph"}},
            {"id": "blk-sub2", "type": "sub_page", "page_id": "p-20", "title": "Subpage 2"},
            {"id": "blk-p3", "type": "p", "properties": {"text": "Ending paragraph"}}
        ]
        models.sync_blocks_from_note_html_orm(self.base_note.id, initial_blocks)

        # Batch move: invert order and update subpage title
        moves = [
            {"id": "blk-p3", "noteId": self.base_note.id, "sortIndex": "a0", "type": "p"},
            {"id": "blk-sub2", "noteId": self.base_note.id, "sortIndex": "a1", "type": "sub_page", "page_id": "p-20", "title": "Subpage 2 Modified"},
            {"id": "blk-p2", "noteId": self.base_note.id, "sortIndex": "a2", "type": "p"},
            {"id": "blk-sub1", "noteId": self.base_note.id, "sortIndex": "a3", "type": "sub_page", "page_id": "p-10", "title": "Subpage 1 Modified"},
            {"id": "blk-p1", "noteId": self.base_note.id, "sortIndex": "a4", "type": "p"}
        ]
        move_res = models.update_batch_blocks_order_orm(moves)
        self.assertTrue(move_res.get('ok'))
        self.assertEqual(move_res.get('updatedCount'), 5)

        # Verify order and property preservation
        blocks_in_db = list(models.Block.select().where(models.Block.note_id == self.base_note.id).order_by(models.Block.sort_index.asc()))
        self.assertEqual(len(blocks_in_db), 5)
        self.assertEqual([b.id for b in blocks_in_db], ["blk-p3", "blk-sub2", "blk-p2", "blk-sub1", "blk-p1"])

        sub2 = models.Block.get(models.Block.id == "blk-sub2").to_dict()
        self.assertEqual(sub2['type'], 'sub_page')
        self.assertEqual(sub2['page_id'], 'p-20')
        self.assertEqual(sub2['title'], 'Subpage 2 Modified')

        sub1 = models.Block.get(models.Block.id == "blk-sub1").to_dict()
        self.assertEqual(sub1['type'], 'sub_page')
        self.assertEqual(sub1['page_id'], 'p-10')
        self.assertEqual(sub1['title'], 'Subpage 1 Modified')

    def test_high_density_subpages_scale(self):
        """Stress test: 100 subpages synced to a single note."""
        count = 100
        payload = [
            {
                "type": "sub_page",
                "id": f"dense-sub-{i:03d}",
                "page_id": f"dense-target-{i:03d}",
                "title": f"Subpage Index #{i:03d}"
            }
            for i in range(count)
        ]
        res = models.sync_blocks_from_note_html_orm(self.base_note.id, payload)
        self.assertTrue(res.get('ok'))

        db_count = models.Block.select().where(
            (models.Block.note_id == self.base_note.id) & (models.Block.type == 'sub_page')
        ).count()
        self.assertEqual(db_count, count)

        # Spot-check first, middle, last
        for i in [0, 49, 99]:
            b = models.Block.get(models.Block.id == f"dense-sub-{i:03d}").to_dict()
            self.assertEqual(b['page_id'], f"dense-target-{i:03d}")
            self.assertEqual(b['title'], f"Subpage Index #{i:03d}")

    def test_sync_idempotence_and_no_duplication(self):
        """Syncing the same subpage blocks multiple times updates in place without block duplication."""
        payload = [
            {"type": "sub_page", "id": "idemp-1", "page_id": "target-1", "title": "V1"},
            {"type": "sub_page", "id": "idemp-2", "page_id": "target-2", "title": "V1"}
        ]
        models.sync_blocks_from_note_html_orm(self.base_note.id, payload)
        self.assertEqual(models.Block.select().where(models.Block.note_id == self.base_note.id).count(), 2)

        # Re-sync with updated titles
        payload[0]['title'] = "V2"
        payload[1]['title'] = "V2"
        models.sync_blocks_from_note_html_orm(self.base_note.id, payload)
        self.assertEqual(models.Block.select().where(models.Block.note_id == self.base_note.id).count(), 2)

        blk1 = models.Block.get(models.Block.id == "idemp-1").to_dict()
        self.assertEqual(blk1['title'], "V2")


class TestAdversarialFrontendEventResolution(unittest.TestCase):
    """Adversarial testing for Frontend Selection Conflict (R1) event resolution."""

    @classmethod
    def setUpClass(cls):
        app_js_path = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
        with open(app_js_path, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def simulate_selection_guard(self, target_tag, target_attrs, parent_hierarchy):
        """
        Pure oracle simulating the JS selection abort guard:
        if (e.target.closest('[contenteditable="true"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        """
        target_tag_upper = target_tag.upper()
        if target_tag_upper in ('INPUT', 'TEXTAREA'):
            return "ABORT_LOCKED_FOR_NATIVE"

        # Check self
        if target_attrs.get('contenteditable') == 'true':
            return "ABORT_LOCKED_FOR_NATIVE"

        # Check parents hierarchy up to panelCanvas
        for parent_tag, parent_attrs in parent_hierarchy:
            if parent_attrs.get('contenteditable') == 'true':
                return "ABORT_LOCKED_FOR_NATIVE"

        # If not editable, test container check:
        # const isEditorContainer = e.target === panelCanvas || Boolean(e.target.closest('.editor-container, .editor-body, #blocks-container'));
        classes = target_attrs.get('class', '').split()
        target_id = target_attrs.get('id', '')
        if target_tag_upper == 'MAIN' and target_id == 'panel-canvas':
            return "ALLOW_MARQUEE_LASSO"

        for parent_tag, parent_attrs in [(target_tag, target_attrs)] + parent_hierarchy:
            p_classes = parent_attrs.get('class', '').split()
            p_id = parent_attrs.get('id', '')
            if 'editor-container' in p_classes or 'editor-body' in p_classes or p_id == 'blocks-container':
                return "ALLOW_MARQUEE_LASSO"

        return "REJECT_NO_MARQUEE"

    def test_deeply_nested_editable_text_blocks_abort_lasso(self):
        """Deeply nested inline elements inside contenteditable rich canvas must abort lasso."""
        hierarchy = [
            ('SPAN', {}),
            ('P', {}),
            ('DIV', {'id': 'rich-editor-canvas', 'contenteditable': 'true'}),
            ('DIV', {'id': 'editor-body', 'class': 'editor-body editor-container'}),
            ('MAIN', {'id': 'panel-canvas', 'class': 'panel-canvas'})
        ]
        result = self.simulate_selection_guard('B', {}, hierarchy)
        self.assertEqual(result, "ABORT_LOCKED_FOR_NATIVE")

    def test_input_and_textarea_abort_lasso(self):
        """Input and textarea elements anywhere in the editor must abort lasso."""
        hierarchy = [
            ('DIV', {'id': 'editor-body', 'class': 'editor-body editor-container'}),
            ('MAIN', {'id': 'panel-canvas', 'class': 'panel-canvas'})
        ]
        self.assertEqual(self.simulate_selection_guard('INPUT', {'type': 'text'}, hierarchy), "ABORT_LOCKED_FOR_NATIVE")
        self.assertEqual(self.simulate_selection_guard('TEXTAREA', {}, hierarchy), "ABORT_LOCKED_FOR_NATIVE")

    def test_empty_canvas_and_outer_margins_allow_lasso(self):
        """Clicking on panelCanvas or editor-container margins must start lasso."""
        res_canvas = self.simulate_selection_guard('MAIN', {'id': 'panel-canvas', 'class': 'panel-canvas'}, [])
        self.assertEqual(res_canvas, "ALLOW_MARQUEE_LASSO")

        res_margin = self.simulate_selection_guard('DIV', {'id': 'editor-body', 'class': 'editor-body editor-container'}, [
            ('MAIN', {'id': 'panel-canvas', 'class': 'panel-canvas'})
        ])
        self.assertEqual(res_margin, "ALLOW_MARQUEE_LASSO")

    def test_mousedown_guard_is_first_statement_in_app_js(self):
        """Verify AST/source: guard statement occurs immediately after panelCanvas mousedown starts."""
        pattern = r"panelCanvas\.addEventListener\('mousedown',\s*\([a-zA-Z0-9_]+\)\s*=>\s*\{([^}]+)"
        match = re.search(pattern, self.app_js)
        self.assertIsNotNone(match, "Could not find panelCanvas mousedown listener in app.js")
        listener_head = match.group(1).strip()
        code_lines = [l.strip() for l in listener_head.split('\n') if l.strip() and not l.strip().startswith('//')]
        self.assertTrue(len(code_lines) > 0)
        self.assertIn("contenteditable", code_lines[0])
        self.assertIn("INPUT", code_lines[0])
        self.assertIn("TEXTAREA", code_lines[0])
        self.assertIn("return", code_lines[0])


class DomTextCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.elements = []
    def handle_data(self, data):
        if data.strip():
            self.texts.append(data.strip())
    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class TestAdversarialFormattingAndFocusMode(unittest.TestCase):
    """Adversarial testing for Formatting Bar Amber Exclusivity & Focus Mode Removal (R4)."""

    @classmethod
    def setUpClass(cls):
        html_path = os.path.join(WORKSPACE_DIR, 'frontend', 'index.html')
        css_path = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')
        js_path = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
        with open(html_path, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(css_path, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(js_path, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_zero_occurrences_of_focus_mode_indicator(self):
        """R4 verification: absolutely 0 occurrences of #focus-mode-indicator."""
        self.assertNotIn("focus-mode-indicator", self.index_html)
        self.assertNotIn("focus-mode-indicator", self.styles_css)
        self.assertNotIn("focus-mode-indicator", self.app_js)

    def test_zero_visible_occurrences_of_modo_concentracion_in_dom(self):
        """R4 verification: absolutely 0 text nodes in DOM tree containing 'Modo concentración'."""
        parser = DomTextCollector()
        parser.feed(self.index_html)
        matches = [t for t in parser.texts if re.search(r"modo\s+concentraci[oó]n", t, re.IGNORECASE)]
        self.assertEqual(len(matches), 0, f"Found visible text nodes with 'Modo concentración': {matches}")

    def test_format_bar_non_insert_buttons_amber_exclusivity_cascade(self):
        """
        Adversarial CSS Cascade Verification:
        R4 Acceptance Criterion:
        'In .desktop-format-bar, only the insert dropdown button (#btn-insert-dropdown) has yellow/amber styling;
         all other toolbar buttons match the canvas/bar background color.'

        Empirical Check:
        Check if global rule at line 9749:
          .btn-secondary:not(.btn-trash-action):not(.btn-danger):not([class*="trash"]):not([class*="delete"])
        overrides scoped rule at line 1847:
          .desktop-format-bar .btn-secondary:not(.btn-trash-action)
        due to higher specificity ((0, 5, 0) vs (0, 3, 0)) and later appearance in stylesheet.
        """
        # Buttons in .desktop-format-bar that have class .btn-secondary
        toolbar_buttons = ['btn-in-note-search', 'btn-pin-note', 'btn-page-appearance']

        # Find line 1847 scoped rule
        scoped_match = re.search(r'\.desktop-format-bar\s+\.btn-secondary:not\(\.btn-trash-action\)\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(scoped_match, "Scoped rule .desktop-format-bar .btn-secondary:not(.btn-trash-action) missing!")

        # Find global amber rule at line 9749
        global_amber_match = re.search(r'(\.btn-secondary:not\(\.btn-trash-action\):not\(\.btn-danger\):not\(\[class\*="trash"\]\):not\(\[class\*="delete"\]\)[^{]*)\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(global_amber_match, "Global amber rule missing from styles.css")

        global_selector_str = global_amber_match.group(1)
        global_body = global_amber_match.group(2)

        # Check if global rule has higher line number and contains !important amber
        scoped_pos = scoped_match.start()
        global_pos = global_amber_match.start()

        # Check if global selector explicitly excludes format bar secondary buttons
        excluded = all(
            neg_class in global_selector_str
            for neg_class in [
                ':not(.format-bar-action-icon-btn)',
                ':not(.in-note-find-trigger)',
                ':not(.page-dots-btn)'
            ]
        )

        if not excluded and global_pos > scoped_pos and 'var(--accent-amber' in global_body and '!important' in global_body:
            # Calculate CSS specificity
            # Scoped selector: .desktop-format-bar .btn-secondary:not(.btn-trash-action) -> 3 classes = (0, 3, 0)
            # Global selector: .btn-secondary:not(...):not(...):not(...):not(...) -> 5 classes/attrs = (0, 5, 0)
            scoped_spec = (0, 3, 0)
            global_spec = (0, 5, 0)
            if global_spec > scoped_spec:
                self.fail(
                    "CASCADE REGRESSION DETECTED: Global amber rule at line ~9749 "
                    "'.btn-secondary:not(.btn-trash-action):not(.btn-danger):not([class*=\"trash\"]):not([class*=\"delete\"])' "
                    "has specificity (0, 5, 0) which exceeds scoped rule specificity (0, 3, 0) and appears 8,000 lines later. "
                    "Because both have !important, Chromium applies amber soft background and amber text to toolbar buttons: "
                    f"{toolbar_buttons}. This directly violates Requirement R4."
                )


if __name__ == '__main__':
    unittest.main()
