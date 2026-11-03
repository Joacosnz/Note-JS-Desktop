#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite: Frameless Window, Top Bar Styling, and Home Button Neutrality
Verifies the fixes for:
1. Double titlebar elimination: frameless=True in desktop_app.py
2. Neutral Home button: .chrome-home-btn is NOT solid amber when resting or active
3. Zero-tab start cleanliness: No fake 'Sin notas abiertas' tab pill
4. Clutter-free top bar: Hidden stray shortcut button and redundant chevron picker
"""

import os
import re
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESKTOP_APP_PATH = os.path.join(WORKSPACE_DIR, 'desktop_app.py')
INDEX_HTML_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'index.html')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')
APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')


class TestFramelessAndTopbarFixes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(DESKTOP_APP_PATH, 'r', encoding='utf-8') as f:
            cls.desktop_app = f.read()
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()

    def test_desktop_app_is_frameless(self):
        """desktop_app.py must configure create_window with frameless=True to eliminate duplicate titlebars."""
        self.assertIn('frameless=True', self.desktop_app)
        self.assertIn('easy_drag=False', self.desktop_app)

    def test_top_bar_has_drag_region(self):
        """index.html header.top-bar must have pywebview-drag-region class."""
        self.assertIn('pywebview-drag-region', self.index_html)
        self.assertIn('-webkit-app-region: drag;', self.styles_css)
        self.assertIn('-webkit-app-region: no-drag;', self.styles_css)

    def test_home_button_is_neutral_when_active(self):
        """Home button (.chrome-home-btn) must NOT be amber by default or when .active."""
        # Find all occurrences of .chrome-home-btn.active in styles.css
        # Verify it has transparent or subtle translucent background, NOT solid var(--accent-amber)
        active_rules = re.findall(r'\.chrome-home-btn\.active\s*\{([^}]+)\}', self.styles_css)
        self.assertTrue(len(active_rules) > 0, "Expected .chrome-home-btn.active styling rules in CSS")
        for rule in active_rules:
            self.assertNotIn(
                'var(--accent-amber) !important',
                rule,
                ".chrome-home-btn.active must never have solid amber background"
            )

    def test_empty_tabs_cleanliness(self):
        """renderNoteTabs in app.js must clear listEl and NOT render fake 'Sin notas abiertas' tab."""
        self.assertNotIn('Sin notas abiertas', self.app_js)
        # Should clear listEl when openTabIds is empty
        self.assertIn('if (!state.openTabIds.length) {\n        listEl.innerHTML = \'\';\n        return;\n      }', self.app_js)

    def test_top_bar_clutter_hidden(self):
        """Redundant picker chevron and top shortcuts button are hidden to match reference image."""
        self.assertIn('#btn-tab-picker', self.styles_css)
        self.assertIn('.top-actions', self.styles_css)
        # Verify display: none is applied to picker wrap and top actions
        hidden_pattern = re.search(r'(?:#btn-tab-picker|note-tab-picker-wrap|top-actions)[\s\S]*?display:\s*none', self.styles_css)
        self.assertIsNotNone(hidden_pattern, "Expected display: none for top bar clutter")

    def test_global_sleek_dark_scrollbar(self):
        """Webview must define dark color-scheme and sleek custom scrollbars to prevent white Windows scrollbars."""
        self.assertIn('color-scheme: dark;', self.styles_css)
        self.assertIn('::-webkit-scrollbar', self.styles_css)
        self.assertIn('::-webkit-scrollbar-thumb', self.styles_css)
        self.assertIn('border-radius: 9999px;', self.styles_css)

    def test_sticky_toc_card_solid_background(self):
        """.sticky-toc-popover must have solid elevated background to prevent note text bleed-through."""
        toc_match = re.search(r'\.sticky-toc-popover\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(toc_match)
        rules = toc_match.group(1)
        self.assertIn('background:', rules)
        self.assertNotIn('background: transparent', rules)
        self.assertIn('box-shadow:', rules)
        self.assertIn('border-radius:', rules)

    def test_insert_button_svg_plus_centering(self):
        """.insert-plus-sign must contain an SVG plus icon with flexbox centering."""
        self.assertIn('<span class="insert-plus-sign"', self.index_html)
        plus_btn_match = re.search(r'<span class="insert-plus-sign"[^>]*>([\s\S]*?)</span>', self.index_html)
        self.assertIsNotNone(plus_btn_match)
        inner = plus_btn_match.group(1)
        self.assertIn('<svg', inner)
        self.assertIn('<line x1="12" y1="5" x2="12" y2="19"></line>', inner)
        self.assertIn('<line x1="5" y1="12" x2="19" y2="12"></line>', inner)


if __name__ == '__main__':
    unittest.main()
