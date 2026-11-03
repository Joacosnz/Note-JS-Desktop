/* Gallery photos live in the app's private attachments, independent of the original file. */
let coverPhotoTargetId = null;

function chooseNoteCoverPhoto(noteId) {
  const note = noteId == null ? getActiveNote() : state.notes.find(n => n.id === Number(noteId));
  if (!note) return;
  coverPhotoTargetId = note.id;
  const input = document.getElementById('cover-photo-picker');
  input.value = '';
  input.click();
}

async function prepareCoverPhoto(file) {
  if (file.size > 20 * 1024 * 1024) throw new Error('Elegí una foto de hasta 20 MB.');
  if (!file.type.startsWith('image/')) throw new Error('Seleccioná un archivo de imagen.');
  const source = URL.createObjectURL(file);
  try {
    const image = new Image();
    image.src = source;
    try { await image.decode(); }
    catch { throw new Error('No se pudo abrir la foto. Probá con JPG, PNG o WebP.'); }
    const ratio = Math.min(1, 2560 / Math.max(image.naturalWidth, image.naturalHeight));
    const canvas = document.createElement('canvas');
    canvas.width = Math.max(1, Math.round(image.naturalWidth * ratio));
    canvas.height = Math.max(1, Math.round(image.naturalHeight * ratio));
    const context = canvas.getContext('2d');
    context.fillStyle = '#ffffff';
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.drawImage(image, 0, 0, canvas.width, canvas.height);
    return await new Promise((resolve, reject) => canvas.toBlob(blob => {
      if (blob) resolve(blob);
      else reject(new Error('No se pudo preparar la foto.'));
    }, 'image/jpeg', 0.9));
  } finally { URL.revokeObjectURL(source); }
}

async function importNoteCoverPhoto(file, noteId) {
  const photo = await prepareCoverPhoto(file);
  const response = await fetch('/api/covers', {
    method: 'POST', headers: {'Content-Type': 'image/jpeg'}, body: photo
  });
  const result = await response.json();
  if (!response.ok || !result.ok) throw new Error(result.error || 'No se pudo guardar la portada.');
  const note = state.notes.find(n => n.id === Number(noteId));
  if (!note || note.isTrashed) return;
  const updated = {...note, hasCover:true, coverStyle:`url(${result.url})`, coverPositionY:50, updatedAt:Date.now()};
  // Persist the captured note: the user may have opened another tab during decoding.
  await window.NoteJSLocal.persist(updated, false);
  window.NoteJSCloud?.changed();
  renderNotesList();
  renderNoteTabs();
  if (state.isHomeActive) renderHomeNotesContent();
  if (state.activeNoteId === note.id && !state.isHomeActive) loadActiveNote();
  showToast('Foto de portada guardada', '🖼');
  return result;
}

async function handleCoverPhotoSelection(input) {
  const file = input.files?.[0];
  const noteId = coverPhotoTargetId;
  input.value = '';
  coverPhotoTargetId = null;
  if (!file || noteId == null) return;
  try { await importNoteCoverPhoto(file, noteId); }
  catch (error) { showToast(error.message, '🖼'); }
}

function noteCoverBackground(note) {
  if (!note?.hasCover || note.isLocked) return 'var(--bg-surface-hover)';
  return note.coverStyle || COVER_PRESETS[0];
}
