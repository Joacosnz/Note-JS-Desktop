"""First-run welcome content; never cleans or replaces an existing library."""
import html
import json
import time
from pathlib import Path

WELCOME_SETTING = 'welcomeInitializedV1'


def welcome_notes(now=None):
    catalog = json.loads(Path(__file__).with_name('welcome_notes.json').read_text(encoding='utf-8'))
    now = int(time.time() * 1000) if now is None else now
    notes = []
    for index, item in enumerate(catalog['notes']):
        parts = []
        for section in item['sections']:
            parts.append('<h2>' + html.escape(section['heading']) + '</h2>')
            body = section.get('desktopBody', section.get('body', ''))
            if body:
                parts.append('<p>' + html.escape(body) + '</p>')
            if section.get('tasks'):
                parts.append('<ul>' + ''.join('<li>' + html.escape(task) + '</li>' for task in section['tasks']) + '</ul>')
        notes.append({
            'id': index + 1, 'title': item['title'], 'emoji': item['icon'],
            'content': ''.join(parts), 'folder': catalog['folder'],
            'folders': [catalog['folder']], 'hasCover': False, 'coverStyle': '',
            'isPinned': index == 0, 'isTrashed': False, 'isArchived': False,
            'tags': '', 'updatedAt': now - index, 'onboardingKey': item['key'],
        })
    return notes


def initialize_first_run():
    import models
    with models.DB_LOCK, models.db.atomic():
        if models.Setting.get_or_none(models.Setting.key == WELCOME_SETTING):
            return False
        # Existing settings/notes/reminders mean an existing installation or restored data.
        fresh = not (models.Note.select().exists() or models.Setting.select().exists() or models.ReminderItem.select().exists())
        if fresh:
            notes = welcome_notes()
            for note in notes:
                models.upsert_note_orm(note, record_history=False)
            models.Folder.insert(name=notes[0]['folder'], emoji='👋', sort_order=0).on_conflict_ignore().execute()
            models.migrate_legacy_notes_to_blocks()
        models.Setting.insert(key=WELCOME_SETTING, value='1').on_conflict_ignore().execute()
        return fresh
