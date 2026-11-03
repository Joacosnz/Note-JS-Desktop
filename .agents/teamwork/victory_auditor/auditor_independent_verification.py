#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Independent Victory Auditor Verification Script
Tests all acceptance criteria directly against live models and SQLite database.
"""

import os
import sys
import json
import uuid
import tempfile
import unittest
from peewee import SqliteDatabase

# Import workspace modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
import models
import rich_text
import backend

class IndependentVictoryVerification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.db_path = os.path.join(cls.temp_dir.name, 'auditor_victory_test.db')
        cls.orig_db = models.db
        cls.test_db = SqliteDatabase(cls.db_path, timeout=10, check_same_thread=False)
        models.db = cls.test_db
        models.BaseModel._meta.database = cls.test_db

        for m in [
            models.Note, models.Folder, models.Setting, models.NoteHistory,
            models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord
        ]:
            m._meta.database = cls.test_db

        cls.test_db.connect(reuse_if_open=True)
        models.init_db()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.test_db.close()
        except Exception:
            pass
        try:
            cls.temp_dir.cleanup()
        except Exception:
            pass
        models.db = cls.orig_db
        models.BaseModel._meta.database = cls.orig_db
        for m in [
            models.Note, models.Folder, models.Setting, models.NoteHistory,
            models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord
        ]:
            m._meta.database = cls.orig_db

    def test_criterion_1_atomic_transactional_protocol(self):
        """Verifies concurrent op.set and op.listAfter executed atomically with rollback."""
        parent_id = str(uuid.uuid4())
        child_id = str(uuid.uuid4())

        # Create parent container
        parent_data = rich_text.create_default_block('page', block_id=parent_id)
        op_set_parent = models.build_op_set(parent_id, parent_data)
        models.apply_transaction([op_set_parent])

        # Atomic child creation: op.set + op.listAfter
        child_data = rich_text.create_default_block('text', block_id=child_id, parent_id=parent_id)
        child_data['properties'] = {'title': [['Independent Victory Test', []]]}
        op_set_child = models.build_op_set(child_id, child_data)
        op_list_after = models.build_op_list_after(parent_id, child_id)

        res = models.apply_transaction([op_set_child, op_list_after])
        self.assertTrue(res.get('ok'))

        # Verify parent content has child_id
        parent_db = models.Block.get_by_id(parent_id)
        parent_content = json.loads(parent_db.content or '[]')
        self.assertIn(child_id, parent_content)

        # Verify child row exists and fields are correct
        child_db = models.Block.get_by_id(child_id)
        self.assertEqual(child_db.parent_id, parent_id)
        self.assertEqual(child_db.type, 'text')
        props = json.loads(child_db.properties)
        self.assertEqual(props['title'][0][0], 'Independent Victory Test')

        # Test Rollback: if 2nd op fails, 1st op must NOT persist
        child2_id = str(uuid.uuid4())
        child2_data = rich_text.create_default_block('text', block_id=child2_id, parent_id=parent_id)
        op_set_child2 = models.build_op_set(child2_id, child2_data)
        # Invalid op targeting non-existent parent
        op_invalid = models.build_op_list_after(str(uuid.uuid4()), child2_id)

        with self.assertRaises(ValueError):
            models.apply_transaction([op_set_child2, op_invalid])

        # Verify child2 was rolled back
        self.assertIsNone(models.Block.get_or_none(models.Block.id == child2_id))

    def test_criterion_2_container_vs_leaf_structural_rules(self):
        """Verifies leaf blocks strictly enforce content: null and reject children."""
        leaf_types = [
            'equation', 'divider', 'code', 'image', 'video',
            'audio', 'file', 'pdf', 'bookmark', 'table_row',
            'transclusion_reference', 'sub_page'
        ]

        for ltype in leaf_types:
            leaf_id = str(uuid.uuid4())
            leaf_data = rich_text.create_default_block(ltype, block_id=leaf_id)
            self.assertIsNone(leaf_data['content'], f"Leaf {ltype} default content must be None (null)")

            # Save leaf to DB
            op_set = models.build_op_set(leaf_id, leaf_data)
            models.apply_transaction([op_set])

            # Try to add child to leaf -> must raise ValueError
            child_id = str(uuid.uuid4())
            child_data = rich_text.create_default_block('text', block_id=child_id)
            with self.assertRaises(ValueError, msg=f"Leaf {ltype} allowed child addition!"):
                models.add_child_block(leaf_id, child_data)

            # Try direct listAfter on leaf -> must raise ValueError
            op_list = models.build_op_list_after(leaf_id, child_id)
            with self.assertRaises(ValueError, msg=f"Leaf {ltype} allowed direct op.listAfter!"):
                models.apply_transaction([op_list])

    def test_criterion_3_toggleable_headers_dynamic_validation(self):
        """Verifies headers allow children if and only if format.toggleable = True."""
        header_types = ['header', 'sub_header', 'sub_sub_header', 'header_4']

        for htype in header_types:
            hid = str(uuid.uuid4())
            hdata = rich_text.create_default_block(htype, block_id=hid)
            # By default toggleable is False/unset
            op_set = models.build_op_set(hid, hdata)
            models.apply_transaction([op_set])

            # Should reject children
            child_id = str(uuid.uuid4())
            child_data = rich_text.create_default_block('text', block_id=child_id)
            with self.assertRaises(ValueError, msg=f"Non-toggleable {htype} allowed children!"):
                models.add_child_block(hid, child_data)

            # Now update to format.toggleable = True
            hdata['format']['toggleable'] = True
            op_update = models.build_op_set(hid, hdata)
            models.apply_transaction([op_update])

            # Now adding child MUST succeed
            child = models.add_child_block(hid, child_data)
            self.assertIsNotNone(child)
            h_refreshed = models.Block.get_by_id(hid)
            content = json.loads(h_refreshed.content or '[]')
            self.assertIn(child_id, content)

    def test_criterion_4_extended_block_types_schemas(self):
        """Verifies all 11 newly integrated block types validate against canonical schemas."""
        new_types = [
            'header_4', 'to_do', 'quote', 'callout',
            'transclusion_container', 'transclusion_reference',
            'video', 'audio', 'file', 'pdf', 'bookmark'
        ]

        for btype in new_types:
            self.assertTrue(rich_text.is_valid_block_type(btype), f"{btype} must be a valid block type")
            block_dict = rich_text.create_default_block(btype)
            is_valid, err = rich_text.validate_block(block_dict)
            self.assertTrue(is_valid, f"{btype} failed validation: {err}")

    def test_criterion_5_to_do_checked_property(self):
        """Verifies to_do checked property representation."""
        todo_data = rich_text.create_default_block('to_do')
        todo_data['properties'] = {
            'title': [['Buy milk', []]],
            'checked': [['Yes', []]],
        }
        is_valid, err = rich_text.validate_block(todo_data)
        self.assertTrue(is_valid, f"to_do validation error: {err}")

if __name__ == '__main__':
    unittest.main()
