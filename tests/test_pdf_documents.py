"""PDF import/reopen and HTTP contract tests; never use the user's database."""
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

import backend
from pdf_documents import MAX_PDF_BYTES, resolve_pdf, store_pdf

PDF = b'%PDF-1.4\n1 0 obj << /Type /Catalog >> endobj\n%%EOF\n'


class PdfDocumentsTest(unittest.TestCase):
    def test_import_reopen_deduplicate_and_keep_original(self):
        with tempfile.TemporaryDirectory() as root:
            first = store_pdf(PDF, root, 'C:\\docs\\Álgebra.pdf')
            second = store_pdf(PDF, root, 'otra-copia.pdf')
            self.assertEqual(first['name'], 'Álgebra.pdf')
            self.assertEqual(first['url'], second['url'])
            self.assertEqual(len(list(Path(root).iterdir())), 1)
            self.assertEqual(resolve_pdf(first['url'].rsplit('/', 1)[1], root).read_bytes(), PDF)
            changed = store_pdf(PDF + b'\n% edit', root)
            self.assertNotEqual(first['url'], changed['url'])
            self.assertEqual(resolve_pdf(first['url'].rsplit('/', 1)[1], root).read_bytes(), PDF)

    def test_reject_invalid_oversized_and_path_traversal(self):
        with tempfile.TemporaryDirectory() as root:
            for data in (b'', b'<html>not a PDF</html>', b'%PDF-' + b' ' * MAX_PDF_BYTES):
                with self.assertRaises(ValueError):
                    store_pdf(data, root)
            for name in ('../notejs.db', '..%2fsecret.pdf', '/notejs.db', 'x.pdf'):
                with self.assertRaises(ValueError):
                    resolve_pdf(name, root)
            self.assertEqual(list(Path(root).iterdir()), [])


class PdfHttpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.patch = patch.object(backend, 'DATA_DIR', cls.temp.name)
        cls.patch.start()
        cls.server = backend.ThreadingHTTPServer(('127.0.0.1', 0), backend.NoteJSRequestHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.patch.stop()
        cls.temp.cleanup()

    def test_upload_read_and_head(self):
        request = urllib.request.Request(self.url + '/api/pdfs?name=manual.pdf', PDF,
                                         {'Content-Type': 'application/pdf', 'Origin': self.url})
        with urllib.request.urlopen(request) as response:
            self.assertEqual(response.status, 201)
            result = json.load(response)
        with urllib.request.urlopen(self.url + result['url']) as response:
            self.assertEqual(response.headers['Content-Type'], 'application/pdf')
            self.assertEqual(response.read(), PDF)
        with urllib.request.urlopen(urllib.request.Request(self.url + result['url'], method='HEAD')) as response:
            self.assertEqual(int(response.headers['Content-Length']), len(PDF))
            self.assertEqual(response.read(), b'')

    def test_upload_rejects_invalid_data_and_foreign_origin(self):
        for data, headers, expected in [
            (b'bad', {'Content-Type': 'application/pdf'}, 400),
            (PDF, {'Content-Type': 'text/plain'}, 400),
            (PDF, {'Content-Type': 'application/pdf', 'Origin': 'https://example.com'}, 403),
            (PDF, {'Content-Type': 'application/pdf', 'Content-Length': str(MAX_PDF_BYTES + 1)}, 413),
        ]:
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(urllib.request.Request(self.url + '/api/pdfs', data, headers))
            self.assertEqual(caught.exception.code, expected)

    def test_missing_pdf_and_bundled_viewer_assets(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(self.url + '/api/pdfs/' + 'a' * 64 + '.pdf')
        self.assertEqual(caught.exception.code, 404)
        for path, mime in [('/pdf-viewer.html', 'text/html'), ('/pdf-viewer.mjs', 'application/javascript'),
                           ('/vendor/pdfjs/build/pdf.worker.mjs', 'application/javascript')]:
            with urllib.request.urlopen(self.url + path) as response:
                self.assertIn(mime, response.headers['Content-Type'])
                self.assertGreater(len(response.read()), 100)


if __name__ == '__main__':
    unittest.main()
