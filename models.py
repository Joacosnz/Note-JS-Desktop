#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Note JS — Capa de Datos ORM con SQLite + Peewee
Define los modelos relacionales (Note, Folder, Setting) y las transacciones atómicas.
"""

import os
import sys
import re
import html
import datetime
import json
import time
import base64
import mimetypes
import threading
import urllib.request
from urllib.parse import unquote, urlparse
from peewee import (
    SqliteDatabase,
    Model,
    AutoField,
    IntegerField,
    CharField,
    TextField,
)


def get_data_dir():
    """Obtiene el directorio de escritura para la base de datos SQLite notejs.db."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


DATA_DIR = get_data_dir()
DB_PATH = os.path.join(DATA_DIR, 'notejs.db')
DB_LOCK = threading.Lock()

# Configuración de SQLite + Peewee con modo WAL resiliente y timeout contra bloqueos
db = SqliteDatabase(
    DB_PATH,
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -64000,  # 64MB cache
        'foreign_keys': 1,
        'synchronous': 1,      # Normal en lugar de 0 para prevenir corrupción de archivos
        'busy_timeout': 10000, # 10 segundos de tolerancia a bloqueos concurrentes
    },
    timeout=15,
    check_same_thread=False,
)


class BaseModel(Model):
    class Meta:
        database = db


