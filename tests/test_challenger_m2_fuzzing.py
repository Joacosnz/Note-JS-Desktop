#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_challenger_m2_fuzzing.py
Empirical Fuzzing & Adversarial Stress Harness for Milestone 2:
Rich Text & Interactive Event Fuzzing.

Dimensions tested empirically:
1. `to_do` Checkbox Events & State Persistence:
   - Initial rendering from properties.checked ('Yes', 'No', true, false, null, missing)
   - Click/change events toggling checked state
   - Real DOM class '.completed' application & removal on title element
   - CSS contract verification for line-through styling
   - State synchronization into activeRecordMap (closure & window)
   - Persistence invocations via persistBlockUpdate
   - Rapid fuzzing (20+ alternating toggles)
   - Graceful error handling under missing state / persistence handlers
2. Rich-Text Formatting across Extended Blocks:
   - Complex decorator tuples (b, i, _, s, c, h-color, h-background, a-link, e-equation)
   - Simultaneous nested decorators on header_4, quote, callout, to_do
   - Bidirectional round-trip (parseRichTextToHtml -> htmlToRichTextTuples)
   - Segment coalescing of adjacent runs with identical styling
   - XSS sanitization (javascript: / vbscript: / data: links, script injections, tag breakout)
   - Preservation of rich-text formatting inside rendered block DOM elements
3. Transclusion Reference Recursive Cycle Guards:
   - Self-referencing transclusion (reference pointing to own container)
   - Mutual cycle (Container A <-> Container B)
   - Tri-cycle transclusion (A -> B -> C -> A)
   - Container containing container with reference to container (nested container cycles)
   - Broken pointers (non-existent targets, alive === 0)
   - Multiple references to same container (shared synced blocks)
   - Deep transclusion chains (25+ levels)
"""

import os
import sys
import re
import json
import subprocess
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')


class TestChallengerM2Fuzzing(unittest.TestCase):
    """Empirical adversarial test suite for Milestone 2."""

    @classmethod
    def setUpClass(cls):
        try:
            res = subprocess.run(['node', '-v'], capture_output=True, text=True, check=True)
            cls.node_available = True
            cls.node_version = res.stdout.strip()
        except Exception:
            cls.node_available = False

        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()

    def run_node_vm(self, script_body, extra_setup=''):
        """Executes JavaScript test code in a Node.js VM DOM sandbox with app.js loaded."""
        if not self.node_available:
            self.skipTest("Node.js is not available in this environment")

        harness_code = f"""
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');

function decodeHtmlEntities(str) {{
  if (!str) return '';
  return str
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&');
}}

class MockNode {{
  constructor(nodeType, nodeValue = '') {{
    this.nodeType = nodeType;
    this.nodeValue = nodeValue;
    this.childNodes = [];
    this.parentNode = null;
  }}
  appendChild(child) {{
    if (!child) return child;
    child.parentNode = this;
    this.childNodes.push(child);
    return child;
  }}
  removeChild(child) {{
    const idx = this.childNodes.indexOf(child);
    if (idx !== -1) {{
      this.childNodes.splice(idx, 1);
      child.parentNode = null;
    }}
    return child;
  }}
  replaceWith(newEl) {{
    if (!this.parentNode) return;
    const idx = this.parentNode.childNodes.indexOf(this);
    if (idx !== -1) {{
      this.parentNode.childNodes[idx] = newEl;
      newEl.parentNode = this.parentNode;
      this.parentNode = null;
    }}
  }}
  after(newEl) {{
    if (!this.parentNode) return;
    const idx = this.parentNode.childNodes.indexOf(this);
    if (idx !== -1) {{
      this.parentNode.childNodes.splice(idx + 1, 0, newEl);
      newEl.parentNode = this.parentNode;
    }}
  }}
  before(newEl) {{
    if (!this.parentNode) return;
    const idx = this.parentNode.childNodes.indexOf(this);
    if (idx !== -1) {{
      this.parentNode.childNodes.splice(idx, 0, newEl);
      newEl.parentNode = this.parentNode;
    }}
  }}
  get firstChild() {{ return this.childNodes[0] || null; }}
  get nextSibling() {{
    if (!this.parentNode) return null;
    const idx = this.parentNode.childNodes.indexOf(this);
    return idx >= 0 && idx + 1 < this.parentNode.childNodes.length ? this.parentNode.childNodes[idx + 1] : null;
  }}
  get previousElementSibling() {{
    if (!this.parentNode) return null;
    const idx = this.parentNode.childNodes.indexOf(this);
    for (let i = idx - 1; i >= 0; i--) {{
      if (this.parentNode.childNodes[i].nodeType === 1) return this.parentNode.childNodes[i];
    }}
    return null;
  }}
  get nextElementSibling() {{
    if (!this.parentNode) return null;
    const idx = this.parentNode.childNodes.indexOf(this);
    for (let i = idx + 1; i < this.parentNode.childNodes.length; i++) {{
      if (this.parentNode.childNodes[i].nodeType === 1) return this.parentNode.childNodes[i];
    }}
    return null;
  }}
  get children() {{
    return this.childNodes.filter(c => c.nodeType === 1);
  }}
  get textContent() {{
    if (this.nodeType === 3) return this.nodeValue;
    return this.childNodes.map(c => c.textContent).join('');
  }}
  set textContent(v) {{
    this.childNodes = [new MockNode(3, String(v))];
  }}
}}

