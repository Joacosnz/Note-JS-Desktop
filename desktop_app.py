#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Note JS — Aplicación Nativa de Escritorio con PyWebView y SQLite + Peewee ORM
Reemplaza completamente a Electron usando el motor nativo del sistema (WebView2 en Windows,
WebKitGTK en Linux, WKWebView en macOS) junto con el puente directo window.pywebview.api.
"""

import os
import sys
import time
import socket
import threading
import base64
import webbrowser
from urllib.parse import urlencode
import webview
from pdf_documents import MAX_PDF_BYTES, store_pdf
from onboarding import initialize_first_run

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

from models import (
    DATA_DIR,
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
    apply_transaction,
)
from backend import (
    ThreadingHTTPServer,
    NoteJSRequestHandler,
    create_block_api,
    get_block_api,
    get_record_map_api,
    update_block_api,
    reorder_block_children_api,
    soft_delete_block_api,
    restore_block_api,
    convert_rich_text_api,
    apply_transactions_api,
)


class PyWebViewBridge:
    """
    API nativa de Python expuesta directamente a JavaScript como `window.pywebview.api`.
    Permite que el frontend interactúe con SQLite + Peewee ORM sin latencia de red.
    """

    def open_project_link(self, url):
        links = {
            'https://ko-fi.com/yubelljs',
            'https://github.com/Joacosnz/Note-JS-Desktop',
            'https://github.com/Joacosnz/Note-JS-movile',
        }
        if not isinstance(url, str) or url not in links:
            return {'ok': False, 'error': 'Enlace del proyecto inválido.'}
        return {'ok': bool(webbrowser.open(url))}

    def open_microsoft_signin(self):
        from urllib.parse import urlsplit
        if not webview.windows:
            return {'ok': False, 'error': 'No hay una ventana activa.'}
        current = urlsplit(webview.windows[0].get_current_url())
        if current.scheme != 'http' or current.hostname not in ('127.0.0.1', 'localhost'):
            return {'ok': False, 'error': 'Origen de la aplicación inválido.'}
        existing = getattr(self, '_microsoft_window', None)
        if existing is not None and existing in webview.windows:
            existing.show()
            return {'ok': True}
        # No js_api: provider/federated pages cannot call local note/file APIs.
        # All windows use the shared storage_path configured by webview.start.
        self._microsoft_window = webview.create_window(
            title='Conectar con Microsoft · Note JS',
            url=f'{current.scheme}://{current.netloc}/microsoft-signin.html',
            width=580, height=760, min_size=(420, 560), frameless=False
        )
        return {'ok': True}

    def open_firebase_signin(self, state):
        from urllib.parse import urlsplit
        from firebase_connection import SIGN_IN_HANDOFF
        if not isinstance(state, str) or state not in SIGN_IN_HANDOFF.sessions or not webview.windows:
            return {'ok': False, 'error': 'Sesión inválida.'}
        current = urlsplit(webview.windows[0].get_current_url())
        url = f'{current.scheme}://{current.netloc}/firebase-signin.html?' + urlencode({'state': state})
        return {'ok': bool(webbrowser.open(url))}

    def open_google_calendar(self, state):
        from urllib.parse import urlsplit
        from google_calendar import GOOGLE_CALENDAR
        if not isinstance(state, str) or state not in GOOGLE_CALENDAR.handoff.sessions or not webview.windows:
            return {'ok': False, 'error': 'Conexión inválida.'}
        current = urlsplit(webview.windows[0].get_current_url())
        if current.scheme != 'http' or current.hostname not in ('127.0.0.1', 'localhost'):
            return {'ok': False, 'error': 'Origen inválido.'}
        url = f'http://{current.netloc}/google-calendar-connect.html?' + urlencode({'state': state})
        return {'ok': bool(webbrowser.open(url))}

    def save_pdf_copy(self, data_url, name='Documento.pdf'):
        """Save an explicit copy through the native dialog, never overwrite the source silently."""
        try:
            prefix = 'data:application/pdf;base64,'
            if not isinstance(data_url, str) or not data_url.startswith(prefix):
                raise ValueError('Datos PDF inválidos.')
            if len(data_url) > (MAX_PDF_BYTES * 4 // 3) + 100:
                raise ValueError('El límite por PDF es de 50 MB.')
            data = base64.b64decode(data_url[len(prefix):], validate=True)
            if not data.startswith(b'%PDF-'):
                raise ValueError('Datos PDF inválidos.')
            filename = os.path.basename(str(name).replace('\\', '/'))
            selected = webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG, save_filename=filename,
                file_types=('Documentos PDF (*.pdf)',))
            if not selected:
                return {'ok': False, 'cancelled': True}
            destination = selected[0] if isinstance(selected, (tuple, list)) else str(selected)
            if not destination.lower().endswith('.pdf'):
                destination += '.pdf'
            with open(destination, 'wb') as stream:
                stream.write(data)
            return {'ok': True}
        except Exception as exc:
            return {'ok': False, 'error': str(exc)}

    # -------------------------------------------------------------------------
    # Métodos de Bloques Estilo Notion (Milestone 2)
    # -------------------------------------------------------------------------

    def apply_transaction(self, operations):
        """
        Ejecuta atómicamente un lote de operaciones Notion (op.set, op.listAfter)
        con rollback completo ante fallos.
        """
        if isinstance(operations, dict) and 'operations' in operations:
            payload = operations
        elif isinstance(operations, list):
            payload = {'operations': operations}
        else:
            payload = operations
        res, _ = apply_transactions_api(payload)
        return res

    def create_block(self, block_dict, target_index=None, after_id=None, before_id=None):
        res, _ = create_block_api(block_dict, target_index=target_index, after_id=after_id, before_id=before_id)
        return res

    def get_block(self, block_id, resolve_tree=False):
        res, _ = get_block_api(block_id, resolve_tree=resolve_tree)
        return res

    def get_record_map(self, root_id):
        res, _ = get_record_map_api(root_id)
        return res

    def get_block_record_map(self, root_id, include_trashed=False):
        res, _ = get_record_map_api(root_id, include_trashed=include_trashed)
        return res

    def update_block(self, block_id, updates, expected_version=None):
        res, _ = update_block_api(block_id, updates, expected_version=expected_version)
        return res

    def reorder_block_children(self, parent_id, content_array):
        res, _ = reorder_block_children_api(parent_id, content_array)
        return res

    def soft_delete_block(self, block_id):
        res, _ = soft_delete_block_api(block_id, permanent=False)
        return res

    def delete_block(self, block_id, permanent=False):
        res, _ = soft_delete_block_api(block_id, permanent=permanent)
        return res

    def restore_block(self, block_id):
        res, _ = restore_block_api(block_id)
        return res

    def convert_rich_text(self, payload):
        res, _ = convert_rich_text_api(payload)
        return res


    def bootstrap(self):
        return get_bootstrap_data()

    def save_note(self, note_obj, summary=None, force_history=False):
        return save_single_note(note_obj, summary=summary, force_history=force_history)

    def delete_note(self, note_id):
        return delete_single_note(note_id)

    def get_note_history(self, note_id):
        return get_note_history_list(note_id)

    def create_note_snapshot(self, note_obj, summary='Punto de restauración manual'):
        return create_manual_note_snapshot(note_obj, summary=summary)

    def revert_note_version(self, note_id, version_id):
        return revert_note_to_version(note_id, version_id)

    def delete_note_version(self, note_id, version_id):
        return delete_note_history_version(note_id, version_id)

    def resolve_local_image(self, path_str):
        return resolve_local_image_path(path_str)

    def pick_local_image(self):
        try:
            if webview.windows:
                file_types = ('Imágenes (*.png;*.jpg;*.jpeg;*.gif;*.webp;*.svg;*.bmp)', 'Todos los archivos (*.*)')
                selected = webview.windows[0].create_file_dialog(
                    webview.OPEN_DIALOG,
                    allow_multiple=False,
                    file_types=file_types,
                )
                if selected and len(selected) > 0:
                    chosen_path = selected[0] if isinstance(selected, (list, tuple)) else str(selected)
                    return resolve_local_image_path(chosen_path)
            return {'ok': False, 'cancelled': True}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def sync_all(self, payload):
        return sync_all_data(payload)

    def save_folders(self, folders_payload, folder_emojis=None):
        return save_folders_list(folders_payload, folder_emojis)

    def move_folder_hierarchy(self, source_folder, target_parent_folder='', folders_list=None, folder_emojis=None, notes_list=None):
        return move_folder_hierarchy_orm(
            source_folder,
            target_parent_folder=target_parent_folder,
            folders_list=folders_list,
            folder_emojis=folder_emojis,
            notes_list=notes_list,
        )

    def set_folder_emoji(self, folder_name, emoji):
        return update_folder_emoji_orm(folder_name, emoji)

    def save_settings(self, settings_dict):
        return save_settings_dict(settings_dict)

    def get_note_blocks(self, note_id):
        return get_note_blocks_orm(note_id)

    def update_block_order(self, block_id, prev_id=None, next_id=None, parent_id=None, note_id=None):
        return update_block_order_orm(block_id, prev_id=prev_id, next_id=next_id, parent_id=parent_id, note_id=note_id)

    def update_batch_blocks_order(self, moves):
        return update_batch_blocks_order_orm(moves)

    def sync_note_blocks(self, note_id, blocks_data):
        return sync_blocks_from_note_html_orm(note_id, blocks_data)

    def query_smart_folder(self, folder_name=None, rules=None, match_mode='all'):
        return query_smart_folder_orm(folder_name=folder_name, rules=rules, match_mode=match_mode)

    def save_smart_folder(self, name, rules, match_mode='all', emoji='⚙️', old_name=None):
        return save_smart_folder_orm(name, rules, match_mode=match_mode, emoji=emoji, old_name=old_name)

    def delete_smart_folder(self, name):
        return delete_smart_folder_orm(name)

    def get_reminders(self):
        return get_reminders_orm()

    def save_reminder(self, reminder_dict):
        return save_reminder_orm(reminder_dict)

    def delete_reminder(self, reminder_id):
        return delete_reminder_orm(reminder_id)

    def sync_reminders(self, reminders_list):
        return sync_reminders_orm(reminders_list)

    def fetch_weblink_metadata(self, url):
        return fetch_weblink_metadata_orm(url)

    def save_signature(self, note_id=None, points_json='[]', image_data=''):
        return save_signature_orm(note_id=note_id, points_json=points_json, image_data=image_data)

    def get_signatures(self, note_id=None):
        return get_signatures_orm(note_id=note_id)

    def minimize_window(self):
        try:
            if webview.windows:
                webview.windows[0].minimize()
                return {'ok': True, 'action': 'minimize'}
            return {'ok': False, 'error': 'No active window'}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def toggle_maximize_window(self):
        try:
            if webview.windows:
                win = webview.windows[0]
                if getattr(win, '_is_maximized', False):
                    win.restore()
                    win._is_maximized = False
                    return {'ok': True, 'action': 'restore', 'is_maximized': False}
                else:
                    win.maximize()
                    win._is_maximized = True
                    return {'ok': True, 'action': 'maximize', 'is_maximized': True}
            return {'ok': False, 'error': 'No active window'}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def close_window(self):
        try:
            if webview.windows:
                webview.windows[0].destroy()
                return {'ok': True, 'action': 'close'}
            return {'ok': False, 'error': 'No active window'}
        except Exception as e:
            return {'ok': False, 'error': str(e)}


def find_available_port(preferred=3000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', preferred)) != 0:
            return preferred
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def start_backend_thread(port):
    init_db()
    server = ThreadingHTTPServer(('127.0.0.1', port), NoteJSRequestHandler)
    server.serve_forever()


def launch_pywebview_app():
    # Configurar AppUserModelID para icono en barra de tareas de Windows 11
    if sys.platform == 'win32':
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('NoteJS.Desktop.App.v2')
        except Exception:
            pass

    init_db()
    initialize_first_run()
    port = find_available_port(3000)
    url = f"http://127.0.0.1:{port}"

    # Explorer / Open With passes the selected PDF as a command-line argument.
    pdf_argument = next((arg for arg in sys.argv[1:] if arg.lower().endswith('.pdf') and os.path.isfile(arg)), None)
    if pdf_argument:
        try:
            if os.path.getsize(pdf_argument) > MAX_PDF_BYTES:
                raise ValueError('El límite por PDF es de 50 MB.')
            with open(pdf_argument, 'rb') as stream:
                result = store_pdf(stream.read(MAX_PDF_BYTES + 1), os.path.join(DATA_DIR, 'attachments', 'pdfs'), os.path.basename(pdf_argument))
            url += '/?' + urlencode({'pdf': result['url'], 'pdfName': result['name']})
        except (OSError, ValueError) as exc:
            url += '/?' + urlencode({'pdfError': str(exc)})

    # Iniciar servidor local de recursos y API en segundo plano
    t = threading.Thread(target=start_backend_thread, args=(port,), daemon=True)
    t.start()
    time.sleep(0.15)

    bridge = PyWebViewBridge()

    # Detectar icono de aplicación
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_file = os.path.join(base_dir, 'public', 'icon.ico')
    if not os.path.exists(icon_file):
        icon_file = os.path.join(base_dir, 'icon.ico')

    # Crear ventana nativa con PyWebView (sin Electron, frameless para barra integrada única)
    window = webview.create_window(
        title='Note JS — PC Desktop (PyWebView + SQLite & Peewee ORM)',
        url=url,
        js_api=bridge,
        width=1360,
        height=860,
        min_size=(940, 620),
        background_color='#0f1115',
        text_select=True,
        confirm_close=False,
        frameless=True,
        easy_drag=False,
    )

    if sys.platform == 'win32':
        def on_window_shown():
            try:
                import ctypes
                hwnd = window.native.Handle.ToInt32() if hasattr(window, 'native') and window.native else None
                if hwnd:
                    GWL_STYLE = -16
                    WS_THICKFRAME = 0x00040000
                    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
                    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style | WS_THICKFRAME)
            except Exception:
                pass
        window.events.shown += on_window_shown

    webview.start(debug=False, icon=icon_file if os.path.exists(icon_file) else None,
                  private_mode=False, storage_path=os.path.join(DATA_DIR, 'webview'))


if __name__ == '__main__':
    launch_pywebview_app()
