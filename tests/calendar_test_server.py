import os,sys,time
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import models,backend,google_calendar
from tests.test_google_calendar import FakeCalendar
root=sys.argv[1];models.db.init(os.path.join(root,'calendar.db'));models.init_db();models.DATA_DIR=backend.DATA_DIR=root
service=FakeCalendar();service.token='test-session-memory';service.expires=time.monotonic()+3600
service.calendars=lambda:[{'id':'primary','name':'Mi calendario','primary':True,'timeZone':'America/Argentina/Buenos_Aires'}]
service.events['remote-event']={'id':'remote-event','etag':'v1','summary':'Evento desde Google','start':{'date':'2026-11-07'},'end':{'date':'2026-11-08'}}
google_calendar.GOOGLE_CALENDAR=service
models.save_reminder_orm({'id':234,'title':'Recordatorio local','date':'2026-11-06','time':'09:00'})
class Handler(backend.NoteJSRequestHandler):
 def do_GET(self):
  if self.path=='/api/firebase/config': self._send_json({'configured':False})
  else:super().do_GET()
server=backend.ThreadingHTTPServer(('127.0.0.1',0),Handler);print(server.server_port,flush=True);server.serve_forever()
