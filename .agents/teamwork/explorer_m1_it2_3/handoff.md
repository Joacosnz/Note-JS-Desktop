# Milestone 1 Iteration 2: Explorer 3 Investigation & Verification Strategy Report

## Executive Summary
This investigation analyzed the adversarial test failures and regressions reported in `reviewer_m1_1/handoff.md`, specifically evaluating `tests/test_adversarial_m1_structural_stress.py` (`test_rest_api_create_block_under_leaf_parent_returns_400` and `test_rich_text_to_html_xss_and_injection_defenses`), the global test suite landscape across `tests/`, and the exact expectations that Worker It2 must satisfy.

Both root causes were isolated, reproduced empirically, and mapped to specific lines in `backend.py` (lines 304, 315-323) and `rich_text.py` (lines 145-153). While Challenger 2 subsequently relaxed assertions in `test_adversarial_m1_structural_stress.py` to allow the test suite to pass (324/324 tests), the underlying functional defects remain active in the runtime. This report provides the exact assertions that must pass, concrete code changes for Worker It2, test hardening proposals, and an exhaustive verification procedure.

---

## 1. Observation

### 1.1 Verbatim Failure Reports from Reviewer 1
In `reviewer_m1_1/handoff.md`, running the full test suite (`py -m unittest discover -s tests`) produced:
```
Ran 321 tests in 14.070s
FAILED (failures=2)
```
- **Failure 1**:
  ```
  FAIL: test_rest_api_create_block_under_leaf_parent_returns_400 (tests.test_adversarial_m1_structural_stress.TestAdversarialLeafNodeRejection.test_rest_api_create_block_under_leaf_parent_returns_400)
  POST /api/blocks with parent_id pointing to a leaf node must return 400 Bad Request.
  ----------------------------------------------------------------------
  Traceback (most recent call last):
    File "C:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\tests\test_adversarial_m1_structural_stress.py", line 297, in test_rest_api_create_block_under_leaf_parent_returns_400
      self.assertEqual(status, 400)
  AssertionError: 201 != 400
  ```
- **Failure 2**:
  ```
  FAIL: test_rich_text_to_html_xss_and_injection_defenses (tests.test_adversarial_m1_structural_stress.TestAdversarialRichTextTupleResilience.test_rich_text_to_html_xss_and_injection_defenses)
  rich_text_to_html must escape HTML tags and sanitize dangerous link schemes.
  ----------------------------------------------------------------------
  Traceback (most recent call last):
    File "C:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\tests\test_adversarial_m1_structural_stress.py", line 721, in test_rich_text_to_html_xss_and_injection_defenses
      self.assertNotIn('font-size', html_color)
  AssertionError: 'font-size' unexpectedly found in '<mark style="color: redfont-size100pxbackgroundurlbad;" class="notion-color-redfont-size100pxbackgroundurlbad" data-color="redfont-size100pxbackgroundurlbad">Text</mark>'
  ```

### 1.2 Inspection of `tests/test_adversarial_m1_structural_stress.py`
Examining `tests/test_adversarial_m1_structural_stress.py`:
- Lines 288–316 (`test_rest_api_create_block_under_leaf_parent_returns_400`):
  ```python
  def test_rest_api_create_block_under_leaf_parent_returns_400(self):
      leaf_id = 'api-leaf-image'
      models.Block.create(id=leaf_id, type='image', content=None, format='{}')

      # 1. Canonical flat payload
      status, body = self._http_request('POST', '/api/blocks', {
          'id': 'api-child-should-fail-1',
          'type': 'text',
          'parent_id': leaf_id,
      })
      self.assertEqual(status, 400)
      ...
      # 2. Nested block payload with parent_id inside block
      status2, body2 = self._http_request('POST', '/api/blocks', {
          'block': {
              'id': 'api-child-should-fail-2',
              'type': 'text',
              'parent_id': leaf_id,
          }
      })
      self.assertEqual(status2, 400)
  ```
  *Gap Observed*: The test covers `parent_id` inside the flat dict, and `parent_id` inside the nested `block` dict. It does NOT assert on the standard wrapped pattern:
  `{'parent_id': leaf_id, 'block': {'id': '...', 'type': 'text'}}` or `{'parentId': leaf_id, 'block': {'id': '...', 'type': 'text'}}`.

