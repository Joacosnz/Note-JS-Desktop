import os
import sys
import json
import tempfile
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, WORKSPACE_DIR)

import models
from peewee import SqliteDatabase

class TestIndependentAdversarialR1R2R3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.db_path = os.path.join(cls.temp_dir.name, 'indep_test.db')
        cls.original_db = models.db
        cls.test_db = SqliteDatabase(cls.db_path)
        models.db = cls.test_db
        models.BaseModel._meta.database = cls.test_db
        for m in [models.Note, models.Folder, models.Setting, models.NoteHistory,
                  models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord]:
            m._meta.database = cls.test_db
        cls.test_db.connect()
        cls.test_db.create_tables([models.Note, models.Block])

    @classmethod
    def tearDownClass(cls):
        try:
            if not cls.test_db.is_closed():
                cls.test_db.close()
            cls.temp_dir.cleanup()
        except Exception:
            pass
        finally:
            models.db = cls.original_db
            models.BaseModel._meta.database = cls.original_db

    def test_r2_sqlite_persistence_various_types(self):
        note = models.Note.create(
            id=2001,
            title="Note R2 Test",
            folder="General",
            category="General",
            pinned=0,
            is_trashed=0,
            has_cover=0,
            created_at=1000,
            updated_at=1000
        )
        
        # Test 1: standard UUID string page_id
        blocks = [
            {
                "id": "blk-sub-str",
                "type": "sub_page",
                "page_id": "note-target-123",
                "title": "Subpage String ID"
            },
            # Test 2: integer page_id
            {
                "id": "blk-sub-int",
                "type": "sub_page",
                "page_id": 9999,
                "title": "Subpage Int ID"
            },
            # Test 3: camelCase pageId
            {
                "id": "blk-sub-camel",
                "type": "sub_page",
                "pageId": "note-target-456",
                "title": "Subpage Camel ID"
            },
            # Test 4: Unicode & emojis
            {
                "id": "blk-sub-unicode",
                "type": "sub_page",
                "page_id": "note-target-emoji",
                "title": "Subpage 📄 Emojis & Español (áéíóú, ñ)"
            }
        ]

        res = models.sync_blocks_from_note_html_orm(note.id, blocks)
        self.assertTrue(res['ok'])
        self.assertEqual(res['syncedCount'], 4)

        retrieved = models.get_note_blocks_orm(note.id)
        self.assertTrue(retrieved['ok'])
        retrieved_map = {b['id']: b for b in retrieved['blocks']}

        # Verify Test 1
        b1 = retrieved_map['blk-sub-str']
        self.assertEqual(b1['type'], 'sub_page')
        self.assertEqual(b1['page_id'], 'note-target-123')
        self.assertEqual(b1['title'], 'Subpage String ID')

        # Verify Test 2
        b2 = retrieved_map['blk-sub-int']
        self.assertEqual(b2['type'], 'sub_page')
        self.assertEqual(b2['page_id'], 9999)
        self.assertEqual(b2['title'], 'Subpage Int ID')

        # Verify Test 3
        b3 = retrieved_map['blk-sub-camel']
        self.assertEqual(b3['type'], 'sub_page')
        self.assertEqual(b3['page_id'], 'note-target-456')
        self.assertEqual(b3['title'], 'Subpage Camel ID')

        # Verify Test 4
        b4 = retrieved_map['blk-sub-unicode']
        self.assertEqual(b4['type'], 'sub_page')
        self.assertEqual(b4['page_id'], 'note-target-emoji')
        self.assertEqual(b4['title'], 'Subpage 📄 Emojis & Español (áéíóú, ñ)')

    def test_r2_corrupted_properties_json_resilience(self):
        # Create block directly with malformed JSON
        b = models.Block.create(
            id='blk-corrupted',
            note_id=2001,
            parent_id=None,
            type='sub_page',
            properties='{invalid-json!@@#$',
            sort_index='z9'
        )
        data = b.to_dict()
        self.assertEqual(data['id'], 'blk-corrupted')
        self.assertEqual(data['type'], 'sub_page')
        self.assertIsNone(data.get('page_id'))
        self.assertEqual(data.get('title'), '')

    def test_integrity_no_dummy_or_facade_implementations(self):
        # Check models.py for real database calls
        import inspect
        sync_src = inspect.getsource(models.sync_blocks_from_note_html_orm)
        self.assertIn("Block.get_or_none", sync_src)
        self.assertIn("blk.save()", sync_src)
        self.assertIn("Block.create", sync_src)

        batch_src = inspect.getsource(models.update_batch_blocks_order_orm)
        self.assertIn("Block.get_or_none", batch_src)
        self.assertIn("blk.save()", batch_src)
        self.assertIn("Block.create", batch_src)

if __name__ == '__main__':
    unittest.main()
