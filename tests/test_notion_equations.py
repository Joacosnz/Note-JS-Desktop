#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_notion_equations.py — Pruebas Automatizadas de Ecuaciones Matemáticas Estilo Notion
Valida:
1. Bloques de ecuación dedicados (type: "equation", leaf node con content: null, properties.title, crdt_data).
2. Ecuaciones en línea con token semántico canónico "⁍" (U+204D) y decorador ["e", latex].
3. Conversión bidireccional fiel (HTML <-> Tuplas de Notion) en Python y JavaScript.
4. Soporte para sintaxis LaTeX completa de la universidad (cases, matrices, vectores, fracciones, conjuntos huecos).
5. Paquete offline de activos KaTeX en frontend/vendor/katex/ y tipos MIME en backend.py.
"""

import os
import sys
import json
import unittest
import subprocess

from models import init_db, db, Block, add_child_block, resolve_subtree_record_map
import rich_text
import backend

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestNotionEquations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        # Limpiar bloques creados para tests
        with db.atomic():
            Block.delete().where(Block.id.startswith('eq-test-')).execute()

    def tearDown(self):
        with db.atomic():
            Block.delete().where(Block.id.startswith('eq-test-')).execute()

    # -------------------------------------------------------------------------
    # 1. Bloques de Ecuación Dedicados (type: "equation")
    # -------------------------------------------------------------------------
    def test_dedicated_equation_block_schema_and_leaf_node(self):
        """Verifica que un bloque de ecuación sea un nodo hoja atómico sin hijos."""
        eq_latex = r"A^{-1} = \frac{1}{|A|} \cdot \text{adj}(A)"
        
        # Crear bloque raíz de página
        page = Block.create(
            id='eq-test-page-1',
            space_id='space-math',
            type='page',
            properties=json.dumps({'title': [['Página de Álgebra Lineal', []]]}),
            content='[]',
            parent_id=None,
            parent_table='space'
        )

        # Crear bloque de ecuación dedicado
        crdt_structure = {
            'title': {
                'r': 'test_user,"start","end"',
                'n': {
                    'test_user,"start","end"': {
                        's': {
                            'x': 'test_user',
                            'i': [
                                {'t': 's'},
                                {'t': 't', 'i': ['test_user', 1], 'o': 'start', 'l': len(eq_latex), 'c': eq_latex},
                                {'t': 'e'}
                            ],
                            'l': ''
                        },
                        'c': []
                    }
                }
            }
        }

        eq_block_data = {
            'id': 'eq-test-block-1',
            'space_id': 'space-math',
            'type': 'equation',
            'properties': {'title': [[eq_latex, []]]},
            'content': None,
            'format': {'metadata': {'math_engine': 'katex'}},
            'crdt_data': crdt_structure,
        }

        created = add_child_block(page.id, eq_block_data)
        self.assertIsNotNone(created)
        self.assertEqual(created.type, 'equation')
        self.assertEqual(created.parent_id, page.id)
        self.assertEqual(created.parent_table, 'block')

        # Verificar que la página padre contenga el ID del bloque de ecuación
        page_refreshed = Block.get_by_id(page.id)
        p_content = json.loads(page_refreshed.content)
        self.assertIn(created.id, p_content)

        # Verificar to_dict y subárbol BFS
        d = created.to_dict()
        self.assertEqual(d['type'], 'equation')
        self.assertEqual(d['properties']['title'][0][0], eq_latex)
        self.assertIn('title', d['crdt_data'])
        self.assertIn('test_user,"start","end"', d['crdt_data']['title']['r'])

        record_map = resolve_subtree_record_map(page.id)
        self.assertIn(created.id, record_map['block'])
        self.assertEqual(record_map['block'][created.id]['value']['type'], 'equation')

    # -------------------------------------------------------------------------
    # 2. Ecuaciones en Línea con Marcador Canónico "⁍" (U+204D)
    # -------------------------------------------------------------------------
    def test_inline_equation_canonical_token_and_tuple_decorator(self):
        """Verifica la serialización y deserialización del token ⁍ con decorador ["e", latex]."""
        # Caso real extraído de la base de datos de Notion
        formula = r"|\vec{x} \cdot \vec{y}| \leq \|\vec{x}\| \|\vec{y}\|"
        canonical_tuples = [
            ["⁍", [["e", formula]]]
        ]

        # 1. Plain text extraction
        plain = rich_text.rich_text_to_plain_text(canonical_tuples)
        self.assertEqual(plain, formula)

        # 2. Rich text to HTML
        html_out = rich_text.rich_text_to_html(canonical_tuples)
        self.assertIn('class="inline-equation notion-inline-equation"', html_out)
        self.assertIn(f'data-latex="{formula}"', html_out)

        # 3. HTML to Rich text roundtrip
        parsed = rich_text.html_to_rich_text(html_out)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0][0], '⁍')
        self.assertEqual(parsed[0][1], [['e', formula]])

    def test_mixed_text_and_multiple_inline_equations(self):
        """Verifica la segmentación combinada de texto y múltiples fórmulas matemáticas."""
        # Ejemplo: "Puntos (x, y) donde f(x, y) = c"
        notion_segments = [
            ["Puntos ", []],
            ["⁍", [["e", "(x, y)"]]],
            [" donde ", []],
            ["⁍", [["e", "f(x, y) = c"]]]
        ]

        # Texto plano extraído
        plain = rich_text.rich_text_to_plain_text(notion_segments)
        self.assertEqual(plain, "Puntos (x, y) donde f(x, y) = c")

        # HTML generado
        html_out = rich_text.rich_text_to_html(notion_segments)
        self.assertIn('Puntos ', html_out)
        self.assertIn('data-latex="(x, y)"', html_out)
        self.assertIn(' donde ', html_out)
        self.assertIn('data-latex="f(x, y) = c"', html_out)

        # Roundtrip a tuplas de Notion
        reconstructed = rich_text.html_to_rich_text(html_out)
        self.assertEqual(len(reconstructed), 4)
        self.assertEqual(reconstructed[0], ["Puntos ", []])
        self.assertEqual(reconstructed[1], ["⁍", [["e", "(x, y)"]]])
        self.assertEqual(reconstructed[2], [" donde ", []])
        self.assertEqual(reconstructed[3], ["⁍", [["e", "f(x, y) = c"]]])

    # -------------------------------------------------------------------------
    # 3. Soporte de Sintaxis Matemática Completa (Cases, Matrices, Vectores, etc.)
    # -------------------------------------------------------------------------
    def test_advanced_university_math_formulas(self):
        """Verifica que la sintaxis LaTeX de la universidad no se corrompa ni se escape incorrectamente."""
        formulas = [
            # 1. Sistemas de ecuaciones con \begin{cases}
            r"\begin{cases} 2x + 3y = 10 \\ 4x - 5y = -3 \end{cases}",
            # 2. Matrices con corchetes \begin{bmatrix}
            r"\begin{bmatrix} 1 & \frac{1}{k} & | 0 \\ 1 & k & | 1 \end{bmatrix}",
            # 3. Determinantes y matrices con paréntesis \begin{pmatrix}
            r"\det \begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc",
            # 4. Límites y fracciones
            r"\lim_{x \to 0} \frac{\sin x}{x} = 1",
            # 5. Vectores y normas
            r"\vec{x} \cdot \vec{y} = \|\vec{x}\| \|\vec{y}\| \cos(\theta)",
            # 6. Conjuntos con \mathbb{R}
            r"\mathbb{R}^n = \{ (x_1, \dots, x_n) : x_i \in \mathbb{R} \}"
        ]

        for f in formulas:
            tuples = [["⁍", [["e", f]]]]
            # Conversión a HTML
            h = rich_text.rich_text_to_html(tuples)
            # Reversión a tuplas
            back = rich_text.html_to_rich_text(h)
            self.assertEqual(back[0][0], '⁍')
            self.assertEqual(back[0][1][0][0], 'e')
            self.assertEqual(back[0][1][0][1], f)

    # -------------------------------------------------------------------------
    # 4. Activos KaTeX Offline Locales y MIME Types
    # -------------------------------------------------------------------------
    def test_offline_katex_assets_bundled(self):
        """Verifica que los activos de KaTeX existan localmente en frontend/vendor/katex/ para funcionamiento offline."""
        katex_dir = os.path.join(BASE_DIR, 'frontend', 'vendor', 'katex')
        self.assertTrue(os.path.isdir(katex_dir), "El directorio local frontend/vendor/katex debe existir")
        
        js_file = os.path.join(katex_dir, 'katex.min.js')
        css_file = os.path.join(katex_dir, 'katex.min.css')
        mhchem_file = os.path.join(katex_dir, 'contrib', 'mhchem.min.js')
        fonts_dir = os.path.join(katex_dir, 'fonts')

        self.assertTrue(os.path.isfile(js_file), "katex.min.js debe existir localmente")
        self.assertTrue(os.path.getsize(js_file) > 100000, "katex.min.js debe ser el archivo completo")
        self.assertTrue(os.path.isfile(css_file), "katex.min.css debe existir localmente")
        self.assertTrue(os.path.isfile(mhchem_file), "contrib/mhchem.min.js debe existir localmente")
        self.assertTrue(os.path.isdir(fonts_dir), "fonts/ de KaTeX debe existir localmente")

        # Verificar tipografías matemáticas
        main_font = os.path.join(fonts_dir, 'KaTeX_Main-Regular.woff2')
        math_font = os.path.join(fonts_dir, 'KaTeX_Math-Italic.woff2')
        self.assertTrue(os.path.isfile(main_font), "KaTeX_Main-Regular.woff2 debe existir")
        self.assertTrue(os.path.isfile(math_font), "KaTeX_Math-Italic.woff2 debe existir")

    # -------------------------------------------------------------------------
    # 5. Pruebas Dinámicas en Entorno Node.js VM (Frontend)
    # -------------------------------------------------------------------------
    def test_node_vm_equation_block_and_inline_rendering(self):
        """Ejecuta el código real de app.js en Node.js VM para validar el renderizado de ecuaciones."""
        app_js_path = os.path.join(BASE_DIR, 'frontend', 'app.js').replace('\\', '/')
        node_script = f"""
        const fs = require('fs');
        const vm = require('vm');
        const assert = require('assert');

        class MockClassList {{
          constructor() {{ this._set = new Set(); }}
          add(...tokens) {{ tokens.forEach(t => this._set.add(String(t))); }}
          remove(...tokens) {{ tokens.forEach(t => this._set.delete(String(t))); }}
          contains(t) {{ return this._set.has(String(t)); }}
          has(t) {{ return this._set.has(String(t)); }}
          toString() {{ return Array.from(this._set).join(' '); }}
        }}

        class MockElement {{
          constructor(tag) {{
            this.tagName = tag.toUpperCase();
            this.attributes = {{}};
            this.style = {{}};
            this.classList = new MockClassList();
            this.id = '';
            this.childNodes = [];
          }}
          setAttribute(k, v) {{
            this.attributes[k] = String(v);
            if (k === 'id') this.id = String(v);
            if (k === 'class') this.classList = new MockClassList();
          }}
          getAttribute(k) {{ return this.attributes[k] !== undefined ? this.attributes[k] : null; }}
          hasAttribute(k) {{ return this.attributes[k] !== undefined; }}
          removeAttribute(k) {{ delete this.attributes[k]; }}
          get className() {{ return this.classList.toString(); }}
          set className(v) {{
            this.classList = new MockClassList();
            if (v) String(v).split(/\\s+/).forEach(c => this.classList.add(c));
          }}
          appendChild(c) {{ this.childNodes.push(c); return c; }}
          querySelector(sel) {{
            const cls = sel.startsWith('.') ? sel.slice(1) : sel;
            if (this.classList.contains(cls)) return this;
            for (const c of this.childNodes) {{
              if (c.querySelector) {{
                const res = c.querySelector(sel);
                if (res) return res;
              }}
            }}
            return null;
          }}
          querySelectorAll(sel) {{
            const res = [];
            const cls = sel.startsWith('.') ? sel.slice(1) : sel;
            if (this.classList.contains(cls)) res.push(this);
            for (const c of this.childNodes) {{
              if (c.querySelectorAll) res.push(...c.querySelectorAll(sel));
            }}
            return res;
          }}
          set innerHTML(html) {{
            this._innerHTML = html;
            this.childNodes = [];
            if (html.includes('notion-equation-display')) {{
              const d = new MockElement('div');
              d.className = 'notion-equation-display block-equation-display';
              d.setAttribute('data-latex', 'test-latex');
              this.childNodes.push(d);
            }}
            if (html.includes('notion-equation-popover')) {{
              const p = new MockElement('div');
              p.className = 'notion-equation-popover block-equation-popover';
              const inp = new MockElement('textarea');
              inp.className = 'notion-equation-input notion-equation-textarea';
              p.childNodes.push(inp);
              this.childNodes.push(p);
            }}
          }}
          get innerHTML() {{ return this._innerHTML || ''; }}
        }}

        const mockKatex = {{
          render: function(tex, el, opts) {{
            el.innerHTML = '<span class="katex-rendered">' + tex + '</span>';
          }}
        }};

        const mockDoc = {{
          createElement: (t) => new MockElement(t),
          getElementById: () => null,
          querySelector: () => null,
          querySelectorAll: () => [],
          addEventListener: () => {{}},
          removeEventListener: () => {{}},
          body: new MockElement('body')
        }};

        const sandbox = {{
          Node: {{ ELEMENT_NODE: 1, TEXT_NODE: 3 }},
          window: null,
          document: mockDoc,
          navigator: {{ clipboard: {{ writeText: () => Promise.resolve() }} }},
          localStorage: {{ getItem: () => null, setItem: () => {{}}, removeItem: () => {{}} }},
          setTimeout: () => {{}},
          clearTimeout: () => {{}},
          setInterval: () => {{}},
          clearInterval: () => {{}},
          addEventListener: () => {{}},
          removeEventListener: () => {{}},
          state: {{ activeNoteId: 'n1', activeRecordMap: {{ block: {{}} }} }},
          katex: mockKatex,
          console: console
        }};
        sandbox.window = sandbox;
        sandbox.global = sandbox;

        const appCode = fs.readFileSync('{app_js_path}', 'utf8');
        vm.runInNewContext(appCode, sandbox);

        // 1. Validar buildEquationCrdt
        const crdt = sandbox.buildEquationCrdt('E = mc^2', 2, 'user_42');
        assert(crdt.title, 'crdt.title debe existir');
        assert(crdt.title.r.includes('user_42'), 'clock debe contener client_id');
        assert.strictEqual(crdt.title.n[crdt.title.r].s.i[1].c, 'E = mc^2');

        // 2. Validar parseRichTextToHtml con token ⁍
        const html = sandbox.parseRichTextToHtml([
          ['Puntos ', []],
          ['⁍', [['e', '(x, y)']]],
          [' fin', []]
        ]);
        assert(html.includes('inline-equation'), 'Debe incluir clase inline-equation');
        assert(html.includes('data-latex="(x, y)"'), 'Debe incluir data-latex');
        assert(html.includes('Puntos '), 'Debe incluir prefijo');
        assert(html.includes(' fin'), 'Debe incluir sufijo');

        // 3. Validar renderBlock para ecuación
        const eqBlock = {{
          id: 'b-eq-1',
          type: 'equation',
          properties: {{ title: [['\\\\int_0^1 x dx', []]] }}
        }};
        const el = sandbox.renderBlock(eqBlock);
        assert.strictEqual(el.getAttribute('data-type'), 'equation');
        assert(el.querySelector('.notion-equation-display'), 'Debe tener notion-equation-display');
        assert(el.querySelector('.notion-equation-input'), 'Debe tener notion-equation-input');

        console.log('SUCCESS_VM_EQUATIONS');
        """

        p = subprocess.run(['node', '-e', node_script], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, f"Error en Node VM: {p.stderr}")
        self.assertIn("SUCCESS_VM_EQUATIONS", p.stdout)


if __name__ == '__main__':
    unittest.main()