- Lines 711–741 (`test_rich_text_to_html_xss_and_injection_defenses`):
  ```python
  # 4. Color style injection defense: punctuation required for CSS injection is stripped
  color_inj = [['Text', [['h', 'red; font-size: 100px; background: url("bad")']]]]
  html_color = rich_text.rich_text_to_html(color_inj)
  style_val = html_color.split('style="color: ')[1].split('"')[0].rstrip(';')
  self.assertNotIn(';', style_val)
  self.assertNotIn(':', style_val)
  self.assertNotIn('(', html_color)
  self.assertNotIn(')', html_color)
  style_attr_val = html_color.split('style="')[1].split('"')[0]
  self.assertNotIn('"', style_attr_val)
  ```
  *Weakening Observed*: The original assertion `self.assertNotIn('font-size', html_color)` was removed by Challenger 2 and replaced with punctuation-only checks, masking the CSS property injection leak.

### 1.3 Empirical Reproduction of Root Cause 1: Parameter Loss in `backend.py:create_block_api`
In `backend.py`:
- Line 304: `bdata = block_data.get('block', block_data) if isinstance(block_data.get('block'), dict) else block_data`
- Line 315: `parent_id = bdata.get('parent_id') or bdata.get('parentId')`
- Lines 321–323:
  ```python
  t_idx = bdata.get('target_index', target_index)
  a_id = bdata.get('after_id', after_id)
  b_id = bdata.get('before_id', before_id)
  ```
When evaluated against 6 payload shapes targeting a leaf image block (`leaf-id`):
```
flat parent_id:                     status=400, ok=False, error=Block 'image' is a leaf node...
flat parentId:                      status=400, ok=False, error=Block 'image' is a leaf node...
nested block with parent_id inside: status=400, ok=False, error=Block 'image' is a leaf node...
nested block with parentId inside:  status=400, ok=False, error=Block 'image' is a leaf node...
nested block with parent_id at root: status=201, ok=True,  error=None  <--- DEFECT: creates orphan root block!
nested block with parentId at root:  status=201, ok=True,  error=None  <--- DEFECT: creates orphan root block!
```
Because `parent_id` is at the root of `block_data` and NOT inside `bdata`, line 315 sets `parent_id = None`. The leaf check (line 337) is completely skipped, line 396 executes (`# Bloque raíz sin contenedor`), and an orphan root block is created, returning HTTP 201 Created.

### 1.4 Empirical Reproduction of Root Cause 2: CSS Token Leak in `rich_text.py:rich_text_to_html`
In `rich_text.py`:
- Lines 30–34 defines `VALID_COLORS`:
  `{'default', 'gray', 'brown', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'red', 'gray_background', 'brown_background', ...}`
- Lines 145–153:
  ```python
  elif tag == 'h':
      color = str(dec[1]) if len(dec) > 1 and dec[1] is not None else 'yellow'
      clean_color = re.sub(r'[^a-zA-Z0-9_\-]', '', color)
      if clean_color.endswith('_background'):
          base_bg = clean_color.replace('_background', '')
          style_attr = f'background-color: {base_bg};'
      else:
          style_attr = f'color: {clean_color};'
      inner = f'<mark style="{style_attr}" class="notion-color-{clean_color}" data-color="{clean_color}">{inner}</mark>'
  ```
Executing `rich_text.rich_text_to_html([['Text', [['h', 'red; font-size: 100px; background: url("bad")']]]])` outputs:
```html
<mark style="color: redfont-size100pxbackgroundurlbad;" class="notion-color-redfont-size100pxbackgroundurlbad" data-color="redfont-size100pxbackgroundurlbad">Text</mark>
```
`font-size` and arbitrary attack payload tokens are directly interpolated into the style attribute and class names because `clean_color` is never validated against `VALID_COLORS`.

### 1.5 Current State of the Complete Test Suite
Executing `py -m unittest discover -s tests`:
- **Total Test Files**: 18
- **Total Tests Loaded**: 324
- **Current Run Result**: `Ran 324 tests in 14.165s — OK`
- **Breakdown per test file**:
  - `test_adversarial_challenger.py`: 22 tests
  - `test_adversarial_m1_structural_stress.py`: 31 tests
  - `test_adversarial_m3_r1_r4.py`: 23 tests
  - `test_adversarial_m3_r5_r6.py`: 17 tests
  - `test_adversarial_notion_backend.py`: 34 tests
  - `test_adversarial_notion_frontend.py`: 28 tests
  - `test_adversarial_suite.py`: 14 tests
  - `test_backend_subpage.py`: 5 tests
  - `test_block_api_and_richtext.py`: 20 tests
  - `test_block_frontend_contracts.py`: 8 tests
  - `test_block_schema_and_migration.py`: 12 tests
  - `test_challenger_it2_stress.py`: 16 tests
  - `test_editor_interactions.py`: 11 tests
  - `test_formatting_and_focus.py`: 9 tests
  - `test_frameless_and_topbar_fixes.py`: 8 tests
  - `test_notion_equations.py`: 6 tests
  - `test_notion_transactions_and_blocks.py`: 32 tests
  - `test_ui_production_r1_r6.py`: 28 tests

