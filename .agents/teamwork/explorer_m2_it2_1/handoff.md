# Handoff Report — Milestone 2 Iteration 2 Remediation (Defect 1)

**Agent**: `explorer_m2_it2_1` (Explorer Subagent)  
**Roles**: investigator, explorer, synthesist  
**Focus Area**: Defect 1 — `unsyncBlockInstance` is shadowed by legacy function (Dead Code)  
**Parent**: `4ad26d22-329a-498b-97c2-c4b62703d7bb`  
**Working Directory**: `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\explorer_m2_it2_1`  
**Timestamp**: 2026-11-02T14:55:00Z  

---

## 1. Observation

### 1.1 Direct Conflict at Line 7666 vs Line 15498 in `frontend/app.js`
In `frontend/app.js`, two duplicate top-level function declarations named `unsyncBlockInstance` exist:

- **Milestone 2 Canonical Declaration (lines 7666–7675)**:
  ```javascript
  7666:     function unsyncBlockInstance(referenceElOrBtn) {
  7667:       const refEl = (referenceElOrBtn && referenceElOrBtn.closest) ? referenceElOrBtn.closest('.block-transclusion-reference, .notion-synced-block') : null;
  7668:       if (!refEl) return;
  7669:       const blockId = refEl.getAttribute('data-block-id');
  7670:       if (blockId && typeof convertBlockType === 'function') {
  7671:         convertBlockType(blockId, 'text');
  7672:         if (typeof showToast === 'function') showToast('Bloque desvinculado (convertido a texto)', '✂️');
  7673:       }
  7674:     }
  7675:     window.unsyncBlockInstance = unsyncBlockInstance;
  ```

- **Legacy Declaration (lines 15498–15507)**:
  ```javascript
  15498:     function unsyncBlockInstance(btnEl) {
  15499:       const block = btnEl ? btnEl.closest('.notion-synced-block') : null;
  15500:       if (!block) return;
  15501:       const bodyEl = block.querySelector('.notion-synced-body');
  15502:       const wrapper = document.createElement('div');
  15503:       wrapper.innerHTML = bodyEl ? bodyEl.innerHTML : '';
  15504:       block.replaceWith(...Array.from(wrapper.childNodes));
  15505:       syncRichEditor();
  15506:       showToast('Bloque desvinculado y convertido en texto independiente', '🔓');
  15507:     }
  ```

### 1.2 Verbatim Adversarial Test Failure
Running `py -m unittest tests/test_milestone2_adversarial_challenge.py -k test_defect_unsync_block_instance_is_shadowed_by_legacy_function` reproduces the exact defect failure:
```text
AssertionError [ERR_ASSERTION]: DEFECT CONFIRMED: unsyncBlockInstance no invoca convertBlockType porque fue sobrescrita por la función legacy de la línea 15498. Código activo: function unsyncBlockInstance(btnEl) {
      const block = btnEl ? btnEl.closest('.notion-synced-block') : null;
      if (!block) return;
      const bodyEl = block.querySelector('.notion-synced-body');
      const wrapper = document.createElement('div');
      wrapper.innerHTML = bodyEl ? bodyEl.innerHTML : '';
      block.replaceWith(...Array.from(wrapper.childNodes));
      syncRichEditor();
      showToast('Bloque desvinculado y convertido en texto independiente', '🔓');
    }
```

### 1.3 Empirical Scan for Duplicate Identifiers across `frontend/app.js`
An AST/regex scan of all 18,523 lines in `frontend/app.js` revealed **EXACTLY TWO** duplicate function declarations in the entire codebase:
1. `unsyncBlockInstance`: line 7666 vs line 15498 (count = 2)
2. `copySyncedBlockReference`: line 7655 vs line 15479 (count = 2)

Both occur between the Milestone 2 block engine (lines 7655–7675) and the pre-M2 legacy HTML-string synced block section (lines 15479–15507). Because JavaScript hoists function declarations to script scope, the second declaration overwrites the first throughout execution, making the M2 implementations unreachable dead code.

