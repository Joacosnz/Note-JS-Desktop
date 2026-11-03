#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Sub-note Block Schema and SQLite Persistence (Requirement R2)
Verifies:
1. Block.to_dict() exposes top-level page_id and title when type == 'sub_page' or page_id in props.
2. sync_blocks_from_note_html_orm preserves top-level page_id and title in properties JSON.
3. update_batch_blocks_order_orm preserves top-level page_id and title.
4. get_note_blocks_orm returns sub_page blocks accurately without downcasting to plain text.
5. _extract_note_signature includes 'blocks'.
"""

import os
import sys
import json
import tempfile
import unittest
from peewee import SqliteDatabase

# Ensure workspace root is in sys.path
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

import models


class TestBackendSubpagePersistence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary SQLite database for test isolation
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = os.path.join(cls.temp_dir.name, 'test_notejs.db')
        cls.original_db = models.db
        
        # Configure Peewee test database
        cls.test_db = SqliteDatabase(cls.test_db_path)
        models.db = cls.test_db
        models.BaseModel._meta.database = cls.test_db
        for model in [models.Note, models.Folder, models.Setting, models.NoteHistory,
                      models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord]:
            model._meta.database = cls.test_db

        cls.test_db.connect()
        cls.test_db.create_tables([
            models.Note, models.Folder, models.Setting, models.NoteHistory,
            models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord
        ])

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
            for model in [models.Note, models.Folder, models.Setting, models.NoteHistory,
                          models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord]:
                model._meta.database = cls.original_db

    def setUp(self):
        # Clean Block and Note tables before each test
        models.Block.delete().execute()
        models.Note.delete().execute()

    def test_block_to_dict_exposes_subpage_keys(self):
        """Test that Block.to_dict exposes page_id and title at top level for sub_page blocks."""
        blk = models.Block(
            id='blk-sub-001',
            note_id=100,
            parent_id=None,
            type='sub_page',
            properties=json.dumps({
                'page_id': 'note-200',
                'title': 'Investigación Arquitectura'
            }),
            sort_index='a0'
        )
        data = blk.to_dict()
        self.assertEqual(data['id'], 'blk-sub-001')
        self.assertEqual(data['type'], 'sub_page')
        self.assertEqual(data['page_id'], 'note-200')
        self.assertEqual(data['title'], 'Investigación Arquitectura')
        self.assertIn('properties', data)
        self.assertEqual(data['properties']['page_id'], 'note-200')

    def test_block_to_dict_fallback_page_id_in_props(self):
        """Test that if type is not sub_page but page_id is in props, it still exposes page_id."""
        blk = models.Block(
            id='blk-sub-002',
            note_id=100,
            parent_id=None,
            type='custom_card',
            properties=json.dumps({
                'page_id': 'note-300',
                'title': 'Nota vinculada'
            }),
            sort_index='a1'
        )
        data = blk.to_dict()
        self.assertEqual(data['page_id'], 'note-300')
        self.assertEqual(data['title'], 'Nota vinculada')

    def test_sync_blocks_preserves_subpage_payload(self):
        """Test sync_blocks_from_note_html_orm preserves top-level page_id and title."""
        note_id = 555
        incoming_blocks = [
            {
                'id': 'blk-uuid-test-1',
                'type': 'sub_page',
                'page_id': 'target_note_999',
                'title': 'Sub-nota Proyecto Q4',
                'sortIndex': 'a0'
            },
            {
                'id': 'blk-uuid-test-2',
                'type': 'p',
                'properties': {'text': 'Párrafo de prueba', 'html': '<p>Párrafo de prueba</p>'},
                'sortIndex': 'a1'
            }
        ]

        result = models.sync_blocks_from_note_html_orm(note_id, incoming_blocks)
        self.assertTrue(result['ok'])
        self.assertEqual(result['syncedCount'], 2)

        # Retrieve blocks from SQLite via get_note_blocks_orm
        retrieved = models.get_note_blocks_orm(note_id)
        self.assertTrue(retrieved['ok'])
        self.assertEqual(len(retrieved['blocks']), 2)

        sub_block = next((b for b in retrieved['blocks'] if b['id'] == 'blk-uuid-test-1'), None)
        self.assertIsNotNone(sub_block, "Subpage block should be persisted in SQLite")
        self.assertEqual(sub_block['type'], 'sub_page')
        self.assertEqual(sub_block['page_id'], 'target_note_999')
        self.assertEqual(sub_block['title'], 'Sub-nota Proyecto Q4')

        # Verify inside raw database properties column
        raw_db_row = models.Block.get(models.Block.id == 'blk-uuid-test-1')
        raw_props = json.loads(raw_db_row.properties)
        self.assertEqual(raw_props['page_id'], 'target_note_999')
        self.assertEqual(raw_props['title'], 'Sub-nota Proyecto Q4')

    def test_update_batch_blocks_order_preserves_subpage(self):
        """Test update_batch_blocks_order_orm preserves sub_page properties."""
        moves = [
            {
                'id': 'blk-batch-sub-1',
                'noteId': 888,
                'type': 'sub_page',
                'page_id': 'target-note-777',
                'title': 'Subnota en Lote',
                'sortIndex': 'a5'
            }
        ]

        result = models.update_batch_blocks_order_orm(moves)
        self.assertTrue(result['ok'])
        self.assertEqual(result['updatedCount'], 1)

        saved_blk = result['blocks'][0]
        self.assertEqual(saved_blk['type'], 'sub_page')
        self.assertEqual(saved_blk['page_id'], 'target-note-777')
        self.assertEqual(saved_blk['title'], 'Subnota en Lote')

    def test_extract_note_signature_includes_blocks(self):
        """Test _extract_note_signature includes blocks list for state comparison."""
        note_without_blocks = {'title': 'Nota 1', 'blocks': []}
        note_with_blocks = {'title': 'Nota 1', 'blocks': [{'id': 'b1', 'type': 'sub_page', 'page_id': 'p2'}]}

        sig1 = models._extract_note_signature(note_without_blocks)
        sig2 = models._extract_note_signature(note_with_blocks)

        self.assertIn('"blocks": []', sig1)
        self.assertIn('"blocks": [{"id": "b1"', sig2)
        self.assertNotEqual(sig1, sig2, "Changing blocks must produce different note signatures")


if __name__ == '__main__':
    unittest.main()
