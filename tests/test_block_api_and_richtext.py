#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_block_api_and_richtext.py
Test suite automatizada completa para Milestone 2:
- Motor de Rich Text en Python puro (rich_text.py): tuplas, HTML, texto plano, sanitización, decoradores.
- Esquemas canónicos y validación para los 17 tipos de bloques de Notion + sub_page.
- Endpoints HTTP REST en backend.py (/api/blocks, /recordMap, /reorder, /restore, /rich-text/convert).
- Desambiguación de rutas reservadas (/api/blocks/order, /api/blocks/batch).
- Métodos nativos de PyWebViewBridge en desktop_app.py.
"""

import os
import json
import time
import socket
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from peewee import SqliteDatabase

import models
import backend
import rich_text
import desktop_app


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


class TestRichTextEngine(unittest.TestCase):
    """Pruebas del motor puro de rich text en rich_text.py."""

    def test_plain_text_to_rich_text(self):
        self.assertEqual(rich_text.plain_text_to_rich_text(None), [])
        self.assertEqual(rich_text.plain_text_to_rich_text(""), [])
        self.assertEqual(rich_text.plain_text_to_rich_text("Hola"), [["Hola", []]])

    def test_rich_text_to_plain_text(self):
        self.assertEqual(rich_text.rich_text_to_plain_text(None), "")
        self.assertEqual(rich_text.rich_text_to_plain_text(""), "")
        self.assertEqual(rich_text.rich_text_to_plain_text("Texto directo"), "Texto directo")
        tuples = [
            ["Hola ", [["b"]]],
            ["Mundo ", [["i"]]],
            ["!", []],
        ]
        self.assertEqual(rich_text.rich_text_to_plain_text(tuples), "Hola Mundo !")

    def test_all_eight_decorators_to_html(self):
        tuples = [
            ["Negrita", [["b"]]],
            [" Cursiva", [["i"]]],
            [" Subrayado", [["_"]]],
            [" Tachado", [["s"]]],
            [" Codigo", [["c"]]],
            [" Resaltado", [["h", "yellow_background"]]],
            [" ColorTexto", [["h", "blue"]]],
            [" Enlace", [["a", "https://example.com/test"]]],
            ["E=mc^2", [["e", "E=mc^2"]]],
        ]
        html_out = rich_text.rich_text_to_html(tuples)

        self.assertIn("<strong>Negrita</strong>", html_out)
        self.assertIn("<em> Cursiva</em>", html_out)
        self.assertIn("<u> Subrayado</u>", html_out)
        self.assertIn("<s> Tachado</s>", html_out)
        self.assertIn("<code> Codigo</code>", html_out)
        self.assertIn('background-color: yellow;', html_out)
        self.assertIn('notion-color-yellow_background', html_out)
        self.assertIn('color: blue;', html_out)
        self.assertIn('notion-color-blue', html_out)
        self.assertIn('href="https://example.com/test"', html_out)
        self.assertIn('class="inline-equation notion-inline-equation"', html_out)
        self.assertIn('data-latex="E=mc^2"', html_out)

    def test_html_to_rich_text_parsing_and_roundtrip(self):
        raw_html = (
            "<strong>Negrita</strong> "
            "<em>Cursiva</em> "
            "<u>Subrayado</u> "
            "<s>Tachado</s> "
            "<code>Codigo</code> "
            '<mark style="color: red;" data-color="red">Rojo</mark> '
            '<mark style="background-color: yellow;" data-color="yellow_background">Amarillo</mark> '
            '<a href="https://example.com">Enlace</a> '
            '<span class="inline-equation" data-latex="\\sqrt{x}">\\sqrt{x}</span>'
        )
        parsed = rich_text.html_to_rich_text(raw_html)
        self.assertTrue(len(parsed) >= 9)

        # Verificar decoradores extraídos
        decs_flat = [seg[1] for seg in parsed if len(seg) > 1 and seg[1]]
        tag_types = {d[0] for dec_list in decs_flat for d in dec_list}
        self.assertIn('b', tag_types)
        self.assertIn('i', tag_types)
        self.assertIn('_', tag_types)
        self.assertIn('s', tag_types)
        self.assertIn('c', tag_types)
        self.assertIn('h', tag_types)
        self.assertIn('a', tag_types)
        self.assertIn('e', tag_types)

        # Plain text extraído debe ser consistente
        plain = rich_text.rich_text_to_plain_text(parsed)
        self.assertIn("Negrita", plain)
        self.assertIn("Cursiva", plain)
        self.assertIn("Rojo", plain)
        self.assertIn("\\sqrt{x}", plain)

    def test_nested_decorators(self):
        raw_html = "<strong><em>Texto en Negrita y Cursiva</em></strong>"
        parsed = rich_text.html_to_rich_text(raw_html)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0][0], "Texto en Negrita y Cursiva")
        decs = parsed[0][1]
        tags = {d[0] for d in decs}
        self.assertEqual(tags, {'b', 'i'})

    def test_xss_and_dangerous_schemes_sanitization(self):
        malicious_tuples = [
            ["<script>alert(1)</script>", [["b"]]],
            ["Click here", [["a", "javascript:alert(document.cookie)"]]],
            ["VBScript", [["a", "vbscript:msgbox(1)"]]],
        ]
        html_out = rich_text.rich_text_to_html(malicious_tuples, sanitize=True)

        self.assertNotIn("<script>", html_out)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html_out)
        self.assertNotIn("javascript:", html_out)
        self.assertNotIn("vbscript:", html_out)
        self.assertIn('href="#"', html_out)

    def test_adjacent_segment_merging(self):
        # 3 segmentos contiguos en negrita deben fusionarse en uno solo
        html_input = "<strong>Parte 1</strong><strong> Parte 2</strong><strong> Parte 3</strong>"
        parsed = rich_text.html_to_rich_text(html_input)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0][0], "Parte 1 Parte 2 Parte 3")
        self.assertEqual(parsed[0][1], [['b']])


class TestNotionBlockSchemasAndValidation(unittest.TestCase):
    """Pruebas de validación y definición canónica de los 17 tipos de bloques de Notion."""

    def test_all_17_block_types_in_catalog(self):
        expected_types = [
            'page', 'column_list', 'column', 'divider',
            'text', 'header', 'sub_header', 'sub_sub_header',
            'bulleted_list', 'numbered_list', 'toggle',
            'code', 'equation', 'table', 'table_row',
            'collection_view', 'collection_view_page',
            'image', 'sub_page'
        ]
        for btype in expected_types:
            self.assertTrue(
                rich_text.is_valid_block_type(btype),
                f"El tipo de bloque '{btype}' debe estar en el catálogo canónico"
            )
            self.assertIn(btype, rich_text.BLOCK_SCHEMAS)

    def test_validate_block_valid_cases(self):
        test_blocks = [
            {'type': 'page', 'properties': {'title': [['Mi Página', []]]}, 'content': ['c1']},
            {'type': 'column_list', 'content': ['col1', 'col2']},
            {'type': 'column', 'format': {'column_ratio': 0.5}, 'content': ['t1']},
            {'type': 'divider', 'content': []},
            {'type': 'text', 'properties': {'title': [['Un párrafo', []]]}},
            {'type': 'header', 'properties': {'title': [['Encabezado H1', []]]}, 'content': []},
            {'type': 'sub_header', 'properties': {'title': [['Encabezado H2', []]]}, 'content': []},
            {'type': 'sub_sub_header', 'properties': {'title': [['Encabezado H3', []]]}, 'content': []},
            {'type': 'bulleted_list', 'properties': {'title': [['Item', []]]}},
            {'type': 'numbered_list', 'properties': {'title': [['1. Item', []]]}},
            {'type': 'toggle', 'properties': {'title': [['Desplegable', []]]}, 'content': ['child-1']},
            {'type': 'code', 'properties': {'title': [['print("hola")', []]], 'language': [['python', []]]}},
            {'type': 'equation', 'properties': {'title': [['\\int_0^1 x dx', []]]}},
            {'type': 'table', 'format': {'table_block_column_order': ['col1', 'col2']}, 'content': ['row1']},
            {'type': 'table_row', 'properties': {'col1': [['Celda 1', []]]}},
            {'type': 'collection_view', 'format': {'collection_id': 'c1', 'view_ids': ['v1']}},
            {'type': 'collection_view_page', 'properties': {'title': [['DB', []]]}},
            {'type': 'image', 'properties': {'source': [['https://example.com/pic.png', []]]}, 'format': {'block_width': 600}},
            {'type': 'sub_page', 'properties': {'page_id': 'target-note-1', 'title': 'Subnota'}},
        ]

        for blk in test_blocks:
            is_valid, err = rich_text.validate_block(blk)
            self.assertTrue(is_valid, f"Bloque {blk['type']} falló validación: {err}")

    def test_validate_block_invalid_cases(self):
        # 1. Tipo desconocido
        is_valid, err = rich_text.validate_block({'type': 'alien_block'})
        self.assertFalse(is_valid)
        self.assertIn("Unknown or unsupported", err)

        # 2. Divider con hijos no permitidos
        is_valid, err = rich_text.validate_block({'type': 'divider', 'content': ['illegal-child']})
        self.assertFalse(is_valid)
        self.assertIn("does not permit children", err)

        # 3. column_ratio inválido
        is_valid, err = rich_text.validate_block({'type': 'column', 'format': {'column_ratio': 1.5}})
        self.assertFalse(is_valid)
        self.assertIn("column_ratio", err)

        # 4. sub_page sin page_id
        is_valid, err = rich_text.validate_block({'type': 'sub_page', 'properties': {'title': 'Sin id'}})
        self.assertFalse(is_valid)
        self.assertIn("requires 'page_id'", err)

        # 5. Rich text malformado en properties.title
        is_valid, err = rich_text.validate_block({
            'type': 'text',
            'properties': {'title': 'Deberia ser lista de tuplas'}
        })
        self.assertFalse(is_valid)


class TestBlockRESTAndBridgeIntegration(unittest.TestCase):
    """
    Pruebas integrales de la API REST (backend.py) y del puente PyWebViewBridge (desktop_app.py).
    """

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = os.path.join(cls.temp_dir.name, 'test_m2.db')
        cls.orig_db = models.db
        cls.test_db = SqliteDatabase(cls.test_db_path)
        models.db = cls.test_db
        models.BaseModel._meta.database = cls.test_db

        for m in [
            models.Note, models.Folder, models.Setting, models.NoteHistory,
            models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord
        ]:
            m._meta.database = cls.test_db

        cls.test_db.connect()
        models.init_db()

        # Iniciar servidor HTTP en puerto dinámico para pruebas REST
        cls.server_port = find_free_port()
        backend.PORT = cls.server_port
        cls.http_server = backend.ThreadingHTTPServer(('127.0.0.1', cls.server_port), backend.NoteJSRequestHandler)
        cls.server_thread = threading.Thread(target=cls.http_server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server_port}"
        time.sleep(0.1)

        cls.bridge = desktop_app.PyWebViewBridge()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.http_server.shutdown()
            cls.http_server.server_close()
        except Exception:
            pass
        try:
            cls.temp_dir.cleanup()
        except Exception:
            pass
        models.db = cls.orig_db
        models.BaseModel._meta.database = cls.orig_db
        for m in [
            models.Note, models.Folder, models.Setting, models.NoteHistory,
            models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord
        ]:
            m._meta.database = cls.orig_db

    def setUp(self):
        models.Block.delete().execute()
        models.Note.delete().execute()

    def _http_request(self, method, path, payload=None):
        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode('utf-8') if payload is not None else None
        headers = {'Content-Type': 'application/json'} if payload is not None else {}
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
                body = json.loads(response.read().decode('utf-8'))
                return status, body
        except urllib.error.HTTPError as e:
            status = e.code
            try:
                body = json.loads(e.read().decode('utf-8'))
            except Exception:
                body = {'ok': False, 'error': str(e)}
            return status, body

    # -------------------------------------------------------------------------
    # REST Endpoints: Creación, Consulta, Actualización y Reordenamiento
    # -------------------------------------------------------------------------

    def test_rest_create_and_get_block(self):
        """Verifica POST /api/blocks y GET /api/blocks/<id>."""
        # 1. Crear bloque raíz
        status, res = self._http_request('POST', '/api/blocks', {
            'id': 'root-page-1',
            'type': 'page',
            'properties': {'title': [['Página Principal', []]]},
        })
        self.assertEqual(status, 201)
        self.assertTrue(res['ok'])
        self.assertEqual(res['block']['id'], 'root-page-1')
        self.assertEqual(res['block']['type'], 'page')

        # 2. Consultar bloque individual
        status, get_res = self._http_request('GET', '/api/blocks/root-page-1')
        self.assertEqual(status, 200)
        self.assertTrue(get_res['ok'])
        self.assertEqual(get_res['block']['id'], 'root-page-1')

    def test_rest_create_child_with_positioning(self):
        """Verifica inserción en content con target_index, after_id y before_id."""
        # Crear padre
        self._http_request('POST', '/api/blocks', {
            'id': 'parent-col-1',
            'type': 'column',
        })

        # Insertar hijo 1 (append)
        status, c1 = self._http_request('POST', '/api/blocks', {
            'id': 'child-1',
            'type': 'text',
            'parent_id': 'parent-col-1',
        })
        self.assertEqual(status, 201)

        # Insertar hijo 2 (append)
        status, c2 = self._http_request('POST', '/api/blocks', {
            'id': 'child-2',
            'type': 'text',
            'parent_id': 'parent-col-1',
        })
        self.assertEqual(status, 201)

        # Insertar hijo 3 entre child-1 y child-2 mediante after_id='child-1'
        status, c3 = self._http_request('POST', '/api/blocks', {
            'id': 'child-3',
            'type': 'text',
            'parent_id': 'parent-col-1',
            'after_id': 'child-1',
        })
        self.assertEqual(status, 201)

        # Verificar orden en parent.content: ['child-1', 'child-3', 'child-2']
        _, p_check = self._http_request('GET', '/api/blocks/parent-col-1')
        self.assertEqual(p_check['block']['content'], ['child-1', 'child-3', 'child-2'])

    def test_rest_cycle_detection(self):
        """Verifica que no se permita jerarquía circular (un bloque siendo su propio ancestro)."""
        self._http_request('POST', '/api/blocks', {'id': 'b-ancestor', 'type': 'page'})
        self._http_request('POST', '/api/blocks', {'id': 'b-child', 'type': 'text', 'parent_id': 'b-ancestor'})

        # Intentar crear un bloque hijo que tenga a b-ancestor como parent pero id igual
        status, res = self._http_request('POST', '/api/blocks', {
            'id': 'b-ancestor',
            'type': 'text',
            'parent_id': 'b-ancestor',
        })
        self.assertEqual(status, 400)
        self.assertIn("own parent", res['error'])

    def test_rest_update_and_concurrency(self):
        """Verifica PUT /api/blocks/<id> y detección de conflictos con expected_version."""
        self._http_request('POST', '/api/blocks', {
            'id': 'blk-mut',
            'type': 'text',
            'properties': {'title': [['Original', []]]},
        })

        # Actualización correcta con expected_version=1
        status, up_res = self._http_request('PUT', '/api/blocks/blk-mut', {
            'properties': {'title': [['Modificado', []]]},
            'format': {'block_color': 'green'},
            'expected_version': 1,
        })
        self.assertEqual(status, 200)
        self.assertEqual(up_res['block']['version'], 2)
        self.assertEqual(up_res['block']['properties']['title'], [['Modificado', []]])

        # Conflicto de versión: intentar actualizar enviando expected_version=1 cuando actual es 2
        status_conflict, conf_res = self._http_request('PUT', '/api/blocks/blk-mut', {
            'properties': {'title': [['Desincronizado', []]]},
            'expected_version': 1,
        })
        self.assertEqual(status_conflict, 409)
        self.assertFalse(conf_res['ok'])
        self.assertEqual(conf_res['current_version'], 2)

    def test_rest_subtree_record_map(self):
        """Verifica BFS resolution de subárbol en /api/blocks/<id>/recordMap."""
        # Construir árbol: Página -> ListaColumnas -> Columna1 -> Texto1
        self._http_request('POST', '/api/blocks', {'id': 'p-root', 'type': 'page'})
        self._http_request('POST', '/api/blocks', {'id': 'c-list', 'type': 'column_list', 'parent_id': 'p-root'})
        self._http_request('POST', '/api/blocks', {'id': 'col-1', 'type': 'column', 'parent_id': 'c-list'})
        self._http_request('POST', '/api/blocks', {'id': 'txt-1', 'type': 'text', 'parent_id': 'col-1'})

        status, rmap_res = self._http_request('GET', '/api/blocks/p-root/recordMap')
        self.assertEqual(status, 200)
        self.assertTrue(rmap_res['ok'])
        self.assertEqual(rmap_res['rootId'], 'p-root')

        bmap = rmap_res['recordMap']['block']
        self.assertIn('p-root', bmap)
        self.assertIn('c-list', bmap)
        self.assertIn('col-1', bmap)
        self.assertIn('txt-1', bmap)
        self.assertEqual(bmap['txt-1']['role'], 'editor')

    def test_rest_reorder_endpoint(self):
        """Verifica POST /api/blocks/<id>/reorder."""
        self._http_request('POST', '/api/blocks', {'id': 'p-order', 'type': 'page'})
        self._http_request('POST', '/api/blocks', {'id': 'item-1', 'type': 'text', 'parent_id': 'p-order'})
        self._http_request('POST', '/api/blocks', {'id': 'item-2', 'type': 'text', 'parent_id': 'p-order'})
        self._http_request('POST', '/api/blocks', {'id': 'item-3', 'type': 'text', 'parent_id': 'p-order'})

        status, reorder_res = self._http_request('POST', '/api/blocks/p-order/reorder', {
            'content': ['item-3', 'item-1', 'item-2'],
        })
        self.assertEqual(status, 200)
        self.assertEqual(reorder_res['parent']['content'], ['item-3', 'item-1', 'item-2'])

    def test_rest_soft_delete_and_restore(self):
        """Verifica DELETE /api/blocks/<id> y POST /api/blocks/<id>/restore."""
        self._http_request('POST', '/api/blocks', {'id': 'parent-del', 'type': 'page'})
        self._http_request('POST', '/api/blocks', {'id': 'child-del', 'type': 'text', 'parent_id': 'parent-del'})

        # Borrado lógico
        status_del, res_del = self._http_request('DELETE', '/api/blocks/child-del')
        self.assertEqual(status_del, 200)
        self.assertEqual(res_del['alive'], 0)

        # Comprobar que ya no aparece en consulta regular (alive=0)
        status_get, _ = self._http_request('GET', '/api/blocks/child-del')
        self.assertEqual(status_get, 404)

        # Comprobar que fue removido del content del padre
        _, p_check = self._http_request('GET', '/api/blocks/parent-del')
        self.assertNotIn('child-del', p_check['block']['content'])

        # Restaurar
        status_rest, res_rest = self._http_request('POST', '/api/blocks/child-del/restore')
        self.assertEqual(status_rest, 200)
        self.assertEqual(res_rest['alive'], 1)

        # Comprobar que reaparece en el padre
        _, p_after = self._http_request('GET', '/api/blocks/parent-del')
        self.assertIn('child-del', p_after['block']['content'])

    def test_rest_rich_text_convert_endpoint(self):
        """Verifica POST /api/blocks/rich-text/convert y GET de ayuda."""
        # 1. GET ayuda
        status_get, res_help = self._http_request('GET', '/api/blocks/rich-text/convert')
        self.assertEqual(status_get, 200)
        self.assertIn('usage', res_help)

        # 2. HTML a RichText
        status, res_html = self._http_request('POST', '/api/blocks/rich-text/convert', {
            'html': '<strong>Importante</strong>',
        })
        self.assertEqual(status, 200)
        self.assertEqual(res_html['rich_text'], [['Importante', [['b']]]])

        # 3. RichText a HTML y texto plano
        status, res_rt = self._http_request('POST', '/api/blocks/rich-text/convert', {
            'rich_text': [['Importante', [['b']]]],
        })
        self.assertEqual(status, 200)
        self.assertIn('<strong>Importante</strong>', res_rt['html'])
        self.assertEqual(res_rt['plain_text'], 'Importante')

    def test_reserved_subpaths_disambiguation(self):
        """
        Garantiza que /api/blocks/order, /api/blocks/batch y /api/blocks/rich-text/convert
        no sean tratados como IDs dinámicos de bloques.
        """
        # POST a /api/blocks/order debe ser enrutado al manejador fraccionario legacy
        status, res_order = self._http_request('POST', '/api/blocks/order', {
            'blockId': 'legacy-order-blk',
            'noteId': 101,
        })
        self.assertEqual(status, 200)
        self.assertTrue(res_order['ok'])
        self.assertIn('sortIndex', res_order)

        # POST a /api/blocks/batch debe ser enrutado al manejador batch legacy
        status, res_batch = self._http_request('POST', '/api/blocks/batch', {
            'moves': [{'id': 'legacy-batch-1', 'sortIndex': 'a1'}],
        })
        self.assertEqual(status, 200)
        self.assertTrue(res_batch['ok'])

    # -------------------------------------------------------------------------
    # PyWebView Bridge Native Methods
    # -------------------------------------------------------------------------

    def test_bridge_native_methods(self):
        """Verifica los métodos nativos de window.pywebview.api expuestos por PyWebViewBridge."""
        # 1. create_block
        create_res = self.bridge.create_block({
            'id': 'bridge-root',
            'type': 'page',
            'properties': {'title': [['Bridge Page', []]]},
        })
        self.assertTrue(create_res['ok'])
        self.assertEqual(create_res['block']['id'], 'bridge-root')

        # 2. get_block
        get_res = self.bridge.get_block('bridge-root')
        self.assertTrue(get_res['ok'])
        self.assertEqual(get_res['block']['id'], 'bridge-root')

        # 3. create child
        child_res = self.bridge.create_block({
            'id': 'bridge-child-1',
            'type': 'text',
            'parent_id': 'bridge-root',
            'properties': {'title': [['Párrafo hijo', []]]},
        })
        self.assertTrue(child_res['ok'])

        # 4. get_record_map
        rmap_res = self.bridge.get_record_map('bridge-root')
        self.assertTrue(rmap_res['ok'])
        self.assertIn('bridge-root', rmap_res['recordMap']['block'])
        self.assertIn('bridge-child-1', rmap_res['recordMap']['block'])

        # 5. update_block
        up_res = self.bridge.update_block('bridge-child-1', {
            'properties': {'title': [['Párrafo editado', []]]},
        })
        self.assertTrue(up_res['ok'])
        self.assertEqual(up_res['block']['properties']['title'], [['Párrafo editado', []]])

        # 6. reorder_block_children
        self.bridge.create_block({'id': 'bridge-child-2', 'type': 'text', 'parent_id': 'bridge-root'})
        reorder_res = self.bridge.reorder_block_children('bridge-root', ['bridge-child-2', 'bridge-child-1'])
        self.assertTrue(reorder_res['ok'])
        self.assertEqual(reorder_res['parent']['content'], ['bridge-child-2', 'bridge-child-1'])

        # 7. soft_delete_block y restore_block
        del_res = self.bridge.soft_delete_block('bridge-child-2')
        self.assertTrue(del_res['ok'])
        self.assertEqual(del_res['alive'], 0)

        rest_res = self.bridge.restore_block('bridge-child-2')
        self.assertTrue(rest_res['ok'])
        self.assertEqual(rest_res['alive'], 1)

        # 8. convert_rich_text
        conv_res = self.bridge.convert_rich_text({'html': '<em>Cursiva nativa</em>'})
        self.assertTrue(conv_res['ok'])
        self.assertEqual(conv_res['rich_text'], [['Cursiva nativa', [['i']]]])


if __name__ == '__main__':
    unittest.main()
