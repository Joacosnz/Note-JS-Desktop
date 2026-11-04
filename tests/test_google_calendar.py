import copy
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import models
from google_calendar import CalendarError, CalendarHandoff, GoogleCalendar, event_body


class FakeCalendar(GoogleCalendar):
    def __init__(self):
        super().__init__()
        self.email = 'owner@example.com'
        self.events = {}
        self.offline = False
        self.lose_insert_response = False
        self.calls = []

    def request(self, method, path, body=None, etag=None, profile=False):
        if self.offline:
            raise CalendarError('Sin conexión')
        self.calls.append((method, path, copy.deepcopy(body)))
        key = path.split('/')[-1].split('?')[0]
        if method == 'GET' and '/events?' in path:
            return {'items': copy.deepcopy(list(self.events.values()))}
        if method == 'GET':
            return copy.deepcopy(self.events[key])
        if method == 'POST':
            key = body['id']
            if key in self.events:
                error = CalendarError('Already exists'); error.status = 409; raise error
            self.events[key] = {**copy.deepcopy(body), 'etag': 'v1'}
            if self.lose_insert_response:
                self.lose_insert_response = False
                raise CalendarError('Lost response')
        elif method == 'PATCH':
            if etag != self.events[key]['etag']:
                error = CalendarError('Changed'); error.status = 412; raise error
            self.events[key].update(copy.deepcopy(body))
            self.events[key]['etag'] += 'x'
        elif method == 'DELETE':
            self.events[key]['status'] = 'cancelled'
            return {}
        return copy.deepcopy(self.events[key])


class CalendarSyncTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous = models.db.database
        if not models.db.is_closed(): models.db.close()
        models.db.init(str(Path(self.temp.name) / 'test.db'))
        models.init_db()
        self.calendar = FakeCalendar()

    def tearDown(self):
        models.db.close(); models.db.init(self.previous); self.temp.cleanup()

    def local(self, **changes):
        return models.save_reminder_orm({'id': 123, 'title': 'Reunión', 'date': '2026-11-05', 'time': '10:00', 'priority': 3, **changes})['reminder']

    def remote(self):
        return next(iter(self.calendar.events.values()))

    def test_repeated_sync_does_not_duplicate_or_rewrite_events(self):
        self.local(); self.calendar.sync('primary')
        self.assertEqual(self.calendar.sync('primary')['exported'], 0)
        self.assertEqual(len(self.calendar.events), 1)
        self.assertEqual(len(models.get_reminders_orm()['reminders']), 1)

    def test_google_edit_is_imported_without_losing_local_priority(self):
        self.local(); self.calendar.sync('primary')
        self.remote().update(summary='Cambio desde Google', etag='v2', location='Oficina')
        self.calendar.sync('primary')
        item = models.get_reminders_orm()['reminders'][0]
        self.assertEqual(item['title'], 'Cambio desde Google')
        self.assertEqual(item['priority'], 3)

    def test_local_title_edit_keeps_remote_duration_and_attendees(self):
        self.local(); self.calendar.sync('primary')
        self.remote().update(end={'dateTime': '2026-11-05T14:00:00+00:00'}, attendees=[{'email': 'guest@example.com'}])
        self.local(title='Nuevo título'); self.calendar.sync('primary')
        self.assertEqual(self.remote()['end']['dateTime'], '2026-11-05T14:00:00+00:00')
        self.assertEqual(len(self.remote()['attendees']), 1)

    def test_concurrent_edits_are_preserved_and_can_converge(self):
        self.local(); self.calendar.sync('primary')
        self.local(title='Edición local'); self.remote().update(summary='Edición remota', etag='v2')
        self.assertEqual(self.calendar.sync('primary')['conflicts'], 1)
        self.assertEqual(models.get_reminders_orm()['reminders'][0]['title'], 'Edición local')
        self.assertEqual(self.remote()['summary'], 'Edición remota')
        self.remote().update(summary='📌 Edición local', etag='v3')
        self.assertEqual(self.calendar.sync('primary')['conflicts'], 0)

    def test_remote_delete_is_not_recreated(self):
        self.local(); self.calendar.sync('primary')
        self.remote()['status'] = 'cancelled'
        self.calendar.sync('primary'); self.calendar.sync('primary')
        self.assertEqual(models.get_reminders_orm()['reminders'], [])
        self.assertEqual(len(self.calendar.events), 1)

    def test_local_delete_removes_only_the_linked_google_event(self):
        self.local(); self.calendar.sync('primary')
        models.delete_reminder_orm(123); self.calendar.sync('primary')
        self.assertEqual(self.remote()['status'], 'cancelled')

    def test_offline_preserves_local_pending_edits(self):
        self.local(); self.calendar.sync('primary'); self.local(title='Pendiente')
        self.calendar.offline = True
        with self.assertRaises(CalendarError): self.calendar.sync('primary')
        self.assertEqual(models.get_reminders_orm()['reminders'][0]['title'], 'Pendiente')
        self.calendar.offline = False; self.calendar.sync('primary')
        self.assertEqual(self.remote()['summary'], '📌 Pendiente')

    def test_lost_insert_response_is_recovered_without_duplicate(self):
        self.local(); self.calendar.lose_insert_response = True
        with self.assertRaises(CalendarError): self.calendar.sync('primary')
        self.calendar.sync('primary')
        self.assertEqual(len(self.calendar.events), 1)
        self.assertEqual(len(models.get_reminders_orm()['reminders']), 1)

    def test_import_new_google_event_only_once(self):
        self.calendar.events['abc'] = {'id': 'abc', 'etag': 'v1', 'summary': 'Cena', 'start': {'date': '2026-11-10'}, 'end': {'date': '2026-11-11'}}
        self.assertEqual(self.calendar.sync('primary')['imported'], 1)
        self.assertEqual(self.calendar.sync('primary')['imported'], 0)
        self.assertEqual(models.get_reminders_orm()['reminders'][0]['title'], 'Cena')

    def test_lost_response_followed_by_google_edit_preserves_both_versions(self):
        self.local(); self.calendar.lose_insert_response = True
        with self.assertRaises(CalendarError): self.calendar.sync('primary')
        self.remote().update(summary='Cambio después de perder la respuesta', etag='v2')
        self.assertEqual(self.calendar.sync('primary')['conflicts'], 1)
        self.assertEqual(len(self.calendar.events), 1)
        self.assertEqual(models.get_reminders_orm()['reminders'][0]['title'], 'Reunión')

    def test_missing_date_is_not_exported_as_today(self):
        self.local(date='')
        self.assertEqual(self.calendar.sync('primary')['skipped'], 1)
        self.assertEqual(self.calendar.events, {})

    def test_map_contains_no_oauth_credentials(self):
        self.local(); self.calendar.token = 'private-oauth-token'; self.calendar.sync('primary')
        self.assertNotIn('private-oauth-token', ''.join(s.value for s in models.Setting.select()))


