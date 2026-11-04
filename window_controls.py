"""Shared native window actions for the bridge and HTTP API."""
import sys


def toggle_maximize(window):
    if sys.platform == 'win32' and getattr(window, 'native', None) is not None:
        from System import Action
        from System.Windows.Forms import FormWindowState, Screen

        result = {}

        def toggle():
            form = window.native
            # Borderless forms otherwise maximize over the Windows taskbar.
            form.MaximizedBounds = Screen.FromHandle(form.Handle).WorkingArea
            maximized = form.WindowState != FormWindowState.Maximized
            form.WindowState = (FormWindowState.Maximized if maximized
                                else FormWindowState.Normal)
            window._is_maximized = maximized
            result.update(ok=True, action='maximize' if maximized else 'restore',
                          is_maximized=maximized)

        window.native.Invoke(Action(toggle))
        return result

    maximized = not getattr(window, '_is_maximized', False)
    (window.maximize if maximized else window.restore)()
    window._is_maximized = maximized
    return {'ok': True, 'action': 'maximize' if maximized else 'restore',
            'is_maximized': maximized}


def enable_edit_context_menu(window):
    """Keep native Cut/Copy/Paste available where no app menu handles the event."""
    if sys.platform != 'win32':
        return
    from System import Action

    def configure():
        window.native.browser.webview.CoreWebView2.Settings.AreDefaultContextMenusEnabled = True

    window.native.Invoke(Action(configure))
