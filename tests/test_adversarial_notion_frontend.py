#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_adversarial_notion_frontend.py
Adversarial verification and empirical stress-test suite for Milestone 4:
Frontend Rich Text Engine, Notion Block Suite, and DOM Rendering.

Aggressive test coverage dimensions:
1. Extreme Rich Text Decorator Combinations:
   - All 8 decorators applied simultaneously (b, i, _, s, c, h, a, e)
   - Deeply nested tag trees and recursion limits
   - Overlapping and interleaved HTML decorator tags
   - Empty, null, and whitespace string segments
   - Multi-byte Unicode, complex emojis (ZWJ, skin-tones), and RTL scripts
   - LaTeX formulas with backslashes, quotes, and HTML special chars
2. XSS & HTML Injection Vectors:
   - Malicious URL schemes in sanitizeLinkUrl & rich text links (javascript:, vbscript:, data:, file:)
   - HTML and script injection in text and equation formulas (<script>, <img onerror>, <svg>)
   - Attribute breakout attacks in color (<mark>) and link (<a>) decorators
   - Tag soup and malformed HTML in htmlToRichTextTuples
   - Direct boundary testing of sanitizeLinkUrl
3. Node.js VM DOM Stress Test Rendering Malformed Block Dictionaries:
   - Missing required fields (type, id, properties, content, format)
   - Unexpected types (null, primitives, non-dict properties, non-array content)
   - Corrupted properties and titles
   - Malformed recordMaps and missing child records
   - Circular reference loops (A -> B -> A, A -> A) and deep nesting (40+ levels)
4. Column Layout Boundary Tests:
   - Extreme column counts (10 to 25 columns in a single row)
   - Boundary ratios (ratio = 0, ratio = 1.0, extreme values)
   - Invalid and non-numeric ratios (negative, string, null, undefined)
5. Table Block Stress Test:
   - Missing column order fallback mechanisms
   - Row length mismatch with column order (shorter rows, longer rows)
   - Empty and corrupted row properties
   - Column order with duplicate, empty, or special keys
6. Missing KaTeX Fallback Behavior:
   - Equation block rendering when window.katex is undefined
   - Equation input event handler execution without window.katex
   - Inline equation rich text fallback to raw LaTeX
   - Graceful handling when window.katex.render throws a KaTeX ParseError
