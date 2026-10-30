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
import zipfile
from urllib.parse import urlparse, unquote
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from models import (
    DB_PATH,
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
        ]
        for arcname, fpath in files_to_pack:
            if os.path.exists(fpath):
                zf.write(fpath, arcname=f"NoteJS-Python-PyWebView/{arcname}")

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


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class NoteJSRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _send_json(self, data, status=200):
        payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
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

        # Healthcheck endpoint
        if path == '/health':
            self._send_json({'status': 'healthy', 'ok': True, 'port': PORT})
            return

        # 1. API: Obtener estado completo desde SQLite + Peewee ORM
        if path == '/api/bootstrap':
            self._send_json(get_bootstrap_data())
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
            from urllib.parse import parse_qs
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
            from urllib.parse import parse_qs
            qs = parse_qs(parsed.query)
            target_url = qs.get('url', [''])[0]
            self._send_json(fetch_weblink_metadata_orm(target_url))
            return

        # 1g. API: Obtener firmas manuscritas
        if path == '/api/signatures':
            from urllib.parse import parse_qs
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
                '.json': 'application/json; charset=utf-8',
                '.png': 'image/png',
                '.svg': 'image/svg+xml',
                '.ico': 'image/x-icon'
            }
            ctype = mime_map.get(ext, 'application/octet-stream')
            with open(target_file, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-cache')
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

        try:
            body = self._read_json_body()
        except Exception as e:
            self._send_json({'ok': False, 'error': str(e)}, status=400)
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

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

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
