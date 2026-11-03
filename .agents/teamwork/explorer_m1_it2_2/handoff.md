# Investigation & Fix Strategy: `rich_text.py` Color Sanitization & CSS Injection Defense

**Agent**: Explorer 2 (Milestone 1 Iteration 2)  
**Target**: `rich_text.py:rich_text_to_html` (lines 145–154) and `VALID_COLORS` (lines 30–34)  
**Status**: Completed (Read-only Analysis)  

---

## 1. Observation

### 1.1 Current Color Handling in `rich_text.py`
Direct observation of `rich_text.py`:

- **Lines 30–34 (`VALID_COLORS` definition)**:
  ```python
  VALID_COLORS = {
      'default', 'gray', 'brown', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'red',
      'gray_background', 'brown_background', 'orange_background', 'yellow_background',
      'green_background', 'blue_background', 'purple_background', 'pink_background', 'red_background'
  }
  ```
  *Note*: `VALID_COLORS` is defined here at module top-level but was **never used anywhere in `rich_text.py`**. Furthermore, it contains 19 colors but omits `teal` and `teal_background`.

- **Lines 145–154 (`rich_text_to_html` decorator 'h')**:
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

- **Lines 267–289 (`_RichTextHTMLParser._extract_color`)**:
  ```python
  def _extract_color(self, attrs_dict):
      # 1. data-color
      if 'data-color' in attrs_dict and attrs_dict['data-color']:
          return attrs_dict['data-color'].strip()

      # 2. class="... notion-color-<color> ..."
      cls = attrs_dict.get('class', '')
      for c in cls.split():
          if c.startswith('notion-color-'):
              return c[len('notion-color-'):]

      # 3. style="background-color: ...; color: ...;"
      style = attrs_dict.get('style', '')
      bg_match = re.search(r'background(?:-color)?\s*:\s*([^;]+)', style, re.I)
      if bg_match:
          c = bg_match.group(1).strip().lower()
          return f"{c}_background" if not c.endswith('_background') else c

      color_match = re.search(r'(?<!background-)color\s*:\s*([^;]+)', style, re.I)
      if color_match:
          return color_match.group(1).strip().lower()

      return None
  ```

### 1.2 Reviewer 1 Report & Adversarial Test
From `reviewer_m1_1/handoff.md`:
```
AssertionError: 'font-size' unexpectedly found in '<mark style="color: redfont-size100pxbackgroundurlbad;" class="notion-color-redfont-size100pxbackgroundurlbad" data-color="redfont-size100pxbackgroundurlbad">Text</mark>'
```
And in `tests/test_adversarial_m1_structural_stress.py` lines 731–741:
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

### 1.3 Palette Discrepancy Across the Codebase
- In `frontend/styles.css` (lines 11133 & 11144):
  ```css
  .notion-color-teal { color: #0d9488 !important; }
  .notion-color-teal_background { background-color: rgba(13, 148, 136, 0.25) !important; padding: 2px 4px; border-radius: 3px; }
  ```
- In `frontend/app.js` (lines 6179 & 6189):
  `NOTION_COLOR_HEX_MAP` includes `teal: '#0d9488'` and `teal_background: 'rgba(13, 148, 136, 0.25)'`.
- In `tests/test_adversarial_notion_frontend.py` (line 405 & 417):
  Tuples with `['h', 'teal_background']` are tested and expected to produce `notion-color-teal_background`.
- However, `rich_text.py:VALID_COLORS` does **not** include `teal` or `teal_background`.

---

## 2. Logic Chain

1. **Vulnerability Mechanics**:
   - In `rich_text.py:147`, `clean_color = re.sub(r'[^a-zA-Z0-9_\-]', '', color)` strips punctuation, but explicitly preserves hyphens (`-`).
   - When an attacker provides a payload like `'red; font-size: 100px; background: url("bad")'`, the sanitized string becomes `'redfont-size100pxbackgroundurlbad'`.
   - The substring `'font-size'` remains in the rendered HTML, as highlighted by Reviewer 1.
   - Furthermore, `clean_color` is never checked against `VALID_COLORS`. Arbitrary strings, CSS property names, and garbage tokens are injected into DOM attributes (`style`, `class="notion-color-..."`, and `data-color="..."`).

2. **Analysis of Reviewer 1's Proposed Fix**:
   - Reviewer 1 suggested:
     ```python
     if clean_color not in VALID_COLORS:
         clean_color = 'yellow_background' if 'background' in clean_color else 'yellow'
     ```
   - **Flaw Detected**: If given `'red; font-size: 100px; background: url("bad")'`, the substring `'background'` is present in the adversarial injection. Reviewer 1's check `'background' in clean_color` evaluates to `True`, forcing `clean_color = 'yellow_background'`.
   - As a result, `style_attr` becomes `background-color: yellow;`.
   - However, `tests/test_adversarial_m1_structural_stress.py` line 734 explicitly executes:
     `style_val = html_color.split('style="color: ')[1].split('"')[0].rstrip(';')`
   - Splitting on `'style="color: '` when `style="background-color: ` is generated results in `IndexError: list index out of range` and causes a test suite failure.
   - Additionally, the user's intent was to apply the text color `'red'`. The sanitization should discard the malicious injection suffix and preserve the valid Notion color.

