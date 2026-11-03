"""Persistent, content-addressed PDF attachments (independent of the notes database)."""
import hashlib
import os
import re
import tempfile
from pathlib import Path

MAX_PDF_BYTES = 50 * 1024 * 1024


def store_pdf(data, directory, name='Documento.pdf'):
    if not data or len(data) > MAX_PDF_BYTES:
        raise ValueError('El PDF debe tener entre 1 byte y 50 MB.')
    if not data.startswith(b'%PDF-'):
        raise ValueError('El archivo seleccionado no es un PDF válido.')
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(data).hexdigest()
    destination = root / (digest + '.pdf')
    if not destination.exists():
        fd, temporary = tempfile.mkstemp(dir=root, suffix='.tmp')
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
            os.replace(temporary, destination)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    title = str(name).replace('\\', '/').rsplit('/', 1)[-1][:200]
    return {'ok': True, 'url': '/api/pdfs/' + digest + '.pdf',
            'name': title or 'Documento.pdf', 'size': len(data)}


def resolve_pdf(filename, directory):
    if not re.fullmatch(r'[a-f0-9]{64}\.pdf', filename):
        raise ValueError('Identificador de PDF inválido.')
    path = Path(directory) / filename
    if not path.is_file():
        raise FileNotFoundError('El PDF ya no está disponible.')
    return path
