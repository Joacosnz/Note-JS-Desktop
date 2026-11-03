#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Note JS — Backend en Python con SQLite + Peewee ORM y PyWebView
Servidor HTTP + API REST + Empaquetador para VS Code / PyInstaller (.exe)
"""

import os
import sys

# Redirigir stdout y stderr en modo ejecutable (--noconsole) para evitar bloqueos en Windows
if sys.stdout is None:
    try:
        sys.stdout = open(os.devnull, 'w')
    except Exception:
        pass
if sys.stderr is None:
    try:
        sys.stderr = open(os.devnull, 'w')
    except Exception:
        pass

import io
import json
import time
import uuid
import datetime
import zipfile
from urllib.parse import urlparse, unquote, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from pdf_documents import MAX_PDF_BYTES, store_pdf, resolve_pdf
from cover_images import MAX_COVER_BYTES, store_cover, resolve_cover
from onboarding import initialize_first_run
from firebase_connection import load_firebase_config, SIGN_IN_HANDOFF
from firebase_connection import load_firebase_config, SIGN_IN_HANDOFF

from models import (
    DATA_DIR,
    DB_PATH,
    DB_LOCK,
    db,
    Block,
    Note,
    init_db,
    get_bootstrap_data,
    save_single_note,
    delete_single_note,
    sync_all_data,
    save_folders_list,
    move_folder_hierarchy_orm,
    update_folder_emoji_orm,
    save_settings_dict,
    get_note_history_list,
    create_manual_note_snapshot,
    revert_note_to_version,
    delete_note_history_version,
    resolve_local_image_path,
    get_note_blocks_orm,
    update_block_order_orm,
    update_batch_blocks_order_orm,
    sync_blocks_from_note_html_orm,
    query_smart_folder_orm,
    save_smart_folder_orm,
    delete_smart_folder_orm,
    get_reminders_orm,
    save_reminder_orm,
    delete_reminder_orm,
    sync_reminders_orm,
    fetch_weblink_metadata_orm,
    save_signature_orm,
    get_signatures_orm,
    add_child_block,
    move_child_block,
    reorder_children,
    soft_delete_block,
    restore_block,
    resolve_subtree_record_map,
    migrate_legacy_notes_to_blocks,
    build_op_set,
    build_op_list_after,
    apply_operation,
    apply_transaction,
)
from rich_text import (
    rich_text_to_plain_text,
    plain_text_to_rich_text,
    rich_text_to_html,
    html_to_rich_text,
    validate_block,
    is_valid_block_type,
    BLOCK_SCHEMAS,
    is_container_block,
    CONTAINER_BLOCK_TYPES,
    LEAF_BLOCK_TYPES,
    TOGGLEABLE_HEADER_TYPES,
)




def get_base_dir():
    """Obtiene el directorio de recursos estáticos (compatible con PyInstaller --onefile)."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
PORT = int(os.environ.get('DEFAULT_APP_PORT', os.environ.get('APP_PORT', 3000)))


def build_vscode_project_zip():
    """Genera un archivo .zip en memoria con el proyecto completo Python + SQLite + Peewee + PyWebView listo para VS Code."""
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        files_to_pack = [
            ('models.py', os.path.join(BASE_DIR, 'models.py')),
            ('peewee.py', os.path.join(BASE_DIR, 'peewee.py')),
            ('rich_text.py', os.path.join(BASE_DIR, 'rich_text.py')),
            ('pdf_documents.py', os.path.join(BASE_DIR, 'pdf_documents.py')),
            ('cover_images.py', os.path.join(BASE_DIR, 'cover_images.py')),
            ('onboarding.py', os.path.join(BASE_DIR, 'onboarding.py')),
            ('welcome_notes.json', os.path.join(BASE_DIR, 'welcome_notes.json')),
            ('firebase_connection.py', os.path.join(BASE_DIR, 'firebase_connection.py')),
            ('backend.py', os.path.join(BASE_DIR, 'backend.py')),
            ('desktop_app.py', os.path.join(BASE_DIR, 'desktop_app.py')),
            ('requirements.txt', os.path.join(BASE_DIR, 'requirements.txt')),
            ('build_exe.bat', os.path.join(BASE_DIR, 'build_exe.bat')),
            ('build_linux.sh', os.path.join(BASE_DIR, 'build_linux.sh')),
            ('run_desktop.bat', os.path.join(BASE_DIR, 'run_desktop.bat')),
            ('run_server.bat', os.path.join(BASE_DIR, 'run_server.bat')),
            ('dist/NoteJS.exe', os.path.join(BASE_DIR, 'dist', 'NoteJS.exe')),
            ('frontend/index.html', os.path.join(FRONTEND_DIR, 'index.html')),
            ('frontend/styles.css', os.path.join(FRONTEND_DIR, 'styles.css')),
            ('frontend/app.js', os.path.join(FRONTEND_DIR, 'app.js')),
            ('frontend/pdf-integration.js', os.path.join(FRONTEND_DIR, 'pdf-integration.js')),
            ('frontend/pdf-viewer.html', os.path.join(FRONTEND_DIR, 'pdf-viewer.html')),
            ('frontend/pdf-viewer.css', os.path.join(FRONTEND_DIR, 'pdf-viewer.css')),
            ('frontend/pdf-viewer.mjs', os.path.join(FRONTEND_DIR, 'pdf-viewer.mjs')),
            ('frontend/vendor/pdf-lib.min.js', os.path.join(FRONTEND_DIR, 'vendor', 'pdf-lib.min.js')),
            ('frontend/vendor/pdf-lib.LICENSE.md', os.path.join(FRONTEND_DIR, 'vendor', 'pdf-lib.LICENSE.md')),
        ]
        for filename in ('firebase-config.json','firebase-sdk-entry.mjs','firebase-client.mjs','firebase-sync-core.mjs','firebase-mobile-codec.mjs','firebase-signin.html','desktop-menu.js','desktop-polish.css','cloud-table-editor.js','note-cover-contract.mjs','note-cover-photos.js','microsoft-auth.mjs','microsoft-signin.html'):
            files_to_pack.append((f'frontend/{filename}', os.path.join(FRONTEND_DIR, filename)))
        files_to_pack.append(('frontend/vendor/firebase-sdk.mjs', os.path.join(FRONTEND_DIR, 'vendor', 'firebase-sdk.mjs')))
        for arcname, fpath in files_to_pack:
            if os.path.exists(fpath):
                zf.write(fpath, arcname=f"NoteJS-Python-PyWebView/{arcname}")

        for directory, archive_root in (
            (os.path.join(FRONTEND_DIR, 'vendor', 'pdfjs'), 'frontend/vendor/pdfjs'),
            (os.path.join(DATA_DIR, 'attachments', 'pdfs'), 'attachments/pdfs'),
            (os.path.join(DATA_DIR, 'attachments', 'covers'), 'attachments/covers'),
        ):
            for folder, _, filenames in os.walk(directory):
                for filename in filenames:
                    full_path = os.path.join(folder, filename)
                    relative = os.path.relpath(full_path, directory).replace(os.sep, '/')
                    zf.write(full_path, arcname=f'NoteJS-Python-PyWebView/{archive_root}/{relative}')

        # Incluir base de datos SQLite actual con las notas del usuario si existe
        if os.path.exists(DB_PATH):
            zf.write(DB_PATH, arcname="NoteJS-Python-PyWebView/notejs.db")

        readme_content = """# Note JS — Desktop App (Python + SQLite + Peewee ORM + PyWebView)

## Arquitectura (Sin Electron)
- **`models.py`**: Capa de datos relacional usando **SQLite + Peewee ORM** (`Note`, `NoteHistory`, `Folder`, `Setting`) con modo WAL y transacciones atómicas (`db.atomic()`).
- **`desktop_app.py`**: Ventana nativa de escritorio con **PyWebView** (`webview.create_window`) y puente directo JS <-> Python (`window.pywebview.api`).
- **`backend.py`**: Servidor HTTP multihilo local y endpoints REST sincronizados con Peewee ORM.
- **`frontend/`**: Interfaz en HTML5, CSS3 y JavaScript Vanilla (`index.html`, `styles.css`, `app.js`).
- **`build_exe.bat` / `build_linux.sh`**: Scripts para compilar a ejecutable nativo `.exe` o binario de Linux con **PyInstaller**.

## Cómo ejecutar en VS Code (Con Ventana Nativa PyWebView)
1. Abre esta carpeta en **Visual Studio Code**.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicia la aplicación nativa de escritorio con **PyWebView**:
   ```bash
   python desktop_app.py
   ```

## Cómo compilar a `.exe` en Windows desde VS Code
Ejecuta en la terminal integrada de VS Code:
```bat
.\\build_exe.bat
```
O directamente con PyInstaller:
```bat
pip install peewee pywebview pyinstaller
pyinstaller --noconsole --onefile --add-data "frontend;frontend" --name "NoteJS" desktop_app.py
```
El ejecutable aparecerá en **`dist/NoteJS.exe`** (ligero y nativo con PyWebView, sin el peso de Electron).
"""
        zf.writestr("NoteJS-Python-PyWebView/README.md", readme_content)

    mem_zip.seek(0)
    return mem_zip.getvalue()


