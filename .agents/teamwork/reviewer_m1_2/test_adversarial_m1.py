#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

import json
import time
import uuid
import threading
import tempfile
from peewee import SqliteDatabase

# Setup isolated database
temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
test_db_path = os.path.join(temp_dir.name, 'adversarial_test.db')

import models
import backend
import rich_text

orig_db = models.db
test_db = SqliteDatabase(test_db_path, pragmas={
    'journal_mode': 'wal',
    'busy_timeout': 10000,
}, timeout=15, check_same_thread=False)

models.db = test_db
models.BaseModel._meta.database = test_db
for m in [models.Note, models.Folder, models.Setting, models.NoteHistory,
         models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord]:
    m._meta.database = test_db

test_db.connect(reuse_if_open=True)
models.init_db()

results = {}

print("=== 1. LEAF NODE REJECTION ===")
leaf_types = list(rich_text.LEAF_BLOCK_TYPES)
orm_leaf_results = {}
api_leaf_results = {}

for lt in leaf_types:
    bid = f"leaf-orm-{lt}"
    props = {'page_id': 'sub-uuid'} if lt == 'sub_page' else {}
    models.Block.create(
        id=bid, type=lt, properties=json.dumps(props),
        content=None, format='{}', alive=1
    )
    # 1. ORM add_child_block
    try:
        models.add_child_block(bid, {'type': 'text'})
        orm_leaf_results[lt] = "FAILED (allowed child)"
    except ValueError as e:
        orm_leaf_results[lt] = "OK (rejected with ValueError)"
    except Exception as e:
        orm_leaf_results[lt] = f"FAILED ({type(e).__name__}: {e})"

    # 2. REST API create_block_api
    resp, code = backend.create_block_api({'type': 'text', 'parent_id': bid})
    if code == 400 and not resp.get('ok'):
        api_leaf_results[lt] = "OK (HTTP 400)"
    else:
        api_leaf_results[lt] = f"FAILED (status {code}, resp={resp})"

results['orm_leaf_rejection'] = orm_leaf_results
results['api_leaf_rejection'] = api_leaf_results
print(f"ORM Leaf Rejection: {all('OK' in v for v in orm_leaf_results.values())}")
print(f"API Leaf Rejection: {all('OK' in v for v in api_leaf_results.values())}")

print("\n=== 2. TOGGLEABLE HEADER TRANSITION ===")
# Create toggleable header with toggleable = True
h_id = "header-toggle-test"
models.Block.create(
    id=h_id, type="header", properties=json.dumps({'title': [['Title', []]]}),
    format=json.dumps({'toggleable': True}), content=json.dumps([]), alive=1
)
# Add child
c1 = models.add_child_block(h_id, {'id': 'child-h1', 'type': 'text'})
# Check child was added
h_row = models.Block.get(models.Block.id == h_id)
assert 'child-h1' in json.loads(h_row.content)

# Now toggle format to toggleable = False via update_block_api
up_resp, up_code = backend.update_block_api(h_id, {'format': {'toggleable': False}})
h_row_after = models.Block.get(models.Block.id == h_id)
h_dict_after = h_row_after.to_dict()

# Try adding another child now via ORM
orm_post_toggle_rejected = False
try:
    models.add_child_block(h_id, {'id': 'child-h2', 'type': 'text'})
except ValueError:
    orm_post_toggle_rejected = True

# Try adding another child now via API
api_post_toggle_resp, api_post_toggle_code = backend.create_block_api({'type': 'text', 'parent_id': h_id})
api_post_toggle_rejected = (api_post_toggle_code == 400 and not api_post_toggle_resp.get('ok'))

results['toggle_transition'] = {
    'update_code': up_code,
    'persisted_content_after_toggle_off': json.loads(h_row_after.content),
    'to_dict_content_after_toggle_off': h_dict_after.get('content'),
    'orm_post_toggle_rejected': orm_post_toggle_rejected,
    'api_post_toggle_rejected': api_post_toggle_rejected,
}
print(f"Toggle transition results: {results['toggle_transition']}")

print("\n=== 3. CYCLIC PARENT DETECTION ===")
# A) create_block_api self-parent
self_parent_resp, self_parent_code = backend.create_block_api({'id': 'self-p', 'type': 'text', 'parent_id': 'self-p'})
print(f"API self-parent: {self_parent_code}, ok={self_parent_resp.get('ok')}")

# B) create_block_api ancestor cycle: p1 -> p2 -> p3, then try to make p1 child of p3
p1 = models.Block.create(id='p1', type='page', content=json.dumps(['p2']), alive=1)
p2 = models.Block.create(id='p2', type='page', parent_id='p1', content=json.dumps(['p3']), alive=1)
p3 = models.Block.create(id='p3', type='page', parent_id='p2', content=json.dumps([]), alive=1)

cycle_api_resp, cycle_api_code = backend.create_block_api({'id': 'p1', 'type': 'page', 'parent_id': 'p3'})
print(f"API ancestor cycle: {cycle_api_code}, ok={cycle_api_resp.get('ok')}, error={cycle_api_resp.get('error')}")

# C) ORM add_child_block self-parent
orm_self_parent_caught = False
try:
    models.add_child_block('p1', {'id': 'p1', 'type': 'text'})
except Exception as e:
    orm_self_parent_caught = True
    print(f"ORM add_child_block self-parent caught with: {type(e).__name__}: {e}")

# D) ORM move_child_block cycle: move p1 under p3
orm_cycle_caught = False
try:
    models.move_child_block('p1', 'p3')
    # Check if cycle was created
    p1_check = models.Block.get(models.Block.id == 'p1')
    print(f"ORM move_child_block result: p1.parent_id is now {p1_check.parent_id}")
    if p1_check.parent_id == 'p3':
        orm_cycle_caught = False
