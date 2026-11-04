"""Exercise the real HTTP boundary without reading or modifying user notes."""
import http.client
import io
import tempfile
import threading
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import backend


class HttpBoundaryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = backend.ThreadingHTTPServer(('127.0.0.1', 0), backend.NoteJSRequestHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, headers=None, method='GET'):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=3)
        try:
            connection.request(method, '/health', headers=headers or {})
            response = connection.getresponse()
            response.read()
            return response.status, response.headers
        finally:
            connection.close()

    def test_local_health_and_headers(self):
        origin = f'http://127.0.0.1:{self.server.server_port}'
        status, headers = self.request({'Origin': origin})
        self.assertEqual(status, 200)
        self.assertIsNone(headers.get('Access-Control-Allow-Origin'))
        self.assertEqual(headers['Referrer-Policy'], 'no-referrer')
        self.assertEqual(headers['Cross-Origin-Resource-Policy'], 'same-origin')

    def test_browser_attacks_blocked_for_all_methods(self):
        for method in ('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'):
            for headers in ({'Origin': 'https://attacker.test'}, {'Origin': 'null'},
                            {'Host': 'attacker.test'}, {'Sec-Fetch-Site': 'cross-site'},
                            {'Sec-Fetch-Site': 'same-site'}):
                with self.subTest(method=method, headers=headers):
                    self.assertEqual(self.request(headers, method)[0], 403)

    def test_bad_framing_rejected_before_read(self):
        for headers, status in [({'Content-Length': '-1'}, 400),
                                ({'Content-Length': 'invalid'}, 400),
                                ({'Transfer-Encoding': 'chunked'}, 400),
                                ({'Content-Length': str(backend.NoteJSRequestHandler.MAX_REQUEST_BYTES + 1)}, 413)]:
            self.assertEqual(self.request(headers, 'POST')[0], status)

    def test_remote_bind_rejected(self):
        with self.assertRaises(ValueError):
            backend.run_server(port=0, host='0.0.0.0')


class DistributionPrivacyTest(unittest.TestCase):
    def test_source_zip_excludes_private_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'notejs.db').write_bytes(b'private database')
            for kind in ('pdfs', 'covers'):
                folder = root / 'attachments' / kind
                folder.mkdir(parents=True)
                (folder / 'private.txt').write_text('private attachment')
            with patch.multiple(backend, BASE_DIR=directory, FRONTEND_DIR=directory,
                                DATA_DIR=directory, DB_PATH=str(root / 'notejs.db')):
                archive = backend.build_vscode_project_zip()
            with zipfile.ZipFile(io.BytesIO(archive)) as zf:
                self.assertFalse(any('notejs.db' in name or 'attachments/' in name for name in zf.namelist()))


if __name__ == '__main__':
    unittest.main()