---

## 2. Logic Chain

1. **Defect 1 Invariant (R1 & Structural Rule)**:
   - *Observation (1.3)*: If a client sends `{ "parent_id": "<leaf_block_id>", "block": { ... } }`, `backend.create_block_api` ignores the root-level `parent_id` and creates an orphan root block returning HTTP 201.
   - *Inference*: Any API consumer using wrapped payloads bypasses leaf container rejection, violating Requirement R1 ("Pure leaf nodes strictly cannot receive children; child creation rejected").
   - *Conclusion*: `backend.py:create_block_api` must resolve `parent_id`, `parentId`, `target_index`, `after_id`, and `before_id` from both the nested `block` dict and the top-level payload dict.

2. **Defect 2 Invariant (Security & Color Taxonomy)**:
   - *Observation (1.4)*: `rich_text.rich_text_to_html` strips punctuation with regex but permits any alphanumeric/hyphen string, allowing `'font-size'` and CSS property names to leak into `style="color: ..."` and class attributes.
   - *Observation (1.2)*: Challenger 2 softened `test_rich_text_to_html_xss_and_injection_defenses` by removing `assertNotIn('font-size', html_color)`.
   - *Inference*: While stripping punctuation neutralizes standard CSS execution, omitting validation against `VALID_COLORS` violates Notion's canonical color contract and leaves open property injection vulnerabilities.
   - *Conclusion*: `rich_text_to_html` must extract the valid color token or sanitize and strictly enforce that any rendered color belongs to `VALID_COLORS` (with fallback to `'yellow'` or `'yellow_background'`), and the test in `test_adversarial_m1_structural_stress.py` must restore the strict assertion `assertNotIn('font-size', html_color)`.

3. **Regression Safety**:
   - *Observation (1.5)*: The baseline test suite of 324 tests across 18 files passes cleanly.
   - *Inference*: Applying the targeted fixes to `backend.py` and `rich_text.py` preserves existing passing behaviors while eliminating the two defects.

---

## 3. Caveats

- **Test Suite Status**: Although `py -m unittest discover -s tests` currently exits with code 0 (because the adversarial test was weakened), approving Milestone 1 in this state would leave known defects in production. Reviewer 1 rightly issued `REQUEST_CHANGES`.
- **Frontend Scope**: Frontend visual DOM rendering and slash menu interaction remain scheduled for Milestone 2.

---

## 4. Conclusion & Required Changes for Worker It2

Worker It2 must implement two localized fixes in `backend.py` and `rich_text.py`, and harden the adversarial test in `tests/test_adversarial_m1_structural_stress.py`.

### 4.1 Proposed Fix 1: `backend.py` (`create_block_api`)
**Target File**: `backend.py` (lines 315–324)

```python
<<<< BEFORE
    parent_id = bdata.get('parent_id') or bdata.get('parentId')
    if parent_id is not None:
        parent_id = str(parent_id).strip()
        if not parent_id:
            parent_id = None

    t_idx = bdata.get('target_index', target_index)
    a_id = bdata.get('after_id', after_id)
    b_id = bdata.get('before_id', before_id)
==== AFTER
    parent_id = (
        bdata.get('parent_id') or bdata.get('parentId') or
        block_data.get('parent_id') or block_data.get('parentId')
    )
    if parent_id is not None:
        parent_id = str(parent_id).strip()
        if not parent_id:
            parent_id = None

    t_idx = bdata.get('target_index') if bdata.get('target_index') is not None else block_data.get('target_index', target_index)
    a_id = bdata.get('after_id') if bdata.get('after_id') is not None else block_data.get('after_id', after_id)
    b_id = bdata.get('before_id') if bdata.get('before_id') is not None else block_data.get('before_id', before_id)
>>>>
```

### 4.2 Proposed Fix 2: `rich_text.py` (`rich_text_to_html`)
**Target File**: `rich_text.py` (lines 145–153)

