const assert = require('node:assert/strict');
const fs = require('node:fs'), os = require('node:os'), path = require('node:path');
const {spawn} = require('node:child_process');
const {openBrowser, until} = require('./browser_helpers.cjs');
const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'notejs-context-'));
const python = process.env.NOTEJS_TEST_PYTHON || path.join(process.env.LOCALAPPDATA, 'Python/pythoncore-3.15-64/python.exe');
let server, browser;
(async () => {
  server = spawn(python, ['-u', path.join(__dirname, 'cover_photo_test_server.py'), directory, '--welcome'], {windowsHide:true});
  server.stderr.on('data', d => process.stderr.write(d));
  const port = await new Promise((resolve, reject) => {server.stdout.once('data', d => resolve(Number(d.toString().trim()))); server.once('error', reject);});
  browser = await openBrowser(directory);
  await browser.navigate('http://127.0.0.1:' + port);
  const evaluate = browser.evaluate;
  await until(() => evaluate('!!window.NoteJSLocal'), 'App did not initialize');
  await evaluate('NoteJSLocal.ready');
  await evaluate(`window.testErrors=[]; window.addEventListener('error', e=>testErrors.push(e.message)); state.notes.forEach(n=>n.isPinned=false); navigateToHome();`);
  async function clickMenu(label) {
    assert.equal(await evaluate(`(() => {const b=[...document.querySelectorAll('#custom-context-menu button')].find(b=>b.textContent.includes(${JSON.stringify(label)})); if(!b)return false;b.click();return true;})()`), true);
  }
  async function openHomeMenu() {
    await evaluate(`document.querySelector('.home-grid-card').dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:200,clientY:200}))`);
    assert.equal(await evaluate(`document.getElementById('custom-context-menu').classList.contains('open')`), true);
  }
  await openHomeMenu();
  const id = await evaluate(`Number(document.querySelector('.home-grid-card').dataset.homeNoteId)`);
  await clickMenu('Fijar nota');
  assert.equal(await evaluate(`state.notes.find(n=>n.id===${id}).isPinned`), true);
  await openHomeMenu();
  const count = await evaluate('state.notes.length');
  await clickMenu('Duplicar');
  assert.equal(await evaluate('state.notes.length'), count+1);
  assert.deepEqual(await evaluate('testErrors'), []);
  console.log('Context menus: home pin and duplicate passed');
})().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();server?.kill();});
