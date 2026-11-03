#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_adversarial_m1_structural_stress.py
Adversarial Stress Test Suite for Milestone 1 (Challenger 2).

Empirically challenges:
1. Pure leaf node child rejection across all leaf types (code, divider, equation, image, video, audio, file, pdf, bookmark, table_row, transclusion_reference, sub_page).
2. Toggleable headers: dynamic switching between True/False/None/arbitrary objects with and without children.
3. Canonical properties and format schema validation for the 11 new block types.
4. Rich-text title tuple resilience, security sanitization, and round-tripping.
"""

import os
import json
import time
import socket
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from peewee import SqliteDatabase

import models
import backend
import rich_text
import desktop_app


def find_free_port():
    """Obtiene un puerto TCP libre efímero para aislar el servidor HTTP en pruebas."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


class BaseAdversarialTest(unittest.TestCase):
    """
    Fixture base con SQLite aislada en memoria/tempfile y servidor HTTP efímero.
    """

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = os.path.join(cls.temp_dir.name, 'test_adversarial.db')
        cls.orig_db = models.db
        cls.test_db = SqliteDatabase(cls.test_db_path, timeout=10, check_same_thread=False)
        models.db = cls.test_db
        models.BaseModel._meta.database = cls.test_db

        for m in [
            models.Note, models.Folder, models.Setting, models.NoteHistory,
            models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord
        ]:
            m._meta.database = cls.test_db

        cls.test_db.connect(reuse_if_open=True)
        models.init_db()

        cls.server_port = find_free_port()
        backend.PORT = cls.server_port
        cls.http_server = backend.ThreadingHTTPServer(('127.0.0.1', cls.server_port), backend.NoteJSRequestHandler)
        cls.server_thread = threading.Thread(target=cls.http_server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server_port}"
        time.sleep(0.1)

        cls.bridge = desktop_app.PyWebViewBridge()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.http_server.shutdown()
            cls.http_server.server_close()
        except Exception:
            pass
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

    def setUp(self):
        models.Block.delete().execute()
        models.Note.delete().execute()

    def _http_request(self, method, path, payload=None):
        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode('utf-8') if payload is not None else None
        headers = {'Content-Type': 'application/json'} if payload is not None else {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                status = resp.status
                body = json.loads(resp.read().decode('utf-8'))
                return status, body
        except urllib.error.HTTPError as e:
            try:
                body = json.loads(e.read().decode('utf-8'))
            except Exception:
                body = {'raw': str(e)}
            return e.code, body


# =============================================================================
# Challenge 1: Pure Leaf Node Child Rejection Across ALL Leaf Types
# =============================================================================

class TestAdversarialLeafNodeRejection(BaseAdversarialTest):
    """
    Stress tests pure leaf nodes:
    Leaf types: code, divider, equation, image, video, audio, file, pdf,
                bookmark, table_row, transclusion_reference, sub_page.
    """

    ALL_LEAF_TYPES = [
        'code',
        'divider',
        'equation',
        'image',
        'video',
        'audio',
        'file',
        'pdf',
        'bookmark',
        'table_row',
        'transclusion_reference',
        'sub_page',
    ]

    def test_is_container_block_returns_false_for_all_leaf_types_under_fuzz(self):
        """is_container_block must return False for all leaf types across adversarial format dicts."""
        fuzz_formats = [
            None,
            {},
            {'toggleable': True},
            {'toggleable': 'true'},
            {'children_allowed': True},
            {'toggleable': 1},
            {'table_block_column_order': ['c1']},
            '{"toggleable": true}',
            'random_non_json_string',
            12345,
            [1, 2, 3],
            {'nested': {'toggleable': True}},
        ]
        for ltype in self.ALL_LEAF_TYPES:
            for fmt in fuzz_formats:
                res = rich_text.is_container_block(ltype, fmt)
                self.assertFalse(
                    res,
                    f"is_container_block('{ltype}', {fmt}) must return False, got {res}"
                )

    def test_validate_block_rejects_non_empty_content_for_all_leaf_types(self):
        """validate_block must reject any leaf block with content containing elements."""
        adversarial_contents = [
            ['child-uuid-1'],
            ['child-uuid-1', 'child-uuid-2'],
            [''],
            [None],
            [123],
            ['a' * 64],
        ]
        for ltype in self.ALL_LEAF_TYPES:
            for bad_cnt in adversarial_contents:
                blk = {
                    'type': ltype,
                    'content': bad_cnt,
                    'properties': {},
                    'format': {},
                }
                if ltype == 'sub_page':
                    blk['properties'] = {'page_id': 'p1'}
                ok, err = rich_text.validate_block(blk)
                self.assertFalse(
                    ok,
                    f"validate_block should reject leaf '{ltype}' with content {bad_cnt}, but passed"
                )
                self.assertIn("does not permit children", str(err))

    def test_validate_block_allows_none_and_empty_list_for_all_leaf_types(self):
        """validate_block should accept content: None or content: [] (0 children) for leaf types."""
        for ltype in self.ALL_LEAF_TYPES:
            blk_none = {'type': ltype, 'content': None, 'properties': {}, 'format': {}}
            blk_empty = {'type': ltype, 'content': [], 'properties': {}, 'format': {}}
            if ltype == 'sub_page':
                blk_none['properties'] = {'page_id': 'p1'}
                blk_empty['properties'] = {'page_id': 'p1'}

            ok_none, err_none = rich_text.validate_block(blk_none)
            self.assertTrue(ok_none, f"Leaf '{ltype}' with content: None should pass: {err_none}")

            ok_empty, err_empty = rich_text.validate_block(blk_empty)
            self.assertTrue(ok_empty, f"Leaf '{ltype}' with content: [] should pass: {err_empty}")

    def test_add_child_block_strictly_raises_value_error_for_every_leaf_type(self):
        """add_child_block must raise ValueError and create zero rows when parent is any leaf type."""
        for idx, ltype in enumerate(self.ALL_LEAF_TYPES):
            leaf_id = f"leaf-parent-{ltype}-{idx}"
            models.Block.create(
                id=leaf_id,
                type=ltype,
                format='{}',
                properties='{}',
                content=None,
                alive=1,
            )
            child_id = f"child-should-fail-{ltype}"

            with self.assertRaises(ValueError) as ctx:
                models.add_child_block(leaf_id, {'id': child_id, 'type': 'text'})

            self.assertIn("leaf node or non-toggleable header", str(ctx.exception))

            # Verify child block was NOT created in DB (atomic guarantee)
            child_in_db = models.Block.get_or_none(models.Block.id == child_id)
            self.assertIsNone(child_in_db, f"Child block {child_id} should not exist in DB after leaf rejection")

            # Verify parent content was not mutated
            parent_in_db = models.Block.get_by_id(leaf_id)
            self.assertIsNone(parent_in_db.to_dict()['content'])

    def test_apply_operation_list_after_and_before_strictly_reject_leaf_parents(self):
        """apply_operation with listAfter or listBefore must raise ValueError if parent is leaf."""
        for ltype in self.ALL_LEAF_TYPES:
            leaf_id = f"op-leaf-{ltype}"
            models.Block.create(id=leaf_id, type=ltype, content=None, format='{}')

            op_after = models.build_op_list_after(leaf_id, 'child-uuid-x')
            with self.assertRaises(ValueError):
                models.apply_operation(op_after)

            op_before = {
                'pointer': {'table': 'block', 'id': leaf_id},
                'path': ['content'],
                'command': 'listBefore',
                'args': {'id': 'child-uuid-x'},
            }
            with self.assertRaises(ValueError):
                models.apply_operation(op_before)

    def test_transactional_atomic_rollback_on_leaf_child_creation(self):
        """Transactional creation [op.set, op.listAfter] on leaf must rollback op.set completely."""
        leaf_id = 'atomic-leaf-divider'
        models.Block.create(id=leaf_id, type='divider', content=None, format='{}')

        child_id = 'atomic-orphan-test'
        op_set = models.build_op_set(child_id, {'type': 'text', 'properties': {'title': [['orphan', []]]}})
        op_list = models.build_op_list_after(leaf_id, child_id)

        with self.assertRaises(ValueError):
            models.apply_transaction([op_set, op_list])

        # Child must NOT exist in the database (0 orphan rows)
        orphan = models.Block.get_or_none(models.Block.id == child_id)
        self.assertIsNone(orphan, "Child block record must be rolled back by SQLite when parent is a leaf")

    def test_move_child_block_strictly_rejects_leaf_target_parent(self):
        """move_child_block must reject moving any child under a leaf node."""
        valid_parent = models.Block.create(id='valid-container-page', type='page', content=json.dumps(['child-move-1']))
        child = models.Block.create(id='child-move-1', type='text', parent_id='valid-container-page')

        for ltype in self.ALL_LEAF_TYPES:
            leaf_id = f"target-leaf-{ltype}"
            models.Block.create(id=leaf_id, type=ltype, content=None, format='{}')

            with self.assertRaises(ValueError) as ctx:
                models.move_child_block(child.id, leaf_id)

            self.assertIn("leaf node", str(ctx.exception))
            # Child must still belong to valid_parent
            refreshed_child = models.Block.get_by_id(child.id)
            self.assertEqual(refreshed_child.parent_id, 'valid-container-page')

    def test_rest_api_create_block_under_leaf_parent_returns_400(self):
        """POST /api/blocks with parent_id pointing to a leaf node must return 400 Bad Request."""
        leaf_id = 'api-leaf-image'
        models.Block.create(id=leaf_id, type='image', content=None, format='{}')

        # Test canonical flat payload
        status, body = self._http_request('POST', '/api/blocks', {
            'id': 'api-child-should-fail-1',
            'type': 'text',
            'parent_id': leaf_id,
        })
        self.assertEqual(status, 400)
        self.assertFalse(body.get('ok'))
        self.assertIn("cannot accept children", body.get('error', ''))
        self.assertIsNone(models.Block.get_or_none(models.Block.id == 'api-child-should-fail-1'))

        # Test nested block payload with parent_id inside block
        status2, body2 = self._http_request('POST', '/api/blocks', {
            'block': {
                'id': 'api-child-should-fail-2',
                'type': 'text',
                'parent_id': leaf_id,
            }
        })
        self.assertEqual(status2, 400)
        self.assertFalse(body2.get('ok'))
        self.assertIn("cannot accept children", body2.get('error', ''))
        self.assertIsNone(models.Block.get_or_none(models.Block.id == 'api-child-should-fail-2'))

        # Test nested block payload with parent_id at root level
        status3, body3 = self._http_request('POST', '/api/blocks', {
            'parent_id': leaf_id,
            'block': {
                'id': 'api-child-should-fail-3',
                'type': 'text',
            }
        })
        self.assertEqual(status3, 400)
        self.assertFalse(body3.get('ok'))
        self.assertIn("cannot accept children", body3.get('error', ''))
        self.assertIsNone(models.Block.get_or_none(models.Block.id == 'api-child-should-fail-3'))

        # Test nested block payload with parentId at root level
        status4, body4 = self._http_request('POST', '/api/blocks', {
            'parentId': leaf_id,
            'block': {
                'id': 'api-child-should-fail-4',
                'type': 'text',
            }
        })
        self.assertEqual(status4, 400)
        self.assertFalse(body4.get('ok'))
        self.assertIn("cannot accept children", body4.get('error', ''))
        self.assertIsNone(models.Block.get_or_none(models.Block.id == 'api-child-should-fail-4'))

    def test_all_leaf_blocks_serialize_content_as_none_in_to_dict(self):
        """Block.to_dict() must return content: None for all leaf blocks in the database."""
        for ltype in self.ALL_LEAF_TYPES:
            b = models.Block.create(id=f"serialize-leaf-{ltype}", type=ltype, content=None, format='{}')
            d = b.to_dict()
            self.assertIsNone(
                d['content'],
                f"Leaf block '{ltype}' must serialize content as None, got {d['content']}"
            )


# =============================================================================
# Challenge 2: Toggleable Headers Dynamic Switching & Invariant Stress
# =============================================================================

class TestAdversarialToggleableHeaders(BaseAdversarialTest):
    """
    Stress tests toggleable headers: header, sub_header, sub_sub_header, header_4.
    Dynamically switches format.toggleable between True, False, None, and arbitrary objects.
    """

    HEADER_TYPES = ['header', 'sub_header', 'sub_sub_header', 'header_4']

    def test_is_container_block_matrix_for_headers(self):
        """Exhaustively verify truth table of format.toggleable for all header types."""
        truthy_cases = [
            {'toggleable': True},
            {'toggleable': 1},
            {'toggleable': 42},
            {'toggleable': 'true'},
            {'toggleable': 'yes'},
            {'toggleable': [1]},
            {'toggleable': {'open': True}},
            '{"toggleable": true}',
            '{"toggleable": 1}',
        ]
        falsy_cases = [
            {'toggleable': False},
            {'toggleable': None},
            {'toggleable': 0},
            {'toggleable': ''},
            {'toggleable': []},
            {'toggleable': {}},
            {},
            None,
            '{"toggleable": false}',
            '{"toggleable": null}',
            '{"toggleable": 0}',
            '{"other_key": true}',
            'invalid_json_string',
            12345,
            [1, 2, 3],
        ]

        for htype in self.HEADER_TYPES:
            for fmt in truthy_cases:
                self.assertTrue(
                    rich_text.is_container_block(htype, fmt),
                    f"is_container_block('{htype}', {fmt}) should be True"
                )
            for fmt in falsy_cases:
                self.assertFalse(
                    rich_text.is_container_block(htype, fmt),
                    f"is_container_block('{htype}', {fmt}) should be False"
                )

    def test_child_addition_succeeds_when_header_toggleable_is_true(self):
        """Header with format.toggleable = True allows adding children and serializes content as list."""
        for htype in self.HEADER_TYPES:
            hid = f"toggle-h-true-{htype}"
            models.Block.create(
                id=hid,
                type=htype,
                format=json.dumps({'toggleable': True, 'block_color': 'default'}),
                content='[]',
            )

            # Add child via add_child_block
            cid = f"child-under-{htype}"
            child = models.add_child_block(hid, {'id': cid, 'type': 'text'})
            self.assertEqual(child.parent_id, hid)

            # Parent content must contain child
            parent = models.Block.get_by_id(hid)
            p_dict = parent.to_dict()
            self.assertIsInstance(p_dict['content'], list)
            self.assertIn(cid, p_dict['content'])

    def test_child_addition_fails_when_header_toggleable_is_false(self):
        """Header with format.toggleable = False strictly rejects adding children."""
        for htype in self.HEADER_TYPES:
            hid = f"toggle-h-false-{htype}"
            models.Block.create(
                id=hid,
                type=htype,
                format=json.dumps({'toggleable': False}),
                content=None,
            )

            with self.assertRaises(ValueError):
                models.add_child_block(hid, {'id': f'fail-child-{htype}', 'type': 'text'})

            parent = models.Block.get_by_id(hid)
            self.assertIsNone(parent.to_dict()['content'])

    def test_dynamic_switching_lifecycle_with_children(self):
        """
        Dynamically cycle a header through states:
        1. toggleable = True -> Add children c1, c2, c3
        2. toggleable = False -> Cannot add c4; existing children preserved in DB
        3. toggleable = True again -> Can add c4; content now [c1, c2, c3, c4]
        """
        hid = 'dynamic-lifecycle-header'
        models.Block.create(
            id=hid,
            type='header_4',
            format=json.dumps({'toggleable': True}),
            content='[]',
        )

        # 1. Add c1, c2, c3
        c1 = models.add_child_block(hid, {'id': 'dyn-c1', 'type': 'text'})
        c2 = models.add_child_block(hid, {'id': 'dyn-c2', 'type': 'text'})
        c3 = models.add_child_block(hid, {'id': 'dyn-c3', 'type': 'text'})

        parent = models.Block.get_by_id(hid)
        self.assertEqual(parent.to_dict()['content'], ['dyn-c1', 'dyn-c2', 'dyn-c3'])

        # 2. Switch toggleable to False via update operation
        models.apply_operation({
            'pointer': {'table': 'block', 'id': hid},
            'command': 'update',
            'args': {'format': {'toggleable': False}}
        })

        parent = models.Block.get_by_id(hid)
        self.assertFalse(rich_text.is_container_block(parent.type, parent.format))

        # Adding c4 must fail
        with self.assertRaises(ValueError):
            models.add_child_block(hid, {'id': 'dyn-c4', 'type': 'text'})

        # Existing children must NOT be wiped or lost in database
        refreshed = models.Block.get_by_id(hid)
        self.assertEqual(json.loads(refreshed.content), ['dyn-c1', 'dyn-c2', 'dyn-c3'])
        # In to_dict(), non-empty content is preserved
        self.assertEqual(refreshed.to_dict()['content'], ['dyn-c1', 'dyn-c2', 'dyn-c3'])

        # 3. Switch toggleable back to True
        models.apply_operation({
            'pointer': {'table': 'block', 'id': hid},
            'command': 'update',
            'args': {'format': {'toggleable': True}}
        })

        parent = models.Block.get_by_id(hid)
        self.assertTrue(rich_text.is_container_block(parent.type, parent.format))

        # Adding c4 now succeeds
        c4 = models.add_child_block(hid, {'id': 'dyn-c4', 'type': 'text'})
        refreshed2 = models.Block.get_by_id(hid)
        self.assertEqual(refreshed2.to_dict()['content'], ['dyn-c1', 'dyn-c2', 'dyn-c3', 'dyn-c4'])

    def test_moving_children_between_toggleable_and_non_toggleable_headers(self):
        """Moving children to a toggleable header succeeds; moving to non-toggleable header fails."""
        h_toggle = models.Block.create(id='h-src-toggle', type='header', format=json.dumps({'toggleable': True}), content='[]')
        h_non_toggle = models.Block.create(id='h-dst-non-toggle', type='header', format=json.dumps({'toggleable': False}), content=None)

        child = models.add_child_block(h_toggle.id, {'id': 'movable-child', 'type': 'text'})

        # Attempt to move child to non-toggleable header must fail
        with self.assertRaises(ValueError):
            models.move_child_block(child.id, h_non_toggle.id)

        # Child remains in h_toggle
        self.assertEqual(models.Block.get_by_id(child.id).parent_id, h_toggle.id)


# =============================================================================
# Challenge 3: Canonical Properties and Format Schema Validation (11 Block Types)
# =============================================================================

class TestAdversarialBlockSchemasAndCanonicalValidation(BaseAdversarialTest):
    """
    Stress tests schemas and canonical definitions for the 11 new block types:
    header_4, to_do, quote, callout, transclusion_container, transclusion_reference,
    video, audio, file, pdf, bookmark.
    """

    ELEVEN_NEW_TYPES = [
        'header_4',
        'to_do',
        'quote',
        'callout',
        'transclusion_container',
        'transclusion_reference',
        'video',
        'audio',
        'file',
        'pdf',
        'bookmark',
    ]

    def test_create_default_block_matches_canonical_schema_for_all_11_types(self):
        """create_default_block must instantiate exact default schemas matching Notion specs."""
        expected_content = {
            'header_4': None,
            'to_do': [],
            'quote': [],
            'callout': [],
            'transclusion_container': [],
            'transclusion_reference': None,
            'video': None,
            'audio': None,
            'file': None,
            'pdf': None,
            'bookmark': None,
        }

        for btype in self.ELEVEN_NEW_TYPES:
            blk = rich_text.create_default_block(btype, block_id=f"default-{btype}")
            self.assertEqual(blk['type'], btype)
            self.assertEqual(blk['content'], expected_content[btype])

            # Every default block must pass validate_block 100% cleanly
            ok, err = rich_text.validate_block(blk)
            self.assertTrue(ok, f"Default block for '{btype}' must pass validate_block: {err}")

    def test_to_do_checked_property_validation(self):
        """to_do checked property must accept [['Yes', []]] and [['No', []]]."""
        for state in ['Yes', 'No']:
            todo = {
                'type': 'to_do',
                'properties': {'title': [['Task', []]], 'checked': [[state, []]]},
                'format': {},
                'content': [],
            }
            ok, err = rich_text.validate_block(todo)
            self.assertTrue(ok, f"to_do checked '{state}' must pass: {err}")

    def test_callout_icon_and_background_color_validation(self):
        """callout must validate page_icon and block_color in format."""
        callout = {
            'type': 'callout',
            'properties': {'title': [['Alert message', [['b']]]]},
            'format': {'page_icon': '⚠️', 'block_color': 'red_background'},
            'content': ['nested-text-uuid'],
        }
        ok, err = rich_text.validate_block(callout)
        self.assertTrue(ok, f"callout with emoji and red_background must pass: {err}")

    def test_transclusion_reference_pointer_validation(self):
        """transclusion_reference requires format.transclusion_reference_pointer and rejects content."""
        valid_ref = {
            'type': 'transclusion_reference',
            'properties': {},
            'format': {
                'transclusion_reference_pointer': {
                    'id': 'source-block-uuid',
                    'table': 'block',
                    'space_id': 'default_space',
                }
            },
            'content': None,
        }
        ok, err = rich_text.validate_block(valid_ref)
        self.assertTrue(ok, f"transclusion_reference must pass: {err}")

        # Non-empty content rejected
        invalid_ref = dict(valid_ref)
        invalid_ref['content'] = ['illegal-child']
        ok, err = rich_text.validate_block(invalid_ref)
        self.assertFalse(ok, "transclusion_reference must reject children")

    def test_media_leaf_blocks_source_and_format_validation(self):
        """Media blocks (video, audio, file, pdf, bookmark) must validate properties and format."""
        media_specs = [
            ('video', {'source': [['https://cdn.example.com/v.mp4', []]], 'caption': [['Sample', []]]}, {'block_width': 750, 'block_alignment': 'center'}),
            ('audio', {'source': [['https://cdn.example.com/a.mp3', []]]}, {'block_width': 400}),
            ('file', {'source': [['https://cdn.example.com/f.zip', []]], 'title': [['archive.zip', []]], 'size': [['10MB', []]]}, {'block_color': 'gray'}),
            ('pdf', {'source': [['https://cdn.example.com/doc.pdf', []]]}, {'block_width': 700, 'block_height': 500, 'block_alignment': 'left'}),
            ('bookmark', {'link': [['https://github.com', []]], 'title': [['GitHub', []]], 'description': [['Code repo', []]], 'caption': []}, {'bookmark_icon': '🐙'}),
        ]
        for btype, props, fmt in media_specs:
            blk = {
                'type': btype,
                'properties': props,
                'format': fmt,
                'content': None,
            }
            ok, err = rich_text.validate_block(blk)
            self.assertTrue(ok, f"Media block '{btype}' must pass validation: {err}")

            # Rejection with children
            bad_blk = dict(blk)
            bad_blk['content'] = ['child-uuid']
            ok_bad, _ = rich_text.validate_block(bad_blk)
            self.assertFalse(ok_bad, f"Media block '{btype}' must reject content with children")

    def test_database_persistence_roundtrip_for_all_11_types(self):
        """Insert each of the 11 new types via op.set in SQLite and verify fidelity via to_dict()."""
        for btype in self.ELEVEN_NEW_TYPES:
            bid = f"roundtrip-{btype}"
            default_blk = rich_text.create_default_block(btype, block_id=bid)
            op_set = models.build_op_set(bid, default_blk)
            res = models.apply_transaction([op_set])
            self.assertTrue(res.get('ok'))

            loaded = models.Block.get_by_id(bid)
            loaded_dict = loaded.to_dict()
            self.assertEqual(loaded_dict['id'], bid)
            self.assertEqual(loaded_dict['type'], btype)

            # Check content parity
            if btype in rich_text.CONTAINER_BLOCK_TYPES:
                self.assertIsInstance(loaded_dict['content'], list)
            else:
                self.assertIsNone(loaded_dict['content'])


# =============================================================================
# Challenge 4: Rich-Text Title Tuple Resilience & Security
# =============================================================================

class TestAdversarialRichTextTupleResilience(unittest.TestCase):
    """
    Stress tests Notion rich-text tuple manipulation, edge cases, XSS sanitization,
    and HTML roundtrip fidelity.
    """

    def test_validate_rich_text_rejects_fuzz_structures(self):
        """validate_rich_text must reject corrupted, malformed, or hostile tuple structures."""
        invalid_cases = [
            "raw string instead of list",
            12345,
            {'segment': 'text'},
            ['not a nested list'],
            [[]],  # empty segment
            [[12345, []]],  # non-string text
            [[None, []]],
            [[['nested'], []]],
            [['text', 'not a list decorator']],
            [['text', 12345]],
            [['text', [[]]]],  # empty decorator
            [['text', ['b']]],  # non-list decorator item
            [['text', [['unknown_tag']]]],
            [['text', [['script']]]],
            [['text', [['blink']]]],
            [['text', [['style']]]],
        ]
        for bad in invalid_cases:
            ok, err = rich_text.validate_rich_text(bad)
            self.assertFalse(ok, f"validate_rich_text should reject {bad!r}, but passed")

    def test_validate_rich_text_accepts_all_canonical_decorators(self):
        """validate_rich_text must accept all valid decorators: b, i, _, s, c, h, a, e."""
        valid_tuples = [
            [],
            [['Plain text', []]],
            [['Styled', [['b'], ['i'], ['_'], ['s'], ['c']]]],
            [['Colored', [['h', 'red'], ['h', 'blue_background']]]],
            [['Link', [['a', 'https://notion.so']]]],
            [['Inline Equation', [['e', 'E=mc^2']]]],
            [['Complex combo', [['b'], ['h', 'green'], ['a', 'https://example.com']]]],
        ]
        for good in valid_tuples:
            ok, err = rich_text.validate_rich_text(good)
            self.assertTrue(ok, f"validate_rich_text should accept {good!r}: {err}")

    def test_rich_text_to_plain_text_resilience(self):
        """rich_text_to_plain_text handles edge cases, None, raw strings, and equations."""
        self.assertEqual(rich_text.rich_text_to_plain_text(None), "")
        self.assertEqual(rich_text.rich_text_to_plain_text("raw string"), "raw string")
        self.assertEqual(rich_text.rich_text_to_plain_text([]), "")
        self.assertEqual(
            rich_text.rich_text_to_plain_text([['Hello ', [['b']]], ['World', []]]),
            "Hello World"
        )
        # Inline equation extraction with canonical token '⁍'
        self.assertEqual(
            rich_text.rich_text_to_plain_text([['⁍', [['e', '\\alpha + \\beta']]]]),
            "\\alpha + \\beta"
        )
        # Dirty segment resilience (should not raise exception)
        res = rich_text.rich_text_to_plain_text([None, 123, ['Text', None]])
        self.assertIn("Text", res)

    def test_plain_text_to_rich_text(self):
        """plain_text_to_rich_text wraps text safely into Notion tuple format."""
        self.assertEqual(rich_text.plain_text_to_rich_text(None), [])
        self.assertEqual(rich_text.plain_text_to_rich_text(""), [])
        self.assertEqual(rich_text.plain_text_to_rich_text("Hello"), [["Hello", []]])
        self.assertEqual(rich_text.plain_text_to_rich_text(123), [["123", []]])

    def test_rich_text_to_html_xss_and_injection_defenses(self):
        """rich_text_to_html must escape HTML tags and sanitize dangerous link schemes."""
        # 1. HTML tag injection in raw text
        raw_xss = [['<script>alert(1)</script>', []]]
        html_out = rich_text.rich_text_to_html(raw_xss)
        self.assertNotIn("<script>", html_out)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html_out)

        # 2. Dangerous javascript: scheme in link
        js_link = [['Click Me', [['a', 'javascript:alert(document.cookie)']]]]
        html_link = rich_text.rich_text_to_html(js_link)
        self.assertNotIn('href="javascript:', html_link)
        self.assertIn('href="#"', html_link)

        # 3. Data URI scheme in link
        data_link = [['Click Me', [['a', 'data:text/html,<script>alert(1)</script>']]]]
        html_data = rich_text.rich_text_to_html(data_link)
        self.assertNotIn('href="data:', html_data)
        self.assertIn('href="#"', html_data)

        # 4. Color style injection defense: punctuation required for CSS injection and arbitrary CSS properties are stripped
        color_inj = [['Text', [['h', 'red; font-size: 100px; background: url("bad")']]]]
        html_color = rich_text.rich_text_to_html(color_inj)
        self.assertNotIn('font-size', html_color)
        self.assertNotIn('url', html_color)
        style_val = html_color.split('style="color: ')[1].split('"')[0].rstrip(';')
        self.assertNotIn(';', style_val)
        self.assertNotIn(':', style_val)
        self.assertNotIn('(', html_color)
        self.assertNotIn(')', html_color)
        style_attr_val = html_color.split('style="')[1].split('"')[0]
        self.assertNotIn('"', style_attr_val)

    def test_bidirectional_roundtrip_fidelity(self):
        """Converting Notion tuples to HTML and back to Notion tuples preserves text and decorators."""
        sample_tuples = [
            [['Bold text ', [['b']]], ['Italic text', [['i']]]],
            [['Underlined', [['_']]], [' and Strikethrough', [['s']]]],
            [['Code block', [['c']]]],
            [['Highlighted', [['h', 'blue_background']]]],
        ]
        for original in sample_tuples:
            html_rep = rich_text.rich_text_to_html(original)
            parsed_tuples = rich_text.html_to_rich_text(html_rep)
            plain_orig = rich_text.rich_text_to_plain_text(original)
            plain_parsed = rich_text.rich_text_to_plain_text(parsed_tuples)
            self.assertEqual(
                plain_orig,
                plain_parsed,
                f"Roundtrip must preserve plain text: original='{plain_orig}', parsed='{plain_parsed}'"
            )

    def test_html_parser_merges_adjacent_identical_styles(self):
        """html_to_rich_text merges contiguous segments with identical formatting."""
        html_input = "<strong>Part 1 </strong><strong>Part 2</strong>"
        tuples = rich_text.html_to_rich_text(html_input)
        self.assertEqual(len(tuples), 1)
        self.assertEqual(tuples[0][0], "Part 1 Part 2")
        self.assertEqual(tuples[0][1], [['b']])

    def test_fuzz_massive_and_unicode_text_resilience(self):
        """Ensure rich text system withstands huge strings, emojis, and unicode edge cases."""
        massive_text = "A" * 50000
        emoji_text = "🚀🔥✨💡🎉🐱💻📦🔑"
        combining_text = "Z̸a̸l̸g̸o̸ ̸t̸e̸x̸t̸ ̸c̸o̸m̸b̸i̸n̸i̸n̸g̸"
        rtl_text = "مرحبا بالعالم (Arabic RTL) שלום עולם (Hebrew RTL)"

        for text in [massive_text, emoji_text, combining_text, rtl_text]:
            tuples = [[text, [['b'], ['i']]]]
            ok, err = rich_text.validate_rich_text(tuples)
            self.assertTrue(ok, f"Failed on unicode/massive text: {err}")

            plain = rich_text.rich_text_to_plain_text(tuples)
            self.assertEqual(plain, text)

            html_out = rich_text.rich_text_to_html(tuples)
            parsed = rich_text.html_to_rich_text(html_out)
            self.assertEqual(rich_text.rich_text_to_plain_text(parsed), text)