### 1.4 Headless Harness Incompatibilities in Current Line 7666
Even if hoisting were not present, line 7666 exhibited two significant weaknesses identified by Challenger 2:
1. **Parameter Fragility (`null !== 'tr-ref-1'`)**: Line 7667 called `(referenceElOrBtn && referenceElOrBtn.closest)`. If invoked with a string identifier `unsyncBlockInstance('tr-ref-1')` (common in headless unit tests or automation scripts), `referenceElOrBtn.closest` is `undefined`, `refEl` becomes `null`, and line 7668 aborts immediately without converting anything.
2. **Lexical Bypass of Window Mocks**: Line 7670 invoked `convertBlockType(blockId, 'text')` using a bare lexical identifier. In headless Node.js VM tests where `sandbox.convertBlockType` or `window.convertBlockType` is mocked or spied on, the unqualified lexical call ignores the window mock. Furthermore, `window.convertBlockType = convertBlockType` was never exported at line 6830.

---

## 2. Logic Chain

1. **JavaScript Scoping and Hoisting Mechanics**:
   - `frontend/app.js` is evaluated as a global script file in browser and test VM environments.
   - During compilation/parsing, all `function <name>` declarations are hoisted to the top of the enclosing script scope.
   - When duplicate function declarations share the same identifier (`unsyncBlockInstance`), the latter declaration (line 15498) supersedes the former (line 7666).
   - Even though line 7675 writes `window.unsyncBlockInstance = unsyncBlockInstance;`, the lexical identifier `unsyncBlockInstance` is already bound to the legacy function from line 15498.

2. **Impact on Data Model and UX**:
   - The legacy function performs raw DOM element replacement via `block.replaceWith(...Array.from(wrapper.childNodes))` without calling `convertBlockType` or updating `state.activeRecordMap` or persisting to SQLite via `persistBlockUpdate`.
   - If `.notion-synced-body` is empty, the legacy function replaces the block with zero nodes, permanently deleting the block from the DOM without recording the change in backend models.

3. **Remediation Strategy**:
   - **Step 1: Clean up line 15498**. Eliminate `function unsyncBlockInstance(btnEl)` from line 15498 so that JS function hoisting no longer overwrites line 7666. Also clean up sibling duplicate `copySyncedBlockReference` at line 15479.
   - **Step 2: Polymorphic parameter resolution at line 7666**. Support both string block IDs (`typeof referenceElOrBtn === 'string'`) and DOM elements (`referenceElOrBtn.closest` or `referenceElOrBtn.getAttribute`).
   - **Step 3: Converter & Toast resolution**. Resolve converter via `(typeof window !== 'undefined' && typeof window.convertBlockType === 'function' ? window.convertBlockType : (typeof convertBlockType === 'function' ? convertBlockType : null))`. Resolve toast via `window.showToast || showToast`.
   - **Step 4: Graceful fallback for legacy blocks**. If `refEl` is an older legacy synced block without `data-block-id`, provide safe fallback unwrapping and preserve legacy toast (`'Bloque desvinculado y convertido en texto independiente'`, `'🔓'`).
   - **Step 5: Export `window.convertBlockType`**. Export `window.convertBlockType = convertBlockType` at line 6831 and ensure `convertBlockType` can accept either a string ID or element.

---

## 3. Caveats

- **Scope Boundary**: This report focuses strictly on Defect 1 (`unsyncBlockInstance` shadowing and headless harness compatibility). Defect 2 (`targetBlock.alive !== 0` check in `renderTreeFromRecordMap`) and Defect 3 (`visited` Set multi-reference starvation) reside in lines 7592–7640 and are addressed in their respective work items.
- **Backward Compatibility**: Notes created under legacy Note-JS versions containing `<div class="notion-synced-block" data-synced-id="...">` remain fully functional because the unified `unsyncBlockInstance` falls back to unwrapping if no `data-block-id` is found.

---

## 4. Conclusion & Patch Specification

### Concrete Patch Specification for the Worker

#### Patch 1: Export `window.convertBlockType` and support polymorphic lookup in `convertBlockType`
**File**: `frontend/app.js`, around line 6772 & line 6830

