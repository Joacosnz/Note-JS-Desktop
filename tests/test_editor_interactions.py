#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Editor Interactions: Selection Conflict (R1) & Sub-note Frontend Rendering (R3)
Validates:
1. R1 Selection Conflict:
   - mousedown handler in frontend/app.js aborts immediately on editable elements
     ([contenteditable="true"], INPUT, TEXTAREA).
   - frontend/index.html includes 'editor-container' in #editor-body.
   - frontend/styles.css includes '.editor-container' styling.
   - Lasso initiation is strictly restricted to panelCanvas or .editor-container / margins.
2. R3 Sub-note Frontend Rendering & Navigation:
   - renderBlock(block) with case 'sub_page' creates .block-subpage with 📄 and title,
     contenteditable="false", and onclick loadNote.
   - renderBlocks and attachSubpageBlockListeners are implemented.
   - loadActiveNote invokes attachSubpageBlockListeners.
   - loadNote(pageId) is attached to window with validation and error toasts.
   - collectAndSyncNoteBlocks preserves type: 'sub_page', page_id, and title.
   - insertSubpageBlock inserts .block-subpage component.
   - frontend/styles.css defines .block-subpage with pointer cursor, flex alignment, and hover effects.
"""

import os
import re
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
INDEX_HTML_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'index.html')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')


class TestEditorInteractions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()

    # --- R1: Selection Conflict Tests ---

    def test_r1_selection_guard_aborts_on_editable_elements(self):
        """Verifies mousedown handler in initSpatialBlockController aborts on editable elements on the first line."""
        # Find initSpatialBlockController and its mousedown handler
        self.assertIn("function initSpatialBlockController()", self.app_js)
        
        # Check the exact guard clause
        guard_pattern = r"if\s*\(\s*e\.target\.closest\(\s*['\"]\[contenteditable=[\"']true[\"']\]['\"]\s*\)\s*\|\|\s*e\.target\.tagName\s*===\s*['\"]INPUT['\"]\s*\|\|\s*e\.target\.tagName\s*===\s*['\"]TEXTAREA['\"]\s*\)\s*return;"
        match = re.search(guard_pattern, self.app_js)
        self.assertIsNotNone(match, "Mousedown listener must abort immediately if target is inside contenteditable, INPUT, or TEXTAREA")

    def test_r1_editor_container_in_index_html(self):
        """Verifies editor-container class is added to #editor-body in index.html."""
        pattern = r'<div\s+id=["\']editor-body["\']\s+class=["\'][^"\']*editor-container[^"\']*["\']'
        match = re.search(pattern, self.index_html)
        self.assertIsNotNone(match, "<div id='editor-body'> must include class 'editor-container'")

    def test_r1_editor_container_in_styles_css(self):
        """Verifies .editor-container is included in styles.css with layout rules."""
        pattern = r'\.editor-body\s*,\s*\.editor-container\s*\{'
        match = re.search(pattern, self.styles_css)
        self.assertIsNotNone(match, "styles.css must style .editor-container along with .editor-body")

    def test_r1_lasso_restricted_to_empty_canvas_and_editor_container(self):
        """Verifies marquee lasso only starts when clicking panelCanvas or within .editor-container background."""
        self.assertIn("isEditorContainer", self.app_js)
        pattern = r"const\s+isEditorContainer\s*=\s*e\.target\s*===\s*panelCanvas\s*\|\|\s*Boolean\(e\.target\.closest\(['\"].*?\.editor-container"
        match = re.search(pattern, self.app_js)
        self.assertIsNotNone(match, "Lasso activation must check panelCanvas or .editor-container empty background")

    # --- R3: Sub-note Frontend Rendering & Navigation Tests ---

    def test_r3_render_block_subpage_case(self):
        """Verifies renderBlock includes switch (block.type) with case 'sub_page'."""
        self.assertIn("function renderBlock(block)", self.app_js)
        self.assertIn("case 'sub_page':", self.app_js)
        self.assertIn("block-subpage", self.app_js)
        self.assertIn("📄", self.app_js)
        self.assertIn("subpage-title", self.app_js)
        self.assertIn("loadNote(pageId)", self.app_js)

    def test_r3_render_blocks_and_listener_attachment(self):
        """Verifies renderBlocks and attachSubpageBlockListeners exist."""
        self.assertIn("function renderBlocks(blocks", self.app_js)
        self.assertIn("function attachSubpageBlockListeners()", self.app_js)
        self.assertIn("window.renderBlock = renderBlock", self.app_js)
        self.assertIn("window.renderBlocks = renderBlocks", self.app_js)
        self.assertIn("window.attachSubpageBlockListeners = attachSubpageBlockListeners", self.app_js)

    def test_r3_load_active_note_invokes_attach_subpage_listeners(self):
        """Verifies loadActiveNote invokes attachSubpageBlockListeners()."""
        # In loadActiveNote, attachSubpageBlockListeners must be called
        load_note_idx = self.app_js.find("function loadActiveNote()")
        self.assertNotEqual(load_note_idx, -1)
        sub_slice = self.app_js[load_note_idx:load_note_idx + 5000]
        self.assertIn("attachSubpageBlockListeners()", sub_slice)

    def test_r3_load_note_implementation_and_window_binding(self):
        """Verifies window.loadNote exists with error handling for empty ID, not found, and trashed notes."""
        self.assertIn("function loadNote(pageId)", self.app_js)
        self.assertIn("window.loadNote = loadNote", self.app_js)
        self.assertIn("ID de nota inválido", self.app_js)
        self.assertIn("Nota no encontrada", self.app_js)
        self.assertIn("Restaura la nota desde la papelera", self.app_js)
        self.assertIn("selectNote(note.id)", self.app_js)

    def test_r3_collect_and_sync_preserves_subpage_type_and_keys(self):
        """Verifies collectAndSyncNoteBlocks preserves type: 'sub_page', page_id, and title."""
        sync_fn_idx = self.app_js.find("function collectAndSyncNoteBlocks(noteId)")
        self.assertNotEqual(sync_fn_idx, -1)
        sync_slice = self.app_js[sync_fn_idx:sync_fn_idx + 1500]
        self.assertIn("block-subpage", sync_slice)
        self.assertIn("sub_page", sync_slice)
        self.assertIn("data-page-id", sync_slice)
        self.assertIn("blockObj.page_id", sync_slice)
        self.assertIn("blockObj.title", sync_slice)

    def test_r3_insert_subpage_block_component(self):
        """Verifies insertSubpageBlock inserts .block-subpage component."""
        insert_fn_idx = self.app_js.find("function insertSubpageBlock()")
        self.assertNotEqual(insert_fn_idx, -1)
        insert_slice = self.app_js[insert_fn_idx:insert_fn_idx + 2000]
        self.assertIn("renderBlock", insert_slice)
        self.assertIn("type: 'sub_page'", insert_slice)
        self.assertIn("attachSubpageBlockListeners()", insert_slice)

    def test_r3_subpage_css_styles(self):
        """Verifies .block-subpage styling in styles.css."""
        self.assertIn(".block-subpage", self.styles_css)
        self.assertIn("cursor: pointer", self.styles_css)
        self.assertIn("rgba(128, 128, 128, 0.12)", self.styles_css)
        self.assertIn("#e5e7eb", self.styles_css)
        self.assertIn(".subpage-icon", self.styles_css)
        self.assertIn(".subpage-title", self.styles_css)


if __name__ == '__main__':
    unittest.main()
