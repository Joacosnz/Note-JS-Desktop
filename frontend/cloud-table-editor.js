/* Table tools operate on the existing editor and use its normal autosave. */
(() => {
  const cells = block => [...block.querySelector('table').rows].flatMap(row => [...row.cells]);
  const save = () => { if (typeof syncRichEditor === 'function') syncRichEditor(); };
  function updateSize(block) {
    const table = block.querySelector('table');
    block.querySelector('.cloud-table-size').textContent = `${table.rows.length} × ${table.rows[0]?.cells.length || 0}`;
  }
  function addRow(block) {
    const table = block.querySelector('table');
    if (table.rows.length >= 500 || (table.rows.length + 1) * table.rows[0].cells.length > 10000) return null;
    const row = (table.tBodies[0] || table.createTBody()).insertRow();
    for (let c = 0; c < table.rows[0].cells.length; c++) {
      const cell = row.insertCell(); cell.contentEditable = 'true'; cell.innerHTML = '<br>';
    }
    updateSize(block); return row;
  }
  function addColumn(block) {
    const table = block.querySelector('table');
    if (table.rows[0].cells.length >= 100 || table.rows.length * (table.rows[0].cells.length + 1) > 10000) return;
    for (const row of table.rows) {
      const cell = document.createElement(row.parentElement.tagName === 'THEAD' ? 'th' : 'td');
      if (cell.tagName === 'TH') cell.scope = 'col';
      cell.contentEditable = 'true'; cell.innerHTML = '<br>'; row.appendChild(cell);
    }
    updateSize(block);
  }
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-table-action]');
    const block = button?.closest('.cloud-table-block');
    if (!block || !block.closest('#rich-editor-canvas')) return;
    event.preventDefault();
    if (button.dataset.tableAction === 'row') addRow(block)?.cells[0]?.focus();
    if (button.dataset.tableAction === 'column') { addColumn(block); block.querySelector('table').rows[0].lastElementChild.focus(); }
    save();
  });
  document.addEventListener('keydown', event => {
    const cell = event.target.closest('.cloud-table-block td, .cloud-table-block th');
    if (!cell || !cell.closest('#rich-editor-canvas') || event.key !== 'Tab') return;
    const block = cell.closest('.cloud-table-block'), ordered = cells(block), index = ordered.indexOf(cell);
    const target = ordered[index + (event.shiftKey ? -1 : 1)];
    if (!target && event.shiftKey) return;
    event.preventDefault(); event.stopPropagation();
    if (target) target.focus();
    else { addRow(block)?.cells[0]?.focus(); save(); }
  },true);
  document.addEventListener('paste', event => {
    const cell = event.target.closest('.cloud-table-block td, .cloud-table-block th');
    const text = event.clipboardData?.getData('text/plain');
    if (!cell || !cell.closest('#rich-editor-canvas') || !text?.includes('\t')) return;
    const matrix = text.replace(/\r/g,'').replace(/\n$/,'').split('\n').map(line => line.split('\t'));
    const table = cell.closest('table'), block = cell.closest('.cloud-table-block');
    const firstRow = cell.parentElement.rowIndex, firstCol = cell.cellIndex;
    const requiredRows = firstRow + matrix.length, requiredCols = firstCol + Math.max(...matrix.map(row => row.length));
    if (requiredRows > 500 || requiredCols > 100 || Math.max(table.rows.length,requiredRows) * Math.max(table.rows[0].cells.length,requiredCols) > 10000) return;
    event.preventDefault(); event.stopPropagation();
    while (table.rows[0].cells.length < requiredCols) addColumn(block);
    while (table.rows.length < requiredRows) addRow(block);
    matrix.forEach((row,r) => row.forEach((value,c) => { table.rows[firstRow+r].cells[firstCol+c].textContent = value; }));
    updateSize(block); save();
  },true);
})();
