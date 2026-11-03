#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_notion_transactions_and_blocks.py
Test suite de extremo a extremo (E2E) para el sistema de transacciones y tipos de bloques de Notion.

Cubre 4 niveles (Tiers) de verificación rigurosa:
- Tier 1: Validación canónica de esquemas, 11 nuevos tipos de bloques, nodos hoja atómicos vs contenedores,
          validación dinámica de encabezados desplegables (format.toggleable) y propiedad checked de to_do.
- Tier 2: Protocolo transaccional atómico (op.set + op.listAfter), garantías de rollback (0 bloques huérfanos),
          posicionamiento espacial direccional (after_id, before_id, index 0) y rechazo estricto de hijos en hojas.
- Tier 3: Contratos de la API REST (/api/transactions, /api/blocks) y puente nativo PyWebViewBridge.
- Tier 4: Escenarios reales de aplicación (minutas de reunión, bloques sincronizados, tablero de recursos multimedia,
          jerarquías anidadas con integridad transaccional, y documentación con header_4 y citas).
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
    """Obtiene un puerto TCP libre efímero para aislar el servidor HTTP en pruebas."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


# =============================================================================
# Clase Base con Fixture de Base de Datos SQLite Aislada y Servidor HTTP
# =============================================================================

class BaseNotionTest(unittest.TestCase):
    """
    Fixture base con base de datos SQLite aislada en tempfile.TemporaryDirectory,
    revinculación de modelos Peewee, limpieza de tablas en setUp y servidor HTTP efímero.
    """

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = os.path.join(cls.temp_dir.name, 'test_notion_e2e.db')
        cls.orig_db = models.db
        cls.test_db = SqliteDatabase(cls.test_db_path, timeout=10, check_same_thread=False)
        models.db = cls.test_db
        models.BaseModel._meta.database = cls.test_db

        for m in [
            models.Note, models.Folder, models.Setting, models.NoteHistory,
            models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord
        ]:
            m._meta.database = cls.test_db

        cls.test_db.connect(reuse_if_open=True)
        models.init_db()

        # Iniciar servidor HTTP en puerto dinámico
        cls.server_port = find_free_port()
        backend.PORT = cls.server_port
        cls.http_server = backend.ThreadingHTTPServer(('127.0.0.1', cls.server_port), backend.NoteJSRequestHandler)
        cls.server_thread = threading.Thread(target=cls.http_server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server_port}"
        time.sleep(0.1)

        # Instanciar bridge PyWebView
        cls.bridge = desktop_app.PyWebViewBridge()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.http_server.shutdown()
            cls.http_server.server_close()
        except Exception:
            pass
        try:
            cls.test_db.close()
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

    def _create_block_row(self, b_id, b_type='page', properties=None, fmt=None, content=None, parent_id=None):
        """Helper para crear una fila Block directamente en SQLite con valores canónicos."""
        now_ms = int(time.time() * 1000)
        props_str = json.dumps(properties or {}, ensure_ascii=False)
        fmt_str = json.dumps(fmt or {}, ensure_ascii=False)
        content_str = json.dumps(content, ensure_ascii=False) if content is not None else None
        crdt_str = json.dumps({'clock': 1, 'mutations': []}, ensure_ascii=False)

        return models.Block.create(
            id=str(b_id),
            space_id='default_space',
            version=1,
            last_version=0,
            type=str(b_type),
            properties=props_str,
            content=content_str,
            parent_id=str(parent_id) if parent_id else None,
            parent_table='block' if parent_id else 'space',
            alive=1,
            format=fmt_str,
            crdt_format_version=1,
            crdt_data=crdt_str,
            created_time=now_ms,
            last_edited_time=now_ms,
            permissions='[]',
        )


# =============================================================================
# Tier 1: Validación Canónica y Esquemas de Bloques (rich_text.py)
# =============================================================================

class TestTier1SchemaAndValidation(unittest.TestCase):
    """Pruebas unitarias de esquemas y reglas estructurales en rich_text.py."""

    NEW_TYPES = [
        'header_4',
        'to_do',
        'quote',
        'callout',
        'transclusion_container',
        'transclusion_reference',
        'video',
        'audio',
        'file',
        'pdf',
        'bookmark',
    ]

    LEAF_TYPES = [
        'code',
        'divider',
        'equation',
        'image',
        'video',
        'audio',
        'file',
        'pdf',
        'bookmark',
        'table_row',
        'transclusion_reference',
        'sub_page',
    ]

    HEADER_TYPES = [
        'header',
        'sub_header',
        'sub_sub_header',
        'header_4',
    ]

    def test_all_11_new_types_recognized_by_is_valid_block_type(self):
        """Verifica que los 11 nuevos tipos de bloques sean reconocidos por is_valid_block_type."""
        for btype in self.NEW_TYPES:
            self.assertTrue(
                rich_text.is_valid_block_type(btype),
                f"El tipo de bloque '{btype}' debe ser reconocido como válido"
            )
            # Prueba con mayúsculas y espacios
            self.assertTrue(
                rich_text.is_valid_block_type(f"  {btype.upper()}  "),
                f"El tipo '{btype.upper()}' debe ser normalizado y reconocido"
            )

        # Tipos no válidos deben ser rechazados
        self.assertFalse(rich_text.is_valid_block_type('unknown_custom_type'))
        self.assertFalse(rich_text.is_valid_block_type('widget'))
        self.assertFalse(rich_text.is_valid_block_type(''))
        self.assertFalse(rich_text.is_valid_block_type(None))

    def test_validate_block_header_4(self):
        """Verifica la validación canónica de header_4 (Heading 4)."""
        valid_h4 = {
            'type': 'header_4',
            'properties': {'title': [['Encabezado Nivel 4', [['b']]]]},
            'format': {'block_color': 'blue', 'toggleable': False},
        }
        ok, err = rich_text.validate_block(valid_h4)
        self.assertTrue(ok, f"header_4 válido debe pasar validación: {err}")

        # Rechaza propiedad no permitida
        invalid_prop = {
            'type': 'header_4',
            'properties': {'title': [['Texto', []]], 'invalid_prop': 'test'},
        }
        # En rich_text actual, las propiedades desconocidas o malformadas no deben ser permitidas si se valida
        # O verifica que title con rich text no válido sea rechazado:
        invalid_rt = {
            'type': 'header_4',
            'properties': {'title': 'Cadena plana no tupla'},
        }
        ok, err = rich_text.validate_block(invalid_rt)
        self.assertFalse(ok, "header_4 con title como string plano debe fallar validación")

    def test_validate_block_to_do_and_checked_property(self):
        """Verifica la validación de to_do y su propiedad checked."""
        # to_do sin marcar
        todo_unchecked = {
            'type': 'to_do',
            'properties': {
                'title': [['Tarea pendiente', []]],
                'checked': [['No', []]],
            },
        }
        ok, err = rich_text.validate_block(todo_unchecked)
        self.assertTrue(ok, f"to_do desmarcado debe ser válido: {err}")

        # to_do marcado
        todo_checked = {
            'type': 'to_do',
            'properties': {
                'title': [['Tarea completada', [['s']]]],
                'checked': [['Yes', []]],
            },
        }
        ok, err = rich_text.validate_block(todo_checked)
        self.assertTrue(ok, f"to_do marcado debe ser válido: {err}")

        # to_do es un contenedor: permite hijos
        todo_with_children = {
            'type': 'to_do',
            'properties': {'title': [['Tarea padre', []]]},
            'content': ['sub-task-1', 'sub-task-2'],
        }
        ok, err = rich_text.validate_block(todo_with_children)
        self.assertTrue(ok, f"to_do debe permitir hijos en content: {err}")

    def test_validate_block_quote(self):
        """Verifica la validación de quote (bloque de cita)."""
        valid_quote = {
            'type': 'quote',
            'properties': {'title': [['Cita celebre', [['i']]]]},
            'format': {'block_color': 'gray'},
            'content': ['child-block-1'],
        }
        ok, err = rich_text.validate_block(valid_quote)
        self.assertTrue(ok, f"quote válido debe pasar validación: {err}")

    def test_validate_block_callout(self):
        """Verifica la validación de callout (recuadro destacado)."""
        valid_callout = {
            'type': 'callout',
            'properties': {'title': [['Nota importante: revisar antes del viernes', [['b']]]]},
            'format': {'page_icon': '💡', 'block_color': 'yellow_background'},
            'content': ['nested-paragraph-1'],
        }
        ok, err = rich_text.validate_block(valid_callout)
        self.assertTrue(ok, f"callout con icono y color debe ser válido: {err}")

    def test_validate_block_transclusion_container_and_reference(self):
        """Verifica la validación de transclusion_container y transclusion_reference."""
        # transclusion_container: contenedor de contenido sincronizado
        container = {
            'type': 'transclusion_container',
            'properties': {},
            'format': {},
            'content': ['shared-b1', 'shared-b2'],
        }
        ok, err = rich_text.validate_block(container)
        self.assertTrue(ok, f"transclusion_container debe permitir hijos: {err}")

        # transclusion_reference: referencia hoja apuntando al contenedor
        ref = {
            'type': 'transclusion_reference',
            'properties': {},
            'format': {
                'transclusion_reference_pointer': {
                    'id': 'source-container-uuid',
                    'table': 'block',
                }
            },
            'content': None,
        }
        ok, err = rich_text.validate_block(ref)
        self.assertTrue(ok, f"transclusion_reference debe ser válido: {err}")

        # transclusion_reference con hijos debe ser RECHAZADO (es nodo hoja)
        ref_with_children = {
            'type': 'transclusion_reference',
            'format': {'transclusion_reference_pointer': {'id': 'x'}},
            'content': ['illegal-child'],
        }
        ok, err = rich_text.validate_block(ref_with_children)
        self.assertFalse(ok, "transclusion_reference no debe permitir hijos en content")

    def test_validate_block_media_leaves(self):
        """Verifica la validación de los bloques multimedia hoja: video, audio, file, pdf."""
        video_block = {
            'type': 'video',
            'properties': {'source': [['https://example.com/video.mp4', []]], 'caption': [['Demo', []]]},
            'format': {'block_width': 800, 'block_alignment': 'center'},
            'content': None,
        }
        ok, err = rich_text.validate_block(video_block)
        self.assertTrue(ok, f"video válido debe pasar: {err}")

        audio_block = {
            'type': 'audio',
            'properties': {'source': [['https://example.com/audio.mp3', []]]},
            'format': {'block_width': 500},
            'content': None,
        }
        ok, err = rich_text.validate_block(audio_block)
        self.assertTrue(ok, f"audio válido debe pasar: {err}")

        file_block = {
            'type': 'file',
            'properties': {
                'source': [['https://example.com/manual.pdf', []]],
                'title': [['Manual de Usuario', []]],
                'size': [['2.4 MB', []]],
            },
            'format': {'block_color': 'gray_background'},
            'content': None,
        }
        ok, err = rich_text.validate_block(file_block)
        self.assertTrue(ok, f"file válido debe pasar: {err}")

        pdf_block = {
            'type': 'pdf',
            'properties': {'source': [['https://example.com/doc.pdf', []]]},
            'format': {'block_width': 750, 'block_height': 600, 'block_alignment': 'center'},
            'content': None,
        }
        ok, err = rich_text.validate_block(pdf_block)
        self.assertTrue(ok, f"pdf válido debe pasar: {err}")

    def test_validate_block_bookmark(self):
        """Verifica la validación de bookmark (marcador web)."""
        bookmark_block = {
            'type': 'bookmark',
            'properties': {
                'link': [['https://notion.so', []]],
                'title': [['Notion Workspace', []]],
                'description': [['All-in-one workspace', []]],
                'caption': [],
            },
            'format': {'bookmark_icon': 'https://notion.so/favicon.ico'},
            'content': None,
        }
        ok, err = rich_text.validate_block(bookmark_block)
        self.assertTrue(ok, f"bookmark válido debe pasar validación: {err}")

    def test_leaf_blocks_strictly_reject_non_empty_content(self):
        """
        Regla estructural canónica: Todos los bloques hoja atómicos
        (code, divider, equation, image, video, audio, file, pdf, bookmark, table_row, transclusion_reference, sub_page)
        deben rechazar estrictamente tener hijos en content.
        """
        for leaf in self.LEAF_TYPES:
            props = {'page_id': 'sub-page-uuid'} if leaf == 'sub_page' else {}
            # 1. content no vacío -> DEBE FALLAR
            block_with_child = {
                'type': leaf,
                'properties': props,
                'content': ['child-uuid-1'],
            }
            ok, err = rich_text.validate_block(block_with_child)
            self.assertFalse(
                ok,
                f"El bloque hoja '{leaf}' debe rechazar content no vacío, pero validate_block retornó True"
            )
            self.assertIn("does not permit children", str(err).lower())

            # 2. content vacío o None -> DEBE SER VÁLIDO
            block_empty_content = {
                'type': leaf,
                'properties': props,
                'content': [],
            }
            ok_empty, _ = rich_text.validate_block(block_empty_content)
            self.assertTrue(ok_empty, f"El bloque hoja '{leaf}' con content=[] debe ser válido")

            block_none_content = {
                'type': leaf,
                'properties': props,
                'content': None,
            }
            ok_none, _ = rich_text.validate_block(block_none_content)
            self.assertTrue(ok_none, f"El bloque hoja '{leaf}' con content=None debe ser válido")

    def test_toggleable_headers_allow_children_iff_toggleable_true(self):
        """
        Regla dinámica de encabezados: header, sub_header, sub_sub_header, header_4
        permiten hijos en content SI Y SOLO SI format.toggleable = True.
        """
        for h_type in self.HEADER_TYPES:
            # Caso 1: format.toggleable = True con hijos -> DEBE PASAR
            h_toggle_on = {
                'type': h_type,
                'properties': {'title': [[f'Encabezado {h_type}', []]]},
                'format': {'toggleable': True},
                'content': ['child-block-uuid-1', 'child-block-uuid-2'],
            }
            ok, err = rich_text.validate_block(h_toggle_on)
            self.assertTrue(
                ok,
                f"Encabezado '{h_type}' con toggleable=True debe permitir hijos en content. Error: {err}"
            )

            # Caso 2: format.toggleable = False con hijos -> DEBE FALLAR
            h_toggle_off = {
                'type': h_type,
                'properties': {'title': [[f'Encabezado {h_type}', []]]},
                'format': {'toggleable': False},
                'content': ['child-block-uuid-1'],
            }
            ok, err = rich_text.validate_block(h_toggle_off)
            self.assertFalse(
                ok,
                f"Encabezado '{h_type}' con toggleable=False debe rechazar hijos en content"
            )

            # Caso 3: format sin toggleable (vacío) con hijos -> DEBE FALLAR
            h_no_toggle = {
                'type': h_type,
                'properties': {'title': [[f'Encabezado {h_type}', []]]},
                'format': {},
                'content': ['child-block-uuid-1'],
            }
            ok, err = rich_text.validate_block(h_no_toggle)
            self.assertFalse(
                ok,
                f"Encabezado '{h_type}' sin format.toggleable debe rechazar hijos en content"
            )

            # Caso 4: format = None con hijos -> DEBE FALLAR
            h_none_format = {
                'type': h_type,
                'properties': {'title': [[f'Encabezado {h_type}', []]]},
                'format': None,
                'content': ['child-block-uuid-1'],
            }
            ok, err = rich_text.validate_block(h_none_format)
            self.assertFalse(
                ok,
                f"Encabezado '{h_type}' con format=None debe rechazar hijos en content"
            )

    def test_create_default_block_defaults_for_all_new_types(self):
        """Verifica que create_default_block genere estructuras canónicas para los nuevos tipos."""
        for btype in self.NEW_TYPES:
            blk = rich_text.create_default_block(btype, block_id=f"test-{btype}")
            self.assertEqual(blk['type'], btype)
            self.assertEqual(blk['id'], f"test-{btype}")
            self.assertEqual(blk['version'], 1)
            self.assertEqual(blk['alive'], 1)

            # Verificar que sea válido según validate_block
            ok, err = rich_text.validate_block(blk)
            self.assertTrue(ok, f"Bloque por defecto '{btype}' debe ser válido según validate_block: {err}")

            # Bloques hoja deben tener content=None, contenedores content=[]
            if btype in rich_text.LEAF_BLOCK_TYPES or (
                btype in rich_text.TOGGLEABLE_HEADER_TYPES and not bool(blk['format'].get('toggleable'))
            ):
                self.assertIsNone(blk['content'], f"Bloque hoja '{btype}' debe tener content=None por defecto")
            else:
                self.assertIsInstance(blk['content'], list, f"Contenedor '{btype}' debe tener content=[] por defecto")


# =============================================================================
# Tier 2: Protocolo Transaccional y Operaciones Atómicas (models.py)
# =============================================================================

class TestTier2TransactionalProtocolAndOperations(BaseNotionTest):
    """
    Pruebas del protocolo transaccional de creación atómica (op.set + op.listAfter),
    garantías de rollback en SQLite y reglas de inserción de hijos.
    """

    def test_build_op_set_canonical_structure(self):
        """Verifica la estructura canónica generada por models.build_op_set."""
        self.assertTrue(hasattr(models, 'build_op_set'), "models.py debe implementar build_op_set")
        child_id = 'crdt-block-uuid-1'
        data = {'type': 'text', 'properties': {'title': [['Párrafo', []]]}}
        op = models.build_op_set(child_id, data, space_id='test_space')

        self.assertEqual(op['command'], 'set')
        self.assertEqual(op['pointer']['table'], 'block')
        self.assertEqual(op['pointer']['id'], child_id)
        self.assertEqual(op['path'], [])
        self.assertIsInstance(op['args'], dict)
        self.assertEqual(op['args']['id'], child_id)
        self.assertEqual(op['args']['type'], 'text')

    def test_build_op_list_after_canonical_structure(self):
        """Verifica la estructura canónica generada por models.build_op_list_after."""
        self.assertTrue(hasattr(models, 'build_op_list_after'), "models.py debe implementar build_op_list_after")
        parent_id = 'parent-page-uuid'
        child_id = 'child-block-uuid'
        after_id = 'sibling-block-uuid'
        op = models.build_op_list_after(parent_id, child_id, after_id=after_id)

        self.assertEqual(op['command'], 'listAfter')
        self.assertEqual(op['pointer']['table'], 'block')
        self.assertEqual(op['pointer']['id'], parent_id)
        self.assertEqual(op['path'], ['content'])
        self.assertEqual(op['args']['id'], child_id)
        self.assertEqual(op['args']['after'], after_id)

    def test_apply_transaction_atomic_creation(self):
        """
        Verifica que models.apply_transaction ejecute op.set y op.listAfter
        dentro de una transacción SQLite atómica consistente.
        """
        self.assertTrue(hasattr(models, 'apply_transaction'), "models.py debe implementar apply_transaction")

        # 1. Crear página padre contenedor
        parent = self._create_block_row('tx-parent-page', b_type='page', content=[])

        # 2. Construir operaciones atómicas concurrentes
        child_id = 'tx-child-todo'
        child_data = {
            'type': 'to_do',
            'properties': {'title': [['Aprender Peewee WAL', []]], 'checked': [['No', []]]},
            'parent_id': parent.id,
            'parent_table': 'block',
        }
        op_set = models.build_op_set(child_id, child_data)
        op_list = models.build_op_list_after(parent.id, child_id, after_id=None)

        # 3. Ejecutar transacción
        res = models.apply_transaction([op_set, op_list])
        self.assertTrue(res.get('ok'), f"apply_transaction falló: {res}")

        # 4. Verificar en SQLite: el hijo existe con punteros correctos
        child_in_db = models.Block.get_or_none(models.Block.id == child_id)
        self.assertIsNotNone(child_in_db, "El hijo debe persistir en SQLite")
        self.assertEqual(child_in_db.type, 'to_do')
        self.assertEqual(child_in_db.parent_id, str(parent.id))
        self.assertEqual(child_in_db.parent_table, 'block')
        self.assertEqual(child_in_db.version, 1)

        # 5. Verificar en SQLite: el padre tiene el UUID en su array content
        parent_reloaded = models.Block.get(models.Block.id == parent.id)
        parent_content = json.loads(parent_reloaded.content or '[]')
        self.assertIn(child_id, parent_content)
        self.assertTrue(parent_reloaded.version >= 2, "La versión del padre debe haberse incrementado")

    def test_transaction_rollback_leaves_zero_orphaned_blocks(self):
        """
        Garantía de atomicidad: Si una operación falla durante la transacción
        (por ejemplo, la actualización del padre falla), la transacción debe revertirse
        completamente y dejar CERO bloques huérfanos en SQLite.
        """
        self.assertTrue(hasattr(models, 'apply_transaction'), "models.py debe implementar apply_transaction")

        # Intentar crear un bloque hijo pero asociarlo a una operación de lista con error
        child_id = 'orphan-candidate-uuid'
        child_data = {
            'type': 'text',
            'properties': {'title': [['Texto que debe revertirse', []]]},
            'parent_id': 'non-existent-parent-uuid',
        }
        op_set = models.build_op_set(child_id, child_data)
        # Operación inválida que fuerza fallo transaccional
        failing_op = {
            'pointer': {'table': 'block', 'id': 'non-existent-parent-uuid'},
            'path': ['content'],
            'command': 'listAfter',
            'args': {'id': child_id, 'after': None},
        }

        # Ejecutar la transacción: debe fallar o abortar
        try:
            res = models.apply_transaction([op_set, failing_op])
            tx_succeeded = res.get('ok', False)
        except Exception:
            tx_succeeded = False

        self.assertFalse(tx_succeeded, "La transacción con operación inválida no debe tener éxito")

        # Comprobar que en SQLite NO EXISTE el bloque hijo (0 huérfanos)
        child_check = models.Block.get_or_none(models.Block.id == child_id)
        self.assertIsNone(child_check, "Garantía de atomicidad violada: se creó un bloque huérfano en SQLite")

    def test_directional_spatial_positioning_after_id_and_start(self):
        """
        Verifica el posicionamiento espacial con after_id y al inicio de la lista:
        - after_id coloca el hijo inmediatamente después del elemento especificado.
        - after_id=None coloca al inicio o final de forma controlada.
        """
        parent = self._create_block_row('pos-parent', b_type='page', content=['b1', 'b2', 'b3'])

        # 1. Insertar b_new1 después de 'b1'
        models.add_child_block(parent.id, {'id': 'b_new1', 'type': 'text'}, after_id='b1')
        p_reloaded = models.Block.get(models.Block.id == parent.id)
        content = json.loads(p_reloaded.content)
        self.assertEqual(content, ['b1', 'b_new1', 'b2', 'b3'])

        # 2. Insertar b_new2 después de 'b3' (al final)
        models.add_child_block(parent.id, {'id': 'b_new2', 'type': 'text'}, after_id='b3')
        p_reloaded = models.Block.get(models.Block.id == parent.id)
        content = json.loads(p_reloaded.content)
        self.assertEqual(content, ['b1', 'b_new1', 'b2', 'b3', 'b_new2'])

        # 3. Insertar b_start al inicio (index=0 o after_id=None al comienzo)
        models.add_child_block(parent.id, {'id': 'b_start', 'type': 'text'}, index=0)
        p_reloaded = models.Block.get(models.Block.id == parent.id)
        content = json.loads(p_reloaded.content)
        self.assertEqual(content[0], 'b_start')

        # 4. after_id inexistente: debe añadir al final de manera segura sin error
        models.add_child_block(parent.id, {'id': 'b_fallback', 'type': 'text'}, after_id='missing-id')
        p_reloaded = models.Block.get(models.Block.id == parent.id)
        content = json.loads(p_reloaded.content)
        self.assertEqual(content[-1], 'b_fallback')

    def test_add_child_block_rejects_pure_leaf_parents(self):
        """
        Verifica que models.add_child_block rechace estrictamente la inserción de hijos
        bajo bloques hoja puros (divider, code, equation, image, video, bookmark, etc.).
        """
        for leaf_type in ['divider', 'code', 'equation', 'image', 'video', 'audio', 'file', 'pdf', 'bookmark', 'table_row']:
            leaf = self._create_block_row(f"leaf-{leaf_type}", b_type=leaf_type, content=None)

            # Intentar agregar un hijo a un nodo hoja debe levantar ValueError
            with self.assertRaises(ValueError, msg=f"add_child_block debe rechazar agregar hijos a '{leaf_type}'"):
                models.add_child_block(leaf.id, {'id': f"child-of-{leaf_type}", 'type': 'text'})

            # El bloque hoja en SQLite no debe haber modificado su content
            reloaded = models.Block.get(models.Block.id == leaf.id)
            self.assertIn(reloaded.content, [None, 'null', ''], f"El content de '{leaf_type}' debe seguir siendo null")

    def test_add_child_block_rejects_non_toggleable_header(self):
        """
        Verifica que un encabezado con format.toggleable ausente o False
        rechace la inserción de hijos con ValueError.
        """
        # Encabezado estándar sin toggleable
        static_header = self._create_block_row(
            'static-h2',
            b_type='sub_header',
            fmt={'block_color': 'default', 'toggleable': False},
            content=None
        )

        with self.assertRaises(ValueError, msg="Encabezado no desplegable debe rechazar hijos"):
            models.add_child_block(static_header.id, {'id': 'child-to-reject', 'type': 'text'})

    def test_add_child_block_permits_toggleable_header(self):
        """
        Verifica que un encabezado con format.toggleable = True
        acepte hijos satisfactoriamente y los registre en content.
        """
        toggle_h = self._create_block_row(
            'toggle-h1',
            b_type='header',
            fmt={'toggleable': True},
            content=[]
        )

        child = models.add_child_block(toggle_h.id, {'id': 'child-of-toggle', 'type': 'to_do'})
        self.assertIsNotNone(child)
        self.assertEqual(child.id, 'child-of-toggle')

        reloaded = models.Block.get(models.Block.id == toggle_h.id)
        content = json.loads(reloaded.content)
        self.assertIn('child-of-toggle', content)

    def test_block_to_dict_preserves_leaf_content_null_vs_container_list(self):
        """
        Verifica que Block.to_dict() retorne content: None para nodos hoja
        y una lista para nodos contenedores.
        """
        leaf = self._create_block_row('test-leaf-div', b_type='divider', content=None)
        leaf_dict = leaf.to_dict()
        self.assertIsNone(leaf_dict.get('content'), "Nodo hoja divider debe tener content: None en to_dict()")

        container = self._create_block_row('test-container-page', b_type='page', content=['c1'])
        container_dict = container.to_dict()
        self.assertEqual(container_dict.get('content'), ['c1'], "Contenedor page debe tener lista en to_dict()")


# =============================================================================
# Tier 3: Contratos de la API REST y PyWebViewBridge (backend.py, desktop_app.py)
# =============================================================================

class TestTier3APIAndBridgeContracts(BaseNotionTest):
    """
    Pruebas de los endpoints REST (/api/transactions, /api/blocks)
    y de los métodos nativos de window.pywebview.api en PyWebViewBridge.
    """

    def test_post_api_transactions_batch_execution(self):
        """Verifica POST /api/transactions para la ejecución atómica de un lote de operaciones."""
        parent = self._create_block_row('api-tx-parent', b_type='page', content=[])

        operations = [
            models.build_op_set('api-callout-1', {
                'type': 'callout',
                'parent_id': parent.id,
                'properties': {'title': [['Aviso importante', []]]},
                'format': {'page_icon': '⭐', 'block_color': 'yellow_background'},
            }),
            models.build_op_list_after(parent.id, 'api-callout-1', after_id=None),
            models.build_op_set('api-todo-1', {
                'type': 'to_do',
                'parent_id': 'api-callout-1',
                'properties': {'title': [['Acción requerida', []]], 'checked': [['No', []]]},
            }),
            models.build_op_list_after('api-callout-1', 'api-todo-1', after_id=None),
        ]

        status, res = self._http_request('POST', '/api/transactions', {'operations': operations})
        self.assertIn(status, [200, 201], f"POST /api/transactions debe retornar 200/201: {res}")
        self.assertTrue(res.get('ok'), f"Respuesta de transacciones debe ser ok: {res}")

        # Comprobar ambos bloques en SQLite
        callout_db = models.Block.get_or_none(models.Block.id == 'api-callout-1')
        self.assertIsNotNone(callout_db)
        todo_db = models.Block.get_or_none(models.Block.id == 'api-todo-1')
        self.assertIsNotNone(todo_db)

        # Comprobar jerarquía de contenidos
        callout_content = json.loads(callout_db.content or '[]')
        self.assertIn('api-todo-1', callout_content)

    def test_post_api_transactions_rollback_on_error(self):
        """Verifica que POST /api/transactions aborte y retorne 400/500 ante operaciones inválidas."""
        parent = self._create_block_row('api-rollback-parent', b_type='page', content=[])

        operations = [
            models.build_op_set('should-rollback-blk', {
                'type': 'text',
                'parent_id': parent.id,
                'properties': {'title': [['No debe persistir', []]]},
            }),
            models.build_op_list_after(parent.id, 'should-rollback-blk', after_id=None),
            # Operación fallida contra objetivo inexistente
            {
                'pointer': {'table': 'block', 'id': 'invalid-missing-target'},
                'path': ['content'],
                'command': 'listAfter',
                'args': {'id': 'x', 'after': None},
            }
        ]

        status, res = self._http_request('POST', '/api/transactions', {'operations': operations})
        self.assertIn(status, [400, 500], f"Debe retornar código de error HTTP 400/500: {status}")
        self.assertFalse(res.get('ok', False))

        # Verificar que el primer bloque no fue persistido
        self.assertIsNone(models.Block.get_or_none(models.Block.id == 'should-rollback-blk'))

    def test_post_api_blocks_transactional_creation(self):
        """Verifica que POST /api/blocks cree un bloque hijo usando el protocolo transaccional."""
        parent = self._create_block_row('rest-parent-page', b_type='page', content=[])

        status, res = self._http_request('POST', '/api/blocks', {
            'id': 'rest-created-child',
            'type': 'header_4',
            'parent_id': str(parent.id),
            'properties': {'title': [['Subsección H4', []]]},
            'format': {'toggleable': True},
        })

        self.assertEqual(status, 201)
        self.assertTrue(res['ok'])
        self.assertEqual(res['block']['id'], 'rest-created-child')
        self.assertEqual(res['block']['type'], 'header_4')

        # Comprobar que el padre tiene al hijo en content
        p_reloaded = models.Block.get(models.Block.id == parent.id)
        self.assertIn('rest-created-child', json.loads(p_reloaded.content))

    def test_post_api_blocks_rejects_pure_leaf_parent(self):
        """Verifica que POST /api/blocks retorne 400 al intentar crear un hijo bajo un bloque hoja."""
        leaf = self._create_block_row('rest-leaf-divider', b_type='divider', content=None)

        status, res = self._http_request('POST', '/api/blocks', {
            'id': 'illegal-rest-child',
            'type': 'text',
            'parent_id': str(leaf.id),
        })

        self.assertEqual(status, 400, "Debe rechazar con HTTP 400 Bad Request")
        self.assertFalse(res['ok'])
        err_msg = str(res.get('error', '')).lower()
        self.assertTrue(
            any(w in err_msg for w in ['cannot accept children', 'leaf node', 'permit', 'does not permit']),
            f"El mensaje de error debe indicar rechazo de hijos en nodo hoja: {res.get('error')}"
        )
        self.assertIsNone(models.Block.get_or_none(models.Block.id == 'illegal-rest-child'))

    def test_post_api_blocks_toggleable_header_handling(self):
        """Verifica que POST /api/blocks valide format.toggleable en encabezados."""
        # Encabezado estático: rechaza
        static_h = self._create_block_row('rest-static-h', b_type='header', fmt={'toggleable': False}, content=None)
        status_rej, res_rej = self._http_request('POST', '/api/blocks', {
            'type': 'text',
            'parent_id': str(static_h.id),
        })
        self.assertEqual(status_rej, 400)
        self.assertFalse(res_rej['ok'])

        # Encabezado desplegable: acepta
        toggle_h = self._create_block_row('rest-toggle-h', b_type='header', fmt={'toggleable': True}, content=[])
        status_acc, res_acc = self._http_request('POST', '/api/blocks', {
            'type': 'text',
            'parent_id': str(toggle_h.id),
            'properties': {'title': [['Hijo de toggle header', []]]},
        })
        self.assertEqual(status_acc, 201)
        self.assertTrue(res_acc['ok'])

    def test_pywebview_bridge_apply_transaction(self):
        """Verifica el método nativo apply_transaction expuesto en PyWebViewBridge."""
        self.assertTrue(hasattr(self.bridge, 'apply_transaction'), "PyWebViewBridge debe implementar apply_transaction")

        parent = self._create_block_row('bridge-tx-parent', b_type='page', content=[])
        op_set = models.build_op_set('bridge-quote-1', {
            'type': 'quote',
            'parent_id': parent.id,
            'properties': {'title': [['Cita vía PyWebView Bridge', []]]},
        })
        op_list = models.build_op_list_after(parent.id, 'bridge-quote-1')

        res = self.bridge.apply_transaction([op_set, op_list])
        self.assertTrue(res.get('ok'), f"apply_transaction en puente debe retornar ok: {res}")
        self.assertIsNotNone(models.Block.get_or_none(models.Block.id == 'bridge-quote-1'))

    def test_pywebview_bridge_create_block_with_leaf_validation(self):
        """Verifica que PyWebViewBridge.create_block valide las restricciones de nodos hoja."""
        leaf = self._create_block_row('bridge-leaf-code', b_type='code', content=None)

        res = self.bridge.create_block({
            'type': 'text',
            'parent_id': str(leaf.id),
            'properties': {'title': [['Hijo ilegal', []]]},
        })
        self.assertFalse(res.get('ok', False), "create_block en puente debe rechazar agregar hijos a un bloque de código")


# =============================================================================
# Tier 4: Escenarios de Aplicación Reales (End-to-End)
# =============================================================================

class TestTier4RealWorldScenarios(BaseNotionTest):
    """
    Pruebas complejas de flujos de trabajo de usuario reales: minutas con toggles,
    bloques sincronizados, tableros multimedia, árboles jerárquicos profundos y documentación rica.
    """

    def test_scenario_1_toggleable_meeting_notes(self):
        """
        Escenario 1: Minuta de reunión completa con encabezados desplegables, tareas to_do interactivas,
        citas de objetivos y recuadros destacados (callouts).
        """
        # 1. Página principal de la reunión
        page = self._create_block_row('meeting-root', b_type='page', properties={'title': [['Reunión Sprint 42', []]]}, content=[])

        # 2. Callout de objetivo de la reunión
        callout = models.add_child_block(page.id, {
            'id': 'meeting-goal',
            'type': 'callout',
            'properties': {'title': [['Objetivo: Alinear entregables de la versión 1.2.0', [['b']]]]},
            'format': {'page_icon': '🎯', 'block_color': 'green_background'},
        })

        # 3. Encabezado desplegable de "Acciones Requeridas"
        toggle_h = models.add_child_block(page.id, {
            'id': 'meeting-actions-header',
            'type': 'header',
            'properties': {'title': [['Acciones del Equipo', []]]},
            'format': {'toggleable': True},
        })

        # 4. Tareas to_do dentro del encabezado desplegable
        task1 = models.add_child_block(toggle_h.id, {
            'id': 'task-1',
            'type': 'to_do',
            'properties': {'title': [['Actualizar esquema de base de datos', []]], 'checked': [['No', []]]},
        })
        task2 = models.add_child_block(toggle_h.id, {
            'id': 'task-2',
            'type': 'to_do',
            'properties': {'title': [['Ejecutar suite de pruebas de regresión', []]], 'checked': [['No', []]]},
        })

        # 5. Marcar task1 como completada
        task1_reloaded = models.Block.get(models.Block.id == task1.id)
        props = json.loads(task1_reloaded.properties)
        props['checked'] = [['Yes', []]]
        task1_reloaded.properties = json.dumps(props)
        task1_reloaded.save()

        # 6. Cita con recordatorio final
        quote = models.add_child_block(page.id, {
            'id': 'meeting-motto',
            'type': 'quote',
            'properties': {'title': [['"La simplicidad es prerrequisito para la fiabilidad."', [['i']]]]},
            'format': {'block_color': 'gray'},
        })

        # 7. Resolver recordMap completo del subárbol
        rmap_res = models.resolve_subtree_record_map(page.id)
        blocks = rmap_res.get('recordMap', {}).get('block') if 'recordMap' in rmap_res else rmap_res.get('block', {})
        self.assertTrue(len(blocks) > 0, "El subárbol resuelto debe contener bloques")

        self.assertIn('meeting-root', blocks)
        self.assertIn('meeting-goal', blocks)
        self.assertIn('meeting-actions-header', blocks)
        self.assertIn('task-1', blocks)
        self.assertIn('task-2', blocks)
        self.assertIn('meeting-motto', blocks)

        # Verificar checked en el recordMap
        task1_map = blocks['task-1']['value']
        self.assertEqual(task1_map['properties']['checked'], [['Yes', []]])

    def test_scenario_2_synced_block_container_and_reference(self):
        """
        Escenario 2: Bloque sincronizado maestro (transclusion_container) con contenido compartido
        y puntero de referencia (transclusion_reference) en otra página.
        """
        page_a = self._create_block_row('page-source', b_type='page', content=[])
        page_b = self._create_block_row('page-target', b_type='page', content=[])

        # 1. Crear contenedor sincronizado maestro en Page A
        synced_container = models.add_child_block(page_a.id, {
            'id': 'shared-nav-container',
            'type': 'transclusion_container',
            'properties': {},
            'format': {},
        })

        # 2. Agregar elementos compartidos al contenedor
        b1 = models.add_child_block(synced_container.id, {
            'id': 'nav-item-1',
            'type': 'text',
            'properties': {'title': [['Inicio', [['b']]]]},
        })
        b2 = models.add_child_block(synced_container.id, {
            'id': 'nav-item-2',
            'type': 'text',
            'properties': {'title': [['Documentación', []]]},
        })

        # 3. Crear puntero de referencia en Page B
        synced_ref = models.add_child_block(page_b.id, {
            'id': 'shared-nav-pointer',
            'type': 'transclusion_reference',
            'properties': {},
            'format': {
                'transclusion_reference_pointer': {
                    'id': str(synced_container.id),
                    'table': 'block',
                }
            },
        })

        # 4. Validar reglas estructurales
        # El contenedor es un contenedor con 2 hijos
        c_reloaded = models.Block.get(models.Block.id == synced_container.id)
        self.assertEqual(json.loads(c_reloaded.content), ['nav-item-1', 'nav-item-2'])

        # La referencia es un nodo hoja con content: None
        ref_reloaded = models.Block.get(models.Block.id == synced_ref.id)
        self.assertIsNone(ref_reloaded.to_dict().get('content'))

        # Intentar agregar un hijo a la referencia DEBE fallar
        with self.assertRaises(ValueError):
            models.add_child_block(synced_ref.id, {'type': 'text'})

    def test_scenario_3_media_rich_resource_board(self):
        """
        Escenario 3: Tablero de recursos multimedia en columnas con bookmark, video, audio, file y pdf.
        Verifica la persistencia de metadatos y la invariante de nodos hoja.
        """
        page = self._create_block_row('media-board', b_type='page', content=[])

        # 1. Lista de columnas
        col_list = models.add_child_block(page.id, {'id': 'media-cols', 'type': 'column_list'})
        col1 = models.add_child_block(col_list.id, {'id': 'col-1', 'type': 'column'})
        col2 = models.add_child_block(col_list.id, {'id': 'col-2', 'type': 'column'})

        # 2. En Columna 1: bookmark y video
        bm = models.add_child_block(col1.id, {
            'id': 'bm-repo',
            'type': 'bookmark',
            'properties': {
                'link': [['https://github.com/example/repo', []]],
                'title': [['Repositorio Oficial', []]],
                'description': [['Código fuente y documentación técnica', []]],
            },
            'format': {'bookmark_icon': 'https://github.com/favicon.ico'},
        })

        video = models.add_child_block(col1.id, {
            'id': 'vid-demo',
            'type': 'video',
            'properties': {'source': [['https://example.com/demo.webm', []]], 'caption': [['Demo 1080p', []]]},
            'format': {'block_width': 720},
        })

        # 3. En Columna 2: audio, file y pdf
        audio = models.add_child_block(col2.id, {
            'id': 'aud-podcast',
            'type': 'audio',
            'properties': {'source': [['https://example.com/episode.mp3', []]]},
            'format': {'block_width': 400},
        })

        file_card = models.add_child_block(col2.id, {
            'id': 'file-archive',
            'type': 'file',
            'properties': {
                'source': [['https://example.com/archive.zip', []]],
                'title': [['Paquete de Recursos', []]],
                'size': [['18.5 MB', []]],
            },
        })

        pdf_embed = models.add_child_block(col2.id, {
            'id': 'pdf-whitepaper',
            'type': 'pdf',
            'properties': {'source': [['https://example.com/whitepaper.pdf', []]]},
            'format': {'block_width': 700, 'block_height': 500},
        })

        # 4. Verificar que todos son hojas y rechazan hijos
        for media_blk in [bm, video, audio, file_card, pdf_embed]:
            self.assertIsNone(media_blk.to_dict().get('content'))
            with self.assertRaises(ValueError):
                models.add_child_block(media_blk.id, {'type': 'text'})

        # 5. Resolver árbol del tablero
        rmap = models.resolve_subtree_record_map(page.id)
        blocks = rmap.get('recordMap', {}).get('block') if 'recordMap' in rmap else rmap.get('block', {})
        self.assertEqual(len(blocks), 9)  # page + col_list + 2 cols + 5 media = 9

    def test_scenario_4_deeply_nested_container_tree_with_rollback(self):
        """
        Escenario 4: Jerarquía multinivel profunda con verificación de integridad transaccional
        y atomicidad en caso de aborto.
        """
        # Estructura: Page -> Header (toggle) -> Quote -> Callout -> To_Do -> Text
        page = self._create_block_row('deep-root', b_type='page', content=[])

        h1 = models.add_child_block(page.id, {'id': 'deep-h1', 'type': 'sub_header', 'format': {'toggleable': True}})
        quote = models.add_child_block(h1.id, {'id': 'deep-quote', 'type': 'quote', 'properties': {'title': [['Cita', []]]}})
        callout = models.add_child_block(quote.id, {'id': 'deep-callout', 'type': 'callout', 'properties': {'title': [['Alerta', []]]}})
        todo = models.add_child_block(callout.id, {'id': 'deep-todo', 'type': 'to_do', 'properties': {'title': [['Tarea', []]]}})
        leaf_text = models.add_child_block(todo.id, {'id': 'deep-leaf-text', 'type': 'text', 'properties': {'title': [['Final', []]]}})

        # Verificar cadena de punteros ascendente y descendente
        self.assertEqual(leaf_text.parent_id, todo.id)
        self.assertEqual(todo.parent_id, callout.id)
        self.assertEqual(callout.parent_id, quote.id)
        self.assertEqual(quote.parent_id, h1.id)
        self.assertEqual(h1.parent_id, page.id)

        # Ahora simular una transacción en la que se intenta agregar un hijo ilegal a un nodo hoja divider
        divider = models.add_child_block(page.id, {'id': 'deep-divider', 'type': 'divider'})
        bad_ops = [
            models.build_op_set('temp-should-not-exist', {'type': 'text'}),
            # Intento de inserción en divider (nodo hoja)
            {
                'pointer': {'table': 'block', 'id': divider.id},
                'path': ['content'],
                'command': 'listAfter',
                'args': {'id': 'temp-should-not-exist', 'after': None},
            }
        ]

        try:
            models.apply_transaction(bad_ops)
        except Exception:
            pass

        self.assertIsNone(models.Block.get_or_none(models.Block.id == 'temp-should-not-exist'))

    def test_scenario_5_documentation_page_with_header4_and_quotes(self):
        """
        Escenario 5: Página de documentación estructurada con encabezados de nivel 4 (header_4),
        bloques de cita con decoradores de rich text y eliminación en cascada.
        """
        doc_page = self._create_block_row('doc-page', b_type='page', properties={'title': [['Guía de Arquitectura', []]]}, content=[])

        # H4 estático
        h4_static = models.add_child_block(doc_page.id, {
            'id': 'doc-h4-static',
            'type': 'header_4',
            'properties': {'title': [['1.1 Requisitos del Sistema', [['b']]]]},
            'format': {'toggleable': False},
        })

        # H4 desplegable
        h4_toggle = models.add_child_block(doc_page.id, {
            'id': 'doc-h4-toggle',
            'type': 'header_4',
            'properties': {'title': [['1.2 Parámetros Avanzados', [['b'], ['_']]]]},
            'format': {'toggleable': True},
        })

        # Contenido dentro del H4 desplegable
        nested_quote = models.add_child_block(h4_toggle.id, {
            'id': 'doc-nested-quote',
            'type': 'quote',
            'properties': {'title': [['Nota: Modificar bajo su propio riesgo.', [['c'], ['h', 'red']]]]},
        })

        # Comprobar que H4 desplegable contiene la cita
        h4_reloaded = models.Block.get(models.Block.id == h4_toggle.id)
        self.assertIn('doc-nested-quote', json.loads(h4_reloaded.content))

        # Soft-delete del H4 desplegable debe marcar alive=0
        models.soft_delete_block(h4_toggle.id)
        h4_deleted = models.Block.get(models.Block.id == h4_toggle.id)
        self.assertEqual(h4_deleted.alive, 0)


if __name__ == '__main__':
    unittest.main()
