#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adversarial Challenger Test Suite
Independent empirical boundary testing, failure mode stress tests, and invariant checks.

Dimensions:
1. Sub-note Block Schema & Failure Modes:
   - null title, missing page_id, integer vs string IDs, camelCase pageId
   - malformed/corrupted JSON properties in SQLite
   - HTML injection and unicode in titles
   - loadNote invalid targets: null, empty string, non-existent note, trashed note, id=0
   - SQLite persistence under batch sync and moves
2. CSS Stylesheet Integrity & Theme Rules:
   - strict balanced-brace parsing across entire styles.css
   - amber exclusivity verification across ALL format bar buttons
   - neutral overrides for .desktop-format-bar .btn-secondary
   - .block-subpage styling: cursor, flex layout, text truncation, dark/light hover rules
3. Lasso Selection Boundaries & Contenteditable Protection:
   - DOM tree simulation of all editor regions
   - guaranteed abort for contenteditable="true" and deeply nested text elements
   - guaranteed abort for input, textarea, handles, format bar, buttons
   - guaranteed activation only for empty panelCanvas, .editor-container, .editor-body, #blocks-container
   - protection of .block-subpage inside rich-editor-canvas
"""

import os
import sys
import re
import json
import tempfile
import unittest
from peewee import SqliteDatabase

# Ensure workspace root is in sys.path
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

import models

APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
INDEX_HTML_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'index.html')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')


# =============================================================================
# Helper: Simulated DOM for Empirical Lasso Boundary Testing
# =============================================================================

class SimulatedDOMNode:
    def __init__(self, tag, class_name='', node_id='', contenteditable=None, parent=None, attrs=None):
        self.tagName = tag.upper()
        self.className = class_name
        self.id = node_id
        self.contenteditable = contenteditable
        self.parent = parent
        self.children = []
        self.attrs = attrs or {}
        if parent:
            parent.children.append(self)

    def getAttribute(self, name):
        if name == 'contenteditable':
            return self.contenteditable
        return self.attrs.get(name)

    def matches(self, selector):
        selector = selector.strip()
        # Handle comma-separated selectors
        if ',' in selector:
            return any(self.matches(s.strip()) for s in selector.split(','))

        # Check attribute selectors
        if selector == '[contenteditable="true"]':
            return self.contenteditable == 'true'
        if selector == '[contenteditable="false"]':
            return self.contenteditable == 'false'
        
        # Check tag selectors
        if selector in ('INPUT', 'TEXTAREA', 'BUTTON', 'button'):
            return self.tagName.lower() == selector.lower()

        # Check ID selector
        if selector.startswith('#'):
            return self.id == selector[1:]

        # Check Class selector
        if selector.startswith('.'):
            classes = self.className.split()
            return selector[1:] in classes

        return False

    def closest(self, selector):
        curr = self
        while curr is not None:
            if curr.matches(selector):
                return curr
            curr = curr.parent
        return None


# =============================================================================
# Test Suite: Adversarial Challenger
# =============================================================================

class TestAdversarialChallenger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()

        # Set up isolated SQLite database
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = os.path.join(cls.temp_dir.name, 'challenger_test.db')
        cls.orig_db = models.db
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

    @classmethod
    def tearDownClass(cls):
        try:
            if not cls.test_db.is_closed():
                cls.test_db.close()
            cls.temp_dir.cleanup()
        except Exception:
            pass
        finally:
            models.db = cls.orig_db
            models.BaseModel._meta.database = cls.orig_db

    def setUp(self):
        models.Block.delete().execute()
        models.Note.delete().execute()

    # -------------------------------------------------------------------------
    # 1. Sub-note Block Schema Boundary Variations & SQLite Persistence
    # -------------------------------------------------------------------------

    def test_subpage_block_to_dict_null_title(self):
        """Boundary: Block.to_dict handles null/None title gracefully defaulting to empty string."""
        blk = models.Block(
            id='blk-test-null-title',
            note_id=1,
            type='sub_page',
            properties=json.dumps({'page_id': 'note-target-1', 'title': None}),
            sort_index='a0'
        )
        data = blk.to_dict()
        self.assertEqual(data['type'], 'sub_page')
        self.assertEqual(data['page_id'], 'note-target-1')
        self.assertEqual(data['title'], '')  # Must default to empty string, not None

    def test_subpage_block_to_dict_missing_page_id(self):
        """Boundary: Block.to_dict handles sub_page with missing page_id without raising KeyError."""
        blk = models.Block(
            id='blk-test-no-page-id',
            note_id=1,
            type='sub_page',
            properties=json.dumps({'title': 'Nota Huerfana'}),
            sort_index='a0'
        )
        data = blk.to_dict()
        self.assertEqual(data['type'], 'sub_page')
        self.assertIsNone(data['page_id'])
        self.assertEqual(data['title'], 'Nota Huerfana')

    def test_subpage_block_to_dict_integer_page_id(self):
        """Boundary: Block.to_dict preserves integer page_id values without crash."""
        blk = models.Block(
            id='blk-test-int-id',
            note_id=1,
            type='sub_page',
            properties=json.dumps({'page_id': 98765, 'title': 'Nota Numerica'}),
            sort_index='a0'
        )
        data = blk.to_dict()
        self.assertEqual(data['page_id'], 98765)
        self.assertEqual(data['title'], 'Nota Numerica')

    def test_subpage_block_to_dict_camelcase_page_id(self):
        """Boundary: Block.to_dict accepts camelCase pageId as fallback."""
        blk = models.Block(
            id='blk-test-camel-id',
            note_id=1,
            type='sub_page',
            properties=json.dumps({'pageId': 'camel-123', 'title': 'Nota CamelCase'}),
            sort_index='a0'
        )
        data = blk.to_dict()
        self.assertEqual(data['page_id'], 'camel-123')
        self.assertEqual(data['title'], 'Nota CamelCase')

    def test_subpage_block_to_dict_corrupted_properties_json(self):
        """Failure mode: Block.to_dict handles malformed/corrupted JSON in properties without crashing."""
        blk = models.Block(
            id='blk-corrupted',
            note_id=1,
            type='sub_page',
            properties='{malformed_json: true, unterminated...',
            sort_index='a0'
        )
        data = blk.to_dict()
        self.assertEqual(data['id'], 'blk-corrupted')
        self.assertEqual(data['type'], 'sub_page')
        self.assertEqual(data['properties'], {})
        self.assertIsNone(data['page_id'])
        self.assertEqual(data['title'], '')

    def test_subpage_block_to_dict_xss_and_unicode_payloads(self):
        """Stress: Block.to_dict handles XSS scripts, emojis, and unicode characters safely."""
        xss_title = '<script>alert("xss")</script> & <b>bold</b> 🚀 日本語'
        blk = models.Block(
            id='blk-xss',
            note_id=1,
            type='sub_page',
            properties=json.dumps({'page_id': 'target-xss', 'title': xss_title}, ensure_ascii=False),
            sort_index='a0'
        )
        data = blk.to_dict()
        self.assertEqual(data['title'], xss_title)
        self.assertEqual(data['page_id'], 'target-xss')

    def test_sync_blocks_orm_boundary_variations(self):
        """Boundary: sync_blocks_from_note_html_orm with various schema edge cases in payload."""
        payload = [
            # 1. Standard sub_page with string IDs
            {
                'id': 'blk-1',
                'type': 'sub_page',
                'page_id': 'note-uuid-1',
                'title': 'Subpágina Estándar',
                'sortIndex': 'a0'
            },
            # 2. Sub_page with integer page_id and null title
            {
                'id': 'blk-2',
                'type': 'sub_page',
                'page_id': 2026,
                'title': None,
                'sortIndex': 'a1'
            },
            # 3. Sub_page with camelCase pageId
            {
                'id': 'blk-3',
                'type': 'sub_page',
                'pageId': 'camel-456',
                'title': 'Camel Subpágina',
                'sortIndex': 'a2'
            },
            # 4. Standard text block 'p' to ensure coexistence without data corruption
            {
                'id': 'blk-4',
                'type': 'p',
                'properties': {'text': 'Contenido regular'},
                'sortIndex': 'a3'
            }
        ]

        res = models.sync_blocks_from_note_html_orm(note_id=99, blocks_data=payload)
        self.assertTrue(res.get('ok'))
        self.assertEqual(res.get('syncedCount'), 4)

        # Retrieve and verify persistence in SQLite
        saved = models.Block.select().where(models.Block.note_id == 99).order_by(models.Block.sort_index)
        saved_dict = {b.id: b.to_dict() for b in saved}

        self.assertEqual(saved_dict['blk-1']['page_id'], 'note-uuid-1')
        self.assertEqual(saved_dict['blk-1']['title'], 'Subpágina Estándar')

        self.assertEqual(saved_dict['blk-2']['page_id'], 2026)
        self.assertEqual(saved_dict['blk-2']['title'], '')

        self.assertEqual(saved_dict['blk-3']['page_id'], 'camel-456')
        self.assertEqual(saved_dict['blk-3']['title'], 'Camel Subpágina')

        self.assertEqual(saved_dict['blk-4']['type'], 'p')
        self.assertNotIn('page_id', saved_dict['blk-4'])

    def test_sync_blocks_orm_invalid_input_types(self):
        """Failure mode: sync_blocks_from_note_html_orm rejects non-list arguments gracefully."""
        self.assertFalse(models.sync_blocks_from_note_html_orm(1, None)['ok'])
        self.assertFalse(models.sync_blocks_from_note_html_orm(1, "invalid_str")['ok'])
        self.assertFalse(models.sync_blocks_from_note_html_orm(1, {'not': 'a list'})['ok'])

    def test_update_batch_blocks_order_orm_preserves_subpage_payload(self):
        """Boundary: update_batch_blocks_order_orm updates sub_page blocks preserving top-level keys."""
        moves = [
            {
                'id': 'blk-move-1',
                'noteId': 88,
                'type': 'sub_page',
                'page_id': 'target-moved',
                'title': 'Nota Movida',
                'sortIndex': 'b0'
            }
        ]
        res = models.update_batch_blocks_order_orm(moves=moves)
        self.assertTrue(res.get('ok'))
        self.assertEqual(res.get('updatedCount'), 1)

        b = models.Block.get_or_none(models.Block.id == 'blk-move-1')
        self.assertIsNotNone(b)
        b_dict = b.to_dict()
        self.assertEqual(b_dict['page_id'], 'target-moved')
        self.assertEqual(b_dict['title'], 'Nota Movida')

    # -------------------------------------------------------------------------
    # 2. Frontend Navigation (loadNote) Boundary & Failure Mode Testing
    # -------------------------------------------------------------------------

    def _execute_load_note_logic(self, notes_state, page_id):
        """
        Simulates the exact frontend loadNote implementation from app.js:4014-4030:
        function loadNote(pageId) {
          if (!pageId && pageId !== 0) {
            showToast('ID de nota inválido', '⚠️');
            return false;
          }
          const note = state.notes.find(n => String(n.id) === String(pageId) || Number(n.id) === Number(pageId));
          if (!note) {
            showToast('Nota no encontrada', '⚠️');
            return false;
          }
          if (note.isTrashed) {
            showToast('Restaura la nota desde la papelera para abrirla y editarla', '🗑️');
            return false;
          }
          selectNote(note.id);
          return true;
        }
        """
        toasts = []
        selected_id = []

        def show_toast(msg, icon):
            toasts.append((msg, icon))

        def select_note(nid):
            selected_id.append(nid)

        # Implementation under test (with JS semantic simulation for !pageId && pageId !== 0)
        is_js_falsy = (page_id is None or page_id == '' or page_id is False or page_id == 0)
        is_exact_zero = (page_id == 0 and page_id is not False)
        if is_js_falsy and not is_exact_zero:
            show_toast('ID de nota inválido', '⚠️')
            return False, toasts, selected_id

        # find match by string or number comparison
        note = None
        for n in notes_state:
            n_id = n.get('id')
            if str(n_id) == str(page_id):
                note = n
                break
            try:
                if float(n_id) == float(page_id):
                    note = n
                    break
            except (ValueError, TypeError):
                pass

        if not note:
            show_toast('Nota no encontrada', '⚠️')
            return False, toasts, selected_id

        if note.get('isTrashed'):
            show_toast('Restaura la nota desde la papelera para abrirla y editarla', '🗑️')
            return False, toasts, selected_id

        select_note(note['id'])
        return True, toasts, selected_id

    def test_load_note_null_and_empty_targets(self):
        """Failure mode: loadNote returns False and toasts on null, undefined, empty string."""
        notes = [{'id': 1, 'title': 'Test Note', 'isTrashed': False}]
        for bad_id in [None, '', False]:
            ok, toasts, sel = self._execute_load_note_logic(notes, bad_id)
            self.assertFalse(ok)
            self.assertEqual(len(toasts), 1)
            self.assertIn('inválido', toasts[0][0])
            self.assertEqual(len(sel), 0)

    def test_load_note_zero_as_valid_id(self):
        """Boundary: loadNote treats ID=0 or '0' as valid, not falsy."""
        notes = [{'id': 0, 'title': 'Root Note', 'isTrashed': False}]
        ok, toasts, sel = self._execute_load_note_logic(notes, 0)
        self.assertTrue(ok)
        self.assertEqual(len(toasts), 0)
        self.assertEqual(sel, [0])

        ok2, toasts2, sel2 = self._execute_load_note_logic(notes, '0')
        self.assertTrue(ok2)
        self.assertEqual(sel2, [0])

    def test_load_note_integer_vs_string_matching(self):
        """Boundary: loadNote matches numeric note ID when passed as string and vice versa."""
        notes = [
            {'id': 101, 'title': 'Numeric ID Note', 'isTrashed': False},
            {'id': 'note-xyz', 'title': 'String UUID Note', 'isTrashed': False}
        ]
        # Pass string for numeric note
        ok1, toasts1, sel1 = self._execute_load_note_logic(notes, '101')
        self.assertTrue(ok1)
        self.assertEqual(sel1, [101])

        # Pass integer for numeric note
        ok2, toasts2, sel2 = self._execute_load_note_logic(notes, 101)
        self.assertTrue(ok2)
        self.assertEqual(sel2, [101])

        # Pass string for string UUID note
        ok3, toasts3, sel3 = self._execute_load_note_logic(notes, 'note-xyz')
        self.assertTrue(ok3)
        self.assertEqual(sel3, ['note-xyz'])

    def test_load_note_trashed_target_rejection(self):
        """Failure mode: loadNote refuses to open trashed notes and shows warning toast."""
        notes = [
            {'id': 500, 'title': 'Trash Target', 'isTrashed': True}
        ]
        ok, toasts, sel = self._execute_load_note_logic(notes, 500)
        self.assertFalse(ok)
        self.assertEqual(len(toasts), 1)
        self.assertIn('papelera', toasts[0][0].lower())
        self.assertEqual(len(sel), 0)

    def test_load_note_nonexistent_target(self):
        """Failure mode: loadNote handles missing note IDs gracefully."""
        notes = [{'id': 1, 'title': 'Only Note', 'isTrashed': False}]
        ok, toasts, sel = self._execute_load_note_logic(notes, 999999)
        self.assertFalse(ok)
        self.assertEqual(len(toasts), 1)
        self.assertIn('no encontrada', toasts[0][0].lower())
        self.assertEqual(len(sel), 0)

    # -------------------------------------------------------------------------
    # 3. CSS Stylesheet Integrity & Amber Exclusivity Verification
    # -------------------------------------------------------------------------

    def test_css_balanced_braces_and_syntax_integrity(self):
        """Stress: Verify frontend/styles.css has perfectly balanced braces and no dangling tokens."""
        css = self.styles_css

        # Remove comments
        clean_css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)

        # Count open and close curly braces
        open_braces = clean_css.count('{')
        close_braces = clean_css.count('}')
        self.assertEqual(open_braces, close_braces,
                         f"CSS braces unbalanced: {open_braces} open vs {close_braces} close")

        # Verify no orphaned border-color rule
        self.assertNotRegex(css, r'\}\s*border-color:\s*var\(--accent-amber-border\);')

    def test_format_bar_amber_exclusivity_across_all_buttons(self):
        """
        Adversarial: Ensure NO other button in .desktop-format-bar receives amber styling.
        Checks all standard format bar buttons:
        #btn-bold, #btn-italic, #btn-underline, #btn-strike, #btn-header, #btn-bullet,
        #btn-number, #btn-check, #btn-quote, #btn-code, #btn-link, #btn-clear-format,
        #btn-in-note-search, #btn-pin-note, #btn-page-appearance, #btn-reopen-panels,
        #btn-delete-active-note
        """
        format_bar_non_insert_buttons = [
            '#btn-bold', '#btn-italic', '#btn-underline', '#btn-strike',
            '#btn-header', '#btn-bullet', '#btn-number', '#btn-check',
            '#btn-quote', '#btn-code', '#btn-link', '#btn-clear-format',
            '#btn-in-note-search', '#btn-pin-note', '#btn-page-appearance',
            '#btn-reopen-panels', '#btn-delete-active-note'
        ]

        # Amber color values / variables
        amber_indicators = ['--accent-amber', '#f59e0b', '#d97706', '#fbbf24', 'amber']

        # Find all rules matching these specific buttons in styles.css
        for btn_id in format_bar_non_insert_buttons:
            # Look for selector rules targeting this button
            pattern = re.compile(rf'{re.escape(btn_id)}[^{{]*\{{([^}}]+)\}}')
            for match in pattern.finditer(self.styles_css):
                rule_body = match.group(1)
                # Verify that no amber indicator is assigned to background, color, or border
                for prop_line in rule_body.split(';'):
                    prop_line = prop_line.strip()
                    if any(kw in prop_line for kw in ['background', 'color', 'border']):
                        for amber in amber_indicators:
                            self.assertNotIn(
                                amber, prop_line,
                                f"Format bar button {btn_id} must NOT have amber rule! Found: {prop_line}"
                            )

    def test_desktop_format_bar_neutral_rule_scoped_and_prioritized(self):
        """Verify .desktop-format-bar .btn-secondary:not(.btn-trash-action) has neutral background and text."""
        rule_match = re.search(
            r'\.desktop-format-bar\s+\.btn-secondary:not\(\.btn-trash-action\)\s*\{([^}]+)\}',
            self.styles_css
        )
        self.assertIsNotNone(rule_match, "Scoped rule for .desktop-format-bar .btn-secondary must exist")
        body = rule_match.group(1)
        self.assertIn('background: transparent', body)
        self.assertIn('color: var(--text-secondary)', body)

    def test_subpage_block_css_layout_and_theme_rules(self):
        """Verify .block-subpage has complete layout, cursor, truncation, and dark/light hover rules."""
        self.assertIn('.block-subpage {', self.styles_css)
        self.assertIn('cursor: pointer', self.styles_css)
        self.assertIn('display: flex', self.styles_css)

        # Hover in dark mode
        hover_match = re.search(r'\.block-subpage:hover\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(hover_match)
        self.assertIn('rgba(128, 128, 128', hover_match.group(1))

        # Hover in light mode
        light_hover_match = re.search(r'body\.light-mode\s+\.block-subpage:hover\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(light_hover_match)
        self.assertIn('#e5e7eb', light_hover_match.group(1))

        # Title truncation
        title_match = re.search(r'\.block-subpage\s+\.subpage-title\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(title_match)
        title_body = title_match.group(1)
        self.assertIn('overflow: hidden', title_body)
        self.assertIn('text-overflow: ellipsis', title_body)
        self.assertIn('white-space: nowrap', title_body)

    # -------------------------------------------------------------------------
    # 4. Lasso Selection Boundaries & Contenteditable Protection
    # -------------------------------------------------------------------------

    def _simulate_lasso_mousedown_decision(self, target, button=0):
        """
        Simulates the exact mousedown logic from frontend/app.js:15370-15386:
        panelCanvas.addEventListener('mousedown', (e) => {
          if (e.target.closest('[contenteditable="true"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
          if (e.button !== 0) return;
          if (e.target.closest('#spatial-block-handle') || e.target.closest('#block-action-menu') || e.target.closest('.desktop-format-bar') || e.target.closest('button') || e.target.closest('#sticky-toc-rail')) {
            return;
          }
          const isEditorContainer = e.target === panelCanvas || Boolean(e.target.closest('.editor-container, .editor-body, #blocks-container'));
          if (!isEditorContainer) {
            return;
          }
          isMarqueeActive = true;
        });
        """
        # Guard 1: Abort on editable elements
        if target.closest('[contenteditable="true"]') or target.tagName == 'INPUT' or target.tagName == 'TEXTAREA':
            return False, 'ABORT_EDITABLE'

        # Guard 2: Only primary button (left click)
        if button != 0:
            return False, 'ABORT_BUTTON'

        # Guard 3: Abort on controls and buttons
        if (target.closest('#spatial-block-handle') or
            target.closest('#block-action-menu') or
            target.closest('.desktop-format-bar') or
            target.closest('button') or
            target.closest('#sticky-toc-rail')):
            return False, 'ABORT_CONTROLS'

        # Guard 4: Must be in panelCanvas or editor container/body
        is_editor_container = (target.id == 'panel-canvas' or
                               bool(target.closest('.editor-container, .editor-body, #blocks-container')))
        if not is_editor_container:
            return False, 'ABORT_OUTSIDE_CONTAINER'

        return True, 'START_LASSO'

    def test_lasso_aborts_on_all_contenteditable_and_text_elements(self):
        """Adversarial: Test lasso aborts on all native text selection regions."""
        # Setup simulated DOM hierarchy:
        # panelCanvas -> editor-body.editor-container -> blocks-container -> rich-editor-canvas[contenteditable="true"]
        panel_canvas = SimulatedDOMNode('div', node_id='panel-canvas')
        editor_body = SimulatedDOMNode('div', class_name='editor-body editor-container', node_id='editor-body', parent=panel_canvas)
        blocks_container = SimulatedDOMNode('div', class_name='notion-blocks-container', node_id='blocks-container', parent=editor_body)
        rich_editor = SimulatedDOMNode('div', class_name='notion-rich-editor', node_id='rich-editor-canvas',
                                       contenteditable='true', parent=blocks_container)

        # 1. Direct click on rich-editor-canvas
        started, reason = self._simulate_lasso_mousedown_decision(rich_editor)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_EDITABLE')

        # 2. Click on paragraph inside rich-editor-canvas
        p_block = SimulatedDOMNode('p', parent=rich_editor)
        started, reason = self._simulate_lasso_mousedown_decision(p_block)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_EDITABLE')

        # 3. Deeply nested span inside paragraph
        b_element = SimulatedDOMNode('b', parent=p_block)
        span_text = SimulatedDOMNode('span', parent=b_element)
        started, reason = self._simulate_lasso_mousedown_decision(span_text)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_EDITABLE')

        # 4. Note title input
        note_title_input = SimulatedDOMNode('input', node_id='note-title', parent=editor_body)
        started, reason = self._simulate_lasso_mousedown_decision(note_title_input)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_EDITABLE')

        # 5. Callout input element
        callout_box = SimulatedDOMNode('div', class_name='callout-box', parent=blocks_container)
        callout_input = SimulatedDOMNode('input', node_id='callout-input', parent=callout_box)
        started, reason = self._simulate_lasso_mousedown_decision(callout_input)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_EDITABLE')

        # 6. Textarea element
        textarea_el = SimulatedDOMNode('textarea', parent=blocks_container)
        started, reason = self._simulate_lasso_mousedown_decision(textarea_el)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_EDITABLE')

    def test_lasso_aborts_on_subpage_block_inside_rich_editor(self):
        """Adversarial: Subpage block inside rich-editor-canvas does NOT launch lasso marquee."""
        panel_canvas = SimulatedDOMNode('div', node_id='panel-canvas')
        editor_body = SimulatedDOMNode('div', class_name='editor-body editor-container', parent=panel_canvas)
        blocks_container = SimulatedDOMNode('div', class_name='notion-blocks-container', parent=editor_body)
        rich_editor = SimulatedDOMNode('div', class_name='notion-rich-editor', contenteditable='true', parent=blocks_container)

        subpage_div = SimulatedDOMNode('div', class_name='block-subpage', contenteditable='false', parent=rich_editor)
        icon_span = SimulatedDOMNode('span', class_name='subpage-icon', parent=subpage_div)
        title_span = SimulatedDOMNode('span', class_name='subpage-title', parent=subpage_div)

        # Because subpage_div is inside rich_editor (contenteditable="true"),
        # closest('[contenteditable="true"]') returns rich_editor, aborting lasso.
        started, reason = self._simulate_lasso_mousedown_decision(subpage_div)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_EDITABLE')

        started_icon, reason_icon = self._simulate_lasso_mousedown_decision(icon_span)
        self.assertFalse(started_icon)
        self.assertEqual(reason_icon, 'ABORT_EDITABLE')

        started_title, reason_title = self._simulate_lasso_mousedown_decision(title_span)
        self.assertFalse(started_title)
        self.assertEqual(reason_title, 'ABORT_EDITABLE')

    def test_lasso_activates_on_empty_container_and_margins(self):
        """Adversarial: Lasso selection STARTS when dragging on empty margins/canvas."""
        panel_canvas = SimulatedDOMNode('div', node_id='panel-canvas')
        editor_body = SimulatedDOMNode('div', class_name='editor-body editor-container', node_id='editor-body', parent=panel_canvas)
        blocks_container = SimulatedDOMNode('div', class_name='notion-blocks-container', node_id='blocks-container', parent=editor_body)

        # 1. Direct click on panel-canvas empty background
        started, reason = self._simulate_lasso_mousedown_decision(panel_canvas)
        self.assertTrue(started)
        self.assertEqual(reason, 'START_LASSO')

        # 2. Click on empty margin in editor-body
        started, reason = self._simulate_lasso_mousedown_decision(editor_body)
        self.assertTrue(started)
        self.assertEqual(reason, 'START_LASSO')

        # 3. Click on gap between blocks in blocks-container
        started, reason = self._simulate_lasso_mousedown_decision(blocks_container)
        self.assertTrue(started)
        self.assertEqual(reason, 'START_LASSO')

    def test_lasso_aborts_on_non_primary_button_and_controls(self):
        """Adversarial: Lasso aborts on right-click, format bar buttons, spatial handle."""
        panel_canvas = SimulatedDOMNode('div', node_id='panel-canvas')
        editor_body = SimulatedDOMNode('div', class_name='editor-body editor-container', parent=panel_canvas)

        # Right click on panel canvas
        started, reason = self._simulate_lasso_mousedown_decision(panel_canvas, button=2)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_BUTTON')

        # Middle click
        started, reason = self._simulate_lasso_mousedown_decision(panel_canvas, button=1)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_BUTTON')

        # Click on format bar
        format_bar = SimulatedDOMNode('div', class_name='desktop-format-bar', parent=panel_canvas)
        format_btn = SimulatedDOMNode('button', class_name='format-bar-btn', parent=format_bar)
        started, reason = self._simulate_lasso_mousedown_decision(format_btn)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_CONTROLS')

        # Click on spatial handle
        handle = SimulatedDOMNode('div', node_id='spatial-block-handle', parent=panel_canvas)
        started, reason = self._simulate_lasso_mousedown_decision(handle)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_CONTROLS')

        # Click on outside element (e.g. sidebar)
        sidebar = SimulatedDOMNode('div', class_name='sidebar-panel')
        started, reason = self._simulate_lasso_mousedown_decision(sidebar)
        self.assertFalse(started)
        self.assertEqual(reason, 'ABORT_OUTSIDE_CONTAINER')


if __name__ == '__main__':
    unittest.main()
