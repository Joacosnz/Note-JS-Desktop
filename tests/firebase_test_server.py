"""Serve the actual desktop UI against isolated SQLite and Firebase emulators."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import models
import backend

root = sys.argv[1]
models.DATA_DIR = backend.DATA_DIR = root
models.DB_PATH = os.path.join(root,'test.db')
models.db.init(models.DB_PATH)
models.init_db()
configuration = {
    'configured':True,'firebase':{'projectId':'demo-notejs-desktop','apiKey':'demo-key','appId':'1:123:web:desktop','authDomain':'localhost'},
    'databaseId':'desktop-test','databaseEdition':'ENTERPRISE','storageAvailable':False,
    'emulators':{'host':'127.0.0.1','auth':'http://127.0.0.1:19099','firestorePort':18085,'storagePort':19199}
}


class Handler(backend.NoteJSRequestHandler):
    def do_GET(self):
        if self.path == '/api/firebase/config':
            self._send_json(configuration)
        else:
            super().do_GET()


server = backend.ThreadingHTTPServer(('127.0.0.1',0),Handler)
print(server.server_port,flush=True)
server.serve_forever()
