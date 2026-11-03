#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitarios y de integración para Milestone 1:
- Esquema DDL y modelo Peewee de Block (16 campos Notion + compatibilidad legacy)
- Persistencia bidireccional jerárquica (add, move, reorder)
- Borrado lógico (alive = 0) y restauración (alive = 1)
- Versionado optimista y registro local de mutaciones CRDT
- Recorrido BFS de subárbol con detección de ciclos (resolve_subtree_record_map)
- Migración automática, no destructiva e idempotente de notas legacy
- Vista SQL de compatibilidad 'blocks'
"""

import os
import json
import time
import tempfile
import unittest
import datetime
from peewee import SqliteDatabase
import models


class TestBlockSchemaAndMigration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = os.path.join(cls.temp_dir.name, 'test_m1.db')
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

    @classmethod
    def tearDownClass(cls):
        try:
            cls.test_db.close()
        except Exception:
            pass
        cls.temp_dir.cleanup()
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

    # -------------------------------------------------------------------------
    # 1. Validación del Esquema DDL de 16 Campos Notion + Compatibilidad
    # -------------------------------------------------------------------------

    def test_block_16_field_schema_and_defaults(self):
        """Verifica que el modelo Block posea la tabla 'block', todos los 16 campos Notion y campos legacy."""
        self.assertEqual(models.Block._meta.table_name, 'block')

        expected_notion_fields = [
            'id', 'space_id', 'version', 'last_version', 'type',
            'properties', 'content', 'parent_id', 'parent_table',
            'alive', 'format', 'crdt_format_version', 'crdt_data',
            'created_time', 'last_edited_time', 'permissions'
        ]
        for field in expected_notion_fields:
            self.assertIn(field, models.Block._meta.fields, f"Campo Notion faltante: {field}")

        expected_legacy_fields = ['note_id', 'sort_index', 'created_at', 'updated_at']
        for field in expected_legacy_fields:
            self.assertIn(field, models.Block._meta.fields, f"Campo legacy faltante: {field}")

        # Instanciar con mínimos argumentos y verificar defaults canónicos
        blk = models.Block.create(id='test-minimal-block')
        self.assertEqual(blk.space_id, 'default_space')
        self.assertEqual(blk.version, 1)
        self.assertEqual(blk.last_version, 1)
        self.assertEqual(blk.type, 'text')
        self.assertEqual(blk.properties, '{}')
        self.assertEqual(blk.content, '[]')
        self.assertIsNone(blk.parent_id)
        self.assertEqual(blk.parent_table, 'block')
        self.assertEqual(blk.alive, 1)
        self.assertEqual(blk.format, '{}')
        self.assertEqual(blk.crdt_format_version, 1)
        self.assertEqual(blk.crdt_data, '{}')
        self.assertGreater(blk.created_time, 0)
        self.assertGreater(blk.last_edited_time, 0)
        self.assertEqual(blk.permissions, '[]')
        self.assertEqual(blk.sort_index, 'a0')

    def test_block_to_dict_full_notion_and_legacy_keys(self):
        """Verifica que to_dict() exponga todas las claves canónicas de Notion y las claves legacy."""
        blk = models.Block.create(
            id='blk-to-dict-1',
            space_id='custom_space',
            version=3,
            last_version=2,
            type='header',
            properties=json.dumps({'title': [['Encabezado Principal', [['b']]]]}, ensure_ascii=False),
            content=json.dumps(['child-1', 'child-2']),
            parent_id='parent-root',
            parent_table='block',
            alive=1,
            format=json.dumps({'color': 'blue'}),
            crdt_format_version=1,
            crdt_data=json.dumps({'clock': 5}),
            created_time=1730000000000,
            last_edited_time=1730005000000,
            permissions=json.dumps([{'role': 'editor'}]),
            note_id=42,
            sort_index='a1',
        )

        d = blk.to_dict()

        # 16 claves canónicas Notion
        self.assertEqual(d['id'], 'blk-to-dict-1')
        self.assertEqual(d['space_id'], 'custom_space')
        self.assertEqual(d['version'], 3)
        self.assertEqual(d['last_version'], 2)
        self.assertEqual(d['type'], 'header')
        self.assertEqual(d['properties'], {'title': [['Encabezado Principal', [['b']]]]})
        self.assertEqual(d['content'], ['child-1', 'child-2'])
        self.assertEqual(d['parent_id'], 'parent-root')
        self.assertEqual(d['parent_table'], 'block')
        self.assertEqual(d['alive'], 1)
        self.assertEqual(d['format'], {'color': 'blue'})
        self.assertEqual(d['crdt_format_version'], 1)
        self.assertEqual(d['crdt_data'], {'clock': 5})
        self.assertEqual(d['created_time'], 1730000000000)
        self.assertEqual(d['last_edited_time'], 1730005000000)
        self.assertEqual(d['permissions'], [{'role': 'editor'}])

        # Claves legacy
        self.assertEqual(d['noteId'], 42)
        self.assertEqual(d['parentId'], 'parent-root')
        self.assertEqual(d['sortIndex'], 'a1')
        self.assertIn('createdAt', d)
        self.assertIn('updatedAt', d)
        self.assertEqual(d['title'], 'Encabezado Principal')

    def test_block_to_dict_subpage_keys(self):
        """Verifica que bloques sub_page expongan page_id y title plano en to_dict."""
        blk = models.Block.create(
            id='blk-sub-test',
            type='sub_page',
            properties=json.dumps({'page_id': 'target-note-88', 'title': 'Mi Subnota'}),
        )
        d = blk.to_dict()
        self.assertEqual(d['type'], 'sub_page')
        self.assertEqual(d['page_id'], 'target-note-88')
        self.assertEqual(d['title'], 'Mi Subnota')

    # -------------------------------------------------------------------------
    # 2. Persistencia Jerárquica y Consistencia Bidireccional
    # -------------------------------------------------------------------------

    def test_bidirectional_consistency_add_child(self):
        """Verifica add_child_block: actualización atómica de parent.content y child.parent_id."""
        parent = models.Block.create(
            id='page-parent-1',
            type='page',
            properties=json.dumps({'title': [['Página Contenedora', []]]}),
            content='[]',
            version=1,
        )

        child = models.add_child_block(
            parent_id=parent.id,
            child_data={
                'id': 'child-text-1',
                'type': 'text',
                'properties': {'title': [['Primer Párrafo', []]]},
            }
        )

        # Verificar hijo
        self.assertEqual(child.id, 'child-text-1')
        self.assertEqual(child.parent_id, parent.id)
        self.assertEqual(child.parent_table, 'block')
        self.assertEqual(child.alive, 1)

        # Verificar padre
        parent_updated = models.Block.get_by_id(parent.id)
        parent_content = json.loads(parent_updated.content)
        self.assertEqual(parent_content, ['child-text-1'])
        self.assertEqual(parent_updated.version, 2)
        self.assertEqual(parent_updated.last_version, 1)

        # Verificar mutación CRDT registrada en el padre
        crdt = json.loads(parent_updated.crdt_data)
        self.assertTrue(len(crdt.get('mutations', [])) > 0)
        self.assertEqual(crdt['mutations'][-1]['op'], 'add_child')
        self.assertEqual(crdt['mutations'][-1]['child_id'], 'child-text-1')

        # Insertar con índice específico
        models.add_child_block(
            parent_id=parent.id,
            child_data={'id': 'child-text-0', 'type': 'text'},
            index=0
        )
        parent_updated = models.Block.get_by_id(parent.id)
        parent_content = json.loads(parent_updated.content)
        self.assertEqual(parent_content, ['child-text-0', 'child-text-1'])
        self.assertEqual(parent_updated.version, 3)

    def test_bidirectional_consistency_reorder_children(self):
        """Verifica reorder_children: actualiza el array content y version del padre."""
        parent = models.Block.create(
            id='page-reorder',
            type='page',
            content='[]',
            version=1,
        )
        models.add_child_block(parent.id, {'id': 'b1'})
        models.add_child_block(parent.id, {'id': 'b2'})
        models.add_child_block(parent.id, {'id': 'b3'})

        reordered = models.reorder_children(parent.id, ['b3', 'b1', 'b2'])
        content = json.loads(reordered.content)
        self.assertEqual(content, ['b3', 'b1', 'b2'])
        self.assertGreater(reordered.version, 3)

        crdt = json.loads(reordered.crdt_data)
        self.assertEqual(crdt['mutations'][-1]['op'], 'reorder_children')
        self.assertEqual(crdt['mutations'][-1]['order'], ['b3', 'b1', 'b2'])

    def test_bidirectional_consistency_move_between_parents(self):
        """Verifica move_child_block: traslado atómico entre diferentes padres y actualización de punteros."""
        p_src = models.Block.create(id='parent-source', type='page', content='[]', version=1)
        p_dst = models.Block.create(id='parent-target', type='page', content='[]', version=1)

        c1 = models.add_child_block(p_src.id, {'id': 'item-to-move', 'type': 'text'})
        self.assertEqual(json.loads(models.Block.get_by_id(p_src.id).content), ['item-to-move'])
        self.assertEqual(json.loads(models.Block.get_by_id(p_dst.id).content), [])

        # Mover a p_dst en índice 0
        moved = models.move_child_block(c1.id, p_dst.id, index=0)

        # Verificar hijo
        self.assertEqual(moved.parent_id, p_dst.id)
        self.assertEqual(moved.parent_table, 'block')

        # Verificar padre origen
        p_src_after = models.Block.get_by_id(p_src.id)
        self.assertEqual(json.loads(p_src_after.content), [])
        crdt_src = json.loads(p_src_after.crdt_data)
        self.assertEqual(crdt_src['mutations'][-1]['op'], 'remove_child')

        # Verificar padre destino
        p_dst_after = models.Block.get_by_id(p_dst.id)
        self.assertEqual(json.loads(p_dst_after.content), ['item-to-move'])
        crdt_dst = json.loads(p_dst_after.crdt_data)
        self.assertEqual(crdt_dst['mutations'][-1]['op'], 'add_child')

    # -------------------------------------------------------------------------
    # 3. Borrado Lógico (alive = 0) y Restauración (alive = 1)
    # -------------------------------------------------------------------------

    def test_soft_delete_preserves_row_and_removes_from_parent(self):
        """Verifica que soft_delete_block establezca alive = 0 manteniendo la fila en SQLite y desvinculando del padre."""
        parent = models.Block.create(id='p-del', type='page', content='[]', version=1)
        child = models.add_child_block(parent.id, {'id': 'c-del', 'type': 'text'})

        # Borrado lógico
        deleted = models.soft_delete_block(child.id)
        self.assertEqual(deleted.alive, 0)
        self.assertEqual(deleted.id, 'c-del')

        # Comprobar persistencia física en SQLite (NO DEBE SER BORRADO)
        row = models.Block.get_or_none(models.Block.id == 'c-del')
        self.assertIsNotNone(row)
        self.assertEqual(row.alive, 0)

        # Comprobar desvinculación visual del padre
        p_after = models.Block.get_by_id(parent.id)
        self.assertEqual(json.loads(p_after.content), [])

    def test_restore_block_reactivates_alive_and_relinks_parent(self):
        """Verifica restore_block: reactiva alive = 1 y re-inserta el ID en el padre."""
        parent = models.Block.create(id='p-restore', type='page', content='[]', version=1)
        child = models.add_child_block(parent.id, {'id': 'c-restore', 'type': 'text'})

        models.soft_delete_block(child.id)
        self.assertEqual(models.Block.get_by_id(child.id).alive, 0)
        self.assertEqual(json.loads(models.Block.get_by_id(parent.id).content), [])

        # Restaurar
        restored = models.restore_block(child.id)
        self.assertEqual(restored.alive, 1)

        # Comprobar que volvió al content del padre
        p_after = models.Block.get_by_id(parent.id)
        self.assertIn('c-restore', json.loads(p_after.content))

    # -------------------------------------------------------------------------
    # 4. Recorrido BFS de Subárbol y Detección de Ciclos
    # -------------------------------------------------------------------------

    def test_resolve_subtree_record_map_bfs_and_cycle_prevention(self):
        """Verifica resolve_subtree_record_map con recorrido BFS y protección contra referencias circulares."""
        root = models.Block.create(id='root-page', type='page', content='[]')
        col_list = models.add_child_block(root.id, {'id': 'col-list-1', 'type': 'column_list'})
        col1 = models.add_child_block(col_list.id, {'id': 'col-1', 'type': 'column'})
        text1 = models.add_child_block(col1.id, {'id': 'text-1', 'type': 'text'})

        # Resolver mapa de registros
        rmap = models.resolve_subtree_record_map(root.id)
        self.assertIn('block', rmap)
        block_dict = rmap['block']

        self.assertIn('root-page', block_dict)
        self.assertIn('col-list-1', block_dict)
        self.assertIn('col-1', block_dict)
        self.assertIn('text-1', block_dict)

        self.assertEqual(block_dict['root-page']['role'], 'editor')
        self.assertEqual(block_dict['text-1']['value']['id'], 'text-1')

        # Prueba de ciclo forzado (text1 contiene a root-page en su content)
        text1.content = json.dumps(['root-page'])
        text1.save()

        # Debe resolver sin entrar en ciclo infinito ni lanzar RecursionError
        rmap_cycle = models.resolve_subtree_record_map(root.id)
        self.assertIn('root-page', rmap_cycle['block'])
        self.assertEqual(len(rmap_cycle['block']), 4)

    # -------------------------------------------------------------------------
    # 5. Migración Automática, Idempotente y No Destructiva de Notas Legacy
    # -------------------------------------------------------------------------

    def test_migrate_legacy_notes_to_blocks_preserves_content_and_idempotency(self):
        """Verifica que migrate_legacy_notes_to_blocks transforme notas en páginas y bloques hijos preservando notas."""
        now_ms = int(time.time() * 1000)

        # Crear nota preexistente con HTML estructurado
        legacy_html = (
            "<h1>Título Sección</h1>"
            "<p>Este es el párrafo principal de la nota legacy.</p>"
            '<div class="block-subpage" data-page-id="note-999" data-title="Subnota Enlazada">📄 Subnota Enlazada</div>'
            "<pre><code class=\"language-python\">def hola(): print('mundo')</code></pre>"
            "<hr>"
        )
        note = models.Note.create(
            id=101,
            title="Nota de Prueba Migración",
            folder="Trabajo",
            tags="arquitectura, notion",
            content=legacy_html,
            updated_at=now_ms,
            data_json=json.dumps({'emoji': '🚀', 'hasCover': True, 'coverStyle': 'linear-gradient(to right, red, blue)'})
        )

        # Ejecutar migración
        res = models.migrate_legacy_notes_to_blocks()
        self.assertTrue(res.get('ok'))
        self.assertGreaterEqual(res.get('migratedCount'), 1)

        # 1. Verificar bloque raíz page
        page_block = models.Block.get_or_none(models.Block.id == '101')
        self.assertIsNotNone(page_block)
        self.assertEqual(page_block.type, 'page')
        self.assertEqual(page_block.parent_table, 'space')
        self.assertIsNone(page_block.parent_id)

        # Título enriquecido y formato visual preservados
        p_dict = page_block.to_dict()
        self.assertEqual(p_dict['title'], "Nota de Prueba Migración")
        self.assertEqual(p_dict['format'].get('page_icon'), '🚀')
        self.assertEqual(p_dict['format'].get('folder'), 'Trabajo')
        self.assertIn('page_cover', p_dict['format'])

        # 2. Verificar bloques hijos generados y vinculados en content
        child_ids = p_dict['content']
        self.assertGreaterEqual(len(child_ids), 4)

        header_blk = models.Block.get_or_none(models.Block.id == child_ids[0])
        self.assertIsNotNone(header_blk)
        self.assertEqual(header_blk.type, 'header')
        self.assertEqual(header_blk.to_dict()['title'], 'Título Sección')

        text_blk = models.Block.get_or_none(models.Block.id == child_ids[1])
        self.assertIsNotNone(text_blk)
        self.assertEqual(text_blk.type, 'text')
        self.assertIn('párrafo principal', text_blk.to_dict()['title'])

        subpage_blk = models.Block.get_or_none(models.Block.id == child_ids[2])
        self.assertIsNotNone(subpage_blk)
        self.assertEqual(subpage_blk.type, 'sub_page')
        self.assertEqual(subpage_blk.to_dict()['page_id'], 'note-999')

        code_blk = models.Block.get_or_none(models.Block.id == child_ids[3])
        self.assertIsNotNone(code_blk)
        self.assertEqual(code_blk.type, 'code')
        self.assertEqual(code_blk.to_dict()['format'].get('language'), 'python')

        # 3. Verificar que la tabla notes original permanece 100% intacta
        note_in_db = models.Note.get_by_id(101)
        self.assertEqual(note_in_db.title, "Nota de Prueba Migración")
        self.assertEqual(note_in_db.content, legacy_html)

        # 4. Verificar idempotencia: una segunda ejecución no crea duplicados
        count_before = models.Block.select().count()
        res_idempotent = models.migrate_legacy_notes_to_blocks()
        self.assertTrue(res_idempotent.get('ok'))
        self.assertEqual(res_idempotent.get('migratedCount'), 0)
        self.assertEqual(models.Block.select().count(), count_before)

    # -------------------------------------------------------------------------
    # 6. Vista SQL de Compatibilidad 'blocks' y Operaciones ORM Legacy
    # -------------------------------------------------------------------------

    def test_sqlite_compatibility_view_blocks(self):
        """Verifica que la vista SQL 'blocks' permita consultar de forma transparente la tabla 'block'."""
        blk = models.Block.create(id='view-test-block', type='text', sort_index='b0')

        cursor = self.test_db.execute_sql("SELECT id, type, sort_index FROM blocks WHERE id = ?", ('view-test-block',))
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], 'view-test-block')
        self.assertEqual(row[1], 'text')
        self.assertEqual(row[2], 'b0')

    def test_legacy_block_operations_compatibility(self):
        """Verifica que las funciones get_note_blocks_orm, update_block_order_orm y sync sigan funcionando."""
        note_id = 777
        payload = [
            {'id': 'legacy-b1', 'type': 'sub_page', 'page_id': 'target-1', 'title': 'Sub 1', 'sortIndex': 'a0'},
            {'id': 'legacy-b2', 'type': 'p', 'properties': {'text': 'Hola mundo'}, 'sortIndex': 'a1'},
        ]
        sync_res = models.sync_blocks_from_note_html_orm(note_id, payload)
        self.assertTrue(sync_res['ok'])
        self.assertEqual(sync_res['syncedCount'], 2)

        blocks_res = models.get_note_blocks_orm(note_id)
        self.assertTrue(blocks_res['ok'])
        self.assertEqual(len(blocks_res['blocks']), 2)
        self.assertEqual(blocks_res['blocks'][0]['id'], 'legacy-b1')
        self.assertEqual(blocks_res['blocks'][0]['page_id'], 'target-1')


if __name__ == '__main__':
    unittest.main()
