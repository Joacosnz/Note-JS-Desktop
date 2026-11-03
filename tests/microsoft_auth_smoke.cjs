const assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {spawn}=require('node:child_process');
const {openBrowser,until}=require('./browser_helpers.cjs');
const root=path.resolve(__dirname,'..');
const temporary=fs.mkdtempSync(path.join(os.tmpdir(),'notejs-microsoft-'));
const python=process.env.NOTEJS_TEST_PYTHON || path.join(process.env.LOCALAPPDATA,'Python/pythoncore-3.15-64/python.exe');
let server,browser,nativeSession;
async function evaluateIn(sessionId,expression){
  const result=await browser.call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true},sessionId);
  if(result.exceptionDetails)throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  return result.result.value;
}
async function fillProviderForm(sessionId,email,name){
  await evaluateIn(sessionId,"[...document.querySelectorAll('button')].find(b=>b.textContent.includes('Add new account')).click()");
  await evaluateIn(sessionId,`(()=>{for(const [id,value] of Object.entries({'email-input':${JSON.stringify(email)},'display-name-input':${JSON.stringify(name)}})){const input=document.getElementById(id);input.value=value;input.dispatchEvent(new Event('input',{bubbles:true}));input.dispatchEvent(new Event('change',{bubbles:true}))} [...document.querySelectorAll('button')].find(b=>b.textContent.includes('Sign in with Microsoft.com')).click()})()`);
}
(async()=>{
  server=spawn(python,['-u',path.join(__dirname,'firebase_test_server.py'),temporary],{cwd:root,windowsHide:true});
  server.stderr.on('data',d=>process.stderr.write(d));
  const port=await new Promise((resolve,reject)=>{server.stdout.once('data',d=>resolve(Number(d.toString().trim())));server.once('error',reject)});
  browser=await openBrowser(temporary);
  await browser.navigate('http://127.0.0.1:'+port);
  await until(()=>browser.evaluate("document.getElementById('firebase-status')?.textContent.includes('Conecta tu cuenta')"),'Auth UI did not initialize');
  await browser.evaluate('openCloudSettings()');
  await browser.call('Runtime.evaluate',{expression:"document.getElementById('firebase-signin-microsoft').click()",userGesture:true},browser.sessionId);
  let popup;
  await until(async()=>{
    const targets=await browser.call('Target.getTargets');
    popup=targets.targetInfos.find(t=>t.type==='page' && t.url.includes('/emulator/auth/handler'));
    return !!popup;
  },'Microsoft popup did not open');
  const attached=await browser.call('Target.attachToTarget',{targetId:popup.targetId,flatten:true});
  const popupSession=attached.sessionId;
  await until(()=>evaluateIn(popupSession,"document.readyState==='complete' && !!document.body.textContent.trim()"),'Provider form did not load');
  await fillProviderForm(popupSession,'microsoft-desktop@example.test','Microsoft Desktop');
  await until(()=>browser.evaluate("document.getElementById('firebase-account')?.textContent==='Microsoft Desktop'"),'Microsoft account did not sign in');
  const identity=await browser.evaluate("import('/vendor/firebase-sdk.mjs').then(s=>({uid:s.getAuth().currentUser.uid,providers:s.getAuth().currentUser.providerData.map(p=>p.providerId)}))");
  assert.ok(identity.providers.includes('microsoft.com'));
  assert.equal(await browser.evaluate("document.getElementById('firebase-signin').hidden && document.getElementById('firebase-signin-microsoft').hidden"),true);
  await until(()=>browser.evaluate("document.getElementById('firebase-status').textContent.includes('Conectado.')"),'Microsoft sync did not become ready');
  const remoteId=await browser.evaluate("(async()=>{createNewNote();const n=getActiveNote();n.title='Nota Microsoft';n.content='<p>Creada con Microsoft</p>';await NoteJSLocal.persist(n,false);await NoteJSCloud.syncNow();return n.cloud.remoteId})()");
  const document=await fetch(`http://127.0.0.1:18085/v1/projects/demo-notejs-desktop/databases/desktop-test/documents/users/${identity.uid}/notes/${remoteId}`,{headers:{Authorization:'Bearer owner'}}).then(r=>r.json());
  assert.equal(document.fields.userId.stringValue,identity.uid);
  assert.equal(document.fields.title.stringValue,'Nota Microsoft');
  await browser.navigate('http://127.0.0.1:'+port+'/?restore=1');
  await until(()=>browser.evaluate("document.getElementById('firebase-account')?.textContent==='Microsoft Desktop'"),'Microsoft session did not persist');
  await browser.evaluate("document.getElementById('firebase-signout').click()");
  await until(()=>browser.evaluate("document.getElementById('firebase-account').textContent==='Sin cuenta conectada'"),'Sign out failed');
  assert.equal(await browser.evaluate("!document.getElementById('firebase-signin').hidden && !document.getElementById('firebase-signin-microsoft').hidden"),true);
  // WebView2 owns its session through a full redirect, without replaying Microsoft tokens.
  await browser.evaluate("window.pywebview={api:{open_microsoft_signin:()=>{window.open('/microsoft-signin.html','native-microsoft','noopener');return Promise.resolve({ok:true})}}}");
  await browser.call('Runtime.evaluate',{expression:"document.getElementById('firebase-signin-microsoft').click()",userGesture:true},browser.sessionId);
  let nativeWindow;
  await until(async()=>{nativeWindow=(await browser.call('Target.getTargets')).targetInfos.find(t=>t.type==='page'&&t.url.includes('/microsoft-signin.html'));return !!nativeWindow},'Native authentication window did not open');
  nativeSession=(await browser.call('Target.attachToTarget',{targetId:nativeWindow.targetId,flatten:true})).sessionId;
  await until(()=>evaluateIn(nativeSession,"!!document.getElementById('signin') && !document.getElementById('signin').disabled"),'Microsoft window did not initialize');
  assert.equal(await evaluateIn(nativeSession,'!!window.pywebview?.api'),false);
  await browser.call('Runtime.evaluate',{expression:"document.getElementById('signin').click()",userGesture:true},nativeSession);
  await until(async()=>{try{return await evaluateIn(nativeSession,"location.pathname.includes('/emulator/auth/handler') && document.readyState==='complete'")}catch{return false}},'Desktop Microsoft redirect did not open');
  await fillProviderForm(nativeSession,'microsoft-native@example.test','Microsoft Native');
  await until(async()=>{try{return await browser.evaluate("document.getElementById('firebase-account')?.textContent==='Microsoft Native'")}catch{return false}},'Desktop redirect did not restore its Firebase session');
  const nativeIdentity=await browser.evaluate("import('/vendor/firebase-sdk.mjs').then(s=>({uid:s.getAuth().currentUser.uid,providers:s.getAuth().currentUser.providerData.map(p=>p.providerId)}))");
  assert.ok(nativeIdentity.providers.includes('microsoft.com'));
  assert.notEqual(nativeIdentity.uid,identity.uid);
  assert.ok(!await browser.evaluate(`state.notes.some(n=>n.title==='Nota Microsoft' && n.cloud?.uid===${JSON.stringify(nativeIdentity.uid)})`));
  console.log('PASS: Microsoft popup and desktop redirect; correct Firebase provider and UID; synchronized note; session persistence; sign out and account isolation.');
})().catch(async e=>{console.error(e);if(browser)console.error(await browser.evaluate("document.getElementById('firebase-status')?.textContent"));if(nativeSession){try{console.error(await evaluateIn(nativeSession,"({path:location.pathname,text:document.body.innerText})"))}catch{}}process.exitCode=1}).finally(async()=>{if(browser)await browser.close();if(server)server.kill()});