class Note(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField(max_length=500, default='Sin título')
    folder = CharField(max_length=120, index=True, default='Personal')
    tags = TextField(default='')
    is_pinned = IntegerField(default=0, index=True)
    content = TextField(default='')
    updated_at = IntegerField(default=0, index=True)
    data_json = TextField(default='{}')

    class Meta:
        table_name = 'notes'

    def to_dict(self):
        """Serializa el modelo Peewee Note al formato JSON esperado por el frontend."""
        try:
            extra = json.loads(self.data_json or '{}')
        except Exception:
            extra = {}

        note = dict(extra)
        note['id'] = self.id
        note['title'] = self.title
        note['folder'] = self.folder
        note['tags'] = self.tags
        note['isPinned'] = bool(self.is_pinned)
        note['content'] = self.content
        note['updatedAt'] = self.updated_at
        return note


class NoteHistory(BaseModel):
    id = AutoField(primary_key=True)
    note_id = IntegerField(index=True)
    title = CharField(max_length=500, default='Sin título')
    folder = CharField(max_length=120, default='Personal')
    tags = TextField(default='')
    content = TextField(default='')
    summary = CharField(max_length=255, default='Edición guardada')
    created_at = IntegerField(default=0, index=True)
    snapshot_json = TextField(default='{}')

    class Meta:
        table_name = 'note_history'

    def to_dict(self):
        """Serializa una versión histórica de la nota almacenada en SQLite."""
        try:
            snapshot = json.loads(self.snapshot_json or '{}')
        except Exception:
            snapshot = {}

        return {
            'id': self.id,
            'noteId': self.note_id,
            'title': self.title,
            'folder': self.folder,
            'tags': self.tags,
            'content': self.content,
            'summary': self.summary,
            'createdAt': self.created_at,
            'snapshot': snapshot,
        }


DEFAULT_FOLDER_EMOJIS = {
    'Personal': '🏠',
    'Trabajo': '💼',
    'Universidad': '🎓',
    'Ideas': '💡',
}


class Folder(BaseModel):
    name = CharField(primary_key=True, max_length=200)
    parent_name = CharField(max_length=200, default='', index=True)
    emoji = CharField(max_length=32, default='📁')
    sort_order = IntegerField(default=0, index=True)
    is_smart = IntegerField(default=0)
    smart_rules_json = TextField(default='')

    class Meta:
        table_name = 'folders'

    def to_dict(self):
        parts = [p.strip() for p in str(self.name or '').split('/') if p.strip()]
        derived_parent = '/'.join(parts[:-1]) if len(parts) > 1 else ''
        smart_cfg = None
        if self.is_smart and self.smart_rules_json:
            try:
                smart_cfg = json.loads(self.smart_rules_json)
            except Exception:
                smart_cfg = None
        return {
            'name': self.name,
            'parentName': '' if self.is_smart else (self.parent_name or derived_parent),
            'emoji': self.emoji or DEFAULT_FOLDER_EMOJIS.get(self.name, '⚙️' if self.is_smart else '📁'),
            'sortOrder': self.sort_order,
            'isSmart': bool(self.is_smart),
            'smartConfig': smart_cfg,
        }


class Setting(BaseModel):
    key = CharField(primary_key=True, max_length=120)
    value = TextField(default='')

    class Meta:
        table_name = 'settings'


BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def generate_key_between(a: str = None, b: str = None) -> str:
    """
    Genera una clave de orden fraccionario (Fractional Indexing) lexicográficamente
    estrictamente entre `a` y `b`.
    Garantiza: (a is None or a < resultado) y (b is None or resultado < b).
    Permite mover cualquier bloque con una única actualización O(1) de una sola fila en SQLite.
    """
    if a is not None and b is not None and a >= b:
        # Si por desincronización llegan invertidas o iguales, genera sufijo único
        return a + "V"

    if a is None and b is None:
        return "a0"
    if a is None:
        prefix = ""
        for char in b:
            if char not in BASE62:
                continue
            idx = BASE62.index(char)
            if idx > 0:
                mid = BASE62[idx // 2]
                return prefix + mid
            prefix += char
        return "0" + (b or "")
    if b is None:
        head = a[0] if len(a) > 0 and a[0] in BASE62 else "a"
        idx = BASE62.index(head)
        if idx < len(BASE62) - 1:
            mid = BASE62[(idx + len(BASE62)) // 2]
            return mid
        return a + "V"

    prefix = ""
    i = 0
    while True:
        char_a = a[i] if i < len(a) and a[i] in BASE62 else "0"
        char_b = b[i] if i < len(b) and b[i] in BASE62 else "z"
        idx_a = BASE62.index(char_a)
        idx_b = BASE62.index(char_b)

        if idx_b - idx_a > 1:
            mid_idx = (idx_a + idx_b) // 2
            return prefix + BASE62[mid_idx]
        elif idx_b - idx_a == 1:
            prefix += char_a
            i += 1
            tail_a = a[i] if i < len(a) and a[i] in BASE62 else "0"
            idx_tail_a = BASE62.index(tail_a)
            if idx_tail_a < len(BASE62) - 1:
                mid_idx = (idx_tail_a + len(BASE62)) // 2
                return prefix + BASE62[mid_idx]
            else:
                return prefix + "V"
        else:
            prefix += char_a
            i += 1
            if i >= len(a) and i >= len(b):
                return prefix + "V"


class Block(BaseModel):
    """
    Entidad Block de Notion en SQLite.
    Cada párrafo, imagen, columna, llamada o lista es una fila independiente,
    con jerarquía anidada (parent_id) y ordenamiento fraccionario (sort_index).
    """
    id = CharField(primary_key=True, max_length=64)
    note_id = IntegerField(index=True)
    parent_id = CharField(max_length=64, null=True, index=True)
    type = CharField(max_length=64, default='p')
    properties = TextField(default='{}')
    sort_index = CharField(max_length=64, index=True, default='a0')
    created_at = IntegerField(default=0)
    updated_at = IntegerField(default=0)

    class Meta:
        table_name = 'blocks'

    def to_dict(self):
        try:
            props = json.loads(self.properties or '{}')
        except Exception:
            props = {}
        return {
            'id': self.id,
            'noteId': self.note_id,
            'parentId': self.parent_id,
            'type': self.type,
            'properties': props,
            'sortIndex': self.sort_index,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at,
        }


class ReminderItem(BaseModel):
    """
    Entidad de Recordatorios y Eventos de Calendario en SQLite.
    Migrado de ReminderEntity / CalendarEvent de Android a Python + Peewee ORM para PC.
    """
    id = IntegerField(primary_key=True)
    title = CharField(max_length=500, default='Recordatorio')
    date_str = CharField(max_length=32, index=True, default='')  # YYYY-MM-DD
    time_str = CharField(max_length=64, default='Todo el día')
    category = CharField(max_length=120, default='Trabajo')
    completed = IntegerField(default=0, index=True)
    priority = IntegerField(default=0)  # 0=Ninguna, 1=Baja, 2=Media, 3=Urgente
    notes = TextField(default='')
    recurrence = CharField(max_length=32, default='NONE')
    subtasks_json = TextField(default='[]')
    linked_note_id = IntegerField(null=True, index=True)
    created_at = IntegerField(default=0)
    updated_at = IntegerField(default=0, index=True)

    class Meta:
        table_name = 'reminders'

    def to_dict(self):
        try:
            subtasks = json.loads(self.subtasks_json or '[]')
        except Exception:
            subtasks = []
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date_str,
            'time': self.time_str,
            'category': self.category,
            'completed': bool(self.completed),
            'priority': self.priority,
            'notes': self.notes,
            'recurrence': self.recurrence,
            'subtasks': subtasks,
            'linkedNoteId': self.linked_note_id,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at,
        }


class WebLinkCache(BaseModel):
    """
    Caché de Metadatos de Enlaces Web (OpenGraph) en SQLite.
    Migrado de WebLinkCacheEntity / WebLinkMetadataFetcher de Android a Python + Peewee ORM.
    """
    url = CharField(primary_key=True, max_length=1000)
    domain = CharField(max_length=255, default='')
    title = CharField(max_length=500, default='')
    description = TextField(default='')
    image_url = TextField(default='')
    favicon_url = TextField(default='')
    site_name = CharField(max_length=255, default='')
    fetched_at = IntegerField(default=0)

    class Meta:
        table_name = 'web_link_cache'

    def to_dict(self):
        return {
            'url': self.url,
            'domain': self.domain,
            'title': self.title,
            'description': self.description,
            'imageUrl': self.image_url,
            'faviconUrl': self.favicon_url,
            'siteName': self.site_name,
            'fetchedAt': self.fetched_at,
        }


class SignatureRecord(BaseModel):
    """
    Trazos y firmas manuscritas digitales en SQLite.
    Migrado de SignatureEntity de Android a Python + Peewee ORM.
    """
    id = AutoField(primary_key=True)
    note_id = IntegerField(null=True, index=True)
    points_json = TextField(default='[]')
    image_data = TextField(default='')
    created_at = IntegerField(default=0)

    class Meta:
        table_name = 'signatures'

    def to_dict(self):
        try:
            pts = json.loads(self.points_json or '[]')
        except Exception:
            pts = []
        return {
            'id': self.id,
            'noteId': self.note_id,
            'points': pts,
            'imageData': self.image_data,
            'createdAt': self.created_at,
        }


def _extract_note_signature(note_obj):
    """Genera una firma comparable del estado de la nota y sus bloques para evitar duplicados vacíos."""
    if not isinstance(note_obj, dict):
        return ''
    relevant = {
        'title': str(note_obj.get('title') or ''),
        'folder': str(note_obj.get('folder') or ''),
        'tags': str(note_obj.get('tags') or ''),
        'content': str(note_obj.get('content') or ''),
        'emoji': str(note_obj.get('emoji') or ''),
        'hasCover': bool(note_obj.get('hasCover')),
        'coverStyle': str(note_obj.get('coverStyle') or ''),
        'showCallout': bool(note_obj.get('showCallout')),
        'callout': str(note_obj.get('callout') or ''),
        'showQuote': bool(note_obj.get('showQuote')),
        'quote': str(note_obj.get('quote') or ''),
        'showToggle': bool(note_obj.get('showToggle')),
        'toggleHeader': str(note_obj.get('toggleHeader') or ''),
        'toggleBody': str(note_obj.get('toggleBody') or ''),
        'showCode': bool(note_obj.get('showCode')),
        'code': str(note_obj.get('code') or ''),
        'showKanban': bool(note_obj.get('showKanban')),
        'kanban': note_obj.get('kanban') or [],
        'showTable': bool(note_obj.get('showTable')),
        'tableFormula': str(note_obj.get('tableFormula') or ''),
        'tableRows': note_obj.get('tableRows') or [],
        'showChecklist': bool(note_obj.get('showChecklist')),
        'checklists': note_obj.get('checklists') or [],
        'katex': str(note_obj.get('katex') or ''),
    }
    return json.dumps(relevant, sort_keys=True, ensure_ascii=False)


def record_note_history_orm(note_obj, summary=None, force=False):
    """
    Registra una instantánea en la tabla note_history de SQLite.
    Agrupa ediciones rápidas automáticas (< 12 seg) para no saturar de pulsaciones,
    pero conserva versiones separadas cuando cambia significativamente o cuando force=True.
    """
    if not isinstance(note_obj, dict):
        return None

    note_id = int(note_obj.get('id') or int(time.time() * 1000))
    now_ms = int(time.time() * 1000)
    title = str(note_obj.get('title') or 'Sin título')
    folder = str(note_obj.get('folder') or 'Personal')
    raw_tags = note_obj.get('tags', '')
    if isinstance(raw_tags, list):
        tags = ', '.join(str(t).strip() for t in raw_tags if str(t).strip())
    else:
        tags = str(raw_tags or '')
    content = str(note_obj.get('content') or '')
    snapshot_str = json.dumps(note_obj, ensure_ascii=False)

    latest = (
        NoteHistory.select()
        .where(NoteHistory.note_id == note_id)
        .order_by(NoteHistory.created_at.desc(), NoteHistory.id.desc())
        .first()
    )

    if latest is None:
        effective_summary = summary or 'Versión inicial'
        created = NoteHistory.create(
            note_id=note_id,
            title=title,
            folder=folder,
            tags=tags,
            content=content,
            summary=effective_summary,
            created_at=int(note_obj.get('updatedAt') or now_ms),
            snapshot_json=snapshot_str,
        )
        return created.id

    try:
        latest_snap = json.loads(latest.snapshot_json or '{}')
    except Exception:
        latest_snap = {}

    if not force and _extract_note_signature(latest_snap) == _extract_note_signature(note_obj):
        return latest.id

    # Determinar descripción automática del cambio si no se especificó summary
    if not summary:
        if latest.title != title:
            summary = f'Título cambiado a "{title[:32]}"'
        elif latest.folder != folder:
            summary = f'Movida a carpeta "{folder}"'
        elif latest.tags != tags:
            summary = 'Etiquetas actualizadas'
        else:
            summary = 'Edición guardada en SQLite'

    # Si es un guardado automático muy reciente (< 12s) y el último no fue manual ni reversión, actualizar la fila reciente
    is_auto = not force and summary in ('Edición guardada en SQLite', 'Guardado automático')
    if (
        is_auto
        and (now_ms - int(latest.created_at or 0)) < 12000
        and latest.summary not in ('Versión inicial', 'Punto de restauración manual')
        and not str(latest.summary).startswith('Revertido a')
        and not str(latest.summary).startswith('Estado previo')
    ):
        latest.title = title
        latest.folder = folder
        latest.tags = tags
        latest.content = content
        latest.created_at = now_ms
        latest.snapshot_json = snapshot_str
        latest.save()
        return latest.id

    created = NoteHistory.create(
        note_id=note_id,
        title=title,
        folder=folder,
        tags=tags,
        content=content,
        summary=summary,
        created_at=now_ms,
        snapshot_json=snapshot_str,
    )

    # Mantener las últimas 50 versiones por nota para optimizar notejs.db
    old_ids = [
        h.id
        for h in NoteHistory.select(NoteHistory.id)
        .where(NoteHistory.note_id == note_id)
        .order_by(NoteHistory.created_at.desc(), NoteHistory.id.desc())
        .offset(50)
    ]
    if old_ids:
        NoteHistory.delete().where(NoteHistory.id.in_(old_ids)).execute()

    return created.id


def _ensure_folder_emoji_column():
    """Garantiza que la tabla folders tenga las columnas emoji, parent_name, is_smart y smart_rules_json."""
    try:
        cursor = db.execute_sql("PRAGMA table_info(folders);")
        columns = [row[1] for row in cursor.fetchall()]
        if 'emoji' not in columns:
            db.execute_sql("ALTER TABLE folders ADD COLUMN emoji VARCHAR(32) DEFAULT '📁';")
            for fname, default_emoji in DEFAULT_FOLDER_EMOJIS.items():
                db.execute_sql(
                    "UPDATE folders SET emoji = ? WHERE name = ? AND (emoji IS NULL OR emoji = '' OR emoji = '📁');",
                    (default_emoji, fname),
                )
        if 'parent_name' not in columns:
            db.execute_sql("ALTER TABLE folders ADD COLUMN parent_name VARCHAR(200) DEFAULT '';")
        if 'is_smart' not in columns:
            db.execute_sql("ALTER TABLE folders ADD COLUMN is_smart INTEGER DEFAULT 0;")
        if 'smart_rules_json' not in columns:
            db.execute_sql("ALTER TABLE folders ADD COLUMN smart_rules_json TEXT DEFAULT '';")
    except Exception:
        pass


def init_db():
    """Inicializa la conexión Peewee, crea las tablas si no existen y siembra carpetas iniciales con emojis."""
    with DB_LOCK:
        try:
            db.connect(reuse_if_open=True)
        except Exception:
            for ext in ('-shm', '-wal'):
                try:
                    fpath = f"{DB_PATH}{ext}"
                    if os.path.exists(fpath):
                        os.remove(fpath)
                except Exception:
                    pass
            db.connect(reuse_if_open=True)

        db.create_tables([Note, Folder, Setting, NoteHistory, Block, ReminderItem, WebLinkCache, SignatureRecord], safe=True)
        _ensure_folder_emoji_column()

        if Folder.select().count() == 0:
            default_folders = ['Personal', 'Trabajo', 'Universidad', 'Ideas']
            with db.atomic():
                for idx, fname in enumerate(default_folders):
                    emoji = DEFAULT_FOLDER_EMOJIS.get(fname, '📁')
                    Folder.insert(name=fname, emoji=emoji, sort_order=idx).on_conflict_ignore().execute()


def get_note_blocks_orm(note_id):
    """Obtiene todos los bloques de una nota ordenados por su sort_index fraccionario."""
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        rows = list(
            Block.select()
            .where(Block.note_id == int(note_id))
            .order_by(Block.sort_index.asc())
        )
        return {'ok': True, 'noteId': int(note_id), 'blocks': [r.to_dict() for r in rows]}


def update_block_order_orm(block_id, prev_id=None, next_id=None, parent_id=None, note_id=None):
    """
    Actualiza la posición de un bloque de forma O(1) calculando un nuevo sort_index
    estrictamente entre prev_id y next_id sin reescribir bloques vecinos.
    """
    if not block_id:
        return {'ok': False, 'error': 'block_id requerido'}

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            target_block = Block.get_or_none(Block.id == str(block_id))
            now_ms = int(time.time() * 1000)
            if target_block is None:
                target_block = Block.create(
                    id=str(block_id),
                    note_id=int(note_id or 0),
                    parent_id=str(parent_id) if parent_id else None,
                    type='p',
                    properties='{}',
                    sort_index='a0',
                    created_at=now_ms,
                    updated_at=now_ms,
                )

            prev_index = None
            if prev_id:
                prev_block = Block.get_or_none(Block.id == str(prev_id))
                if prev_block:
                    prev_index = prev_block.sort_index

            next_index = None
            if next_id:
                next_block = Block.get_or_none(Block.id == str(next_id))
                if next_block:
                    next_index = next_block.sort_index

            new_sort_index = generate_key_between(prev_index, next_index)
            target_block.sort_index = new_sort_index
            if parent_id is not None:
                target_block.parent_id = str(parent_id) if str(parent_id).strip() else None
            if note_id:
                target_block.note_id = int(note_id)
            target_block.updated_at = now_ms
            target_block.save()

    return {
        'ok': True,
        'blockId': target_block.id,
        'sortIndex': new_sort_index,
        'parentId': target_block.parent_id,
        'noteId': target_block.note_id,
    }


def update_batch_blocks_order_orm(moves):
    """
    Aplica una reubicación en lote de múltiples bloques atómicamente en SQLite.
    moves: lista de diccionarios [{'id': ..., 'sortIndex': ..., 'parentId': ..., 'noteId': ...}]
    """
    if not isinstance(moves, list):
        return {'ok': False, 'error': 'moves debe ser una lista'}

    updated = []
    now_ms = int(time.time() * 1000)
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            for m in moves:
                bid = str(m.get('id') or '')
                if not bid:
                    continue
                sort_idx = str(m.get('sortIndex') or 'a0')
                parent_id = m.get('parentId')
                parent_id_val = str(parent_id) if parent_id else None
                note_id = int(m.get('noteId') or 0)
                btype = str(m.get('type') or 'p')
                props = json.dumps(m.get('properties') or {})

                blk = Block.get_or_none(Block.id == bid)
                if blk:
                    blk.sort_index = sort_idx
                    blk.parent_id = parent_id_val
                    if note_id:
                        blk.note_id = note_id
                    blk.updated_at = now_ms
                    blk.save()
                else:
                    blk = Block.create(
                        id=bid,
                        note_id=note_id,
                        parent_id=parent_id_val,
                        type=btype,
                        properties=props,
                        sort_index=sort_idx,
                        created_at=now_ms,
                        updated_at=now_ms,
                    )
                updated.append(blk.to_dict())

    return {'ok': True, 'updatedCount': len(updated), 'blocks': updated}


def sync_blocks_from_note_html_orm(note_id, blocks_data):
    """
    Sincroniza los bloques extraídos del lienzo HTML actual de una nota en la tabla Block.
    """
    nid = int(note_id)
    if not isinstance(blocks_data, list):
        return {'ok': False, 'error': 'blocks_data debe ser una lista'}

    now_ms = int(time.time() * 1000)
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            incoming_ids = []
            for b in blocks_data:
                bid = str(b.get('id') or f"blk-{int(time.time()*1000)}-{len(incoming_ids)}")
                incoming_ids.append(bid)
                btype = str(b.get('type') or 'p')
                parent_id = str(b.get('parentId')) if b.get('parentId') else None
                sort_idx = str(b.get('sortIndex') or 'a0')
                props = json.dumps(b.get('properties') or {})

                blk = Block.get_or_none(Block.id == bid)
                if blk:
                    blk.note_id = nid
                    blk.parent_id = parent_id
                    blk.type = btype
                    blk.properties = props
                    blk.sort_index = sort_idx
                    blk.updated_at = now_ms
                    blk.save()
                else:
                    Block.create(
                        id=bid,
                        note_id=nid,
                        parent_id=parent_id,
                        type=btype,
                        properties=props,
                        sort_index=sort_idx,
                        created_at=now_ms,
                        updated_at=now_ms,
                    )
            if incoming_ids:
                Block.delete().where((Block.note_id == nid) & (Block.id.not_in(incoming_ids))).execute()

    return {'ok': True, 'noteId': nid, 'syncedCount': len(incoming_ids)}


def upsert_note_orm(note_obj, record_history=True, history_summary=None, force_history=False):
    """Inserta o actualiza una nota usando el ORM Peewee y registra su versión en note_history."""
    note_id = int(note_obj.get('id') or int(time.time() * 1000))
    title = str(note_obj.get('title') or 'Sin título')
    folder = str(note_obj.get('folder') or 'Personal')
    raw_tags = note_obj.get('tags', '')
    if isinstance(raw_tags, list):
        tags = ', '.join(str(t).strip() for t in raw_tags if str(t).strip())
    else:
        tags = str(raw_tags or '')
    is_pinned = 1 if note_obj.get('isPinned') else 0
    content = str(note_obj.get('content') or '')
    updated_at = int(note_obj.get('updatedAt') or int(time.time() * 1000))
    data_json = json.dumps(note_obj, ensure_ascii=False)

    Note.insert(
        id=note_id,
        title=title,
        folder=folder,
        tags=tags,
        is_pinned=is_pinned,
        content=content,
        updated_at=updated_at,
        data_json=data_json,
    ).on_conflict_replace().execute()

    if record_history:
        record_note_history_orm(note_obj, summary=history_summary, force=force_history)

    return note_id


def get_bootstrap_data():
    """Consulta mediante Peewee ORM todas las notas, carpetas (con sus iconos de emoji y reglas inteligentes) y ajustes."""
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        _ensure_folder_emoji_column()
        notes_query = Note.select().order_by(Note.is_pinned.desc(), Note.updated_at.desc())
        notes = [n.to_dict() for n in notes_query]

        folders_query = list(Folder.select().order_by(Folder.sort_order.asc()))
        folders = [f.name for f in folders_query]
        folder_emojis = {
            f.name: (f.emoji or DEFAULT_FOLDER_EMOJIS.get(f.name, '⚙️' if f.is_smart else '📁'))
            for f in folders_query
        }
        smart_folders = {}
        for f in folders_query:
            if f.is_smart and f.smart_rules_json:
                try:
                    parsed_cfg = json.loads(f.smart_rules_json)
                    if isinstance(parsed_cfg, dict):
                        smart_folders[f.name] = parsed_cfg
                except Exception:
                    pass
        folder_items = [f.to_dict() for f in folders_query]

        settings_query = Setting.select()
        settings = {s.key: s.value for s in settings_query}

        reminders_query = ReminderItem.select().order_by(ReminderItem.date_str.asc(), ReminderItem.time_str.asc())
        reminders = [r.to_dict() for r in reminders_query]

    return {
        'ok': True,
        'engine': 'SQLite + Peewee ORM',
        'desktopShell': 'PyWebView',
        'dbPath': DB_PATH,
        'notes': notes,
        'folders': folders,
        'folderEmojis': folder_emojis,
        'smartFolders': smart_folders,
        'folderItems': folder_items,
        'settings': settings,
        'reminders': reminders,
    }


def save_single_note(note_obj, summary=None, force_history=False):
    """Guarda una única nota de forma atómica con Peewee ORM y actualiza su historial."""
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            saved_id = upsert_note_orm(
                note_obj,
                record_history=True,
                history_summary=summary,
                force_history=force_history,
            )
    return {'ok': True, 'savedId': saved_id, 'engine': 'SQLite + Peewee ORM'}


def delete_single_note(note_id):
    """Elimina una nota por ID y su historial asociado usando Peewee ORM."""
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            Note.delete().where(Note.id == int(note_id)).execute()
            NoteHistory.delete().where(NoteHistory.note_id == int(note_id)).execute()
    return {'ok': True, 'deletedId': int(note_id)}


def get_note_history_list(note_id):
    """Obtiene todas las versiones históricas de una nota guardadas en SQLite."""
    nid = int(note_id)
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        rows = list(
            NoteHistory.select()
            .where(NoteHistory.note_id == nid)
            .order_by(NoteHistory.created_at.desc(), NoteHistory.id.desc())
        )
        if not rows:
            note_row = Note.get_or_none(Note.id == nid)
            if note_row is not None:
                with db.atomic():
                    record_note_history_orm(note_row.to_dict(), summary='Versión inicial', force=True)
                rows = list(
                    NoteHistory.select()
                    .where(NoteHistory.note_id == nid)
                    .order_by(NoteHistory.created_at.desc(), NoteHistory.id.desc())
                )
        history = [r.to_dict() for r in rows]

    return {
        'ok': True,
        'noteId': nid,
        'history': history,
        'engine': 'SQLite + Peewee ORM',
    }


def create_manual_note_snapshot(note_obj, summary='Punto de restauración manual'):
    """Guarda la nota actual y fuerza la creación de un nuevo punto de restauración en SQLite."""
    if not isinstance(note_obj, dict) or note_obj.get('id') is None:
        return {'ok': False, 'error': 'Nota inválida'}
    nid = int(note_obj.get('id'))
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            upsert_note_orm(
                note_obj,
                record_history=True,
                history_summary=summary or 'Punto de restauración manual',
                force_history=True,
            )
            rows = list(
                NoteHistory.select()
                .where(NoteHistory.note_id == nid)
                .order_by(NoteHistory.created_at.desc(), NoteHistory.id.desc())
            )
            history = [r.to_dict() for r in rows]

    return {
        'ok': True,
        'noteId': nid,
        'history': history,
        'engine': 'SQLite + Peewee ORM',
    }


def revert_note_to_version(note_id, version_id):
    """
    Revierte una nota en SQLite a una versión histórica específica (version_id),
    respaldando el estado previo antes de restaurar.
    """
    nid = int(note_id)
    vid = int(version_id)
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        target_ver = NoteHistory.get_or_none(
            (NoteHistory.id == vid) & (NoteHistory.note_id == nid)
        )
        if target_ver is None:
            return {'ok': False, 'error': 'Versión histórica no encontrada en SQLite'}

        try:
            restored_note = json.loads(target_ver.snapshot_json or '{}')
        except Exception:
            restored_note = {}

        if not isinstance(restored_note, dict):
            restored_note = {}

        now_ms = int(time.time() * 1000)
        restored_note['id'] = nid
        restored_note['title'] = target_ver.title
        restored_note['folder'] = target_ver.folder
        restored_note['tags'] = target_ver.tags
        restored_note['content'] = target_ver.content
        restored_note['updatedAt'] = now_ms

        with db.atomic():
            current_note_row = Note.get_or_none(Note.id == nid)
            if current_note_row is not None:
                current_dict = current_note_row.to_dict()
                if _extract_note_signature(current_dict) != _extract_note_signature(restored_note):
                    record_note_history_orm(
                        current_dict,
                        summary='Respaldo previo a reversión',
                        force=False,
                    )

            upsert_note_orm(
                restored_note,
                record_history=True,
                history_summary=f'Revertido a versión ({target_ver.title[:24]})',
                force_history=True,
            )

            rows = list(
                NoteHistory.select()
                .where(NoteHistory.note_id == nid)
                .order_by(NoteHistory.created_at.desc(), NoteHistory.id.desc())
            )
            history = [r.to_dict() for r in rows]

    return {
        'ok': True,
        'noteId': nid,
        'restoredVersionId': vid,
        'note': restored_note,
        'history': history,
        'engine': 'SQLite + Peewee ORM',
    }


def delete_note_history_version(note_id, version_id):
    """Elimina una versión específica del historial de una nota en SQLite."""
    nid = int(note_id)
    vid = int(version_id)
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            NoteHistory.delete().where(
                (NoteHistory.id == vid) & (NoteHistory.note_id == nid)
            ).execute()
            rows = list(
                NoteHistory.select()
                .where(NoteHistory.note_id == nid)
                .order_by(NoteHistory.created_at.desc(), NoteHistory.id.desc())
            )
            history = [r.to_dict() for r in rows]
    return {'ok': True, 'noteId': nid, 'deletedVersionId': vid, 'history': history}


def _persist_folders_orm(folders_list, folder_emojis=None, smart_folders=None):
    """Persiste la lista ordenada de carpetas, sus iconos de emoji y configuración de carpetas inteligentes en SQLite."""
    _ensure_folder_emoji_column()
    existing_rows = {f.name: f for f in Folder.select()}
    existing_emojis = {
        fname: (row.emoji or DEFAULT_FOLDER_EMOJIS.get(fname, '📁'))
        for fname, row in existing_rows.items()
    }
    existing_smart = {}
    for fname, row in existing_rows.items():
        if row.is_smart and row.smart_rules_json:
            try:
                existing_smart[fname] = json.loads(row.smart_rules_json)
            except Exception:
                pass

    provided_emojis = folder_emojis if isinstance(folder_emojis, dict) else {}
    provided_smart = smart_folders if isinstance(smart_folders, dict) else existing_smart

    normalized_names = []
    resolved_emojis = {}
    resolved_smart = {}

    for item in (folders_list or []):
        if isinstance(item, dict):
            fname = str(item.get('name') or '').strip()
            item_emoji = str(item.get('emoji') or '').strip()
            item_smart = item.get('smartConfig')
        else:
            fname = str(item or '').strip()
            item_emoji = ''
            item_smart = None
        if not fname or fname in resolved_emojis:
            continue

        smart_cfg = item_smart if isinstance(item_smart, dict) else provided_smart.get(fname)
        is_smart_folder = isinstance(smart_cfg, dict)
        # Las carpetas inteligentes siempre viven en la raíz (no admiten subcarpetas)
        if is_smart_folder and '/' in fname:
            fname = [p.strip() for p in fname.split('/') if p.strip()][-1]

        emoji_val = (
            item_emoji
            or str(provided_emojis.get(fname) or '').strip()
            or existing_emojis.get(fname)
            or DEFAULT_FOLDER_EMOJIS.get(fname, '⚙️' if is_smart_folder else '📁')
        )
        normalized_names.append(fname)
        resolved_emojis[fname] = emoji_val
        if is_smart_folder:
            resolved_smart[fname] = smart_cfg

    Folder.delete().execute()
    for idx, fname in enumerate(normalized_names):
        smart_cfg = resolved_smart.get(fname)
        is_smart_flag = 1 if isinstance(smart_cfg, dict) else 0
        parts = [p.strip() for p in str(fname).split('/') if p.strip()]
        parent_val = '' if is_smart_flag else ('/'.join(parts[:-1]) if len(parts) > 1 else '')
        Folder.insert(
            name=fname,
            parent_name=parent_val,
            emoji=resolved_emojis.get(fname, '⚙️' if is_smart_flag else '📁'),
            sort_order=idx,
            is_smart=is_smart_flag,
            smart_rules_json=json.dumps(smart_cfg, ensure_ascii=False) if is_smart_flag else '',
        ).on_conflict_replace().execute()

    return normalized_names, resolved_emojis, resolved_smart


def sync_all_data(body):
    """Sincroniza notas, carpetas (con emojis y carpetas inteligentes) y ajustes en una transacción atómica de Peewee ORM."""
    notes_list = body.get('notes', [])
    folders_list = body.get('folders', None)
    folder_emojis = body.get('folderEmojis', None)
    smart_folders = body.get('smartFolders', None)
    settings_dict = body.get('settings', None)
    replace_all = bool(body.get('replaceAll'))

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            if isinstance(notes_list, list):
                keep_ids = []
                for n in notes_list:
                    if isinstance(n, dict) and n.get('id') is not None:
                        nid = upsert_note_orm(n, record_history=True)
                        keep_ids.append(nid)
                if replace_all and keep_ids:
                    Note.delete().where(Note.id.not_in(keep_ids)).execute()
                elif replace_all and len(keep_ids) == 0:
                    Note.delete().execute()

            if isinstance(folders_list, list) and folders_list:
                _persist_folders_orm(folders_list, folder_emojis, smart_folders)

            reminders_list = body.get('reminders', None)
            if isinstance(reminders_list, list):
                for item in reminders_list:
                    if isinstance(item, dict):
                        save_reminder_orm(item)

            if isinstance(settings_dict, dict):
                for k, v in settings_dict.items():
                    Setting.insert(key=str(k), value=str(v)).on_conflict_replace().execute()

    return {'ok': True, 'engine': 'SQLite + Peewee ORM'}


def save_folders_list(folders_payload, folder_emojis=None):
    """Reemplaza el orden, lista de carpetas, emojis y carpetas inteligentes usando Peewee ORM."""
    smart_folders = None
    if isinstance(folders_payload, dict):
        folders_list = folders_payload.get('folders', [])
        if folder_emojis is None:
            folder_emojis = folders_payload.get('folderEmojis')
        smart_folders = folders_payload.get('smartFolders')
    elif isinstance(folders_payload, list):
        folders_list = folders_payload
    else:
        folders_list = []

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            names, emojis, smart_map = _persist_folders_orm(folders_list, folder_emojis, smart_folders)
    return {'ok': True, 'folders': names, 'folderEmojis': emojis, 'smartFolders': smart_map}


def move_folder_hierarchy_orm(source_folder, target_parent_folder='', folders_list=None, folder_emojis=None, notes_list=None):
    """
    Actualiza atómicamente la jerarquía de una carpeta (y todas sus subcarpetas y notas asociadas)
    en SQLite mediante Peewee ORM cuando se arrastra una carpeta sobre otra.
    """
    src = str(source_folder or '').strip()
    tgt_parent = str(target_parent_folder or '').strip()
    if not src or src.lower() == 'todas las notas':
        return {'ok': False, 'error': 'La carpeta origen no puede moverse'}
    if tgt_parent.lower() == 'todas las notas':
        tgt_parent = ''
    if src == tgt_parent or (tgt_parent and tgt_parent.startswith(src + '/')):
        return {'ok': False, 'error': 'Jerarquía circular no permitida'}

    leaf = [p.strip() for p in src.split('/') if p.strip()][-1]
    new_path = f"{tgt_parent}/{leaf}" if tgt_parent else leaf
    old_prefix = src + '/'
    new_prefix = new_path + '/'

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        _ensure_folder_emoji_column()
        with db.atomic():
            src_row = Folder.get_or_none(Folder.name == src)
            if src_row and src_row.is_smart and tgt_parent:
                return {'ok': False, 'error': 'Las carpetas inteligentes siempre se ubican en la raíz y no pueden ser subcarpetas'}
            if tgt_parent:
                tgt_row = Folder.get_or_none(Folder.name == tgt_parent)
                if tgt_row and tgt_row.is_smart:
                    return {'ok': False, 'error': 'Las carpetas inteligentes no admiten subcarpetas'}

            if isinstance(folders_list, list) and folders_list:
                names, emojis, _ = _persist_folders_orm(folders_list, folder_emojis)
            else:
                existing_rows = list(Folder.select().order_by(Folder.sort_order.asc()))
                updated_names = []
                updated_emojis = {}
                for row in existing_rows:
                    fname = row.name
                    if fname == src:
                        mapped = new_path
                    elif fname.startswith(old_prefix):
                        mapped = new_prefix + fname[len(old_prefix):]
                    else:
                        mapped = fname
                    updated_names.append(mapped)
                    updated_emojis[mapped] = row.emoji or '📁'
                names, emojis, _ = _persist_folders_orm(updated_names, updated_emojis)

            if isinstance(notes_list, list) and notes_list:
                for n in notes_list:
                    if isinstance(n, dict) and n.get('id') is not None:
                        upsert_note_orm(n, record_history=False)
            else:
                for note_row in Note.select():
                    note_dict = note_row.to_dict()
                    raw_folder = str(note_dict.get('folder') or '')
                    parts = [p.strip() for p in raw_folder.split('|') if p.strip()]
                    changed = False
                    new_parts = []
                    for p in parts:
                        if p == src:
                            new_parts.append(new_path)
                            changed = True
                        elif p.startswith(old_prefix):
                            new_parts.append(new_prefix + p[len(old_prefix):])
                            changed = True
                        else:
                            new_parts.append(p)
                    if changed:
                        note_dict['folder'] = ' | '.join(new_parts)
                        if isinstance(note_dict.get('folders'), list):
                            note_dict['folders'] = [
                                new_path if f == src else (new_prefix + f[len(old_prefix):] if str(f).startswith(old_prefix) else f)
                                for f in note_dict['folders']
                            ]
                        upsert_note_orm(note_dict, record_history=False)

    return {
        'ok': True,
        'oldPath': src,
        'newPath': new_path,
        'parentFolder': tgt_parent,
        'folders': names,
        'folderEmojis': emojis,
    }


def update_folder_emoji_orm(folder_name, emoji):
    """Actualiza o asigna un icono de emoji personalizado a una carpeta específica en SQLite."""
    fname = str(folder_name or '').strip()
    clean_emoji = str(emoji or '').strip() or '📁'
    if not fname:
        return {'ok': False, 'error': 'Nombre de carpeta vacío'}

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        _ensure_folder_emoji_column()
        with db.atomic():
            folder_row = Folder.get_or_none(Folder.name == fname)
            if folder_row is not None:
                folder_row.emoji = clean_emoji
                folder_row.save()
            else:
                max_order = Folder.select().count()
                parts = [p.strip() for p in str(fname).split('/') if p.strip()]
                parent_val = '/'.join(parts[:-1]) if len(parts) > 1 else ''
                Folder.insert(name=fname, parent_name=parent_val, emoji=clean_emoji, sort_order=max_order).on_conflict_replace().execute()

            folders_query = list(Folder.select().order_by(Folder.sort_order.asc()))
            folders = [f.name for f in folders_query]
            folder_emojis = {
                f.name: (f.emoji or DEFAULT_FOLDER_EMOJIS.get(f.name, '📁'))
                for f in folders_query
            }

    return {
        'ok': True,
        'folder': fname,
        'emoji': clean_emoji,
        'folders': folders,
        'folderEmojis': folder_emojis,
    }


def save_settings_dict(settings_dict):
    """Actualiza pares clave-valor de configuración usando Peewee ORM."""
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            for k, v in settings_dict.items():
                Setting.insert(key=str(k), value=str(v)).on_conflict_replace().execute()
    return {'ok': True}


def _extract_tags_from_note_dict(note_dict):
    """Extrae todas las etiquetas asociadas a una nota (campo tags y menciones inline #tag)."""
    tags_set = set()
    raw = note_dict.get('tags') or ''
    if isinstance(raw, list):
        items = raw
    else:
        items = str(raw).split(',')
    for t in items:
        clean = str(t or '').strip().lower().lstrip('#')
        if clean:
            tags_set.add(clean)
    content_text = re.sub(r'<[^>]*>', ' ', str(note_dict.get('content') or ''))
    title_text = str(note_dict.get('title') or '')
    for m in re.findall(r'(?:^|\s)#([a-zA-Z0-9_áéíóúñÁÉÍÓÚÑ-]{2,32})', f"{title_text} {content_text}"):
        clean = m.strip().lower().lstrip('#')
        if clean:
            tags_set.add(clean)
    return list(tags_set)


def _extract_mentions_from_note_dict(note_dict):
    """Extrae las menciones de usuario (@usuario) de una nota."""
    mentions_set = set()
    raw_mentions = note_dict.get('mentions')
    if isinstance(raw_mentions, list):
        for m in raw_mentions:
            clean = str(m or '').strip().lower().lstrip('@')
            if clean:
                mentions_set.add(clean)
    combined = f"{note_dict.get('title') or ''} {note_dict.get('content') or ''} {note_dict.get('callout') or ''} {note_dict.get('quote') or ''}"
    clean_combined = re.sub(r'<[^>]*>', ' ', combined)
    for m in re.findall(r'(?:^|\s)@([a-zA-Z0-9_.-]{2,32})', clean_combined):
        clean = m.strip().lower().lstrip('@')
        if clean:
            mentions_set.add(clean)
    return list(mentions_set)


def _extract_shared_users_from_note_dict(note_dict):
    """Extrae la lista de usuarios compartidos de una nota."""
    shared_set = set()
    raw = note_dict.get('sharedWith')
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, str) and raw.strip():
        items = raw.split(',')
    else:
        items = []
    for u in items:
        clean = str(u or '').strip().lower().lstrip('@')
        if clean:
            shared_set.add(clean)
    return list(shared_set)


def _note_matches_smart_rule_python(note_dict, rule):
    """Evalúa individualmente una regla de Carpeta Inteligente contra una nota."""
    if not isinstance(rule, dict):
        return False
    rule_type = str(rule.get('type') or '')
    if not rule_type:
        return False
    condition = str(rule.get('condition') or 'any')

    if rule_type == 'tags':
        note_tags = _extract_tags_from_note_dict(note_dict)
        if condition == 'untagged':
            return len(note_tags) == 0
        if condition == 'any_tag':
            return len(note_tags) > 0
        raw_vals = rule.get('values')
        if not raw_vals:
            raw_vals = rule.get('value') or ''
        if isinstance(raw_vals, list):
            target_tags = [str(t or '').strip().lower().lstrip('#') for t in raw_vals if str(t or '').strip()]
        else:
            target_tags = [str(t or '').strip().lower().lstrip('#') for t in str(raw_vals).split(',') if str(t or '').strip()]
        if not target_tags:
            return False
        if condition == 'all_selected':
            return all(t in note_tags for t in target_tags)
        if condition == 'none_selected':
            return all(t not in note_tags for t in target_tags)
        return any(t in note_tags for t in target_tags)

    if rule_type == 'date':
        field = 'createdAt' if rule.get('field') == 'createdAt' else 'updatedAt'
        raw_ts = note_dict.get(field) or note_dict.get('updatedAt') or note_dict.get('id') or 0
        try:
            ts = int(raw_ts)
        except (ValueError, TypeError):
            ts = 0
        now = datetime.datetime.now()
        start_of_today = datetime.datetime(now.year, now.month, now.day).timestamp() * 1000
        start_of_yesterday = start_of_today - 86400000

        if condition == 'today':
            return ts >= start_of_today
        if condition == 'yesterday':
            return ts >= start_of_yesterday and ts < start_of_today
        if condition == 'last_7_days':
            return ts >= (now.timestamp() * 1000 - 7 * 86400000)
        if condition == 'last_30_days':
            return ts >= (now.timestamp() * 1000 - 30 * 86400000)
        if condition == 'custom_range':
            after_from = True
            before_to = True
            from_str = rule.get('from')
            if from_str:
                try:
                    from_dt = datetime.datetime.strptime(str(from_str).strip()[:10], '%Y-%m-%d')
                    after_from = ts >= from_dt.timestamp() * 1000
                except Exception:
                    pass
            to_str = rule.get('to')
            if to_str:
                try:
                    to_dt = datetime.datetime.strptime(str(to_str).strip()[:10], '%Y-%m-%d')
                    before_to = ts <= (to_dt.timestamp() * 1000 + 86399999)
                except Exception:
                    pass
            return after_from and before_to
        return False

    if rule_type == 'checklists':
        checklists = note_dict.get('checklists') if (note_dict.get('showChecklist') and isinstance(note_dict.get('checklists'), list)) else []
        html = str(note_dict.get('content') or '')
        has_html_check = bool(re.search(r'type=["\']checkbox["\']|task-list-item', html, re.I))
        has_checklists = len(checklists) > 0 or has_html_check
        has_unchecked = any(not it.get('done') for it in checklists) or bool(re.search(r'type=["\']checkbox["\'](?![^>]*checked)', html, re.I))
        has_checked = any(bool(it.get('done')) for it in checklists) or bool(re.search(r'type=["\']checkbox["\'][^>]*checked', html, re.I))

        if condition == 'none':
            return not has_checklists
        if condition == 'unchecked':
            return has_checklists and has_unchecked
        if condition == 'checked':
            return has_checklists and has_checked
        if condition == 'both':
            return has_checklists and has_unchecked and has_checked
        return has_checklists

    if rule_type == 'attachments':
        html = str(note_dict.get('content') or '')
        has_photos_or_videos = bool(re.search(r'note-image-block|<img\b|<video\b|\.(?:png|jpe?g|gif|webp|mp4|webm)', html, re.I))
        has_pdf = bool(re.search(r'\.pdf\b|application/pdf', html, re.I))
        has_audio = bool(re.search(r'<audio\b|\.(?:mp3|wav|ogg|m4a)\b', html, re.I))
        has_drawing = bool(re.search(r'<svg\b|<canvas\b|data:image/svg\+xml', html, re.I) or note_dict.get('katex'))
        has_web_links = bool(re.search(r'<a\s+[^>]*href=|https?://[^\s<"]+|note-embedded-card', html, re.I))

        if condition == 'photos_videos':
            return has_photos_or_videos
        if condition == 'pdfs':
            return has_pdf
        if condition == 'audio':
            return has_audio
        if condition == 'drawings':
            return has_drawing
        if condition == 'links':
            return has_web_links
        return has_photos_or_videos or has_pdf or has_audio or has_drawing or has_web_links

    if rule_type == 'shared':
        shared_users = _extract_shared_users_from_note_dict(note_dict)
        is_shared = bool(note_dict.get('isShared')) or len(shared_users) > 0
        if condition == 'not_shared':
            return not is_shared
        if condition == 'specific_user':
            target_user = str(rule.get('value') or '').strip().lower().lstrip('@')
            if not target_user:
                return is_shared
            return any(target_user in u for u in shared_users)
        return is_shared

    if rule_type == 'pinned_locked':
        is_pinned = bool(note_dict.get('isPinned'))
        is_locked = bool(note_dict.get('isLocked'))
        if condition == 'pinned':
            return is_pinned
        if condition == 'locked':
            return is_locked
        if condition == 'not_locked':
            return not is_locked
        if condition == 'pinned_or_locked':
            return is_pinned or is_locked
        if condition == 'not_pinned':
            return not is_pinned
        return is_locked

    if rule_type == 'mentions':
        mentions = _extract_mentions_from_note_dict(note_dict)
        if condition == 'no_mentions':
            return len(mentions) == 0
        if condition == 'specific_mention':
            target_mention = str(rule.get('value') or '').strip().lower().lstrip('@')
            if not target_mention:
                return len(mentions) > 0
            return any(target_mention in m for m in mentions)
        return len(mentions) > 0

    return False


def eval_note_smart_rules(note_dict, rules, match_mode='all'):
    """Evalúa si una nota cumple el conjunto de reglas de una Carpeta Inteligente."""
    if not isinstance(rules, list) or len(rules) == 0:
        return False
    mode = str(match_mode or 'all').lower()
    if mode == 'any':
        return any(_note_matches_smart_rule_python(note_dict, r) for r in rules)
    return all(_note_matches_smart_rule_python(note_dict, r) for r in rules)


def query_smart_folder_orm(folder_name=None, rules=None, match_mode='all'):
    """
    Ejecuta una consulta dinámica en la base de datos SQLite con Peewee ORM
    filtrando todas las notas según las condiciones y reglas de una Carpeta Inteligente.
    Retorna un diccionario con las notas coincidentes ordenadas por fijadas y fecha de actualización.
    """
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        target_name = (folder_name or '').strip()
        resolved_rules = rules
        resolved_mode = match_mode or 'all'

        if resolved_rules is None and target_name:
            folder_row = Folder.get_or_none(Folder.name == target_name)
            if folder_row:
                if not folder_row.is_smart:
                    return {
                        'ok': False,
                        'error': f"La carpeta '{target_name}' no es una carpeta inteligente",
                        'folder': target_name,
                        'notes': [],
                        'count': 0
                    }
                if folder_row.smart_rules_json:
                    try:
                        cfg = json.loads(folder_row.smart_rules_json)
                        if isinstance(cfg, dict):
                            resolved_rules = cfg.get('rules', [])
                            resolved_mode = cfg.get('matchMode', resolved_mode)
                    except Exception:
                        resolved_rules = []
                else:
                    resolved_rules = []

        if not resolved_rules:
            # Una carpeta inteligente sin reglas no muestra todas las notas por defecto
            return {
                'ok': True,
                'folder': target_name,
                'matchMode': resolved_mode,
                'rules': [],
                'notes': [],
                'count': 0
            }

        matched_notes = []
        try:
            query = Note.select().order_by(Note.is_pinned.desc(), Note.updated_at.desc())
            for note_row in query:
                note_dict = note_row.to_dict()
                if note_dict.get('isTrashed'):
                    continue
                if eval_note_smart_rules(note_dict, resolved_rules, match_mode=resolved_mode):
                    matched_notes.append(note_dict)

            return {
                'ok': True,
                'folder': target_name,
                'matchMode': resolved_mode,
                'rules': resolved_rules,
                'notes': matched_notes,
                'count': len(matched_notes),
            }
        except Exception as e:
            return {
                'ok': False,
                'error': f"Error en consulta dinámica: {str(e)}",
                'folder': target_name,
                'notes': [],
                'count': 0,
            }


def save_smart_folder_orm(name, rules, match_mode='all', emoji='⚙️', old_name=None):
    """
    Crea o actualiza una Carpeta Inteligente individual en SQLite con Peewee ORM.
    Garantiza que se guarde en el nivel raíz con is_smart=1 y smart_rules_json persistido.
    """
    clean_name = str(name or '').strip().replace('/', '-')
    clean_emoji = str(emoji or '').strip() or '⚙️'
    mode = 'any' if str(match_mode).lower() == 'any' else 'all'
    rules_list = rules if isinstance(rules, list) else []

    if not clean_name:
        return {'ok': False, 'error': 'El nombre de la carpeta inteligente no puede estar vacío'}

    if clean_name.lower() in ('todas las notas', 'papelera'):
        return {'ok': False, 'error': 'Nombre de carpeta reservado por el sistema'}

    smart_cfg = {
        'matchMode': mode,
        'rules': rules_list
    }
    rules_json = json.dumps(smart_cfg, ensure_ascii=False)

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        _ensure_folder_emoji_column()
        with db.atomic():
            old = str(old_name or '').strip()
            if old and old != clean_name:
                Folder.delete().where(Folder.name == old).execute()

            existing = Folder.get_or_none(Folder.name == clean_name)
            max_order = Folder.select().count()
            order_val = existing.sort_order if existing is not None else max_order

            Folder.insert(
                name=clean_name,
                parent_name='',
                emoji=clean_emoji,
                sort_order=order_val,
                is_smart=1,
                smart_rules_json=rules_json,
            ).on_conflict_replace().execute()

            folders_query = list(Folder.select().order_by(Folder.sort_order.asc()))
            folders = [f.name for f in folders_query]
            folder_emojis = {
                f.name: (f.emoji or DEFAULT_FOLDER_EMOJIS.get(f.name, '⚙️' if f.is_smart else '📁'))
                for f in folders_query
            }
            smart_folders = {}
            for f in folders_query:
                if f.is_smart and f.smart_rules_json:
                    try:
                        cfg = json.loads(f.smart_rules_json)
                        if isinstance(cfg, dict):
                            smart_folders[f.name] = cfg
                    except Exception:
                        pass

    return {
        'ok': True,
        'folder': clean_name,
        'emoji': clean_emoji,
        'matchMode': mode,
        'rules': rules_list,
        'folders': folders,
        'folderEmojis': folder_emojis,
        'smartFolders': smart_folders,
    }


def delete_smart_folder_orm(name):
    """
    Elimina una Carpeta Inteligente de SQLite sin tocar las notas físicas del usuario.
    """
    clean_name = str(name or '').strip()
    if not clean_name or clean_name.lower() in ('todas las notas', 'papelera'):
        return {'ok': False, 'error': 'No se puede eliminar esta carpeta'}

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        _ensure_folder_emoji_column()
        with db.atomic():
            Folder.delete().where(Folder.name == clean_name).execute()

            folders_query = list(Folder.select().order_by(Folder.sort_order.asc()))
            folders = [f.name for f in folders_query]
            folder_emojis = {
                f.name: (f.emoji or DEFAULT_FOLDER_EMOJIS.get(f.name, '⚙️' if f.is_smart else '📁'))
                for f in folders_query
            }
            smart_folders = {}
            for f in folders_query:
                if f.is_smart and f.smart_rules_json:
                    try:
                        cfg = json.loads(f.smart_rules_json)
                        if isinstance(cfg, dict):
                            smart_folders[f.name] = cfg
                    except Exception:
                        pass

    return {
        'ok': True,
        'deletedFolder': clean_name,
        'folders': folders,
        'folderEmojis': folder_emojis,
        'smartFolders': smart_folders,
    }


ALLOWED_IMAGE_MIMES = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.bmp': 'image/bmp',
    '.ico': 'image/x-icon',
    '.avif': 'image/avif',
}


