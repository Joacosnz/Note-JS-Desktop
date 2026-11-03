/* Shared entry points for standalone PDFs and persistent PDF blocks. */
async function uploadPdfFile(file) {
  if (file.size > 50 * 1024 * 1024) throw new Error('El límite por PDF es de 50 MB.');
  const response = await fetch('/api/pdfs?name=' + encodeURIComponent(file.name), {
    method: 'POST', headers: { 'Content-Type': 'application/pdf' }, body: file
  });
  const result = await response.json();
  if (!response.ok || !result.ok) throw new Error(result.error || 'No se pudo importar el PDF.');
  return result;
}

function openPdfDocument(source, name) {
  const dialog = document.getElementById('pdf-reader-dialog');
  const frame = document.getElementById('pdf-reader-frame');
  if (dialog.open) return;
  frame.src = pdfViewerUrl(source, name);
  dialog.showModal();
}

async function pickPdfDocument(input) {
  const file = input.files?.[0];
  input.value = '';
  if (!file) return;
  try {
    const result = await uploadPdfFile(file);
    openPdfDocument(result.url, result.name);
  } catch (error) { showToast(error.message, '📑'); }
}

document.addEventListener('DOMContentLoaded', () => {
  const dialog = document.getElementById('pdf-reader-dialog');
  const frame = document.getElementById('pdf-reader-frame');
  const requestClose = () => frame.contentWindow.postMessage({ type: 'notejs-pdf-close' }, location.origin);
  document.getElementById('pdf-reader-close').onclick = requestClose;
  dialog.addEventListener('cancel', event => { event.preventDefault(); requestClose(); });
  window.addEventListener('message', event => {
    if (event.origin === location.origin && event.source === frame.contentWindow && event.data?.type === 'notejs-pdf-close-ok') {
      dialog.close(); frame.src = 'about:blank';
    }
  });
  const params = new URLSearchParams(location.search);
  if (params.get('pdf')) openPdfDocument(params.get('pdf'), params.get('pdfName') || 'Documento.pdf');
  if (params.get('pdfError')) alert(params.get('pdfError'));
});
