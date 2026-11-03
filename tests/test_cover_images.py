"""Local cover attachments stay durable without inflating note JSON."""
import tempfile
import unittest
from pathlib import Path
from cover_images import MAX_COVER_BYTES, store_cover, resolve_cover


class CoverImagesTest(unittest.TestCase):
    def test_store_deduplicate_and_reopen_by_hash(self):
        data = b'\xff\xd8\xff\xe0fixture\xff\xd9'
        with tempfile.TemporaryDirectory() as directory:
            first = store_cover(data, directory)
            self.assertEqual(first, store_cover(data, directory))
            self.assertEqual(len(list(Path(directory).iterdir())), 1)
            self.assertEqual(resolve_cover(first['url'].split('/')[-1], directory).read_bytes(), data)

    def test_invalid_empty_and_oversized_images_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            for data in (b'', b'not a photo', b'\xff\xd8\xfftruncated', b'\xff\xd8\xff' + b'x' * MAX_COVER_BYTES + b'\xff\xd9'):
                with self.assertRaises(ValueError):
                    store_cover(data, directory)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_only_generated_attachment_names_can_be_resolved(self):
        with tempfile.TemporaryDirectory() as directory:
            for name in ('../notejs.db', '/etc/passwd', 'x.jpg', 'a' * 64 + '.svg'):
                with self.assertRaises(ValueError):
                    resolve_cover(name, directory)
            with self.assertRaises(FileNotFoundError):
                resolve_cover('a' * 64 + '.jpg', directory)
