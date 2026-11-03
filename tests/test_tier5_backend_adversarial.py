#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_tier5_backend_adversarial.py
Tier 5 Adversarial Coverage Hardening Suite for Note-JS-Desktop.

Focus: White-box Backend Audit & Adversarial Hardening:
1. Malformed transactions: invalid table, missing pointer/id, unknown commands, circular references.
2. Database rollback under simulated operational failures inside apply_transaction.
3. Concurrency stress on build_op_list_after, build_op_set, and apply_transaction.
4. Leaf vs container invariants under direct API bypasses (all 12 leaf types).
5. Dynamic toggleable header validation when format.toggleable is mutated across states.
"""

import os
import sys
import json
import time
import socket
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from peewee import SqliteDatabase

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

import models
import backend
import rich_text
import desktop_app


def find_free_port():
    """Obtains an ephemeral TCP port for isolated HTTP server testing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


class BaseTier5AdversarialTest(unittest.TestCase):
    """Base fixture with isolated SQLite database and ephemeral HTTP test server."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = os.path.join(cls.temp_dir.name, 'test_tier5_adversarial.db')
        cls.orig_db = models.db
        cls.test_db = SqliteDatabase(cls.test_db_path, timeout=15, check_same_thread=False)
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

    def _http_post(self, path, payload):
        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
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
# 1. Malformed Transactions Audit
# =============================================================================

class TestMalformedTransactionsAdversarial(BaseTier5AdversarialTest):
    """Adversarial testing of malformed operations, pointers, commands, and circular references."""

    def test_malformed_operations_non_dict_and_non_list(self):
        """Rejects operations payload when not a list or containing non-dict items."""
        with self.assertRaises(ValueError):
            models.apply_transaction("not_a_list")

        with self.assertRaises(ValueError):
            models.apply_transaction(12345)

        with self.assertRaises(ValueError):
            models.apply_transaction(None)

        with self.assertRaises(ValueError):
            models.apply_transaction(["string_instead_of_dict"])

        with self.assertRaises(ValueError):
            models.apply_transaction([None])

    def test_malformed_pointer_invalid_table(self):
        """Rejects transaction when pointer table is not 'block'."""
        invalid_tables = ['workspace', 'notes', 'user', 'space', '', None, 999]
        for tbl in invalid_tables:
            op = {
                'pointer': {'table': tbl, 'id': 'test-id-1'},
                'command': 'set',
                'args': {'type': 'text'}
            }
            with self.assertRaises(ValueError, msg=f"Should reject table={tbl}"):
                models.apply_transaction([op])

    def test_malformed_pointer_missing_or_empty_id(self):
        """Rejects operations with missing, null, or empty record ID."""
        for bad_id in [None, '', False]:
            op = {
                'pointer': {'table': 'block', 'id': bad_id},
                'command': 'set',
                'args': {'type': 'text'}
            }
            with self.assertRaises(ValueError, msg=f"Should reject id={bad_id}"):
                models.apply_transaction([op])

    def test_malformed_pointer_not_a_dict(self):
        """Safely rolls back when pointer itself is not a dictionary."""
        op = {
            'pointer': 'invalid_pointer_string',
            'command': 'set',
            'args': {'type': 'text'}
        }
        res, status = backend.apply_transactions_api({'operations': [op]})
        self.assertEqual(status, 400)
        self.assertFalse(res.get('ok'))

    def test_malformed_unknown_commands(self):
        """Rejects unrecognized operation commands."""
        unknown_cmds = ['delete', 'drop', 'exec', 'select', 'truncate', '', None, 'SET_UPPER']
        for cmd in unknown_cmds:
            op = {
                'pointer': {'table': 'block', 'id': 'test-cmd-id'},
                'command': cmd,
                'args': {}
            }
            with self.assertRaises(ValueError, msg=f"Should reject command='{cmd}'"):
                models.apply_transaction([op])

    def test_malformed_missing_targets_in_commands(self):
        """Rejects listAfter, listBefore, update, and listRemove targeting non-existent blocks."""
        non_existent_id = 'non-existent-uuid-9999'

        # listAfter on missing parent
        op_list_after = {
            'pointer': {'table': 'block', 'id': non_existent_id},
            'command': 'listAfter',
            'path': ['content'],
            'args': {'id': 'child-1'}
        }
        with self.assertRaises(ValueError):
            models.apply_transaction([op_list_after])

        # listBefore on missing parent
        op_list_before = {
            'pointer': {'table': 'block', 'id': non_existent_id},
            'command': 'listBefore',
            'path': ['content'],
            'args': {'id': 'child-1'}
        }
        with self.assertRaises(ValueError):
            models.apply_transaction([op_list_before])

        # update on missing block
        op_update = {
            'pointer': {'table': 'block', 'id': non_existent_id},
            'command': 'update',
            'args': {'properties': {'title': 'new'}}
        }
        with self.assertRaises(ValueError):
            models.apply_transaction([op_update])

        # listRemove on missing parent
        op_remove = {
            'pointer': {'table': 'block', 'id': non_existent_id},
            'command': 'listRemove',
            'path': ['content'],
            'args': {'id': 'child-1'}
        }
        with self.assertRaises(ValueError):
            models.apply_transaction([op_remove])

    def test_empty_operations_list_is_graceful(self):
        """Applying an empty operations list succeeds without modifying state."""
        res = models.apply_transaction([])
        self.assertTrue(res.get('ok'))
        self.assertEqual(res.get('results'), [])

    def test_circular_reference_self_parenting_rejected(self):
        """create_block_api strictly rejects a block designating itself as parent."""
        # Case 1: Existing block attempting to designate itself as parent
        block_id = 'self-parent-node-1'
        create_res, _ = backend.create_block_api({'id': block_id, 'type': 'page'})
        self.assertTrue(create_res.get('ok'))

        res, status = backend.create_block_api({
            'id': block_id,
            'type': 'page',
            'parent_id': block_id,
        })
        self.assertEqual(status, 400)
        self.assertIn("cannot be its own parent", res.get('error', '').lower())

        # Case 2: New unpersisted block with parent_id == bid fails because parent does not exist
        new_bid = 'self-parent-uncreated'
        res2, status2 = backend.create_block_api({
            'id': new_bid,
            'type': 'page',
            'parent_id': new_bid
        })
        self.assertIn(status2, (400, 404))
        self.assertIsNone(models.Block.get_or_none(models.Block.id == new_bid))

    def test_circular_reference_indirect_ancestor_loop_rejected(self):
        """create_block_api detects and prevents ancestor cycle (A -> B -> C -> A)."""
        # 1. Create root page A
        p_a, _ = backend.create_block_api({'id': 'node-A', 'type': 'page'})
        self.assertTrue(p_a.get('ok'))

        # 2. Create child container B under A
        p_b, _ = backend.create_block_api({'id': 'node-B', 'type': 'text', 'parent_id': 'node-A'})
        self.assertTrue(p_b.get('ok'))

        # 3. Create child container C under B
        p_c, _ = backend.create_block_api({'id': 'node-C', 'type': 'quote', 'parent_id': 'node-B'})
        self.assertTrue(p_c.get('ok'))

        # 4. Attempt to create or move block where parent would create cycle:
        # Trying to create node-A with parent_id='node-C'
        res, status = backend.create_block_api({
            'id': 'node-A',
            'type': 'page',
            'parent_id': 'node-C'
        })
        self.assertEqual(status, 400)
        self.assertIn("circular", res.get('error', '').lower())

    def test_circular_reference_record_map_traversal_termination(self):
        """Directly seeded circular references in DB do not cause infinite recursion in record_map."""
        # Force a cycle directly in DB: A has content [B], B has content [A]
        models.Block.create(
            id='loop-A',
            type='page',
            content=json.dumps(['loop-B']),
            alive=1
        )
        models.Block.create(
            id='loop-B',
            type='text',
            content=json.dumps(['loop-A']),
            alive=1
        )

        res, status = backend.get_record_map_api('loop-A')
        self.assertEqual(status, 200)
        self.assertTrue(res.get('ok'))
        block_map = res.get('recordMap', {}).get('block', {})
        self.assertIn('loop-A', block_map)
        self.assertIn('loop-B', block_map)
        # Ensure it visited each exactly once without infinite recursion
        self.assertEqual(len(block_map), 2)


# =============================================================================
# 2. Database Rollback Under Simulated Operational Failures
# =============================================================================

class TestDatabaseRollbackAdversarial(BaseTier5AdversarialTest):
    """Adversarial testing of atomic rollback integrity during multi-operation transactions."""

    def test_atomic_rollback_on_midway_failure(self):
        """Preceding successful ops in a batch must completely roll back when a subsequent op fails."""
        blk1_id = 'atomic-blk-1'
        blk2_id = 'atomic-blk-2'

        op1 = models.build_op_set(blk1_id, {'type': 'text', 'properties': {'title': [['Hello', []]]}})
        op2 = models.build_op_set(blk2_id, {'type': 'quote', 'properties': {'title': [['Quote', []]]}})
        op3_failing = {
            'pointer': {'table': 'invalid_table', 'id': 'fail-id'},
            'command': 'set',
            'args': {'type': 'text'}
        }

        with self.assertRaises(ValueError):
            models.apply_transaction([op1, op2, op3_failing])

        # Verification: NEITHER blk1 nor blk2 must exist in SQLite
        self.assertIsNone(models.Block.get_or_none(models.Block.id == blk1_id))
        self.assertIsNone(models.Block.get_or_none(models.Block.id == blk2_id))

    def test_atomic_rollback_on_tenth_op_failure(self):
        """A 10-op transaction where the 10th op fails leaves zero persistent rows."""
        ops = []
        block_ids = [f"batch-rollback-{i}" for i in range(9)]
        for bid in block_ids:
            ops.append(models.build_op_set(bid, {'type': 'text'}))

        # 10th operation invalid: listAfter on non-existent parent
        ops.append({
            'pointer': {'table': 'block', 'id': 'ghost-parent-99'},
            'command': 'listAfter',
            'path': ['content'],
            'args': {'id': 'child-xyz'}
        })

        with self.assertRaises(ValueError):
            models.apply_transaction(ops)

        for bid in block_ids:
            self.assertIsNone(models.Block.get_or_none(models.Block.id == bid))

    def test_atomic_rollback_preserves_existing_block_state(self):
        """Failed transaction modifying an existing block must restore its original version and content."""
        orig_id = 'orig-block-to-preserve'
        models.Block.create(
            id=orig_id,
            type='page',
            version=7,
            last_version=6,
            properties=json.dumps({'title': [['Untouched', []]]}),
            content=json.dumps(['child-0']),
            alive=1
        )

        op_update = {
            'pointer': {'table': 'block', 'id': orig_id},
            'command': 'update',
            'args': {
                'properties': {'title': [['Corrupted', []]]},
                'alive': 0
            }
        }
        op_fail = {
            'pointer': {'table': 'block', 'id': 'ghost-target'},
            'command': 'unknown_fail_command',
            'args': {}
        }

        with self.assertRaises(ValueError):
            models.apply_transaction([op_update, op_fail])

        refreshed = models.Block.get_by_id(orig_id)
        self.assertEqual(refreshed.version, 7)
        self.assertEqual(refreshed.alive, 1)
        props = json.loads(refreshed.properties)
        self.assertEqual(props.get('title'), [['Untouched', []]])
        content = json.loads(refreshed.content)
        self.assertEqual(content, ['child-0'])

    def test_atomic_rollback_on_simulated_system_exception(self):
        """Simulated runtime exception midway through execution triggers complete Peewee rollback."""
        blk_id = 'crash-test-blk'
        op1 = models.build_op_set(blk_id, {'type': 'to_do'})

        # Wrap apply_operation with a simulated crash on 2nd op
        orig_apply = models.apply_operation
        call_count = {'val': 0}

        def mock_apply_op(op, db_transaction=None):
            call_count['val'] += 1
            if call_count['val'] == 2:
                raise RuntimeError("Simulated SQLite Disk I/O Crash")
            return orig_apply(op, db_transaction=db_transaction)

        models.apply_operation = mock_apply_op
        try:
            op2 = models.build_op_set('crash-blk-2', {'type': 'text'})
            with self.assertRaises(RuntimeError):
                models.apply_transaction([op1, op2])
        finally:
            models.apply_operation = orig_apply

        self.assertIsNone(models.Block.get_or_none(models.Block.id == blk_id))

    def test_http_api_and_bridge_rollback_reporting(self):
        """HTTP endpoint /api/transactions and PyWebViewBridge report 400 and rollback zero orphans."""
        b_id = 'http-atomic-blk'
        payload = {
            'operations': [
                models.build_op_set(b_id, {'type': 'text'}),
                {'pointer': {'table': 'invalid_table', 'id': 'fail'}, 'command': 'set', 'args': {}}
            ]
        }
        status, body = self._http_post('/api/transactions', payload)
        self.assertEqual(status, 400)
        self.assertFalse(body.get('ok'))
        self.assertIsNone(models.Block.get_or_none(models.Block.id == b_id))

        # PyWebViewBridge
        bridge_res = self.bridge.apply_transaction(payload['operations'])
        self.assertFalse(bridge_res.get('ok'))
        self.assertIn('error', bridge_res)


# =============================================================================
# 3. Concurrency Stress on build_op_set, build_op_list_after, & apply_transaction
# =============================================================================

class TestConcurrencyStressAdversarial(BaseTier5AdversarialTest):
    """Concurrency stress-testing for thread isolation, dictionary immutability, and locking."""

    def test_build_ops_multithreaded_immutability(self):
        """Concurrent calls to build_op_set and build_op_list_after do not cross-pollute or mutate inputs."""
        shared_template = {
            'type': 'text',
            'properties': {'title': [['Base', []]]},
            'format': {'block_color': 'gray'}
        }

        results = []
        errors = []

        def worker(idx):
            try:
                bid = f"worker-blk-{idx}"
                pid = f"worker-parent-{idx}"
                op_set = models.build_op_set(bid, shared_template)
                op_list = models.build_op_list_after(pid, bid)

                # Assert that caller template was not mutated
                if 'id' in shared_template:
                    raise AssertionError("Shared template was contaminated with 'id'!")

                if op_set['pointer']['id'] != bid:
                    raise AssertionError(f"ID mismatch in op_set: {op_set['pointer']['id']}")
                if op_list['args']['id'] != bid:
                    raise AssertionError(f"ID mismatch in op_list: {op_list['args']['id']}")

                results.append((op_set, op_list))
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(25)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Errors in concurrent builders: {errors}")
        self.assertEqual(len(results), 25)

    def test_concurrent_apply_transactions_same_parent(self):
        """Concurrent worker threads appending children to the same container maintain WAL serialization."""
        parent_id = 'concurrent-root-page'
        # Create root parent page
        root_op = models.build_op_set(parent_id, {'type': 'page'})
        models.apply_transaction([root_op])

        num_workers = 15
        errors = []

        def worker_insert(worker_idx):
            try:
                child_id = f"c-child-{worker_idx}"
                op_set = models.build_op_set(child_id, {'type': 'text', 'parent_id': parent_id})
                op_list = models.build_op_list_after(parent_id, child_id)
                res = models.apply_transaction([op_set, op_list])
                if not res.get('ok'):
                    errors.append(f"Worker {worker_idx} failed: {res}")
            except Exception as ex:
                errors.append(f"Worker {worker_idx} exception: {ex}")

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(worker_insert, i) for i in range(num_workers)]
            for f in futures:
                f.result()

        self.assertEqual(len(errors), 0, f"Concurrent transaction errors: {errors}")

        parent = models.Block.get_by_id(parent_id)
        p_content = json.loads(parent.content or '[]')
        self.assertEqual(len(p_content), num_workers, "All children must be registered in parent content")
        self.assertEqual(len(set(p_content)), num_workers, "Content must have zero duplicate UUIDs")

    def test_concurrent_mixed_success_and_failure_transactions(self):
        """Concurrent valid and failing transactions do not corrupt successful workers."""
        valid_results = []
        fail_results = []

        def worker_mixed(idx):
            bid = f"mixed-blk-{idx}"
            if idx % 2 == 0:
                # Valid transaction
                op_set = models.build_op_set(bid, {'type': 'to_do'})
                res = models.apply_transaction([op_set])
                valid_results.append(bid)
            else:
                # Invalid transaction
                op_fail = {
                    'pointer': {'table': 'unknown_table', 'id': bid},
                    'command': 'set',
                    'args': {'type': 'text'}
                }
                try:
                    models.apply_transaction([op_fail])
                except ValueError:
                    fail_results.append(bid)

        threads = [threading.Thread(target=worker_mixed, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(valid_results), 10)
        self.assertEqual(len(fail_results), 10)

        # Confirm all 10 valid blocks exist and 0 invalid blocks exist
        for bid in valid_results:
            self.assertIsNotNone(models.Block.get_or_none(models.Block.id == bid))
        for bid in fail_results:
            self.assertIsNone(models.Block.get_or_none(models.Block.id == bid))


# =============================================================================
# 4. Leaf vs Container Invariants Under Direct API Bypasses
# =============================================================================

class TestLeafVsContainerInvariantsAdversarial(BaseTier5AdversarialTest):
    """Adversarial testing that all 12 leaf types strictly reject children under all direct API bypasses."""

    ALL_12_LEAF_TYPES = [
        'equation', 'divider', 'code', 'image', 'video',
        'audio', 'file', 'pdf', 'bookmark', 'table_row',
        'transclusion_reference', 'sub_page'
    ]

    def test_all_12_leaf_types_reject_list_after_direct_transaction(self):
        """Direct apply_transaction listAfter must fail with ValueError across all 12 leaf types."""
        for leaf_type in self.ALL_12_LEAF_TYPES:
            leaf_id = f"leaf-la-{leaf_type}"
            # Create the leaf block
            models.apply_transaction([models.build_op_set(leaf_id, {'type': leaf_type})])

            # Attempt listAfter
            op_list_after = models.build_op_list_after(leaf_id, f"child-{leaf_type}")
            with self.assertRaises(ValueError, msg=f"Leaf '{leaf_type}' allowed listAfter!"):
                models.apply_transaction([op_list_after])

    def test_all_12_leaf_types_reject_list_before_direct_transaction(self):
        """Direct apply_operation listBefore must fail with ValueError across all 12 leaf types."""
        for leaf_type in self.ALL_12_LEAF_TYPES:
            leaf_id = f"leaf-lb-{leaf_type}"
            models.apply_transaction([models.build_op_set(leaf_id, {'type': leaf_type})])

            op_list_before = {
                'pointer': {'table': 'block', 'id': leaf_id},
                'command': 'listBefore',
                'path': ['content'],
                'args': {'id': f"child-before-{leaf_type}"}
            }
            with self.assertRaises(ValueError, msg=f"Leaf '{leaf_type}' allowed listBefore!"):
                models.apply_transaction([op_list_before])

    def test_all_12_leaf_types_reject_add_child_block_bypass(self):
        """models.add_child_block must reject child addition on all 12 leaf types."""
        for leaf_type in self.ALL_12_LEAF_TYPES:
            leaf_id = f"leaf-acb-{leaf_type}"
            models.apply_transaction([models.build_op_set(leaf_id, {'type': leaf_type})])

            with self.assertRaises(ValueError, msg=f"add_child_block did not reject leaf {leaf_type}"):
                models.add_child_block(leaf_id, {'type': 'text'})

    def test_all_12_leaf_types_reject_move_child_block_as_target(self):
        """models.move_child_block must reject moving a child into any leaf block container."""
        # Create a valid child under a page
        page_id = 'move-src-page'
        models.apply_transaction([models.build_op_set(page_id, {'type': 'page'})])
        child = models.add_child_block(page_id, {'type': 'text'})

        for leaf_type in self.ALL_12_LEAF_TYPES:
            leaf_id = f"leaf-target-{leaf_type}"
            models.apply_transaction([models.build_op_set(leaf_id, {'type': leaf_type})])

            with self.assertRaises(ValueError, msg=f"move_child_block allowed target leaf {leaf_type}"):
                models.move_child_block(child.id, leaf_id)

    def test_all_12_leaf_types_reject_create_block_api_parent(self):
        """create_block_api returns 400 when parent_id points to any leaf block."""
        for leaf_type in self.ALL_12_LEAF_TYPES:
            leaf_id = f"leaf-parent-api-{leaf_type}"
            models.apply_transaction([models.build_op_set(leaf_id, {'type': leaf_type})])

            res, status = backend.create_block_api({
                'type': 'text',
                'parent_id': leaf_id
            })
            self.assertEqual(status, 400, f"create_block_api allowed child under leaf {leaf_type}")
            self.assertIn("leaf node", res.get('error', '').lower())

    def test_validate_block_rejects_content_in_all_12_leaf_types(self):
        """rich_text.validate_block returns False whenever a leaf block dict has content items."""
        for leaf_type in self.ALL_12_LEAF_TYPES:
            block_dict = {
                'type': leaf_type,
                'content': ['illegal-child-uuid'],
            }
            if leaf_type == 'sub_page':
                block_dict['properties'] = {'page_id': 'pg-1', 'title': 'Sub'}
            is_valid, err = rich_text.validate_block(block_dict)
            self.assertFalse(is_valid, f"validate_block permitted content on leaf {leaf_type}")
            self.assertIn("does not permit children", err)

    def test_leaf_to_dict_canonical_content_null_invariant(self):
        """Pure leaf blocks initialized canonically output content as None in to_dict."""
        for leaf_type in self.ALL_12_LEAF_TYPES:
            leaf_id = f"leaf-dict-{leaf_type}"
            models.apply_transaction([models.build_op_set(leaf_id, {'type': leaf_type})])
            blk = models.Block.get_by_id(leaf_id)
            d = blk.to_dict()
            self.assertIsNone(d.get('content'), f"Leaf {leaf_type} content must be None in to_dict, got {d.get('content')}")


# =============================================================================
# 5. Dynamic Toggleable Header Validation When format.toggleable Is Mutated
# =============================================================================

class TestDynamicToggleableHeadersAdversarial(BaseTier5AdversarialTest):
    """Adversarial stress-testing of dynamic header transitions between container and leaf states."""

    HEADER_TYPES = ['header', 'sub_header', 'sub_sub_header', 'header_4']

    def test_headers_non_toggleable_by_default_reject_children(self):
        """All 4 header types start as non-toggleable and reject child operations."""
        for htype in self.HEADER_TYPES:
            hid = f"header-default-{htype}"
            models.apply_transaction([models.build_op_set(hid, {'type': htype, 'format': {}})])

            blk = models.Block.get_by_id(hid)
            self.assertFalse(rich_text.is_container_block(blk.type, blk.format))
            self.assertIsNone(blk.to_dict().get('content'))

            # Direct add_child_block rejected
            with self.assertRaises(ValueError):
                models.add_child_block(hid, {'type': 'text'})

            # Direct listAfter rejected
            with self.assertRaises(ValueError):
                models.apply_transaction([models.build_op_list_after(hid, 'child-uuid')])

            # REST API parent rejected
            res, status = backend.create_block_api({'type': 'text', 'parent_id': hid})
            self.assertEqual(status, 400)

    def test_dynamic_transition_non_toggleable_to_toggleable_allows_children(self):
        """Mutating format.toggleable to True dynamically enables container capabilities."""
        for htype in self.HEADER_TYPES:
            hid = f"header-dyn-{htype}"
            models.apply_transaction([models.build_op_set(hid, {'type': htype, 'format': {}})])

            # Mutate format to toggleable=True
            up_res, up_status = backend.update_block_api(hid, {'format': {'toggleable': True}})
            self.assertEqual(up_status, 200)

            refreshed = models.Block.get_by_id(hid)
            self.assertTrue(rich_text.is_container_block(refreshed.type, refreshed.format))

            # Now adding children must succeed
            child1 = models.add_child_block(hid, {'type': 'text', 'properties': {'title': [['C1', []]]}})
            self.assertIsNotNone(child1)

            # listAfter must succeed
            c2_id = f"c2-{htype}"
            models.apply_transaction([
                models.build_op_set(c2_id, {'type': 'text', 'parent_id': hid}),
                models.build_op_list_after(hid, c2_id, after_id=child1.id)
            ])

            parent_dict = models.Block.get_by_id(hid).to_dict()
            self.assertEqual(parent_dict.get('content'), [str(child1.id), c2_id])

    def test_dynamic_transition_toggleable_back_to_non_toggleable_blocks_new_children(self):
        """Toggling format.toggleable back to False locks container and blocks further child additions."""
        for htype in self.HEADER_TYPES:
            hid = f"header-lock-{htype}"
            models.apply_transaction([
                models.build_op_set(hid, {'type': htype, 'format': {'toggleable': True}})
            ])

            # Add initial child
            c1 = models.add_child_block(hid, {'type': 'text'})
            self.assertIsNotNone(c1)

            # Mutate format.toggleable back to False
            up_res, up_status = backend.update_block_api(hid, {'format': {'toggleable': False}})
            self.assertEqual(up_status, 200)

            locked = models.Block.get_by_id(hid)
            self.assertFalse(rich_text.is_container_block(locked.type, locked.format))

            # Attempting further child additions must now be rejected
            with self.assertRaises(ValueError):
                models.add_child_block(hid, {'type': 'text'})

            with self.assertRaises(ValueError):
                models.apply_transaction([models.build_op_list_after(hid, 'child-3')])

            res, status = backend.create_block_api({'type': 'text', 'parent_id': hid})
            self.assertEqual(status, 400)

            # validate_block detects the structural conflict
            is_val, err = rich_text.validate_block(locked.to_dict())
            self.assertFalse(is_val)
            self.assertIn("does not permit children", err)

    def test_re_enabling_toggleable_restores_container_with_preserved_children(self):
        """Re-enabling toggleable restores valid container state with previously inserted children intact."""
        hid = 'header-re-enable-h4'
        models.apply_transaction([
            models.build_op_set(hid, {'type': 'header_4', 'format': {'toggleable': True}})
        ])
        c1 = models.add_child_block(hid, {'type': 'text'})

        # Disable
        backend.update_block_api(hid, {'format': {'toggleable': False}})

        # Re-enable
        backend.update_block_api(hid, {'format': {'toggleable': True}})

        restored = models.Block.get_by_id(hid)
        self.assertTrue(rich_text.is_container_block(restored.type, restored.format))
        self.assertEqual(restored.to_dict().get('content'), [str(c1.id)])

        # Can add child again
        c2 = models.add_child_block(hid, {'type': 'text'})
        self.assertEqual(models.Block.get_by_id(hid).to_dict().get('content'), [str(c1.id), str(c2.id)])

    def test_toggleable_format_boundary_values(self):
        """Evaluates boundary data types for format.toggleable (bool, int, str, None)."""
        for htype in self.HEADER_TYPES:
            # None / False / 0 / empty dict -> False
            self.assertFalse(rich_text.is_container_block(htype, {}))
            self.assertFalse(rich_text.is_container_block(htype, {'toggleable': False}))
            self.assertFalse(rich_text.is_container_block(htype, {'toggleable': 0}))
            self.assertFalse(rich_text.is_container_block(htype, {'toggleable': None}))
            self.assertFalse(rich_text.is_container_block(htype, "{malformed_json: true}"))

            # True / 1 -> True
            self.assertTrue(rich_text.is_container_block(htype, {'toggleable': True}))
            self.assertTrue(rich_text.is_container_block(htype, {'toggleable': 1}))
            self.assertTrue(rich_text.is_container_block(htype, json.dumps({'toggleable': True})))


if __name__ == '__main__':
    unittest.main()