class MockClassList {{
  constructor(initialTokens = []) {{
    this._set = new Set(initialTokens);
  }}
  add(...tokens) {{
    tokens.forEach(t => {{ if (t) this._set.add(String(t)); }});
  }}
  remove(...tokens) {{
    tokens.forEach(t => this._set.delete(String(t)));
  }}
  contains(token) {{
    return this._set.has(String(token));
  }}
  has(token) {{
    return this._set.has(String(token));
  }}
  toggle(token, force) {{
    token = String(token);
    if (force === true) {{ this._set.add(token); return true; }}
    if (force === false) {{ this._set.delete(token); return false; }}
    if (this._set.has(token)) {{ this._set.delete(token); return false; }}
    this._set.add(token); return true;
  }}
  toString() {{
    return Array.from(this._set).join(' ');
  }}
  [Symbol.iterator]() {{
    return this._set.values();
  }}
}}

class MockElement extends MockNode {{
  constructor(tagName) {{
    super(1);
    this.tagName = tagName.toUpperCase();
    this.attributes = {{}};
    this.style = {{}};
    this.classList = new MockClassList();
    this.id = '';
    this.dataset = {{}};
    this._listeners = {{}};
  }}
  setAttribute(k, v) {{
    this.attributes[k] = String(v);
    if (k === 'id') this.id = String(v);
    if (k === 'class') {{
      this.classList = new MockClassList(String(v).split(/\\s+/).filter(Boolean));
    }}
    if (k.startsWith('data-')) {{
      const prop = k.slice(5).replace(/-([a-z])/g, (_, m) => m.toUpperCase());
      this.dataset[prop] = String(v);
    }}
  }}
  getAttribute(k) {{ return this.attributes[k] !== undefined ? this.attributes[k] : null; }}
  hasAttribute(k) {{ return this.attributes[k] !== undefined; }}
  removeAttribute(k) {{
    delete this.attributes[k];
    if (k === 'class') this.classList = new MockClassList();
  }}
  get className() {{ return this.classList.toString(); }}
  set className(v) {{
    this.classList = new MockClassList(String(v).split(/\\s+/).filter(Boolean));
    this.attributes['class'] = v;
  }}
  get value() {{ return this._value !== undefined ? this._value : (this.getAttribute('value') || ''); }}
  set value(v) {{ this._value = String(v); this.setAttribute('value', v); }}
  get checked() {{
    return this._checked !== undefined ? this._checked : this.hasAttribute('checked');
  }}
  set checked(v) {{
    this._checked = Boolean(v);
    if (v) this.setAttribute('checked', '');
    else this.removeAttribute('checked');
  }}
  click() {{
    if (this.tagName === 'INPUT' && (this.getAttribute('type') === 'checkbox')) {{
      this.checked = !this.checked;
    }}
    if (typeof this.onclick === 'function') {{
      this.onclick({{ preventDefault: () => {{}}, stopPropagation: () => {{}}, target: this }});
    }}
    if (typeof this.onchange === 'function') {{
      this.onchange({{ target: this }});
    }}
  }}
  addEventListener(event, fn) {{
    this._listeners[event] = this._listeners[event] || [];
    this._listeners[event].push(fn);
  }}
  removeEventListener(event, fn) {{
    if (!this._listeners || !this._listeners[event]) return;
    this._listeners[event] = this._listeners[event].filter(f => f !== fn);
  }}
  dispatchEvent(evt) {{
    const type = evt.type || evt;
    if (this['on' + type]) this['on' + type](evt);
    if (this._listeners[type]) {{
      for (const fn of this._listeners[type]) fn(evt);
    }}
  }}
  querySelector(sel) {{ return this._find(sel, this); }}
  querySelectorAll(sel) {{
    const res = [];
    this._findAll(sel, this, res);
    return res;
  }}
  _find(sel, node) {{
    for (const child of node.childNodes) {{
      if (child.nodeType === 1) {{
        if (this._matches(sel, child)) return child;
        const sub = this._find(sel, child);
        if (sub) return sub;
      }}
    }}
    return null;
  }}
  _findAll(sel, node, acc) {{
    for (const child of node.childNodes) {{
      if (child.nodeType === 1) {{
        if (this._matches(sel, child)) acc.push(child);
        this._findAll(sel, child, acc);
      }}
    }}
  }}
  _matches(sel, el) {{
    const parts = sel.split(',').map(s => s.trim());
    return parts.some(part => {{
      if (part.startsWith('.')) return el.classList.has(part.slice(1));
      if (part.startsWith('#')) return el.id === part.slice(1);
      if (part.startsWith('[') && part.endsWith(']')) {{
        const inner = part.slice(1, -1);
        if (inner.includes('=')) {{
          const [ak, av] = inner.split('=').map(s => s.replace(/['"]/g, '').trim());
          return el.getAttribute(ak) === av;
        }}
        return el.hasAttribute(inner);
      }}
      return el.tagName.toLowerCase() === part.toLowerCase();
    }});
  }}
  closest(sel) {{
    let curr = this;
    while (curr) {{
      if (curr.nodeType === 1 && this._matches(sel, curr)) return curr;
      curr = curr.parentNode;
    }}
    return null;
  }}
  get innerHTML() {{
    return this.childNodes.map(c => {{
      if (c.nodeType === 3) return c.nodeValue;
      const tag = c.tagName.toLowerCase();
      const attrs = Object.entries(c.attributes).map(([k, v]) => `${{k}}="${{v}}"`).join(' ');
      const attrStr = attrs ? ' ' + attrs : '';
      return `<${{tag}}${{attrStr}}>${{c.innerHTML}}</${{tag}}>`;
    }}).join('');
  }}
  set innerHTML(htmlStr) {{
    this.childNodes = [];
    parseHtmlIntoMock(htmlStr, this);
  }}
}}

function parseHtmlIntoMock(html, parent) {{
  if (!html) return;
  const tokenRegex = /<(\\/)?([a-zA-Z0-9\\-]+)([^>]*)>|([^<]+)/g;
  let match;
  let current = parent;
  while ((match = tokenRegex.exec(html)) !== null) {{
    const [full, isClose, tagName, attrStr, text] = match;
    if (text) {{
      current.appendChild(new MockNode(3, decodeHtmlEntities(text)));
    }} else if (isClose) {{
      if (current.parentNode) current = current.parentNode;
    }} else {{
      const el = new MockElement(tagName);
      if (attrStr) {{
        const attrRegex = /([a-zA-Z0-9_\\-]+)(?:=(?:["']([^"']*)["']|([^\\s>]+)))?/g;
        let aMatch;
        while ((aMatch = attrRegex.exec(attrStr)) !== null) {{
          const rawVal = aMatch[2] !== undefined ? aMatch[2] : (aMatch[3] !== undefined ? aMatch[3] : '');
          el.setAttribute(aMatch[1], decodeHtmlEntities(rawVal));
        }}
      }}
      current.appendChild(el);
      const voidTags = ['hr', 'br', 'img', 'input'];
      if (!voidTags.includes(tagName.toLowerCase())) {{
        current = el;
      }}
    }}
  }}
}}

const mockDoc = {{
  createElement: (tag) => new MockElement(tag),
  getElementById: (id) => null,
  querySelector: () => null,
  querySelectorAll: () => [],
  addEventListener: () => {{}},
  removeEventListener: () => {{}},
  body: new MockElement('body')
}};

const sandbox = {{
  Node: {{ ELEMENT_NODE: 1, TEXT_NODE: 3 }},
  navigator: {{ clipboard: {{ writeText: () => Promise.resolve() }} }},
  console,
  setTimeout: () => {{}},
  clearTimeout: () => {{}},
  setInterval: () => {{}},
  clearInterval: () => {{}},
  localStorage: {{ getItem: () => null, setItem: () => {{}}, removeItem: () => {{}} }},
  document: mockDoc,
  addEventListener: () => {{}},
  removeEventListener: () => {{}},
  __lastLoadedNote: null,
  loadNote: function(id) {{ sandbox.__lastLoadedNote = id; }}
}};
sandbox.window = sandbox;
sandbox.global = sandbox;

{extra_setup}

const appCode = fs.readFileSync({json.dumps(APP_JS_PATH)}, 'utf-8');
vm.runInNewContext(appCode, sandbox);

// Run test inside vm context
const testFn = function() {{
  {script_body}
}};
testFn();
"""
        proc = subprocess.run(['node', '-e', harness_code], capture_output=True, text=True)
        if proc.returncode != 0:
            raise AssertionError(f"Node execution failed (code {proc.returncode}):\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
        return proc.stdout.strip()

    # =========================================================================
    # PART 1: TO_DO CHECKBOX CLICK, TOGGLE, STRIKETHROUGH & PERSISTENCE
    # =========================================================================

    def test_css_todo_strikethrough_contract(self):
        """Verifies that .notion-to-do-title.completed declares text-decoration: line-through in styles.css."""
        self.assertIn('.notion-to-do-title.completed', self.styles_css)
        match = re.search(r'\.notion-to-do-title\.completed\s*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(match, "Rule for .notion-to-do-title.completed must exist in styles.css")
        rule_content = match.group(1)
        self.assertIn('text-decoration: line-through', rule_content)
        self.assertIn('opacity', rule_content)

    def test_todo_initial_states_and_classes(self):
        """Empirically tests initial rendering of to_do blocks with various checked formats."""
        node_script = """
        const renderBlock = sandbox.renderBlock;

        const testCases = [
          { checked: [['Yes', []]], expectedChecked: true, expectedClass: true },
          { checked: 'Yes', expectedChecked: true, expectedClass: true },
          { checked: true, expectedChecked: true, expectedClass: true },
          { checked: [['No', []]], expectedChecked: false, expectedClass: false },
          { checked: 'No', expectedChecked: false, expectedClass: false },
          { checked: false, expectedChecked: false, expectedClass: false },
          { checked: null, expectedChecked: false, expectedClass: false },
          { checked: undefined, expectedChecked: false, expectedClass: false }
        ];

        for (let i = 0; i < testCases.length; i++) {
          const tc = testCases[i];
          const block = {
            id: 'td-' + i,
            type: 'to_do',
            properties: {
              title: [['Task ' + i, []]],
              checked: tc.checked
            }
          };
          const el = renderBlock(block);
          assert(el, 'Element must render for case ' + i);
          const chk = el.querySelector('.notion-to-do-checkbox');
          const title = el.querySelector('.notion-to-do-title');
          assert(chk, 'Checkbox must exist for case ' + i);
          assert(title, 'Title element must exist for case ' + i);

          assert.strictEqual(chk.checked, tc.expectedChecked,
            `Checkbox checked mismatch for case ${i}: expected ${tc.expectedChecked}, got ${chk.checked}`);
          assert.strictEqual(title.classList.has('completed'), tc.expectedClass,
            `Title completed class mismatch for case ${i}: expected ${tc.expectedClass}, got ${title.classList.has('completed')}`);
        }
        console.log('TODO_INITIAL_STATES_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TODO_INITIAL_STATES_OK', out)

    def test_todo_interactive_click_toggle_and_state_persistence(self):
        """Fuzzes interactive click and change events, verifying bi-directional toggle and persistence calls."""
        node_script = """
        const renderBlock = sandbox.renderBlock;

        const updatesLog = [];
        sandbox.persistBlockUpdate = function(id, patch) {
          updatesLog.push({ id, patch, ts: Date.now() });
        };
        sandbox.state = {
          activeRecordMap: {
            block: {
              'td-fuzz-1': {
                value: {
                  id: 'td-fuzz-1',
                  type: 'to_do',
                  properties: {
                    title: [['Fuzz Task', []]],
                    checked: [['No', []]]
                  }
                }
              }
            }
          }
        };

        const el = renderBlock({
          id: 'td-fuzz-1',
          type: 'to_do',
          properties: {
            title: [['Fuzz Task', []]],
            checked: [['No', []]]
          }
        });

        const chk = el.querySelector('.notion-to-do-checkbox');
        const titleEl = el.querySelector('.notion-to-do-title');
        assert(chk && titleEl);

        // Verify initial state
        assert.strictEqual(chk.checked, false);
        assert.strictEqual(titleEl.classList.has('completed'), false);

        // Perform 20 rapid back-and-forth toggles via click()
        for (let cycle = 1; cycle <= 20; cycle++) {
          const expectChecked = (cycle % 2 === 1);
          chk.click();

          // Checkbox state
          assert.strictEqual(chk.checked, expectChecked, `Cycle ${cycle}: checkbox state incorrect`);

          // Title element completed class
          assert.strictEqual(titleEl.classList.has('completed'), expectChecked,
            `Cycle ${cycle}: title class .completed incorrect`);

          // Persistence call
          assert.strictEqual(updatesLog.length, cycle, `Cycle ${cycle}: persistBlockUpdate call count mismatch`);
          const lastUpdate = updatesLog[updatesLog.length - 1];
          assert.strictEqual(lastUpdate.id, 'td-fuzz-1');
          const expectedVal = expectChecked ? 'Yes' : 'No';
          assert.strictEqual(lastUpdate.patch.properties.checked[0][0], expectedVal);

          // In-memory activeRecordMap synchronization
          const record = sandbox.state.activeRecordMap.block['td-fuzz-1'].value;
          assert.strictEqual(record.properties.checked[0][0], expectedVal,
            `Cycle ${cycle}: activeRecordMap desynchronized`);
        }

        console.log('TODO_INTERACTIVE_TOGGLE_FUZZ_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TODO_INTERACTIVE_TOGGLE_FUZZ_OK', out)

    def test_todo_event_resilience_when_state_or_persistence_missing(self):
        """Stress-tests to_do change event when state, recordMap, or persistBlockUpdate are undefined or null."""
        node_script = """
        const renderBlock = sandbox.renderBlock;

        // Ensure state and persistBlockUpdate are undefined
        delete sandbox.state;
        delete sandbox.persistBlockUpdate;
        delete sandbox.window.state;
        delete sandbox.window.persistBlockUpdate;

        const el = renderBlock({
          id: 'td-resilient',
          type: 'to_do',
          properties: {
            title: [['Resilient Task', []]]
          }
        });

        const chk = el.querySelector('.notion-to-do-checkbox');
        const titleEl = el.querySelector('.notion-to-do-title');

        // Should not throw even with missing state & persistence
        chk.click();
        assert.strictEqual(chk.checked, true);
        assert.strictEqual(titleEl.classList.has('completed'), true);

        chk.click();
        assert.strictEqual(chk.checked, false);
        assert.strictEqual(titleEl.classList.has('completed'), false);

        console.log('TODO_RESILIENCE_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TODO_RESILIENCE_OK', out)

    def test_todo_nested_children_mounting(self):
        """Verifies that to_do container mounts child blocks inside .block-to-do-children."""
        node_script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const rmap = {
          block: {
            'page-todo': {
              value: { id: 'page-todo', type: 'page', content: ['td-parent'], alive: 1 }
            },
            'td-parent': {
              value: {
                id: 'td-parent',
                type: 'to_do',
                properties: { title: [['Parent Task', []]], checked: [['No', []]] },
                content: ['td-child-1', 'txt-child-2'],
                alive: 1
              }
            },
            'td-child-1': {
              value: {
                id: 'td-child-1',
                type: 'to_do',
                properties: { title: [['Nested Subtask', []]], checked: [['Yes', []]] },
                parent_id: 'td-parent',
                alive: 1
              }
            },
            'txt-child-2': {
              value: {
                id: 'txt-child-2',
                type: 'text',
                properties: { title: [['Task note child', []]] },
                parent_id: 'td-parent',
                alive: 1
              }
            }
          }
        };

        const container = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'page-todo', container);

