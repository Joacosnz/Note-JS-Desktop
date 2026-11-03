import * as sdk from '/vendor/firebase-sdk.mjs';
import { localSignature, hasLocalChanges, remoteRevision, writeDecision, newLocalId, compareRemoteUpdates } from '/firebase-sync-core.mjs';
import { mobileToHtml, htmlToMobile, toRemoteNote, upgradeMobileTables, MOBILE_CODEC_VERSION } from '/firebase-mobile-codec.mjs';
import { remoteCoverToDesktop } from '/note-cover-contract.mjs';
import { signInMicrosoft, microsoftAuthMessage } from '/microsoft-auth.mjs';

const $ = id => document.getElementById(id);
let auth, db, storage, unsubscribe, ready = false, processing = Promise.resolve(), timer, loginPending = false, storageAvailable = false;
let microsoftLoginRequested = false;
const setStatus = message => {
  if ($('firebase-status')) $('firebase-status').textContent = message;
  window.dispatchEvent(new CustomEvent('notejs:cloud-status', {detail:{message,connected:!!auth?.currentUser,name:auth?.currentUser?.displayName || auth?.currentUser?.email || '',pending:local()?.getNotes().filter(note => note.cloud?.uid === auth?.currentUser?.uid && hasLocalChanges(note)).length || 0}}));
};
const local = () => window.NoteJSLocal;
const enqueue = task => { processing = processing.then(task).catch(error => setStatus(explain(error))); return processing; };
function explain(error) {
  const messages = {'permission-denied':'Firebase rechazó el acceso. Comprueba las reglas de tu cuenta.', 'auth/unauthorized-domain':'Este dominio no está autorizado para iniciar sesión.', 'auth/popup-closed-by-user':'Inicio de sesión cancelado.', 'unavailable':'Sin conexión. Tus cambios siguen guardados en esta PC.', 'storage/unauthorized':'No se pudo subir el adjunto. Comprueba las reglas de Storage.'};
  return microsoftAuthMessage(error) || messages[error.code] || `No se pudo sincronizar: ${error.message}`;
}
function setLoginPending(value) {
  loginPending = value;
  for (const id of ['firebase-signin','firebase-signin-microsoft']) if ($(id)) $(id).disabled = value;
}
function current(uid) { return auth.currentUser?.uid === uid; }
function notes() { return local().getNotes(); }
function makeCloud(uid, remoteId = crypto.randomUUID()) { return {uid,remoteId,baseRevision:null,syncedSignature:null,remote:{}}; }
function notify(message) { window.showToast?.(message, '☁️'); }
function timestampMillis(value) { return value?.toMillis?.() || (value?.seconds ? value.seconds * 1000 : Number(value)) || Date.now(); }

