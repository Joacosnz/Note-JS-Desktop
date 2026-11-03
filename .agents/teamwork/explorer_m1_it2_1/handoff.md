# Milestone 1 Iteration 2: Explorer 1 Investigation Report

**Subject**: `backend.py:create_block_api` Parameter Resolution & Container Validation Analysis  
**Working Directory**: `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\explorer_m1_it2_1`  
**Date**: 2026-11-02  

---

## 1. Observation

### 1.1 Code Inspection of `backend.py:create_block_api`
In `backend.py` (lines 304–324):
```python
304:     bdata = block_data.get('block', block_data) if isinstance(block_data.get('block'), dict) else block_data
305:     bid = str(bdata.get('id') or uuid.uuid4()).strip()
306:     btype = str(bdata.get('type') or 'text').strip().lower()
307: 
308:     if not is_valid_block_type(btype):
309:         return {'ok': False, 'error': f"Unknown or unsupported block type: '{btype}'"}, 400
310: 
311:     is_valid, err_msg = validate_block(bdata)
312:     if not is_valid:
313:         return {'ok': False, 'error': f"Block validation failed: {err_msg}"}, 400
314: 
315:     parent_id = bdata.get('parent_id') or bdata.get('parentId')
316:     if parent_id is not None:
317:         parent_id = str(parent_id).strip()
318:         if not parent_id:
319:             parent_id = None
320: 
321:     t_idx = bdata.get('target_index', target_index)
322:     a_id = bdata.get('after_id', after_id)
323:     b_id = bdata.get('before_id', before_id)
```

In lines 327–340:
```python
327:         if parent_id is not None:
328:             parent = Block.get_or_none(Block.id == parent_id)
329:             if parent is None:
330:                 return {'ok': False, 'error': f"Parent block with id '{parent_id}' does not exist"}, 404
331:             if parent.alive == 0:
332:                 return {'ok': False, 'error': f"Cannot add child to trashed parent block '{parent_id}'"}, 400
333:             if parent_id == bid:
334:                 return {'ok': False, 'error': "Block cannot be its own parent"}, 400
335: 
336:             # Validación de contenedor estructural de Notion
337:             if not is_container_block(parent.type, parent.format):
338:                 return {'ok': False, 'error': f"Block '{parent.type}' is a leaf node or non-toggleable header and cannot accept children"}, 400
```

In lines 396–416:
```python
396:         else:
397:             # Bloque raíz sin contenedor ejecutado mediante protocolo de transacciones atómicas
398:             child_dict = {
399:                 'id': bid,
400:                 'space_id': str(bdata.get('space_id') or 'default_space'),
401:                 'type': btype,
...
410:                 'parent_id': None,
411:                 'parent_table': str(bdata.get('parent_table') or 'space'),
412:             }
413:             op_set = build_op_set(bid, child_dict, space_id=child_dict['space_id'])
414:             apply_transaction([op_set])
415:             child = Block.get_by_id(bid)
416:             return {'ok': True, 'block': child.to_dict(), 'parent': None}, 201
```

### 1.2 Direct Empirical Reproduction of the Vulnerability
We executed an isolated test in Python to observe the exact response when sending a payload with top-level `parent_id` targeting a pure leaf block (`image`):
- **Command**:
  ```powershell
  py -c "import backend, models; models.init_db(); models.Block.create(id='leaf_test_img', type='image', content=None, format='{}'); res, code = backend.create_block_api({'parent_id': 'leaf_test_img', 'block': {'id': 'nested_child_1', 'type': 'text'}}); print('Result:', code, res); models.Block.delete().where(models.Block.id.in_(['leaf_test_img', 'nested_child_1'])).execute()"
  ```