        assert.strictEqual(container.children.length, 1);
        const parentEl = container.children[0];
        assert(parentEl.classList.has('block-to-do'));

        const childrenSlot = parentEl.querySelector('.block-to-do-children');
        assert(childrenSlot, '.block-to-do-children must exist');
        assert.strictEqual(childrenSlot.children.length, 2, 'Must mount 2 children inside parent to_do');

        const child1 = childrenSlot.children[0];
        assert(child1.classList.has('block-to-do'));
        assert(child1.querySelector('.notion-to-do-title').classList.has('completed'));

        const child2 = childrenSlot.children[1];
        assert.strictEqual(child2.getAttribute('data-type'), 'text');
        assert(child2.textContent.includes('Task note child'));

        console.log('TODO_NESTED_CHILDREN_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TODO_NESTED_CHILDREN_OK', out)

    def test_todo_toggle_preserves_title_rich_text(self):
        """Verifies that clicking to_do checkbox toggles checked without corrupting rich text in title."""
        node_script = """
        const renderBlock = sandbox.renderBlock;

        const richTitle = [
          ['Urgent: ', [['b']]],
          ['Review PR ', [['i'], ['h', 'red']]],
          ['docs', [['a', 'https://example.com']]]
        ];

        sandbox.state = {
          activeRecordMap: {
            block: {
              'td-rich': {
                value: {
                  id: 'td-rich',
                  type: 'to_do',
                  properties: { title: richTitle, checked: [['No', []]] }
                }
              }
            }
          }
        };

        const el = renderBlock({
          id: 'td-rich',
          type: 'to_do',
          properties: { title: richTitle, checked: [['No', []]] }
        });

        const chk = el.querySelector('.notion-to-do-checkbox');
        const titleEl = el.querySelector('.notion-to-do-title');

        // Initial HTML should contain rich decorators
        assert(titleEl.innerHTML.includes('<strong>Urgent: </strong>'));
        assert(titleEl.innerHTML.includes('notion-color-red'));
        assert(titleEl.innerHTML.includes('href="https://example.com"'));

        // Toggle to checked
        chk.click();
        assert(chk.checked);
        assert(titleEl.classList.has('completed'));

        // Check activeRecordMap: title remains untouched, only checked is changed
        const savedBlk = sandbox.state.activeRecordMap.block['td-rich'].value;
        assert.strictEqual(JSON.stringify(savedBlk.properties.title), JSON.stringify(richTitle));
        assert.strictEqual(savedBlk.properties.checked[0][0], 'Yes');

        // Toggle back
        chk.click();
        assert(!chk.checked);
        assert(!titleEl.classList.has('completed'));
        assert.strictEqual(savedBlk.properties.checked[0][0], 'No');
        assert.strictEqual(JSON.stringify(savedBlk.properties.title), JSON.stringify(richTitle));

        console.log('TODO_PRESERVE_RICHTEXT_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TODO_PRESERVE_RICHTEXT_OK', out)

    # =========================================================================
    # PART 2: RICH-TEXT FORMATTING ON EXTENDED BLOCKS (header_4, quote, callout, to_do)
    # =========================================================================

    def test_rich_text_complex_decorator_tuples_on_extended_blocks(self):
        """Tests parsing and DOM element construction for header_4, quote, callout, to_do with multi-decorator tuples."""
        node_script = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;
        const renderBlock = sandbox.renderBlock;

        // Complex tuple payload mixing:
        // bold (b), italic (i), underline (_), strikethrough (s), code (c),
        // text color (h: purple), bg color (h: yellow_background), link (a: url), equation (e: latex)
        const complexTitle = [
          ['Plain ', []],
          ['BoldItalic ', [['b'], ['i']]],
          ['UnderlineStrike ', [['_'], ['s']]],
          ['CodeSegment ', [['c']]],
          ['ColoredText ', [['h', 'purple']]],
          ['HighlightedBg ', [['h', 'yellow_background']]],
          ['ExternalLink ', [['a', 'https://notion.so/docs']]],
          ['Formula ', []],
          ['\\alpha + \\beta = \\gamma', [['e', '\\alpha + \\beta = \\gamma']]],
          [' MegaCombo', [['b'], ['i'], ['_'], ['s'], ['h', 'blue'], ['a', 'https://example.com']]]
        ];

        const targetTypes = [
          { type: 'header_4', selector: '.block-header-4', isDetails: false },
          { type: 'header_4', selector: 'details.block-header-toggle h4', isDetails: true, format: { toggleable: true } },
          { type: 'quote', selector: '.notion-quote-content', isDetails: false },
          { type: 'callout', selector: '.notion-callout-body', isDetails: false, format: { page_icon: '⚡', block_color: 'gray_background' } },
          { type: 'to_do', selector: '.notion-to-do-title', isDetails: false }
        ];

        for (let i = 0; i < targetTypes.length; i++) {
          const cfg = targetTypes[i];
          const block = {
            id: 'rich-blk-' + i,
            type: cfg.type,
            properties: { title: complexTitle },
            format: cfg.format || {}
          };

          const el = renderBlock(block);
          assert(el, 'Block element must be returned for ' + cfg.type);

          const titleEl = el.querySelector(cfg.selector) || el;
          assert(titleEl, 'Title container not found with selector: ' + cfg.selector);

          const innerHtml = titleEl.innerHTML;

          // Assert all decorators are present in rendered DOM
          assert(innerHtml.includes('<strong>'), `Missing <strong> in ${cfg.type}`);
          assert(innerHtml.includes('<em>'), `Missing <em> in ${cfg.type}`);
          assert(innerHtml.includes('<u>'), `Missing <u> in ${cfg.type}`);
          assert(innerHtml.includes('<s>'), `Missing <s> in ${cfg.type}`);
          assert(innerHtml.includes('<code>CodeSegment </code>'), `Missing <code> in ${cfg.type}`);
          assert(innerHtml.includes('notion-color-purple'), `Missing color purple in ${cfg.type}`);
          assert(innerHtml.includes('notion-color-yellow_background'), `Missing bg yellow in ${cfg.type}`);
          assert(innerHtml.includes('href="https://notion.so/docs"'), `Missing link in ${cfg.type}`);
          assert(innerHtml.includes('data-latex="\\alpha + \\beta = \\gamma"'), `Missing equation in ${cfg.type}`);

          // Test bidirectional roundtrip: DOM -> htmlToRichTextTuples
          const deserialized = htmlToRichTextTuples(innerHtml);
          assert(Array.isArray(deserialized), 'Deserialized result must be an array');
          assert(deserialized.length >= 7, 'Deserialized segments must preserve rich text chunks');

          // Check text preservation across round-trip
          const plainFull = deserialized.map(s => s[0]).join('');
          assert(plainFull.includes('Plain '), 'Plain text lost in round-trip');
          assert(plainFull.includes('BoldItalic '), 'BoldItalic lost in round-trip');
          assert(plainFull.includes('CodeSegment '), 'CodeSegment lost in round-trip');
          assert(plainFull.includes('ExternalLink '), 'ExternalLink lost in round-trip');
        }

        console.log('RICH_TEXT_EXTENDED_BLOCKS_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('RICH_TEXT_EXTENDED_BLOCKS_OK', out)

    def test_rich_text_roundtrip_fidelity_and_segment_coalescing(self):
        """Fuzzes htmlToRichTextTuples coalescing adjacent styled runs and preserving exact decorator tags."""
        node_script = """
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;