# -----------------------------------------------------------------------------
# Operaciones Canónicas de Bloques (API REST y PyWebView Bridge)
# -----------------------------------------------------------------------------

def resolve_block_record_map(root_block_id, include_trashed=False):
    """
    Recorrido BFS que resuelve el subárbol completo de bloques a partir de un ID raíz,
    devolviendo un diccionario normalizado { "block": { "<id>": { "value": <data>, "role": "editor" } } }
    con prevención estricta de ciclos y soporte para búsqueda defensiva bidireccional.
    """
    root_id = str(root_block_id or '').strip()
    if not root_id:
        return {'block': {}}

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        root = Block.get_or_none(Block.id == root_id)
        if not root:
            # Comprobar si corresponde al note_id de una página migrada
            try:
                nid = int(root_id)
                root = Block.get_or_none((Block.note_id == nid) & (Block.type == 'page'))
            except (ValueError, TypeError):
                root = None

        if not root:
            return {'block': {}}

        if not include_trashed and root.alive == 0:
            return {'block': {}}

        record_map = {'block': {}}
        queue = [root]
        visited = {str(root.id)}

        while queue:
            curr = queue.pop(0)
            if not include_trashed and curr.alive == 0:
                continue

            record_map['block'][str(curr.id)] = {
                'value': curr.to_dict(),
                'role': 'editor',
            }

            try:
                content_ids = json.loads(curr.content or '[]')
                if not isinstance(content_ids, list):
                    content_ids = []
            except Exception:
                content_ids = []

            for cid in content_ids:
                cid_str = str(cid)
                if cid_str not in visited:
                    visited.add(cid_str)
                    child = Block.get_or_none(Block.id == cid_str)
                    if child and (include_trashed or child.alive == 1):
                        queue.append(child)

            # Búsqueda defensiva de bloques hijos que apunten a este bloque como parent_id
            children_query = Block.select().where(
                (Block.parent_id == str(curr.id)) &
                (Block.alive == 1 if not include_trashed else True)
            )
            for c_blk in children_query:
                c_id = str(c_blk.id)
                if c_id not in visited:
                    visited.add(c_id)
                    queue.append(c_blk)

        return record_map


def get_record_map_api(root_id, include_trashed=False):
    """
    Resuelve el recordMap canónico para un bloque o nota raíz.
    Si el ID corresponde a una nota legacy no migrada, ejecuta la migración y reintenta.
    """
    if not root_id:
        return {'ok': False, 'error': 'Root ID required', 'recordMap': {'block': {}}}, 400

    r_id_str = str(root_id).strip()
    rmap = resolve_block_record_map(r_id_str, include_trashed=include_trashed)
    if rmap.get('block'):
        return {'ok': True, 'rootId': r_id_str, 'recordMap': rmap}, 200

    # Comprobar si existe como nota legacy
    try:
        nid = int(r_id_str)
        note = Note.get_or_none(Note.id == nid)
        if note:
            migrate_legacy_notes_to_blocks()
            rmap = resolve_block_record_map(r_id_str, include_trashed=include_trashed)
            if rmap.get('block'):
                return {'ok': True, 'rootId': r_id_str, 'recordMap': rmap}, 200
    except (ValueError, TypeError):
        pass

    return {'ok': False, 'error': f"Root block or note '{r_id_str}' not found", 'recordMap': {'block': {}}}, 404


def get_block_api(block_id, resolve_tree=False, include_trashed=False):
    """
    Obtiene un bloque individual por su ID.
    Si resolve_tree es True, resuelve el subárbol completo en formato recordMap.
    """
    if not block_id:
        return {'ok': False, 'error': 'Block ID required'}, 400

    bid = str(block_id).strip()
    if resolve_tree:
        return get_record_map_api(bid, include_trashed=include_trashed)

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        blk = Block.get_or_none(Block.id == bid)
        if blk is None or (blk.alive == 0 and not include_trashed):
            return {'ok': False, 'error': f"Block '{bid}' not found"}, 404
        return {'ok': True, 'block': blk.to_dict()}, 200