except Exception as e:
    orm_cycle_caught = True
    print(f"ORM move_child_block caught cycle: {type(e).__name__}: {e}")

# E) resolve_subtree_record_map with existing cycle: does it infinite loop?
# In case a cycle exists in DB, let's see if BFS hangs or safely halts
sub_res = models.resolve_subtree_record_map('p1')
print(f"resolve_subtree_record_map with potential cycle returned {len(sub_res.get('block', {}))} blocks without hanging.")

results['cycle_handling'] = {
    'api_self_parent_rejected': self_parent_code == 400,
    'api_ancestor_cycle_rejected': cycle_api_code == 400,
    'orm_self_parent_caught': orm_self_parent_caught,
    'orm_move_child_cycle_caught': orm_cycle_caught,
    'resolve_subtree_safely_halts': 'p1' in sub_res.get('block', {}),
}

print("\n=== 4. CORRUPTED PAYLOAD HANDLING ===")
corrupt_results = {}

# A) Corrupted parent.content in SQLite
corrupt_parent = models.Block.create(
    id='corrupt-p', type='page', content="[INVALID JSON", properties='{}', format='{}', alive=1
)
try:
    c_child = models.add_child_block('corrupt-p', {'id': 'child-of-corrupt', 'type': 'text'})
    corrupt_results['corrupted_parent_content_recovered'] = True
except Exception as e:
    corrupt_results['corrupted_parent_content_recovered'] = False
    print(f"Corrupted parent content exception: {e}")

# B) Corrupted properties and format in to_dict()
corrupt_block = models.Block.create(
    id='corrupt-fields', type='page', properties="{NOT JSON", format="NOT JSON", crdt_data="NOT JSON",
    content="NOT JSON", alive=1
)
try:
    d = corrupt_block.to_dict()
    corrupt_results['to_dict_resilient_to_corrupt_json'] = (
        isinstance(d['properties'], dict) and
        isinstance(d['format'], dict) and
        isinstance(d['crdt_data'], dict) and
        isinstance(d['content'], list)
    )
except Exception as e:
    corrupt_results['to_dict_resilient_to_corrupt_json'] = False
    print(f"to_dict exception on corrupt fields: {e}")

# C) Malformed operations in apply_transaction
tx_corrupt_results = []
for bad_ops in [
    None,
    "not a list",
    [],
    [None],
    ["not a dict"],
    [{'command': 'unknown_cmd', 'pointer': {'table': 'block', 'id': 'x'}}],
    [{'command': 'set', 'pointer': {'table': 'unknown_table', 'id': 'x'}}],
    [{'command': 'set', 'pointer': {'table': 'block'}}], # missing id
]:
    try:
        res = models.apply_transaction(bad_ops)
        tx_corrupt_results.append(f"ALLOWED ({bad_ops})")
    except ValueError:
        tx_corrupt_results.append("REJECTED_VALUE_ERROR")
    except Exception as e:
        tx_corrupt_results.append(f"EXCEPTION_{type(e).__name__}")

corrupt_results['tx_malformed_operations'] = tx_corrupt_results

# D) Corrupted args in apply_operation('set')
try:
    res = models.apply_operation({
        'command': 'set',
        'pointer': {'table': 'block', 'id': 'bad-args-id'},
        'args': None
    })
    corrupt_results['apply_operation_set_none_args'] = "Handled gracefully"
except Exception as e:
    corrupt_results['apply_operation_set_none_args'] = f"Raised {e}"

# E) Corrupted args in apply_operation('listAfter')
try:
    res = models.apply_operation({
        'command': 'listAfter',
        'pointer': {'table': 'block', 'id': 'corrupt-p'},
        'args': None
    })
    corrupt_results['apply_operation_listAfter_none_args'] = "Handled gracefully"
except Exception as e:
    corrupt_results['apply_operation_listAfter_none_args'] = f"Raised {e}"

results['corrupted_payload_handling'] = corrupt_results
print(f"Corrupted payload results: {json.dumps(corrupt_results, indent=2)}")

print("\n=== 5. CONCURRENCY & WAL MODE STRESS TEST ===")
concurrency_errors = []
num_threads = 10
ops_per_thread = 20

# Create root page for concurrent child creations
concur_root = models.Block.create(id='concur-root', type='page', content=json.dumps([]), alive=1)

def worker_task(tid):
    for i in range(ops_per_thread):
        cid = f"concur-{tid}-{i}"
        try:
            models.add_child_block('concur-root', {'id': cid, 'type': 'text', 'properties': {'title': [[f'T{tid}-{i}', []]]}})
            # Also do a read
            b = models.Block.get_or_none(models.Block.id == cid)
            if not b:
                concurrency_errors.append(f"Thread {tid} could not read just created block {cid}")
        except Exception as e:
            concurrency_errors.append(f"Thread {tid} op {i} failed: {type(e).__name__}: {e}")

threads = [threading.Thread(target=worker_task, args=(t,)) for t in range(num_threads)]
start_t = time.time()
for th in threads:
    th.start()
for th in threads:
    th.join()
duration = time.time() - start_t

root_after = models.Block.get(models.Block.id == 'concur-root')
final_children = json.loads(root_after.content)

results['concurrency'] = {
    'num_threads': num_threads,
    'total_ops': num_threads * ops_per_thread,
    'duration_sec': round(duration, 3),
    'errors_count': len(concurrency_errors),
    'errors_sample': concurrency_errors[:5],
    'children_recorded_in_root': len(final_children),
}
print(f"Concurrency results: {results['concurrency']}")

test_db.close()
temp_dir.cleanup()
print("\nAll adversarial tests completed.")
