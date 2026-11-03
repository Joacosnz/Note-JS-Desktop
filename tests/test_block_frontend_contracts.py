#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_block_frontend_contracts.py
Comprehensive automated test suite for Milestone 3:
Frontend Dynamic Rendering, Rich Text & Interactive Editor.

Covers:
1. Static contract verification:
   - Exported globals on window (renderBlock, renderBlocks, attachSubpageBlockListeners,
     loadNote, parseRichTextToHtml, htmlToRichTextTuples, renderTreeFromRecordMap).
   - renderBlock switch-case coverage for all 17 Notion block types + sub_page.
   - Lasso selection guard ([contenteditable="true"], INPUT, TEXTAREA).
   - Bridge & REST persistence patterns (update_block, reorder, recordMap).
   - CSS layout rules for Notion blocks (flexbox columns, toggles, tables, codes, equations).
2. Dynamic execution via Node.js vm:
   - Rich Text Tuple Engine: parseRichTextToHtml, htmlToRichTextTuples, all 8 decorators,
     URL sanitization, round-tripping, text coalescing.
   - Extended Element Factory: renderBlock creating valid DOM elements across all 18 types.
   - Recursive RecordMap Tree Renderer: renderTreeFromRecordMap resolving visual hierarchy,
     nested containers (column_list, column, toggle, table), skipping alive === 0,
     and cycle prevention with visited Set.