def create_block_api(block_data, target_index=None, after_id=None, before_id=None):
    """
    Crea un bloque en SQLite con asignación de UUIDv4, validación de ancestros,
    detección de jerarquías circulares e inserción ordenada en el array 'content' del contenedor.
    """
    if not isinstance(block_data, dict):
        return {'ok': False, 'error': 'Block data must be a dictionary'}, 400

    # Unpack block data dictionary (supports flat payload and nested {'block': {...}})
    if isinstance(block_data.get('block'), dict):
        bdata = dict(block_data['block'])
        # Inherit top-level metadata fields if not defined inside bdata
        for key in ('id', 'type', 'properties', 'format', 'content', 'space_id', 'note_id', 'alive', 'crdt_data', 'permissions', 'sort_index'):
            if key not in bdata and key in block_data:
                bdata[key] = block_data[key]
    else:
        bdata = dict(block_data)

    bid = str(bdata.get('id') or block_data.get('id') or uuid.uuid4()).strip()
    btype_raw = bdata.get('type') or block_data.get('type')
    btype = str(btype_raw or '').strip().lower()

    if btype_raw and not is_valid_block_type(btype):
        return {'ok': False, 'error': f"Unknown or unsupported block type: '{btype}'"}, 400

    is_valid, err_msg = validate_block(bdata)
    if not is_valid:
        return {'ok': False, 'error': f"Block validation failed: {err_msg}"}, 400

    parent_id = (
        bdata.get('parent_id')
        or bdata.get('parentId')
        or block_data.get('parent_id')
        or block_data.get('parentId')
    )
    if parent_id is not None:
        parent_id = str(parent_id).strip()
        if not parent_id:
            parent_id = None

    t_idx = None
    for cand in (
        bdata.get('target_index'),
        bdata.get('targetIndex'),
        block_data.get('target_index'),
        block_data.get('targetIndex'),
        target_index,
    ):
        if cand is not None:
            t_idx = cand
            break

    a_id = (
        bdata.get('after_id')
        or bdata.get('afterId')
        or block_data.get('after_id')
        or block_data.get('afterId')
        or after_id
    )
    b_id = (
        bdata.get('before_id')
        or bdata.get('beforeId')
        or block_data.get('before_id')
        or block_data.get('beforeId')
        or before_id
    )

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        if parent_id is not None:
            parent = Block.get_or_none(Block.id == parent_id)
            if parent is None:
                return {'ok': False, 'error': f"Parent block with id '{parent_id}' does not exist"}, 404
            if parent.alive == 0:
                return {'ok': False, 'error': f"Cannot add child to trashed parent block '{parent_id}'"}, 400
            if parent_id == bid:
                return {'ok': False, 'error': "Block cannot be its own parent"}, 400

            # Validación de contenedor estructural de Notion
            if not is_container_block(parent.type, parent.format):
                return {'ok': False, 'error': f"Block '{parent.type}' is a leaf node or non-toggleable header and cannot accept children"}, 400

            # Detección de ciclos
            visited = {parent_id}
            curr = parent
            while curr and curr.parent_id:
                p_up = str(curr.parent_id)
                if p_up == bid:
                    return {'ok': False, 'error': "Circular block hierarchy detected"}, 400
                if p_up in visited:
                    break
                visited.add(p_up)
                curr = Block.get_or_none(Block.id == p_up)

            # Determinar índice de inserción en parent.content
            try:
                p_content = json.loads(parent.content or '[]')
                if not isinstance(p_content, list):
                    p_content = []
            except Exception:
                p_content = []

            idx = None
            calc_after_id = None
            if a_id is not None and str(a_id) in p_content:
                idx = p_content.index(str(a_id)) + 1
                calc_after_id = str(a_id)
            elif b_id is not None and str(b_id) in p_content:
                idx = p_content.index(str(b_id))
                calc_after_id = p_content[idx - 1] if idx > 0 else None
            elif t_idx is not None:
                try:
                    idx = max(0, min(int(t_idx), len(p_content)))
                    calc_after_id = p_content[idx - 1] if idx > 0 else None
                except (ValueError, TypeError):
                    idx = None
                    calc_after_id = None

            child_dict = {
                'id': bid,
                'space_id': bdata.get('space_id') or getattr(parent, 'space_id', 'default_space'),
                'type': btype,
                'properties': bdata.get('properties', {}),
                'content': bdata.get('content', []),
                'format': bdata.get('format', {}),
                'crdt_data': bdata.get('crdt_data', {'clock': 1}),
                'alive': int(bdata.get('alive', 1)),
                'permissions': bdata.get('permissions', []),
                'note_id': bdata.get('note_id', getattr(parent, 'note_id', 0)),
                'sort_index': bdata.get('sort_index', 'a0'),
            }
            try:
                child = add_child_block(parent_id, child_dict, index=idx, after_id=calc_after_id)
            except ValueError as e:
                return {'ok': False, 'error': str(e)}, 400

            parent_refreshed = Block.get_or_none(Block.id == parent_id)
            return {
                'ok': True,
                'block': child.to_dict(),
                'parent': parent_refreshed.to_dict() if parent_refreshed else None,
            }, 201
        else:
            # Bloque raíz sin contenedor ejecutado mediante protocolo de transacciones atómicas
            child_dict = {
                'id': bid,
                'space_id': str(bdata.get('space_id') or 'default_space'),
                'type': btype,
                'properties': bdata.get('properties', {}),
                'content': bdata.get('content', []),
                'format': bdata.get('format', {}),
                'crdt_data': bdata.get('crdt_data', {'clock': 1}),
                'alive': int(bdata.get('alive', 1)),
                'permissions': bdata.get('permissions', []),
                'note_id': bdata.get('note_id', 0),
                'sort_index': bdata.get('sort_index', 'a0'),
                'parent_id': None,
                'parent_table': str(bdata.get('parent_table') or 'space'),
            }
            try:
                op_set = build_op_set(bid, child_dict, space_id=child_dict['space_id'])
                apply_transaction([op_set])
                child = Block.get_by_id(bid)
                return {'ok': True, 'block': child.to_dict(), 'parent': None}, 201
            except ValueError as e:
                return {'ok': False, 'error': str(e)}, 400


def apply_transactions_api(data):
    """
    Ejecuta un lote de operaciones transaccionales Notion (op.set, op.listAfter, etc.)
    atómicamente dentro de una única transacción SQLite con rollback completo ante errores.
    """
    if not isinstance(data, dict):
        return {'ok': False, 'error': 'Transaction payload must be a dictionary'}, 400

    operations = data.get('operations')
    if operations is None and 'transactions' in data:
        tx_list = data['transactions']
        operations = []
        if isinstance(tx_list, list):
            for tx in tx_list:
                if isinstance(tx, dict) and 'operations' in tx:
                    operations.extend(tx['operations'])
    elif operations is None and isinstance(data.get('ops'), list):
        operations = data.get('ops')

    if not isinstance(operations, list):
        return {'ok': False, 'error': 'Missing or invalid operations list'}, 400

    try:
        res = apply_transaction(operations)
        return res, 200
    except Exception as e:
        return {'ok': False, 'error': str(e)}, 400