- **Observed Result**:
  ```
  Result: 201 {'ok': True, 'block': {'id': 'nested_child_1', 'space_id': 'default_space', 'version': 1, 'last_version': 1, 'type': 'text', 'properties': {}, 'content': [], 'parent_id': None, 'parent_table': 'space', 'alive': 1, 'format': {}, 'crdt_format_version': 1, 'crdt_data': {'clock': 1, ...}, 'permissions': [], 'noteId': 0, 'parentId': None, 'sortIndex': 'a0', ...}, 'parent': None}
  ```
- **Consequences directly observed**:
  1. The API returned HTTP status `201` instead of `400`.
  2. The leaf block rejection check (`if not is_container_block(parent.type, parent.format):`) was completely bypassed.
  3. The child block record was committed to SQLite as an orphaned root block (`parent_id = None`, `parent_table = 'space'`).
  4. The caller's intent to place the block under `leaf_test_img` was silently discarded.

### 1.3 Analysis of Payload Formats
The API receives block creation requests in five distinct structural configurations:

| Format ID | Structure Description | Example Payload | Current Behavior in `backend.py` | Required Behavior |
|:---|:---|:---|:---|:---|
| **F1** | Flat payload | `{'id': 'c1', 'type': 'text', 'parent_id': 'p1'}` | Correctly extracts `parent_id = 'p1'` from `bdata` | Validate parent container; reject leaf parents with 400 |
| **F2** | Nested in `'block'` | `{'block': {'id': 'c2', 'type': 'text', 'parent_id': 'p1'}}` | Correctly extracts `parent_id = 'p1'` from `bdata` | Validate parent container; reject leaf parents with 400 |
| **F3** | Top-level `parent_id` with nested `'block'` | `{'parent_id': 'p1', 'block': {'id': 'c3', 'type': 'text'}}` | **FAILS**: `bdata` is inner block; misses `parent_id`, sets `None`, creates orphan with 201 | **Extract `parent_id = 'p1'` from outer `block_data`**, validate container, reject leaf with 400 |
| **F4** | JavaScript camelCase `parentId` at top-level | `{'parentId': 'p1', 'block': {'id': 'c4', 'type': 'text'}}` | **FAILS**: misses `parentId`, creates orphan with 201 | **Extract `parent_id = 'p1'`**, validate container, reject leaf with 400 |
| **F5** | Root block creation | `{'type': 'text'}` or `{'block': {'type': 'text'}}` | `parent_id = None`, creates root block with 201 | Create root block via `op_set` with 201 |

In addition, positioning parameters (`target_index`, `after_id`, `before_id`) and their camelCase counterparts (`targetIndex`, `afterId`, `beforeId`) are currently subject to the identical defect: lines 321–323 query only `bdata`, losing any positioning keys supplied at the top level of `block_data`.

---

## 2. Logic Chain

1. *Premise 1 (R1 & Project Specification)*: Note-JS-Desktop must strictly reject adding child blocks to pure leaf nodes (`divider`, `code`, `equation`, `image`, `video`, `audio`, `file`, `pdf`, `bookmark`, `table_row`, `transclusion_reference`, `sub_page`) and non-toggleable headers, returning HTTP `400 Bad Request`.
2. *Premise 2 (API Design)*: REST APIs and PyWebView client bridges frequently wrap entity data inside a `'block'` envelope while passing relational and routing parameters (`parent_id`, `after_id`, `target_index`) at the top level of the JSON request payload.
3. *Observation 1*: At `backend.py:304`, when `block_data['block']` is a dict, `bdata` is assigned that nested dict.
4. *Observation 2*: At `backend.py:315`, `parent_id = bdata.get('parent_id') or bdata.get('parentId')`. If the client passes `parent_id` at the top level of `block_data`, `parent_id` evaluates to `None`.
5. *Observation 3*: At `backend.py:327`, because `parent_id is None`, the entire container validation block (lines 327–395) is bypassed, and the execution flows into line 396 (`else:`), creating a root block with `parent_id = None` and returning `201 Created`.
6. *Deduction*: Any client submitting Format F3 or F4 to `POST /api/blocks` with a leaf parent bypasses the structural validator and successfully creates an unwanted orphaned root block instead of being rejected with 400.
7. *Conclusion*: `backend.py:create_block_api` must be modified to unpack both layers of the dictionary: inheriting top-level properties into `bdata`, checking `parent_id` / `parentId` across both dictionaries, and resolving positioning parameters across both scopes.

