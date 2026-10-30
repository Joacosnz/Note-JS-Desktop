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
import webview

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
from backend import ThreadingHTTPServer, NoteJSRequestHandler


class PyWebViewBridge:
    """
    API nativa de Python expuesta directamente a JavaScript como `window.pywebview.api`.
    Permite que el frontend interactúe con SQLite + Peewee ORM sin latencia de red.
    """

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
    init_db()
    port = find_available_port(3000)
    url = f"http://127.0.0.1:{port}"

    # Iniciar servidor local de recursos y API en segundo plano
    t = threading.Thread(target=start_backend_thread, args=(port,), daemon=True)
    t.start()
    time.sleep(0.15)

    bridge = PyWebViewBridge()

    # Crear ventana nativa con PyWebView (sin Electron)
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
    )

    webview.start(debug=False)


if __name__ == '__main__':
    launch_pywebview_app()