def update_block_api(block_id, updates, expected_version=None):
    """
    Actualiza propiedades semánticas, metadatos visuales o tipo de un bloque,
    incrementando su versión y validando concurrencia optimista mediante expected_version.
    """
    if not block_id:
        return {'ok': False, 'error': 'Block ID required'}, 400
    if not isinstance(updates, dict):
        return {'ok': False, 'error': 'Updates must be a dictionary'}, 400

    up_data = updates.get('block', updates) if isinstance(updates.get('block'), dict) else updates

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        blk = Block.get_or_none(Block.id == str(block_id))
        if blk is None:
            return {'ok': False, 'error': f"Block with id '{block_id}' does not exist"}, 404

        exp_v = up_data.get('expected_version', expected_version)
        if exp_v is not None:
            try:
                exp_v_int = int(exp_v)
                if blk.version != exp_v_int:
                    return {
                        'ok': False,
                        'error': 'Version conflict',
                        'current_version': blk.version,
                        'expected_version': exp_v_int,
                    }, 409
            except (ValueError, TypeError):
                pass

        now_ms = int(time.time() * 1000)
        with db.atomic():
            blk.last_version = blk.version
            blk.version += 1
            blk.last_edited_time = now_ms
            blk.updated_at = datetime.datetime.now()

            if 'type' in up_data:
                new_type = str(up_data['type']).strip().lower()
                if is_valid_block_type(new_type):
                    blk.type = new_type

            if 'properties' in up_data:
                new_props = up_data['properties']
                if isinstance(new_props, dict):
                    try:
                        curr_props = json.loads(blk.properties or '{}')
                        if not isinstance(curr_props, dict):
                            curr_props = {}
                    except Exception:
                        curr_props = {}
                    curr_props.update(new_props)
                    blk.properties = json.dumps(curr_props, ensure_ascii=False)
                elif isinstance(new_props, str):
                    blk.properties = new_props

            if 'format' in up_data:
                new_fmt = up_data['format']
                if isinstance(new_fmt, dict):
                    try:
                        curr_fmt = json.loads(blk.format or '{}')
                        if not isinstance(curr_fmt, dict):
                            curr_fmt = {}
                    except Exception:
                        curr_fmt = {}
                    curr_fmt.update(new_fmt)
                    blk.format = json.dumps(curr_fmt, ensure_ascii=False)
                elif isinstance(new_fmt, str):
                    blk.format = new_fmt

            if 'content' in up_data:
                new_cnt = up_data['content']
                if isinstance(new_cnt, list):
                    blk.content = json.dumps([str(x) for x in new_cnt], ensure_ascii=False)

            if 'alive' in up_data:
                blk.alive = int(up_data['alive'])

            # Registro de mutación CRDT
            try:
                crdt_obj = json.loads(blk.crdt_data or '{}')
                if not isinstance(crdt_obj, dict):
                    crdt_obj = {}
            except Exception:
                crdt_obj = {}

            if 'crdt_data' in up_data and isinstance(up_data['crdt_data'], dict):
                crdt_obj.update(up_data['crdt_data'])

            mutations = crdt_obj.get('mutations', [])
            if not isinstance(mutations, list):
                mutations = []
            mutations.append({
                'op': 'update',
                'timestamp': now_ms,
                'version': blk.version,
                'keys': list(up_data.keys()),
            })
            crdt_obj['mutations'] = mutations[-100:]
            crdt_obj['last_mutation_time'] = now_ms
            crdt_obj['clock'] = crdt_obj.get('clock', 0) + 1
            blk.crdt_data = json.dumps(crdt_obj, ensure_ascii=False)

            blk.save()

    return {'ok': True, 'block': blk.to_dict()}, 200


def reorder_block_children_api(parent_id, content_or_data):
    """
    Reordena bloques hijos dentro de un padre o mueve un bloque hijo entre diferentes padres.
    """
    if not parent_id:
        return {'ok': False, 'error': 'Parent ID required'}, 400

    with DB_LOCK:
        db.connect(reuse_if_open=True)
        parent = Block.get_or_none(Block.id == str(parent_id))
        if parent is None:
            return {'ok': False, 'error': f"Parent block with id '{parent_id}' does not exist"}, 404

        # Caso 1: Lista directa de UUIDs
        if isinstance(content_or_data, list):
            new_order = [str(x) for x in content_or_data]
            reorder_children(parent_id, new_order)
            parent_ref = Block.get_by_id(str(parent_id))
            return {'ok': True, 'parent': parent_ref.to_dict()}, 200

        # Caso 2: Diccionario con clave 'content' o movimiento específico
        if isinstance(content_or_data, dict):
            if 'content' in content_or_data and isinstance(content_or_data['content'], list):
                new_order = [str(x) for x in content_or_data['content']]
                reorder_children(parent_id, new_order)
                parent_ref = Block.get_by_id(str(parent_id))
                return {'ok': True, 'parent': parent_ref.to_dict()}, 200

            # Movimiento relativo o cambio de padre
            child_id = content_or_data.get('child_id') or content_or_data.get('childId')
            if child_id:
                child_id_str = str(child_id)
                target_parent_id = str(content_or_data.get('new_parent_id') or parent_id)
                t_idx = content_or_data.get('target_index')
                a_id = content_or_data.get('after_id')
                b_id = content_or_data.get('before_id')

                # Calcular índice de destino
                target_parent = Block.get_or_none(Block.id == target_parent_id)
                if target_parent:
                    try:
                        tp_content = json.loads(target_parent.content or '[]')
                        if not isinstance(tp_content, list):
                            tp_content = []
                    except Exception:
                        tp_content = []

                    if a_id is not None and str(a_id) in tp_content:
                        t_idx = tp_content.index(str(a_id)) + 1
                    elif b_id is not None and str(b_id) in tp_content:
                        t_idx = tp_content.index(str(b_id))

                child = move_child_block(child_id_str, target_parent_id, index=t_idx)
                parent_ref = Block.get_by_id(str(parent_id))
                return {
                    'ok': True,
                    'child': child.to_dict(),
                    'parent': parent_ref.to_dict(),
                }, 200

        return {'ok': False, 'error': 'Invalid reorder payload (expected list or dict with content/child_id)'}, 400


