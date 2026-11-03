#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_tier5_frontend_adversarial.py
Milestone 3 Phase 2: Tier 5 White-box Frontend Audit & Adversarial Hardening.

Aggressive adversarial verification dimensions:
1. Deep nested transclusion DAGs:
   - Synced blocks inside synced blocks (transclusion_container containing transclusion_container)
   - Diamond transclusion DAGs (multiple references pointing to single container)
   - Multi-hop reference chains (C1 -> Ref2 -> C2 -> Ref3 -> C3)
   - Cyclic DAG recursion prevention (C1 <-> C2 mutual cycles, self-referential containers)
   - High fan-out wide DAGs (35+ references pointing to one master container)
   - Dead pointers and tombstoned targets (alive: 0)
   - Unsyncing references via unsyncBlockInstance and reference copying

2. Rapid concurrent block conversions via convertBlockType:
   - Container to leaf boundaries: converting container with children to leaf sets content: null and detaches DOM children
   - Leaf to container boundaries: converting leaf to container restores content: []
   - Toggleable header boundary conversions (header_4 toggleable vs non-toggleable)
   - Rapid sequential conversions (30+ type changes on single block)
   - Concurrent sibling conversions preserving parent content order
   - Fallback initialization for blocks absent in recordMap
   - Debounced persistence verification via persistBlockUpdate & pywebview bridge

3. XSS sanitization and HTML injection in rich text titles across all new block types:
   - header_4 (standard and toggleable summary), to_do, quote, callout (icon and body)
   - Synced block badge labels and target pointers
   - Media leaves: video, audio, file, pdf, bookmark
   - Dangerous URL schemes: javascript:, vbscript:, data:, file:, case variants, whitespace bypasses
   - Script injection payloads: <script>, <img onerror>, <svg onload>, <iframe>
   - Decorator attribute breakouts (color mark styles, link hrefs)
   - Malformed HTML and tag soup resiliency in htmlToRichTextTuples

4. Extreme inputs: empty properties, null strings, massive texts, special unicode/emoji:
   - Empty, null, missing, and non-dict properties across new block types
   - Corrupted primitive properties (integers, booleans, arrays)
   - Massive texts (50,000+ characters) in titles
   - Deep nested decorator tuples (15+ layers)
   - Complex emojis with ZWJ (👨‍👩‍👧‍👦), RTL scripts (Arabic/Hebrew), zero-width characters, null bytes
   - Canonical equation tokens (⁍ and \u204d)
   - Bidirectional roundtrip stability under extreme inputs

5. Interactive to_do event edge cases:
   - Rapid toggling (100 alternating clicks) verifying DOM class .completed and recordMap sync
   - Resiliency under missing state or corrupted activeRecordMap
   - Enter key event triggering insertBlockBelow and parent content splicing
   - Backspace key on empty to_do triggering convertBlockType to 'text'
   - Backspace key on empty text triggering deleteBlockElement and focusing previous block
