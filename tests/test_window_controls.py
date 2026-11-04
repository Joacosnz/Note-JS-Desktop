import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import window_controls


class WindowControlsTests(unittest.TestCase):
    def test_windows_uses_work_area_and_actual_window_state(self):
        states = SimpleNamespace(Normal=0, Maximized=2)
        area = object()
        form = SimpleNamespace(WindowState=0, Handle=123)
        form.Invoke = lambda callback: callback()
        window = SimpleNamespace(native=form, _is_maximized=True)
        modules = {
            'System': SimpleNamespace(Action=lambda callback: callback),
            'System.Windows.Forms': SimpleNamespace(
                FormWindowState=states,
                Screen=SimpleNamespace(FromHandle=lambda handle: SimpleNamespace(WorkingArea=area))),
        }
        with patch.object(window_controls.sys, 'platform', 'win32'), patch.dict(sys.modules, modules):
            self.assertEqual(window_controls.toggle_maximize(window)['action'], 'maximize')
            self.assertIs(form.MaximizedBounds, area)
            self.assertEqual(form.WindowState, states.Maximized)
            self.assertEqual(window_controls.toggle_maximize(window)['action'], 'restore')
            self.assertEqual(form.WindowState, states.Normal)
            # Simulate a maximize caused by Windows snapping rather than our button.
            form.WindowState = states.Maximized
            self.assertEqual(window_controls.toggle_maximize(window)['action'], 'restore')

    def test_edit_menu_enabled_without_debug_mode(self):
        settings = SimpleNamespace(AreDefaultContextMenusEnabled=False)
        form = SimpleNamespace(browser=SimpleNamespace(webview=SimpleNamespace(
            CoreWebView2=SimpleNamespace(Settings=settings))))
        form.Invoke = lambda callback: callback()
        with patch.object(window_controls.sys, 'platform', 'win32'), patch.dict(
                sys.modules, {'System': SimpleNamespace(Action=lambda callback: callback)}):
            window_controls.enable_edit_context_menu(SimpleNamespace(native=form))
        self.assertTrue(settings.AreDefaultContextMenusEnabled)


if __name__ == '__main__':
    unittest.main()