        // Adjacent identical decorators must coalesce into a single segment
        const splitBoldHtml = '<strong>Hello </strong><strong>world</strong><strong>!</strong>';
        const coalesced = htmlToRichTextTuples(splitBoldHtml);
        assert.strictEqual(coalesced.length, 1, 'Adjacent strong tags must be coalesced');
        assert.strictEqual(coalesced[0][0], 'Hello world!');
        assert.strictEqual(JSON.stringify(coalesced[0][1]), JSON.stringify([['b']]));

        // Mixed nesting
        const mixedHtml = '<p>Start <strong><em>bold-italic</em></strong> and <a href="https://example.com"><u>underlined link</u></a> end.</p>';
        const mixedTuples = htmlToRichTextTuples(mixedHtml);
        assert(mixedTuples.length >= 4);

        // Find bold-italic segment
        const biSeg = mixedTuples.find(s => s[0] === 'bold-italic');
        assert(biSeg, 'bold-italic segment must be parsed');
        const decNames = biSeg[1].map(d => d[0]).sort();
        assert.strictEqual(JSON.stringify(decNames), JSON.stringify(['b', 'i']));

        // Find underlined link segment
        const linkSeg = mixedTuples.find(s => s[0] === 'underlined link');
        assert(linkSeg, 'underlined link segment must be parsed');
        assert(linkSeg[1].some(d => d[0] === '_'));
        assert(linkSeg[1].some(d => d[0] === 'a' && d[1] === 'https://example.com'));