def soft_delete_block_api(block_id, permanent=False):
    """
    Realiza un borrado lógico (alive = 0) de un bloque y su subárbol,
    o borrado físico permanente de la base de datos si permanent es True.
    """
    if not block_id:
        return {'ok': False, 'error': 'Block ID required'}, 400

    bid = str(block_id).strip()
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        blk = Block.get_or_none(Block.id == bid)
        if blk is None:
            return {'ok': False, 'error': f"Block with id '{bid}' does not exist"}, 404

        if permanent:
            with db.atomic():
                Block.delete().where(Block.id == bid).execute()
            return {'ok': True, 'deletedId': bid, 'permanent': True}, 200
        else:
            soft_delete_block(bid)
            return {'ok': True, 'deletedId': bid, 'alive': 0}, 200


def restore_block_api(block_id):
    """
    Restaura un bloque borrado lógicamente (alive = 1) y lo reinserta en su contenedor.
    """
    if not block_id:
        return {'ok': False, 'error': 'Block ID required'}, 400

    bid = str(block_id).strip()
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        blk = Block.get_or_none(Block.id == bid)
        if blk is None:
            return {'ok': False, 'error': f"Block with id '{bid}' does not exist"}, 404

        restore_block(bid)
        refreshed = Block.get_by_id(bid)
        return {'ok': True, 'restoredId': bid, 'alive': 1, 'block': refreshed.to_dict()}, 200


def convert_rich_text_api(payload):
    """
    Convierte bidireccionalmente entre HTML, tuplas de rich text de Notion y texto plano.
    """
    if not isinstance(payload, dict):
        return {'ok': False, 'error': 'Payload must be a dictionary'}, 400

    if 'html' in payload:
        return {'ok': True, 'rich_text': html_to_rich_text(payload['html'])}, 200
    elif 'rich_text' in payload:
        rt = payload['rich_text']
        return {
            'ok': True,
            'html': rich_text_to_html(rt),
            'plain_text': rich_text_to_plain_text(rt),
        }, 200
    elif 'plain_text' in payload:
        return {'ok': True, 'rich_text': plain_text_to_rich_text(payload['plain_text'])}, 200
    else:
        return {'ok': False, 'error': 'Payload must contain html, rich_text, or plain_text'}, 400





