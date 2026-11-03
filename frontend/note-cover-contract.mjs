// Stable IDs are shared with Android's NoteCoverPresets. Never store CSS in Firestore.
export const NOTE_COVERS = [
  {id:'midnight',label:'Medianoche',colors:['#0f172a','#1e293b','#334155']},
  {id:'slate',label:'Pizarra',colors:['#0f172a','#334155','#475569']},
  {id:'forest',label:'Bosque',colors:['#064e3b','#059669','#10b981']},
  {id:'violet',label:'Lavanda',colors:['#4c1d95','#7c3aed','#c084fc']},
  {id:'rose',label:'Rosa',colors:['#831843','#db2777','#f472b6']}
];
export const coverCss = preset => `linear-gradient(135deg, ${preset.colors[0]} 0%, ${preset.colors[1]} 50%, ${preset.colors[2]} 100%)`;
// Local attachment URLs are device-specific and must never be published to Firestore.
export const isLocalPhotoCover = style => typeof style === 'string' && /^url\(\/api\/covers\/[a-f0-9]{64}\.jpg\)$/.test(style);
export function desktopCoverToRemote(note) {
  const selected = NOTE_COVERS.find(preset => coverCss(preset) === note.coverStyle)
    || NOTE_COVERS.find(preset => preset.id === note.coverPresetId) || NOTE_COVERS[0];
  const position = typeof note.coverPositionY === 'number' && Number.isFinite(note.coverPositionY) ? note.coverPositionY : 50;
  return {hasCover:!!note.hasCover,coverPresetId:selected.id,coverPositionY:Math.round(Math.min(100,Math.max(0,position)))};
}
export function remoteCoverToDesktop(data, existing = {}) {
  existing = existing || {};
  if (typeof data.hasCover !== 'boolean') return {hasCover:!!existing.hasCover,coverStyle:existing.coverStyle || coverCss(NOTE_COVERS[0]),coverPositionY:existing.coverPositionY ?? 50};
  const selected = NOTE_COVERS.find(preset => preset.id === data.coverPresetId) || NOTE_COVERS[0];
  const position = typeof data.coverPositionY === 'number' && Number.isFinite(data.coverPositionY) ? data.coverPositionY : 50;
  const style = data.hasCover && isLocalPhotoCover(existing.coverStyle) ? existing.coverStyle : coverCss(selected);
  return {hasCover:data.hasCover,coverPresetId:selected.id,coverStyle:style,coverPositionY:Math.round(Math.min(100,Math.max(0,position)))};
}
