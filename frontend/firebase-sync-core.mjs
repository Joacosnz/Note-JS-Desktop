// Pure synchronization decisions, independent of Firebase and the UI.
export function canonical(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
  return '{' + Object.keys(value).sort().filter(key => value[key] !== undefined).map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}';
}
export function localSignature(note) {
  const { cloud, updatedAt, revisions, ...content } = note;
  return canonical(content);
}
export function remoteRevision(data) {
  const timestamp = data?.updatedAt;
  return timestamp && typeof timestamp.seconds === 'number'
    ? `${timestamp.seconds}:${timestamp.nanoseconds}` : canonical(timestamp ?? data?.lastModifiedLocal ?? null);
}
// Listener callbacks may be queued behind a write that has already been acknowledged.
// Ignore older snapshots instead of turning our own previous write into a conflict.
export function compareRemoteUpdates(left, right) {
  const time = data => {
    const value = data?.updatedAt;
    if (value && Number.isFinite(value.seconds) && Number.isFinite(value.nanoseconds)) return [value.seconds,value.nanoseconds];
    if (typeof value === 'number' && Number.isFinite(value)) return [Math.floor(value/1000),Math.round((value%1000)*1e6)];
    return null;
  };
  const a = time(left), b = time(right);
  return a && b ? Math.sign(a[0]-b[0]) || Math.sign(a[1]-b[1]) : null;
}
export function hasLocalChanges(note) {
  return !!note.cloud && localSignature(note) !== note.cloud.syncedSignature;
}
export function writeDecision(note, uid, remote) {
  if (!note.cloud || note.cloud.uid !== uid) return 'wrong-account';
  if (!hasLocalChanges(note)) return 'unchanged';
  if (!remote) return note.cloud.baseRevision ? 'deleted-remotely' : 'create';
  if (!note.cloud.baseRevision || remoteRevision(remote) !== note.cloud.baseRevision) return 'conflict';
  return 'update';
}
export function newLocalId(notes, now = Date.now()) {
  const occupied = new Set(notes.map(note => Number(note.id)));
  while (occupied.has(now)) now++;
  return now;
}