---

## 3. Caveats

1. **Scope Boundary**: This report focuses strictly on `backend.py:create_block_api` (Finding 1 of Reviewer M1 Iteration 1). Finding 2 (`rich_text.py` color decorator CSS sanitization) is investigated separately by Explorer 2.
2. **Explicit `None` vs Missing**: If a client explicitly passes `{"parent_id": None}` or `{"parent_id": ""}`, this represents an explicit request to create a root block without a parent. The extraction logic must treat `None`, empty string `""`, and whitespace-only strings as `None`, correctly falling back to root block creation.
3. **Precedence**: If `parent_id` is specified in both `bdata` and `block_data`, the innermost definition (`bdata`) takes precedence, with fallback to the envelope `block_data`.
4. **No Direct Source Modification**: In accordance with the Explorer archetype constraints, no source files were modified during this investigation.

---

## 4. Conclusion & Proposed Fix Strategy

### 4.1 Recommended Implementation for Worker

In `backend.py`, replace lines 301–324 with the following unified extraction logic:

```python
<<<<
    if not isinstance(block_data, dict):
        return {'ok': False, 'error': 'Block data must be a dictionary'}, 400

    bdata = block_data.get('block', block_data) if isinstance(block_data.get('block'), dict) else block_data
    bid = str(bdata.get('id') or uuid.uuid4()).strip()
    btype = str(bdata.get('type') or 'text').strip().lower()

    if not is_valid_block_type(btype):
        return {'ok': False, 'error': f"Unknown or unsupported block type: '{btype}'"}, 400

    is_valid, err_msg = validate_block(bdata)
    if not is_valid:
        return {'ok': False, 'error': f"Block validation failed: {err_msg}"}, 400

    parent_id = bdata.get('parent_id') or bdata.get('parentId')
    if parent_id is not None:
        parent_id = str(parent_id).strip()
        if not parent_id:
            parent_id = None

    t_idx = bdata.get('target_index', target_index)
    a_id = bdata.get('after_id', after_id)
    b_id = bdata.get('before_id', before_id)
====
    if not isinstance(block_data, dict):
        return {'ok': False, 'error': 'Block data must be a dictionary'}, 400

    # Unpack block data dictionary (supports flat payload and nested {'block': {...}})
    if isinstance(block_data.get('block'), dict):
        bdata = dict(block_data['block'])
        # Inherit top-level metadata fields if not defined inside bdata
        for key in ('id', 'type', 'properties', 'format', 'content', 'space_id', 'note_id', 'alive', 'crdt_data', 'permissions', 'sort_index'):
            if key not in bdata and key in block_data:
                bdata[key] = block_data[key]
    else:
        bdata = dict(block_data)

    bid = str(bdata.get('id') or block_data.get('id') or uuid.uuid4()).strip()
    btype = str(bdata.get('type') or block_data.get('type') or 'text').strip().lower()

    if not is_valid_block_type(btype):
        return {'ok': False, 'error': f"Unknown or unsupported block type: '{btype}'"}, 400

    # Ensure canonical fields are synchronized on bdata prior to validation
    bdata['id'] = bid
    bdata['type'] = btype

    is_valid, err_msg = validate_block(bdata)
    if not is_valid:
        return {'ok': False, 'error': f"Block validation failed: {err_msg}"}, 400

    # Dual-level parent_id resolution: checks nested bdata and top-level block_data (snake_case and camelCase)
    raw_parent_id = (
        bdata.get('parent_id')
        or bdata.get('parentId')
        or block_data.get('parent_id')
        or block_data.get('parentId')
    )
    parent_id = None
    if raw_parent_id is not None:
        parent_id_str = str(raw_parent_id).strip()
        if parent_id_str:
            parent_id = parent_id_str

    # Positioning parameters resolution: bdata -> block_data -> explicit kwargs
    t_idx = None
    for cand in (
        bdata.get('target_index'),
        bdata.get('targetIndex'),
        block_data.get('target_index'),
        block_data.get('targetIndex'),
        target_index,
    ):
        if cand is not None:
            t_idx = cand
            break

    a_id = (
        bdata.get('after_id')
        or bdata.get('afterId')
        or block_data.get('after_id')
        or block_data.get('afterId')
        or after_id
    )

    b_id = (
        bdata.get('before_id')
        or bdata.get('beforeId')
        or block_data.get('before_id')
        or block_data.get('beforeId')
        or before_id
    )
>>>>
```

