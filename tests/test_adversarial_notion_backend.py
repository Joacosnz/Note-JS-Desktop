#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_adversarial_notion_backend.py
Milestone 4 — Adversarial Verification & Coverage Hardening Test Suite (Challenger 1)

Aggressively stress-tests and challenges Backend Database, ORM, Consistency, and API layers:
1. Deep hierarchy nesting (15+, 30+, 50+ levels deep parent-child chains) and stack overflow immunity.
2. Cycle attacks / circular parent pointers (A->B->A, A->B->C->A, self-loops) and cycle defense.
3. Malformed / corrupted payloads in properties, format, crdt_data, and content JSON fields.
4. Optimistic concurrency collisions: stale expected_version (409 Conflict) and rapid parallel race conditions.
5. Orphaned blocks, cascade soft-delete (alive = 0), and selective restoration (alive = 1).
6. SQL injection hardening in block IDs, query parameters, delete operations, and properties.
"""

import os
import sys
import json
import time
import socket
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from peewee import SqliteDatabase, IntegrityError

# Ensure root directory is on sys.path
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

import models
import backend
import rich_text
import desktop_app


def find_free_port():
    """Finds an unused ephemeral TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


class TestAdversarialNotionBackend(unittest.TestCase):
    """
    Empirical adversarial stress test suite verifying Backend DB, ORM,
    Consistency algorithms, and REST API robustness.
    """

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = os.path.join(cls.temp_dir.name, 'test_adversarial.db')
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

        # Iniciar servidor HTTP dedicado en puerto dinámico
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

    def _http_request(self, method, path, payload=None, raw_body=None, timeout=10, headers=None):
        """Helper robusto para ejecutar peticiones HTTP directas al backend."""
        url = f"{self.base_url}{path}"
        req_headers = {'Content-Type': 'application/json'}
        if headers:
            req_headers.update(headers)

        if raw_body is not None:
            data = raw_body if isinstance(raw_body, bytes) else raw_body.encode('utf-8')
        elif payload is not None:
            data = json.dumps(payload).encode('utf-8')
        else:
            data = None
            if 'Content-Type' in req_headers and raw_body is None:
                del req_headers['Content-Type']

        req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                status = response.getcode()
                raw_text = response.read().decode('utf-8')
                try:
                    body = json.loads(raw_text)
                except Exception:
                    body = {'raw': raw_text}
                return status, body
        except urllib.error.HTTPError as e:
            status = e.code
            raw_text = e.read().decode('utf-8')
            try:
                body = json.loads(raw_text)
            except Exception:
                body = {'ok': False, 'error': str(e), 'raw': raw_text}
            return status, body

    # =========================================================================
    # 1. DEEP HIERARCHY NESTING (15+, 30+, 50+ LEVELS DEEP)
    # =========================================================================

    def test_01_deep_hierarchy_15_levels_record_map(self):
        """Verifica que un árbol lineal de 15 niveles de profundidad resuelve todos los nodos en recordMap."""
        root_id = "root_page_15"
        models.Block.create(
            id=root_id,
            type="page",
            properties=json.dumps({"title": [["Raíz 15 Niveles", []]]}),
            content=json.dumps(["child_level_1"]),
            parent_id=None,
            parent_table="space",
            alive=1
        )

        for lvl in range(1, 16):
            cid = f"child_level_{lvl}"
            next_cid = f"child_level_{lvl + 1}" if lvl < 15 else None
            p_id = root_id if lvl == 1 else f"child_level_{lvl - 1}"
            models.Block.create(
                id=cid,
                type="text",
                properties=json.dumps({"title": [[f"Nivel {lvl}", []]]}),
                content=json.dumps([next_cid] if next_cid else []),
                parent_id=p_id,
                parent_table="block",
                alive=1
            )

        res = models.resolve_subtree_record_map(root_id)
        self.assertIn("block", res)
        block_map = res["block"]
        self.assertEqual(len(block_map), 16)
        self.assertIn(root_id, block_map)
        for lvl in range(1, 16):
            self.assertIn(f"child_level_{lvl}", block_map)
            self.assertEqual(block_map[f"child_level_{lvl}"]["role"], "editor")

    def test_02_deep_hierarchy_30_levels_record_map_bfs_no_stack_overflow(self):
        """Verifica que una jerarquía de 30 niveles resuelve sin desbordar la pila de llamadas."""
        root_id = "root_page_30"
        models.Block.create(
            id=root_id,
            type="page",
            properties="{}",
            content=json.dumps(["lvl_30_1"]),
            parent_id=None,
            parent_table="space",
            alive=1
        )

        for lvl in range(1, 31):
            cid = f"lvl_30_{lvl}"
            next_cid = f"lvl_30_{lvl + 1}" if lvl < 30 else None
            p_id = root_id if lvl == 1 else f"lvl_30_{lvl - 1}"
            models.Block.create(
                id=cid,
                type="toggle",
                properties=json.dumps({"title": [[f"Toggle {lvl}", []]]}),
                content=json.dumps([next_cid] if next_cid else []),
                parent_id=p_id,
                parent_table="block",
                alive=1
            )

        res = models.resolve_subtree_record_map(root_id)
        self.assertEqual(len(res["block"]), 31)

    def test_03_deep_hierarchy_50_levels_rest_endpoint(self):
        """Verifica GET /api/blocks/<id>/recordMap en una cadena de 50 niveles de profundidad."""
        root_id = "deep_root_50"
        models.Block.create(
            id=root_id,
            type="page",
            properties=json.dumps({"title": [["Root 50", []]]}),
            content=json.dumps(["node_50_1"]),
            alive=1
        )

        for lvl in range(1, 51):
            cid = f"node_50_{lvl}"
            next_cid = f"node_50_{lvl + 1}" if lvl < 50 else None
            p_id = root_id if lvl == 1 else f"node_50_{lvl - 1}"
            models.Block.create(
                id=cid,
                type="text",
                properties=json.dumps({"title": [[f"Profundidad {lvl}", []]]}),
                content=json.dumps([next_cid] if next_cid else []),
                parent_id=p_id,
                parent_table="block",
                alive=1
            )

        status, body = self._http_request('GET', f"/api/blocks/{root_id}/recordMap")
        self.assertEqual(status, 200)
        self.assertTrue(body.get("ok"))
        self.assertEqual(len(body["recordMap"]["block"]), 51)
        self.assertIn("node_50_50", body["recordMap"]["block"])

    def test_04_deep_hierarchy_pywebview_bridge(self):
        """Verifica que el puente nativo PyWebViewBridge.get_block_record_map soporte jerarquías profundas."""
        root_id = "bridge_deep_root_20"
        models.Block.create(
            id=root_id,
            type="page",
            content=json.dumps(["bnode_1"]),
            alive=1
        )
        for i in range(1, 21):
            cid = f"bnode_{i}"
            nid = f"bnode_{i + 1}" if i < 20 else None
            pid = root_id if i == 1 else f"bnode_{i - 1}"
            models.Block.create(
                id=cid,
                type="text",
                content=json.dumps([nid] if nid else []),
                parent_id=pid,
                alive=1
            )

        bridge_res = self.bridge.get_block_record_map(root_id)
        self.assertTrue(bridge_res.get("ok"))
        self.assertEqual(len(bridge_res["recordMap"]["block"]), 21)

    def test_05_deep_hierarchy_cascade_soft_delete(self):
        """Verifica que el soft-delete en cascada borre una jerarquía de 25 niveles sin agotar la recursión."""
        root_id = "cascade_deep_root_25"
        models.Block.create(
            id=root_id,
            type="page",
            content=json.dumps(["casc_1"]),
            alive=1
        )
        for i in range(1, 26):
            cid = f"casc_{i}"
            nid = f"casc_{i + 1}" if i < 25 else None
            pid = root_id if i == 1 else f"casc_{i - 1}"
            models.Block.create(
                id=cid,
                type="text",
                content=json.dumps([nid] if nid else []),
                parent_id=pid,
                alive=1
            )

        models.soft_delete_block(root_id)
        # Todos los 26 nodos deben tener alive == 0
        root = models.Block.get_by_id(root_id)
        self.assertEqual(root.alive, 0)
        for i in range(1, 26):
            blk = models.Block.get_by_id(f"casc_{i}")
            self.assertEqual(blk.alive, 0, f"casc_{i} debió ser marcado con alive=0")

    def test_06_wide_and_deep_hierarchy(self):
        """Verifica árbol ancho y profundo: 1 raíz -> 5 ramas -> 5 subramas -> 3 hojas (106 bloques)."""
        root_id = "tree_root_wide"
        branch_ids = [f"branch_{i}" for i in range(5)]
        models.Block.create(
            id=root_id,
            type="page",
            content=json.dumps(branch_ids),
            alive=1
        )

        all_ids = {root_id} | set(branch_ids)

        for b_id in branch_ids:
            sub_ids = [f"{b_id}_sub_{j}" for j in range(5)]
            all_ids.update(sub_ids)
            models.Block.create(
                id=b_id,
                type="column_list",
                content=json.dumps(sub_ids),
                parent_id=root_id,
                alive=1
            )
            for s_id in sub_ids:
                leaf_ids = [f"{s_id}_leaf_{k}" for k in range(3)]
                all_ids.update(leaf_ids)
                models.Block.create(
                    id=s_id,
                    type="column",
                    content=json.dumps(leaf_ids),
                    parent_id=b_id,
                    alive=1
                )
                for l_id in leaf_ids:
                    models.Block.create(
                        id=l_id,
                        type="text",
                        content="[]",
                        parent_id=s_id,
                        alive=1
                    )

        self.assertEqual(len(all_ids), 106)
        res = models.resolve_subtree_record_map(root_id)
        self.assertEqual(len(res["block"]), 106)

    # =========================================================================
    # 2. CYCLE ATTACKS AND CIRCULAR PARENT POINTERS
    # =========================================================================

    def test_07_direct_cycle_two_nodes(self):
        """Verifica que un ciclo directo A -> B -> A en content no cause un bucle infinito en BFS."""
        models.Block.create(
            id="cycle_a",
            type="page",
            content=json.dumps(["cycle_b"]),
            parent_id="cycle_b",
            alive=1
        )
        models.Block.create(
            id="cycle_b",
            type="text",
            content=json.dumps(["cycle_a"]),
            parent_id="cycle_a",
            alive=1
        )

        res = models.resolve_subtree_record_map("cycle_a")
        self.assertEqual(len(res["block"]), 2)
        self.assertIn("cycle_a", res["block"])
        self.assertIn("cycle_b", res["block"])

    def test_08_cycle_three_nodes(self):
        """Verifica ciclo de 3 nodos A -> B -> C -> A."""
        models.Block.create(id="c3_a", type="page", content=json.dumps(["c3_b"]), alive=1)
        models.Block.create(id="c3_b", type="text", content=json.dumps(["c3_c"]), parent_id="c3_a", alive=1)
        models.Block.create(id="c3_c", type="text", content=json.dumps(["c3_a"]), parent_id="c3_b", alive=1)

        res = models.resolve_subtree_record_map("c3_a")
        self.assertEqual(len(res["block"]), 3)
        self.assertEqual(set(res["block"].keys()), {"c3_a", "c3_b", "c3_c"})

    def test_09_self_referencing_block(self):
        """Verifica auto-referencia en content (A incluye a A)."""
        models.Block.create(
            id="self_ref",
            type="page",
            content=json.dumps(["self_ref"]),
            parent_id="self_ref",
            alive=1
        )
        res = models.resolve_subtree_record_map("self_ref")
        self.assertEqual(len(res["block"]), 1)
        self.assertIn("self_ref", res["block"])

    def test_10_backend_resolve_with_bidirectional_pointer_cycle(self):
        """Verifica resolve_block_record_map con punteros inversos de parent_id circulares."""
        models.Block.create(id="bi_a", type="page", content="[]", parent_id="bi_b", alive=1)
        models.Block.create(id="bi_b", type="text", content="[]", parent_id="bi_a", alive=1)

        rmap = backend.resolve_block_record_map("bi_a")
        self.assertEqual(len(rmap["block"]), 2)
        self.assertIn("bi_a", rmap["block"])
        self.assertIn("bi_b", rmap["block"])

    def test_11_create_block_api_rejects_self_parent(self):
        """Verifica que POST /api/blocks rechace asignar a un bloque a sí mismo como su propio padre."""
        # 1. Cuando el bloque padre ya existe y se intenta asignar parent_id == id -> 400
        models.Block.create(id="existing_self_node", type="text", alive=1)
        status, body = self._http_request('POST', '/api/blocks', {
            'id': 'existing_self_node',
            'parent_id': 'existing_self_node',
            'type': 'text'
        })
        self.assertEqual(status, 400)
        self.assertFalse(body.get('ok'))
        self.assertIn("Block cannot be its own parent", body.get('error', ''))

        # 2. Cuando el bloque padre no existe -> 404
        status_none, body_none = self._http_request('POST', '/api/blocks', {
            'id': 'nonexistent_self_node',
            'parent_id': 'nonexistent_self_node',
            'type': 'text'
        })
        self.assertEqual(status_none, 404)
        self.assertFalse(body_none.get('ok'))

    def test_12_create_block_api_rejects_ancestor_cycle(self):
        """Verifica que POST /api/blocks detecte ancestros circulares (A->B->C y C intenta adoptar A)."""
        # Crear A -> B -> C
        models.Block.create(id="anc_a", type="page", content=json.dumps(["anc_b"]), alive=1)
        models.Block.create(id="anc_b", type="column", content=json.dumps(["anc_c"]), parent_id="anc_a", alive=1)
        models.Block.create(id="anc_c", type="text", content="[]", parent_id="anc_b", alive=1)

        # Intentar crear/vincular 'anc_a' como hijo de 'anc_c'
        status, body = self._http_request('POST', '/api/blocks', {
            'id': 'anc_a',
            'parent_id': 'anc_c',
            'type': 'text'
        })
        self.assertEqual(status, 400)
        self.assertFalse(body.get('ok'))
        self.assertIn("Circular block hierarchy detected", body.get('error', ''))

    def test_13_cascade_soft_delete_under_circular_hierarchy(self):
        """Verifica que soft_delete_block no entre en bucle infinito si la DB contiene un ciclo."""
        models.Block.create(id="cyc_del_a", type="page", content=json.dumps(["cyc_del_b"]), alive=1)
        models.Block.create(id="cyc_del_b", type="text", content=json.dumps(["cyc_del_a"]), alive=1)

        models.soft_delete_block("cyc_del_a")
        blk_a = models.Block.get_by_id("cyc_del_a")
        blk_b = models.Block.get_by_id("cyc_del_b")
        self.assertEqual(blk_a.alive, 0)
        self.assertEqual(blk_b.alive, 0)

    # =========================================================================
    # 3. MALFORMED / CORRUPTED PAYLOADS IN JSON FIELDS
    # =========================================================================

    def test_14_corrupted_json_strings_in_block_fields(self):
        """Verifica que Block.to_dict() y resolve_subtree_record_map se recuperen ante cadenas JSON corruptas."""
        models.Block.create(
            id="corrupt_strings_block",
            type="text",
            properties="{broken: json, unquoted",
            content="[incomplete, 123",
            format="not json at all",
            crdt_data="!! corrupt crdt !!",
            permissions="not array",
            alive=1
        )

        blk = models.Block.get_by_id("corrupt_strings_block")
        data = blk.to_dict()
        self.assertIsInstance(data["properties"], dict)
        self.assertEqual(data["properties"], {})
        self.assertIsInstance(data["content"], list)
        self.assertEqual(data["content"], [])
        self.assertIsInstance(data["format"], dict)
        self.assertEqual(data["format"], {})
        self.assertIsInstance(data["crdt_data"], dict)
        self.assertEqual(data["crdt_data"], {})
        self.assertIsInstance(data["permissions"], list)
        self.assertEqual(data["permissions"], [])

        # resolve_subtree_record_map no debe fallar
        res = models.resolve_subtree_record_map("corrupt_strings_block")
        self.assertEqual(len(res["block"]), 1)

    def test_15_wrong_types_in_json_fields(self):
        """Verifica tolerancia cuando los campos JSON almacenan tipos inesperados (e.g. número en properties)."""
        models.Block.create(
            id="wrong_types_block",
            type="text",
            properties=json.dumps(12345),
            content=json.dumps({"not": "a list"}),
            format=json.dumps(["not a dict"]),
            crdt_data=json.dumps("string"),
            permissions=json.dumps({"not": "a list"}),
            alive=1
        )

        blk = models.Block.get_by_id("wrong_types_block")
        data = blk.to_dict()
        self.assertIsInstance(data["properties"], dict)
        self.assertEqual(data["properties"], {})
        self.assertIsInstance(data["content"], list)
        self.assertEqual(data["content"], [])
        self.assertIsInstance(data["format"], dict)
        self.assertEqual(data["format"], {})
        self.assertIsInstance(data["crdt_data"], dict)
        self.assertEqual(data["crdt_data"], {})
        self.assertIsInstance(data["permissions"], list)
        self.assertEqual(data["permissions"], [])

        res = models.resolve_subtree_record_map("wrong_types_block")
        self.assertEqual(len(res["block"]), 1)

    def test_16_none_null_values_in_fields(self):
        """Verifica que el ORM y to_dict manejen graciosamente valores None o vacíos sin lanzar excepciones."""
        # En memoria / objeto instanciado
        blk = models.Block(
            id="null_fields_block",
            type="text",
            properties=None,
            content=None,
            format=None,
            crdt_data=None,
            permissions=None,
            alive=1
        )
        data = blk.to_dict()
        self.assertIsInstance(data["properties"], dict)
        self.assertIsInstance(data["content"], list)
        self.assertIsInstance(data["format"], dict)

        # En base de datos, SQLite rechaza NULL en campos con NOT NULL constraint
        with self.assertRaises(IntegrityError):
            models.Block.create(
                id="null_db_block",
                type="text",
                properties=None,
                alive=1
            )

    def test_17_giant_properties_payload_via_api(self):
        """Prueba de estrés con payload gigante (~500KB - 1MB de propiedades JSON)."""
        giant_title = "A" * 200000
        giant_props = {
            "title": [[giant_title, [["b"]]]],
            "extra_metadata": {f"key_{i}": f"val_{i}" for i in range(1000)}
        }

        status, body = self._http_request('POST', '/api/blocks', {
            'id': 'giant_block_1',
            'type': 'page',
            'properties': giant_props
        })
        self.assertEqual(status, 201)
        self.assertTrue(body.get('ok'))

        # Consultar por ID
        status_get, body_get = self._http_request('GET', '/api/blocks/giant_block_1')
        self.assertEqual(status_get, 200)
        retrieved_title = body_get['block']['properties']['title'][0][0]
        self.assertEqual(len(retrieved_title), 200000)

    def test_18_corrupted_rich_text_decorator_tuples(self):
        """Verifica que el motor de rich_text no falle ante tuplas malformadas o tipos arbitrarios."""
        malformed_inputs = [
            None,
            "",
            12345,
            [["Válido", None]],
            [["Válido", "no_es_una_lista"]],
            [["Válido", [["h"]]]],                     # falta color
            [["Válido", [["a"]]]],                     # falta url
            [["Válido", [["e"]]]],                     # falta expresión latex
            [["Válido", [["unknown_tag", 1, 2, 3]]]],  # etiqueta desconocida con argumentos
            [[{"invalido": "objeto"}]],                # segmento no es lista
            ["no es tupla segmentada"],
            [["Texto", [42, None, ["b"]]]],            # elementos no lista dentro de decoradores
        ]

        for inp in malformed_inputs:
            # Ni to_html ni to_plain_text deben lanzar excepciones
            html_out = rich_text.rich_text_to_html(inp)
            self.assertIsInstance(html_out, str)
            plain_out = rich_text.rich_text_to_plain_text(inp)
            self.assertIsInstance(plain_out, str)

    def test_19_malformed_json_request_body_via_http(self):
        """Verifica que peticiones HTTP con cuerpos JSON inválidos devuelvan 400 Bad Request."""
        # 1. JSON sintácticamente roto
        status, body = self._http_request(
            'POST', '/api/blocks',
            raw_body=b'{"broken_json": true,'
        )
        self.assertEqual(status, 400)
        self.assertFalse(body.get('ok'))

        # 2. JSON que es un array en lugar de diccionario
        status, body = self._http_request(
            'POST', '/api/blocks',
            raw_body=b'[1, 2, 3]'
        )
        self.assertEqual(status, 400)
        self.assertFalse(body.get('ok'))

        # 3. Cuerpo vacío
        status, body = self._http_request(
            'POST', '/api/blocks',
            raw_body=b''
        )
        self.assertEqual(status, 400)
        self.assertFalse(body.get('ok'))

    # =========================================================================
    # 4. OPTIMISTIC CONCURRENCY COLLISIONS (409 CONFLICT)
    # =========================================================================

    def test_20_stale_expected_version_rejected_409(self):
        """Verifica que una actualización con expected_version obsoleto devuelva 409 Conflict."""
        # Crear bloque inicial (versión 1)
        status, b_init = self._http_request('POST', '/api/blocks', {
            'id': 'occ_block_20',
            'type': 'text',
            'properties': {'title': [['Original', []]]}
        })
        self.assertEqual(status, 201)
        self.assertEqual(b_init['block']['version'], 1)

        # Actualizar bloque legítimamente -> versión 2
        status_up, b_up = self._http_request('POST', '/api/blocks/occ_block_20', {
            'properties': {'title': [['Actualización V2', []]]}
        })
        self.assertEqual(status_up, 200)
        self.assertEqual(b_up['block']['version'], 2)

        # Cliente obsoleto intenta actualizar esperando versión 1
        status_stale, b_stale = self._http_request('POST', '/api/blocks/occ_block_20', {
            'expected_version': 1,
            'properties': {'title': [['Actualización con versión obsoleta', []]]}
        })
        self.assertEqual(status_stale, 409)
        self.assertFalse(b_stale.get('ok'))
        self.assertEqual(b_stale.get('error'), 'Version conflict')
        self.assertEqual(b_stale.get('current_version'), 2)
        self.assertEqual(b_stale.get('expected_version'), 1)

    def test_21_matching_expected_version_succeeds_200(self):
        """Verifica que una actualización con expected_version correcto incremente versión a 3 con 200 OK."""
        # Crear bloque (v1) y actualizar a v2
        self._http_request('POST', '/api/blocks', {'id': 'occ_block_21', 'type': 'text'})
        self._http_request('POST', '/api/blocks/occ_block_21', {'properties': {'title': [['V2', []]]}})

        status, body = self._http_request('POST', '/api/blocks/occ_block_21', {
            'expected_version': 2,
            'properties': {'title': [['Actualización exitosa V3', []]]}
        })
        self.assertEqual(status, 200)
        self.assertTrue(body.get('ok'))
        self.assertEqual(body['block']['version'], 3)
        self.assertEqual(body['block']['last_version'], 2)

    def test_22_query_parameter_expected_version_409(self):
        """Verifica que expected_version pasado en query parameter (?expected_version=...) detecte conflicto."""
        self._http_request('POST', '/api/blocks', {'id': 'occ_block_22', 'type': 'text'})

        status, body = self._http_request(
            'PUT', '/api/blocks/occ_block_22?expected_version=99',
            payload={'properties': {'title': [['Intento PUT', []]]}}
        )
        self.assertEqual(status, 409)
        self.assertFalse(body.get('ok'))
        self.assertEqual(body.get('error'), 'Version conflict')
        self.assertEqual(body.get('current_version'), 1)

    def test_23_concurrent_parallel_updates_stress(self):
        """Prueba de colisión concurrente: 10 hilos intentan actualizar el mismo bloque con expected_version=1.
        Exactamente 1 debe triunfar (200) y los otros 9 deben recibir 409 Conflict.
        """
        # Crear bloque en versión 1
        b_id = "concurrent_race_block"
        self._http_request('POST', '/api/blocks', {
            'id': b_id,
            'type': 'text',
            'properties': {'title': [['Race Start', []]]}
        })

        results = []

        def worker(thread_idx):
            payload = {
                'expected_version': 1,
                'properties': {'title': [[f"Ganador Hilo {thread_idx}", []]]}
            }
            status, res = self._http_request('POST', f"/api/blocks/{b_id}", payload)
            return status, res

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(worker, i) for i in range(10)]
            for f in futures:
                results.append(f.result())

        statuses = [r[0] for r in results]
        success_count = statuses.count(200)
        conflict_count = statuses.count(409)

        self.assertEqual(success_count, 1, f"Se esperaba exactamente 1 éxito (200), pero se obtuvo {success_count}. Estados: {statuses}")
        self.assertEqual(conflict_count, 9, f"Se esperaban exactamente 9 conflictos (409), pero se obtuvo {conflict_count}. Estados: {statuses}")

        # La versión final en la base de datos debe ser exactamente 2
        blk = models.Block.get_by_id(b_id)
        self.assertEqual(blk.version, 2)

    def test_24_invalid_expected_version_types(self):
        """Verifica que expected_version con valores inválidos (no enteros) se manejen sin error 500."""
        # Crear bloque
        self._http_request('POST', '/api/blocks', {'id': 'exp_type_test', 'type': 'text'})

        # String no entero
        status, body = self._http_request('POST', '/api/blocks/exp_type_test', {
            'expected_version': 'not_an_int',
            'properties': {'title': [['Test', []]]}
        })
        self.assertIn(status, [200, 400])

        # None
        status, body = self._http_request('POST', '/api/blocks/exp_type_test', {
            'expected_version': None,
            'properties': {'title': [['Test 2', []]]}
        })
        self.assertEqual(status, 200)

    # =========================================================================
    # 5. ORPHANED BLOCKS, CASCADE SOFT-DELETE, AND SELECTIVE RESTORATION
    # =========================================================================

    def test_25_cascade_soft_delete_multi_branch_tree(self):
        """Verifica el borrado en cascada lógico de un árbol jerárquico de 7 nodos."""
        # Root -> [Sec1, Sec2]
        # Sec1 -> [Text1A, Text1B]
        # Sec2 -> [Text2A, Text2B]
        models.Block.create(id="c_root", type="page", content=json.dumps(["c_sec1", "c_sec2"]), alive=1)
        models.Block.create(id="c_sec1", type="column", content=json.dumps(["c_t1a", "c_t1b"]), parent_id="c_root", alive=1)
        models.Block.create(id="c_sec2", type="column", content=json.dumps(["c_t2a", "c_t2b"]), parent_id="c_root", alive=1)
        models.Block.create(id="c_t1a", type="text", parent_id="c_sec1", alive=1)
        models.Block.create(id="c_t1b", type="text", parent_id="c_sec1", alive=1)
        models.Block.create(id="c_t2a", type="text", parent_id="c_sec2", alive=1)
        models.Block.create(id="c_t2b", type="text", parent_id="c_sec2", alive=1)

        status, body = self._http_request('DELETE', '/api/blocks/c_root')
        self.assertEqual(status, 200)
        self.assertTrue(body.get('ok'))
        self.assertEqual(body.get('alive'), 0)

        # Verificar que los 7 bloques tienen alive = 0 en SQLite
        all_ids = ["c_root", "c_sec1", "c_sec2", "c_t1a", "c_t1b", "c_t2a", "c_t2b"]
        for bid in all_ids:
            blk = models.Block.get_by_id(bid)
            self.assertEqual(blk.alive, 0, f"Bloque {bid} debió tener alive=0")

        # La raíz debe registrar la mutación de soft_delete en CRDT
        root_blk = models.Block.get_by_id("c_root")
        crdt = json.loads(root_blk.crdt_data or '{}')
        self.assertTrue(any(m.get('op') == 'soft_delete' for m in crdt.get('mutations', [])))

        # Las filas siguen existiendo físicamente en SQLite
        self.assertEqual(models.Block.select().where(models.Block.id.in_(all_ids)).count(), 7)

    def test_26_selective_restoration_with_dead_parent(self):
        """Verifica restauración selectiva de un hijo cuando su contenedor padre sigue en la papelera (alive=0)."""
        # Crear estructura con padre e hijo muertos
        models.Block.create(id="sel_parent_26", type="column", content="[]", alive=0)
        models.Block.create(id="sel_child_26", type="text", parent_id="sel_parent_26", alive=0)

        status, body = self._http_request('POST', '/api/blocks/sel_child_26/restore')
        self.assertEqual(status, 200)
        self.assertTrue(body.get('ok'))
        self.assertEqual(body.get('alive'), 1)

        # sel_child_26 ahora está vivo
        child = models.Block.get_by_id("sel_child_26")
        self.assertEqual(child.alive, 1)

        # El padre sel_parent_26 sigue muerto (alive=0)
        parent = models.Block.get_by_id("sel_parent_26")
        self.assertEqual(parent.alive, 0)

        # El padre NO debe contener a sel_child_26 en content porque sigue muerto
        parent_content = json.loads(parent.content or '[]')
        self.assertNotIn("sel_child_26", parent_content)

    def test_27_selective_restoration_after_parent_restoration(self):
        """Verifica que al restaurar al padre y luego restaurar a otro hijo, este se reinserta en content."""
        models.Block.create(id="sel_parent_27", type="column", content="[]", alive=0)
        models.Block.create(id="sel_child_27", type="text", parent_id="sel_parent_27", alive=0)

        # Restaurar al padre sel_parent_27
        status, _ = self._http_request('POST', '/api/blocks/sel_parent_27/restore')
        self.assertEqual(status, 200)

        # Ahora restaurar sel_child_27
        status_b, body_b = self._http_request('POST', '/api/blocks/sel_child_27/restore')
        self.assertEqual(status_b, 200)

        # sel_parent_27 ahora tiene a sel_child_27 en su array content
        parent = models.Block.get_by_id("sel_parent_27")
        parent_content = json.loads(parent.content or '[]')
        self.assertIn("sel_child_27", parent_content)

    def test_28_orphan_block_handling_and_reparenting(self):
        """Verifica que un bloque huérfano (parent_id fantasma) pueda consultarse y luego ser adoptado."""
        models.Block.create(
            id="orphan_block_1",
            type="text",
            properties=json.dumps({"title": [["Huérfano", []]]}),
            parent_id="ghost_parent_9999",
            alive=1
        )

        # Consultar huérfano individualmente
        status, body = self._http_request('GET', '/api/blocks/orphan_block_1')
        self.assertEqual(status, 200)
        self.assertEqual(body['block']['id'], 'orphan_block_1')

        # Consultar su recordMap
        status_rm, body_rm = self._http_request('GET', '/api/blocks/orphan_block_1/recordMap')
        self.assertEqual(status_rm, 200)
        self.assertIn('orphan_block_1', body_rm['recordMap']['block'])

        # Crear nuevo padre adoptivo
        models.Block.create(id="adoptive_parent", type="page", content="[]", alive=1)

        # Adoptar al huérfano mediante reorder
        status_re, body_re = self._http_request('POST', '/api/blocks/adoptive_parent/reorder', {
            'child_id': 'orphan_block_1'
        })
        self.assertEqual(status_re, 200)

        # Verificar adopción
        parent = models.Block.get_by_id("adoptive_parent")
        self.assertIn("orphan_block_1", json.loads(parent.content or '[]'))

        child = models.Block.get_by_id("orphan_block_1")
        self.assertEqual(child.parent_id, "adoptive_parent")

    def test_29_child_soft_delete_updates_parent_content(self):
        """Verifica que el borrado lógico de un hijo actualice el array content del contenedor padre."""
        models.Block.create(
            id="parent_content_test",
            type="page",
            content=json.dumps(["child_del_1", "child_del_2", "child_del_3"]),
            alive=1
        )
        models.Block.create(id="child_del_1", type="text", parent_id="parent_content_test", alive=1)
        models.Block.create(id="child_del_2", type="text", parent_id="parent_content_test", alive=1)
        models.Block.create(id="child_del_3", type="text", parent_id="parent_content_test", alive=1)

        # Borrar hijo 2
        status, body = self._http_request('DELETE', '/api/blocks/child_del_2')
        self.assertEqual(status, 200)

        # El padre ahora solo tiene 1 y 3 en content
        parent = models.Block.get_by_id("parent_content_test")
        p_content = json.loads(parent.content or '[]')
        self.assertEqual(p_content, ["child_del_1", "child_del_3"])

        # La versión del padre debió incrementarse
        self.assertTrue(parent.version > 1)

    # =========================================================================
    # 6. SQL INJECTION HARDENING
    # =========================================================================

    def test_30_sql_injection_in_block_id_lookup(self):
        """Verifica resistencia contra inyección SQL en la consulta de bloque por ID."""
        malicious_ids = [
            "' OR '1'='1",
            "root'; DROP TABLE block; --",
            "1 UNION SELECT * FROM block --",
            "../../../../etc/passwd",
            "admin'--",
            "1'; SELECT SLEEP(5); --"
        ]

        for m_id in malicious_ids:
            enc_id = urllib.parse.quote(m_id)
            status, body = self._http_request('GET', f"/api/blocks/{enc_id}")
            self.assertIn(status, [400, 404])
            self.assertFalse(body.get('ok'))

        # Asegurar que la tabla block no fue eliminada ni alterada
        self.assertTrue(models.Block.table_exists())

    def test_31_sql_injection_in_record_map(self):
        """Verifica que inyecciones SQL en /recordMap no alteren la base de datos."""
        m_id = urllib.parse.quote("'; DROP TABLE block; --")
        status, body = self._http_request('GET', f"/api/blocks/{m_id}/recordMap")
        self.assertIn(status, [400, 404])
        self.assertTrue(models.Block.table_exists())

        # Probar en /api/notes/<id>/recordMap
        status_note, body_note = self._http_request('GET', f"/api/notes/{m_id}/recordMap")
        self.assertIn(status_note, [400, 404])
        self.assertTrue(models.Block.table_exists())
        self.assertTrue(models.Note.table_exists())

    def test_32_sql_injection_in_delete_endpoint(self):
        """Verifica que DELETE /api/blocks/<injected_id> no borre masivamente la base de datos."""
        # Crear bloque legítimo
        models.Block.create(id="safe_block_to_keep", type="page", alive=1)

        m_id = urllib.parse.quote("' OR 1=1; --")
        status, body = self._http_request('DELETE', f"/api/blocks/{m_id}")
        self.assertIn(status, [400, 404])

        # El bloque seguro debe seguir existiendo intacto
        safe_blk = models.Block.get_or_none(models.Block.id == "safe_block_to_keep")
        self.assertIsNotNone(safe_blk)
        self.assertEqual(safe_blk.alive, 1)

    def test_33_sql_injection_in_block_properties(self):
        """Verifica que cadenas de inyección SQL en properties, format y título se almacenen como texto plano sin ejecutar SQL."""
        injection_props = {
            "title": [["'); DROP TABLE block; --", []]],
            "sql_attack": "SELECT * FROM notes WHERE '1'='1'",
        }
        injection_format = {
            "color": "red'; DROP TABLE notes; --"
        }

        status, body = self._http_request('POST', '/api/blocks', {
            'id': 'sqli_prop_block',
            'type': 'code',
            'properties': injection_props,
            'format': injection_format
        })
        self.assertEqual(status, 201)

        # Consultar y verificar preservación literal
        status_get, body_get = self._http_request('GET', '/api/blocks/sqli_prop_block')
        self.assertEqual(status_get, 200)
        retrieved_props = body_get['block']['properties']
        self.assertEqual(retrieved_props['title'][0][0], "'); DROP TABLE block; --")
        self.assertEqual(body_get['block']['format']['color'], "red'; DROP TABLE notes; --")

        # Ambas tablas siguen vivas
        self.assertTrue(models.Block.table_exists())
        self.assertTrue(models.Note.table_exists())

    def test_34_sql_injection_in_legacy_note_blocks_endpoint(self):
        """Verifica que /api/notes/<id>/blocks maneje inyecciones SQL en note_id devolviendo 400."""
        m_id = urllib.parse.quote("' OR 1=1 --")
        status, body = self._http_request('GET', f"/api/notes/{m_id}/blocks")
        self.assertEqual(status, 400)
        self.assertFalse(body.get('ok'))


if __name__ == '__main__':
    unittest.main()