3. **Prefix Extraction & Strict Validation**:
   - Valid Notion color decorators begin with a valid color name (e.g. `'red'`, `'blue_background'`, `'teal'`).
   - By extracting the primary alphanumeric/underscore token before any separator or punctuation:
     `token = re.split(r'[^a-z0-9_]', raw_lower)[0] if raw_lower else ''`
   - If `token in VALID_COLORS`, `clean_color = token`.
     For `'red; font-size: 100px; background: url("bad")'`, `token` is `'red'`, which is valid. The injection is discarded, `'red'` is preserved, and `style="color: red;"` is rendered.
   - If `raw_lower in VALID_COLORS`, `clean_color = raw_lower`.
   - If neither is in `VALID_COLORS`:
     Fall back safely to `'yellow_background'` if the input ends with `_background` (or `'background'` in `token`), otherwise `'yellow'`.
   - This ensures `clean_color` is **provably constrained to `VALID_COLORS`**. It can never contain hyphens, colons, semicolons, quotes, parentheses, spaces, or arbitrary CSS property names.

4. **Completeness & Bidirectional Symmetry**:
   - Adding `teal` and `teal_background` to `VALID_COLORS` synchronizes backend taxonomy with `styles.css` and `app.js`.
   - Validating colors in `_RichTextHTMLParser._extract_color` against `VALID_COLORS` ensures that untrusted HTML input cannot inject invalid colors during `html_to_rich_text` deserialization.

---

## 3. Caveats

- **Scope Boundary**: As an Explorer, this analysis is read-only. Source files have not been modified. Implementation must be performed by the worker agent.
- **Hyphen Policy**: Notion standard colors never contain hyphens (`_background` uses underscores). Stripping hyphens or tokenizing on non-`[a-z0-9_]` is 100% safe and compliant with Notion's color specification.
- **`default` Color**: In Notion, `'default'` denotes standard uncolored text. In `rich_text.py`, it emits `color: default;`, styled appropriately via CSS classes.

---

## 4. Conclusion & Proposed Implementation

### 4.1 Update `VALID_COLORS` in `rich_text.py` (lines 30–34)

```python
VALID_COLORS = {
    'default', 'gray', 'brown', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'red',
    'gray_background', 'brown_background', 'orange_background', 'yellow_background',
    'green_background', 'teal_background', 'blue_background', 'purple_background', 'pink_background', 'red_background'
}
```

### 4.2 Update `rich_text_to_html` (lines 145–154)

Replace:
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
With:
```python
            elif tag == 'h':
                raw_val = str(dec[1]).strip() if len(dec) > 1 and dec[1] is not None else 'yellow'
                raw_lower = raw_val.lower()
                token = re.split(r'[^a-z0-9_]', raw_lower)[0] if raw_lower else ''

                if token in VALID_COLORS:
                    clean_color = token
                elif raw_lower in VALID_COLORS:
                    clean_color = raw_lower
                else:
                    clean_color = 'yellow_background' if raw_lower.endswith('_background') or token.endswith('_background') else 'yellow'

                if clean_color.endswith('_background'):
                    base_bg = clean_color.replace('_background', '')
                    style_attr = f'background-color: {base_bg};'
                else:
                    style_attr = f'color: {clean_color};'
                inner = f'<mark style="{style_attr}" class="notion-color-{clean_color}" data-color="{clean_color}">{inner}</mark>'
```

### 4.3 Update `_RichTextHTMLParser._extract_color` (lines 267–289)

```python
    def _extract_color(self, attrs_dict):
        # 1. data-color
        if 'data-color' in attrs_dict and attrs_dict['data-color']:
            c = attrs_dict['data-color'].strip().lower()
            if c in VALID_COLORS:
                return c

        # 2. class="... notion-color-<color> ..."
        cls = attrs_dict.get('class', '')
        for c in cls.split():
            if c.startswith('notion-color-'):
                col = c[len('notion-color-'):].strip().lower()
                if col in VALID_COLORS:
                    return col

        # 3. style="background-color: ...; color: ...;"
        style = attrs_dict.get('style', '')
        bg_match = re.search(r'background(?:-color)?\s*:\s*([^;]+)', style, re.I)
        if bg_match:
            c = bg_match.group(1).strip().lower()
            col = f"{c}_background" if not c.endswith('_background') else c
            if col in VALID_COLORS:
                return col

        color_match = re.search(r'(?<!background-)color\s*:\s*([^;]+)', style, re.I)
        if color_match:
            c = color_match.group(1).strip().lower()
            if c in VALID_COLORS:
                return c

        return None
```

---

## 5. Verification Method

1. **Verify Adversarial Resilience**:
   ```powershell
   py -m unittest tests/test_adversarial_m1_structural_stress.py
   ```
   *Expected outcome*: Ran 31 tests, OK (exit code 0). Line 731 color injection test passes without `IndexError`, `'font-size'` is absent, and no CSS punctuation exists in the output.

2. **Verify Full Automated Suite**:
   ```powershell
   py -m unittest discover -s tests
   ```
   *Expected outcome*: All tests pass (0 failures, exit code 0).

3. **Verify Round-Trip & Palette Consistency**:
   ```powershell
   py -c "import rich_text; h = rich_text.rich_text_to_html([['T', [['h', 'red; font-size: 100px']]]]); assert 'font-size' not in h and 'color: red;' in h; print('Color Sanitization Verified')"
   ```
   *Expected outcome*: Prints `Color Sanitization Verified`.

4. **Invalidation Condition**:
   Any test failure where `html_color.split('style="color: ')` raises `IndexError` or where unescaped CSS properties or invalid colors are emitted into HTML attributes invalidates the solution.