class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class NoteJSRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _send_json(self, data, status=200):
        payload = json.dumps(data, ensure_ascii=False, default=str).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(payload)

    def _read_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode('utf-8')
        return json.loads(raw) if raw else {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_HEAD(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path in ('/health', '/api/bootstrap', '/'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8' if path == '/' else 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return
        self.do_GET()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path == '/api/firebase/config':
            self._send_json(load_firebase_config(BASE_DIR))
            return

        if path == '/api/firebase/config':
            self._send_json(load_firebase_config(BASE_DIR))
            return

        if path.startswith('/api/covers/'):
            try:
                photo = resolve_cover(path[len('/api/covers/'):], os.path.join(DATA_DIR, 'attachments', 'covers'))
                data = photo.read_bytes()
            except (ValueError, FileNotFoundError) as exc:
                self._send_json({'ok': False, 'error': str(exc)}, status=404)
                return
            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'private, max-age=31536000, immutable')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(data)
            return

        if path.startswith('/api/pdfs/'):
            try:
                pdf_path = resolve_pdf(path[len('/api/pdfs/'):], os.path.join(DATA_DIR, 'attachments', 'pdfs'))
                data = pdf_path.read_bytes()
            except (ValueError, FileNotFoundError) as exc:
                self._send_json({'ok': False, 'error': str(exc)}, status=404)
                return
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(data)
            return

        # Healthcheck endpoint
        if path == '/health':
            self._send_json({'status': 'healthy', 'ok': True, 'port': PORT})
            return

        # 1. API: Obtener estado completo desde SQLite + Peewee ORM
        if path == '/api/bootstrap':
            self._send_json(get_bootstrap_data())
            return

        # 1-RT. API: Rich Text Converter GET ayuda de uso
        if path == '/api/blocks/rich-text/convert':
            self._send_json({'ok': True, 'usage': 'POST with html, rich_text, or plain_text payload'})
            return

        # 1-RM. API: Resolver recordMap de un bloque raíz (/api/blocks/<id>/recordMap)
        if path.startswith('/api/blocks/') and path.endswith('/recordMap'):
            bid = path[len('/api/blocks/'):-len('/recordMap')].strip('/')
            qs = parse_qs(parsed.query)
            inc_trashed = qs.get('include_trashed', ['false'])[0].lower() == 'true'
            res, status = get_record_map_api(bid, include_trashed=inc_trashed)
            self._send_json(res, status=status)
            return

        # 1-RN. API: Resolver recordMap de una página/nota raíz (/api/notes/<id>/recordMap)
        if path.startswith('/api/notes/') and path.endswith('/recordMap'):
            nid = path[len('/api/notes/'):-len('/recordMap')].strip('/')
            qs = parse_qs(parsed.query)
            inc_trashed = qs.get('include_trashed', ['false'])[0].lower() == 'true'
            res, status = get_record_map_api(nid, include_trashed=inc_trashed)
            self._send_json(res, status=status)
            return

        # 1-BLK. API: Obtener bloque individual por ID (/api/blocks/<id>)
        if path.startswith('/api/blocks/') and not any(path.startswith(f'/api/blocks/{r}') for r in ('order', 'batch', 'rich-text')):
            bid = path[len('/api/blocks/'):].strip('/')
            if bid:
                qs = parse_qs(parsed.query)
                resolve = (qs.get('resolve', ['false'])[0].lower() == 'true') or (qs.get('resolve_tree', ['false'])[0].lower() == 'true')
                inc_trashed = qs.get('include_trashed', ['false'])[0].lower() == 'true'
                res, status = get_block_api(bid, resolve_tree=resolve, include_trashed=inc_trashed)
                self._send_json(res, status=status)
                return

        # 1b. API: Obtener historial de versiones de una nota en SQLite
        if path.startswith('/api/notes/') and path.endswith('/history'):
            middle = path[len('/api/notes/'):-len('/history')].strip('/')
            try:
                note_id = int(middle)
            except ValueError:
                self._send_json({'ok': False, 'error': 'ID de nota inválido'}, status=400)
                return
            self._send_json(get_note_history_list(note_id))
            return

        # 1c. API: Obtener bloques de una nota en SQLite
        if path.startswith('/api/notes/') and path.endswith('/blocks'):
            middle = path[len('/api/notes/'):-len('/blocks')].strip('/')
            try:
                note_id = int(middle)
            except ValueError:
                self._send_json({'ok': False, 'error': 'ID de nota inválido'}, status=400)
                return
            self._send_json(get_note_blocks_orm(note_id))
            return

        # 1d. API: Consulta dinámica para carpetas inteligentes en SQLite
        if path in ('/api/smart-folders/query', '/api/folders/smart/query'):
            qs = parse_qs(parsed.query)
            folder_name = qs.get('folder', qs.get('folderName', ['']))[0]
            match_mode = qs.get('matchMode', ['all'])[0]
            rules_raw = qs.get('rules', [''])[0]
            rules = None
            if rules_raw:
                try:
                    rules = json.loads(rules_raw)
                except Exception:
                    rules = None
            self._send_json(query_smart_folder_orm(folder_name=folder_name, rules=rules, match_mode=match_mode))
            return

        # 1e. API: Obtener recordatorios y eventos de calendario en SQLite
        if path == '/api/reminders':
            self._send_json(get_reminders_orm())
            return

        # 1f. API: Obtener metadatos OpenGraph para enlaces web
        if path in ('/api/weblinks/metadata', '/api/links/metadata'):
            qs = parse_qs(parsed.query)
            target_url = qs.get('url', [''])[0]
            self._send_json(fetch_weblink_metadata_orm(target_url))
            return

        # 1g. API: Obtener firmas manuscritas
        if path == '/api/signatures':
            qs = parse_qs(parsed.query)
            nid_str = qs.get('noteId', [None])[0]
            self._send_json(get_signatures_orm(nid_str))
            return

        # 2. Descarga del proyecto completo para VS Code, PyWebView y PyInstaller (.zip)
        if path == '/download/NoteJS-Windows.exe':
            exe_path = os.path.join(BASE_DIR, 'dist', 'NoteJS.exe')
            if os.path.exists(exe_path):
                with open(exe_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/vnd.microsoft.portable-executable')
                self.send_header('Content-Disposition', 'attachment; filename="NoteJS.exe"')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        if path in ('/download/NoteJS-VSCode-Python.zip', '/download/NoteJS-Linux.AppImage'):
            zip_bytes = build_vscode_project_zip()
            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="NoteJS-Python-PyWebView-Peewee.zip"')
            self.send_header('Content-Length', str(len(zip_bytes)))
            self.end_headers()
            self.wfile.write(zip_bytes)
            return

        if path in ('/download/build_exe.bat', '/download/NoteJS-Windows-PC.bat'):
            bat_path = os.path.join(BASE_DIR, 'build_exe.bat')
            content = open(bat_path, 'rb').read() if os.path.exists(bat_path) else b''
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Disposition', 'attachment; filename="build_exe.bat"')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        if path in ('/download/build_linux.sh', '/download/notejs-linux-pc.sh'):
            sh_path = os.path.join(BASE_DIR, 'build_linux.sh')
            content = open(sh_path, 'rb').read() if os.path.exists(sh_path) else b''
            self.send_response(200)
            self.send_header('Content-Type', 'application/x-sh')
            self.send_header('Content-Disposition', 'attachment; filename="build_linux.sh"')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        # 3. Servir archivos del Frontend (index.html, styles.css, app.js)
        if path == '/' or path == '/index.html':
            target_file = os.path.join(FRONTEND_DIR, 'index.html')
        elif path.startswith('/frontend/'):
            rel = path[len('/frontend/'):]
            target_file = os.path.join(FRONTEND_DIR, rel)
        else:
            rel = path.lstrip('/')
            target_file = os.path.join(FRONTEND_DIR, rel)
            if not os.path.exists(target_file):
                target_file = os.path.join(BASE_DIR, 'public', rel)

        if os.path.exists(target_file) and os.path.isfile(target_file):
            ext = os.path.splitext(target_file)[1].lower()
            mime_map = {
                '.html': 'text/html; charset=utf-8',
                '.css': 'text/css; charset=utf-8',
                '.js': 'application/javascript; charset=utf-8',
                '.mjs': 'application/javascript; charset=utf-8',
                '.wasm': 'application/wasm',
                '.pdf': 'application/pdf',
                '.bcmap': 'application/octet-stream',
                '.json': 'application/json; charset=utf-8',
                '.png': 'image/png',
                '.svg': 'image/svg+xml',
                '.ico': 'image/x-icon',
                '.woff2': 'font/woff2',
                '.woff': 'font/woff',
                '.ttf': 'font/ttf',
            }
            ctype = mime_map.get(ext, 'application/octet-stream')
            with open(target_file, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(data)
            return

        # Fallback SPA a index.html
        index_file = os.path.join(FRONTEND_DIR, 'index.html')
        if os.path.exists(index_file):
            with open(index_file, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404, 'Archivo no encontrado')

    def do_POST(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path.startswith('/api/firebase/auth/'):
            origin = self.headers.get('Origin')
            if origin != 'http://' + self.headers.get('Host', '') or self.headers.get('X-NoteJS-Client') != 'firebase':
                self._send_json({'ok': False, 'error': 'Origen no permitido.'}, status=403)
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length < 0 or length > 20000:
                    raise ValueError('Solicitud demasiado grande.')
                body = self._read_json_body()
                if path == '/api/firebase/auth/start':
                    result = {'ok': True, **SIGN_IN_HANDOFF.start()}
                elif path == '/api/firebase/auth/complete':
                    SIGN_IN_HANDOFF.complete(body.get('state'), body.get('credential'))
                    result = {'ok': True}
                elif path == '/api/firebase/auth/poll':
                    result = SIGN_IN_HANDOFF.consume(body.get('state'), body.get('pollToken'))
                else:
                    raise ValueError('Ruta inválida.')
                self._send_json(result)
            except (ValueError, TypeError, AttributeError) as exc:
                self._send_json({'ok': False, 'error': str(exc)}, status=400)
            return

        if path.startswith('/api/firebase/auth/'):
            origin = self.headers.get('Origin')
            if origin != 'http://' + self.headers.get('Host', '') or self.headers.get('X-NoteJS-Client') != 'firebase':
                self._send_json({'ok': False, 'error': 'Origen no permitido.'}, status=403)
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length < 0 or length > 20000:
                    raise ValueError('Solicitud demasiado grande.')
                body = self._read_json_body()
                if path == '/api/firebase/auth/start':
                    result = {'ok': True, **SIGN_IN_HANDOFF.start()}
                elif path == '/api/firebase/auth/complete':
                    SIGN_IN_HANDOFF.complete(body.get('state'), body.get('credential'))
                    result = {'ok': True}
                elif path == '/api/firebase/auth/poll':
                    result = SIGN_IN_HANDOFF.consume(body.get('state'), body.get('pollToken'))
                else:
                    raise ValueError('Ruta inválida.')
                self._send_json(result)
            except (ValueError, TypeError, AttributeError) as exc:
                self._send_json({'ok': False, 'error': str(exc)}, status=400)
            return

        if path == '/api/covers':
            origin = self.headers.get('Origin')
            if origin and origin != 'http://' + self.headers.get('Host', ''):
                self._send_json({'ok': False, 'error': 'Origen no permitido.'}, status=403)
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length <= 0 or length > MAX_COVER_BYTES:
                    self._send_json({'ok': False, 'error': 'El límite por foto es de 20 MB.'}, status=413)
                    return
                if self.headers.get_content_type() != 'image/jpeg':
                    raise ValueError('Seleccioná una foto de portada.')
                result = store_cover(self.rfile.read(length), os.path.join(DATA_DIR, 'attachments', 'covers'))
                self._send_json(result, status=201)
            except (ValueError, OSError) as exc:
                self._send_json({'ok': False, 'error': str(exc)}, status=400)
            return

        if path == '/api/pdfs':
            # Raw binary avoids inflating PDFs into base64 inside the notes database.
            # Browsers cannot send this request cross-origin without a preflight.
            origin = self.headers.get('Origin')
            if origin and origin != 'http://' + self.headers.get('Host', ''):
                self._send_json({'ok': False, 'error': 'Origen no permitido.'}, status=403)
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length <= 0 or length > MAX_PDF_BYTES:
                    self._send_json({'ok': False, 'error': 'El límite por PDF es de 50 MB.'}, status=413)
                    return
                if self.headers.get_content_type() != 'application/pdf':
                    raise ValueError('Selecciona un archivo PDF.')
                name = parse_qs(parsed.query).get('name', ['Documento.pdf'])[0]
                result = store_pdf(self.rfile.read(length), os.path.join(DATA_DIR, 'attachments', 'pdfs'), name)
                self._send_json(result, status=201)
            except (ValueError, OSError) as exc:
                self._send_json({'ok': False, 'error': str(exc)}, status=400)
            return

        try:
            body = self._read_json_body()
        except Exception as e:
            self._send_json({'ok': False, 'error': str(e)}, status=400)
            return

        # Controles de ventana nativa de escritorio
        if path == '/api/window/minimize':
            try:
                import webview
                if webview.windows:
                    webview.windows[0].minimize()
            except Exception:
                pass
            self._send_json({'success': True, 'action': 'minimize'})
            return

        if path == '/api/window/maximize':
            action = 'maximize'
            try:
                import webview
                if webview.windows:
                    win = webview.windows[0]
                    if getattr(win, '_is_maximized', False):
                        win.restore()
                        win._is_maximized = False
                        action = 'restore'
                    else:
                        win.maximize()
                        win._is_maximized = True
                        action = 'maximize'
            except Exception:
                pass
            self._send_json({'success': True, 'action': action})
            return

        if path == '/api/window/close':
            try:
                import webview
                if webview.windows:
                    webview.windows[0].destroy()
            except Exception:
                pass
            self._send_json({'success': True, 'action': 'close'})
            return

        # Guardar o actualizar una nota individual con Peewee ORM
        if path == '/api/notes':
            note_obj = body.get('note', body)
            summary = body.get('summary')
            force_history = bool(body.get('forceHistory'))
            self._send_json(save_single_note(note_obj, summary=summary, force_history=force_history))
            return

        # Crear punto de restauración manual en el historial SQLite de una nota
        if path.startswith('/api/notes/') and path.endswith('/history'):
            middle = path[len('/api/notes/'):-len('/history')].strip('/')
            note_obj = body.get('note', body)
            if isinstance(note_obj, dict) and note_obj.get('id') is None:
                try:
                    note_obj['id'] = int(middle)
                except ValueError:
                    pass
            summary = body.get('summary', 'Punto de restauración manual')
            self._send_json(create_manual_note_snapshot(note_obj, summary=summary))
            return

        # Revertir una nota a una versión anterior guardada en SQLite
        if path.startswith('/api/notes/') and path.endswith('/revert'):
            middle = path[len('/api/notes/'):-len('/revert')].strip('/')
            try:
                note_id = int(middle)
                version_id = int(body.get('versionId'))
            except (ValueError, TypeError):
                self._send_json({'ok': False, 'error': 'ID de nota o versión inválido'}, status=400)
                return
            self._send_json(revert_note_to_version(note_id, version_id))
            return

        # Sincronizar lista completa de notas, carpetas y ajustes con Peewee ORM
        if path == '/api/sync':
            self._send_json(sync_all_data(body))
            return

        # Guardar carpetas y sus iconos de emoji personalizados con Peewee ORM
        if path == '/api/folders':
            self._send_json(save_folders_list(body))
            return

        # Crear o actualizar una Carpeta Inteligente individual en SQLite
        if path in ('/api/smart-folders/save', '/api/folders/smart/save', '/api/smart-folders'):
            name = body.get('name', body.get('folder', ''))
            rules = body.get('rules', [])
            match_mode = body.get('matchMode', 'all')
            emoji = body.get('emoji', '⚙️')
            old_name = body.get('oldName', None)
            result = save_smart_folder_orm(name, rules, match_mode=match_mode, emoji=emoji, old_name=old_name)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Eliminar una Carpeta Inteligente individual en SQLite (sin borrar notas)
        if path in ('/api/smart-folders/delete', '/api/folders/smart/delete'):
            name = body.get('name', body.get('folder', ''))
            result = delete_smart_folder_orm(name)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Mover una carpeta dentro de otra carpeta (convertir en subcarpeta o promover a raíz) en SQLite
        if path == '/api/folders/move':
            source_folder = body.get('sourceFolder', '')
            target_parent = body.get('targetParentFolder', '')
            folders_list = body.get('folders', None)
            folder_emojis = body.get('folderEmojis', None)
            notes_list = body.get('notes', None)
            result = move_folder_hierarchy_orm(
                source_folder,
                target_parent_folder=target_parent,
                folders_list=folders_list,
                folder_emojis=folder_emojis,
                notes_list=notes_list,
            )
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Actualizar el icono de emoji de una carpeta específica en SQLite
        if path == '/api/folders/emoji':
            folder_name = body.get('folder', '')
            emoji = body.get('emoji', '📁')
            result = update_folder_emoji_orm(folder_name, emoji)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Consulta dinámica en la base de datos para Carpetas Inteligentes
        if path in ('/api/smart-folders/query', '/api/folders/smart/query'):
            folder_name = body.get('folder', body.get('folderName', ''))
            rules = body.get('rules', None)
            match_mode = body.get('matchMode', 'all')
            result = query_smart_folder_orm(folder_name=folder_name, rules=rules, match_mode=match_mode)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Guardar ajustes con Peewee ORM
        if path == '/api/settings':
            self._send_json(save_settings_dict(body))
            return

        # Procesar y resolver ruta local de imagen o URL para insertar como bloque en el editor
        if path == '/api/images/resolve':
            raw_path = body.get('path', '')
            result = resolve_local_image_path(raw_path)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Convertidor de Rich Text
        if path == '/api/blocks/rich-text/convert':
            res, status = convert_rich_text_api(body)
            self._send_json(res, status=status)
            return

        # Transacciones atómicas de bloques (Notion transactional protocol)
        if path in ('/api/transactions', '/api/transaction'):
            res, status = apply_transactions_api(body)
            self._send_json(res, status=status)
            return

        # Crear nuevo bloque Notion
        if path == '/api/blocks':
            res, status = create_block_api(body)
            self._send_json(res, status=status)
            return

        # Reordenar hijos de un bloque o mover entre padres
        if path.startswith('/api/blocks/') and path.endswith('/reorder'):
            bid = path[len('/api/blocks/'):-len('/reorder')].strip('/')
            res, status = reorder_block_children_api(bid, body)
            self._send_json(res, status=status)
            return

        # Restaurar bloque borrado lógicamente
        if path.startswith('/api/blocks/') and path.endswith('/restore'):
            bid = path[len('/api/blocks/'):-len('/restore')].strip('/')
            res, status = restore_block_api(bid)
            self._send_json(res, status=status)
            return

        # Actualizar orden fraccionario de un bloque individual O(1)
        if path == '/api/blocks/order':
            block_id = body.get('blockId')
            prev_id = body.get('prevId')
            next_id = body.get('nextId')
            parent_id = body.get('parentId')
            note_id = body.get('noteId')
            result = update_block_order_orm(block_id, prev_id=prev_id, next_id=next_id, parent_id=parent_id, note_id=note_id)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Actualización en lote de múltiples bloques (batch drag & drop)
        if path == '/api/blocks/batch':
            moves = body.get('moves', [])
            result = update_batch_blocks_order_orm(moves)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Actualización de bloque mediante POST /api/blocks/<id>
        if path.startswith('/api/blocks/') and not any(path.startswith(f'/api/blocks/{r}') for r in ('order', 'batch', 'rich-text')):
            bid = path[len('/api/blocks/'):].strip('/')
            if bid:
                qs = parse_qs(parsed.query)
                exp_v = qs.get('expected_version', [None])[0]
                res, status = update_block_api(bid, body, expected_version=exp_v)
                self._send_json(res, status=status)
                return

        # Sincronizar bloques de una nota completa desde HTML
        if path.startswith('/api/notes/') and path.endswith('/blocks/sync'):
            middle = path[len('/api/notes/'):-len('/blocks/sync')].strip('/')
            try:
                note_id = int(middle)
            except ValueError:
                self._send_json({'ok': False, 'error': 'ID de nota inválido'}, status=400)
                return
            blocks_data = body.get('blocks', [])
            result = sync_blocks_from_note_html_orm(note_id, blocks_data)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Guardar o actualizar recordatorio o evento de calendario en SQLite
        if path == '/api/reminders':
            item_data = body.get('reminder', body)
            result = save_reminder_orm(item_data)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Sincronización en lote de recordatorios
        if path == '/api/reminders/sync':
            items = body.get('reminders', [])
            result = sync_reminders_orm(items)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Metadatos de enlace web (POST)
        if path in ('/api/weblinks/metadata', '/api/links/metadata'):
            target_url = body.get('url', '')
            result = fetch_weblink_metadata_orm(target_url)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        # Guardar firma digital o trazos manuscritos
        if path == '/api/signatures':
            nid = body.get('noteId')
            pts = body.get('points', body.get('points_json', '[]'))
            img = body.get('imageData', body.get('image_data', ''))
            result = save_signature_orm(note_id=nid, points_json=pts, image_data=img)
            self._send_json(result, status=200 if result.get('ok') else 400)
            return

        self._send_json({'ok': False, 'error': 'Ruta no encontrada'}, status=404)

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        try:
            body = self._read_json_body()
        except Exception as e:
            self._send_json({'ok': False, 'error': str(e)}, status=400)
            return

        # Actualización de bloque mediante PUT /api/blocks/<id>
        if path.startswith('/api/blocks/') and not any(path.startswith(f'/api/blocks/{r}') for r in ('order', 'batch', 'rich-text')):
            bid = path[len('/api/blocks/'):].strip('/')
            if bid:
                qs = parse_qs(parsed.query)
                exp_v = qs.get('expected_version', [None])[0]
                res, status = update_block_api(bid, body, expected_version=exp_v)
                self._send_json(res, status=status)
                return

        self._send_json({'ok': False, 'error': 'Ruta PUT no válida'}, status=404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        # Borrado de bloque: DELETE /api/blocks/<id>
        if path.startswith('/api/blocks/') and not any(path.startswith(f'/api/blocks/{r}') for r in ('order', 'batch', 'rich-text')):
            bid = path[len('/api/blocks/'):].strip('/')
            if bid:
                qs = parse_qs(parsed.query)
                perm = qs.get('permanent', ['false'])[0].lower() == 'true'
                res, status = soft_delete_block_api(bid, permanent=perm)
                self._send_json(res, status=status)
                return

        # Eliminar recordatorio por ID en SQLite
        if path.startswith('/api/reminders/'):
            rid_str = path[len('/api/reminders/'):].strip().strip('/')
            try:
                rid = int(rid_str)
                self._send_json(delete_reminder_orm(rid))
                return
            except ValueError:
                self._send_json({'ok': False, 'error': 'ID de recordatorio inválido'}, status=400)
                return

        # Eliminar una versión específica del historial de una nota
        if path.startswith('/api/notes/') and '/history/' in path:
            parts = path[len('/api/notes/'):].split('/history/')
            if len(parts) == 2:
                try:
                    note_id = int(parts[0].strip('/'))
                    version_id = int(parts[1].strip('/'))
                except ValueError:
                    self._send_json({'ok': False, 'error': 'ID inválido'}, status=400)
                    return
                self._send_json(delete_note_history_version(note_id, version_id))
                return

        if path.startswith('/api/notes/'):
            note_id_str = path[len('/api/notes/'):].strip()
            try:
                note_id = int(note_id_str)
            except ValueError:
                self._send_json({'ok': False, 'error': 'ID inválido'}, status=400)
                return

            self._send_json(delete_single_note(note_id))
            return

        self._send_json({'ok': False, 'error': 'Ruta DELETE no válida'}, status=404)



def run_server(port=PORT, host='0.0.0.0'):
    init_db()
    initialize_first_run()
    server = ThreadingHTTPServer((host, port), NoteJSRequestHandler)
    print(f"[Note JS] Servidor activo en http://{host}:{port} (Motor: SQLite + Peewee ORM -> {DB_PATH})", flush=True)
    server.serve_forever()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Note JS Server')
    parser.add_argument('--port', type=int, default=PORT, help='Port to bind')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind')
    args, _ = parser.parse_known_args()
    run_server(port=args.port, host=args.host)
