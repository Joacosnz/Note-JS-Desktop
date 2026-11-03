import unittest
from unittest.mock import Mock, patch
import desktop_app


class MicrosoftWindowTest(unittest.TestCase):
    def test_authentication_window_has_no_local_api_bridge(self):
        main=Mock()
        main.get_current_url.return_value='http://127.0.0.1:3000/'
        with patch.object(desktop_app.webview,'windows',[main]), patch.object(desktop_app.webview,'create_window') as create:
            bridge=desktop_app.PyWebViewBridge()
            self.assertTrue(bridge.open_microsoft_signin()['ok'])
            options=create.call_args.kwargs
            self.assertEqual(options['url'],'http://127.0.0.1:3000/microsoft-signin.html')
            self.assertNotIn('js_api',options)
            self.assertFalse(options['frameless'])

    def test_existing_auth_window_is_reused(self):
        main,child=Mock(),Mock()
        main.get_current_url.return_value='http://localhost:4321/'
        windows=[main]
        with patch.object(desktop_app.webview,'windows',windows), patch.object(desktop_app.webview,'create_window',return_value=child) as create:
            bridge=desktop_app.PyWebViewBridge()
            bridge.open_microsoft_signin()
            windows.append(child)
            bridge.open_microsoft_signin()
            self.assertEqual(create.call_count,1)
            child.show.assert_called_once()

    def test_foreign_page_cannot_launch_a_local_auth_window(self):
        main=Mock()
        main.get_current_url.return_value='https://example.test/'
        with patch.object(desktop_app.webview,'windows',[main]), patch.object(desktop_app.webview,'create_window') as create:
            self.assertFalse(desktop_app.PyWebViewBridge().open_microsoft_signin()['ok'])
            create.assert_not_called()
