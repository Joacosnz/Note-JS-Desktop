"""Durable local cover photos, referenced by a content hash rather than an OS path."""
import hashlib
import os
import re
import tempfile
from pathlib import Path

MAX_COVER_BYTES = 20 * 1024 * 1024


def store_cover(data, directory):
    if not data or len(data) > MAX_COVER_BYTES:
        raise ValueError('La foto debe tener entre 1 byte y 20 MB.')
    # The browser decodes and normalizes gallery images to JPEG before upload.
    if not data.startswith(b'\xff\xd8\xff') or not data.endswith(b'\xff\xd9'):
        raise ValueError('La portada debe ser una foto JPEG válida.')
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    filename = hashlib.sha256(data).hexdigest() + '.jpg'
    destination = root / filename
    if not destination.exists():
        fd, temporary = tempfile.mkstemp(dir=root, suffix='.tmp')
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
            os.replace(temporary, destination)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    return {'ok': True, 'url': '/api/covers/' + filename, 'size': len(data)}


def resolve_cover(filename, directory):
    if not re.fullmatch(r'[a-f0-9]{64}\.jpg', filename):
        raise ValueError('Identificador de portada inválido.')
    path = Path(directory) / filename
    if not path.is_file():
        raise FileNotFoundError('La foto de portada ya no está disponible.')
    return path