"""

import os
import re
import json
import subprocess
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
INDEX_HTML_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'index.html')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')

ALL_17_NOTION_TYPES_PLUS_SUBPAGE = [
    'page',
    'column_list',
    'column',
    'divider',
    'text',
    'header',
    'sub_header',
    'sub_sub_header',
    'header_4',
    'bulleted_list',
    'numbered_list',
    'to_do',
    'toggle',
    'quote',
    'callout',
    'code',
    'equation',
    'table',
    'table_row',
    'collection_view',
    'collection_view_page',
    'transclusion_container',
    'transclusion_reference',
    'image',
    'video',
    'audio',
    'file',
    'pdf',
    'bookmark',
    'sub_page',
]


class TestBlockFrontendStaticContracts(unittest.TestCase):
    """Pruebas estáticas de contratos, selectores, guardas y exportaciones en frontend/."""

    @classmethod
    def setUpClass(cls):
        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()
        with open(INDEX_HTML_PATH, 'r', encoding='utf-8') as f:
            cls.index_html = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()

    def test_exported_globals_on_window(self):
        """Verifica que todos los identificadores globales de Milestone 3 estén exportados a window."""
        expected_exports = [
            'window.renderBlock = renderBlock',
            'window.renderBlocks = renderBlocks',
            'window.attachSubpageBlockListeners = attachSubpageBlockListeners',
            'window.loadNote = loadNote',
            'window.parseRichTextToHtml = parseRichTextToHtml',
            'window.htmlToRichTextTuples = htmlToRichTextTuples',
            'window.renderTreeFromRecordMap = renderTreeFromRecordMap',
        ]
        for exp in expected_exports:
            self.assertIn(exp, self.app_js, f"Exportación requerida ausente en app.js: {exp}")

    def test_render_block_switch_covers_all_notion_types_plus_subpage(self):
        """Verifica que renderBlock cubra todos los 17 tipos canónicos de Notion + sub_page."""
        render_fn_idx = self.app_js.find('function renderBlock(block)')
        self.assertNotEqual(render_fn_idx, -1, "function renderBlock(block) no encontrada en app.js")

        render_blocks_idx = self.app_js.find('function renderBlocks(', render_fn_idx)
        if render_blocks_idx != -1:
            block_slice = self.app_js[render_fn_idx:render_blocks_idx]
        else:
            block_slice = self.app_js[render_fn_idx:render_fn_idx + 80000]

        for btype in ALL_17_NOTION_TYPES_PLUS_SUBPAGE:
            case_stmt = f"case '{btype}':"
            self.assertIn(case_stmt, block_slice, f"Falta caso de bloque en renderBlock: {case_stmt}")

    def test_lasso_selection_guard_aborts_on_editable(self):
        """Verifies mousedown listener strictly aborts when clicking inside editable elements."""
        guard_pattern = r"if\s*\(\s*e\.target\.closest\(\s*['\"]\[contenteditable=[\"']true[\"']\]['\"]\s*\)\s*\|\|\s*e\.target\.tagName\s*===\s*['\"]INPUT['\"]\s*\|\|\s*e\.target\.tagName\s*===\s*['\"]TEXTAREA['\"]\s*\)\s*return;"
        match = re.search(guard_pattern, self.app_js)
        self.assertIsNotNone(match, "La guarda de selección de lazo para elementos editables debe existir exactamente.")

    def test_load_active_note_fetches_record_map_and_calls_render_tree(self):
        """Verifica que loadActiveNote obtenga recordMap y llame a renderTreeFromRecordMap."""
        self.assertIn('get_record_map', self.app_js)
        self.assertIn('/recordMap', self.app_js)
        self.assertIn('renderTreeFromRecordMap', self.app_js)

    def test_css_block_classes_and_side_by_side_flexbox_columns(self):
        """Verifica que styles.css defina estilos para todos los componentes de bloques y flexbox."""
        expected_selectors = [
            '.notion-block',
            '.block-column-list',
            '.block-column',
            '.block-toggle',
            '.block-toggle-summary',
            '.block-toggle-content',
            '.block-code',
            '.block-equation',
            '.block-table',
            '.block-table-row',
            '.block-table-cell',
            '.block-image',
            '.block-divider',
            '.inline-equation',
            '.block-header-4',
            '.block-header-toggle',
            '.block-quote',
            '.block-callout',
            '.block-to-do',
            '.notion-synced-block',
            '.block-video',
            '.block-audio',
            '.block-file',
            '.block-pdf',
            '.block-bookmark',
        ]
        for sel in expected_selectors:
            self.assertIn(sel, self.styles_css, f"Selector CSS requerido ausente: {sel}")

        # Flexbox side-by-side columns
        col_list_match = re.search(r'\.block-column-list[^{]*\{([^}]+)\}', self.styles_css)
        self.assertIsNotNone(col_list_match, "styles.css debe definir regla para .block-column-list")
        rule_content = col_list_match.group(1)
        self.assertIn('display: flex', rule_content)
        self.assertIn('gap: 16px', rule_content)


class TestBlockFrontendDynamicEngine(unittest.TestCase):
    """Pruebas dinámicas ejecutadas mediante Node.js VM en el entorno de desarrollo."""

    @classmethod
    def setUpClass(cls):
        try:
            res = subprocess.run(['node', '-v'], capture_output=True, text=True, check=True)
            cls.node_available = True
            cls.node_version = res.stdout.strip()
        except Exception:
            cls.node_available = False

    def _run_node_script(self, script_code):
        if not self.node_available:
            self.skipTest("Node.js no está instalado en este entorno")

        runner_code = f"""
const fs = require('fs');
const vm = require('vm');