# =============================================================================
# Challenge 5: Deep Multi-Level Hierarchy & Large Batch Rollback Stress
# =============================================================================

class TestAdversarialDeepHierarchyAndBatchStress(BaseAdversarialTest):
    """
    Stress tests deep multi-level block hierarchies, taxonomy disjointness,
    and massive batch transactional rollbacks.
    """

    def test_taxonomy_sets_are_strictly_disjoint(self):
        """CONTAINER_BLOCK_TYPES, LEAF_BLOCK_TYPES, and TOGGLEABLE_HEADER_TYPES must have zero overlap."""
        c = rich_text.CONTAINER_BLOCK_TYPES
        l = rich_text.LEAF_BLOCK_TYPES
        h = rich_text.TOGGLEABLE_HEADER_TYPES

        self.assertEqual(len(c & l), 0, f"Overlap between containers and leaves: {c & l}")
        self.assertEqual(len(c & h), 0, f"Overlap between containers and headers: {c & h}")
        self.assertEqual(len(l & h), 0, f"Overlap between leaves and headers: {l & h}")

        # All 28 types must be accounted for
        classified = c | l | h | {'collection_view', 'collection_view_page'}
        self.assertTrue(
            rich_text.ALL_NOTION_BLOCK_TYPES.issubset(classified),
            f"Unclassified types: {rich_text.ALL_NOTION_BLOCK_TYPES - classified}"
        )

    def test_deep_mixed_hierarchy_with_leaf_terminal(self):
        """
        Builds a 5-level deep hierarchy:
        Page (container)
          -> Callout (container)
             -> Header_4 (toggleable=True)
                -> To_do (container)
                   -> Divider (leaf)
                      -> Attempt to add child under Divider MUST fail!
        """
        # 1. Page
        page = models.Block.create(id='deep-page', type='page', content='[]')

        # 2. Callout under Page
        callout = models.add_child_block(page.id, {'id': 'deep-callout', 'type': 'callout'})

        # 3. Header_4 (toggleable) under Callout
        h4 = models.add_child_block(
            callout.id,
            {'id': 'deep-h4', 'type': 'header_4', 'format': {'toggleable': True}}
        )

        # 4. To_do under Header_4
        todo = models.add_child_block(h4.id, {'id': 'deep-todo', 'type': 'to_do'})

        # 5. Divider under To_do
        divider = models.add_child_block(todo.id, {'id': 'deep-divider', 'type': 'divider'})

        # 6. Attempt to add child under Divider must fail strictly
        with self.assertRaises(ValueError) as ctx:
            models.add_child_block(divider.id, {'id': 'deep-fail', 'type': 'text'})
        self.assertIn("leaf node", str(ctx.exception))

        # Verify tree integrity: all 5 ancestors exist and have correct children
        self.assertIn(callout.id, models.Block.get_by_id(page.id).to_dict()['content'])
        self.assertIn(h4.id, models.Block.get_by_id(callout.id).to_dict()['content'])
        self.assertIn(todo.id, models.Block.get_by_id(h4.id).to_dict()['content'])
        self.assertIn(divider.id, models.Block.get_by_id(todo.id).to_dict()['content'])
        self.assertIsNone(models.Block.get_by_id(divider.id).to_dict()['content'])

    def test_massive_transaction_batch_all_or_nothing_rollback(self):
        """
        Executes a batch of 50 block creation operations.
        If the 50th operation illegally targets a leaf node, ALL 50 operations must rollback.
        Zero orphan rows must remain.
        """
        leaf_anchor = models.Block.create(id='anchor-leaf', type='code', content=None, format='{}')
        container_parent = models.Block.create(id='anchor-parent', type='page', content='[]')

        ops = []
        created_ids = []
        for i in range(49):
            cid = f"batch-valid-{i}"
            created_ids.append(cid)
            ops.append(models.build_op_set(cid, {'type': 'text', 'parent_id': container_parent.id}))
            ops.append(models.build_op_list_after(container_parent.id, cid, after_id=None))

        # The 50th block attempts to attach to the leaf_anchor
        poison_id = 'batch-poison-50'
        ops.append(models.build_op_set(poison_id, {'type': 'text', 'parent_id': leaf_anchor.id}))
        ops.append(models.build_op_list_after(leaf_anchor.id, poison_id, after_id=None))

        # Must raise ValueError
        with self.assertRaises(ValueError):
            models.apply_transaction(ops)

        # Verify not a single one of the 50 blocks was persisted
        for cid in created_ids:
            self.assertIsNone(models.Block.get_or_none(models.Block.id == cid), f"Block {cid} should have rolled back")
        self.assertIsNone(models.Block.get_or_none(models.Block.id == poison_id))

        # Parent content must be completely untouched (empty)
        p = models.Block.get_by_id(container_parent.id)
        self.assertEqual(p.to_dict()['content'], [])


if __name__ == '__main__':
    unittest.main()