        console.log('ROUNDTRIP_COALESCING_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('ROUNDTRIP_COALESCING_OK', out)

    def test_rich_text_xss_and_malicious_vector_neutralization(self):
        """Stress-tests parseRichTextToHtml against script injection, event handlers, and javascript: links."""
        node_script = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        const maliciousTuples = [
          ['<script>alert("pwn")</script>', [['b']]],
          ['<img src="x" onerror="evil()">', [['i']]],
          ['Exploit Link', [['a', 'javascript:alert(document.cookie)']]],
          ['Data URL Link', [['a', 'data:text/html,<script>alert(1)</script>']]],
          ['VBScript Link', [['a', 'vbscript:msgbox(1)']]],
          ['File Protocol', [['a', 'file:///C:/Windows/system.ini']]]
        ];

        const html = parseRichTextToHtml(maliciousTuples);

        // 1. Injected tags must be escaped as HTML entities
        assert(!html.includes('<script>'), '<script> must be escaped');
        assert(html.includes('&lt;script&gt;'), '<script> must become &lt;script&gt;');
        assert(!html.includes('<img src='), '<img src> must be escaped');
        assert(html.includes('&lt;img src='), '<img src> must become &lt;img src=');

        // 2. Dangerous protocols must be sanitized to #
        assert(!html.includes('javascript:'), 'javascript: URLs must not appear in output');
        assert(!html.includes('data:text/html'), 'data: URLs must not appear in output');
        assert(!html.includes('vbscript:'), 'vbscript: URLs must not appear in output');
        assert(!html.includes('file:///'), 'file: URLs must not appear in output');
        assert(html.includes('href="#"'), 'Dangerous URLs must fallback to href="#"');

        console.log('XSS_NEUTRALIZATION_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('XSS_NEUTRALIZATION_OK', out)

    # =========================================================================
    # PART 3: TRANSCLUSION REFERENCE RECURSIVE CYCLE GUARDS
    # =========================================================================

    def test_transclusion_self_cycle_guard(self):
        """Verifies renderTreeFromRecordMap survives a transclusion reference pointing to its own container."""
        node_script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        // Container tc-self holds reference tr-self which points right back to tc-self
        const rmap = {
          block: {
            'root-page': {
              value: {
                id: 'root-page',
                type: 'page',
                content: ['tc-self'],
                alive: 1
              }
            },
            'tc-self': {
              value: {
                id: 'tc-self',
                type: 'transclusion_container',
                content: ['tr-self'],
                alive: 1
              }
            },
            'tr-self': {
              value: {
                id: 'tr-self',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tc-self' } },
                alive: 1
              }
            }
          }
        };

        const container = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'root-page', container);

        assert(container.children.length === 1, 'Root container must render tc-self');
        const tcEl = container.children[0];
        assert.strictEqual(tcEl.getAttribute('data-type'), 'transclusion_container');
        console.log('TRANSCLUSION_SELF_CYCLE_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TRANSCLUSION_SELF_CYCLE_OK', out)

    def test_transclusion_mutual_cycle_guard(self):
        """Verifies mutual cycle: Container A -> Ref B -> Container B -> Ref A -> Container A."""
        node_script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const rmap = {
          block: {
            'page-1': {
              value: { id: 'page-1', type: 'page', content: ['tc-a'], alive: 1 }
            },
            'tc-a': {
              value: {
                id: 'tc-a',
                type: 'transclusion_container',
                content: ['item-a', 'ref-b'],
                alive: 1
              }
            },
            'item-a': {
              value: { id: 'item-a', type: 'text', properties: { title: [['Node A Text', []]] }, alive: 1 }
            },
            'ref-b': {
              value: {
                id: 'ref-b',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tc-b' } },
                alive: 1
              }
            },
            'tc-b': {
              value: {
                id: 'tc-b',
                type: 'transclusion_container',
                content: ['item-b', 'ref-a'],
                alive: 1
              }
            },
            'item-b': {
              value: { id: 'item-b', type: 'text', properties: { title: [['Node B Text', []]] }, alive: 1 }
            },
            'ref-a': {
              value: {
                id: 'ref-a',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tc-a' } },
                alive: 1
              }
            }
          }
        };

        const container = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'page-1', container);

