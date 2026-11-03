#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_milestone2_adversarial_challenge.py
Adversarial Challenge & Stress Verification Suite for Milestone 2:
Frontend DOM, 30 Block Types, Toggleable Headers, Synced Transclusion, and Media Embeds.

Written by Challenger 1 (Empirical Challenger) to stress-test:
1. All 30 block types under canonical and null/empty inputs.
2. Toggleable headers (h1-h4) with summary, arrow, contenteditable title, and nested children.
3. Synced block transclusion (transclusion_container, transclusion_reference, mirroring, unsync).
4. Media embeds (video, audio, file, pdf, bookmark) DOM structure, controls, and XSS safety.
5. Interactive to-do checkbox toggling, completed class, and state persistence.
6. Container block hierarchy mounting in renderTreeFromRecordMap.
"""

import os
import json
import subprocess
import unittest

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_JS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'app.js')
STYLES_CSS_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'styles.css')

ALL_30_NOTION_BLOCK_TYPES = [
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


class TestMilestone2AdversarialChallenge(unittest.TestCase):
    """Empirical adversarial test suite for Milestone 2."""

    @classmethod
    def setUpClass(cls):
        try:
            res = subprocess.run(['node', '-v'], capture_output=True, text=True, check=True)
            cls.node_available = True
            cls.node_version = res.stdout.strip()
        except Exception:
            cls.node_available = False

        with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
            cls.app_js = f.read()
        with open(STYLES_CSS_PATH, 'r', encoding='utf-8') as f:
            cls.styles_css = f.read()

    def _run_node_script(self, script_code):
        if not self.node_available:
            self.skipTest("Node.js is not available in this environment")

        runner_code = f"""