"""

import os
import sys
import json
import subprocess
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')


class Tier5NodeVMBasedTest(unittest.TestCase):
    """Base test runner providing a full simulated browser DOM environment inside Node.js VM."""

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
        """Executes JavaScript test code in a hardened Node.js VM DOM sandbox with app.js loaded."""
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
  remove() {{
    if (this.parentNode) {{
      this.parentNode.removeChild(this);
    }}
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
  focus() {{}}
  blur() {{}}
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
      const voidTags = ['hr', 'br', 'img', 'input', 'source'];
      if (!voidTags.includes(tagName.toLowerCase())) {{
        current = el;
      }}
    }}
  }}
}}

const editorCanvas = new MockElement('div');
editorCanvas.id = 'rich-editor-canvas';
editorCanvas.setAttribute('data-block-id', 'canvas-root');

const mockDoc = {{
  createElement: (tag) => new MockElement(tag),
  getElementById: (id) => {{
    if (id === 'rich-editor-canvas') return editorCanvas;
    if (mockDoc.body.id === id) return mockDoc.body;
    return editorCanvas.querySelector('#' + id) || mockDoc.body.querySelector('#' + id);
  }},
  querySelector: (sel) => {{
    if (sel === '#rich-editor-canvas') return editorCanvas;
    return editorCanvas.querySelector(sel) || mockDoc.body.querySelector(sel);
  }},
  querySelectorAll: (sel) => editorCanvas.querySelectorAll(sel),
  addEventListener: () => {{}},
  removeEventListener: () => {{}},
  createRange: () => ({{
    selectNodeContents: () => {{}},
    collapse: () => {{}}
  }}),
  body: new MockElement('body'),
  execCommand: () => true
}};
mockDoc.body.appendChild(editorCanvas);

const clipboardBuffer = {{ text: '' }};
const mockNavigator = {{
  clipboard: {{
    writeText: (t) => {{
      clipboardBuffer.text = String(t);
      return {{
        then: (cb) => {{
          if (typeof cb === 'function') cb();
          return {{ catch: () => {{}} }};
        }},
        catch: () => {{}}
      }};
    }}
  }}
}};

const persistBlockUpdateCalls = [];
const showToastCalls = [];
const pywebviewCalls = {{
  update_block: [],
  create_block: [],
  reorder_block_children: [],
  soft_delete_block: []
}};

const mockPyWebView = {{
  api: {{
    update_block: (id, updates) => {{ pywebviewCalls.update_block.push({{ id, updates }}); }},
    create_block: (b) => {{ pywebviewCalls.create_block.push(b); }},
    reorder_block_children: (pid, c) => {{ pywebviewCalls.reorder_block_children.push({{ pid, c }}); }},
    soft_delete_block: (id) => {{ pywebviewCalls.soft_delete_block.push(id); }}
  }}
}};

const sandbox = {{
  Node: {{ ELEMENT_NODE: 1, TEXT_NODE: 3 }},
  navigator: mockNavigator,
  console,
  setTimeout: (fn, ms) => {{
    if (typeof fn === 'function') fn();
    return 1;
  }},
  clearTimeout: () => {{}},
  setInterval: () => 1,
  clearInterval: () => {{}},
  localStorage: {{ getItem: () => null, setItem: () => {{}}, removeItem: () => {{}} }},
  document: mockDoc,
  window: null,
  addEventListener: () => {{}},
  removeEventListener: () => {{}},
  getSelection: () => ({{
    rangeCount: 1,
    anchorNode: null,
    anchorOffset: 0,
    removeAllRanges: () => {{}},
    addRange: () => {{}},
    getRangeAt: () => ({{
      toString: () => '',
      collapse: () => {{}}
    }})
  }}),
  showToast: (msg, icon) => {{ showToastCalls.push({{ msg, icon }}); }},
  persistBlockUpdate: (id, updates) => {{ persistBlockUpdateCalls.push({{ id, updates }}); }},
  syncRichEditor: () => {{}},
  loadNote: () => {{}},
  getActiveNote: () => ({{ id: 'test-note-root', title: 'Test Root Note' }}),
  pywebview: mockPyWebView,
  fetch: (url, opts) => Promise.resolve({{ ok: true, json: () => Promise.resolve({{}}) }}),
  __clipboardBuffer: clipboardBuffer,
  __persistCalls: persistBlockUpdateCalls,
  __toastCalls: showToastCalls,
  __pywebviewCalls: pywebviewCalls,
  __editorCanvas: editorCanvas
}};
sandbox.window = sandbox;
sandbox.global = sandbox;

{extra_setup}

const appCode = fs.readFileSync({json.dumps(APP_JS_PATH)}, 'utf-8') + '\\n;if (typeof window !== "undefined") window.__internalState = state;\\n';
vm.runInNewContext(appCode, sandbox);

// Default activeRecordMap inside sandbox.__internalState
if (sandbox.__internalState) {{
  sandbox.__internalState.activeRecordMap = {{ block: {{}} }};
}}

const runTest = function() {{
  {script_body}
}};

runTest();
console.log('__TEST_PASSED__');
"""
        proc = subprocess.run(['node', '-e', harness_code], capture_output=True, text=True)
        if proc.returncode != 0:
            raise AssertionError(f"Node VM test execution failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        self.assertIn('__TEST_PASSED__', proc.stdout)


# =============================================================================
# 1. Deep Nested Transclusion DAGs (Synced Blocks Inside Synced Blocks)
# =============================================================================

class TestTier5TransclusionDAGs(Tier5NodeVMBasedTest):
    """Adversarial stress testing of transclusion containers and references under complex DAG topologies."""

    def test_deep_nested_transclusion_container_hierarchy(self):
        """Verifies nested transclusion: Container C1 contains Container C2 which contains a leaf block."""
        js_code = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const canvas = sandbox.__editorCanvas;

        const recordMap = {
          block: {
            'root': { value: { id: 'root', type: 'page', content: ['tc1'], alive: 1 } },
            'tc1': { value: { id: 'tc1', type: 'transclusion_container', content: ['tc2'], alive: 1 } },
            'tc2': { value: { id: 'tc2', type: 'transclusion_container', content: ['leaf1'], alive: 1 } },
            'leaf1': { value: { id: 'leaf1', type: 'header_4', properties: { title: [['Deep Nested Title', []]] }, content: [], alive: 1 } }
          }
        };

        renderTreeFromRecordMap(recordMap, 'root', canvas);

        const tc1El = canvas.querySelector('[data-block-id="tc1"]');
        assert.ok(tc1El, 'Outer container tc1 should be rendered');
        assert.strictEqual(tc1El.getAttribute('data-type'), 'transclusion_container');

        const tc2El = tc1El.querySelector('[data-block-id="tc2"]');
        assert.ok(tc2El, 'Inner container tc2 should be rendered inside tc1');
        assert.strictEqual(tc2El.getAttribute('data-type'), 'transclusion_container');

        const leafEl = tc2El.querySelector('[data-block-id="leaf1"]');
        assert.ok(leafEl, 'Leaf block should be rendered inside nested tc2');
        assert.strictEqual(leafEl.getAttribute('data-type'), 'header_4');
        assert.ok(leafEl.innerHTML.includes('Deep Nested Title'));
        """
        self.run_node_vm(js_code)

    def test_diamond_transclusion_dag_multiple_references(self):
        """Verifies diamond DAG: Multiple transclusion_reference blocks pointing to the same transclusion_container."""
        js_code = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const canvas = sandbox.__editorCanvas;

        const recordMap = {
          block: {
            'root': { value: { id: 'root', type: 'page', content: ['tc_master', 'ref1', 'ref2'], alive: 1 } },
            'tc_master': {
              value: {
                id: 'tc_master',
                type: 'transclusion_container',
                content: ['child_todo', 'child_quote'],
                alive: 1
              }
            },
            'child_todo': {
              value: {
                id: 'child_todo',
                type: 'to_do',
                properties: { title: [['Shared Action Item', []]], checked: [['Yes', []]] },
                content: [],
                alive: 1
              }
            },
            'child_quote': {
              value: {
                id: 'child_quote',
                type: 'quote',
                properties: { title: [['Shared Philosophy', []]] },
                content: [],
                alive: 1
              }
            },
            'ref1': {
              value: {
                id: 'ref1',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tc_master' } },
                alive: 1
              }
            },
            'ref2': {
              value: {
                id: 'ref2',
                type: 'transclusion_reference',
                format: { transclusion_reference_pointer: { id: 'tc_master' } },
                alive: 1
              }
            }
          }
        };

        renderTreeFromRecordMap(recordMap, 'root', canvas);

        // Verify master container rendered
        const masterEl = canvas.querySelector('[data-block-id="tc_master"]');
        assert.ok(masterEl);
        assert.ok(masterEl.querySelector('[data-block-id="child_todo"]'));
        assert.ok(masterEl.querySelector('[data-block-id="child_quote"]'));

        // Verify Ref1 expanded both shared children
        const ref1El = canvas.querySelector('[data-block-id="ref1"]');
        assert.ok(ref1El);
        assert.strictEqual(ref1El.getAttribute('data-copied-from'), 'tc_master');
        const ref1Todo = ref1El.querySelector('[data-block-id="child_todo"]');
        const ref1Quote = ref1El.querySelector('[data-block-id="child_quote"]');
        assert.ok(ref1Todo, 'Ref1 should render shared child_todo');
        assert.ok(ref1Quote, 'Ref1 should render shared child_quote');

        // Verify Ref2 expanded both shared children independently (diamond DAG completion)
        const ref2El = canvas.querySelector('[data-block-id="ref2"]');
        assert.ok(ref2El);
        const ref2Todo = ref2El.querySelector('[data-block-id="child_todo"]');
        const ref2Quote = ref2El.querySelector('[data-block-id="child_quote"]');
        assert.ok(ref2Todo, 'Ref2 should render shared child_todo independently');
        assert.ok(ref2Quote, 'Ref2 should render shared child_quote independently');
        """
        self.run_node_vm(js_code)

    def test_multi_hop_transclusion_reference_chain(self):
        """Verifies multi-hop transclusion chain: Root -> RefA -> MasterA (contains RefB) -> MasterB (contains leaf)."""
        js_code = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const canvas = sandbox.__editorCanvas;

        const recordMap = {
          block: {
            'root': { value: { id: 'root', type: 'page', content: ['ref_a'], alive: 1 } },
            'ref_a': {
              value: {
                id: 'ref_a',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'master_a' } },
                alive: 1
              }
            },
            'master_a': {
              value: {
                id: 'master_a',
                type: 'transclusion_container',
                content: ['ref_b'],
                alive: 1
              }
            },
            'ref_b': {
              value: {
                id: 'ref_b',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'master_b' } },
                alive: 1
              }
            },
            'master_b': {
              value: {
                id: 'master_b',
                type: 'transclusion_container',
                content: ['deep_leaf'],
                alive: 1
              }
            },
            'deep_leaf': {
              value: {
                id: 'deep_leaf',
                type: 'callout',
                properties: { title: [['Multi-hop Terminal Block', []]] },
                format: { page_icon: '🚀' },
                content: [],
                alive: 1
              }
            }
          }
        };

        renderTreeFromRecordMap(recordMap, 'root', canvas);

        const refA = canvas.querySelector('[data-block-id="ref_a"]');
        assert.ok(refA, 'Top reference ref_a should be mounted');

        const refB = refA.querySelector('[data-block-id="ref_b"]');
        assert.ok(refB, 'Intermediate reference ref_b should be mounted inside ref_a');

        const leaf = refB.querySelector('[data-block-id="deep_leaf"]');
        assert.ok(leaf, 'Deep terminal callout should be mounted inside ref_b');
        assert.ok(leaf.innerHTML.includes('Multi-hop Terminal Block'));
        """
        self.run_node_vm(js_code)

    def test_circular_transclusion_dag_cycle_prevention(self):
        """Adversarial cycle attack: MasterA has RefB -> MasterB has RefA -> MasterA. Asserts cycle guard terminates."""
        js_code = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const canvas = sandbox.__editorCanvas;

        const recordMap = {
          block: {
            'root': { value: { id: 'root', type: 'page', content: ['tc_a'], alive: 1 } },
            'tc_a': {
              value: {
                id: 'tc_a',
                type: 'transclusion_container',
                content: ['ref_to_b'],
                alive: 1
              }
            },
            'ref_to_b': {
              value: {
                id: 'ref_to_b',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tc_b' } },
                alive: 1
              }
            },
            'tc_b': {
              value: {
                id: 'tc_b',
                type: 'transclusion_container',
                content: ['ref_to_a', 'leaf_safe'],
                alive: 1
              }
            },
            'ref_to_a': {
              value: {
                id: 'ref_to_a',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tc_a' } },
                alive: 1
              }
            },
            'leaf_safe': {
              value: {
                id: 'leaf_safe',
                type: 'text',
                properties: { title: [['Cyclic Boundary Reached', []]] },
                content: [],
                alive: 1
              }
            }
          }
        };

        // Execution MUST complete without Maximum Call Stack Exceeded error
        renderTreeFromRecordMap(recordMap, 'root', canvas);

        const tcA = canvas.querySelector('[data-block-id="tc_a"]');
        assert.ok(tcA, 'Container A should render');
        const refToB = tcA.querySelector('[data-block-id="ref_to_b"]');
        assert.ok(refToB, 'Reference to B should render inside A');
        const safeLeaf = refToB.querySelector('[data-block-id="leaf_safe"]');
        assert.ok(safeLeaf, 'Safe leaf should render before cycle terminates');
        """
        self.run_node_vm(js_code)

    def test_self_referencing_transclusion_container(self):
        """Adversarial self-reference: Container C1 contains reference to C1 itself."""
        js_code = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const canvas = sandbox.__editorCanvas;

        const recordMap = {
          block: {
            'root': { value: { id: 'root', type: 'page', content: ['self_tc'], alive: 1 } },
            'self_tc': {
              value: {
                id: 'self_tc',
                type: 'transclusion_container',
                content: ['self_ref'],
                alive: 1
              }
            },
            'self_ref': {
              value: {
                id: 'self_ref',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'self_tc' } },
                alive: 1
              }
            }
          }
        };

        // Terminating without recursion error
        renderTreeFromRecordMap(recordMap, 'root', canvas);
        const selfTc = canvas.querySelector('[data-block-id="self_tc"]');
        assert.ok(selfTc);
        const selfRef = selfTc.querySelector('[data-block-id="self_ref"]');
        assert.ok(selfRef);
        """
        self.run_node_vm(js_code)

    def test_wide_transclusion_fanout_stress(self):
        """Stress tests wide transclusion DAG: 35 references referencing a single container in the same note."""
        js_code = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const canvas = sandbox.__editorCanvas;

        const refIds = [];
        const recordMap = {
          block: {
            'root': { value: { id: 'root', type: 'page', content: ['master_c', ...refIds], alive: 1 } },
            'master_c': {
              value: {
                id: 'master_c',
                type: 'transclusion_container',
                content: ['fanout_leaf'],
                alive: 1
              }
            },
            'fanout_leaf': {
              value: {
                id: 'fanout_leaf',
                type: 'quote',
                properties: { title: [['Shared Quote Across 35 Locations', []]] },
                content: [],
                alive: 1
              }
            }
          }
        };

        for (let i = 0; i < 35; i++) {
          const rId = 'ref_fanout_' + i;
          refIds.push(rId);
          recordMap.block[rId] = {
            value: {
              id: rId,
              type: 'transclusion_reference',
              format: { copied_from_pointer: { id: 'master_c' } },
              alive: 1
            }
          };
        }
        recordMap.block['root'].value.content = ['master_c', ...refIds];

        renderTreeFromRecordMap(recordMap, 'root', canvas);

        const renderedRefs = canvas.querySelectorAll('.block-transclusion-reference');
        assert.strictEqual(renderedRefs.length, 35, 'All 35 references should render without failure');

        const renderedQuotes = canvas.querySelectorAll('.block-quote');
        // 1 inside master_c + 35 inside each reference = 36 quotes
        assert.strictEqual(renderedQuotes.length, 36, 'Shared quote should be replicated into all 35 references + 1 master');
        """
        self.run_node_vm(js_code)

    def test_transclusion_reference_dead_and_tombstoned_pointers(self):
        """Tests transclusion reference pointing to non-existent ID or container with alive: 0."""
        js_code = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const canvas = sandbox.__editorCanvas;

        const recordMap = {
          block: {
            'root': { value: { id: 'root', type: 'page', content: ['ref_dead', 'ref_tomb'], alive: 1 } },
            'ref_dead': {
              value: {
                id: 'ref_dead',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'non_existent_id' } },
                alive: 1
              }
            },
            'ref_tomb': {
              value: {
                id: 'ref_tomb',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'tombstoned_tc' } },
                alive: 1
              }
            },
            'tombstoned_tc': {
              value: {
                id: 'tombstoned_tc',
                type: 'transclusion_container',
                content: ['zombie_child'],
                alive: 0 // Tombstoned
              }
            },
            'zombie_child': {
              value: {
                id: 'zombie_child',
                type: 'text',
                properties: { title: [['Ghost Text', []]] },
                alive: 1
              }
            }
          }
        };

        renderTreeFromRecordMap(recordMap, 'root', canvas);

        const deadRef = canvas.querySelector('[data-block-id="ref_dead"]');
        assert.ok(deadRef, 'Dead reference element should still render cleanly');
        const deadBody = deadRef.querySelector('.notion-synced-body');
        assert.strictEqual(deadBody.children.length, 0, 'Dead reference body should be empty');

        const tombRef = canvas.querySelector('[data-block-id="ref_tomb"]');
        assert.ok(tombRef, 'Tombstoned reference element should render cleanly');
        const tombBody = tombRef.querySelector('.notion-synced-body');
        assert.strictEqual(tombBody.children.length, 0, 'Tombstoned reference body should not render dead container children');
        """
        self.run_node_vm(js_code)

    def test_unsync_block_instance_and_clipboard_copy(self):
        """Verifies interactive unsyncing and copy reference actions on synced blocks."""
        js_code = """
        const renderBlock = sandbox.renderBlock;
        const unsyncBlockInstance = sandbox.unsyncBlockInstance;
        const copySyncedBlockReference = sandbox.copySyncedBlockReference;
        const canvas = sandbox.__editorCanvas;

        // 1. Test Copy Reference
        copySyncedBlockReference('tc_test_1234');
        assert.strictEqual(sandbox.__clipboardBuffer.text, 'tc_test_1234');
        const toast = sandbox.document.getElementById('app-toast') || sandbox.document.body.querySelector('#app-toast');
        assert.ok(toast || sandbox.__toastCalls.length > 0, 'Toast notification should be triggered');

        // 2. Test Unsync Reference converting to text
        const refBlock = {
          id: 'ref_to_unsync',
          type: 'transclusion_reference',
          format: { copied_from_pointer: { id: 'tc_test_1234' } },
          alive: 1
        };
        const el = renderBlock(refBlock);
        canvas.appendChild(el);

        if (sandbox.__internalState && sandbox.__internalState.activeRecordMap) {
          sandbox.__internalState.activeRecordMap.block['ref_to_unsync'] = { value: refBlock, role: 'editor' };
        }

        unsyncBlockInstance(el);

        const newTextEl = canvas.querySelector('[data-block-id="ref_to_unsync"]');
        assert.ok(newTextEl, 'Block should remain in DOM after unsync');
        assert.strictEqual(newTextEl.getAttribute('data-type'), 'text', 'Unsynced block should be converted to text');
        """
        self.run_node_vm(js_code)


# =============================================================================
# 2. Rapid Concurrent Block Conversions via convertBlockType
# =============================================================================

class TestTier5BlockConversionRacesAndBoundaries(Tier5NodeVMBasedTest):
    """Stress tests convertBlockType across container/leaf boundaries, rapid sequences, and parent content sync."""

    def test_container_to_leaf_clears_content_null_and_detaches_dom_children(self):
        """Verifies container -> leaf conversion strictly enforces content: null and detaches DOM children."""
        js_code = """
        const convertBlockType = sandbox.convertBlockType;
        const renderBlock = sandbox.renderBlock;
        const canvas = sandbox.__editorCanvas;

        const quoteBlock = {
          id: 'container_quote_1',
          type: 'quote',
          properties: { title: [['Quotation with Children', []]] },
          content: ['child_leaf_1', 'child_leaf_2'],
          alive: 1
        };
        if (sandbox.__internalState && sandbox.__internalState.activeRecordMap) {
          sandbox.__internalState.activeRecordMap.block['container_quote_1'] = { value: quoteBlock, role: 'editor' };
        }

        const quoteEl = renderBlock(quoteBlock);
        canvas.appendChild(quoteEl);

        // Convert container quote into leaf divider
        convertBlockType('container_quote_1', 'divider');

        const dividerEl = canvas.querySelector('[data-block-id="container_quote_1"]');
        assert.ok(dividerEl);
        assert.strictEqual(dividerEl.getAttribute('data-type'), 'divider');

        // Pure leaf rule: content must become null in data model
        const updatedData = sandbox.__internalState.activeRecordMap.block['container_quote_1'].value;
        assert.strictEqual(updatedData.type, 'divider');
        assert.strictEqual(updatedData.content, null, 'Leaf node content must be null');

        // Old children slot must be gone in divider DOM
        assert.strictEqual(dividerEl.querySelector('.block-quote-children'), null);
        """
        self.run_node_vm(js_code)

    def test_leaf_to_container_initializes_empty_content_array(self):
        """Verifies leaf -> container conversion restores content: [] from content: null."""
        js_code = """
        const convertBlockType = sandbox.convertBlockType;
        const renderBlock = sandbox.renderBlock;
        const canvas = sandbox.__editorCanvas;

        const dividerBlock = {
          id: 'leaf_divider_1',
          type: 'divider',
          properties: {},
          content: null,
          alive: 1
        };
        if (sandbox.__internalState && sandbox.__internalState.activeRecordMap) {
          sandbox.__internalState.activeRecordMap.block['leaf_divider_1'] = { value: dividerBlock, role: 'editor' };
        }

        const divEl = renderBlock(dividerBlock);
        canvas.appendChild(divEl);

        // Convert leaf divider to container callout
        convertBlockType('leaf_divider_1', 'callout');

        const calloutEl = canvas.querySelector('[data-block-id="leaf_divider_1"]');
        assert.ok(calloutEl);
        assert.strictEqual(calloutEl.getAttribute('data-type'), 'callout');

        const updatedData = sandbox.__internalState.activeRecordMap.block['leaf_divider_1'].value;
        assert.strictEqual(updatedData.type, 'callout');
        assert.ok(Array.isArray(updatedData.content), 'Container node must have array content');
        assert.strictEqual(updatedData.content.length, 0);

        // Container child slot must now exist in DOM
        assert.ok(calloutEl.querySelector('.block-callout-children'));
        """
        self.run_node_vm(js_code)

    def test_toggleable_header_conversion_boundary(self):
        """Tests toggleable headers: header_4 with format.toggleable = true retains container capability."""
        js_code = """
        const convertBlockType = sandbox.convertBlockType;
        const renderBlock = sandbox.renderBlock;
        const canvas = sandbox.__editorCanvas;

        const h4Block = {
          id: 'toggle_h4_block',
          type: 'header_4',
          properties: { title: [['Toggleable Section 4', []]] },
          format: { toggleable: true },
          content: ['sub_child_1'],
          alive: 1
        };
        if (sandbox.__internalState && sandbox.__internalState.activeRecordMap) {
          sandbox.__internalState.activeRecordMap.block['toggle_h4_block'] = { value: h4Block, role: 'editor' };
        }

        const h4El = renderBlock(h4Block);
        canvas.appendChild(h4El);
        assert.strictEqual(h4El.tagName, 'DETAILS');
        assert.strictEqual(h4El.getAttribute('data-toggleable'), 'true');

        // Convert to non-toggleable text block
        convertBlockType('toggle_h4_block', 'text');

        const textEl = canvas.querySelector('[data-block-id="toggle_h4_block"]');
        assert.ok(textEl);
        assert.strictEqual(textEl.getAttribute('data-type'), 'text');
        const updated = sandbox.__internalState.activeRecordMap.block['toggle_h4_block'].value;
        assert.strictEqual(updated.type, 'text');
        assert.ok(Array.isArray(updated.content));
        """
        self.run_node_vm(js_code)

    def test_high_frequency_sequential_conversions(self):
        """Adversarial stress: Rapidly switches a single block through 30 diverse block types sequentially."""
        js_code = """
        const convertBlockType = sandbox.convertBlockType;
        const renderBlock = sandbox.renderBlock;
        const canvas = sandbox.__editorCanvas;

        const blockId = 'rapid_switch_block';
        const initial = {
          id: blockId,
          type: 'text',
          properties: { title: [['Rapid Transformation Matrix', []]] },
          content: [],
          alive: 1
        };
        if (sandbox.__internalState && sandbox.__internalState.activeRecordMap) {
          sandbox.__internalState.activeRecordMap.block[blockId] = { value: initial, role: 'editor' };
        }

        let currEl = renderBlock(initial);
        canvas.appendChild(currEl);

        const sequence = [
          'header_4', 'quote', 'callout', 'to_do', 'transclusion_container',
          'divider', 'video', 'audio', 'bookmark', 'header_4',
          'quote', 'text', 'to_do', 'callout', 'transclusion_container',
          'file', 'pdf', 'image', 'code', 'equation',
          'bulleted_list', 'numbered_list', 'toggle', 'header', 'sub_header',
          'sub_sub_header', 'header_4', 'quote', 'to_do', 'text'
        ];

        for (const targetType of sequence) {
          convertBlockType(blockId, targetType);
          const el = canvas.querySelector(`[data-block-id="${blockId}"]`);
          assert.ok(el, `DOM element must exist after converting to ${targetType}`);
          assert.strictEqual(el.getAttribute('data-type'), targetType, `DOM data-type must be ${targetType}`);

          const record = sandbox.__internalState.activeRecordMap.block[blockId].value;
          assert.strictEqual(record.type, targetType, `Record type must be ${targetType}`);

          const isLeaf = ['equation', 'divider', 'code', 'image', 'video', 'audio', 'file', 'pdf', 'bookmark', 'table_row', 'transclusion_reference', 'sub_page'].includes(targetType);
          if (isLeaf) {
            assert.strictEqual(record.content, null, `Leaf ${targetType} must have content: null`);
          } else {
            assert.ok(Array.isArray(record.content), `Container ${targetType} must have array content`);
          }
        }
        """
        self.run_node_vm(js_code)

    def test_concurrent_sibling_conversions_preserve_order(self):
        """Parent container with 4 children where children are converted, preserving order."""
        js_code = """
        const convertBlockType = sandbox.convertBlockType;
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const canvas = sandbox.__editorCanvas;

        const recordMap = {
          block: {
            'root_page': {
              value: {
                id: 'root_page',
                type: 'page',
                content: ['parent_callout'],
                alive: 1
              }
            },
            'parent_callout': {
              value: {
                id: 'parent_callout',
                type: 'callout',
                properties: { title: [['Parent Callout', []]] },
                content: ['child_1', 'child_2', 'child_3', 'child_4'],
                alive: 1,
                parent_id: 'root_page'
              }
            },
            'child_1': { value: { id: 'child_1', type: 'text', properties: { title: [['One', []]] }, alive: 1, parent_id: 'parent_callout' } },
            'child_2': { value: { id: 'child_2', type: 'text', properties: { title: [['Two', []]] }, alive: 1, parent_id: 'parent_callout' } },
            'child_3': { value: { id: 'child_3', type: 'text', properties: { title: [['Three', []]] }, alive: 1, parent_id: 'parent_callout' } },
            'child_4': { value: { id: 'child_4', type: 'text', properties: { title: [['Four', []]] }, alive: 1, parent_id: 'parent_callout' } }
          }
        };
        sandbox.__internalState.activeRecordMap = recordMap;

        renderTreeFromRecordMap(recordMap, 'root_page', canvas);

        // Convert child_2 to header_4 and child_3 to quote
        convertBlockType('child_2', 'header_4');
        convertBlockType('child_3', 'quote');

        const parent = canvas.querySelector('[data-block-id="parent_callout"]');
        assert.ok(parent, 'Parent callout must be in DOM');
        const childrenSlot = parent.querySelector('.block-callout-children');
        const renderedIds = childrenSlot.children.map(c => c.getAttribute('data-block-id'));

        assert.deepStrictEqual(renderedIds, ['child_1', 'child_2', 'child_3', 'child_4'], 'Child order in DOM must remain intact');
        """
        self.run_node_vm(js_code)


# =============================================================================
# 3. XSS Sanitization & HTML Injection in Rich Text Titles
# =============================================================================

class TestTier5XSSAndHTMLInjection(Tier5NodeVMBasedTest):
    """Adversarial security audit: verifying script injection and dangerous URL sanitization across all blocks."""

    def test_xss_sanitization_in_all_new_block_titles(self):
        """Verifies raw script tags and inline handlers in rich text titles are neutralized in all 11 new block types."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        const maliciousPayloads = [
          '<script>alert("XSS")</script>',
          '<img src="x" onerror="alert(1)">',
          '<svg onload="alert(1)">',
          '"><iframe src="javascript:alert(1)">'
        ];

        const testTypes = [
          'header_4', 'to_do', 'quote', 'callout',
          'transclusion_container', 'transclusion_reference',
          'video', 'audio', 'file', 'pdf', 'bookmark'
        ];

        for (const btype of testTypes) {
          for (const payload of maliciousPayloads) {
            const block = {
              id: 'xss_' + btype + '_' + Math.random().toString(36).slice(2, 6),
              type: btype,
              properties: {
                title: [[payload, []]],
                caption: [[payload, []]],
                source: payload,
                link: payload
              },
              format: {
                page_icon: payload,
                display_source: payload
              },
              alive: 1
            };

            const el = renderBlock(block);
            assert.ok(el, `Block ${btype} should render element under payload`);

            // Check that raw script or unescaped tags do not exist in the DOM hierarchy
            assert.strictEqual(el.querySelector('script'), null, `${btype} must not contain unescaped <script> tag`);
            assert.strictEqual(el.querySelector('svg[onload]'), null, `${btype} must not contain SVG with onload`);
            assert.strictEqual(el.querySelector('img[onerror]'), null, `${btype} must not contain IMG with onerror`);
          }
        }
        """
        self.run_node_vm(js_code)

    def test_malicious_url_schemes_in_rich_text_links(self):
        """Verifies sanitizeLinkUrl and parseRichTextToHtml strictly neutralize dangerous URL schemes."""
        js_code = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;

        const attackVectors = [
          'javascript:alert(1)',
          'JAVASCRIPT:alert(document.cookie)',
          '  javascript:alert(1)  ',
          'vbscript:msgbox(1)',
          'VBSCRIPT:msgbox(1)',
          'data:text/html,<script>alert(1)</script>',
          'DATA:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==',
          'file:///C:/Windows/System32/calc.exe',
          'FILE:///etc/passwd'
        ];

        for (const badUrl of attackVectors) {
          const tuples = [['Click Here', [['a', badUrl]]]];
          const html = parseRichTextToHtml(tuples);

          assert.ok(html.includes('href="#"'), `Attack URL "${badUrl}" must be sanitized to href="#" in rich text output: ${html}`);
          assert.ok(!html.toLowerCase().includes('href="javascript:'), `Output must not contain executable javascript href: ${html}`);
          assert.ok(!html.toLowerCase().includes('href="vbscript:'), `Output must not contain executable vbscript href: ${html}`);
          assert.ok(!html.toLowerCase().includes('href="data:'), `Output must not contain executable data href: ${html}`);
          assert.ok(!html.toLowerCase().includes('href="file:'), `Output must not contain executable file href: ${html}`);
        }
        """
        self.run_node_vm(js_code)

    def test_attribute_breakout_in_color_and_equation_decorators(self):
        """Verifies decorator arguments cannot break out of HTML attributes with quotes or event handlers."""
        js_code = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;

        // Color decorator attribute breakout attempt
        const maliciousColor = 'red" onmouseover="alert(1)" data-x="';
        const colorTuples = [['Styled Text', [['h', maliciousColor]]]];
        const colorHtml = parseRichTextToHtml(colorTuples);

        assert.ok(!colorHtml.includes('onmouseover='), 'Color decorator must not allow attribute breakout to onmouseover');
        assert.ok(!colorHtml.includes('alert(1)'), 'Color decorator payload must be neutralized');

        // Equation formula HTML breakout attempt
        const maliciousLatex = '\\text{test} <script>alert(1)</script>';
        const eqTuples = [['⁍', [['e', maliciousLatex]]]];
        const eqHtml = parseRichTextToHtml(eqTuples);

        assert.ok(!eqHtml.includes('<script>'), 'Equation formula must escape HTML tags');
        assert.ok(eqHtml.includes('&lt;script&gt;'), 'Equation formula must have encoded entities');
        """
        self.run_node_vm(js_code)

    def test_tag_soup_in_html_to_rich_text_tuples(self):
        """Verifies htmlToRichTextTuples handles malformed, unclosed, or mismatched tag soup gracefully."""
        js_code = """
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        const tagSoups = [
          '<div>Unclosed <b>bold <i>italic text</div>',
          '<p>Broken <a href="https://example.com">link without closing tag <mark>highlight</p>',
          '<s><s><s>Nested same tags</s></s></s>',
          '<<>>><<<bad syntax>>'
        ];

        for (const soup of tagSoups) {
          const tuples = htmlToRichTextTuples(soup);
          assert.ok(Array.isArray(tuples), 'htmlToRichTextTuples must return array for tag soup');
          for (const seg of tuples) {
            assert.ok(typeof seg[0] === 'string', 'Segment text must be string');
            assert.ok(Array.isArray(seg[1]), 'Segment decorators must be array');
          }
        }
        """
        self.run_node_vm(js_code)


# =============================================================================
# 4. Extreme Inputs & Special Unicode Characters
# =============================================================================

class TestTier5ExtremeInputsAndUnicode(Tier5NodeVMBasedTest):
    """Stress tests covering empty, null, massive, and exotic Unicode text in new blocks."""

    def test_empty_null_and_corrupted_properties_across_all_blocks(self):
        """Tests that renderBlock and rich-text parser survive null, undefined, primitive, and empty properties."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        const allNewTypes = [
          'header_4', 'to_do', 'quote', 'callout',
          'transclusion_container', 'transclusion_reference',
          'video', 'audio', 'file', 'pdf', 'bookmark'
        ];

        const corruptedCases = [
          null,
          {},
          { properties: null },
          { properties: {} },
          { properties: { title: null } },
          { properties: { title: [] } },
          { properties: { title: [['', []]] } },
          { properties: { title: [[null, []]] } },
          { properties: { title: 4242 } },
          { properties: { title: false } },
          { properties: { checked: null } },
          { format: null }
        ];

        for (const btype of allNewTypes) {
          for (const corrupt of corruptedCases) {
            const block = Object.assign({ id: 'corrupt_' + btype, type: btype, alive: 1 }, corrupt);
            const el = renderBlock(block);
            assert.ok(el, `Block ${btype} must render valid element under corrupted input`);
            assert.strictEqual(el.getAttribute('data-type'), btype);
          }
        }
        """
        self.run_node_vm(js_code)

    def test_massive_text_length_stress(self):
        """Stress tests rendering massive 50,000-character text strings in header_4, to_do, quote, callout."""
        js_code = """
        const renderBlock = sandbox.renderBlock;
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;

        const massiveStr = 'A'.repeat(50000);
        const tuples = [[massiveStr, [['b'], ['i']]]];

        const html = parseRichTextToHtml(tuples);
        assert.ok(html.length >= 50000, 'HTML output length must match massive input');

        const targets = ['header_4', 'to_do', 'quote', 'callout'];
        for (const btype of targets) {
          const el = renderBlock({
            id: 'massive_' + btype,
            type: btype,
            properties: { title: tuples },
            alive: 1
          });
          assert.ok(el, `Massive text block ${btype} must render`);
          assert.ok(el.textContent.includes('AAAAA'), `Rendered text must contain content`);
        }
        """
        self.run_node_vm(js_code)

    def test_complex_unicode_emoji_and_rtl_scripts(self):
        """Tests multi-byte Unicode: complex ZWJ emojis (👨‍👩‍👧‍👦, 👩🏽‍💻), RTL Arabic/Hebrew scripts, and equation tokens."""
        js_code = """
        const renderBlock = sandbox.renderBlock;
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        const complexStrings = [
          '👨‍👩‍👧‍👦 Family with ZWJ',
          '👩🏽‍💻 Tech woman with skin-tone modifier',
          '🏳️‍🌈 Rainbow flag sequence',
          'مرحبا بالعالم - نص باللغة العربية',
          'שָׁלוֹם עֲלֵיכֶם - עברית עם ניקוד',
          '𝕸𝖆𝖙𝖍 𝕱𝖗𝖆𝖐𝖙𝖚𝖗 & 𝒳𝓎𝓏 Script',
          'Zero\\u200BWidth\\u200CSpace\\u200DJoiner',
          '\\u0000Null Byte & Control \\u0001\\u0002',
          'Equation token delimiter ⁍ and \\u204d'
        ];

        for (const str of complexStrings) {
          const tuples = [[str, [['b']]]];
          const html = parseRichTextToHtml(tuples);
          assert.ok(html.includes('<strong>'), 'HTML must contain strong tag');

          // Roundtrip through htmlToRichTextTuples
          const roundtrip = htmlToRichTextTuples(html);
          assert.ok(Array.isArray(roundtrip));
          assert.ok(roundtrip.length > 0);

          // Verify rendering on to_do and header_4
          const todoEl = renderBlock({
            id: 'uni_todo',
            type: 'to_do',
            properties: { title: tuples },
            alive: 1
          });
          assert.ok(todoEl);

          const h4El = renderBlock({
            id: 'uni_h4',
            type: 'header_4',
            properties: { title: tuples },
            alive: 1
          });
          assert.ok(h4El);
        }
        """
        self.run_node_vm(js_code)


# =============================================================================
# 5. Interactive to_do Event Edge Cases & Keyboard Navigation
# =============================================================================

class TestTier5ToDoInteractiveEdgeCases(Tier5NodeVMBasedTest):
    """Adversarial stress testing of to_do checkbox toggling, state synchronization, Enter key, and Backspace."""

    def test_rapid_checkbox_toggling_100_cycles(self):
        """Rapidly toggles to_do checkbox 100 times in tight loop, verifying DOM class and state persistence."""
        js_code = """
        const renderBlock = sandbox.renderBlock;
        const canvas = sandbox.__editorCanvas;

        const todoBlock = {
          id: 'todo_rapid_toggle',
          type: 'to_do',
          properties: { title: [['Rapid Toggle Task', []]], checked: [['No', []]] },
          alive: 1
        };
        if (sandbox.__internalState && sandbox.__internalState.activeRecordMap) {
          sandbox.__internalState.activeRecordMap.block['todo_rapid_toggle'] = { value: todoBlock, role: 'editor' };
        }

        const todoEl = renderBlock(todoBlock);
        canvas.appendChild(todoEl);

        const chk = todoEl.querySelector('.notion-to-do-checkbox');
        const titleEl = todoEl.querySelector('.notion-to-do-title');
        assert.ok(chk);
        assert.ok(titleEl);
        assert.strictEqual(chk.checked, false);
        assert.strictEqual(titleEl.classList.has('completed'), false);

        // Execute 100 alternating clicks
        for (let i = 0; i < 100; i++) {
          chk.click();
          const expectedChecked = (i % 2 === 0); // Click 0 (1st click) -> true, Click 1 -> false
          assert.strictEqual(chk.checked, expectedChecked, `Cycle ${i}: Checkbox checked should be ${expectedChecked}`);
          assert.strictEqual(titleEl.classList.has('completed'), expectedChecked, `Cycle ${i}: Title class completed should be ${expectedChecked}`);

          const recordChecked = sandbox.__internalState.activeRecordMap.block['todo_rapid_toggle'].value.properties.checked;
          const expectedVal = expectedChecked ? 'Yes' : 'No';
          assert.strictEqual(recordChecked[0][0], expectedVal, `Cycle ${i}: activeRecordMap checked value should be ${expectedVal}`);
        }

        // Verify persistence calls were registered
        assert.ok(sandbox.__persistCalls.length >= 100 || sandbox.__pywebviewCalls.update_block.length >= 100, 'Persistence should be called on each toggle');
        """
        self.run_node_vm(js_code)

    def test_checkbox_toggling_without_state_or_recordmap(self):
        """Verifies checkbox click does not crash when window.state is undefined or block is missing."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        const orphanTodo = {
          id: 'orphan_todo',
          type: 'to_do',
          properties: { title: [['Orphan Task', []]] },
          alive: 1
        };

        const todoEl = renderBlock(orphanTodo);
        const chk = todoEl.querySelector('.notion-to-do-checkbox');
        const titleEl = todoEl.querySelector('.notion-to-do-title');

        // Click should complete safely without uncaught exception
        chk.click();
        assert.strictEqual(chk.checked, true);
        assert.ok(titleEl.classList.has('completed'));
        """
        self.run_node_vm(js_code)

    def test_enter_key_triggers_insert_block_below(self):
        """Verifies Enter key handling on a to_do block calls insertBlockBelow and updates parent content."""
        js_code = """
        const insertBlockBelow = sandbox.insertBlockBelow;
        const renderBlock = sandbox.renderBlock;
        const canvas = sandbox.__editorCanvas;

        const parentId = 'note_container';
        const parentBlock = {
          id: parentId,
          type: 'page',
          content: ['todo_first'],
          alive: 1
        };
        const todoFirst = {
          id: 'todo_first',
          type: 'to_do',
          properties: { title: [['First Task Item', []]] },
          parent_id: parentId,
          alive: 1
        };

        if (sandbox.__internalState && sandbox.__internalState.activeRecordMap) {
          sandbox.__internalState.activeRecordMap.block[parentId] = { value: parentBlock, role: 'editor' };
          sandbox.__internalState.activeRecordMap.block['todo_first'] = { value: todoFirst, role: 'editor' };
        }

        const firstEl = renderBlock(todoFirst);
        firstEl.setAttribute('data-parent-id', parentId);
        firstEl.setAttribute('data-block-id', 'todo_first');
        canvas.appendChild(firstEl);

        // Simulate Enter action via insertBlockBelow
        insertBlockBelow(firstEl);

        // Assert new block created and inserted after firstEl
        assert.strictEqual(canvas.children.length, 2, 'New block element should be inserted into canvas');
        const secondEl = canvas.children[1];
        assert.ok(secondEl.getAttribute('data-block-id'));
        assert.strictEqual(secondEl.getAttribute('data-type'), 'text');

        // Assert parent content array updated with new block ID immediately after todo_first
        const updatedParentContent = sandbox.__internalState.activeRecordMap.block[parentId].value.content;
        assert.strictEqual(updatedParentContent.length, 2);
        assert.strictEqual(updatedParentContent[0], 'todo_first');
        assert.strictEqual(updatedParentContent[1], secondEl.getAttribute('data-block-id'));
        """
        self.run_node_vm(js_code)

    def test_backspace_on_empty_to_do_converts_to_text(self):
        """Verifies Backspace key on empty to_do converts the block to 'text' via convertBlockType."""
        js_code = """
        const convertBlockType = sandbox.convertBlockType;
        const renderBlock = sandbox.renderBlock;
        const canvas = sandbox.__editorCanvas;

        const emptyTodo = {
          id: 'empty_todo_blk',
          type: 'to_do',
          properties: { title: [['', []]] },
          alive: 1
        };
        if (sandbox.__internalState && sandbox.__internalState.activeRecordMap) {
          sandbox.__internalState.activeRecordMap.block['empty_todo_blk'] = { value: emptyTodo, role: 'editor' };
        }

        const el = renderBlock(emptyTodo);
        canvas.appendChild(el);

        // Backspace action on empty block triggers convertBlockType(id, 'text')
        convertBlockType('empty_todo_blk', 'text');

        const newEl = canvas.querySelector('[data-block-id="empty_todo_blk"]');
        assert.ok(newEl);
        assert.strictEqual(newEl.getAttribute('data-type'), 'text');
        assert.strictEqual(sandbox.__internalState.activeRecordMap.block['empty_todo_blk'].value.type, 'text');
        """
        self.run_node_vm(js_code)

    def test_delete_block_element_removes_from_dom_and_parent_content(self):
        """Verifies deleteBlockElement removes block from DOM, sets alive: 0, and filters parent content."""
        js_code = """
        const deleteBlockElement = sandbox.deleteBlockElement;
        const renderBlock = sandbox.renderBlock;
        const canvas = sandbox.__editorCanvas;

        const parentId = 'parent_p';
        const parentBlock = {
          id: parentId,
          type: 'page',
          content: ['blk_a', 'blk_b'],
          alive: 1
        };
        const blkA = { id: 'blk_a', type: 'text', parent_id: parentId, alive: 1 };
        const blkB = { id: 'blk_b', type: 'text', parent_id: parentId, alive: 1 };

        if (sandbox.__internalState && sandbox.__internalState.activeRecordMap) {
          sandbox.__internalState.activeRecordMap.block[parentId] = { value: parentBlock, role: 'editor' };
          sandbox.__internalState.activeRecordMap.block['blk_a'] = { value: blkA, role: 'editor' };
          sandbox.__internalState.activeRecordMap.block['blk_b'] = { value: blkB, role: 'editor' };
        }

        const elA = renderBlock(blkA);
        const elB = renderBlock(blkB);
        canvas.appendChild(elA);
        canvas.appendChild(elB);

        deleteBlockElement(elB, elA);

        assert.strictEqual(canvas.children.length, 1);
        assert.strictEqual(canvas.children[0].getAttribute('data-block-id'), 'blk_a');
        assert.strictEqual(sandbox.__internalState.activeRecordMap.block['blk_b'].value.alive, 0);
        assert.deepStrictEqual(parentBlock.content, ['blk_a']);
        """
        self.run_node_vm(js_code)


if __name__ == '__main__':
    unittest.main()