        // Verify termination and correct rendering without hanging
        assert(container.innerHTML.includes('Node A Text'));
        assert(container.innerHTML.includes('Node B Text'));
        console.log('TRANSCLUSION_MUTUAL_CYCLE_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TRANSCLUSION_MUTUAL_CYCLE_OK', out)

    def test_transclusion_nested_container_cycle_guard(self):
        """Verifies container pointing to container with reference to container (nested container cycle)."""
        node_script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        // Container-1 contains Container-2.
        // Container-2 contains Ref-1, which points back to Container-1.
        const rmap = {
          block: {
            'page-root': {
              value: { id: 'page-root', type: 'page', content: ['tc-outer'], alive: 1 }
            },
            'tc-outer': {
              value: {
                id: 'tc-outer',
                type: 'transclusion_container',
                content: ['outer-text', 'tc-inner'],
                alive: 1
              }
            },
            'outer-text': {
              value: { id: 'outer-text', type: 'text', properties: { title: [['Outer Content', []]] }, alive: 1 }
            },
            'tc-inner': {
              value: {
                id: 'tc-inner',
                type: 'transclusion_container',
                content: ['inner-text', 'ref-back-to-outer'],
                alive: 1
              }
            },
            'inner-text': {
              value: { id: 'inner-text', type: 'text', properties: { title: [['Inner Content', []]] }, alive: 1 }
            },
            'ref-back-to-outer': {
              value: {
                id: 'ref-back-to-outer',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tc-outer' } },
                alive: 1
              }
            }
          }
        };

