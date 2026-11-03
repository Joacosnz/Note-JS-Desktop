import * as pdfjs from '/vendor/pdfjs/build/pdf.mjs';
pdfjs.GlobalWorkerOptions.workerSrc = '/vendor/pdfjs/build/pdf.worker.mjs';
const $ = id => document.getElementById(id);
const params = new URLSearchParams(location.search);
const source = params.get('src');
const name = params.get('name') || 'Documento.pdf';
$('title').textContent = name;
document.title = `${name} · Note JS`;
let pdf, original, pageNumber = 1, scale = 'fit', viewport, rendering = false, pending = false;
let drawing = false, stroke = null, dirty = false, searching = false;
const rotations = new Map(), strokes = new Map(), texts = new Map();
const canvas = $('page-canvas'), ink = $('ink');
const status = message => { $('status').textContent = message; };

async function pageText(number) {
  if (!texts.has(number)) {
    const page = await pdf.getPage(number);
    const content = await page.getTextContent();
    texts.set(number, content.items.map(item => (item.str || '') + (item.hasEOL ? '\n' : ' ')).join(''));
  }
  return texts.get(number);
}

function paintInk() {
  const ctx = ink.getContext('2d');
  ctx.clearRect(0, 0, ink.width, ink.height);
  ctx.lineCap = ctx.lineJoin = 'round';
  for (const line of strokes.get(pageNumber) || []) {
    ctx.beginPath();
    ctx.strokeStyle = line.color;
    ctx.lineWidth = 2 * viewport.scale;
    line.points.forEach((point, index) => {
      const [x, y] = viewport.convertToViewportPoint(...point);
      if (index) ctx.lineTo(x, y); else ctx.moveTo(x, y);
    });
    ctx.stroke();
  }
}

async function render() {
  if (!pdf) return;
  if (rendering) { pending = true; return; }
  rendering = true;
  $('draw').disabled = true;
  ink.classList.remove('drawing');
  try {
    const number = pageNumber;
    const page = await pdf.getPage(number);
    const rotation = (page.rotate + (rotations.get(number) || 0)) % 360;
    const base = page.getViewport({ scale: 1, rotation });
    const actualScale = scale === 'fit' ? Math.max(.1, ($('viewport').clientWidth - 32) / base.width) : Number(scale);
    viewport = page.getViewport({ scale: actualScale, rotation });
    // Bound canvas allocation even for unusually large PDF pages.
    const dpr = Math.min(devicePixelRatio || 1, 2, 8192 / Math.max(viewport.width, viewport.height));
    canvas.width = Math.ceil(viewport.width * dpr);
    canvas.height = Math.ceil(viewport.height * dpr);
    canvas.style.width = ink.style.width = `${viewport.width}px`;
    canvas.style.height = ink.style.height = `${viewport.height}px`;
    ink.width = Math.ceil(viewport.width); ink.height = Math.ceil(viewport.height);
    await page.render({ canvasContext: canvas.getContext('2d'), viewport, transform: [dpr, 0, 0, dpr, 0, 0] }).promise;
    paintInk();
    $('page').value = number;
    $('previous').disabled = number <= 1;
    $('next').disabled = number >= pdf.numPages;
    if (!$('text').hidden) $('text').textContent = await pageText(number);
    status(dirty ? 'Cambios pendientes. Guarda una copia para conservarlos.' : '');
  } catch (error) { status(`No se pudo mostrar la página: ${error.message}`); }
  finally {
    rendering = false;
    $('draw').disabled = false;
    ink.classList.toggle('drawing', drawing);
    if (pending) { pending = false; render(); }
  }
}