def resolve_local_image_path(raw_path):
    """
    Resuelve una ruta local de imagen (absoluta, relativa, ~/ o file://) en el sistema,
    la procesa y la devuelve codificada como Data URI (base64) lista para incrustar
    como bloque redimensionable en el documento y persistir en SQLite.
    """
    if not raw_path or not isinstance(raw_path, str):
        return {'ok': False, 'error': 'Ruta de imagen vacía o inválida'}

    cleaned = raw_path.strip().strip('"').strip("'")
    if not cleaned:
        return {'ok': False, 'error': 'Ruta de imagen vacía'}

    # Si ya es data:image o URL http/https, devolverla directamente
    if cleaned.startswith('data:image/') or cleaned.startswith('http://') or cleaned.startswith('https://'):
        return {
            'ok': True,
            'dataUri': cleaned,
            'fileName': os.path.basename(urlparse(cleaned).path) or 'imagen',
            'sourceType': 'url',
        }

    # Si empieza con file://
    if cleaned.lower().startswith('file://'):
        parsed = urlparse(cleaned)
        local_candidate = unquote(parsed.path or '')
        # En Windows file:///C:/ruta deja /C:/ruta
        if len(local_candidate) >= 3 and local_candidate[0] == '/' and local_candidate[2] == ':':
            local_candidate = local_candidate[1:]
        cleaned = local_candidate

    expanded = os.path.expanduser(cleaned)

    # Probar posibles ubicaciones (ruta directa, relativa a DATA_DIR, frontend o public)
    candidates = [
        expanded,
        os.path.abspath(expanded),
        os.path.join(DATA_DIR, cleaned.lstrip('/\\')),
        os.path.join(DATA_DIR, 'frontend', cleaned.lstrip('/\\')),
        os.path.join(DATA_DIR, 'public', cleaned.lstrip('/\\')),
    ]

    found_path = None
    for cand in candidates:
        if cand and os.path.isfile(cand):
            found_path = os.path.abspath(cand)
            break

    if not found_path:
        return {
            'ok': False,
            'error': f'No se encontró el archivo local: {raw_path}',
        }

    ext = os.path.splitext(found_path)[1].lower()
    mime_type = ALLOWED_IMAGE_MIMES.get(ext)
    if not mime_type:
        guessed, _ = mimetypes.guess_type(found_path)
        if guessed and guessed.startswith('image/'):
            mime_type = guessed
        else:
            return {
                'ok': False,
                'error': f'El archivo no tiene un formato de imagen soportado ({ext or "sin extensión"})',
            }

    try:
        file_size = os.path.getsize(found_path)
        if file_size > 25 * 1024 * 1024:
            return {'ok': False, 'error': 'La imagen supera el límite de 25 MB'}

        with open(found_path, 'rb') as f:
            raw_bytes = f.read()

        b64_str = base64.b64encode(raw_bytes).decode('ascii')
        data_uri = f'data:{mime_type};base64,{b64_str}'
        return {
            'ok': True,
            'dataUri': data_uri,
            'fileName': os.path.basename(found_path),
            'resolvedPath': found_path,
            'mimeType': mime_type,
            'sizeBytes': file_size,
            'sourceType': 'local',
        }
    except Exception as exc:
        return {'ok': False, 'error': f'Error al leer la imagen local: {str(exc)}'}


