const fs = require('fs');
const vm = require('vm');
const path = require('path');
const assert = require('assert');

const appPath = path.resolve(__dirname, '../../../frontend/app.js');
let appCode = fs.readFileSync(appPath, 'utf8');

// Apply Proposed Change:
const oldUnsyncM2 = `    function unsyncBlockInstance(referenceElOrBtn) {
      const refEl = (referenceElOrBtn && referenceElOrBtn.closest) ? referenceElOrBtn.closest('.block-transclusion-reference, .notion-synced-block') : null;
      if (!refEl) return;
      const blockId = refEl.getAttribute('data-block-id');
      if (blockId && typeof convertBlockType === 'function') {
        convertBlockType(blockId, 'text');
        if (typeof showToast === 'function') showToast('Bloque desvinculado (convertido a texto)', '✂️');
      }
    }
    window.unsyncBlockInstance = unsyncBlockInstance;`;

const newUnsyncM2 = `    function unsyncBlockInstance(referenceElOrBtn) {
      let refEl = null;
      let blockId = null;

      if (typeof referenceElOrBtn === 'string') {
        blockId = referenceElOrBtn;
        if (typeof document !== 'undefined' && document.querySelector) {
          refEl = document.querySelector(\`[data-block-id="\${blockId}"]\`) || document.getElementById(blockId);
        }
      } else if (referenceElOrBtn) {
        if (typeof referenceElOrBtn.closest === 'function') {
          refEl = referenceElOrBtn.closest('.block-transclusion-reference, .notion-synced-block, [data-block-id]');
        }
        if (!refEl) refEl = referenceElOrBtn;
        if (refEl && refEl.getAttribute) {
          blockId = refEl.getAttribute('data-block-id') || refEl.id || null;
        }
        if (!blockId && refEl && refEl.dataset) {
          blockId = refEl.dataset.blockId || null;
        }
      }

      const converter = (typeof window !== 'undefined' && typeof window.convertBlockType === 'function')
        ? window.convertBlockType
        : (typeof convertBlockType === 'function' ? convertBlockType : null);

      const toast = (typeof window !== 'undefined' && typeof window.showToast === 'function')
        ? window.showToast
        : (typeof showToast === 'function' ? showToast : null);

      if (blockId && typeof converter === 'function') {
        converter(blockId, 'text');
        if (typeof toast === 'function') toast('Bloque desvinculado (convertido a texto)', '✂️');
        return;
      }

      // Fallback para bloques sincronizados legacy sin data-block-id
      const legacyBlock = refEl && (typeof refEl.closest === 'function' ? refEl.closest('.notion-synced-block') : (refEl.classList && refEl.classList.contains('notion-synced-block') ? refEl : null));
      if (legacyBlock) {
        const bodyEl = legacyBlock.querySelector('.notion-synced-body');
        const wrapper = (typeof document !== 'undefined') ? document.createElement('div') : null;
        if (wrapper) {
          wrapper.innerHTML = bodyEl ? bodyEl.innerHTML : '';
          legacyBlock.replaceWith(...Array.from(wrapper.childNodes));
        }
        if (typeof syncRichEditor === 'function') syncRichEditor();
        if (typeof toast === 'function') toast('Bloque desvinculado y convertido en texto independiente', '🔓');
      }
    }
    window.unsyncBlockInstance = unsyncBlockInstance;`;

appCode = appCode.replace(oldUnsyncM2, newUnsyncM2);

// Replace legacy unsync at line 15498
const oldLegacyUnsync = `    function unsyncBlockInstance(btnEl) {
      const block = btnEl ? btnEl.closest('.notion-synced-block') : null;
      if (!block) return;
      const bodyEl = block.querySelector('.notion-synced-body');
      const wrapper = document.createElement('div');
      wrapper.innerHTML = bodyEl ? bodyEl.innerHTML : '';
      block.replaceWith(...Array.from(wrapper.childNodes));
      syncRichEditor();
      showToast('Bloque desvinculado y convertido en texto independiente', '🔓');
    }`;

appCode = appCode.replace(oldLegacyUnsync, '    // Legacy unsyncBlockInstance unificado en la declaración canónica de la línea 7666');