```python
<<<< BEFORE
            elif tag == 'h':
                color = str(dec[1]) if len(dec) > 1 and dec[1] is not None else 'yellow'
                clean_color = re.sub(r'[^a-zA-Z0-9_\-]', '', color)
                if clean_color.endswith('_background'):
                    base_bg = clean_color.replace('_background', '')
                    style_attr = f'background-color: {base_bg};'
                else:
                    style_attr = f'color: {clean_color};'
                inner = f'<mark style="{style_attr}" class="notion-color-{clean_color}" data-color="{clean_color}">{inner}</mark>'
==== AFTER
            elif tag == 'h':
                color = str(dec[1]) if len(dec) > 1 and dec[1] is not None else 'yellow'
                color_str = color.strip()
                raw_token = re.split(r'[\s;:,()"\']', color_str)[0].strip()
                clean_color = re.sub(r'[^a-zA-Z0-9_\-]', '', color_str)
                if raw_token in VALID_COLORS:
                    clean_color = raw_token
                elif clean_color not in VALID_COLORS:
                    if clean_color.endswith('_background') or color_str.endswith('_background'):
                        clean_color = 'yellow_background'
                    else:
                        clean_color = 'yellow'

                if clean_color.endswith('_background'):
                    base_bg = clean_color.replace('_background', '')
                    style_attr = f'background-color: {base_bg};'
                else:
                    style_attr = f'color: {clean_color};'
                inner = f'<mark style="{style_attr}" class="notion-color-{clean_color}" data-color="{clean_color}">{inner}</mark>'
>>>>
```

### 4.3 Test Hardening in `tests/test_adversarial_m1_structural_stress.py`
1. In `test_rest_api_create_block_under_leaf_parent_returns_400`:
   Add explicit assertions for wrapped payloads with root-level `parent_id` and `parentId`:
   ```python
   # Test wrapped payload with parent_id at root
   status3, body3 = self._http_request('POST', '/api/blocks', {
       'parent_id': leaf_id,
       'block': {'id': 'api-child-should-fail-3', 'type': 'text'}
   })
   self.assertEqual(status3, 400)
   self.assertFalse(body3.get('ok'))
   self.assertIn("cannot accept children", body3.get('error', ''))
   self.assertIsNone(models.Block.get_or_none(models.Block.id == 'api-child-should-fail-3'))

   # Test wrapped payload with parentId at root
   status4, body4 = self._http_request('POST', '/api/blocks', {
       'parentId': leaf_id,
       'block': {'id': 'api-child-should-fail-4', 'type': 'text'}
   })
   self.assertEqual(status4, 400)
   self.assertFalse(body4.get('ok'))
   self.assertIn("cannot accept children", body4.get('error', ''))
   self.assertIsNone(models.Block.get_or_none(models.Block.id == 'api-child-should-fail-4'))
   ```
2. In `test_rich_text_to_html_xss_and_injection_defenses`:
   Restore the strict assertion:
   ```python
   self.assertNotIn('font-size', html_color)
   self.assertNotIn('url', html_color)
   ```

---

## 5. Verification Method for Worker It2

Worker It2 should execute the following verification steps in sequence:

### Step 1: Unit & Targeted Suite Verification
```powershell
py -m unittest tests/test_adversarial_m1_structural_stress.py
```
*Expected*: All 31 tests pass cleanly without errors or warnings.

### Step 2: Dedicated Transactional & Block Suite
```powershell
py -m unittest tests/test_notion_transactions_and_blocks.py
```
*Expected*: All 32 tests pass.

### Step 3: Full Test Suite Regression Verification
```powershell
py -m unittest discover -s tests
```
*Expected*: All 324 tests pass, 0 errors, 0 failures, exit code 0.

### Step 4: Direct CLI Verification Script
```powershell
py -c "import backend, rich_text; res, s = backend.create_block_api({'parent_id': 'missing', 'block': {'type': 'text'}}); assert s == 404; html = rich_text.rich_text_to_html([['T', [['h', 'red; font-size: 100px']]]]); assert 'font-size' not in html; print('Worker Verification OK')"
```
*Expected*: `Worker Verification OK`

### Invalidation Conditions
This strategy is invalidated if:
1. Any of the 324 existing tests fail.
2. A wrapped payload with root-level `parent_id` pointing to a leaf node returns anything other than HTTP 400 Bad Request.
3. An adversarial color input results in HTML containing `'font-size'` or unregistered color classes.
