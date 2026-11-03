"""Run the real app against isolated local data without external accounts."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import models
import backend

root = sys.argv[1]
models.DATA_DIR = backend.DATA_DIR = root
models.DB_PATH = os.path.join(root, 'test.db')
models.db.init(models.DB_PATH)
models.init_db()
if '--welcome' in sys.argv:
    from onboarding import initialize_first_run
    initialize_first_run()


class Handler(backend.NoteJSRequestHandler):
    def do_GET(self):
        if self.path == '/api/firebase/config':
            self._send_json({'configured': False})
        else:
            super().do_GET()


server = backend.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
print(server.server_port, flush=True)
server.serve_forever()
