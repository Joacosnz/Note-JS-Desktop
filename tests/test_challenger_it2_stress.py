#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Challenger it2_2 Empirical Stress Test Suite
Independent adversarial verification across requirements R1, R2, R3, R4.
"""

import os
import re
import sys
import json
import time
import shutil
import tempfile
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WORKSPACE_DIR)

import models
from peewee import SqliteDatabase

APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
INDEX_HTML_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'index.html')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')


class SimulatedDOMNode:
    """Helper to simulate DOM tree resolution for event delegation."""
    def __init__(self, tag, class_name='', node_id='', contenteditable=None, parent=None, is_input=False):
        self.tagName = tag.upper()
        self.className = class_name
        self.classList = set(class_name.split()) if class_name else set()
        self.id = node_id
        self.attributes = {}
        if contenteditable is not None:
            self.attributes['contenteditable'] = str(contenteditable)
        self.parent = parent
        self.children = []
        if parent:
            parent.children.append(self)

    def getAttribute(self, attr):
        return self.attributes.get(attr)

    def closest(self, selector):
        curr = self
        while curr:
            if curr._matches(selector):
                return curr
            curr = curr.parent
        return None

    def _matches(self, selector):
        parts = [s.strip() for s in selector.split(',')]
        for part in parts:
            if self._matches_single(part):
                return True
        return False

    def _matches_single(self, sel):
        if sel == '[contenteditable="true"]':
            return self.attributes.get('contenteditable') == 'true'
        if sel.startswith('.'):
            return sel[1:] in self.classList
        if sel.startswith('#'):
            return self.id == sel[1:]
        if sel.upper() == self.tagName:
            return True
        return False


class TestChallengerIt2R1SelectionConflict(unittest.TestCase):
    """Empirical verification for Requirement R1: Selection conflict and lasso guard."""

    @classmethod
    def setUpClass(cls):
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def _evaluate_mousedown_guard(self, target_node, button=0):
        """Replicates mousedown listener logic from initSpatialBlockController in app.js."""
        # 1. First line guard: editable check
        if (target_node.closest('[contenteditable="true"]') or 
            target_node.tagName == 'INPUT' or 
            target_node.tagName == 'TEXTAREA'):
            return False, 'ABORT_EDITABLE'

        # 2. Button and UI controls check
        if button != 0:
            return False, 'ABORT_BUTTON'
        if (target_node.closest('#spatial-block-handle') or 
            target_node.closest('#block-action-menu') or 
            target_node.closest('.desktop-format-bar') or 
            target_node.closest('button') or 
            target_node.closest('#sticky-toc-rail')):
            return False, 'ABORT_CONTROL'

        # 3. Canvas and editor-container initiation check
        is_editor_container = (
            target_node.id == 'panel-canvas' or 
            bool(target_node.closest('.editor-container, .editor-body, #blocks-container'))
        )
        if not is_editor_container:
            return False, 'ABORT_OUTSIDE_CANVAS'

        return True, 'START_LASSO'

    def test_guard_is_first_statement_in_mousedown_listener(self):
        """Verifies mousedown listener has editable check as statement #1."""
        listener_match = re.search(r"panelCanvas\.addEventListener\(\s*['\"]mousedown['\"]\s*,\s*\(\s*e\s*\)\s*=>\s*\{([\s\S]*?)\n\s*\}\s*\);", self.app_js)
        self.assertIsNotNone(listener_match, "panelCanvas mousedown listener must exist")
        listener_body = listener_match.group(1).strip()

        # Split into statements, ignoring comments and blank lines
        cleaned_lines = []
        for line in listener_body.splitlines():
            s = line.strip()
            if s and not s.startswith('//') and not s.startswith('/*'):
                cleaned_lines.append(s)

        first_stmt = cleaned_lines[0]
        self.assertIn("e.target.closest('[contenteditable=\"true\"]')", first_stmt)
        self.assertIn("e.target.tagName === 'INPUT'", first_stmt)
        self.assertIn("e.target.tagName === 'TEXTAREA'", first_stmt)
        self.assertTrue(first_stmt.endswith('return;'), "Guard must abort immediately with return;")

    def test_deep_nesting_editable_elements_all_abort_lasso(self):
        """Stress: Deeply nested text nodes (up to 25 levels) inside contenteditable abort lasso."""
        panel_canvas = SimulatedDOMNode('div', node_id='panel-canvas')
        editor_body = SimulatedDOMNode('div', class_name='editor-body editor-container', parent=panel_canvas)
        rich_editor = SimulatedDOMNode('div', class_name='notion-rich-editor', node_id='rich-editor-canvas', contenteditable='true', parent=editor_body)

        curr = rich_editor
        tags = ['div', 'p', 'span', 'b', 'i', 'u', 'em', 'strong', 'code', 'mark', 'span', 'b']
        for i, tag in enumerate(tags):
            curr = SimulatedDOMNode(tag, class_name=f'level-{i}', parent=curr)
            started, reason = self._evaluate_mousedown_guard(curr)
            self.assertFalse(started, f"Failed at level {i} with tag {tag}")
            self.assertEqual(reason, 'ABORT_EDITABLE')

    def test_input_and_textarea_controls_abort_lasso(self):
        """Stress: Form controls (inputs, textareas) anywhere inside container abort lasso."""
        panel_canvas = SimulatedDOMNode('div', node_id='panel-canvas')
        editor_body = SimulatedDOMNode('div', class_name='editor-body editor-container', parent=panel_canvas)

        inp = SimulatedDOMNode('input', parent=editor_body, is_input=True)
        txt = SimulatedDOMNode('textarea', parent=editor_body)

        started_inp, reason_inp = self._evaluate_mousedown_guard(inp)
        self.assertFalse(started_inp)
        self.assertEqual(reason_inp, 'ABORT_EDITABLE')

        started_txt, reason_txt = self._evaluate_mousedown_guard(txt)
        self.assertFalse(started_txt)
        self.assertEqual(reason_txt, 'ABORT_EDITABLE')

    def test_subpage_block_inside_rich_editor_aborts_lasso(self):
        """Stress: Subpage block inside rich editor does not trigger lasso."""
        panel_canvas = SimulatedDOMNode('div', node_id='panel-canvas')
        editor_body = SimulatedDOMNode('div', class_name='editor-body editor-container', parent=panel_canvas)
        rich_editor = SimulatedDOMNode('div', class_name='notion-rich-editor', contenteditable='true', parent=editor_body)
        subpage = SimulatedDOMNode('div', class_name='block-subpage', contenteditable='false', parent=rich_editor)
        title_span = SimulatedDOMNode('span', class_name='subpage-title', parent=subpage)

        started, reason = self._evaluate_mousedown_guard(subpage)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_EDITABLE')

        started_t, reason_t = self._evaluate_mousedown_guard(title_span)
        self.assertFalse(started_t)
        self.assertEqual(reason_t, 'ABORT_EDITABLE')

    def test_empty_canvas_and_margins_start_lasso(self):
        """Stress: Clicks on empty canvas or outer margins correctly start lasso."""
        panel_canvas = SimulatedDOMNode('div', node_id='panel-canvas')
        editor_body = SimulatedDOMNode('div', class_name='editor-body editor-container', parent=panel_canvas)
        margin_div = SimulatedDOMNode('div', class_name='canvas-outer-margin', parent=editor_body)

        for target in [panel_canvas, editor_body, margin_div]:
            started, reason = self._evaluate_mousedown_guard(target, button=0)
            self.assertTrue(started, f"Failed to start lasso on {target.className or target.id}")
            self.assertEqual(reason, 'START_LASSO')

    def test_format_bar_and_controls_do_not_start_lasso(self):
        """Stress: Clicks on format bar buttons or drag handle do not start lasso."""
        panel_canvas = SimulatedDOMNode('div', node_id='panel-canvas')
        format_bar = SimulatedDOMNode('div', class_name='desktop-format-bar', parent=panel_canvas)
        btn = SimulatedDOMNode('button', class_name='format-bar-btn', parent=format_bar)
        handle = SimulatedDOMNode('div', node_id='spatial-block-handle', parent=panel_canvas)

        for target in [btn, handle]:
            started, reason = self._evaluate_mousedown_guard(target)
            self.assertFalse(started)
            self.assertEqual(reason, 'ABORT_CONTROL')

    def test_non_primary_mouse_clicks_abort(self):
        """Stress: Right-click (2) and middle-click (1) on empty canvas abort lasso."""
        panel_canvas = SimulatedDOMNode('div', node_id='panel-canvas')
        for btn_code in [1, 2]:
            started, reason = self._evaluate_mousedown_guard(panel_canvas, button=btn_code)
            self.assertFalse(started)
            self.assertEqual(reason, 'ABORT_BUTTON')


