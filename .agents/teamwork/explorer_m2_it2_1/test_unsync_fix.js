const fs = require('fs');
const vm = require('vm');
const path = require('path');
const assert = require('assert');

const appPath = path.resolve(__dirname, '../../../frontend/app.js');
let appCode = fs.readFileSync(appPath, 'utf8');

// 1. Export window.convertBlockType after convertBlockType definition
appCode = appCode.replace(
  'syncRichEditor();\n    }\n\n    function renderBlock(block) {',
  'syncRichEditor();\n    }\n    window.convertBlockType = convertBlockType;\n\n    function renderBlock(block) {'
);

// 2. Update unsyncBlockInstance at line 7666
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

assert(appCode.includes(oldUnsyncM2), 'oldUnsyncM2 snippet must match exact text in app.js');
appCode = appCode.replace(oldUnsyncM2, newUnsyncM2);

// 3. Clean up legacy declaration at line 15498
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

assert(appCode.includes(oldLegacyUnsync), 'oldLegacyUnsync snippet must match exact text in app.js');
appCode = appCode.replace(oldLegacyUnsync, '    // Legacy unsyncBlockInstance unificado en la declaración canónica de la línea 7666');

// Setup mock sandbox
class MockElement {
  constructor(tag) {
    this.tagName = tag.toUpperCase();
    this.attributes = {};
    this.children = [];
    this.parentNode = null;
    this.innerHTML = '';
    this.classList = {
      add: () => {},
      remove: () => {},
      contains: () => false
    };
  }
  setAttribute(k, v) { this.attributes[k] = String(v); }
  getAttribute(k) { return this.attributes[k] || null; }
  appendChild(c) { c.parentNode = this; this.children.push(c); return c; }
  querySelector() { return null; }
  querySelectorAll() { return []; }
  closest() { return this; }
}

const mockDoc = {
  createElement: (tag) => new MockElement(tag),
  getElementById: () => null,
  querySelector: () => null,
  querySelectorAll: () => [],
  addEventListener: () => {},
  removeEventListener: () => {},
  body: new MockElement('body')
};

let lastToast = null;
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
  loadNote: function(id) { sandbox.__lastLoadedNote = id; },
  showToast: function(msg, icon) { lastToast = { msg, icon }; }
};
sandbox.window = sandbox;
sandbox.global = sandbox;

vm.runInNewContext(appCode, sandbox);

// Explicitly test window.showToast override
sandbox.window.showToast = function(msg, icon) { lastToast = { msg, icon }; };

// Verification 1: fn string contains convertBlockType
const unsyncFn = sandbox.unsyncBlockInstance;
assert(unsyncFn, 'unsyncBlockInstance debe estar definido en sandbox/window');
const fnStr = unsyncFn.toString();
assert(fnStr.includes('convertBlockType'), 'DEFECT 1 RESOLVED: unsyncBlockInstance contiene convertBlockType');

// Verification 2: string ID invocation
let convertCalls = [];
sandbox.convertBlockType = (id, type) => { convertCalls.push({ id, type }); };
sandbox.unsyncBlockInstance('test-str-id');
assert.strictEqual(convertCalls.length, 1);
assert.deepStrictEqual(convertCalls[0], { id: 'test-str-id', type: 'text' });
assert.deepStrictEqual(lastToast, { msg: 'Bloque desvinculado (convertido a texto)', icon: '✂️' });

// Verification 3: DOM Element invocation
convertCalls = [];
const el = new MockElement('div');
el.setAttribute('data-block-id', 'test-el-id');
sandbox.unsyncBlockInstance(el);
assert.strictEqual(convertCalls.length, 1);
assert.deepStrictEqual(convertCalls[0], { id: 'test-el-id', type: 'text' });
assert.deepStrictEqual(lastToast, { msg: 'Bloque desvinculado (convertido a texto)', icon: '✂️' });

// Verification 4: window.convertBlockType override works
convertCalls = [];
sandbox.window.convertBlockType = (id, type) => { convertCalls.push({ id, type, overridden: true }); };
sandbox.unsyncBlockInstance('test-override-id');
assert.strictEqual(convertCalls.length, 1);
assert.deepStrictEqual(convertCalls[0], { id: 'test-override-id', type: 'text', overridden: true });

console.log('SUCCESS: All 4 verification tests passed flawlessly!');
