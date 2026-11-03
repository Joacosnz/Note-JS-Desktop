#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Independent Victory Verification Test Suite
Executed by the independent Victory Auditor.
Tests all requirements R1, R2, R3, R4 directly and independently.
"""

import os
import sys
import json
import re
import tempfile
import unittest

WORKSPACE_DIR = r"c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop"
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

import models
from peewee import SqliteDatabase


class IndependentVictoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 1. Read frontend files directly
        with open(os.path.join(WORKSPACE_DIR, 'frontend', 'app.js'), 'r', encoding='utf-8') as f:
            cls.app_js = f.read()
        with open(os.path.join(WORKSPACE_DIR, 'frontend', 'index.html'), 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css'), 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()

        # 2. Setup an isolated SQLite database for backend testing
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.db_path = os.path.join(cls.temp_dir.name, 'independent_test.db')
        cls.orig_db = models.db
        cls.test_db = SqliteDatabase(cls.db_path)
        models.db = cls.test_db
        models.BaseModel._meta.database = cls.test_db
        for m in [models.Note, models.Folder, models.Setting, models.NoteHistory,
                  models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord]:
            m._meta.database = cls.test_db
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

    # ----------------------------------------------------
    # R1: Lasso Selection vs Native Text Selection
    # ----------------------------------------------------
    def test_r1_mousedown_first_line_abort_guard(self):
        """Verify that the mousedown listener aborts on editable elements at the very start."""
        pattern = r"panelCanvas\.addEventListener\('mousedown',\s*\(e\)\s*=>\s*\{"
        match = re.search(pattern, self.app_js)
        self.assertIsNotNone(match, "panelCanvas mousedown listener must exist")
        
        # Extract the initial 200 characters of the listener body
        start_idx = match.end()
        body_start = self.app_js[start_idx:start_idx + 350]
        
        expected_guard = "if (e.target.closest('[contenteditable=\"true\"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;"
        self.assertIn(expected_guard, body_start, "Exact required guard clause must be the first operational check in listener")

    def test_r1_editor_container_classes_and_lasso_scoping(self):
        """Verify .editor-container exists on #editor-body and lasso is restricted to empty canvas/margins."""
        # index.html check
        self.assertIn('class="editor-body editor-container"', self.index_html)
        
        # styles.css check
        self.assertIn('.editor-container', self.styles_css)
        
        # app.js check for lasso restriction
        lasso_scope_check = "const isEditorContainer = e.target === panelCanvas || Boolean(e.target.closest('.editor-container, .editor-body, #blocks-container'));"
        self.assertIn(lasso_scope_check, self.app_js)

    # ----------------------------------------------------
    # R2: Sub-note Block Schema & SQLite Persistence
    # ----------------------------------------------------
    def test_r2_sqlite_persistence_roundtrip(self):
        """Verify sub_page blocks are persisted, retrieved, and updated in SQLite without downcasting."""
        note_id = 12345
        subpage_payload = [
            {
                "id": "blk-uuid-victory-1",
                "type": "sub_page",
                "page_id": "target_note_99",
                "title": "Subnota de Auditoría de Victoria",
                "sortIndex": "a0"
            },
            {
                "id": "blk-uuid-victory-2",
                "type": "p",
                "properties": {"text": "Texto regular", "html": "<p>Texto regular</p>"},
                "sortIndex": "a1"
            }
        ]
        
        # 1. Sync blocks into SQLite
        res = models.sync_blocks_from_note_html_orm(note_id, subpage_payload)
        self.assertTrue(res.get('ok'))
        self.assertEqual(res.get('syncedCount'), 2)
        
        # 2. Query blocks back via get_note_blocks_orm
        retrieved = models.get_note_blocks_orm(note_id)
        self.assertTrue(retrieved.get('ok'))
        blocks = retrieved.get('blocks')
        self.assertEqual(len(blocks), 2)
        
        sub_block = next((b for b in blocks if b['id'] == 'blk-uuid-victory-1'), None)
        self.assertIsNotNone(sub_block)
        self.assertEqual(sub_block['type'], 'sub_page')
        self.assertEqual(sub_block['page_id'], 'target_note_99')
        self.assertEqual(sub_block['title'], 'Subnota de Auditoría de Victoria')
        
        # 3. Direct DB inspect to ensure properties column has JSON
        raw_db_row = models.Block.get(models.Block.id == 'blk-uuid-victory-1')
        raw_props = json.loads(raw_db_row.properties)
        self.assertEqual(raw_props['page_id'], 'target_note_99')
        self.assertEqual(raw_props['title'], 'Subnota de Auditoría de Victoria')

    def test_r2_note_signature_detects_block_changes(self):
        """Verify _extract_note_signature detects modifications in note blocks."""
        note_a = {'title': 'N1', 'blocks': [{'id': 'b1', 'type': 'sub_page', 'page_id': 'p1'}]}
        note_b = {'title': 'N1', 'blocks': [{'id': 'b1', 'type': 'sub_page', 'page_id': 'p2'}]}
        sig_a = models._extract_note_signature(note_a)
        sig_b = models._extract_note_signature(note_b)
        self.assertNotEqual(sig_a, sig_b)

    # ----------------------------------------------------
    # R3: Sub-note Block Frontend Rendering & Navigation
    # ----------------------------------------------------
    def test_r3_render_block_subpage_implementation(self):
        """Verify renderBlock handles sub_page, generates .block-subpage with 📄 and onclick loadNote."""
        self.assertIn("case 'sub_page':", self.app_js)
        self.assertIn("div.className = 'block-subpage';", self.app_js)
        self.assertIn("📄", self.app_js)
        self.assertIn("div.setAttribute('contenteditable', 'false');", self.app_js)
        self.assertIn("div.style.cursor = 'pointer';", self.app_js)
        self.assertIn("loadNote(pageId);", self.app_js)

    def test_r3_load_note_functionality(self):
        """Verify window.loadNote is bound and contains standard error handling and navigation."""
        self.assertIn("function loadNote(pageId)", self.app_js)
        self.assertIn("window.loadNote = loadNote;", self.app_js)
        self.assertIn("selectNote(note.id);", self.app_js)
        self.assertIn("ID de nota inválido", self.app_js)
        self.assertIn("Nota no encontrada", self.app_js)
        self.assertIn("Restaura la nota desde la papelera", self.app_js)

    def test_r3_subpage_css_properties(self):
        """Verify .block-subpage CSS rules exist with pointer cursor and light gray hover."""
        self.assertIn(".block-subpage", self.styles_css)
        self.assertIn("cursor: pointer;", self.styles_css)
        self.assertIn("rgba(128, 128, 128, 0.12)", self.styles_css)
        self.assertIn("#e5e7eb", self.styles_css)

    # ----------------------------------------------------
    # R4: Format Bar Amber Exclusivity & Focus Mode Removal
    # ----------------------------------------------------
    def test_r4_focus_mode_indicator_completely_absent(self):
        """Verify #focus-mode-indicator and 'Modo Concentración' are completely removed from frontend files."""
        for name, content in [('index.html', self.index_html), ('app.js', self.app_js), ('styles.css', self.styles_css)]:
            self.assertNotIn('focus-mode-indicator', content, f"focus-mode-indicator must not be in {name}")
            self.assertNotIn('modo concentración', content.lower(), f"Modo Concentración must not be in {name}")

    def test_r4_format_bar_amber_exclusivity(self):
        """Verify that in .desktop-format-bar ONLY #btn-insert-dropdown / .insert-dropdown-btn has amber styling."""
        # 1. Check insert button has amber
        self.assertIn("#btn-insert-dropdown", self.styles_css)
        self.assertIn(".insert-dropdown-btn", self.styles_css)
        
        # 2. Check format bar default buttons have transparent/neutral background
        self.assertIn(".desktop-format-bar .btn-secondary:not(.btn-trash-action)", self.styles_css)
        self.assertIn("background: transparent !important;", self.styles_css)
        
        # 3. Check non-insert buttons are removed from amber section in styles.css
        # Check that none of the other toolbar buttons are in the amber rule selector
        non_insert_buttons = ["#btn-in-note-search", "#btn-pin-note", "#btn-page-appearance", "#btn-reopen-panels"]
        
        # Find global amber section
        amber_idx = self.styles_css.find("/* 2. Botones Secundarios, Cancelar y Acciones Generales */")
        amber_section = self.styles_css[amber_idx:amber_idx + 2500]
        for btn in non_insert_buttons:
            self.assertNotIn(btn, amber_section, f"{btn} must not be styled with amber")


if __name__ == '__main__':
    unittest.main()
