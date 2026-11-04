const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path'),{spawn}=require('node:child_process');
const {openBrowser,until}=require('./browser_helpers.cjs');
const root=path.resolve(__dirname,'..'),temp=fs.mkdtempSync(path.join(os.tmpdir(),'notejs-calendar-'));let server,browser;
(async()=>{
 server=spawn(path.join(process.env.LOCALAPPDATA,'Python/pythoncore-3.15-64/python.exe'),['-u',path.join(__dirname,'calendar_test_server.py'),temp],{cwd:root,windowsHide:true});
 const port=await new Promise((resolve,reject)=>{server.stdout.once('data',d=>resolve(Number(d.toString().trim())));server.once('error',reject);server.stderr.on('data',d=>process.stderr.write(d));});
 const origin='http://127.0.0.1:'+port;browser=await openBrowser(temp);await browser.navigate(origin);
 const ev=browser.evaluate;await until(()=>ev('!!window.NoteJSLocal'),'App did not start');await ev('NoteJSLocal.ready');
 await ev('navigateToReminders()');await until(()=>ev('!!document.querySelector("#google-calendar-panel select")'),'Calendar panel did not load');
 await ev('[...document.querySelectorAll("#google-calendar-panel button")].find(b=>b.textContent==="Sincronizar ahora").click()');
 await until(()=>ev('document.querySelector("#google-calendar-panel").textContent.includes("1 recibidos, 1 enviados")'),'Bidirectional sync failed');
 assert.equal(await ev('state.reminders.length'),2);assert.ok(await ev('state.reminders.some(r=>r.title==="Evento desde Google")'));
 await ev('setRemindersTab("pending")');await until(()=>ev('!!document.querySelector("#google-calendar-panel")'),'Panel lost after render');
 const blocked=await fetch(origin+'/api/google-calendar/sync',{method:'POST',headers:{'Content-Type':'application/json','Origin':'https://untrusted.example','X-NoteJS-Client':'calendar'},body:'{}'});assert.equal(blocked.status,403);
 const shot=await browser.call('Page.captureScreenshot',{format:'png'},browser.sessionId);fs.writeFileSync(path.join(root,'.test-artifacts/calendar-desktop.png'),Buffer.from(shot.data,'base64'));
 await ev('[...document.querySelectorAll("#google-calendar-panel button")].find(b=>b.textContent==="Desconectar").click()');await until(()=>ev('document.querySelector("#google-calendar-panel").textContent.includes("Calendar desconectado")'),'Disconnect failed');assert.equal(await ev('state.reminders.length'),2);
 console.log('PASS: real desktop UI + SQLite + simulated Google Calendar: import/export, view refresh, disconnect preserving items, cross-origin protection.');
})().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close();server?.kill();});