// Mock complete DOM node classes
class MockNode {{
  constructor(nodeType, nodeValue = '') {{
    this.nodeType = nodeType;
    this.nodeValue = nodeValue;
    this.childNodes = [];
    this.parentNode = null;
  }}
  appendChild(child) {{
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
  before(el) {{
    if (!this.parentNode) return;
    const idx = this.parentNode.childNodes.indexOf(this);
    if (idx !== -1) {{
      this.parentNode.childNodes.splice(idx, 0, el);
      el.parentNode = this.parentNode;
    }}
  }}
  after(el) {{
    if (!this.parentNode) return;
    const idx = this.parentNode.childNodes.indexOf(this);
    if (idx !== -1) {{
      this.parentNode.childNodes.splice(idx + 1, 0, el);
      el.parentNode = this.parentNode;
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
  get checked() {{ return this._checked !== undefined ? this._checked : this.hasAttribute('checked'); }}
  set checked(v) {{ this._checked = Boolean(v); if (v) this.setAttribute('checked', ''); else this.removeAttribute('checked'); }}
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
      current.appendChild(new MockNode(3, text));
    }} else if (isClose) {{
      if (current.parentNode) current = current.parentNode;
    }} else {{
      const el = new MockElement(tagName);
      if (attrStr) {{
        const attrRegex = /([a-zA-Z0-9_\\-]+)(?:=(?:["']([^"']*)["']|([^\\s>]+)))?/g;
        let aMatch;
        while ((aMatch = attrRegex.exec(attrStr)) !== null) {{
          const val = aMatch[2] !== undefined ? aMatch[2] : (aMatch[3] !== undefined ? aMatch[3] : '');
          el.setAttribute(aMatch[1], val);
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

const appCode = fs.readFileSync({json.dumps(APP_JS_PATH)}, 'utf-8');
vm.runInNewContext(appCode, sandbox);

// Run test inside vm context
const testFn = function() {{
  const assert = require('assert');
  {script_code}
}};
testFn();
"""
        proc = subprocess.run(['node', '-e', runner_code], capture_output=True, text=True)
        if proc.returncode != 0:
            raise AssertionError(f"Node execution failed (code {proc.returncode}):\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
        return proc.stdout.strip()

    def test_pdf_source_survives_block_collection_and_unsafe_urls_are_rejected(self):
        self._run_node_script("""
        const renderBlock = sandbox.renderBlock;
        const source = '/api/pdfs/' + 'a'.repeat(64) + '.pdf';
        const pdf = renderBlock({type:'pdf', id:'pdf-persist', properties:{source:[[source,[]]], title:[['Álgebra & apuntes.pdf',[]]]}});
        const viewer = pdf.querySelector('iframe').getAttribute('src').replace(/&amp;/g, '&');
        const query = new URL(viewer, 'http://localhost').searchParams;
        assert.strictEqual(query.get('src'), source);
        assert.strictEqual(query.get('name'), 'Álgebra & apuntes.pdf');
        sandbox.document.getElementById = id => id === 'rich-editor-canvas' ? {children:[pdf]} : null;
        let saved;
        sandbox.apiSyncNoteBlocks = (id, blocks) => { saved = blocks; };
        sandbox.collectAndSyncNoteBlocks('note-pdf');
        assert.strictEqual(saved[0].type, 'pdf');
        assert.strictEqual(saved[0].properties.source[0][0], source);
        assert.strictEqual(saved[0].properties.title[0][0], 'Álgebra & apuntes.pdf');
        for (const source of ['javascript:alert(1)', 'data:text/html,<script>alert(1)</script>', 'file:///secret.pdf']) {
          const unsafe = renderBlock({type:'pdf', id:'unsafe', properties:{source:[[source,[]]]}});
          assert(!unsafe.querySelector('iframe'));
        }
        """)

    def test_node_rich_text_parser_and_serializer_roundtrip(self):
        """Verifica parseRichTextToHtml y htmlToRichTextTuples con todos los decoradores."""
        node_script = """
        const parseRichTextToHtml = sandbox.parseRichTextToHtml;
        const htmlToRichTextTuples = sandbox.htmlToRichTextTuples;

        assert.strictEqual(typeof parseRichTextToHtml, 'function');
        assert.strictEqual(typeof htmlToRichTextTuples, 'function');

        // Test all 8 decorators
        const sampleTuples = [
          ['Negrita', [['b']]],
          [' Cursiva', [['i']]],
          [' Subrayado', [['_']]],
          [' Tachado', [['s']]],
          [' Codigo', [['c']]],
          [' Resaltado', [['h', 'yellow_background']]],
          [' Color', [['h', 'blue']]],
          [' Enlace', [['a', 'https://example.com']]],
          [' Formula', []],
          ['E=mc^2', [['e', 'E=mc^2']]],
        ];

        const html = parseRichTextToHtml(sampleTuples);
        assert(html.includes('<strong>Negrita</strong>'));
        assert(html.includes('<em> Cursiva</em>'));
        assert(html.includes('<u> Subrayado</u>'));
        assert(html.includes('<s> Tachado</s>'));
        assert(html.includes('<code> Codigo</code>'));
        assert(html.includes('notion-color-yellow_background'));
        assert(html.includes('notion-color-blue'));
        assert(html.includes('href="https://example.com"'));
        assert(html.includes('data-latex="E=mc^2"'));

        // Test roundtrip
        const parsed = htmlToRichTextTuples(html);
        assert(parsed.length >= 9, 'Debe deserializar todos los segmentos');
        assert.strictEqual(parsed[0][0], 'Negrita');
        assert.strictEqual(JSON.stringify(parsed[0][1]), JSON.stringify([['b']]));
        assert.strictEqual(parsed[1][0], ' Cursiva');
        assert.strictEqual(JSON.stringify(parsed[1][1]), JSON.stringify([['i']]));

        // Malicious URL sanitization
        const malTuples = [['XSS', [['a', 'javascript:alert(1)']]]];
        const malHtml = parseRichTextToHtml(malTuples);
        assert(!malHtml.includes('javascript:alert'), 'URL javascript peligrosa debe ser sanitizada');
        assert(malHtml.includes('href="#"'));

        // Empty / Null safety
        assert.strictEqual(parseRichTextToHtml(null), '');
        assert.strictEqual(parseRichTextToHtml(''), '');
        assert.strictEqual(JSON.stringify(htmlToRichTextTuples(null)), JSON.stringify([]));
        assert.strictEqual(JSON.stringify(htmlToRichTextTuples('')), JSON.stringify([]));

        console.log('SUCCESS_RICHTEXT');
        """
        out = self._run_node_script(node_script)
        self.assertIn('SUCCESS_RICHTEXT', out)

    def test_node_render_block_all_types(self):
        """Verifica que renderBlock produzca elementos correctos para todos los tipos canónicos y extendidos."""
        node_script = """
        const renderBlock = sandbox.renderBlock;

        const types = [
          'page', 'column_list', 'column', 'divider', 'text', 'header',
          'sub_header', 'sub_sub_header', 'header_4', 'bulleted_list', 'numbered_list',
          'to_do', 'toggle', 'quote', 'callout', 'code', 'equation', 'table', 'table_row',
          'collection_view', 'collection_view_page', 'transclusion_container',
          'transclusion_reference', 'image', 'video', 'audio', 'file', 'pdf', 'bookmark', 'sub_page'
        ];

        for (const t of types) {
          const blk = {
            id: 'test-' + t,
            type: t,
            properties: {
              title: [['Titulo de ' + t, []]],
              language: [['javascript', []]],
              source: [['https://example.com/asset.png', []]],
              caption: [['Pie de foto', []]],
              link: [['https://example.com', []]],
              description: [['Descripcion', []]],
              checked: [['Yes', []]],
              size: [['1.2 MB', []]],
              page_id: 'target-note-123'
            },
            format: {
              column_ratio: 0.33,
              table_block_column_order: ['c1', 'c2'],
              block_width: 650,
              page_icon: '💡',
              block_color: 'amber_background',
              copied_from_pointer: { id: 'container-1' }
            }
          };

          const el = renderBlock(blk);
          assert(el, 'renderBlock no debe retornar null para tipo: ' + t);
          assert.strictEqual(el.getAttribute('data-type'), t, 'data-type incorrecto para ' + t);
          assert(el.getAttribute('data-block-id'), 'data-block-id ausente para ' + t);
        }

        // Subpage navigation test
        const sub = renderBlock({ type: 'sub_page', id: 'sp1', page_id: 'n42', title: 'Subnota' });
        assert(sub.classList.has('block-subpage'));
        assert(sub.innerHTML.includes('📄'));
        assert(sub.innerHTML.includes('Subnota'));
        let navCalled = null;
        sandbox.loadNote = function(id) { navCalled = id; };
        sandbox.window.loadNote = sandbox.loadNote;
        sub.onclick({ preventDefault: () => {}, stopPropagation: () => {} });
        assert.strictEqual(navCalled, 'n42', 'Click en subpage debe invocar loadNote');

        // Column List & Column test
        const colListEl = renderBlock({ type: 'column_list', id: 'cl1' });
        assert(colListEl.classList.has('notion-columns-row'));
        const colEl = renderBlock({ type: 'column', id: 'col1', format: { column_ratio: 0.4 } });
        assert(colEl.classList.has('notion-column-slot'));
        assert(colEl.style.flex.includes('0.4'));

        // Toggle test
        const toggleEl = renderBlock({ type: 'toggle', id: 'tg1', properties: { title: [['Seccion', []]] } });
        assert.strictEqual(toggleEl.tagName, 'DETAILS');
        assert(toggleEl.querySelector('summary'));

        // Code test
        const codeEl = renderBlock({ type: 'code', id: 'cd1', properties: { title: [['console.log(1)', []]], language: [['javascript', []]] } });
        assert.strictEqual(codeEl.querySelector('select').value, 'javascript');
        assert.strictEqual(codeEl.querySelector('code').textContent, 'console.log(1)');

        // Header 4 non-toggle test
        const h4El = renderBlock({ type: 'header_4', id: 'h4-1', properties: { title: [['Subtitulo 4', []]] } });
        assert.strictEqual(h4El.tagName, 'H4');
        assert(h4El.classList.has('block-header-4'));

        // Quote test
        const quoteEl = renderBlock({ type: 'quote', id: 'q1', properties: { title: [['Sabiduria', []]] } });
        assert.strictEqual(quoteEl.tagName, 'BLOCKQUOTE');
        assert(quoteEl.querySelector('.notion-quote-content'));
        assert(quoteEl.querySelector('.block-quote-children'));
        assert(quoteEl.querySelector('.notion-block-children'));

        // Callout test
        const calloutEl = renderBlock({
          type: 'callout',
          id: 'co1',
          properties: { title: [['Nota importante', []]] },
          format: { page_icon: '🚀', block_color: 'amber_background' }
        });
        assert(calloutEl.classList.has('block-callout'));
        assert(calloutEl.classList.has('notion-color-amber_background'));
        assert(calloutEl.innerHTML.includes('🚀'));
        assert(calloutEl.querySelector('.block-callout-children'));
        assert(calloutEl.querySelector('.notion-block-children'));

        // To-Do test
        const todoEl = renderBlock({
          type: 'to_do',
          id: 'td1',
          properties: { title: [['Terminar informe', []]], checked: [['Yes', []]] }
        });
        assert(todoEl.classList.has('block-to-do'));
        const todoChk = todoEl.querySelector('.notion-to-do-checkbox');
        assert(todoChk, 'Checkbox debe existir');
        assert(todoChk.hasAttribute('checked'), 'Checkbox debe estar checked');
        assert(todoEl.querySelector('.completed'), 'Titulo debe tener clase completed');
        assert(todoEl.querySelector('.block-to-do-children'));
        assert(todoEl.querySelector('.notion-block-children'));

        // Transclusion container test
        const transContainer = renderBlock({ type: 'transclusion_container', id: 'tc1' });
        assert(transContainer.classList.has('notion-synced-block'));
        assert(transContainer.querySelector('.notion-synced-badge'));
        assert(transContainer.querySelector('.notion-synced-body'));
        assert(transContainer.querySelector('.notion-block-children'));

        // Transclusion reference test
        const transRef = renderBlock({
          type: 'transclusion_reference',
          id: 'tr1',
          format: { copied_from_pointer: { id: 'tc1' } }
        });
        assert(transRef.classList.has('notion-synced-block'));
        assert.strictEqual(transRef.getAttribute('data-copied-from'), 'tc1');
        assert(transRef.querySelector('.notion-synced-badge'));
        assert(transRef.querySelector('.notion-synced-body'));

        // Media & Bookmark tests
        const videoEl = renderBlock({ type: 'video', id: 'vid1', properties: { source: [['https://example.com/v.mp4', []]] } });
        assert(videoEl.querySelector('video'));
        assert.strictEqual(videoEl.querySelector('video').getAttribute('src'), 'https://example.com/v.mp4');

        const audioEl = renderBlock({ type: 'audio', id: 'aud1', properties: { source: [['https://example.com/a.mp3', []]] } });
        assert(audioEl.querySelector('audio'));

        const fileEl = renderBlock({ type: 'file', id: 'fil1', properties: { source: [['https://example.com/doc.pdf', []]], title: [['Manual', []]], size: [['2 MB', []]] } });
        assert(fileEl.querySelector('.notion-file-link'));
        assert(fileEl.innerHTML.includes('Manual'));
        assert(fileEl.innerHTML.includes('2 MB'));

        const pdfEl = renderBlock({ type: 'pdf', id: 'pdf1', properties: { source: [['https://example.com/paper.pdf', []]] } });
        assert(pdfEl.querySelector('iframe'));

        const bkmkEl = renderBlock({ type: 'bookmark', id: 'bm1', properties: { link: [['https://notion.so', []]], title: [['Notion', []]] } });
        assert(bkmkEl.querySelector('.notion-bookmark-inner'));
        assert(bkmkEl.innerHTML.includes('https://notion.so'));

        console.log('SUCCESS_RENDER_BLOCK_ALL_TYPES');
        """
        out = self._run_node_script(node_script)
        self.assertIn('SUCCESS_RENDER_BLOCK_ALL_TYPES', out)

    def test_node_toggleable_headers(self):
        """Verifica que todos los tipos de encabezados soporten format.toggleable = true como <details>."""
        node_script = """
        const renderBlock = sandbox.renderBlock;

        const headerTypes = [
          { type: 'header', tag: 'H1' },
          { type: 'sub_header', tag: 'H2' },
          { type: 'sub_sub_header', tag: 'H3' },
          { type: 'header_4', tag: 'H4' }
        ];

        for (const h of headerTypes) {
          // 1. Non-toggleable: renders standard heading element
          const regularEl = renderBlock({
            type: h.type,
            id: 'reg-' + h.type,
            properties: { title: [['Titulo ' + h.type, []]] }
          });
          assert.strictEqual(regularEl.tagName, h.tag, 'Encabezado regular debe ser tag ' + h.tag);
          assert.strictEqual(regularEl.getAttribute('data-type'), h.type);
          assert.strictEqual(regularEl.getAttribute('contenteditable'), 'true');
          assert.strictEqual(regularEl.getAttribute('data-property'), 'title');
          assert(!regularEl.hasAttribute('data-toggleable'));

          // 2. Toggleable: renders <details> collapsible container
          const toggleEl = renderBlock({
            type: h.type,
            id: 'tog-' + h.type,
            properties: { title: [['Desplegable ' + h.type, []]] },
            format: { toggleable: true }
          });
          assert.strictEqual(toggleEl.tagName, 'DETAILS', 'Encabezado toggleable debe ser DETAILS');
          assert.strictEqual(toggleEl.getAttribute('data-type'), h.type);
          assert.strictEqual(toggleEl.getAttribute('data-toggleable'), 'true');
          assert(toggleEl.classList.has('block-header-toggle'));
          assert(toggleEl.classList.has('notion-block-toggle'));

          // Summary and arrow
          const summary = toggleEl.querySelector('summary');
          assert(summary, 'Toggleable header debe tener elemento summary');
          assert(summary.classList.has('notion-toggle-summary'));
          assert(summary.innerHTML.includes('▶'));

          // Inner title element with contenteditable
          const innerTitle = summary.querySelector(h.tag.toLowerCase());
          assert(innerTitle, 'Summary debe contener tag ' + h.tag.toLowerCase());
          assert.strictEqual(innerTitle.getAttribute('contenteditable'), 'true');
          assert.strictEqual(innerTitle.getAttribute('data-property'), 'title');
          assert(innerTitle.textContent.includes('Desplegable ' + h.type));

          // Child slot
          const childSlot = toggleEl.querySelector('.notion-block-children');
          assert(childSlot, 'Toggleable header debe contener .notion-block-children slot');
        }

        console.log('SUCCESS_TOGGLEABLE_HEADERS');
        """
        out = self._run_node_script(node_script)
        self.assertIn('SUCCESS_TOGGLEABLE_HEADERS', out)

    def test_node_to_do_block_interactive(self):
        """Verifica interactividad del bloque to_do: toggle de checkbox, completed y persistencia."""
        node_script = """
        const renderBlock = sandbox.renderBlock;

        let persistedUpdates = [];
        sandbox.persistBlockUpdate = function(id, updates) {
          persistedUpdates.push({ id, updates });
        };
        sandbox.state = {
          activeRecordMap: {
            block: {
              'td-test': {
                value: {
                  id: 'td-test',
                  type: 'to_do',
                  properties: { title: [['Hacer compras', []]], checked: [['No', []]] }
                }
              }
            }
          }
        };

        const todoEl = renderBlock({
          id: 'td-test',
          type: 'to_do',
          properties: { title: [['Hacer compras', []]], checked: [['No', []]] }
        });

        const chk = todoEl.querySelector('.notion-to-do-checkbox');
        const titleEl = todoEl.querySelector('.notion-to-do-title');
        assert(chk);
        assert(!chk.checked);
        assert(!titleEl.classList.has('completed'));

        // Simulate user checking the box
        chk.checked = true;
        chk.onchange();

        assert(titleEl.classList.has('completed'), 'Titulo debe tener clase completed tras check');
        assert.strictEqual(persistedUpdates.length, 1);
        assert.strictEqual(persistedUpdates[0].id, 'td-test');
        assert.strictEqual(persistedUpdates[0].updates.properties.checked[0][0], 'Yes');
        assert.strictEqual(sandbox.state.activeRecordMap.block['td-test'].value.properties.checked[0][0], 'Yes');

        // Simulate unchecking
        chk.checked = false;
        chk.onchange();
        assert(!titleEl.classList.has('completed'), 'Clase completed debe removerse tras uncheck');
        assert.strictEqual(persistedUpdates[1].updates.properties.checked[0][0], 'No');

        console.log('SUCCESS_TODO_INTERACTIVE');
        """
        out = self._run_node_script(node_script)
        self.assertIn('SUCCESS_TODO_INTERACTIVE', out)

    def test_node_synced_blocks_and_reference_mirroring(self):
        """Verifica que transclusion_reference renderice los hijos del transclusion_container destino."""
        node_script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const container = sandbox.document.createElement('div');

        const rmap = {
          block: {
            'page-1': {
              role: 'editor',
              value: {
                id: 'page-1',
                type: 'page',
                content: ['sync-ref-1'],
                alive: 1
              }
            },
            'sync-container-master': {
              role: 'editor',
              value: {
                id: 'sync-container-master',
                type: 'transclusion_container',
                content: ['child-text-1', 'child-text-2'],
                alive: 1
              }
            },
            'child-text-1': {
              role: 'editor',
              value: {
                id: 'child-text-1',
                type: 'text',
                properties: { title: [['Contenido sincronizado 1', []]] },
                parent_id: 'sync-container-master',
                alive: 1
              }
            },
            'child-text-2': {
              role: 'editor',
              value: {
                id: 'child-text-2',
                type: 'text',
                properties: { title: [['Contenido sincronizado 2', []]] },
                parent_id: 'sync-container-master',
                alive: 1
              }
            },
            'sync-ref-1': {
              role: 'editor',
              value: {
                id: 'sync-ref-1',
                type: 'transclusion_reference',
                format: {
                  copied_from_pointer: { id: 'sync-container-master' }
                },
                parent_id: 'page-1',
                alive: 1
              }
            }
          }
        };

        renderTreeFromRecordMap(rmap, 'page-1', container);

        // Container should have the sync-ref-1 block
        assert.strictEqual(container.children.length, 1);
        const refEl = container.children[0];
        assert.strictEqual(refEl.getAttribute('data-type'), 'transclusion_reference');
        assert.strictEqual(refEl.getAttribute('data-copied-from'), 'sync-container-master');

        // Reference block's synced slot should contain the 2 mirrored children!
        const syncedBody = refEl.querySelector('.notion-synced-body');
        assert(syncedBody, 'Debe contener .notion-synced-body');
        assert.strictEqual(syncedBody.children.length, 2, 'Los 2 hijos del master deben renderizarse dentro de la referencia');
        assert(syncedBody.innerHTML.includes('Contenido sincronizado 1'));
        assert(syncedBody.innerHTML.includes('Contenido sincronizado 2'));

        console.log('SUCCESS_SYNCED_MIRRORING');
        """
        out = self._run_node_script(node_script)
        self.assertIn('SUCCESS_SYNCED_MIRRORING', out)

    def test_node_render_tree_hierarchy_and_cycle_prevention(self):
        """Verifica renderTreeFromRecordMap montando jerarquías complejas y evitando ciclos."""
        node_script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        // Container
        const container = sandbox.document.createElement('div');

        // Construct RecordMap: Root page -> Column List -> 2 Columns -> Paragraphs
        const rmap = {
          block: {
            'root-page': {
              role: 'editor',
              value: {
                id: 'root-page',
                type: 'page',
                content: ['cl-1', 'div-1', 'deleted-blk', 'cycle-a'],
                alive: 1
              }
            },
            'cl-1': {
              role: 'editor',
              value: {
                id: 'cl-1',
                type: 'column_list',
                content: ['col-1', 'col-2'],
                parent_id: 'root-page',
                alive: 1
              }
            },
            'col-1': {
              role: 'editor',
              value: {
                id: 'col-1',
                type: 'column',
                format: { column_ratio: 0.5 },
                content: ['p-1'],
                parent_id: 'cl-1',
                alive: 1
              }
            },
            'p-1': {
              role: 'editor',
              value: {
                id: 'p-1',
                type: 'text',
                properties: { title: [['Columna Izquierda', []]] },
                parent_id: 'col-1',
                alive: 1
              }
            },
            'col-2': {
              role: 'editor',
              value: {
                id: 'col-2',
                type: 'column',
                format: { column_ratio: 0.5 },
                content: ['p-2'],
                parent_id: 'cl-1',
                alive: 1
              }
            },
            'p-2': {
              role: 'editor',
              value: {
                id: 'p-2',
                type: 'text',
                properties: { title: [['Columna Derecha', []]] },
                parent_id: 'col-2',
                alive: 1
              }
            },
            'div-1': {
              role: 'editor',
              value: {
                id: 'div-1',
                type: 'divider',
                parent_id: 'root-page',
                alive: 1
              }
            },
            'deleted-blk': {
              role: 'editor',
              value: {
                id: 'deleted-blk',
                type: 'text',
                properties: { title: [['Borrado', []]] },
                parent_id: 'root-page',
                alive: 0 // Soft-deleted
              }
            },
            // Circular reference: cycle-a -> cycle-b -> cycle-a
            'cycle-a': {
              role: 'editor',
              value: {
                id: 'cycle-a',
                type: 'text',
                properties: { title: [['Ciclo A', []]] },
                content: ['cycle-b'],
                parent_id: 'root-page',
                alive: 1
              }
            },
            'cycle-b': {
              role: 'editor',
              value: {
                id: 'cycle-b',
                type: 'text',
                properties: { title: [['Ciclo B', []]] },
                content: ['cycle-a'],
                parent_id: 'cycle-a',
                alive: 1
              }
            }
          }
        };

        // Render tree
        renderTreeFromRecordMap(rmap, 'root-page', container);

        // Verify structure
        assert.strictEqual(container.children.length, 3, 'Root debe tener column_list, divider y cycle-a');
        const colListEl = container.children[0];
        assert(colListEl.classList.has('block-column-list'));
        assert.strictEqual(colListEl.children.length, 2, 'column_list debe tener 2 columnas');

        // Verify column 1 content
        const col1Slot = colListEl.children[0].querySelector('.notion-column-content');
        assert(col1Slot, 'Columna 1 debe tener slot de hijos');
        assert(col1Slot.textContent.includes('Columna Izquierda'));

        // Verify soft-deleted block was NOT mounted
        assert(!container.innerHTML.includes('Borrado'), 'alive === 0 no debe renderizarse');

        // Verify cycle did not freeze execution (cycle-a has cycle-b, and terminates)
        assert(container.innerHTML.includes('Ciclo A'));
        assert(container.innerHTML.includes('Ciclo B'));

        console.log('SUCCESS_RENDER_TREE_HIERARCHY');
        """
        out = self._run_node_script(node_script)
        self.assertIn('SUCCESS_RENDER_TREE_HIERARCHY', out)


if __name__ == '__main__':
    unittest.main()