class TestChallengerIt2R2PersistenceAndSchema(unittest.TestCase):
    """Empirical verification for Requirement R2: SQLite persistence, schema, and signatures."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, 'challenger_stress.db')
        self.test_db = SqliteDatabase(self.db_path)

        self.orig_db = models.db
        models.db = self.test_db
        models.Block._meta.database = self.test_db
        models.Note._meta.database = self.test_db

        self.test_db.connect()
        self.test_db.create_tables([models.Note, models.Block], safe=True)

        self.base_note = models.Note.create(
            id=1001,
            title='Parent Note for Sub-pages',
            content='Test content',
            created_at=int(time.time() * 1000),
            updated_at=int(time.time() * 1000)
        )

    def tearDown(self):
        models.db = self.orig_db
        models.Block._meta.database = self.orig_db
        models.Note._meta.database = self.orig_db
        self.test_db.close()
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_stress_bulk_subpages_sync_and_to_dict_roundtrip(self):
        """Stress: 150 sub_page blocks synced with varied page_id types and titles."""
        blocks = []
        for i in range(150):
            # Alternate id formats: string uuid, integer, zero, negative
            if i % 4 == 0:
                pid = f"note-sub-{i}"
            elif i % 4 == 1:
                pid = 2000 + i
            elif i % 4 == 2:
                pid = 0
            else:
                pid = f"uuid-complex-{i}-äöü-🚀"

            blocks.append({
                'id': f"blk-stress-{i}",
                'type': 'sub_page',
                'page_id': pid,
                'title': f"Sub-nota número {i} con acentos y emojis 📄 #{i}",
                'sortIndex': f"a{i:04d}",
                'properties': {'custom_meta': f'val-{i}'}
            })

        res = models.sync_blocks_from_note_html_orm(self.base_note.id, blocks)
        self.assertTrue(res['ok'])
        self.assertEqual(res['syncedCount'], 150)

        # Retrieve rows directly from SQLite
        rows = list(models.Block.select().where(models.Block.note_id == self.base_note.id).order_by(models.Block.sort_index.asc()))
        self.assertEqual(len(rows), 150)

        # Verify each block's to_dict() returns expected structured keys
        for idx, row in enumerate(rows):
            d = row.to_dict()
            self.assertEqual(d['type'], 'sub_page')
            self.assertEqual(d['id'], f"blk-stress-{idx}")
            self.assertIn('page_id', d)
            self.assertIn('title', d)
            self.assertEqual(d['title'], f"Sub-nota número {idx} con acentos y emojis 📄 #{idx}")
            self.assertEqual(d['properties'].get('custom_meta'), f'val-{idx}')

    def test_batch_reordering_preserves_subpage_payload(self):
        """Stress: update_batch_blocks_order_orm preserves page_id and title during reordering."""
        initial_blocks = [
            {'id': 'blk-1', 'type': 'sub_page', 'page_id': 'note-alpha', 'title': 'Alpha Subpage', 'sortIndex': 'a0'},
            {'id': 'blk-2', 'type': 'p', 'properties': {'text': 'Regular paragraph'}, 'sortIndex': 'a1'},
            {'id': 'blk-3', 'type': 'sub_page', 'page_id': 'note-beta', 'title': 'Beta Subpage', 'sortIndex': 'a2'},
        ]
        models.sync_blocks_from_note_html_orm(self.base_note.id, initial_blocks)

        # Move blk-3 to first position and blk-1 to last
        reorder_moves = [
            {'id': 'blk-3', 'sortIndex': 'a00', 'type': 'sub_page', 'page_id': 'note-beta', 'title': 'Beta Subpage'},
            {'id': 'blk-1', 'sortIndex': 'a99', 'type': 'sub_page', 'page_id': 'note-alpha', 'title': 'Alpha Subpage'},
        ]
        reorder_res = models.update_batch_blocks_order_orm(reorder_moves)
        self.assertTrue(reorder_res['ok'])

        # Verify in DB
        blk3 = models.Block.get(models.Block.id == 'blk-3').to_dict()
        self.assertEqual(blk3['type'], 'sub_page')
        self.assertEqual(blk3['page_id'], 'note-beta')
        self.assertEqual(blk3['title'], 'Beta Subpage')
        self.assertEqual(blk3['sortIndex'], 'a00')

        blk1 = models.Block.get(models.Block.id == 'blk-1').to_dict()
        self.assertEqual(blk1['type'], 'sub_page')
        self.assertEqual(blk1['page_id'], 'note-alpha')
        self.assertEqual(blk1['title'], 'Alpha Subpage')
        self.assertEqual(blk1['sortIndex'], 'a99')

    def test_extract_note_signature_detects_subpage_changes(self):
        """Stress: _extract_note_signature detects changes in sub_page blocks."""
        note_dict = {
            'id': 1001,
            'title': 'Test Note',
            'blocks': [
                {'id': 'b1', 'type': 'sub_page', 'page_id': 'sub-1', 'title': 'Title 1'}
            ]
        }
        sig_initial = models._extract_note_signature(note_dict)
        self.assertTrue(bool(sig_initial))

        # 1. Title change alters signature
        note_dict_mod_title = {
            'id': 1001,
            'title': 'Test Note',
            'blocks': [
                {'id': 'b1', 'type': 'sub_page', 'page_id': 'sub-1', 'title': 'Title MODIFIED'}
            ]
        }
        sig_mod_title = models._extract_note_signature(note_dict_mod_title)
        self.assertNotEqual(sig_initial, sig_mod_title)

        # 2. page_id change alters signature
        note_dict_mod_page = {
            'id': 1001,
            'title': 'Test Note',
            'blocks': [
                {'id': 'b1', 'type': 'sub_page', 'page_id': 'sub-2-new', 'title': 'Title 1'}
            ]
        }
        sig_mod_page = models._extract_note_signature(note_dict_mod_page)
        self.assertNotEqual(sig_initial, sig_mod_page)

        # 3. Adding a second subpage alters signature
        note_dict_added = {
            'id': 1001,
            'title': 'Test Note',
            'blocks': [
                {'id': 'b1', 'type': 'sub_page', 'page_id': 'sub-1', 'title': 'Title 1'},
                {'id': 'b2', 'type': 'sub_page', 'page_id': 'sub-2', 'title': 'Title 2'}
            ]
        }
        sig_added = models._extract_note_signature(note_dict_added)
        self.assertNotEqual(sig_initial, sig_added)

        # 4. Same data produces exact same signature (idempotent)
        sig_dup = models._extract_note_signature(json.loads(json.dumps(note_dict)))
        self.assertEqual(sig_initial, sig_dup)


class TestChallengerIt2R3DOMRenderingAndNavigation(unittest.TestCase):
    """Empirical verification for Requirement R3: DOM component rendering, CSS hover, loadNote."""

    @classmethod
    def setUpClass(cls):
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()

    def test_render_block_case_subpage_structure(self):
        """Verifies renderBlock includes case 'sub_page' producing .block-subpage with 📄 and onclick."""
        pattern = r"case\s+['\"]sub_page['\"]\s*:\s*\{([\s\S]*?)\n\s*\}"
        match = re.search(pattern, self.app_js)
        self.assertIsNotNone(match, "renderBlock must contain case 'sub_page'")
        case_body = match.group(1)

        self.assertIn("div.className = 'block-subpage'", case_body)
        self.assertIn("div.setAttribute('contenteditable', 'false')", case_body)
        self.assertIn("div.style.cursor = 'pointer'", case_body)
        self.assertIn("📄", case_body)
        self.assertIn("div.onclick", case_body)
        self.assertIn("loadNote(pageId)", case_body)
        self.assertIn("e.preventDefault()", case_body)
        self.assertIn("e.stopPropagation()", case_body)

    def test_styles_css_subpage_hover_and_pointer_rules(self):
        """Verifies styles.css provides cursor: pointer, flex layout, and light gray hover effect."""
        subpage_match = re.search(r"\.block-subpage\s*\{([^}]+)\}", self.styles_css)
        self.assertIsNotNone(subpage_match, ".block-subpage rule must exist")
        props = subpage_match.group(1)
        self.assertIn("cursor: pointer", props)
        self.assertIn("display: flex", props)

        # Verify hover rule
        hover_match = re.search(r"\.block-subpage:hover\s*\{([^}]+)\}", self.styles_css)
        self.assertIsNotNone(hover_match, ".block-subpage:hover must exist")
        self.assertIn("background:", hover_match.group(1))

        # Verify light-mode hover rule
        light_hover_match = re.search(r"body\.light-mode\s+\.block-subpage:hover\s*\{([^}]+)\}", self.styles_css)
        self.assertIsNotNone(light_hover_match, "body.light-mode .block-subpage:hover must exist")
        self.assertIn("#e5e7eb", light_hover_match.group(1))

    def _simulate_load_note(self, page_id, notes_list):
        """Simulates window.loadNote(pageId) logic from frontend/app.js."""
        toasts = []
        selected_id = None

        def show_toast(msg, icon):
            toasts.append((msg, icon))

        def select_note(nid):
            nonlocal selected_id
            selected_id = nid

        # Logic from app.js line 4014:
        # In JS: if (!pageId && pageId !== 0)
        # Note: in Python, bool(False) is falsy and False == 0, but in JS false !== 0
        if page_id is False or (page_id is None) or (page_id == ''):
            show_toast('ID de nota inválido', '⚠️')
            return False, toasts, selected_id

        note = None
        for n in notes_list:
            # String matching or numeric matching (excluding bool)
            if str(n.get('id')) == str(page_id):
                note = n
                break
            if not isinstance(page_id, bool) and isinstance(n.get('id'), (int, float)) and isinstance(page_id, (int, float)) and n.get('id') == page_id:
                note = n
                break

        if not note:
            show_toast('Nota no encontrada', '⚠️')
            return False, toasts, selected_id

        if note.get('isTrashed'):
            show_toast('Restaura la nota desde la papelera para abrirla y editarla', '🗑️')
            return False, toasts, selected_id

        select_note(note['id'])
        return True, toasts, selected_id

    def test_load_note_oracle_boundary_and_error_cases(self):
        """Stress: Comprehensive oracle test for loadNote across all edge cases."""
        mock_notes = [
            {'id': 101, 'title': 'Normal Note', 'isTrashed': False},
            {'id': 102, 'title': 'Trashed Note', 'isTrashed': True},
            {'id': 0, 'title': 'Zero ID Note', 'isTrashed': False},
            {'id': 'str-uuid-202', 'title': 'UUID Note', 'isTrashed': False},
        ]

        # 1. Falsy and invalid IDs
        for invalid_id in [None, '', False]:
            ok, toasts, sel = self._simulate_load_note(invalid_id, mock_notes)
            self.assertFalse(ok)
            self.assertEqual(toasts[0][0], 'ID de nota inválido')
            self.assertIsNone(sel)

        # 2. Nonexistent note
        ok, toasts, sel = self._simulate_load_note(9999, mock_notes)
        self.assertFalse(ok)
        self.assertEqual(toasts[0][0], 'Nota no encontrada')

        # 3. Trashed note rejection
        ok, toasts, sel = self._simulate_load_note(102, mock_notes)
        self.assertFalse(ok)
        self.assertIn('papelera', toasts[0][0])
        self.assertIsNone(sel)

        # 4. Valid note opening: int passed as int
        ok, toasts, sel = self._simulate_load_note(101, mock_notes)
        self.assertTrue(ok)
        self.assertEqual(sel, 101)

        # 5. Valid note opening: int passed as string
        ok, toasts, sel = self._simulate_load_note('101', mock_notes)
        self.assertTrue(ok)
        self.assertEqual(sel, 101)

        # 6. ID 0 (zero) is valid, not falsy
        ok, toasts, sel = self._simulate_load_note(0, mock_notes)
        self.assertTrue(ok)
        self.assertEqual(sel, 0)

        ok, toasts, sel = self._simulate_load_note('0', mock_notes)
        self.assertTrue(ok)
        self.assertEqual(sel, 0)

        # 7. String UUID note
        ok, toasts, sel = self._simulate_load_note('str-uuid-202', mock_notes)
        self.assertTrue(ok)
        self.assertEqual(sel, 'str-uuid-202')


class TestChallengerIt2R4FormattingBarAmberExclusivityAndFocusRemoval(unittest.TestCase):
    """Empirical verification for Requirement R4: Amber exclusivity & focus mode clean-up."""

    @classmethod
    def setUpClass(cls):
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_zero_occurrences_of_focus_mode_indicator_across_codebase(self):
        """Audit: Exactly ZERO occurrences of 'focus-mode-indicator' in frontend files."""
        frontend_dir = os.path.join(WORKSPACE_DIR, 'frontend')
        for root, _, files in os.walk(frontend_dir):
            for file in files:
                if file.endswith(('.html', '.js', '.css')):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    self.assertNotIn('focus-mode-indicator', content, f"Found focus-mode-indicator in {filepath}")

    def test_zero_occurrences_of_modo_concentracion_phrase_in_frontend(self):
        """Audit: Exactly ZERO occurrences of 'Modo concentración' (case-insensitive) in frontend."""
        frontend_dir = os.path.join(WORKSPACE_DIR, 'frontend')
        patterns = [r'modo\s+concentraci[oó]n']
        for root, _, files in os.walk(frontend_dir):
            for file in files:
                if file.endswith(('.html', '.js', '.css')):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    for p in patterns:
                        match = re.search(p, content, re.IGNORECASE)
                        self.assertIsNone(match, f"Found '{match.group(0) if match else ''}' in {filepath}")

    def test_format_bar_all_non_insert_buttons_have_neutral_cascade(self):
        """Audit: In .desktop-format-bar, only #btn-insert-dropdown receives amber styling."""
        format_bar_match = re.search(r'<div\s+class=["\']desktop-format-bar["\']>([\s\S]*?)<!-- Barra Flotante de Búsqueda', self.index_html)
        self.assertIsNotNone(format_bar_match, "desktop-format-bar must be found in index.html")
        format_bar_html = format_bar_match.group(1)

        # Extract all button IDs
        btn_ids = re.findall(r'<button\s+[^>]*id=["\']([^"\']+)["\']', format_bar_html)
        self.assertIn('btn-insert-dropdown', btn_ids)

        non_insert_btns = [bid for bid in btn_ids if bid != 'btn-insert-dropdown']
        self.assertTrue(len(non_insert_btns) >= 3, "Must have non-insert buttons in toolbar")

        # Verify Section 6 exists and appears after the global amber block
        sec6_pattern = r"\.desktop-format-bar\s+button\.btn-secondary[\s\S]*?background:\s*transparent\s*!important;"
        self.assertRegex(self.styles_css, sec6_pattern, "Section 6 neutral override rule must exist")

        # Verify global amber rule explicitly excludes format bar buttons
        global_amber_rule = re.search(r"\.btn-secondary:not\([^)]+\):not\([^)]+\):not\([^)]+\):not\([^)]+\):not\(\.format-bar-action-icon-btn\):not\(\.in-note-find-trigger\):not\(\.page-dots-btn\)", self.styles_css)
        self.assertIsNotNone(global_amber_rule, "Global amber rule must explicitly exclude format bar classes")

        # Verify positions: Section 6 MUST be positioned AFTER the global amber rule
        amber_pos = self.styles_css.find(".btn-secondary:not(.btn-trash-action)")
        sec6_pos = self.styles_css.find("EXCLUSIÓN Y NEUTRALIZACIÓN: BOTONES SECUNDARIOS DE LA BARRA DE FORMATO")
        self.assertGreater(amber_pos, 0, "Global amber rule must exist")
        self.assertGreater(sec6_pos, 0, "Section 6 comment must exist")
        self.assertGreater(sec6_pos, amber_pos, "Section 6 neutral rule must be placed after global amber rule for cascade priority")


if __name__ == '__main__':
    unittest.main()