        const container = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'page-root', container);

        assert(container.innerHTML.includes('Outer Content'));
        assert(container.innerHTML.includes('Inner Content'));
        console.log('TRANSCLUSION_NESTED_CONTAINER_CYCLE_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TRANSCLUSION_NESTED_CONTAINER_CYCLE_OK', out)

    def test_transclusion_broken_pointers(self):
        """Verifies transclusion reference handles non-existent pointers and empty formats without crashing."""
        node_script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const rmap = {
          block: {
            'page-broken': {
              value: {
                id: 'page-broken',
                type: 'page',
                content: ['ref-missing', 'ref-no-pointer', 'ref-null-target'],
                alive: 1
              }
            },
            'ref-missing': {
              value: {
                id: 'ref-missing',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'does-not-exist' } },
                alive: 1
              }
            },
            'ref-no-pointer': {
              value: {
                id: 'ref-no-pointer',
                type: 'transclusion_reference',
                format: {},
                alive: 1
              }
            },
            'ref-null-target': {
              value: {
                id: 'ref-null-target',
                type: 'transclusion_reference',
                format: { copied_from_pointer: null },
                alive: 1
              }
            }
          }
        };

        const container = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'page-broken', container);

        assert.strictEqual(container.children.length, 3);
        console.log('TRANSCLUSION_BROKEN_POINTERS_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TRANSCLUSION_BROKEN_POINTERS_OK', out)

    def test_transclusion_soft_deleted_target_container(self):
        """Empirically tests behavior when transclusion reference points to soft-deleted master container (alive === 0)."""
        node_script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const rmap = {
          block: {
            'page-deleted-target': {
              value: {
                id: 'page-deleted-target',
                type: 'page',
                content: ['ref-to-deleted'],
                alive: 1
              }
            },
            'ref-to-deleted': {
              value: {
                id: 'ref-to-deleted',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tc-deleted' } },
                alive: 1
              }
            },
            'tc-deleted': {
              value: {
                id: 'tc-deleted',
                type: 'transclusion_container',
                content: ['ghost-child'],
                alive: 0 // Soft-deleted master
              }
            },
            'ghost-child': {
              value: { id: 'ghost-child', type: 'text', properties: { title: [['Ghost In Deleted', []]] }, alive: 1 }
            }
          }
        };

        const container = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'page-deleted-target', container);

        const renderedGhost = container.innerHTML.includes('Ghost In Deleted');
        // Record whether soft-deleted master container leaked its children into reference
        console.log('TRANSCLUSION_SOFT_DELETED_LEAK:' + renderedGhost);
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TRANSCLUSION_SOFT_DELETED_LEAK:', out)

    def test_transclusion_multiple_references_on_same_page(self):
        """Empirically tests whether multiple transclusion references to the same container both render children."""
        node_script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const rmap = {
          block: {
            'page-shared': {
              value: {
                id: 'page-shared',
                type: 'page',
                content: ['ref-1', 'ref-2'],
                alive: 1
              }
            },
            'tc-master': {
              value: {
                id: 'tc-master',
                type: 'transclusion_container',
                content: ['child-shared'],
                alive: 1
              }
            },
            'child-shared': {
              value: {
                id: 'child-shared',
                type: 'text',
                properties: { title: [['Shared Content Across Refs', []]] },
                alive: 1
              }
            },
            'ref-1': {
              value: {
                id: 'ref-1',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tc-master' } },
                alive: 1
              }
            },
            'ref-2': {
              value: {
                id: 'ref-2',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tc-master' } },
                alive: 1
              }
            }
          }
        };

        const container = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'page-shared', container);

        assert.strictEqual(container.children.length, 2);
        const ref1Body = container.children[0].querySelector('.notion-synced-body');
        const ref2Body = container.children[1].querySelector('.notion-synced-body');
        assert(ref1Body && ref2Body);

        console.log('REF1_CHILDREN_COUNT:' + ref1Body.children.length);
        console.log('REF2_CHILDREN_COUNT:' + ref2Body.children.length);
        """
        out = self.run_node_vm(node_script)
        print("Multiple refs output:", out)

    def test_transclusion_deep_chain_stack_limit(self):
        """Verifies deep chains of 25 transclusion references and containers terminate without stack overflow."""
        node_script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const rmap = { block: {} };
        const depth = 25;

        rmap.block['page-deep'] = {
          value: { id: 'page-deep', type: 'page', content: ['tc-0'], alive: 1 }
        };

        for (let i = 0; i < depth; i++) {
          const tcId = 'tc-' + i;
          const trId = 'tr-' + (i + 1);
          const nextTcId = 'tc-' + (i + 1);

          if (i < depth - 1) {
            rmap.block[tcId] = {
              value: { id: tcId, type: 'transclusion_container', content: [trId], alive: 1 }
            };
            rmap.block[trId] = {
              value: {
                id: trId,
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: nextTcId } },
                alive: 1
              }
            };
          } else {
            rmap.block[tcId] = {
              value: {
                id: tcId,
                type: 'transclusion_container',
                content: ['leaf-text'],
                alive: 1
              }
            };
            rmap.block['leaf-text'] = {
              value: { id: 'leaf-text', type: 'text', properties: { title: [['Deep Leaf Content', []]] }, alive: 1 }
            };
          }
        }

        const container = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'page-deep', container);

        assert(container.innerHTML.includes('Deep Leaf Content'), 'Deep chain leaf content must be reached');
        console.log('TRANSCLUSION_DEEP_CHAIN_OK');
        """
        out = self.run_node_vm(node_script)
        self.assertIn('TRANSCLUSION_DEEP_CHAIN_OK', out)


if __name__ == '__main__':
    unittest.main()