// Replace legacy copySyncedBlockReference at line 15479 to prevent duplicate declaration
const oldLegacyCopy = `    function copySyncedBlockReference(syncId) {
      const editor = document.getElementById('rich-editor-canvas');
      const sourceBlock = editor ? editor.querySelector(\`.notion-synced-block[data-synced-id="\${syncId}"]\`) : null;
      const bodyEl = sourceBlock ? sourceBlock.querySelector('.notion-synced-body') : null;
      copiedSyncedBlockBuffer = {
        syncId,
        html: bodyEl ? bodyEl.innerHTML : '<p>Contenido sincronizado...</p>'
      };
      showToast('Referencia sincronizada copiada. Usa el menú de bloque o Ctrl+Shift+V para pegarla en cualquier nota', '🔗');
    }`;

const newLegacyCopy = `    // Legacy copySyncedBlockReference unificado en la declaración canónica de la línea 7655
    function legacyCopySyncedBlockBuffer(syncId) {
      const editor = document.getElementById('rich-editor-canvas');
      const sourceBlock = editor ? editor.querySelector(\`.notion-synced-block[data-synced-id="\${syncId}"]\`) : null;
      const bodyEl = sourceBlock ? sourceBlock.querySelector('.notion-synced-body') : null;
      copiedSyncedBlockBuffer = {
        syncId,
        html: bodyEl ? bodyEl.innerHTML : '<p>Contenido sincronizado...</p>'
      };
    }`;

appCode = appCode.replace(oldLegacyCopy, newLegacyCopy);

// Export window.convertBlockType = convertBlockType at line 6830
appCode = appCode.replace(
  'syncRichEditor();\n    }\n\n    function renderBlock(block) {',
  'syncRichEditor();\n    }\n    window.convertBlockType = convertBlockType;\n\n    function renderBlock(block) {'
);

// Now execute the exact script from test_defect_unsync_block_instance_is_shadowed_by_legacy_function
class MockElement {
  constructor(tagName) {
    this.tagName = (tagName || 'DIV').toUpperCase();
    this.nodeType = 1;
    this.className = '';
    this.id = '';
    this.attributes = {};
    this.dataset = {};
    this.style = {};
    this.children = [];
    this.parentNode = null;
    this.innerHTML = '';
    this.textContent = '';
    this.value = '';
    this.checked = false;
    this.classList = {
      add: (c) => { if (!this.className.includes(c)) this.className += ' ' + c; },
      remove: (c) => { this.className = this.className.replace(c, '').trim(); },
      contains: (c) => this.className.includes(c)
    };
  }
  setAttribute(k, v) { this.attributes[k] = String(v); if (k.startsWith('data-')) this.dataset[k.slice(5).replace(/-([a-z])/g, g => g[1].toUpperCase())] = String(v); }
  getAttribute(k) { return this.attributes[k] !== undefined ? this.attributes[k] : null; }
  appendChild(c) { c.parentNode = this; this.children.push(c); return c; }
  querySelector() { return null; }
  querySelectorAll() { return []; }
  closest() { return this; }
}

const mockDoc = {
  createElement: (tag) => new MockElement(tag),
  getElementById: (id) => null,
  querySelector: () => null,
  querySelectorAll: () => [],
  addEventListener: () => {},
  removeEventListener: () => {},
  body: new MockElement('body')
};

const sandbox = {
  Node: { ELEMENT_NODE: 1, TEXT_NODE: 3 },
  navigator: { clipboard: { writeText: () => Promise.resolve() } },
  console,
  setTimeout: () => {},
  clearTimeout: () => {},
  setInterval: () => {},
  clearInterval: () => {},
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  document: mockDoc,
  addEventListener: () => {},
  removeEventListener: () => {},
  __lastLoadedNote: null,
  loadNote: function(id) { sandbox.__lastLoadedNote = id; }
};
sandbox.window = sandbox;
sandbox.global = sandbox;

vm.runInNewContext(appCode, sandbox);

// Exact code from test_defect_unsync_block_instance_is_shadowed_by_legacy_function:
const unsyncFn = sandbox.unsyncBlockInstance;
assert(unsyncFn, 'unsyncBlockInstance debe estar definido en sandbox/window');
const fnStr = unsyncFn.toString();

assert(fnStr.includes('convertBlockType'),
  'DEFECT CONFIRMED: unsyncBlockInstance no invoca convertBlockType porque fue sobrescrita por la función legacy de la línea 15498. Código activo: ' + fnStr
);

console.log('UNSYNC_CONTRACT_VALID');