### 4.2 Defensive Error Handling for Block Insertion
In lines 388–395, wrap `add_child_block` and `apply_transaction` with explicit exception handlers to ensure any underlying `ValueError` from `models.py` cleanly returns HTTP 400:
```python
<<<<
            child = add_child_block(parent_id, child_dict, index=idx, after_id=calc_after_id)
            parent_refreshed = Block.get_or_none(Block.id == parent_id)
            return {
                'ok': True,
                'block': child.to_dict(),
                'parent': parent_refreshed.to_dict() if parent_refreshed else None,
            }, 201
====
            try:
                child = add_child_block(parent_id, child_dict, index=idx, after_id=calc_after_id)
            except ValueError as e:
                return {'ok': False, 'error': str(e)}, 400
            except Exception as e:
                return {'ok': False, 'error': f"Failed to add child block: {str(e)}"}, 500

            parent_refreshed = Block.get_or_none(Block.id == parent_id)
            return {
                'ok': True,
                'block': child.to_dict(),
                'parent': parent_refreshed.to_dict() if parent_refreshed else None,
            }, 201
>>>>
```

### 4.3 Test Harness Extension
In `tests/test_adversarial_m1_structural_stress.py`, inside `test_rest_api_create_block_under_leaf_parent_returns_400`, append assertions for the top-level wrapper payload to prevent future regressions:
```python
        # Test nested block payload with parent_id at top level
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
```

---

## 5. Verification Method

To independently verify this diagnosis and validate the worker's subsequent implementation:

1. **Verify Current Bypass (Before Fix)**:
   ```powershell
   py -c "import backend, models; models.init_db(); models.Block.create(id='leaf_test_img', type='image', content=None, format='{}'); res, code = backend.create_block_api({'parent_id': 'leaf_test_img', 'block': {'id': 'nested_child_1', 'type': 'text'}}); print('Code:', code); assert code == 201; models.Block.delete().where(models.Block.id.in_(['leaf_test_img', 'nested_child_1'])).execute()"
   ```
   *Expected outcome*: prints `Code: 201`, demonstrating the vulnerability.

2. **Verify Fix Behavior (After Fix)**:
   ```powershell
   py -c "import backend, models; models.init_db(); models.Block.create(id='leaf_test_img', type='image', content=None, format='{}'); res, code = backend.create_block_api({'parent_id': 'leaf_test_img', 'block': {'id': 'nested_child_1', 'type': 'text'}}); print('Code:', code); assert code == 400; models.Block.delete().where(models.Block.id == 'leaf_test_img').execute()"
   ```
   *Expected outcome*: prints `Code: 400`, confirming strict rejection of leaf parents across all payload formats.

3. **Verify Adversarial Stress Suite**:
   ```powershell
   py -m unittest tests/test_adversarial_m1_structural_stress.py
   ```

4. **Verify Complete Test Discovery**:
   ```powershell
   py -m unittest discover -s tests
   ```
   *Expected outcome*: 100% passing tests with exit code 0.

5. **Invalidation Conditions**:
   This report's diagnosis is invalidated if a test demonstrates that `backend.py` in its current unmodified state already extracts top-level `parent_id` when `block` is a nested dict (refuted empirically in Section 1.2).