class CalendarProtocolTest(unittest.TestCase):
    def test_all_day_end_is_exclusive_including_leap_day(self):
        data = event_body({'date': '2028-02-29', 'title': 'Viaje'})
        self.assertEqual(data['end'], {'date': '2028-03-01'})

    def test_recurrence_includes_an_explicit_timezone(self):
        data = event_body({'date': '2026-11-05', 'time': '10:00', 'title': 'Clase', 'recurrence': 'WEEKLY'}, 'America/Argentina/Buenos_Aires')
        self.assertEqual(data['start']['timeZone'], 'America/Argentina/Buenos_Aires')
        self.assertEqual(data['recurrence'], ['RRULE:FREQ=WEEKLY'])

    def test_grant_requires_private_poll_token_and_is_consumed_once(self):
        h = CalendarHandoff(); session = h.start()
        h.complete(session['state'], {'accessToken': 'test-access-token'})
        with self.assertRaises(ValueError): h.consume(session['state'], 'wrong')
        self.assertEqual(h.consume(session['state'], session['pollToken'])['credential']['accessToken'], 'test-access-token')
        with self.assertRaises(ValueError): h.consume(session['state'], session['pollToken'])

    def test_pagination_reads_every_page_before_returning(self):
        service = GoogleCalendar()
        with patch.object(service, 'request', side_effect=[{'items': [{'id': 'a'}], 'nextPageToken': 'page2'}, {'items': [{'id': 'b'}]}]) as request:
            self.assertEqual(len(service.pages('events?showDeleted=true')), 2)
            self.assertIn('pageToken=page2', request.call_args.args[1])

    def test_expired_access_requires_reconnection_without_sending_request(self):
        service = GoogleCalendar(); service.token = 'expired'; service.expires = time.monotonic() - 1
        with patch('google_calendar.urlopen') as network:
            with self.assertRaises(CalendarError): service.request('GET', 'calendars')
            network.assert_not_called()
