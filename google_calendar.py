"""Google Calendar integration. OAuth credentials live in memory, never in SQLite."""
import hashlib
import json
import secrets
import threading
import time
from datetime import date, datetime, timedelta
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from firebase_connection import SignInHandoff


class CalendarError(ValueError):
    pass


class CalendarHandoff(SignInHandoff):
    def complete(self, state, credential):
        token = (credential or {}).get('accessToken') if isinstance(credential, dict) else None
        if not isinstance(token, str) or not 10 <= len(token) <= 16000:
            raise CalendarError('Permiso de Calendar inválido.')
        with self.lock:
            self._expire()
            item = self.sessions.get(state)
            if not item or item['credential'] is not None:
                raise CalendarError('La conexión caducó. Volvé a conectar Calendar.')
            item['credential'] = {'accessToken': token}


def fingerprint(item):
    return json.dumps({k: item.get(k) for k in ('title', 'date', 'time', 'notes', 'completed', 'recurrence')}, sort_keys=True, ensure_ascii=False)


def event_body(item, timezone='UTC'):
    day = date.fromisoformat(item['date'])
    clock = item.get('time', '')
    if len(clock) == 5 and clock[2] == ':':
        start = datetime.fromisoformat(f'{day}T{clock}').astimezone()
        timing = {'start': {'dateTime': start.isoformat(), 'timeZone': timezone}, 'end': {'dateTime': (start + timedelta(hours=1)).isoformat(), 'timeZone': timezone}}
    else:
        timing = {'start': {'date': str(day)}, 'end': {'date': str(day + timedelta(days=1))}}
    rules = {'DAILY': 'FREQ=DAILY', 'WEEKDAYS': 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR', 'WEEKLY': 'FREQ=WEEKLY', 'MONTHLY': 'FREQ=MONTHLY', 'YEARLY': 'FREQ=YEARLY'}
    return {**timing, 'summary': ('✓ ' if item.get('completed') else '📌 ') + item['title'],
            'description': item.get('notes', ''), 'recurrence': ['RRULE:' + rules[item['recurrence']]] if item.get('recurrence') in rules else [],
            'reminders': {'useDefault': False, 'overrides': [] if item.get('completed') else [{'method': 'popup', 'minutes': 15}]}}


def local_event(event, local_id):
    start = event.get('start', {})
    stamp = start.get('dateTime')
    parsed = datetime.fromisoformat(stamp.replace('Z', '+00:00')).astimezone() if stamp else None
    title = event.get('summary') or 'Evento de Google Calendar'
    rules = {'FREQ=DAILY': 'DAILY', 'FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR': 'WEEKDAYS', 'FREQ=WEEKLY': 'WEEKLY', 'FREQ=MONTHLY': 'MONTHLY', 'FREQ=YEARLY': 'YEARLY'}
    recurrence = rules.get(next(iter(event.get('recurrence', [])), '').removeprefix('RRULE:'), 'NONE')
    return {'id': local_id, 'title': title.removeprefix('✓ ').removeprefix('📌 '), 'completed': title.startswith('✓ '),
            'date': str(parsed.date()) if parsed else start.get('date', ''), 'time': parsed.strftime('%H:%M') if parsed else 'Todo el día',
            'notes': event.get('description', ''), 'category': 'Google Calendar', 'recurrence': recurrence}


class GoogleCalendar:
    def __init__(self):
        self.handoff = CalendarHandoff()
        self.lock = threading.RLock()
        self.token = None
        self.email = ''
        self.expires = 0

    def request(self, method, path, body=None, etag=None, profile=False):
        if not self.token or time.monotonic() >= self.expires:
            raise CalendarError('Volvé a conectar Google Calendar para renovar el permiso.')
        url = 'https://www.googleapis.com/' + ('oauth2/v2/userinfo' if profile else 'calendar/v3/' + path)
        headers = {'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/json'}
        if etag:
            headers['If-Match'] = etag
        req = Request(url, data=json.dumps(body).encode() if body is not None else None, headers=headers, method=method)
        try:
            with urlopen(req, timeout=30) as response:
                data = response.read()
                return json.loads(data) if data else {}
        except HTTPError as exc:
            if exc.code == 401:
                self.token = None
            error = CalendarError({401: 'Volvé a conectar Calendar: el permiso caducó.', 403: 'Google no autorizó Calendar. Revisá el permiso y que Calendar API esté habilitada.', 412: 'El evento cambió durante la sincronización. Tus cambios se conservaron; sincronizá nuevamente.'}.get(exc.code, f'Google Calendar respondió con error {exc.code}.'))
            error.status = exc.code
            raise error from None
        except (URLError, TimeoutError, OSError):
            raise CalendarError('Sin conexión con Google Calendar. Tus recordatorios siguen guardados; se reintentará al recuperar la conexión.') from None

    def pages(self, path):
        items, token = [], None
        while True:
            data = self.request('GET', path + ('&' if '?' in path else '?') + urlencode({'pageToken': token} if token else {}))
            items.extend(data.get('items', []))
            token = data.get('nextPageToken')
            if not token:
                return items

    def calendars(self):
        return [{'id': c['id'], 'name': c.get('summary', c['id']), 'primary': c.get('primary', False), 'timeZone': c.get('timeZone', 'UTC')}
                for c in self.pages('users/me/calendarList?minAccessRole=writer') if not c.get('deleted')]

    def handle(self, action, body):
        with self.lock:
            if action == 'start':
                return {'ok': True, **self.handoff.start()}
            if action == 'complete':
                self.handoff.complete(body.get('state'), body.get('credential'))
            elif action == 'poll':
                return self.handoff.consume(body.get('state'), body.get('pollToken'))
            elif action == 'connect':
                token = body.get('accessToken')
                if not isinstance(token, str) or not 10 <= len(token) <= 16000:
                    raise CalendarError('Permiso inválido.')
                self.token, self.expires = token, time.monotonic() + 3300
                try:
                    profile = self.request('GET', '', profile=True)
                    self.email = profile.get('email', '')
                    if not self.email or not profile.get('verified_email'):
                        raise CalendarError('No se pudo verificar la cuenta de Google.')
                    return {'ok': True, 'email': self.email, 'calendars': self.calendars()}
                except Exception:
                    self.token, self.email = None, ''
                    raise
            elif action == 'disconnect':
                self.token, self.email, self.expires = None, '', 0
            elif action == 'status':
                return {'ok': True, 'connected': bool(self.token and time.monotonic() < self.expires), 'email': self.email}
            elif action == 'calendars':
                return {'ok': True, 'calendars': self.calendars(), 'email': self.email}
            elif action == 'sync':
                calendar = body.get('calendarId')
                selected = next((c for c in self.calendars() if c['id'] == calendar), None)
                if selected is None:
                    raise CalendarError('Elegí un calendario de tu cuenta con permiso de escritura.')
                return self.sync(calendar, selected['timeZone'])
            else:
                raise CalendarError('Acción de Calendar inválida.')
            return {'ok': True}

    def sync(self, calendar, timezone='UTC'):
        from models import DB_LOCK, Setting, get_reminders_orm, save_reminder_orm, delete_reminder_orm
        key = 'googleCalendar:' + hashlib.sha256((self.email + '\0' + calendar).encode()).hexdigest()
        with DB_LOCK:
            row = Setting.get_or_none(Setting.key == key)
            links = json.loads(row.value) if row else {}
        path = 'calendars/' + quote(calendar, safe='') + '/events'
        remote = {e['id']: e for e in self.pages(path + '?showDeleted=true&singleEvents=false&maxResults=2500')}
        local = {str(i['id']): i for i in get_reminders_orm()['reminders']}
        stats = {'imported': 0, 'exported': 0, 'deleted': 0, 'conflicts': 0, 'skipped': 0}

        def checkpoint():
            with DB_LOCK:
                Setting.insert(key=key, value=json.dumps(links)).on_conflict_replace().execute()

        def link(e, item):
            links[e['id']] = {'id': str(item['id']), 'local': fingerprint(item), 'etag': e.get('etag'), 'event': e}
            checkpoint()

        for event_id, entry in list(links.items()):
            e, item = remote.get(event_id), local.get(entry['id'])
            # Local editing can continue while Google responds. Re-read before merging.
            current = next((i for i in get_reminders_orm()['reminders'] if str(i['id']) == entry['id']), None)
            if (fingerprint(current) if current else None) != (fingerprint(item) if item else None):
                stats['conflicts'] += 1
                continue
            changed_local = item is not None and fingerprint(item) != entry['local']
            deleted_remote = e is None or e.get('status') == 'cancelled'
            changed_remote = not deleted_remote and e.get('etag') != entry['etag']
            if changed_local and changed_remote and fingerprint(local_event(e, item['id'])) == fingerprint(item):
                link(e, item)
                continue
            if (changed_local and (changed_remote or deleted_remote)) or (item is None and changed_remote):
                stats['conflicts'] += 1
                continue
            if deleted_remote:
                if item:
                    delete_reminder_orm(item['id'])
                    local.pop(entry['id'], None)
                del links[event_id]
                checkpoint()
                stats['deleted'] += 1
            elif item is None:
                try:
                    self.request('DELETE', path + '/' + quote(event_id, safe=''), etag=entry['etag'])
                except CalendarError as exc:
                    if getattr(exc, 'status', None) not in (404, 410):
                        raise
                del links[event_id]
                checkpoint()
                stats['deleted'] += 1
            elif changed_remote:
                saved = save_reminder_orm({**item, **local_event(e, item['id'])})['reminder']
                local[entry['id']] = saved
                link(e, saved)
                stats['imported'] += 1
            elif changed_local:
                # Patch only edited fields; retain remote duration, location, attendees and advanced recurrence.
                before = json.loads(entry['local'])
                patch = event_body(item, timezone)
                if item['date'] == before['date'] and item['time'] == before['time']:
                    patch.pop('start'); patch.pop('end')
                if item['recurrence'] == before['recurrence']:
                    patch.pop('recurrence')
                saved = self.request('PATCH', path + '/' + quote(event_id, safe=''), patch, entry['etag'])
                link(saved, item)
                stats['exported'] += 1

        linked_ids = {v['id'] for v in links.values()}
        for event_id, e in remote.items():
            if event_id in links or e.get('status') == 'cancelled' or not e.get('start'):
                continue
            new_id = secrets.randbelow(8_000_000_000_000_000) + 1_000_000_000_000_000
            # Deterministic exported IDs recover a successful insert after a lost response.
            own = e.get('extendedProperties', {}).get('private', {})
            if own.get('notejsDesktopOwner') == key:
                new_id = int(own['notejsDesktopId'])
                if str(new_id) in local:
                    if fingerprint(local_event(e, new_id)) != fingerprint(local[str(new_id)]):
                        stats['conflicts'] += 1
                        linked_ids.add(str(new_id))
                        continue
                    link(e, local[str(new_id)])
                    continue
            saved = save_reminder_orm(local_event(e, new_id))['reminder']
            local[str(new_id)] = saved
            link(e, saved)
            linked_ids.add(str(new_id))
            stats['imported'] += 1
        for rid, item in list(local.items()):
            if rid in linked_ids or any(v['id'] == rid for v in links.values()):
                continue
            if not item.get('date'):
                stats['skipped'] += 1
                continue
            payload = event_body(item, timezone)
            payload['id'] = hashlib.sha256((key + ':' + rid).encode()).hexdigest()
            payload['extendedProperties'] = {'private': {'notejsDesktopOwner': key, 'notejsDesktopId': rid}}
            try:
                e = self.request('POST', path, payload)
            except CalendarError as exc:
                if getattr(exc, 'status', None) != 409:
                    raise
                e = self.request('GET', path + '/' + payload['id'])
            link(e, item)
            stats['exported'] += 1
        return {'ok': True, **stats, 'reminders': get_reminders_orm()['reminders'], 'syncedAt': int(time.time() * 1000)}


GOOGLE_CALENDAR = GoogleCalendar()
