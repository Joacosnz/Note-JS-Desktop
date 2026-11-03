/* Real Edge rendering/export smoke test. Run with Node; no npm dependencies. */
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const assert = require('node:assert/strict');
const { once } = require('node:events');
const { PDFDocument, decodePDFRawStream } = require('../frontend/vendor/pdf-lib.min.js');
const root = path.resolve(__dirname, '..');
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'notejs-pdf-smoke-'));
const python = process.env.NOTEJS_TEST_PYTHON || path.join(process.env.LOCALAPPDATA, 'Python/pythoncore-3.15-64/python.exe');
const edge = process.env.NOTEJS_TEST_BROWSER || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
let server, browser, socket;
async function until(callback, message, timeout = 25000) {
  const end = Date.now() + timeout;
  while (Date.now() < end) { const result = await callback(); if (result) return result; await delay(100); }
  throw new Error(message);
}
(async () => {
  server = spawn(python, ['-u', '-c', "import sys, backend; backend.DATA_DIR=sys.argv[1]; s=backend.ThreadingHTTPServer(('127.0.0.1',0),backend.NoteJSRequestHandler); print(s.server_port,flush=True); s.serve_forever()", temporary], { cwd: root, windowsHide: true });
  server.stderr.on('data', data => process.stderr.write(data));
  const port = await new Promise((resolve, reject) => { server.stdout.once('data', data => resolve(Number(data.toString().trim()))); server.once('error', reject); });
  const base = `http://127.0.0.1:${port}`;
  const fixture = await PDFDocument.create();
  fixture.addPage([500, 650]).drawText('Note JS PDF smoke page one', { x: 35, y: 580 });
  fixture.addPage([500, 650]).drawText('Second page searchable algebra', { x: 35, y: 580 });
  const original = await fixture.save();
  const response = await fetch(base + '/api/pdfs?name=smoke.pdf', { method: 'POST', headers: { 'Content-Type': 'application/pdf' }, body: original });
  assert.equal(response.status, 201);
  const imported = await response.json();
  browser = spawn(edge, ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--remote-debugging-port=0', `--user-data-dir=${path.join(temporary, 'edge')}`, 'about:blank'], { windowsHide: true, stdio: 'ignore' });
  const activePort = path.join(temporary, 'edge', 'DevToolsActivePort');
  await until(() => fs.existsSync(activePort), 'Edge did not start');
  const debugPort = fs.readFileSync(activePort, 'utf8').split('\n')[0];
  const version = await fetch(`http://127.0.0.1:${debugPort}/json/version`).then(r => r.json());
  socket = new WebSocket(version.webSocketDebuggerUrl); await once(socket, 'open');
  let id = 0;
  const waiting = new Map();
  socket.onmessage = event => {
    const data = JSON.parse(event.data);
    if (data.id && waiting.has(data.id)) {
      const { resolve, reject } = waiting.get(data.id); waiting.delete(data.id);
      if (data.error) reject(new Error(data.error.message)); else resolve(data.result);
    }
  };
  function call(method, params = {}, sessionId) {
    return new Promise((resolve, reject) => { const current = ++id; waiting.set(current, { resolve, reject }); socket.send(JSON.stringify({ id: current, method, params, ...(sessionId ? { sessionId } : {}) })); });
  }
  const target = await call('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await call('Target.attachToTarget', { targetId: target.targetId, flatten: true });
  const evaluate = async expression => {
    const result = await call('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true }, sessionId);
    if (result.exceptionDetails) throw new Error(result.exceptionDetails.text + ': ' + result.exceptionDetails.exception?.description);
    return result.result.value;
  };
  await call('Page.enable', {}, sessionId);
  await call('Emulation.setDeviceMetricsOverride', { width: 1100, height: 850, deviceScaleFactor: 1, mobile: false }, sessionId);
  await call('Page.navigate', { url: base + '/pdf-viewer.html?' + new URLSearchParams({ src: imported.url, name: imported.name }) }, sessionId);
  await until(() => evaluate("document.getElementById('pages')?.textContent === '2' && !document.getElementById('draw').disabled"), 'PDF did not render');
  assert.ok(await evaluate("document.getElementById('page-canvas').width > 400"));
  await evaluate("document.getElementById('next').click()");
  await until(() => evaluate("document.getElementById('page').value === '2' && !document.getElementById('draw').disabled"), 'Pagination failed');
  await evaluate("document.getElementById('query').value='algebra'; document.getElementById('search').requestSubmit()");
  await until(() => evaluate("document.getElementById('results').options.length === 1 && !document.getElementById('draw').disabled"), 'Search failed');
  assert.match(await evaluate("document.getElementById('text').textContent"), /algebra/);
  await evaluate("document.getElementById('rotate').click()");
  await until(() => evaluate("!document.getElementById('draw').disabled"), 'Rotation failed');
  await evaluate("document.getElementById('draw').click()");
  const rect = await evaluate("(()=>{const r=document.getElementById('ink').getBoundingClientRect(); return {x:r.x+60,y:r.y+70}})()");
  await call('Input.dispatchMouseEvent', { type: 'mousePressed', ...rect, button: 'left', clickCount: 1 }, sessionId);
  await call('Input.dispatchMouseEvent', { type: 'mouseMoved', x: rect.x + 75, y: rect.y + 30, button: 'left', buttons: 1 }, sessionId);
  await call('Input.dispatchMouseEvent', { type: 'mouseReleased', x: rect.x + 75, y: rect.y + 30, button: 'left', clickCount: 1 }, sessionId);
  await evaluate("window.pywebview={api:{save_pdf_copy:async(data,name)=>{window.savedPdf={data,name};return {ok:true}}}}; document.getElementById('save').click()");
  await until(() => evaluate('!!window.savedPdf'), 'Saving annotated copy failed');
  const saved = await evaluate('window.savedPdf');
  assert.equal(saved.name, 'smoke-anotado.pdf');
  const bytes = Buffer.from(saved.data.split(',')[1], 'base64');
  const reopened = await PDFDocument.load(bytes);
  assert.equal(reopened.getPageCount(), 2);
  assert.equal(reopened.getPages()[1].getRotation().angle, 90);
  const content = reopened.getPages()[1].node.Contents().asArray().map(ref => Buffer.from(decodePDFRawStream(reopened.context.lookup(ref)).decode()).toString()).join('\n');
  assert.match(content, /\bRG\b/, 'Exported PDF must contain the drawn stroke');
  assert.ok(bytes.length > original.length);
  await evaluate("window.savedPdf=null;document.getElementById('save').click()");
  await until(() => evaluate('!!window.savedPdf'), 'Repeated save failed');
  const savedAgain = await evaluate('window.savedPdf.data');
  assert.equal((await PDFDocument.load(Buffer.from(savedAgain.split(',')[1], 'base64'))).getPages()[1].getRotation().angle, 90);
  const originalResponse = await fetch(base + imported.url);
  assert.deepEqual(Buffer.from(await originalResponse.arrayBuffer()), Buffer.from(original));
  const image = await call('Page.captureScreenshot', { format: 'png' }, sessionId);
  fs.mkdirSync(path.join(root, '.test-artifacts'), { recursive: true });
  fs.writeFileSync(path.join(root, '.test-artifacts/pdf-reader.png'), Buffer.from(image.data, 'base64'));
  console.log('PASS: import, rendering, pagination, text search, rotation, drawing, PDF export, repeated save, original preserved.');
  await call('Browser.close');
})().catch(error => { console.error(error); process.exitCode = 1; }).finally(async () => {
  socket?.close(); server?.kill(); browser?.kill();
  await delay(500);
  // The directory was created directly under os.tmpdir for this test only.
  if (path.dirname(temporary) === os.tmpdir() && path.basename(temporary).startsWith('notejs-pdf-smoke-')) fs.rmSync(temporary, { recursive: true, force: true, maxRetries: 10, retryDelay: 200 });
});