const fs = require('fs');
const vm = require('vm');

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
      // Tag with class e.g. a.notion-file-link
      if (part.includes('.')) {{
        const [t, ...classes] = part.split('.');
        const tagMatch = !t || el.tagName.toLowerCase() === t.toLowerCase();
        const classMatch = classes.every(c => el.classList.has(c));
        return tagMatch && classMatch;
      }}
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

    def test_all_30_block_types_rendered_with_canonical_metadata(self):
        """Verifica que los 30 tipos de bloques generen elementos DOM con dataset y atributos canónicos."""
        script = f"""
        const renderBlock = sandbox.renderBlock;
        const types = {json.dumps(ALL_30_NOTION_BLOCK_TYPES)};

        assert.strictEqual(types.length, 30, 'Debe haber exactamente 30 tipos de bloques en el catalogo');

        for (const t of types) {{
          const block = {{
            id: 'blk-' + t,
            type: t,
            properties: {{
              title: [['Texto de prueba ' + t, []]],
              source: [['https://example.com/asset', []]],
              link: [['https://example.com', []]],
              caption: [['Pie de foto', []]],
              language: [['python', []]],
              checked: [['Yes', []]],
              size: [['1.5 MB', []]],
              page_id: 'note-target'
            }},
            format: {{
              column_ratio: 0.5,
              block_color: 'blue',
              page_icon: '🌟',
              copied_from_pointer: {{ id: 'master-block-1' }}
            }}
          }};

          const el = renderBlock(block);
          assert(el, 'renderBlock retorno null o undefined para el tipo: ' + t);
          assert.strictEqual(el.nodeType, 1, 'Debe retornar un MockElement (nodeType=1) para ' + t);
          assert.strictEqual(el.getAttribute('data-type'), t, 'data-type incorrecto para ' + t);
          assert(el.getAttribute('data-block-id'), 'data-block-id ausente para ' + t);
        }}
        console.log('ALL_30_TYPES_SUCCESS');
        """
        out = self._run_node_script(script)
        self.assertIn('ALL_30_TYPES_SUCCESS', out)

    def test_resilience_to_null_undefined_and_empty_payloads(self):
        """Prueba de robustez: renderBlock no debe lanzar excepciones ante bloques vacíos o con propiedades nulas."""
        script = f"""
        const renderBlock = sandbox.renderBlock;
        const types = {json.dumps(ALL_30_NOTION_BLOCK_TYPES)};

        // 1. Invalid input guards
        assert.strictEqual(renderBlock(null), null);
        assert.strictEqual(renderBlock(undefined), null);
        assert.strictEqual(renderBlock({{}}), null);
        assert.strictEqual(renderBlock({{ id: 'bad' }}), null);

        // 2. Minimal valid payload (only type and id)
        for (const t of types) {{
          const minimalBlock = {{ type: t, id: 'min-' + t }};
          const el1 = renderBlock(minimalBlock);
          assert(el1, 'Fallo con bloque minimo para tipo: ' + t);
          assert.strictEqual(el1.getAttribute('data-type'), t);

          // 3. Explicit nulls in properties and format
          const nullsBlock = {{ type: t, id: 'nulls-' + t, properties: null, format: null }};
          const el2 = renderBlock(nullsBlock);
          assert(el2, 'Fallo con properties y format nulos para tipo: ' + t);
        }}
        console.log('RESILIENCE_ALL_PASSED');
        """
        out = self._run_node_script(script)
        self.assertIn('RESILIENCE_ALL_PASSED', out)

    def test_toggleable_headers_contract_and_hierarchy(self):
        """Verifica que h1, h2, h3, h4 soporten toggleable (summary, arrow, child slot) y no-toggleable."""
        script = """
        const renderBlock = sandbox.renderBlock;
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const headers = [
          { type: 'header', tag: 'H1', titleClass: 'block-header-toggle-title' },
          { type: 'sub_header', tag: 'H2', titleClass: 'block-header-toggle-title' },
          { type: 'sub_sub_header', tag: 'H3', titleClass: 'block-header-toggle-title' },
          { type: 'header_4', tag: 'H4', titleClass: 'block-header-4-title' }
        ];

        for (const h of headers) {
          // A. Non-toggleable header
          const reg = renderBlock({
            type: h.type,
            id: 'reg-' + h.type,
            properties: { title: [['Titulo Simple ' + h.type, []]] }
          });
          assert.strictEqual(reg.tagName, h.tag, 'Encabezado no toggleable debe ser tag ' + h.tag);
          assert.strictEqual(reg.getAttribute('contenteditable'), 'true');
          assert.strictEqual(reg.getAttribute('data-property'), 'title');
          assert(!reg.querySelector('summary'), 'No debe tener summary');

          // B. Toggleable header (<details>)
          const tog = renderBlock({
            type: h.type,
            id: 'tog-' + h.type,
            properties: { title: [['Titulo Desplegable ' + h.type, []]] },
            format: { toggleable: true }
          });
          assert.strictEqual(tog.tagName, 'DETAILS', 'Toggleable header debe ser DETAILS');
          assert.strictEqual(tog.getAttribute('data-toggleable'), 'true');
          assert(tog.classList.has('block-header-toggle'));
          assert(tog.classList.has('notion-block-toggle'));

          // Summary verification
          const summary = tog.querySelector('summary');
          assert(summary, 'Debe contener summary');
          assert(summary.classList.has('notion-toggle-summary'));

          // Arrow indicator
          const arrow = summary.querySelector('.notion-toggle-arrow');
          assert(arrow, 'Debe contener flecha .notion-toggle-arrow');
          assert.strictEqual(arrow.textContent.trim(), '▶');

          // Heading tag inside summary
          const innerH = summary.querySelector(h.tag.toLowerCase());
          assert(innerH, 'Summary debe contener el elemento ' + h.tag);
          assert.strictEqual(innerH.getAttribute('contenteditable'), 'true');
          assert.strictEqual(innerH.getAttribute('data-property'), 'title');
          assert(innerH.textContent.includes('Titulo Desplegable ' + h.type));

          // Child container slot
          const childSlot = tog.querySelector('.notion-block-children');
          assert(childSlot, 'Debe contener slot .notion-block-children');
        }

        // C. Tree Mounting: Test children mounting into toggleable headers
        for (const h of headers) {
          const rmap = {
            block: {
              'root': { value: { id: 'root', type: 'page', content: ['h-block'], alive: 1 } },
              'h-block': {
                value: {
                  id: 'h-block',
                  type: h.type,
                  properties: { title: [['Seccion ' + h.type, []]] },
                  format: { toggleable: true },
                  content: ['nested-1', 'nested-2'],
                  alive: 1
                }
              },
              'nested-1': {
                value: {
                  id: 'nested-1',
                  type: 'text',
                  properties: { title: [['Hijo Uno', []]] },
                  alive: 1
                }
              },
              'nested-2': {
                value: {
                  id: 'nested-2',
                  type: 'text',
                  properties: { title: [['Hijo Dos', []]] },
                  alive: 1
                }
              }
            }
          };

          const container = sandbox.document.createElement('div');
          renderTreeFromRecordMap(rmap, 'root', container);
          assert.strictEqual(container.children.length, 1);
          const mountedTog = container.children[0];
          assert.strictEqual(mountedTog.tagName, 'DETAILS');
          const slot = mountedTog.querySelector('.notion-block-children');
          assert.strictEqual(slot.children.length, 2, 'Los 2 hijos deben estar dentro del slot del toggleable header ' + h.type);
          assert(slot.textContent.includes('Hijo Uno'));
          assert(slot.textContent.includes('Hijo Dos'));
        }

        console.log('TOGGLEABLE_HEADERS_VERIFIED');
        """
        out = self._run_node_script(script)
        self.assertIn('TOGGLEABLE_HEADERS_VERIFIED', out)

    def test_media_embeds_dom_structure_and_xss_protection(self):
        """Verifica la estructura DOM de video, audio, file, pdf, bookmark y escape de HTML."""
        script = """
        const renderBlock = sandbox.renderBlock;

        // 1. VIDEO
        const vid = renderBlock({
          type: 'video',
          id: 'vid-1',
          properties: {
            source: [['https://media.example.com/stream.mp4', []]],
            caption: [['Demostracion de video', []]]
          }
        });
        assert.strictEqual(vid.tagName, 'DIV');
        assert(vid.classList.has('block-video'));
        const vEl = vid.querySelector('video');
        assert(vEl, 'Elemento video debe existir');
        assert.strictEqual(vEl.getAttribute('src'), 'https://media.example.com/stream.mp4');
        assert(vEl.hasAttribute('controls'));
        const vCap = vid.querySelector('.block-video-caption');
        assert(vCap);
        assert.strictEqual(vCap.getAttribute('contenteditable'), 'true');
        assert.strictEqual(vCap.getAttribute('data-property'), 'caption');

        // 2. AUDIO
        const aud = renderBlock({
          type: 'audio',
          id: 'aud-1',
          properties: {
            source: [['https://media.example.com/podcast.mp3', []]],
            title: [['Episodio 1', []]]
          }
        });
        assert.strictEqual(aud.tagName, 'DIV');
        assert(aud.classList.has('block-audio'));
        const aEl = aud.querySelector('audio');
        assert(aEl, 'Elemento audio debe existir');
        assert.strictEqual(aEl.getAttribute('src'), 'https://media.example.com/podcast.mp3');
        assert(aEl.hasAttribute('controls'));
        const aTitle = aud.querySelector('.block-audio-title');
        assert(aTitle);
        assert.strictEqual(aTitle.getAttribute('contenteditable'), 'true');
        assert.strictEqual(aTitle.getAttribute('data-property'), 'title');

        // 3. FILE
        const fil = renderBlock({
          type: 'file',
          id: 'fil-1',
          properties: {
            source: [['https://files.example.com/archive.zip', []]],
            title: [['Codigo Fuente.zip', []]],
            size: [['12.4 MB', []]]
          }
        });
        assert.strictEqual(fil.tagName, 'DIV');
        assert(fil.classList.has('block-file'));
        const fLink = fil.querySelector('a');
        assert(fLink);
        assert.strictEqual(fLink.getAttribute('href'), 'https://files.example.com/archive.zip');
        assert.strictEqual(fLink.getAttribute('target'), '_blank');
        assert(fil.innerHTML.includes('Codigo Fuente.zip'));
        assert(fil.innerHTML.includes('12.4 MB'));

        // 4. PDF
        const pdf = renderBlock({
          type: 'pdf',
          id: 'pdf-1',
          properties: {
            source: [['https://documents.example.com/spec.pdf', []]]
          }
        });
        assert.strictEqual(pdf.tagName, 'DIV');
        assert(pdf.classList.has('block-pdf'));
        const ifr = pdf.querySelector('iframe');
        assert(ifr);
        const viewerUrl = ifr.getAttribute('src').replace(/&amp;/g, '&');
        assert(viewerUrl.startsWith('/pdf-viewer.html?'));
        assert.strictEqual(new URL(viewerUrl, 'http://localhost').searchParams.get('src'), 'https://documents.example.com/spec.pdf');
        assert.strictEqual(pdf.getAttribute('data-source'), 'https://documents.example.com/spec.pdf');

        // 5. BOOKMARK
        const bkm = renderBlock({
          type: 'bookmark',
          id: 'bkm-1',
          properties: {
            link: [['https://notion.so', []]],
            title: [['Notion Workspace', []]],
            description: [['All in one workspace', []]]
          }
        });
        assert.strictEqual(bkm.tagName, 'DIV');
        assert(bkm.classList.has('block-bookmark'));
        const bLink = bkm.querySelector('a');
        assert(bLink);
        assert.strictEqual(bLink.getAttribute('href'), 'https://notion.so');
        assert.strictEqual(bLink.getAttribute('target'), '_blank');
        const bTitle = bkm.querySelector('.notion-bookmark-title');
        assert(bTitle);
        assert.strictEqual(bTitle.getAttribute('data-property'), 'title');
        const bDesc = bkm.querySelector('.notion-bookmark-desc');
        assert(bDesc);
        assert.strictEqual(bDesc.getAttribute('data-property'), 'description');
        assert(bkm.innerHTML.includes('https://notion.so'));

        // 6. XSS Injection Stress Test
        const xssPayload = '"><img src=x onerror=alert(1)>';
        const xssBlock = renderBlock({
          type: 'video',
          id: 'xss-v',
          properties: {
            source: [[xssPayload, []]],
            caption: [[xssPayload, []]]
          }
        });
        assert(!xssBlock.innerHTML.includes('<img src=x'), 'HTML debe ser escapado contra inyecciones XSS');

        console.log('MEDIA_EMBEDS_VERIFIED');
        """
        out = self._run_node_script(script)
        self.assertIn('MEDIA_EMBEDS_VERIFIED', out)

    def test_defect_unsync_block_instance_is_shadowed_by_legacy_function(self):
        """DEFECT 1: Verifica si unsyncBlockInstance está sobreescrita por la función legacy de la línea 15498."""
        script = """
        const unsyncFn = sandbox.unsyncBlockInstance;
        assert(unsyncFn, 'unsyncBlockInstance debe estar definido en sandbox/window');
        const fnStr = unsyncFn.toString();

        // El worker de M2 declaró que unsyncBlockInstance convierte el bloque a texto usando convertBlockType(blockId, 'text').
        // Sin embargo, debido a hoisting de JS, la función de la línea 15498 sobrescribe la de la línea 7666.
        assert(fnStr.includes('convertBlockType'),
          'DEFECT CONFIRMED: unsyncBlockInstance no invoca convertBlockType porque fue sobrescrita por la función legacy de la línea 15498. Código activo: ' + fnStr
        );

        console.log('UNSYNC_CONTRACT_VALID');
        """
        out = self._run_node_script(script)
        self.assertIn('UNSYNC_CONTRACT_VALID', out)

    def test_synced_block_mirroring_from_record_map(self):
        """Verifica transclusion_reference resolviendo el container y montando los hijos cuando el master no está en la página."""
        script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const rmap = {
          block: {
            'page-root': {
              value: {
                id: 'page-root',
                type: 'page',
                content: ['sync-ref-instance'],
                alive: 1
              }
            },
            'master-container': {
              value: {
                id: 'master-container',
                type: 'transclusion_container',
                content: ['synced-child-a', 'synced-child-b'],
                alive: 1
              }
            },
            'synced-child-a': {
              value: {
                id: 'synced-child-a',
                type: 'text',
                properties: { title: [['Primer parrafo compartido', []]] },
                alive: 1
              }
            },
            'synced-child-b': {
              value: {
                id: 'synced-child-b',
                type: 'quote',
                properties: { title: [['Cita compartida sincronizada', []]] },
                alive: 1
              }
            },
            'sync-ref-instance': {
              value: {
                id: 'sync-ref-instance',
                type: 'transclusion_reference',
                format: {
                  copied_from_pointer: { id: 'master-container' }
                },
                alive: 1
              }
            }
          }
        };

        const target = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'page-root', target);

        assert.strictEqual(target.children.length, 1);
        const refEl = target.children[0];
        assert.strictEqual(refEl.getAttribute('data-type'), 'transclusion_reference');
        assert.strictEqual(refEl.getAttribute('data-copied-from'), 'master-container');

        const body = refEl.querySelector('.notion-synced-body');
        assert(body, 'Debe existir .notion-synced-body');
        assert.strictEqual(body.children.length, 2, 'Los 2 hijos del master deben renderizarse dentro de la referencia');
        assert(body.textContent.includes('Primer parrafo compartido'));
        assert(body.textContent.includes('Cita compartida sincronizada'));

        console.log('SYNCED_MIRRORING_VERIFIED');
        """
        out = self._run_node_script(script)
        self.assertIn('SYNCED_MIRRORING_VERIFIED', out)

    def test_defect_dead_synced_container_children_resurrected(self):
        """DEFECT 2: Verifica que transclusion_reference hacia un contenedor eliminado (alive: 0) no monte sus hijos."""
        script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const rmap = {
          block: {
            'page-root': {
              value: {
                id: 'page-root',
                type: 'page',
                content: ['ref-dead-target'],
                alive: 1
              }
            },
            'ref-dead-target': {
              value: {
                id: 'ref-dead-target',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'dead-container' } },
                alive: 1
              }
            },
            'dead-container': {
              value: {
                id: 'dead-container',
                type: 'transclusion_container',
                content: ['dead-child'],
                alive: 0 // Soft-deleted master container!
              }
            },
            'dead-child': {
              value: {
                id: 'dead-child',
                type: 'text',
                properties: { title: [['Texto que debe permanecer oculto', []]] },
                alive: 1
              }
            }
          }
        };

        const target = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'page-root', target);

        assert.strictEqual(target.children.length, 1, 'La referencia debe montarse');
        const refBody = target.children[0].querySelector('.notion-synced-body');
        assert(refBody, 'Debe existir el contenedor del cuerpo');
        assert(!target.innerHTML.includes('Texto que debe permanecer oculto'),
          'DEFECT CONFIRMED: renderTreeFromRecordMap no verifica targetBlock.alive !== 0 y resucita hijos de contenedores eliminados!'
        );

        console.log('DEAD_SYNCED_REFERENCES_HANDLED');
        """
        out = self._run_node_script(script)
        self.assertIn('DEAD_SYNCED_REFERENCES_HANDLED', out)

    def test_defect_same_page_synced_mirroring_drops_children(self):
        """DEFECT 3: Verifica que master y referencia en la misma página rendericen ambos sus hijos."""
        script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const rmap = {
          block: {
            'page-1': {
              value: {
                id: 'page-1',
                type: 'page',
                content: ['sync-master', 'sync-ref'],
                alive: 1
              }
            },
            'sync-master': {
              value: {
                id: 'sync-master',
                type: 'transclusion_container',
                content: ['shared-child'],
                alive: 1
              }
            },
            'shared-child': {
              value: {
                id: 'shared-child',
                type: 'text',
                properties: { title: [['Contenido sincronizado', []]] },
                parent_id: 'sync-master',
                alive: 1
              }
            },
            'sync-ref': {
              value: {
                id: 'sync-ref',
                type: 'transclusion_reference',
                format: { copied_from_pointer: { id: 'sync-master' } },
                alive: 1
              }
            }
          }
        };

        const container = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'page-1', container);
        assert.strictEqual(container.children.length, 2);

        const masterEl = container.children[0];
        const refEl = container.children[1];
        const masterBody = masterEl.querySelector('.notion-synced-body');
        const refBody = refEl.querySelector('.notion-synced-body');

        assert.strictEqual(masterBody.children.length, 1, 'Master debe tener su hijo renderizado');
        assert.strictEqual(refBody.children.length, 1,
          'DEFECT CONFIRMED: refBody tiene 0 hijos porque el conjunto global visited descarta childIds ya visitados en la misma página'
        );

        console.log('SAME_PAGE_SYNCED_MIRRORING_PASSED');
        """
        out = self._run_node_script(script)
        self.assertIn('SAME_PAGE_SYNCED_MIRRORING_PASSED', out)

    def test_to_do_checkbox_interaction_and_persistence(self):
        """Verifica interactividad de to_do: checkbox onchange, clase completed y llamadas a persistBlockUpdate."""
        script = """
        const renderBlock = sandbox.renderBlock;

        const persistedCalls = [];
        sandbox.persistBlockUpdate = function(id, patch) {
          persistedCalls.push({ id, patch });
        };
        sandbox.window.persistBlockUpdate = sandbox.persistBlockUpdate;

        sandbox.state = {
          activeRecordMap: {
            block: {
              'todo-test-1': {
                value: {
                  id: 'todo-test-1',
                  type: 'to_do',
                  properties: { title: [['Comprar cafe', []]], checked: [['No', []]] }
                }
              }
            }
          }
        };
        sandbox.window.state = sandbox.state;

        const todoEl = renderBlock(sandbox.state.activeRecordMap.block['todo-test-1'].value);
        assert(todoEl.classList.has('block-to-do'));

        const chk = todoEl.querySelector('.notion-to-do-checkbox');
        const titleEl = todoEl.querySelector('.notion-to-do-title');
        assert(chk);
        assert(!chk.checked);
        assert(!titleEl.classList.has('completed'));

        // Check action
        chk.checked = true;
        chk.onchange();
        assert(titleEl.classList.has('completed'), 'Debe agregar clase completed');
        assert.strictEqual(persistedCalls.length, 1);
        assert.strictEqual(persistedCalls[0].patch.properties.checked[0][0], 'Yes');

        // Uncheck action
        chk.checked = false;
        chk.onchange();
        assert(!titleEl.classList.has('completed'), 'Debe quitar clase completed');
        assert.strictEqual(persistedCalls.length, 2);
        assert.strictEqual(persistedCalls[1].patch.properties.checked[0][0], 'No');

        console.log('TODO_INTERACTION_VERIFIED');
        """
        out = self._run_node_script(script)
        self.assertIn('TODO_INTERACTION_VERIFIED', out)

    def test_quote_and_callout_containers_with_children(self):
        """Verifica que quote y callout sean contenedores que monten hijos en renderTreeFromRecordMap."""
        script = """
        const renderTreeFromRecordMap = sandbox.renderTreeFromRecordMap;

        const rmap = {
          block: {
            'root': {
              value: { id: 'root', type: 'page', content: ['q-1', 'co-1'], alive: 1 }
            },
            'q-1': {
              value: {
                id: 'q-1',
                type: 'quote',
                properties: { title: [['La sabiduria comienza en la reflexion', []]] },
                content: ['q-child'],
                alive: 1
              }
            },
            'q-child': {
              value: {
                id: 'q-child',
                type: 'text',
                properties: { title: [['- Filosofo Anonimo', []]] },
                alive: 1
              }
            },
            'co-1': {
              value: {
                id: 'co-1',
                type: 'callout',
                properties: { title: [['Advertencia importante', []]] },
                format: { page_icon: '⚠️', block_color: 'yellow_background' },
                content: ['co-child'],
                alive: 1
              }
            },
            'co-child': {
              value: {
                id: 'co-child',
                type: 'text',
                properties: { title: [['Detalle de la advertencia', []]] },
                alive: 1
              }
            }
          }
        };

        const target = sandbox.document.createElement('div');
        renderTreeFromRecordMap(rmap, 'root', target);

        assert.strictEqual(target.children.length, 2);
        const qEl = target.children[0];
        assert.strictEqual(qEl.tagName, 'BLOCKQUOTE');
        const qSlot = qEl.querySelector('.block-quote-children');
        assert(qSlot, 'Quote debe tener .block-quote-children');
        assert.strictEqual(qSlot.children.length, 1);
        assert(qSlot.textContent.includes('- Filosofo Anonimo'));

        const coEl = target.children[1];
        assert(coEl.classList.has('block-callout'));
        assert(coEl.classList.has('notion-color-yellow_background'));
        assert(coEl.innerHTML.includes('⚠️'));
        const coSlot = coEl.querySelector('.block-callout-children');
        assert(coSlot, 'Callout debe tener .block-callout-children');
        assert.strictEqual(coSlot.children.length, 1);
        assert(coSlot.textContent.includes('Detalle de la advertencia'));

        console.log('QUOTE_AND_CALLOUT_CONTAINERS_VERIFIED');
        """
        out = self._run_node_script(script)
        self.assertIn('QUOTE_AND_CALLOUT_CONTAINERS_VERIFIED', out)

    def test_css_rules_exist_for_all_extended_blocks(self):
        """Verifica que styles.css defina estilos para todos los 11 tipos extendidos y modificadores."""
        required_classes = [
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
        for rc in required_classes:
            self.assertIn(rc, self.styles_css, f"Clase CSS requerida ausente en styles.css: {rc}")


if __name__ == '__main__':
    unittest.main()