```javascript
<<<< BEFORE (lines 6772-6775)
    function convertBlockType(blockId, newType) {
      const blockEl = document.querySelector(`[data-block-id="${blockId}"]`);
      if (!blockEl) return;
====
>>>> AFTER
    function convertBlockType(blockIdOrEl, newType) {
      let blockEl = null;
      let blockId = null;

      if (typeof blockIdOrEl === 'string') {
        blockId = blockIdOrEl;
        if (typeof document !== 'undefined' && document.querySelector) {
          blockEl = document.querySelector(`[data-block-id="${blockId}"]`) || document.getElementById(blockId);
        }
      } else if (blockIdOrEl && (blockIdOrEl.nodeType === 1 || blockIdOrEl.getAttribute)) {
        blockEl = (typeof blockIdOrEl.closest === 'function')
          ? (blockIdOrEl.closest('[data-block-id], .notion-block') || blockIdOrEl)
          : blockIdOrEl;
        blockId = (blockEl.getAttribute && (blockEl.getAttribute('data-block-id') || blockEl.id)) ||
                  (blockEl.dataset && blockEl.dataset.blockId) || null;
      }
      if (!blockEl && blockId && typeof document !== 'undefined' && document.querySelector) {
        blockEl = document.querySelector(`[data-block-id="${blockId}"]`) || document.getElementById(blockId);
      }
      if (!blockEl) return;
```

```javascript
<<<< BEFORE (line 6830)
      syncRichEditor();
    }

    function renderBlock(block) {
====
>>>> AFTER
      syncRichEditor();
    }
    window.convertBlockType = convertBlockType;

    function renderBlock(block) {
```

---

#### Patch 2: Modern, Polymorphic `unsyncBlockInstance` (and unified `copySyncedBlockReference`)
**File**: `frontend/app.js`, around lines 7655–7676

```javascript
<<<< BEFORE (lines 7655-7676)
    function copySyncedBlockReference(blockId) {
      if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(String(blockId)).then(() => {
          if (typeof showToast === 'function') showToast('Referencia de bloque copiada al portapapeles', '🔗');
        }).catch(() => {});
      } else if (typeof showToast === 'function') {
        showToast('Referencia: ' + String(blockId), '🔗');
      }
    }
    window.copySyncedBlockReference = copySyncedBlockReference;

    function unsyncBlockInstance(referenceElOrBtn) {
      const refEl = (referenceElOrBtn && referenceElOrBtn.closest) ? referenceElOrBtn.closest('.block-transclusion-reference, .notion-synced-block') : null;
      if (!refEl) return;
      const blockId = refEl.getAttribute('data-block-id');
      if (blockId && typeof convertBlockType === 'function') {
        convertBlockType(blockId, 'text');
        if (typeof showToast === 'function') showToast('Bloque desvinculado (convertido a texto)', '✂️');
      }
    }
    window.unsyncBlockInstance = unsyncBlockInstance;
====
>>>> AFTER
    function copySyncedBlockReference(blockIdOrSyncId) {
      const idStr = String(blockIdOrSyncId || '');
      if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(idStr).then(() => {
          if (typeof showToast === 'function') showToast('Referencia de bloque copiada al portapapeles', '🔗');
        }).catch(() => {});
      } else if (typeof showToast === 'function') {
        showToast('Referencia: ' + idStr, '🔗');
      }

      // Compatibilidad con buffer legacy si existe elemento con data-synced-id
      if (typeof document !== 'undefined') {
        const editor = document.getElementById('rich-editor-canvas');
        const sourceBlock = editor ? editor.querySelector(`.notion-synced-block[data-synced-id="${idStr}"]`) : null;
        if (sourceBlock) {
          const bodyEl = sourceBlock.querySelector('.notion-synced-body');
          copiedSyncedBlockBuffer = {
            syncId: idStr,
            html: bodyEl ? bodyEl.innerHTML : '<p>Contenido sincronizado...</p>'
          };
        }
      }
    }
    window.copySyncedBlockReference = copySyncedBlockReference;

    function unsyncBlockInstance(referenceElOrBtn) {
      let refEl = null;
      let blockId = null;

      if (typeof referenceElOrBtn === 'string') {
        blockId = referenceElOrBtn;
        if (typeof document !== 'undefined' && document.querySelector) {
          refEl = document.querySelector(`[data-block-id="${blockId}"]`) || document.getElementById(blockId);
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
    window.unsyncBlockInstance = unsyncBlockInstance;
```

