// Matches NoteBlockSerializer.kt from the companion Android app.
import { desktopCoverToRemote } from '/note-cover-contract.mjs';
export const MOBILE_CODEC_VERSION = 2;
const allowedTags = new Set(['B','STRONG','I','EM','U','S','STRIKE','MARK','CODE','PRE','BR','P','DIV','SPAN','H1','H2','H3','H4','UL','OL','LI','BLOCKQUOTE','A','SUB','SUP','TABLE','THEAD','TBODY','TFOOT','TR','TD','TH','CAPTION','COLGROUP','COL']);
const allowedStyles = new Set(['color','background-color','font-weight','font-style','text-decoration','text-align']);
export function safeUrl(value) {
  return typeof value === 'string' && /^(https?:\/\/|\/api\/pdfs\/|data:image\/(png|jpeg|webp);base64,)/i.test(value) ? value : '';
}
export function safeHtml(html) {
  const template = document.createElement('template'); template.innerHTML = String(html || '');
  const clean = node => {
    for (const child of [...node.children]) {
      if (['SCRIPT','STYLE','IFRAME','OBJECT','EMBED','SVG','MATH','FORM','INPUT'].includes(child.tagName)) { child.remove(); continue; }
      clean(child);
      if (!allowedTags.has(child.tagName)) { child.replaceWith(...child.childNodes); continue; }
      const href = child.tagName === 'A' ? safeUrl(child.getAttribute('href')) : '';
      const spans = ['TD','TH'].includes(child.tagName) ? ['colspan','rowspan'].map(key => [key, Math.min(100, Math.max(1, Number(child.getAttribute(key)) || 1))]) : [];
      const styles = [...child.style].filter(key => allowedStyles.has(key)).map(key => [key, child.style.getPropertyValue(key)]);
      for (const attr of [...child.attributes]) child.removeAttribute(attr.name);
      if (href) { child.setAttribute('href', href); child.setAttribute('rel', 'noopener noreferrer'); }
      for (const [key, value] of spans) if (value > 1) child.setAttribute(key, String(value));
      for (const [key, value] of styles) if (!/url\(|expression|var\(/i.test(value)) child.style.setProperty(key, value);
    }
  };
  clean(template.content);
  return template.innerHTML;
}
const escape = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const sourceAttribute = block => ` data-mobile-block="${escape(JSON.stringify(block))}"`;

function cellColor(value) {
  if (typeof value !== 'string' || !/^(#[a-f0-9]{3,8}|(?:rgb|hsl)a?\([\d\s.,%+-]+\)|[a-z]+)$/i.test(value)) return '';
  // Android stores eight-digit colors as AARRGGBB; CSS expects RRGGBBAA.
  return /^#[a-f0-9]{8}$/i.test(value) ? '#' + value.slice(3) + value.slice(1,3) : value;
}

export function renderMobileTable(block) {
  const matrix = Array.isArray(block.matrix) ? block.matrix : [];
  const rows = Math.max(matrix.length, Number(block.rows) || 0, 1);
  const cols = Math.max(Number(block.cols) || 0, ...matrix.map(row => Array.isArray(row) ? row.length : 0), 1);
  if (rows > 500 || cols > 100 || rows * cols > 10000) return `<div${sourceAttribute(block)} contenteditable="false" class="cloud-preserved-block">Tabla de gran tamaño · Conservada desde el móvil</div>`;
  const rowHtml = Array.from({length:rows}, (_, r) => `<tr>${Array.from({length:cols}, (_, c) => {
    const cell = matrix[r]?.[c] || {};
    const tag = r === 0 && block.hasHeaderRow ? 'th' : 'td';
    const color = cellColor(cell.bg);
    return `<${tag} ${tag === 'th' ? 'scope="col" ' : ''}contenteditable="true" data-mobile-bg="${escape(cell.bg || '')}"${color ? ` style="background-color:${escape(color)}"` : ''}>${safeHtml(cell.text) || '<br>'}</${tag}>`;
  }).join('')}</tr>`);
  return `<div class="cloud-table-block"${sourceAttribute(block)} contenteditable="false" data-zebra="${!!block.hasZebraStripes}"><div class="cloud-table-toolbar"><span class="cloud-table-size">${rows} × ${cols}</span><div><button type="button" data-table-action="row" title="Añadir una fila">+ Fila</button><button type="button" data-table-action="column" title="Añadir una columna">+ Columna</button></div></div><div class="cloud-table-scroll"><table aria-label="Tabla de la nota">${block.hasHeaderRow ? `<thead>${rowHtml.shift()}</thead>` : ''}<tbody>${rowHtml.join('')}</tbody></table></div></div>`;
}

function tableMatrix(table, original = {}) {
  return [...table.rows].map((row,r) => [...row.cells].map((cell,c) => ({
    ...(original.matrix?.[r]?.[c] || {}), text:safeHtml(cell.innerHTML.replace(/^<br\s*\/?>(?:\s*)$/i, '')),
    bg:cell.getAttribute('data-mobile-bg') || cell.style.backgroundColor || original.matrix?.[r]?.[c]?.bg || null
  })));
}

export function upgradeMobileTables(html) {
  const root = document.createElement('div'); root.innerHTML = html || '';
  for (const table of [...root.querySelectorAll('table')]) {
    if (table.closest('.cloud-table-block') || table.closest('td,th')) continue;
    const wrapper = table.closest('[data-mobile-block]');
    let original = {};
    try { original = JSON.parse(wrapper?.getAttribute('data-mobile-block') || '{}'); } catch {}
    if (original.type !== 'table') continue;
    const matrix = tableMatrix(table, original);
    const container = document.createElement('div');
    container.innerHTML = renderMobileTable({...original,matrix,rows:matrix.length,cols:Math.max(0,...matrix.map(row => row.length))});
    wrapper.replaceWith(container.firstElementChild);
  }
  return root.innerHTML;
}

export function mobileToHtml(content) {
  let blocks;
  try { blocks = JSON.parse(content || '[]'); } catch { return safeHtml(content); }
  if (!Array.isArray(blocks)) return `<p>${escape(content)}</p>`;
  return blocks.filter(block => block && typeof block === 'object').map(block => {
    const attr = sourceAttribute(block), text = safeHtml(block.content);
    if (block.type === 'text') {
      const tag = text.includes('<table') ? 'div' : ({TITLE:'h1', SUBTITLE:'h2'}[block.style] || 'p');
      return `<${tag}${attr}>${text || '<br>'}</${tag}>`;
    }
    if (block.type === 'checklist') return `<div${attr} data-cloud-checklist="true"><input type="checkbox" ${block.isChecked ? 'checked' : ''} aria-label="Completada" onchange="this.toggleAttribute('checked',this.checked);syncRichEditor()"><span data-cloud-text="true">${text}</span></div>`;
    if (block.type === 'simpleList') return `<${block.isNumbered ? 'ol' : 'ul'}${attr}><li>${text}</li></${block.isNumbered ? 'ol' : 'ul'}>`;
    if (block.type === 'callout') return `<blockquote${attr}>${text}</blockquote>`;
    if (block.type === 'image' && safeUrl(block.remoteUrl)) return `<div${attr} contenteditable="false"><img src="${escape(safeUrl(block.remoteUrl))}" alt="${escape(block.fileName || 'Imagen')}" style="max-width:100%"></div>`;
    if (block.type === 'pdf' && safeUrl(block.remoteUrl)) return `<div${attr} data-type="pdf" data-source="${escape(block.remoteUrl)}" data-title="${escape(block.fileName || 'Documento.pdf')}" contenteditable="false">${window.createPdfEmbedHTML(block.remoteUrl, block.fileName || 'Documento.pdf')}</div>`;
    if (block.type === 'table') return renderMobileTable(block);
    // Keep unsupported blocks and their original fields intact, including drawings/audio/PDF annotations.
    return `<div${attr} contenteditable="false" class="cloud-preserved-block">📎 ${escape(block.fileName || block.type || 'Bloque móvil')} · Conservado desde el móvil</div>`;
  }).join('');
}

export function htmlToMobile(html) {
  const root = document.createElement('div'); root.innerHTML = html || '';
  const result = [];
  for (const node of root.childNodes) {
    if (node.nodeType === Node.TEXT_NODE) { if (node.textContent.trim()) result.push({type:'text',id:crypto.randomUUID(),content:escape(node.textContent),style:'BODY'}); continue; }
    if (node.nodeType !== Node.ELEMENT_NODE) continue;
    let original = null;
    try { original = JSON.parse(node.getAttribute('data-mobile-block')); } catch {}
    const base = original || { id: node.getAttribute('data-block-id') || crypto.randomUUID() };
    if (original && !['text','checklist','simpleList','callout','table','pdf'].includes(original.type)) { result.push(original); continue; }
    const table = node.tagName === 'TABLE' ? node : node.querySelector('table');
    if (original?.type === 'table' && !table) { result.push(original); continue; }
    if (table) {
      const rows = tableMatrix(table, original || {});
      result.push({...base,type:'table',rows:rows.length,cols:Math.max(0,...rows.map(row => row.length)),matrix:rows,hasHeaderRow:!!table.querySelector('thead th, tr:first-child th') || !!original?.hasHeaderRow,hasZebraStripes:node.hasAttribute('data-zebra') ? node.getAttribute('data-zebra') === 'true' : !!original?.hasZebraStripes});
    } else if (original?.type === 'pdf' || node.getAttribute('data-type') === 'pdf') {
      const src = node.getAttribute('data-source') || original?.remoteUrl || '';
      result.push({...base,type:'pdf',filePath:original?.filePath || '',remoteUrl:src,fileName:node.getAttribute('data-title') || original?.fileName || 'Documento.pdf',fileSizeFormatted:original?.fileSizeFormatted || '',pageCount:original?.pageCount || 0,currentPageIndex:original?.currentPageIndex || 0});
    } else if (node.tagName === 'IMG' || node.querySelector('img')) {
      const image = node.tagName === 'IMG' ? node : node.querySelector('img');
      result.push({...base,type:'image',localUri:'',remoteUrl:image.getAttribute('src') || '',fileName:image.getAttribute('alt') || 'Imagen'});
    } else if (original?.type === 'checklist' || node.querySelector('input[type=checkbox]')) {
      result.push({...base,type:'checklist',content:safeHtml((node.querySelector('[data-cloud-text]') || node.querySelector('[contenteditable=true]') || node).innerHTML),isChecked:!!node.querySelector('input[type=checkbox]')?.checked});
    } else if (node.tagName === 'UL' || node.tagName === 'OL') {
      [...node.children].forEach((item,index) => result.push({...base,id:index ? crypto.randomUUID() : base.id,type:'simpleList',content:safeHtml(item.innerHTML),isNumbered:node.tagName === 'OL',number:index+1}));
    } else {
      result.push({...base,type:node.tagName === 'BLOCKQUOTE' ? 'callout' : 'text',content:safeHtml(node.innerHTML),style:node.tagName === 'H1' ? 'TITLE' : /^H[234]$/.test(node.tagName) ? 'SUBTITLE' : 'BODY'});
    }
  }
  return result;
}

export function toRemoteNote(note, uid, blocks, previous = {}) {
  const data = {...previous, remoteUuid:note.cloud.remoteId,userId:uid,title:note.title || 'Sin título',content:JSON.stringify(blocks),noteType:previous.noteType || 'TEXT',colorIndex:previous.colorIndex || 0,paperStyle:previous.paperStyle || 'BLANK',isPinned:!!note.isPinned,isArchived:!!note.isArchived,isTrashed:!!note.isTrashed,isLocked:!!note.isLocked,lockPin:previous.lockPin || '',tags:note.tags || '',folder:note.folders?.find(folder => folder !== 'Todas Las Notas') || note.folder || 'Personal',checklistData:previous.checklistData || '',drawingData:previous.drawingData || '',mathEvaluations:previous.mathEvaluations || '',pdfPath:previous.pdfPath || '',pdfAnnotationData:previous.pdfAnnotationData || '',isReminderDone:!!previous.isReminderDone,lastModifiedLocal:Math.max(0,note.updatedAt || Date.now()),remoteUrl:previous.remoteUrl || '',remoteImageUrl:previous.remoteImageUrl || '',attachmentsJson:previous.attachmentsJson || '[]'};
  Object.assign(data, desktopCoverToRemote(note), {icon:String(note.emoji || '').slice(0,32)});
  delete data.blocks; delete data.updatedAtServer;
  for (const [key,max] of Object.entries({title:5000,content:500000,tags:5000,folder:200,attachmentsJson:200000})) if (data[key].length > max) throw new Error(`La nota supera el tamaño permitido en ${key}.`);
  return data;
}
