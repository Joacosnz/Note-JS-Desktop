"""Public Firebase configuration and short-lived browser sign-in handoff.

No service account or Firebase session is stored by the Python server.
"""
import json
import secrets
import threading
import time
from pathlib import Path


def load_firebase_config(base_dir):
    path = Path(base_dir) / 'frontend' / 'firebase-config.json'
    if not path.is_file():
        return {'configured': False}
    config = json.loads(path.read_text(encoding='utf-8'))
    return config


class SignInHandoff:
    def __init__(self, ttl=300):
        self.ttl = ttl
        self.sessions = {}
        self.lock = threading.Lock()

    def _expire(self):
        now = time.monotonic()
        self.sessions = {key: value for key, value in self.sessions.items() if value['expires'] > now}

    def start(self):
        with self.lock:
            self._expire()
            if len(self.sessions) >= 10:
                raise ValueError('Ya hay demasiados inicios de sesión pendientes.')
            state, token = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
            self.sessions[state] = {'token': token, 'expires': time.monotonic() + self.ttl, 'credential': None}
            return {'state': state, 'pollToken': token}

    def complete(self, state, credential):
        if not isinstance(credential, dict) or credential.get('providerId') != 'google.com' or not isinstance(credential.get('idToken'), str) or len(credential['idToken']) > 16000:
            raise ValueError('Credencial de Google inválida.')
        with self.lock:
            self._expire()
            session = self.sessions.get(state)
            if not session or session['credential'] is not None:
                raise ValueError('La sesión caducó o ya se utilizó. Inicia sesión de nuevo.')
            session['credential'] = {'idToken': credential['idToken'], 'providerId': 'google.com'}

    def consume(self, state, token):
        with self.lock:
            self._expire()
            session = self.sessions.get(state)
            if not session or not secrets.compare_digest(session['token'], str(token)):
                raise ValueError('La sesión caducó o no es válida.')
            credential = session['credential']
            if credential:
                del self.sessions[state]
            return {'ok': True, 'credential': credential}


SIGN_IN_HANDOFF = SignInHandoff()
