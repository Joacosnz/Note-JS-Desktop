#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Formatting Bar Amber Exclusivity & Focus Mode Removal (Requirement R4)
Validates:
1. Formatting Bar Styling:
   - Syntax error around line 1829 in frontend/styles.css is fixed.
   - .format-bar-btn has neutral default, hover, and active background/color.
   - ONLY #btn-insert-dropdown / .insert-dropdown-btn has amber styling.
   - Non-insert format bar buttons (#btn-in-note-search, #btn-pin-note, #btn-page-appearance,
     #btn-reopen-panels) are excluded from global amber lists in styles.css.
   - Scoped rule .desktop-format-bar .btn-secondary:not(.btn-trash-action) ensures neutral format bar buttons.
   - #btn-pin-note active inline styling in frontend/app.js is neutral (not amber).
2. Focus Mode Indicator Removal:
   - #focus-mode-indicator element is completely removed from frontend/index.html.
   - "Modo Concentración Activo" string is completely removed from frontend/index.html.
   - No references to #focus-mode-indicator remain in frontend/app.js.
"""

import os
import re
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'index.html')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')
APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')


class TestFormattingAndFocus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    # --- Focus Mode Removal Tests ---

    def test_focus_mode_indicator_removed_from_html(self):
        """Verifies #focus-mode-indicator is completely absent from frontend/index.html."""
        self.assertNotIn('id="focus-mode-indicator"', self.index_html)
        self.assertNotIn("id='focus-mode-indicator'", self.index_html)
        self.assertNotIn("Modo Concentración Activo", self.index_html)

    def test_focus_mode_indicator_removed_from_app_js(self):
        """Verifies no references to focus-mode-indicator exist in frontend/app.js."""
        self.assertNotIn('focus-mode-indicator', self.app_js)

    # --- Formatting Bar Styling Tests ---

    def test_syntax_error_fixed_in_styles_css(self):
        """Verifies there is no orphaned bracket or dangling border-color rule in styles.css."""
        # The syntax bug had:
        # .active { ... }
        #   border-color: var(--accent-amber-border);
        # }
        orphaned_pattern = r'\}\s*\n\s*border-color:\s*var\(--accent-amber-border\);\s*\n\s*\}'
        self.assertIsNone(re.search(orphaned_pattern, self.styles_css))

    def test_format_bar_btn_neutral_styles(self):
        """Verifies .format-bar-btn has neutral styling (transparent background, neutral hover)."""
        pattern = r'\.format-bar-btn:not\(\.btn-trash-action\)\s*\{([^}]+)\}'
        match = re.search(pattern, self.styles_css)
        self.assertIsNotNone(match)
        btn_body = match.group(1)
        self.assertIn('background: transparent', btn_body)
        self.assertNotIn('var(--accent-amber-soft)', btn_body)

    def test_insert_dropdown_amber_exclusivity(self):
        """Verifies only #btn-insert-dropdown has amber styles defined."""
        pattern = r'(?:#btn-insert-dropdown|\.insert-dropdown-btn)[^{]*\{([^}]+)\}'
        matches = re.findall(pattern, self.styles_css)
        self.assertTrue(len(matches) > 0, "Insert dropdown button must have amber rules")
        has_amber = any('var(--accent-amber' in m for m in matches)
        self.assertTrue(has_amber, "Insert dropdown button must use accent amber")

    def test_non_insert_buttons_excluded_from_global_amber_lists(self):
        """Verifies #btn-in-note-search, #btn-pin-note, #btn-page-appearance, #btn-reopen-panels are not in global amber lists."""
        # Find the global amber unification block (around section 2 and 3)
        section_idx = self.styles_css.find("Aplica el color amarillo corporativo a todos los botones interactivos")
        self.assertNotEqual(section_idx, -1)
        amber_section = self.styles_css[section_idx:section_idx + 4000]

        self.assertNotIn("#btn-in-note-search", amber_section)
        self.assertNotIn("#btn-pin-note", amber_section)
        self.assertNotIn("#btn-page-appearance", amber_section)
        self.assertNotIn("#btn-reopen-panels", amber_section)
        self.assertIn("#btn-insert-dropdown", amber_section)

    def test_format_bar_btn_excluded_from_global_active_amber_list(self):
        """Verifies format-bar-btn is not in the active amber list."""
        section_idx = self.styles_css.find("/* 3. Botones Activos y Píldoras de Selección */")
        self.assertNotEqual(section_idx, -1)
        active_section = self.styles_css[section_idx:section_idx + 1000]
        self.assertNotIn(".format-bar-btn", active_section)

    def test_desktop_format_bar_scoped_secondary_rule(self):
        """Verifies scoped rule for .desktop-format-bar .btn-secondary ensures neutral appearance."""
        pattern = r'\.desktop-format-bar\s+\.btn-secondary:not\(\.btn-trash-action\)\s*\{([^}]+)\}'
        match = re.search(pattern, self.styles_css)
        self.assertIsNotNone(match, "Must have scoped rule for .desktop-format-bar .btn-secondary:not(.btn-trash-action)")
        rule_body = match.group(1)
        self.assertIn('background: transparent', rule_body)

    def test_pin_note_active_style_in_app_js_neutral(self):
        """Verifies #btn-pin-note inline styling in app.js does not apply amber styles."""
        pin_idx = self.app_js.find("const pinBtn = document.getElementById('btn-pin-note');")
        self.assertNotEqual(pin_idx, -1)
        pin_slice = self.app_js[pin_idx:pin_idx + 700]
        self.assertNotIn("var(--accent-amber)", pin_slice)
        self.assertNotIn("var(--accent-amber-soft)", pin_slice)
        self.assertIn("var(--bg-elevated)", pin_slice)


if __name__ == '__main__':
    unittest.main()