function navigate(number) {
  if (!pdf || rendering) return;
  pageNumber = Math.min(pdf.numPages, Math.max(1, Number(number) || 1));
  stroke = null;
  render();
}
$('previous').onclick = () => navigate(pageNumber - 1);
$('next').onclick = () => navigate(pageNumber + 1);
$('page').onchange = () => navigate($('page').value);
$('zoom').onchange = () => { scale = $('zoom').value; render(); };
function zoomBy(factor) {
  scale = Math.min(4, Math.max(.25, (viewport?.scale || 1) * factor));
  render();
}
$('zoom-in').onclick = () => zoomBy(1.25);
$('zoom-out').onclick = () => zoomBy(.8);
$('rotate').onclick = () => {
  if (!pdf || rendering) return;
  rotations.set(pageNumber, ((rotations.get(pageNumber) || 0) + 90) % 360);
  dirty = true; render();
};
$('draw').onclick = () => {
  if (!pdf || rendering) return;
  drawing = !drawing;
  $('draw').setAttribute('aria-pressed', String(drawing));
  ink.classList.toggle('drawing', drawing);
};
$('undo').onclick = () => { if (rendering) return; strokes.get(pageNumber)?.pop(); paintInk(); dirty = true; status('Cambios pendientes. Guarda una copia para conservarlos.'); };
function point(event) {
  const rect = ink.getBoundingClientRect();
  return viewport.convertToPdfPoint((event.clientX - rect.left) * viewport.width / rect.width, (event.clientY - rect.top) * viewport.height / rect.height);
}
ink.onpointerdown = event => {
  if (!drawing || rendering || event.button !== 0) return;
  ink.setPointerCapture(event.pointerId);
  stroke = { color: $('color').value, points: [point(event)] };
  if (!strokes.has(pageNumber)) strokes.set(pageNumber, []);
  strokes.get(pageNumber).push(stroke);
};
ink.onpointermove = event => { if (stroke) { stroke.points.push(point(event)); paintInk(); } };
ink.onpointerup = ink.onpointercancel = () => {
  if (!stroke) return;
  if (stroke.points.length === 1) stroke.points.push([stroke.points[0][0] + .1, stroke.points[0][1]]);
  stroke = null; dirty = true; paintInk(); status('Cambios pendientes. Guarda una copia para conservarlos.');
};
$('text-toggle').onclick = async () => {
  if (!pdf) return;
  $('text').hidden = !$('text').hidden;
  $('text-toggle').setAttribute('aria-pressed', String(!$('text').hidden));
  if (!$('text').hidden) {
    try { $('text').textContent = (await pageText(pageNumber)) || 'Este PDF no contiene texto seleccionable.'; }
    catch (error) { status(error.message); }
  }
};
$('search').onsubmit = async event => {
  event.preventDefault();
  const query = $('query').value.trim().toLocaleLowerCase();
  if (!pdf || !query || searching) return;
  searching = true; $('results').replaceChildren(); $('results').hidden = true;
  try {
    for (let number = 1; number <= pdf.numPages; number++) {
      status(`Buscando… ${number} / ${pdf.numPages}`);
      if ((await pageText(number)).toLocaleLowerCase().includes(query)) {
        $('results').add(new Option(`Página ${number}`, String(number)));
      }
    }
    $('results').hidden = !$('results').options.length;
    if ($('results').options.length) { $('text').hidden = false; navigate($('results').value); }
    status($('results').options.length ? `${$('results').options.length} páginas con coincidencias.` : 'No se encontraron coincidencias. Los documentos escaneados requieren OCR.');
  } catch (error) { status(`No se pudo buscar: ${error.message}`); }
  finally { searching = false; }
};
$('results').onchange = () => navigate($('results').value);

