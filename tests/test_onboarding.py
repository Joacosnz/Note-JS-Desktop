import tempfile
import unittest
from pathlib import Path
import models
from onboarding import initialize_first_run, welcome_notes, WELCOME_SETTING


class FirstRunWelcomeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous = models.db.database
        if not models.db.is_closed(): models.db.close()
        models.db.init(str(Path(self.temp.name) / 'fresh.db'))
        models.init_db()

    def tearDown(self):
        models.db.close()
        models.db.init(self.previous)
        self.temp.cleanup()

    def test_fresh_library_contains_only_three_welcome_notes_and_no_reminders(self):
        self.assertTrue(initialize_first_run())
        notes = list(models.Note.select())
        self.assertEqual({n.title for n in notes}, {'Bienvenido a Note JS','Tu primera nota','Organizá tu espacio'})
        self.assertEqual(models.ReminderItem.select().count(), 0)
        self.assertTrue(all(not n.to_dict()['hasCover'] for n in notes))
        self.assertEqual(models.Folder.select().count(), 1)
        self.assertTrue(models.Block.select().count() > 3)
        self.assertFalse(initialize_first_run())
        self.assertEqual(models.Note.select().count(), 3)

    def test_deleting_all_guides_does_not_recreate_them(self):
        initialize_first_run()
        models.Note.delete().execute()
        self.assertFalse(initialize_first_run())
        self.assertEqual(models.Note.select().count(), 0)
        self.assertIsNotNone(models.Setting.get_or_none(models.Setting.key == WELCOME_SETTING))

    def test_existing_libraries_are_not_modified(self):
        models.upsert_note_orm({'id':42,'title':'Mi nota personal','content':'Conservar este texto'})
        self.assertFalse(initialize_first_run())
        self.assertEqual(models.Note.select().count(), 1)
        self.assertEqual(models.Note.get_by_id(42).content, 'Conservar este texto')

    def test_existing_empty_installations_with_settings_stay_empty(self):
        models.Setting.create(key='themeMode', value='light')
        self.assertFalse(initialize_first_run())
        self.assertEqual(models.Note.select().count(), 0)

    def test_guides_are_short_editable_content_without_fake_covers(self):
        notes = welcome_notes(now=1000)
        self.assertEqual([n['id'] for n in notes], [1,2,3])
        self.assertTrue(all(n['folder']=='Primeros pasos' and not n['hasCover'] for n in notes))
        self.assertIn('Ctrl + N', notes[1]['content'])
        self.assertNotIn('SQLite', ''.join(n['content'] for n in notes))
