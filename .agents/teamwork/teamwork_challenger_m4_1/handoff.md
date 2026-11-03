# Challenger 1 Adversarial Verification Report: Backend Database, ORM, Consistency & API

**Author**: Challenger 1 (Milestone 4 — Adversarial Verification & Coverage Hardening)  
**Target Scope**: Backend Database (`models.py`, `init_db`), Peewee ORM (`Block`, `Note`), Consistency Algorithms (`resolve_subtree_record_map`, `soft_delete_block`, `restore_block`, `move_child_block`), and API Endpoints (`backend.py`, `/api/blocks/*`)  
**Verdict**: **APPROVE** (Backend Layer)

---

## 1. Observation

### 1.1 Test Suite Creation & Execution
- Authored test suite: `tests/test_adversarial_notion_backend.py` containing 34 empirical stress tests covering 6 adversarial dimensions.
- Command: `py -m unittest tests.test_adversarial_notion_backend -v`
  - Result:
    ```
    Ran 34 tests in 4.021s
    OK
    ```
- All backend-related test suites combined:
  `py -m unittest tests.test_adversarial_notion_backend tests.test_block_schema_and_migration tests.test_block_api_and_richtext tests.test_backend_subpage -v`
  - Result:
    ```
    Ran 71 tests in 6.290s
    OK
    ```