---

#### Patch 3: Clean up legacy declarations at line 15479 & 15498
**File**: `frontend/app.js`, lines 15479–15507

```javascript
<<<< BEFORE (lines 15479-15507)
    function copySyncedBlockReference(syncId) {
      const editor = document.getElementById('rich-editor-canvas');
      const sourceBlock = editor ? editor.querySelector(`.notion-synced-block[data-synced-id="${syncId}"]`) : null;
      const bodyEl = sourceBlock ? sourceBlock.querySelector('.notion-synced-body') : null;
      copiedSyncedBlockBuffer = {
        syncId,
        html: bodyEl ? bodyEl.innerHTML : '<p>Contenido sincronizado...</p>'
      };
      showToast('Referencia sincronizada copiada. Usa el menú de bloque o Ctrl+Shift+V para pegarla en cualquier nota', '🔗');
    }

    function pasteCopiedSyncedBlock() {
      if (!copiedSyncedBlockBuffer) {
        showToast('Primero copia una referencia desde un Bloque Sincronizado', 'ℹ️');
        return;
      }
      insertSyncedBlock(copiedSyncedBlockBuffer.syncId, copiedSyncedBlockBuffer.html);
    }

    function unsyncBlockInstance(btnEl) {
      const block = btnEl ? btnEl.closest('.notion-synced-block') : null;
      if (!block) return;
      const bodyEl = block.querySelector('.notion-synced-body');
      const wrapper = document.createElement('div');
      wrapper.innerHTML = bodyEl ? bodyEl.innerHTML : '';
      block.replaceWith(...Array.from(wrapper.childNodes));
      syncRichEditor();
      showToast('Bloque desvinculado y convertido en texto independiente', '🔓');
    }
====
>>>> AFTER
    // Nota: copySyncedBlockReference legacy unificado en window.copySyncedBlockReference (línea 7655)
    function pasteCopiedSyncedBlock() {
      if (!copiedSyncedBlockBuffer) {
        showToast('Primero copia una referencia desde un Bloque Sincronizado', 'ℹ️');
        return;
      }
      insertSyncedBlock(copiedSyncedBlockBuffer.syncId, copiedSyncedBlockBuffer.html);
    }

    // Nota: unsyncBlockInstance legacy unificado en window.unsyncBlockInstance (línea 7666)
```

---

## 5. Verification Method

### 5.1 Independent Reproduction
Verify current failure prior to applying patch:
```powershell
py -m unittest tests/test_milestone2_adversarial_challenge.py -k test_defect_unsync_block_instance_is_shadowed_by_legacy_function
```
*Current output*: `AssertionError: DEFECT CONFIRMED: unsyncBlockInstance no invoca convertBlockType porque fue sobrescrita por la función legacy de la línea 15498.`

### 5.2 Verification of Proposed Patch
A standalone test runner `.agents/teamwork/explorer_m2_it2_1/test_adversarial_defect1_sim.js` was created and executed in Node.js VM:
```powershell
node .agents\teamwork\explorer_m2_it2_1\test_adversarial_defect1_sim.js
```
*Result*: `UNSYNC_CONTRACT_VALID` with 100% success across all 4 verification vectors:
1. `sandbox.unsyncBlockInstance.toString().includes('convertBlockType') === true`
2. Invocation with string ID `unsyncBlockInstance('test-str-id')` invokes `convertBlockType('test-str-id', 'text')` and fires toast `'✂️'`.
3. Invocation with DOM Element `unsyncBlockInstance(el)` invokes `convertBlockType('test-el-id', 'text')` and fires toast `'✂️'`.
4. Overriding `window.convertBlockType` is respected by `unsyncBlockInstance`.

### 5.3 Invalidation Conditions
- Any occurrence of `function unsyncBlockInstance` remaining in `frontend/app.js` other than the single canonical declaration at line 7666 will invalidate this fix due to JavaScript function declaration hoisting.
- Failure to check `window.convertBlockType` will cause failures in test harnesses that stub `convertBlockType` on the global object.