def get_reminders_orm():
    """Obtiene todos los recordatorios y eventos de calendario registrados en SQLite."""
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        reminders = [r.to_dict() for r in ReminderItem.select().order_by(ReminderItem.date_str.asc(), ReminderItem.time_str.asc())]
    return {'ok': True, 'reminders': reminders}


def save_reminder_orm(item_dict):
    """
    Guarda o actualiza un recordatorio/evento en SQLite con Peewee ORM.
    Migrado desde ReminderEntity / CalendarEvent de Android para la versión PC.
    """
    if not isinstance(item_dict, dict):
        return {'ok': False, 'error': 'Datos de recordatorio inválidos'}
    now_ms = int(time.time() * 1000)
    rid = int(item_dict.get('id') or now_ms)
    title = str(item_dict.get('title') or 'Recordatorio').strip()
    date_str = str(item_dict.get('date') or item_dict.get('date_str') or '')
    time_str = str(item_dict.get('time') or item_dict.get('time_str') or 'Todo el día')
    category = str(item_dict.get('category') or 'Trabajo')
    completed = 1 if item_dict.get('completed') else 0
    priority = int(item_dict.get('priority') or 0)
    notes = str(item_dict.get('notes') or '')
    recurrence = str(item_dict.get('recurrence') or 'NONE')
    subtasks = item_dict.get('subtasks', [])
    subtasks_json = json.dumps(subtasks if isinstance(subtasks, list) else [], ensure_ascii=False)
    linked_note_id = item_dict.get('linkedNoteId')
    linked_note_id = int(linked_note_id) if linked_note_id is not None and str(linked_note_id).isdigit() else None
    created_at = int(item_dict.get('createdAt') or now_ms)
    updated_at = now_ms

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            ReminderItem.insert(
                id=rid,
                title=title,
                date_str=date_str,
                time_str=time_str,
                category=category,
                completed=completed,
                priority=priority,
                notes=notes,
                recurrence=recurrence,
                subtasks_json=subtasks_json,
                linked_note_id=linked_note_id,
                created_at=created_at,
                updated_at=updated_at,
            ).on_conflict_replace().execute()

    return {
        'ok': True,
        'reminder': {
            'id': rid,
            'title': title,
            'date': date_str,
            'time': time_str,
            'category': category,
            'completed': bool(completed),
            'priority': priority,
            'notes': notes,
            'recurrence': recurrence,
            'subtasks': subtasks if isinstance(subtasks, list) else [],
            'linkedNoteId': linked_note_id,
            'createdAt': created_at,
            'updatedAt': updated_at,
        }
    }