- Full repository test discovery:
  `py -m unittest discover -s tests -p "test_*.py"`
  - Result: 255 tests executed; all backend suites passed 100%; 5 failures were observed exclusively in `tests/test_adversarial_notion_frontend.py` (Challenger 2's frontend XSS and formula escaping suite in `frontend/app.js`).

### 1.2 Observed Behaviors by Adversarial Category

1. **Deep Hierarchy Nesting (15+, 30+, 50+ levels)**:
   - Line 1527 of `models.py`: `resolve_subtree_record_map(root_id)` uses an iterative Breadth-First Search (`queue = [root]`) with `while queue:` and a `visited` set.
   - Line 200 of `backend.py`: `resolve_block_record_map(root_id)` similarly employs an iterative BFS queue.
   - Tested 15-level, 30-level, and 50-level deep parent-child chains (`test_01`, `test_02`, `test_03`), as well as a 106-block wide-and-deep tree (`test_06`).
   - Verified that `resolve_subtree_record_map`, `GET /api/blocks/<id>/recordMap`, and `bridge.get_block_record_map` resolved all nodes completely without stack frame recursion or `RecursionError`.
   - Verified that cascading soft-delete (`test_05`) on a 25-level tree marks all 26 nodes with `alive = 0` without hitting Python's recursion limit.

2. **Cycle Attacks & Circular Parent Pointers**:
   - Tested 2-node cycle (`test_07`: A->B->A), 3-node cycle (`test_08`: A->B->C->A), and self-cycle (`test_09`: A->A).
   - In `models.py:1559` (`if cid_str not in visited: visited.add(cid_str); ... queue.append(child)`), visited nodes are checked before enqueuing.
   - Both `resolve_subtree_record_map` and `backend.resolve_block_record_map` terminate in finite time with O(V + E) complexity and zero infinite loops.
   - Line 324-338 of `backend.py`:
     ```python
     if parent_id == bid:
         return {'ok': False, 'error': "Block cannot be its own parent"}, 400
     visited = {parent_id}
     curr = parent
     while curr and curr.parent_id:
         p_up = str(curr.parent_id)
         if p_up == bid:
             return {'ok': False, 'error': "Circular block hierarchy detected"}, 400
     ```
   - Attempting to set parent to self returns 400 (`test_11`); attempting to set parent to a descendant returns 400 (`test_12`).
   - Cascading soft-delete on an artificial cyclic graph (`test_13`) terminates cleanly and sets `alive = 0` on all cycle members without looping.

3. **Malformed / Corrupted Payloads in JSON Fields**:
   - Line 283-317 of `models.py`: `Block.to_dict()` wraps `json.loads` calls for `properties`, `content`, `format`, `crdt_data`, and `permissions` in `try...except Exception:` blocks with type validation fallback (`if not isinstance(props, dict): props = {}`).
   - Blocks with invalid JSON strings (`test_14`), scalar types (`test_15`), or `None` values (`test_16`) produce normalized Python dictionaries and lists.
   - SQLite enforces `NOT NULL` constraints on `block.properties` at the database engine level, rejecting raw `NULL` insertions with `IntegrityError` (`test_16`).
   - Sent a ~500KB giant payload containing 200,000 characters in rich-text title and 1,000 properties (`test_17`); successfully saved and retrieved with 200/201 OK.
   - Rich text tuple parser (`test_18`) with corrupt decorators, non-list segments, and missing decorator parameters handles all inputs without uncaught exceptions.
   - Malformed HTTP bodies (`test_19`: broken JSON, non-object JSON arrays, empty bodies) return 400 Bad Request.

4. **Optimistic Concurrency Collisions**:
   - Line 434-446 of `backend.py`:
     ```python
     exp_v = up_data.get('expected_version', expected_version)
     if exp_v is not None:
         exp_v_int = int(exp_v)
         if blk.version != exp_v_int:
             return {
                 'ok': False,
                 'error': 'Version conflict',
                 'current_version': blk.version,
                 'expected_version': exp_v_int,
             }, 409
     ```
   - Stale `expected_version` reliably returns 409 Conflict (`test_20`, `test_22`). Matching `expected_version` increments version and returns 200 OK (`test_21`).
   - Rapid parallel stress test (`test_23`): 10 concurrent threads updating the same block with `expected_version = 1` resulted in exactly 1 successful update (200 OK) and 9 conflict rejections (409 Conflict), maintaining database integrity at version 2.

5. **Orphaned Blocks, Cascade Soft-Delete, and Selective Restoration**:
   - Line 1356-1441 of `models.py`: `soft_delete_block` sets `alive = 0` on target and recursively cascades to all descendants, while removing the deleted block from its parent's `content` array.
   - Tested 7-node multi-branch tree (`test_25`): all 7 blocks were marked with `alive = 0`, physical rows were preserved in SQLite, and root recorded `soft_delete` in CRDT.
   - Line 1485-1524 of `models.py`: `restore_block` checks `if parent and parent.alive == 1` before re-inserting the child into the parent's `content` array.
   - Selective restoration (`test_26`): restoring a child with a dead parent sets `child.alive = 1` without attaching to the trashed parent.
   - Reviving the parent followed by child restoration (`test_27`) re-establishes the child inside the parent's `content` array.
   - Orphan block queries (`test_28`): blocks with non-existent parent IDs can be retrieved directly and via recordMap, and can be adopted by a new parent.

6. **SQL Injection Hardening**:
   - Peewee queries parameterize SQL variables (`Block.id == str(block_id)`).
   - Injected payloads in `GET /api/blocks/<id>` (`test_30`), `GET /recordMap` (`test_31`), `DELETE /api/blocks/<id>` (`test_32`), and legacy note blocks (`test_34`) returned 400/404 without executing SQL.
   - Injected SQL strings inside properties and format fields (`test_33`) were saved verbatim as text strings; tables `block` and `notes` remained completely intact.

---

## 2. Logic Chain

1. **Premise 1 (Stack Safety)**: Stack overflow in tree resolution occurs when recursion depth scales with tree depth. In `models.py` and `backend.py`, tree traversal is implemented using queue-based Breadth-First Search (iteration rather than recursion). Therefore, deep linear trees (up to 50+ levels tested) cannot cause a stack overflow.
2. **Premise 2 (Cycle Safety)**: Infinite loops in graph traversal occur when previously visited nodes are re-queued. In `resolve_subtree_record_map` and `resolve_block_record_map`, every node ID is added to a `visited` set before being appended to the queue. Therefore, cyclic graphs (direct or multi-node) terminate in exactly $O(V + E)$ operations.
3. **Premise 3 (Cycle Prevention)**: `create_block_api` checks whether `parent_id == id` and traverses the ancestor chain. Any attempt to form a circular hierarchy is rejected with HTTP 400 before persistence.
4. **Premise 4 (Crash Resilience)**: All JSON deserialization in `Block.to_dict()` and `rich_text` conversion uses defensive type-checking and exception fallbacks. Corrupted payloads in SQLite or HTTP requests degrade to safe defaults rather than unhandled 500 exceptions.
5. **Premise 5 (Concurrency Consistency)**: Mutex `DB_LOCK` combined with atomic SQLite transactions and version comparison (`blk.version != exp_v_int`) guarantees that parallel writes are serialized, preventing lost updates and returning 409 Conflict to stale clients.
6. **Premise 6 (SQL Safety)**: Peewee ORM uses parameterized SQLite queries (`?` parameter substitution). No string formatting or concatenation is used in SQL queries for blocks, rendering SQL injection ineffective.

---

## 3. Caveats

- **Scope Boundary**: This evaluation covers the Backend Database, ORM, Consistency, and API layers. Frontend UI rendering, DOM sanitization, and browser-side XSS defenses are handled by Challenger 2 (`tests/test_adversarial_notion_frontend.py`).
- **Single-Machine Architecture**: Concurrency testing was performed using multiple OS threads on a single local process. Multi-process write locks in SQLite rely on SQLite's WAL mode and `busy_timeout` (10,000ms configured in `models.py`).

---

## 4. Conclusion & Verdict

**Verdict**: **APPROVE** (Backend Database, ORM, Consistency & API)

The backend block architecture meets all resilience, concurrency, security, and hierarchy contracts defined in `ORIGINAL_REQUEST.md` and `PROJECT.md`. Deep hierarchies, circular structures, corrupted payloads, race conditions, soft-deletion lifecycles, and SQL injection vectors were empirically tested and survived without data corruption, infinite loops, or crashes.

---

## 5. Verification Method

To independently reproduce and verify this assessment:

1. **Run the Adversarial Backend Test Suite**:
   ```powershell
   py -m unittest tests.test_adversarial_notion_backend -v
   ```
   *Expected outcome*: 34 tests run, 34 pass (OK).

2. **Run All Backend Modules**:
   ```powershell
   py -m unittest tests.test_adversarial_notion_backend tests.test_block_schema_and_migration tests.test_block_api_and_richtext tests.test_backend_subpage -v
   ```
   *Expected outcome*: 71 tests run, 71 pass (OK).

3. **Key Source Files for Code Inspection**:
   - `models.py`: Lines 249-350 (`Block` definition & `to_dict`), 984-1110 (`add_child_block`), 1343-1443 (`soft_delete_block` & `_cascade_soft_delete`), 1446-1525 (`restore_block`), 1527-1566 (`resolve_subtree_record_map`).
   - `backend.py`: Lines 190-238 (`resolve_block_record_map`), 310-378 (`create_block_api` & cycle defense), 416-524 (`update_block_api` & 409 Conflict validation).
   - `tests/test_adversarial_notion_backend.py`: Full test implementation.