$('save').onclick = async () => {
  $('save').disabled = true;
  try {
    let bytes = original;
    const hasEdits = [...rotations.values()].some(Boolean) || [...strokes.values()].some(lines => lines.length);
    if (hasEdits) {
      const { PDFDocument, degrees, rgb } = window.PDFLib;
      const output = await PDFDocument.load(original);
      const pages = output.getPages();
      for (const [number, angle] of rotations) pages[number - 1].setRotation(degrees((pages[number - 1].getRotation().angle + angle) % 360));
      for (const [number, lines] of strokes) {
        for (const line of lines) {
          const color = rgb(...[1, 3, 5].map(index => parseInt(line.color.slice(index, index + 2), 16) / 255));
          for (let i = 1; i < line.points.length; i++) pages[number - 1].drawLine({ start: { x: line.points[i - 1][0], y: line.points[i - 1][1] }, end: { x: line.points[i][0], y: line.points[i][1] }, color, thickness: 2 });
        }
      }
      bytes = await output.save();
    }
    const filename = name.replace(/\.pdf$/i, '') + (hasEdits ? '-anotado.pdf' : '.pdf');
    const bridge = window.parent.pywebview?.api;
    if (bridge?.save_pdf_copy) {
      const blob = new Blob([bytes], { type: 'application/pdf' });
      const dataUrl = await new Promise(resolve => { const reader = new FileReader(); reader.onload = () => resolve(reader.result); reader.readAsDataURL(blob); });
      const result = await bridge.save_pdf_copy(dataUrl, filename);
      if (!result.ok) { if (result.cancelled) return; throw new Error(result.error); }
    } else {
      const url = URL.createObjectURL(new Blob([bytes], { type: 'application/pdf' }));
      const link = document.createElement('a'); link.href = url; link.download = filename; link.click();
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    }
    dirty = false; status('Copia guardada. El archivo original se conserva.');
  } catch (error) { status(`No se pudo guardar: ${error.message}`); }
  finally { $('save').disabled = false; }
};
window.addEventListener('beforeunload', event => { if (dirty) { event.preventDefault(); event.returnValue = ''; } });
window.addEventListener('message', event => {
  if (event.origin === location.origin && event.source === parent && event.data?.type === 'notejs-pdf-close') {
    if (!dirty || confirm('Hay cambios sin guardar. ¿Cerrar el PDF?')) parent.postMessage({ type: 'notejs-pdf-close-ok' }, location.origin);
  }
});
let resizeTimer;
new ResizeObserver(() => { clearTimeout(resizeTimer); resizeTimer = setTimeout(() => { if (scale === 'fit') render(); }, 150); }).observe($('viewport'));

try {
  if (!source) throw new Error('Selecciona un PDF desde Note JS.');
  const url = new URL(source, location.origin);
  if (!['http:', 'https:', 'data:'].includes(url.protocol) || (url.protocol === 'data:' && !source.startsWith('data:application/pdf'))) throw new Error('Enlace de PDF no permitido.');
  const response = await fetch(url);
  if (!response.ok) throw new Error(`El archivo no está disponible (${response.status}).`);
  const blob = await response.blob();
  if (blob.size > 50 * 1024 * 1024) throw new Error('El límite por PDF es de 50 MB.');
  original = new Uint8Array(await blob.arrayBuffer());
  const task = pdfjs.getDocument({ data: original.slice(), cMapUrl: '/vendor/pdfjs/cmaps/', cMapPacked: true, standardFontDataUrl: '/vendor/pdfjs/standard_fonts/', wasmUrl: '/vendor/pdfjs/wasm/', iccUrl: '/vendor/pdfjs/iccs/', isEvalSupported: false });
  task.onPassword = (update, reason) => {
    const password = prompt(reason === 2 ? 'Contraseña incorrecta. Inténtalo de nuevo:' : 'Contraseña del PDF:');
    if (password === null) { task.destroy(); status('Apertura cancelada.'); } else update(password);
  };
  pdf = await task.promise;
  $('pages').textContent = pdf.numPages;
  $('page').max = pdf.numPages;
  $('save').disabled = false;
  await render();
} catch (error) { status(`No se pudo abrir el PDF. ${error.message} Si usas un enlace externo, descarga el archivo y ábrelo localmente.`); }