def delete_reminder_orm(reminder_id):
    """Elimina un recordatorio por ID en SQLite."""
    try:
        rid = int(reminder_id)
    except (ValueError, TypeError):
        return {'ok': False, 'error': 'ID de recordatorio inválido'}

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            ReminderItem.delete().where(ReminderItem.id == rid).execute()
    return {'ok': True, 'deletedId': rid}


def sync_reminders_orm(reminders_list):
    """Sincroniza una lista de recordatorios en lote en SQLite."""
    if not isinstance(reminders_list, list):
        return {'ok': False, 'error': 'reminders_list debe ser una lista'}

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            for item in reminders_list:
                if isinstance(item, dict):
                    save_reminder_orm(item)
    return {'ok': True, 'count': len(reminders_list)}


def fetch_weblink_metadata_orm(url_str):
    """
    Obtiene metadatos OpenGraph / HTML para una URL (título, descripción, imagen, favicon, dominio).
    Utiliza caché local en SQLite (WebLinkCache) para respuesta instantánea.
    Migrado de WebLinkMetadataFetcher de Android a Python puro para la versión PC.
    """
    if not url_str or not isinstance(url_str, str):
        return {'ok': False, 'error': 'URL inválida'}

    clean_url = url_str.strip()
    if not clean_url.startswith(('http://', 'https://')):
        clean_url = 'https://' + clean_url

    now = int(time.time())
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        cached = WebLinkCache.get_or_none(WebLinkCache.url == clean_url)
        # Si está en caché y tiene menos de 7 días (604800 s)
        if cached and (now - int(cached.fetched_at or 0)) < 604800:
            return {'ok': True, 'metadata': cached.to_dict(), 'fromCache': True}

    parsed = urlparse(clean_url)
    domain = parsed.netloc or ''
    title = ''
    description = ''
    image_url = ''
    site_name = domain
    favicon_url = f"{parsed.scheme}://{domain}/favicon.ico" if domain else ''

    try:
        req = urllib.request.Request(
            clean_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            }
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' in content_type or 'xhtml' in content_type:
                raw_html = response.read(256 * 1024).decode('utf-8', errors='ignore')

                # Título og:title o <title>
                m_og_title = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', raw_html, re.I)
                if not m_og_title:
                    m_og_title = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:title["\']', raw_html, re.I)
                m_title = re.search(r'<title[^>]*>([^<]+)</title>', raw_html, re.I)
                if m_og_title:
                    title = html.unescape(m_og_title.group(1).strip())
                elif m_title:
                    title = html.unescape(m_title.group(1).strip())

                # Descripción
                m_og_desc = re.search(r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']+)["\']', raw_html, re.I)
                if not m_og_desc:
                    m_og_desc = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', raw_html, re.I)
                if m_og_desc:
                    description = html.unescape(m_og_desc.group(1).strip())

                # Imagen og:image
                m_og_img = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', raw_html, re.I)
                if m_og_img:
                    image_url = m_og_img.group(1).strip()
                    if image_url.startswith('//'):
                        image_url = parsed.scheme + ':' + image_url
                    elif image_url.startswith('/'):
                        image_url = f"{parsed.scheme}://{domain}{image_url}"

                # Nombre del sitio
                m_og_site = re.search(r'<meta[^>]*property=["\']og:site_name["\'][^>]*content=["\']([^"\']+)["\']', raw_html, re.I)
                if m_og_site:
                    site_name = html.unescape(m_og_site.group(1).strip())

                # Favicon
                m_fav = re.search(r'<link[^>]*rel=["\'](?:shortcut )?icon["\'][^>]*href=["\']([^"\']+)["\']', raw_html, re.I)
                if m_fav:
                    fav_raw = m_fav.group(1).strip()
                    if fav_raw.startswith('//'):
                        favicon_url = parsed.scheme + ':' + fav_raw
                    elif fav_raw.startswith('/'):
                        favicon_url = f"{parsed.scheme}://{domain}{fav_raw}"
                    elif fav_raw.startswith('http'):
                        favicon_url = fav_raw
    except Exception:
        pass

    if not title:
        title = domain or clean_url

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            WebLinkCache.insert(
                url=clean_url,
                domain=domain,
                title=title,
                description=description,
                image_url=image_url,
                favicon_url=favicon_url,
                site_name=site_name,
                fetched_at=now,
            ).on_conflict_replace().execute()

    meta_dict = {
        'url': clean_url,
        'domain': domain,
        'title': title,
        'description': description,
        'imageUrl': image_url,
        'faviconUrl': favicon_url,
        'siteName': site_name,
        'fetchedAt': now,
    }
    return {'ok': True, 'metadata': meta_dict, 'fromCache': False}


def save_signature_orm(note_id=None, points_json='[]', image_data=''):
    """
    Registra trazos manuscritos o firma digital en SQLite.
    Migrado de SignatureEntity de Android para la versión PC.
    """
    now_ms = int(time.time() * 1000)
    nid = int(note_id) if note_id is not None and str(note_id).isdigit() else None
    pts = points_json if isinstance(points_json, str) else json.dumps(points_json or [], ensure_ascii=False)
    img = str(image_data or '')

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        with db.atomic():
            rec = SignatureRecord.create(
                note_id=nid,
                points_json=pts,
                image_data=img,
                created_at=now_ms,
            )
    return {'ok': True, 'signature': rec.to_dict()}


def get_signatures_orm(note_id=None):
    """Consulta firmas y trazos manuscritos guardados en SQLite."""
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        q = SignatureRecord.select().order_by(SignatureRecord.created_at.desc())
        if note_id is not None:
            try:
                q = q.where(SignatureRecord.note_id == int(note_id))
            except (ValueError, TypeError):
                pass
        items = [s.to_dict() for s in q]
    return {'ok': True, 'signatures': items}