"""

import os
import json
import subprocess
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')


class NodeVMBasedTest(unittest.TestCase):
    """Base class providing a hardened Node.js VM DOM environment for stress testing."""

    @classmethod
    def setUpClass(cls):
        try:
            res = subprocess.run(['node', '-v'], capture_output=True, text=True, check=True)
            cls.node_available = True
            cls.node_version = res.stdout.strip()
        except Exception:
            cls.node_available = False

    def run_node_vm(self, test_script, extra_sandbox_js=''):
        """Executes JavaScript test code inside a mocked browser DOM with app.js loaded."""
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

// DOM Mock Implementation
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
  removeAttribute(k) {{ delete this.attributes[k]; }}
  get className() {{ return this.classList.toString(); }}
  set className(v) {{
    this.classList = new MockClassList(String(v).split(/\\s+/).filter(Boolean));
    this.attributes['class'] = v;
  }}
  get value() {{ return this._value !== undefined ? this._value : (this.getAttribute('value') || ''); }}
  set value(v) {{ this._value = String(v); this.setAttribute('value', v); }}
  focus() {{}}
  blur() {{}}
  addEventListener(event, fn) {{
    this._listeners = this._listeners || {{}};
    this._listeners[event] = this._listeners[event] || [];
    this._listeners[event].push(fn);
  }}
  removeEventListener(event, fn) {{
    if (!this._listeners || !this._listeners[event]) return;
    this._listeners[event] = this._listeners[event].filter(f => f !== fn);
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
  createRange: () => ({{
    selectNodeContents: () => {{}},
    collapse: () => {{}}
  }}),
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
  getSelection: () => ({{ removeAllRanges: () => {{}}, addRange: () => {{}} }}),
  __lastLoadedNote: null,
  loadNote: function(id) {{ sandbox.__lastLoadedNote = id; }}
}};
sandbox.window = sandbox;
sandbox.global = sandbox;

{extra_sandbox_js}

const appCode = fs.readFileSync({json.dumps(APP_JS_PATH)}, 'utf-8');
vm.runInNewContext(appCode, sandbox);

// Test Runner
const runTest = function() {{
  {test_script}
}};

runTest();
console.log('__TEST_PASSED__');
""";
        proc = subprocess.run(['node', '-e', harness_code], capture_output=True, text=True)
        if proc.returncode != 0:
            raise AssertionError(f"Node VM test execution failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        self.assertIn('__TEST_PASSED__', proc.stdout)


# =============================================================================
# 1. Extreme Rich Text Decorator Combinations
# =============================================================================

class TestAdversarialRichTextEngine(NodeVMBasedTest):
    """Stress tests on parseRichTextToHtml and htmlToRichTextTuples with extreme inputs."""

    def test_all_eight_decorators_simultaneously(self):
        """Applies all 8 rich text decorators simultaneously and tests roundtrip and DOM safety."""
        js_code = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        // All 8 decorators applied simultaneously on a single segment:
        // b, i, _, s, c, h, a, e
        const all8 = [[
          'FormulaAndText',
          [
            ['b'],
            ['i'],
            ['_'],
            ['s'],
            ['c'],
            ['h', 'teal_background'],
            ['a', 'https://notion.so/workspace'],
            ['e', '\\\\int_{0}^{\\\\infty} e^{-x} dx = 1']
          ]
        ]];

        const html = parseRichTextToHtml(all8);
        assert(html.includes('<strong>'), 'Missing bold tag');
        assert(html.includes('<em>'), 'Missing italic tag');
        assert(html.includes('<u>'), 'Missing underline tag');
        assert(html.includes('<s>'), 'Missing strikethrough tag');
        assert(html.includes('<code>'), 'Missing code tag');
        assert(html.includes('notion-color-teal_background'), 'Missing highlight class');
        assert(html.includes('href="https://notion.so/workspace"'), 'Missing link href');
        assert(html.includes('inline-equation'), 'Missing equation class');
        assert(html.includes('data-latex='), 'Missing data-latex');

        // Test all 7 non-equation text decorators together (pure text formatting roundtrip)
        const all7 = [[
          'AllTextDecors',
          [
            ['b'],
            ['i'],
            ['_'],
            ['s'],
            ['c'],
            ['h', 'blue'],
            ['a', 'https://example.com']
          ]
        ]];
        const html7 = parseRichTextToHtml(all7);
        const parsed7 = htmlToRichTextTuples(html7);

        assert.strictEqual(parsed7.length, 1, 'Should preserve 1 consolidated segment');
        assert.strictEqual(parsed7[0][0], 'AllTextDecors');
        const decMap = new Map();
        parsed7[0][1].forEach(d => decMap.set(d[0], d[1]));
        assert(decMap.has('b'), 'Expected bold decorator');
        assert(decMap.has('i'), 'Expected italic decorator');
        assert(decMap.has('_'), 'Expected underline decorator');
        assert(decMap.has('s'), 'Expected strike decorator');
        assert(decMap.has('c'), 'Expected code decorator');
        assert.strictEqual(decMap.get('h'), 'blue', 'Expected blue highlight');
        assert.strictEqual(decMap.get('a'), 'https://example.com', 'Expected link url');
        """
        self.run_node_vm(js_code)

    def test_deeply_nested_html_decorator_tags(self):
        """Stress-tests htmlToRichTextTuples with 30 layers of deeply nested tags."""
        js_code = """
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        // Build 30 nested tags
        let deepHtml = 'Core Deep Text';
        const tags = ['strong', 'em', 'u', 's', 'code'];
        for (let i = 0; i < 30; i++) {
          const t = tags[i % tags.length];
          deepHtml = `<${t}>${deepHtml}</${t}>`;
        }

        const tuples = htmlToRichTextTuples(deepHtml);
        assert(tuples.length >= 1, 'Failed to extract text from deep tree');
        assert.strictEqual(tuples[0][0], 'Core Deep Text');
        const decNames = tuples[0][1].map(d => d[0]);
        assert(decNames.includes('b'));
        assert(decNames.includes('i'));
        assert(decNames.includes('_'));
        assert(decNames.includes('s'));
        assert(decNames.includes('c'));
        """
        self.run_node_vm(js_code)

    def test_overlapping_and_interleaved_html_decorators(self):
        """Ensures htmlToRichTextTuples handles interleaved/overlapping tags without throwing."""
        js_code = """
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        // Overlapping tags in tag-soup representation
        const mixed = '<b>BoldOnly <i>BoldItalic</b> ItalicOnly</i> <u>Underline</u> Normal';
        const tuples = htmlToRichTextTuples(mixed);
        assert(Array.isArray(tuples));
        assert(tuples.length >= 3, 'Expected multiple segments from mixed tags');
        const fullText = tuples.map(t => t[0]).join('');
        assert(fullText.includes('BoldOnly'));
        assert(fullText.includes('BoldItalic'));
        assert(fullText.includes('ItalicOnly'));
        assert(fullText.includes('Underline'));
        assert(fullText.includes('Normal'));
        """
        self.run_node_vm(js_code)

    def test_empty_and_null_string_segments(self):
        """Tests empty strings, nulls, undefined, and zero-length tuples."""
        js_code = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        assert.strictEqual(parseRichTextToHtml([]), '');
        assert.strictEqual(parseRichTextToHtml(null), '');
        assert.strictEqual(parseRichTextToHtml(undefined), '');
        assert.strictEqual(parseRichTextToHtml(''), '');
        assert.strictEqual(parseRichTextToHtml([['', [['b']]]]), '<strong></strong>');
        assert.strictEqual(parseRichTextToHtml([[null, []]]), '');
        assert.strictEqual(parseRichTextToHtml([[undefined, [['i']]]]), '<em></em>');
        assert.strictEqual(parseRichTextToHtml([['', [['e', '']]]]), '<span class=\"inline-equation notion-inline-equation inline-katex-node\" data-latex=\"\" contenteditable=\"false\"></span>');

        // Cross-realm safe array length/JSON verification
        assert.strictEqual(JSON.stringify(htmlToRichTextTuples(null)), JSON.stringify([]));
        assert.strictEqual(JSON.stringify(htmlToRichTextTuples(undefined)), JSON.stringify([]));
        assert.strictEqual(JSON.stringify(htmlToRichTextTuples('')), JSON.stringify([]));
        assert.strictEqual(JSON.stringify(htmlToRichTextTuples(12345)), JSON.stringify([]));
        assert.strictEqual(JSON.stringify(htmlToRichTextTuples({})), JSON.stringify([]));
        """
        self.run_node_vm(js_code)

    def test_multibyte_unicode_emojis_and_rtl(self):
        """Verifies multi-byte Unicode (ZWJ emojis, skin tones, CJK, Arabic RTL) roundtrips intact."""
        js_code = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        const complexUnicode = [
          ['👨‍👩‍👧‍👦', [['b']]],                        // ZWJ family emoji (11 bytes UTF-8)
          [' 👍🏽 ', [['h', 'yellow_background']]],     // Skin tone modifier
          ['🏳️‍🌈', [['c']]],                           // Rainbow flag (ZWJ)
          ['\u200B\u200C\u200D\uFEFF', [['_']]],     // Zero-width characters
          ['日本語テスト (CJK)', [['i']]],
          ['مرحبا بالعالم (Arabic RTL)', [['a', 'https://example.com/ar']]]
        ];

        const html = parseRichTextToHtml(complexUnicode);
        assert(html.includes('👨‍👩‍👧‍👦'));
        assert(html.includes('👍🏽'));
        assert(html.includes('🏳️‍🌈'));
        assert(html.includes('日本語テスト (CJK)'));
        assert(html.includes('مرحبا بالعالم (Arabic RTL)'));

        const roundtrip = htmlToRichTextTuples(html);
        assert.strictEqual(roundtrip.length, 6);
        assert.strictEqual(roundtrip[0][0], '👨‍👩‍👧‍👦');
        assert.strictEqual(roundtrip[1][0], ' 👍🏽 ');
        assert.strictEqual(roundtrip[2][0], '🏳️‍🌈');
        assert.strictEqual(roundtrip[3][0], '\u200B\u200C\u200D\uFEFF');
        assert.strictEqual(roundtrip[4][0], '日本語テスト (CJK)');
        assert.strictEqual(roundtrip[5][0], 'مرحبا بالعالم (Arabic RTL)');
        """
        self.run_node_vm(js_code)

    def test_latex_backslashes_quotes_and_special_chars(self):
        """Tests LaTeX formulas containing special characters, backslashes, <, >, &, and quotes."""
        js_code = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        const formula = '\\\\int_{0}^{\\\\infty} \\\\frac{\\\\alpha < \\\\beta & \\\\gamma > \\\\delta}{x^2 + \\\"q\\\" + \\\'r\\\'} dx';
        const tuples = [['formula', [['e', formula]]]];

        const html = parseRichTextToHtml(tuples);
        assert(!html.includes('< \\\\beta'), 'Unescaped < in HTML attribute or text');
        assert(!html.includes('> \\\\delta'), 'Unescaped > in HTML attribute or text');
        assert(html.includes('&lt;'), 'Expected escaped &lt;');
        assert(html.includes('&gt;'), 'Expected escaped &gt;');
        assert(html.includes('&amp;'), 'Expected escaped &amp;');
        assert(html.includes('&quot;'), 'Expected escaped &quot;');

        const roundtrip = htmlToRichTextTuples(html);
        assert.strictEqual(roundtrip.length, 1);
        assert.strictEqual(roundtrip[0][0], formula, 'Extracted formula must match original exactly');
        assert.strictEqual(roundtrip[0][1][0][0], 'e');
        assert.strictEqual(roundtrip[0][1][0][1], formula);
        """
        self.run_node_vm(js_code)


# =============================================================================
# 2. XSS and HTML Injection Vectors
# =============================================================================

class TestAdversarialXssAndHtmlInjection(NodeVMBasedTest):
    """Hostile attack payloads targeting XSS, HTML injection, and URL sanitization."""

    def test_xss_dangerous_schemes_in_links(self):
        """Sanitizes dangerous URL schemes: javascript:, vbscript:, data:, file:."""
        js_code = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;

        const maliciousPayloads = [
          'javascript:alert(document.domain)',
          'JAVASCRIPT:alert(1)',
          '  javascript:alert(2)  ',
          'vbscript:msgbox(1)',
          'VBSCRIPT:alert(3)',
          'data:text/html,<script>alert(4)</script>',
          'data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==',
          'file:///C:/Windows/System32/cmd.exe',
          'FILE:///etc/passwd'
        ];

        for (const payload of maliciousPayloads) {
          const tuples = [['Click Here', [['a', payload]]]];
          const html = parseRichTextToHtml(tuples);
          assert(!html.toLowerCase().includes('javascript:'), 'Failed to neutralize javascript: ' + payload);
          assert(!html.toLowerCase().includes('vbscript:'), 'Failed to neutralize vbscript: ' + payload);
          assert(!html.toLowerCase().includes('data:'), 'Failed to neutralize data: ' + payload);
          assert(!html.toLowerCase().includes('file:'), 'Failed to neutralize file: ' + payload);
          assert(html.includes('href=\"#\"'), 'Should fallback to href=\"#\" for: ' + payload);
        }
        """
        self.run_node_vm(js_code)

    def test_xss_in_plain_text_and_formula_segments(self):
        """Escapes raw HTML tags, script injection, and onerror event handlers in text and formulas."""
        js_code = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;

        const injectionTuples = [
          ['<script>alert(\"XSS\")</script>', []],
          ['<img src=\"x\" onerror=\"alert(1)\" />', []],
          ['<svg onload=\"alert(2)\"><g/></svg>', []],
          ['<iframe src=\"javascript:alert(3)\"></iframe>', []],
          ['Formula', [['e', '\"><script>alert(4)</script><span data=\"']]]
        ];

        const html = parseRichTextToHtml(injectionTuples);

        assert(!html.includes('<script>'), 'Unescaped <script> tag generated');
        assert(!html.includes('<img src='), 'Unescaped <img> tag');
        assert(!html.includes('<svg'), 'Unescaped <svg> tag');
        assert(!html.includes('<iframe'), 'Unescaped <iframe> tag');
        assert(!/<[a-zA-Z][^>]*onerror/i.test(html), 'Active onerror handler found');
        assert(!/<[a-zA-Z][^>]*onload/i.test(html), 'Active onload handler found');

        assert(html.includes('&lt;script&gt;'));
        assert(html.includes('&lt;img'));
        assert(html.includes('&lt;svg'));
        """
        self.run_node_vm(js_code)

    def test_xss_attribute_breakout_in_color_and_links(self):
        """Neutralizes attribute breakout injection in highlight colors and links."""
        js_code = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;

        // Color attribute breakout attempt
        const colorBreakout = [['Text', [['h', 'red\" onclick=\"alert(1)\" style=\"evil']]]];
        const colorHtml = parseRichTextToHtml(colorBreakout);
        assert(!colorHtml.includes('onclick=\"alert(1)\"'), 'Color attribute breakout succeeded');
        assert(colorHtml.includes('notion-color-redonclickalert1styleevil'), 'Clean color regex should sanitize payload');

        // Link attribute breakout attempt: Quotes must be escaped to &quot; so href is not terminated
        const linkBreakout = [['Link', [['a', 'https://example.com/\" onmouseover=\"alert(1)']]]];
        const linkHtml = parseRichTextToHtml(linkBreakout);
        assert(!linkHtml.includes('\" onmouseover='), 'Link attribute breakout succeeded via unescaped quote');
        assert(linkHtml.includes('&quot; onmouseover='), 'Quotes in URL must be escaped in attribute value');
        """
        self.run_node_vm(js_code)

    def test_malformed_html_tag_soup_in_deserializer(self):
        """Deserializer survives chaotic tag soup without throwing exceptions."""
        js_code = """
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        const soups = [
          '<div><p>Unclosed <b>nested <i>tags without closing',
          '<<<>>><><><!----><!---->',
          '<unknown-custom-tag attr=\"value\">Custom Text</unknown-custom-tag>',
          'Text before <!-- unclosed comment',
          '<a href=\"javascript:alert(1)\">Link</a>',
          null,
          undefined,
          12345,
          {},
          true
        ];

        for (const soup of soups) {
          const res = htmlToRichTextTuples(soup);
          assert(Array.isArray(res), 'htmlToRichTextTuples must return array for soup: ' + soup);
        }
        """
        self.run_node_vm(js_code)

    def test_sanitize_link_url_direct_boundaries(self):
        """Validates sanitizeLinkUrl logic against diverse boundary cases."""
        js_code = """
        const sanitizeLinkUrl = sandbox.sanitizeLinkUrl;
        assert.strictEqual(typeof sanitizeLinkUrl, 'function');

        // Dangerous schemes
        assert.strictEqual(sanitizeLinkUrl('javascript:alert(1)'), '#');
        assert.strictEqual(sanitizeLinkUrl('JAVASCRIPT:alert(1)'), '#');
        assert.strictEqual(sanitizeLinkUrl('  vbscript:msgbox(1)  '), '#');
        assert.strictEqual(sanitizeLinkUrl('data:text/html,abc'), '#');
        assert.strictEqual(sanitizeLinkUrl('file:///etc/hosts'), '#');

        // Non-string / invalid
        assert.strictEqual(sanitizeLinkUrl(null), '#');
        assert.strictEqual(sanitizeLinkUrl(undefined), '#');
        assert.strictEqual(sanitizeLinkUrl(''), '#');
        assert.strictEqual(sanitizeLinkUrl(12345), '#');
        assert.strictEqual(sanitizeLinkUrl({}), '#');

        // Safe schemes and paths preserved
        assert.strictEqual(sanitizeLinkUrl('https://example.com/path?a=1&b=2'), 'https://example.com/path?a=1&b=2');
        assert.strictEqual(sanitizeLinkUrl('http://localhost:8000/api/notes'), 'http://localhost:8000/api/notes');
        assert.strictEqual(sanitizeLinkUrl('/notes/subpage-123'), '/notes/subpage-123');
        assert.strictEqual(sanitizeLinkUrl('#section-target'), '#section-target');
        assert.strictEqual(sanitizeLinkUrl('mailto:support@notejs.org'), 'mailto:support@notejs.org');
        """
        self.run_node_vm(js_code)


# =============================================================================
# 3. Node.js VM DOM Stress Test Rendering Malformed Block Dictionaries
# =============================================================================

class TestAdversarialMalformedBlockRendering(NodeVMBasedTest):
    """Stress tests renderBlock and renderTreeFromRecordMap with malformed schemas and types."""

    def test_render_block_missing_fields(self):
        """renderBlock handles missing fields (id, type, properties, format) gracefully."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        // Missing type -> returns null safely
        assert.strictEqual(renderBlock({ id: 'missing-type' }), null);

        // Missing id -> auto-generates fallback ID without throwing
        const noId = renderBlock({ type: 'text', properties: { title: [['No ID Block', []]] } });
        assert(noId, 'Should create element when id is missing');
        assert(noId.getAttribute('data-block-id'), 'Missing auto-generated block ID');

        // Missing properties -> renders element without throwing
        const noProps = renderBlock({ id: 'b-no-props', type: 'text' });
        assert(noProps);

        // Header missing title property -> renders empty header
        const emptyH1 = renderBlock({ id: 'h1', type: 'header', properties: {} });
        assert(emptyH1);
        assert.strictEqual(emptyH1.tagName, 'H1');

        // Code missing title and language -> defaults python and empty code
        const code = renderBlock({ id: 'cd', type: 'code', properties: {} });
        assert(code);
        assert.strictEqual(code.querySelector('code').textContent, '');

        // Image missing format and properties -> uses default placeholder
        const img = renderBlock({ id: 'im', type: 'image' });
        assert(img);
        assert(img.querySelector('img').getAttribute('src').length > 0);

        // Subpage missing page_id and title -> defaults gracefully
        const sp = renderBlock({ id: 'sp', type: 'sub_page' });
        assert(sp);
        assert(sp.innerHTML.includes('Sin título'));
        """
        self.run_node_vm(js_code)

    def test_render_block_unexpected_property_types(self):
        """Survives corrupted property types (numbers, booleans, objects, bad arrays)."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        const malformedBlocks = [
          { id: 'b1', type: 'text', properties: 'string-instead-of-object' },
          { id: 'b2', type: 'text', properties: 12345 },
          { id: 'b3', type: 'text', properties: null },
          { id: 'b4', type: 'text', properties: [] },
          { id: 'b5', type: 'text', properties: { title: 42 } },
          { id: 'b6', type: 'text', properties: { title: 'plain-string-title' } },
          { id: 'b7', type: 'text', properties: { title: { nested: 'object' } } },
          { id: 'b8', type: 'text', properties: { title: [null, undefined, 42, {}] } },
          { id: 'b9', type: 'text', properties: { title: [[null, null]] } }
        ];

        for (const blk of malformedBlocks) {
          const el = renderBlock(blk);
          assert(el, 'Failed to render corrupted block: ' + JSON.stringify(blk));
          assert.strictEqual(el.getAttribute('data-type'), 'text');
        }
        """
        self.run_node_vm(js_code)

    def test_render_block_non_array_content(self):
        """Survives corrupted block content fields."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        const blocksWithBadContent = [
          { id: 'c1', type: 'text', content: 'string-content' },
          { id: 'c2', type: 'text', content: 9999 },
          { id: 'c3', type: 'text', content: {} },
          { id: 'c4', type: 'text', content: [null, undefined, 123, {}] }
        ];

        for (const blk of blocksWithBadContent) {
          const el = renderBlock(blk);
          assert(el, 'Should safely render block with non-array content');
        }
        """
        self.run_node_vm(js_code)

    def test_render_block_null_and_primitive_inputs(self):
        """renderBlock handles non-object inputs safely."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        assert.strictEqual(renderBlock(null), null);
        assert.strictEqual(renderBlock(undefined), null);
        assert.strictEqual(renderBlock('not-an-object'), null);
        assert.strictEqual(renderBlock(12345), null);
        assert.strictEqual(renderBlock([]), null);
        """
        self.run_node_vm(js_code)

    def test_render_tree_malformed_record_maps(self):
        """renderTreeFromRecordMap survives nulls, empty dicts, and missing child records."""
        js_code = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const container = sandbox.document.createElement('div');

        // Null / undefined record maps
        renderTreeFromRecordMap(null, 'root', container);
        renderTreeFromRecordMap(undefined, 'root', container);
        renderTreeFromRecordMap({}, 'root', container);
        renderTreeFromRecordMap({ block: null }, 'root', container);
        renderTreeFromRecordMap({ block: 'string' }, 'root', container);
        renderTreeFromRecordMap({ block: { root: null } }, 'root', container);
        renderTreeFromRecordMap({ block: { root: { value: null } } }, 'root', container);

        // RecordMap referencing non-existent child IDs
        const rmapWithMissingChildren = {
          block: {
            'page-1': {
              role: 'editor',
              value: {
                id: 'page-1',
                type: 'page',
                content: ['non-existent-child-1', 'non-existent-child-2', 'valid-child'],
                alive: 1
              }
            },
            'valid-child': {
              role: 'editor',
              value: {
                id: 'valid-child',
                type: 'text',
                properties: { title: [['Solo Hijo Válido', []]] },
                alive: 1
              }
            }
          }
        };

        renderTreeFromRecordMap(rmapWithMissingChildren, 'page-1', container);
        assert.strictEqual(container.children.length, 1, 'Only valid child should be mounted');
        assert(container.innerHTML.includes('Solo Hijo Válido'));
        """
        self.run_node_vm(js_code)

    def test_render_tree_circular_references_and_deep_nesting(self):
        """Prevents infinite recursion and stack overflows in circular and deeply nested trees."""
        js_code = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const container = sandbox.document.createElement('div');

        // 1. Direct Self-referencing node: A -> A
        const selfCycleMap = {
          block: {
            'root': {
              role: 'editor',
              value: { id: 'root', type: 'page', content: ['cycle-self'], alive: 1 }
            },
            'cycle-self': {
              role: 'editor',
              value: { id: 'cycle-self', type: 'text', content: ['cycle-self'], alive: 1 }
            }
          }
        };
        renderTreeFromRecordMap(selfCycleMap, 'root', container);
        assert.strictEqual(container.children.length, 1);

        // 2. 3-Node Cycle: A -> B -> C -> A
        const triCycleMap = {
          block: {
            'root': {
              role: 'editor',
              value: { id: 'root', type: 'page', content: ['nodeA'], alive: 1 }
            },
            'nodeA': {
              role: 'editor',
              value: { id: 'nodeA', type: 'text', content: ['nodeB'], alive: 1 }
            },
            'nodeB': {
              role: 'editor',
              value: { id: 'nodeB', type: 'text', content: ['nodeC'], alive: 1 }
            },
            'nodeC': {
              role: 'editor',
              value: { id: 'nodeC', type: 'text', content: ['nodeA'], alive: 1 }
            }
          }
        };
        renderTreeFromRecordMap(triCycleMap, 'root', container);
        assert.strictEqual(container.children.length, 1);

        // 3. Deep Nesting: Chain of 40 nested blocks
        const deepMap = {
          block: {
            'root': {
              role: 'editor',
              value: { id: 'root', type: 'page', content: ['chain-0'], alive: 1 }
            }
          }
        };
        for (let i = 0; i < 40; i++) {
          deepMap.block['chain-' + i] = {
            role: 'editor',
            value: {
              id: 'chain-' + i,
              type: 'text',
              properties: { title: [['Nivel ' + i, []]] },
              content: i < 39 ? ['chain-' + (i + 1)] : [],
              alive: 1
            }
          };
        }
        renderTreeFromRecordMap(deepMap, 'root', container);
        assert(container.innerHTML.includes('Nivel 0'));
        assert(container.innerHTML.includes('Nivel 39'));
        """
        self.run_node_vm(js_code)


# =============================================================================
# 4. Column Layout Boundary Tests
# =============================================================================

class TestAdversarialColumnLayoutBoundaries(NodeVMBasedTest):
    """Stress tests column layout under extreme counts and extreme/invalid ratios."""

    def test_extreme_column_counts(self):
        """Renders column_list with extreme column counts (10 and 25 columns)."""
        js_code = """
        const renderBlock = sandbox.renderBlock;
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;
        const container = sandbox.document.createElement('div');

        // Column List with 10 columns
        const colList10 = {
          block: {
            'root': { role: 'editor', value: { id: 'root', type: 'page', content: ['cl10'], alive: 1 } },
            'cl10': { role: 'editor', value: { id: 'cl10', type: 'column_list', content: [], alive: 1 } }
          }
        };
        for (let i = 0; i < 10; i++) {
          const cId = 'col-10-' + i;
          colList10.block['cl10'].value.content.push(cId);
          colList10.block[cId] = {
            role: 'editor',
            value: { id: cId, type: 'column', format: { column_ratio: 0.1 }, content: [], alive: 1 }
          };
        }

        renderTreeFromRecordMap(colList10, 'root', container);
        const clEl = container.children[0];
        assert.strictEqual(clEl.children.length, 10, 'Must mount 10 columns');
        for (const col of clEl.children) {
          assert.strictEqual(col.getAttribute('data-type'), 'column');
          assert.strictEqual(col.style.minWidth, '60px');
          assert(col.style.flex.includes('0.1'));
        }

        // Extreme: 25 columns in a single row
        for (let i = 10; i < 25; i++) {
          const cId = 'col-25-' + i;
          colList10.block['cl10'].value.content.push(cId);
          colList10.block[cId] = {
            role: 'editor',
            value: { id: cId, type: 'column', format: { column_ratio: 0.04 }, content: [], alive: 1 }
          };
        }
        renderTreeFromRecordMap(colList10, 'root', container);
        assert.strictEqual(container.children[0].children.length, 25, 'Must mount 25 columns');
        """
        self.run_node_vm(js_code)

    def test_zero_and_extreme_column_ratios(self):
        """Handles ratio=0, ratio=1.0, extreme small and large ratios safely."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        const testRatios = [
          { ratio: 0, expectedFlex: '0 1 0%' },
          { ratio: 1.0, expectedFlex: '1 1 0%' },
          { ratio: 0.0001, expectedFlex: '0.0001 1 0%' },
          { ratio: 50.0, expectedFlex: '50 1 0%' }
        ];

        for (const t of testRatios) {
          const col = renderBlock({
            id: 'col-ratio-' + t.ratio,
            type: 'column',
            format: { column_ratio: t.ratio }
          });
          assert(col);
          assert.strictEqual(col.style.flex, t.expectedFlex);
          assert.strictEqual(col.style.minWidth, '60px');
          assert(col.querySelector('.notion-column-content'));
        }
        """
        self.run_node_vm(js_code)

    def test_invalid_and_non_numeric_column_ratios(self):
        """Falls back safely to default ratio 0.5 when ratio is missing, string, or invalid."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        const invalidRatioBlocks = [
          { id: 'ir1', type: 'column', format: { column_ratio: '50%' } },
          { id: 'ir2', type: 'column', format: { column_ratio: null } },
          { id: 'ir3', type: 'column', format: { column_ratio: undefined } },
          { id: 'ir4', type: 'column', format: {} },
          { id: 'ir5', type: 'column', format: null },
          { id: 'ir6', type: 'column' }
        ];

        for (const blk of invalidRatioBlocks) {
          const col = renderBlock(blk);
          assert(col, 'Must render column element for: ' + JSON.stringify(blk));
          assert.strictEqual(col.style.flex, '0.5 1 0%', 'Must fallback to ratio 0.5');
        }

        // Negative ratio does not throw exception
        const negCol = renderBlock({ id: 'neg', type: 'column', format: { column_ratio: -0.25 } });
        assert(negCol);
        assert.strictEqual(negCol.style.flex, '-0.25 1 0%');
        """
        self.run_node_vm(js_code)


# =============================================================================
# 5. Table Block Stress Test
# =============================================================================

class TestAdversarialTableBlockStress(NodeVMBasedTest):
    """Stress tests table and table_row blocks under missing/corrupted configurations."""

    def test_table_missing_column_order_fallback(self):
        """Falls back to properties keys or default columns when table_block_column_order is absent."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        // 1. Fallback to row properties keys when format.table_block_column_order is missing
        const rowWithProps = renderBlock({
          id: 'tr1',
          type: 'table_row',
          properties: {
            'custom_col_A': [['Valor A', []]],
            'custom_col_B': [['Valor B', []]]
          }
        });
        assert(rowWithProps);
        assert.strictEqual(rowWithProps.tagName, 'TR');
        const cells1 = rowWithProps.children;
        assert.strictEqual(cells1.length, 2);
        assert.strictEqual(cells1[0].getAttribute('data-col-id'), 'custom_col_A');
        assert.strictEqual(cells1[1].getAttribute('data-col-id'), 'custom_col_B');
        assert(cells1[0].innerHTML.includes('Valor A'));
        assert(cells1[1].innerHTML.includes('Valor B'));

        // 2. Absolute fallback to ['col_1', 'col_2'] when both format and properties are empty
        const rowEmpty = renderBlock({
          id: 'tr2',
          type: 'table_row',
          properties: {}
        });
        assert(rowEmpty);
        const cells2 = rowEmpty.children;
        assert.strictEqual(cells2.length, 2);
        assert.strictEqual(cells2[0].getAttribute('data-col-id'), 'col_1');
        assert.strictEqual(cells2[1].getAttribute('data-col-id'), 'col_2');
        """
        self.run_node_vm(js_code)

    def test_table_row_length_mismatch_with_column_order(self):
        """Handles rows with fewer or more properties than defined by column order."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        const definedOrder = ['col_1', 'col_2', 'col_3', 'col_4'];

        // Row with fewer properties (only col_1 provided)
        const rowShorter = renderBlock({
          id: 'tr-short',
          type: 'table_row',
          format: { table_block_column_order: definedOrder },
          properties: {
            'col_1': [['Presente', []]]
          }
        });
        assert.strictEqual(rowShorter.children.length, 4, 'Must create empty cells for missing cols');
        assert.strictEqual(rowShorter.children[0].innerHTML, 'Presente');
        assert.strictEqual(rowShorter.children[1].innerHTML, '');
        assert.strictEqual(rowShorter.children[2].innerHTML, '');
        assert.strictEqual(rowShorter.children[3].innerHTML, '');

        // Row with extra properties (col_1 through col_6)
        const rowLonger = renderBlock({
          id: 'tr-long',
          type: 'table_row',
          format: { table_block_column_order: definedOrder },
          properties: {
            'col_1': [['A', []]],
            'col_2': [['B', []]],
            'col_3': [['C', []]],
            'col_4': [['D', []]],
            'col_5_extra': [['Extra 1', []]],
            'col_6_extra': [['Extra 2', []]]
          }
        });
        assert.strictEqual(rowLonger.children.length, 4, 'Must respect column order length');
        assert.strictEqual(rowLonger.children[0].innerHTML, 'A');
        assert.strictEqual(rowLonger.children[3].innerHTML, 'D');
        """
        self.run_node_vm(js_code)

    def test_table_row_empty_and_corrupted_properties(self):
        """Renders cells safely when properties are null or have corrupted values."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        const rowCorrupted = renderBlock({
          id: 'tr-corrupt',
          type: 'table_row',
          format: { table_block_column_order: ['c1', 'c2', 'c3'] },
          properties: {
            'c1': null,
            'c2': 12345,
            'c3': [[]]
          }
        });
        assert(rowCorrupted);
        assert.strictEqual(rowCorrupted.children.length, 3);
        assert.strictEqual(rowCorrupted.children[0].innerHTML, '');
        // Non-string/non-array properties safely normalize to empty string in getBlockPropertyHtml
        assert.strictEqual(rowCorrupted.children[1].innerHTML, '');
        assert.strictEqual(rowCorrupted.children[2].innerHTML, '');
        """
        self.run_node_vm(js_code)

    def test_table_column_order_duplicates_and_empty_keys(self):
        """Renders table cells without crashing when column order has duplicate or empty keys."""
        js_code = """
        const renderBlock = sandbox.renderBlock;

        const rowDuplicateCols = renderBlock({
          id: 'tr-dup',
          type: 'table_row',
          format: { table_block_column_order: ['col_dup', 'col_dup', '', 'col_other'] },
          properties: {
            'col_dup': [['Repetido', []]],
            'col_other': [['Otro', []]]
          }
        });
        assert(rowDuplicateCols);
        assert.strictEqual(rowDuplicateCols.children.length, 4);
        assert.strictEqual(rowDuplicateCols.children[0].innerHTML, 'Repetido');
        assert.strictEqual(rowDuplicateCols.children[1].innerHTML, 'Repetido');
        assert.strictEqual(rowDuplicateCols.children[3].innerHTML, 'Otro');
        """
        self.run_node_vm(js_code)


# =============================================================================
# 6. Missing KaTeX Fallback Behavior
# =============================================================================

class TestAdversarialKatexFallbackBehavior(NodeVMBasedTest):
    """Validates formula rendering robustness when KaTeX is absent or throws parse errors."""

    def test_equation_block_missing_katex_displays_raw_latex(self):
        """Equation block displays raw LaTeX string without throwing when window.katex is undefined."""
        js_code = """
        // Ensure window.katex is undefined
        assert.strictEqual(typeof sandbox.window.katex, 'undefined');

        const renderBlock = sandbox.renderBlock;
        const formula = '\\\\sum_{k=1}^n k = \\\\frac{n(n+1)}{2}';

        const eqEl = renderBlock({
          id: 'eq-test',
          type: 'equation',
          properties: {
            title: [[formula, []]]
          }
        });

        assert(eqEl, 'Failed to render equation block');
        assert.strictEqual(eqEl.getAttribute('data-type'), 'equation');
        const disp = eqEl.querySelector('.notion-equation-display');
        assert(disp, 'Missing equation display node');
        assert.strictEqual(disp.getAttribute('data-latex'), formula);
        assert.strictEqual(disp.textContent, formula, 'Display must contain raw formula text');
        """
        self.run_node_vm(js_code)

    def test_equation_input_event_missing_katex_no_exception(self):
        """Editing equation via input element updates raw LaTeX display without throwing."""
        js_code = """
        assert.strictEqual(typeof sandbox.window.katex, 'undefined');

        const renderBlock = sandbox.renderBlock;
        const eqEl = renderBlock({
          id: 'eq-edit',
          type: 'equation',
          properties: { title: [['E=mc^2', []]] }
        });

        const disp = eqEl.querySelector('.notion-equation-display');
        const inp = eqEl.querySelector('.notion-equation-input');
        assert(disp && inp);

        // Simulate typing new formula in popover
        const newFormula = '\\\\nabla \\\\times \\\\mathbf{B} = \\\\mu_0 \\\\mathbf{J}';
        inp.value = newFormula;
        inp.oninput();

        assert.strictEqual(disp.getAttribute('data-latex'), newFormula);
        assert.strictEqual(disp.textContent, newFormula, 'Display must update to new raw formula');
        """
        self.run_node_vm(js_code)

    def test_inline_equation_missing_katex_renders_fallback(self):
        """Inline equation tuple generates valid DOM span with raw LaTeX text when KaTeX is absent."""
        js_code = """
        assert.strictEqual(typeof sandbox.window.katex, 'undefined');

        const parseRichTextToHtml = sandbox.parseRichTextToHtml;
        const formula = 'a^2 + b^2 = c^2';
        const tuples = [['Pythagoras', [['e', formula]]]];

        const html = parseRichTextToHtml(tuples);
        assert(html.includes('inline-equation'));
        assert(html.includes('data-latex=\"a^2 + b^2 = c^2\"'));
        assert(html.includes('contenteditable=\"false\"'));
        assert(html.includes(formula));
        """
        self.run_node_vm(js_code)

    def test_katex_parse_error_exception_handled_gracefully(self):
        """Catches and handles KaTeX render exceptions (e.g. invalid syntax) without crashing."""
        extra_sandbox = """
        // Mock a KaTeX implementation that throws on malformed syntax
        sandbox.katex = {
          render: function(tex, element, options) {
            if (tex.includes('INVALID_SYNTAX')) {
              throw new Error('KaTeX ParseError: KaTeX parse error: Expected EOF, got INVALID_SYNTAX');
            }
            element.textContent = 'RENDERED:' + tex;
          }
        };
        sandbox.window.katex = sandbox.katex;
        """

        js_code = """
        const renderBlock = sandbox.renderBlock;

        const eqEl = renderBlock({
          id: 'eq-syntax-error',
          type: 'equation',
          properties: { title: [['E = mc^2', []]] }
        });

        const disp = eqEl.querySelector('.notion-equation-display');
        const inp = eqEl.querySelector('.notion-equation-input');

        // Input broken formula that triggers KaTeX throw
        const badFormula = '\\\\frac{1}{0} INVALID_SYNTAX';
        inp.value = badFormula;

        // Must NOT throw uncaught error; must catch and fallback to raw text
        inp.oninput();

        assert.strictEqual(disp.getAttribute('data-latex'), badFormula);
        assert.strictEqual(disp.textContent, badFormula, 'Must fallback to raw formula on parse error');
        """
        self.run_node_vm(js_code, extra_sandbox_js=extra_sandbox)


if __name__ == '__main__':
    unittest.main()