async function persist(note, refresh = false) { await local().persist(note, refresh); }
async function applyRemote(uid, id, data, existing) {
  if (!current(uid)) return;
  const note = {
    ...(existing || {}), id:existing?.id || newLocalId(notes()),
    ...remoteCoverToDesktop(data,existing),
    title:data.title || 'Sin título', content:mobileToHtml(data.content),
    folder:data.folder || 'Personal', folders:[local().masterFolder, data.folder || 'Personal'],
    tags:data.tags || '',isPinned:!!data.isPinned,isTrashed:!!data.isTrashed,isArchived:!!data.isArchived,isLocked:!!data.isLocked,
    createdAt:timestampMillis(data.createdAt),updatedAt:data.lastModifiedLocal || timestampMillis(data.updatedAt),
    emoji:typeof data.icon === 'string' ? (data.icon || '📝') : (existing?.emoji || '📝'),cloud:{uid,remoteId:id,baseRevision:remoteRevision(data),remote:data,codecVersion:MOBILE_CODEC_VERSION}
  };
  note.cloud.syncedSignature = localSignature(note);
  await persist(note, true);
}
async function keepBoth(uid, note, remoteData) {
  const copy = {...JSON.parse(JSON.stringify(note)),id:newLocalId(notes()),title:(note.title || 'Nota') + ' (copia en conflicto)',cloud:{...makeCloud(uid),remote:note.cloud.remote}};
  await persist(copy, false);
  await applyRemote(uid, note.cloud.remoteId, remoteData, note);
  notify('Había cambios en ambos dispositivos. Se conservaron las dos versiones.');
}
async function detachDeleted(note) {
  note = {...note,title:(note.title || 'Nota') + ' (copia local)',cloud:null};
  await persist(note, true);
  notify('Una nota se eliminó en la nube. Se conservó una copia local.');
}
async function receiveSnapshot(uid, snapshot, first) {
  if (!current(uid)) return;
  if (first) {
    const ids = new Set(snapshot.docs.map(document => document.id));
    for (const note of [...notes()]) if (note.cloud?.uid === uid && note.cloud.baseRevision && !ids.has(note.cloud.remoteId)) await detachDeleted(note);
  }
  for (const change of snapshot.docChanges()) {
    if (!current(uid) || change.doc.metadata.hasPendingWrites) continue;
    if (tombstones().some(item => item.uid === uid && item.remoteId === change.doc.id)) continue;
    const existing = notes().find(note => note.cloud?.uid === uid && note.cloud.remoteId === change.doc.id);
    if (change.type === 'removed') { if (existing) await detachDeleted(existing); continue; }
    const data = change.doc.data();
    if (data.userId !== uid || data.remoteUuid !== change.doc.id) continue;
    if (existing && compareRemoteUpdates(data,existing.cloud.remote) === -1) continue;
    if (existing?.cloud.baseRevision === remoteRevision(data)) {
      // Publish covers that existed only on desktop before presentation sync was added.
      if (typeof data.hasCover !== 'boolean' && existing.hasCover) existing.cloud.syncedSignature = null;
      if (existing.cloud.codecVersion !== MOBILE_CODEC_VERSION) {
        const dirty = hasLocalChanges(existing);
        existing.content = upgradeMobileTables(existing.content);
        existing.cloud.codecVersion = MOBILE_CODEC_VERSION;
        if (!dirty) existing.cloud.syncedSignature = localSignature(existing);
        await persist(existing,true);
      }
      continue;
    }
    if (existing && hasLocalChanges(existing)) await keepBoth(uid, existing, data);
    else await applyRemote(uid, change.doc.id, data, existing);
  }
  schedule();
}
async function uploadAttachments(blocks, uid) {
  for (const block of blocks) {
    if (!['pdf','image','audio'].includes(block.type) || !block.remoteUrl || /^https?:\/\//i.test(block.remoteUrl)) continue;
    if (!storageAvailable) throw new Error('Firebase Storage no está habilitado. La nota con adjuntos locales se conserva en esta PC hasta poder subir sus archivos.');
    const response = await fetch(block.remoteUrl);
    if (!response.ok) throw new Error('No se encuentra un PDF adjunto en esta PC.');
    const blob = await response.blob();
    const digest = [...new Uint8Array(await crypto.subtle.digest('SHA-256', await blob.arrayBuffer()))].map(value => value.toString(16).padStart(2,'0')).join('');
    const filename = digest + ({pdf:'.pdf',image:'.png',audio:'.webm'}[block.type]);
    const reference = sdk.ref(storage, `users/${uid}/notes_media/${filename}`);
    await sdk.uploadBytes(reference, blob, {contentType:blob.type || 'application/octet-stream'});
    if (!current(uid)) throw new Error('La cuenta cambió durante la sincronización.');
    block.remoteUrl = await sdk.getDownloadURL(reference);
    block.filePath = '';
  }
}
async function syncOne(note, uid) {
  if (!current(uid) || note.cloud?.uid !== uid || !hasLocalChanges(note)) return;
  const captured = JSON.parse(JSON.stringify(note));
  const capturedSignature = localSignature(captured);
  const reference = sdk.doc(db,'users',uid,'notes',captured.cloud.remoteId);
  const blocks = htmlToMobile(captured.content);
  await uploadAttachments(blocks, uid);
  const outcome = await sdk.runTransaction(db, async transaction => {
    const snapshot = await transaction.get(reference);
    if (!current(uid)) throw new Error('La cuenta cambió durante la sincronización.');
    const remote = snapshot.exists() ? snapshot.data() : null;
    const decision = writeDecision(captured, uid, remote);
    if (!['create','update'].includes(decision)) return {decision,remote};
    const data = toRemoteNote(captured,uid,blocks,remote || captured.cloud.remote);
    data.createdAt = remote?.createdAt || sdk.serverTimestamp();
    data.updatedAt = sdk.serverTimestamp();
    transaction.set(reference,data);
    return {decision};
  });
  if (!current(uid)) return;
  const latest = notes().find(item => item.id === note.id);
  if (!latest || latest.cloud?.uid !== uid) return;
  if (outcome.decision === 'conflict') { await keepBoth(uid,latest,outcome.remote); return; }
  if (outcome.decision === 'deleted-remotely') { await detachDeleted(latest); return; }
  if (['create','update'].includes(outcome.decision)) {
    const confirmed = await sdk.getDocFromServer(reference);
    if (!current(uid) || !confirmed.exists()) return;
    latest.cloud.baseRevision = remoteRevision(confirmed.data());
    latest.cloud.remote = confirmed.data();
    latest.cloud.syncedSignature = capturedSignature;
    await persist(latest, false);
  }
}
const tombstoneKey = 'notejs-firebase-deletions-v1';
function tombstones() { try { return JSON.parse(localStorage.getItem(tombstoneKey) || '[]'); } catch { return []; } }
async function syncDeletions(uid) {
  for (const item of tombstones().filter(item => item.uid === uid)) {
    const reference = sdk.doc(db,'users',uid,'notes',item.remoteId);
    const conflict = await sdk.runTransaction(db, async transaction => {
      const remote = await transaction.get(reference);
      if (!current(uid)) throw new Error('La cuenta cambió durante la sincronización.');
      if (!remote.exists()) return null;
      if (remoteRevision(remote.data()) !== item.baseRevision) return remote.data();
      transaction.delete(reference); return null;
    });
    if (!current(uid)) return;
    localStorage.setItem(tombstoneKey,JSON.stringify(tombstones().filter(entry => entry.uid !== uid || entry.remoteId !== item.remoteId)));
    if (conflict) { await applyRemote(uid,item.remoteId,conflict,null); notify('La nota cambió en el móvil y se conservó para evitar perder cambios.'); }
  }
}
async function synchronize() {
  const uid = auth.currentUser?.uid;
  if (!ready || !uid) return;
  if (!navigator.onLine) { setStatus('Sin conexión. Tus notas siguen guardadas en esta PC.'); return; }
  setStatus('Sincronizando notas…');
  await syncDeletions(uid);
  const failed = [];
  for (const note of [...notes()]) {
    try { await syncOne(note,uid); } catch(error) { failed.push(error); }
  }
  if (current(uid)) setStatus(failed.length ? `${failed.length} nota(s) pendiente(s). ${explain(failed[0])}` : 'Conectado. Las notas vinculadas se sincronizan con el móvil.');
}
function schedule() { clearTimeout(timer); timer = setTimeout(() => enqueue(synchronize),800); }
window.NoteJSCloud = {
  syncNow() { if (!auth?.currentUser) { window.openCloudSettings?.(); return Promise.resolve(); } return enqueue(synchronize); },
  attachNew(note) { if (auth?.currentUser) note.cloud = makeCloud(auth.currentUser.uid); },
  changed() { if (ready) schedule(); },
  deleted(note) {
    if (!note?.cloud) return;
    const pending = tombstones().filter(entry => entry.uid !== note.cloud.uid || entry.remoteId !== note.cloud.remoteId);
    pending.push({uid:note.cloud.uid,remoteId:note.cloud.remoteId,baseRevision:note.cloud.baseRevision});
    localStorage.setItem(tombstoneKey,JSON.stringify(pending));
    schedule();
  }
};

async function api(path,body) {
  const response = await fetch('/api/firebase/auth/' + path,{method:'POST',headers:{'Content-Type':'application/json','X-NoteJS-Client':'firebase'},body:JSON.stringify(body)});
  const data = await response.json(); if (!response.ok || !data.ok) throw new Error(data.error); return data;
}
async function login() {
  if (loginPending) return;
  setLoginPending(true);
  let popup;
  try {
    // Open immediately while the browser still has user activation.
    if (!window.pywebview?.api?.open_firebase_signin) popup = window.open('about:blank','notejs-signin');
    const session = await api('start',{});
    const url = '/firebase-signin.html?' + new URLSearchParams({state:session.state});
    if (window.pywebview?.api?.open_firebase_signin) {
      const result = await window.pywebview.api.open_firebase_signin(session.state);
      if (!result.ok) throw new Error('No se pudo abrir el navegador.');
    } else if (popup) popup.location = url;
    else throw new Error('Permite abrir la ventana de inicio de sesión.');
    setStatus('Completa el inicio de sesión en el navegador y vuelve aquí.');
    const expires = Date.now()+300000;
    while (Date.now()<expires) {
      await new Promise(resolve => setTimeout(resolve,1500));
      const result = await api('poll',session);
      if (result.credential) {
        await sdk.signInWithCredential(auth,sdk.GoogleAuthProvider.credential(result.credential.idToken));
        return;
      }
    }
    throw new Error('El inicio de sesión caducó. Inténtalo de nuevo.');
  } catch(error) { popup?.close(); setStatus(explain(error)); }
  finally { setLoginPending(false); }
}
async function loginMicrosoft() {
  if (loginPending) return;
  setLoginPending(true);
  setStatus('Conectando con Microsoft…');
  try {
    if (window.pywebview?.api?.open_microsoft_signin) {
      microsoftLoginRequested = true;
      const result = await window.pywebview.api.open_microsoft_signin();
      if (!result?.ok) throw new Error(result?.error || 'No se pudo abrir el acceso Microsoft.');
      setStatus('Completá el acceso en la ventana de Microsoft y volvé a tus notas.');
    } else {
      await signInMicrosoft(sdk, auth, false);
    }
  } catch(error) { microsoftLoginRequested = false; setStatus(explain(error)); }
  finally { setLoginPending(false); }
}
async function restoreMicrosoftSession() {
  if (!microsoftLoginRequested) return;
  microsoftLoginRequested = false;
  try {
    const active = window.getActiveNote?.();
    if (active) await local().persist(active,false);
    // Restore through the public SDK on startup; no OAuth/session tokens cross windows.
    location.reload();
  } catch(error) { setStatus(explain(error)); }
}
if ('BroadcastChannel' in window) {
  const channel = new BroadcastChannel('notejs-microsoft-auth');
  channel.onmessage = event => { if (event.data?.type === 'completed') restoreMicrosoftSession(); };
}
window.addEventListener('storage',event => { if (event.key === 'notejs-microsoft-auth-completed') restoreMicrosoftSession(); });
async function bindLocalNotes() {
  const uid = auth.currentUser?.uid;
  if (!uid) return;
  $('firebase-link-local').disabled = true;
  try {
    for (const note of [...notes()]) {
      if (!current(uid)) break;
      if (!note.cloud) { note.cloud = makeCloud(uid); await persist(note,false); }
    }
    await enqueue(synchronize);
  } finally { $('firebase-link-local').disabled = false; }
}

async function initialize() {
  await local().ready;
  const config = await fetch('/api/firebase/config').then(response => response.json());
  if (!config.configured) { setStatus('Firebase todavía no está configurado.'); return; }
  const app = sdk.initializeApp(config.firebase);
  storageAvailable = !!config.storageAvailable;
  auth = sdk.getAuth(app);
  // Emulator configuration must happen before persistence restoration starts network work.
  if (config.emulators) sdk.connectAuthEmulator(auth,config.emulators.auth,{disableWarnings:true});
  await sdk.setPersistence(auth,sdk.browserLocalPersistence);
  // Redirect returns to the same app/profile, so Microsoft retains its full Firebase session.
  let redirectError = null;
  try { await sdk.getRedirectResult(auth); } catch(error) { redirectError = error; }
  db = sdk.initializeFirestore(app,{localCache:sdk.memoryLocalCache()},config.databaseId);
  storage = sdk.getStorage(app);
  // Explicit test configuration only; localhost is also used by the real desktop app.
  if (config.emulators) {
    sdk.connectFirestoreEmulator(db,config.emulators.host,config.emulators.firestorePort);
    sdk.connectStorageEmulator(storage,config.emulators.host,config.emulators.storagePort);
  }
  $('firebase-signin').onclick = login;
  $('firebase-signin-microsoft').onclick = loginMicrosoft;
  $('firebase-signout').onclick = () => sdk.signOut(auth).catch(error => setStatus(explain(error)));
  $('firebase-link-local').onclick = bindLocalNotes;
  $('firebase-sync-now').onclick = () => enqueue(synchronize);
  sdk.onAuthStateChanged(auth,user => {
    unsubscribe?.(); ready = false;
    $('firebase-account').textContent = user?.displayName || user?.email || 'Sin cuenta conectada';
    $('firebase-signin').hidden = !!user;
    $('firebase-signin-microsoft').hidden = !!user;
    for (const id of ['firebase-signout','firebase-link-local','firebase-sync-now']) $(id).hidden = !user;
    if (!user) { setStatus(redirectError ? explain(redirectError) : 'Conecta tu cuenta de Google o Microsoft para sincronizar las notas con el móvil.'); redirectError = null; return; }
    setStatus('Conectando con tus notas…');
    let first = true;
    unsubscribe = sdk.onSnapshot(sdk.collection(db,'users',user.uid,'notes'),{includeMetadataChanges:true},snapshot => {
      if (snapshot.metadata.fromCache || snapshot.metadata.hasPendingWrites) return;
      const initial = first; first = false;
      enqueue(async () => {
        await receiveSnapshot(user.uid,snapshot,initial);
        if (current(user.uid)) { ready = true; await synchronize(); }
      });
    },error => setStatus(explain(error)));
  });
  window.addEventListener('online',schedule);
  setInterval(() => { if (ready && auth.currentUser && navigator.onLine) enqueue(synchronize); },30000);
}
initialize().catch(error => setStatus(explain(error)));
