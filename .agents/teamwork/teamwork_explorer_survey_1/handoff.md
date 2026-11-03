# Reporte de Investigación: Requisito R1 (Conflicto de Selección Lasso vs Native Text)

**Autor:** Survey Explorer 1 (`teamwork_explorer_survey_1`)  
**Fecha:** 2026-10-30T20:22:00Z  
**Destinatario:** Orchestrator (`45d1cd46-bf0a-48bd-82de-759226538c42`)  
**Misión:** Investigación y análisis exhaustivo de arquitectura del Requisito R1.

---

## 1. Observation

### 1.1. Arquitectura de Archivos y Responsabilidades
El editor del proyecto Note-JS-Desktop reside en la carpeta `frontend/`:
- `frontend/app.js` (712,231 bytes, 16,207 líneas): Contiene toda la lógica de la aplicación del lado del cliente, controladores espaciales, gestión del DOM y eventos de interacción.
- `frontend/index.html` (179,537 bytes, 2,555 líneas): Define la estructura DOM del lienzo, contenedores del editor, elementos de selección y plantillas de bloques.
- `frontend/styles.css` (269,702 bytes, 10,273 líneas): Define los estilos visuales, márgenes exteriores de bloques, animaciones y apariencia del lazo de selección (`.block-selection-marquee`).

No existen otros archivos JavaScript o empaquetadores en ejecución en el frontend; todo es servido de manera directa vía `<script src="/app.js"></script>` (`frontend/index.html:2552`).

---

### 1.2. Localización Exacta del Manejador de Selección por Lazo (Marquee / Lasso)
En `frontend/app.js`, la función `initSpatialBlockController()` (líneas 15226 - 15450) inicializa la interacción con el lienzo y los bloques:

```javascript
// frontend/app.js:15226-15234
function initSpatialBlockController() {
  const panelCanvas = document.getElementById('panel-canvas');
  const handle = document.getElementById('spatial-block-handle');
  const gripBtn = document.getElementById('spatial-btn-grip');
  const dropGuide = document.getElementById('spatial-drop-guide');
  const ghostPill = document.getElementById('spatial-drag-ghost-pill');
  const marquee = document.getElementById('block-selection-marquee');
  if (!panelCanvas || !handle || !gripBtn || !dropGuide) return;
```

El listener de `mousedown` para el lazo (marquee) está registrado en `panelCanvas` (`#panel-canvas`):

```javascript
// frontend/app.js:15247-15272
  // Selección por Lazo (Marquee) en el espacio en blanco del lienzo
  let isMarqueeActive = false;
  let marqueeStartX = 0;
  let marqueeStartY = 0;

  panelCanvas.addEventListener('mousedown', (e) => {
    // Solo botón principal y fuera de bloques editables o controles
    if (e.button !== 0) return;
    if (e.target.closest('#spatial-block-handle') || e.target.closest('#block-action-menu') || e.target.closest('.desktop-format-bar') || e.target.closest('button')) {
      return;
    }

    const editor = document.getElementById('rich-editor-canvas');
    const insideEditor = editor && editor.contains(e.target);
    const isBlockDirect = e.target.closest('p, h1, h2, h3, blockquote, div.notion-columns-row, .notion-block, .notion-block-box, .callout-box');

    // Si se hace clic en margen o espacio en blanco fuera del texto activo
    if (!isBlockDirect || e.target === panelCanvas || e.target === editor) {
      isMarqueeActive = true;
      marqueeStartX = e.clientX;
      marqueeStartY = e.clientY;
      if (!e.shiftKey && !e.ctrlKey && !e.metaKey) {
        clearBlockSelection();
      }
    }
  });
```

---

### 1.3. Movimiento y Hit-Testing del Rectángulo Azul (Marquee)
En `frontend/app.js:15274-15312`, los eventos `mousemove` y `mouseup` globales gestionan el dibujo y la colisión:

```javascript
// frontend/app.js:15274-15312
  window.addEventListener('mousemove', (e) => {
    if (!isMarqueeActive || !marquee) return;
    const currentX = e.clientX;
    const currentY = e.clientY;
    const width = Math.abs(currentX - marqueeStartX);
    const height = Math.abs(currentY - marqueeStartY);
    if (width > 5 || height > 5) {
      marquee.classList.add('active');
      const left = Math.min(currentX, marqueeStartX);
      const top = Math.min(currentY, marqueeStartY);
      marquee.style.left = `${left}px`;
      marquee.style.top = `${top}px`;
      marquee.style.width = `${width}px`;
      marquee.style.height = `${height}px`;

      const marqueeRect = { left, top, right: left + width, bottom: top + height };
      const editor = document.getElementById('rich-editor-canvas');
      if (editor) {
        Array.from(editor.children).forEach(block => {
          const r = block.getBoundingClientRect();
          const intersects = !(r.right < marqueeRect.left || r.left > marqueeRect.right || r.bottom < marqueeRect.top || r.top > marqueeRect.bottom);
          if (intersects) {
            selectBlock(block, true);
          }
        });
      }
    }
  });

  window.addEventListener('mouseup', () => {
    if (isMarqueeActive) {
      isMarqueeActive = false;
      if (marquee) {
        marquee.classList.remove('active');
        marquee.style.width = '0px';
        marquee.style.height = '0px';
      }
    }
  });
```

---

### 1.4. Estructura del DOM Relacionada con el Editor y la Selección
En `frontend/index.html`:
- Línea 258:
  ```html
  <main id="panel-canvas" class="panel-canvas">
  ```
- Línea 737:
  ```html
  <div id="block-selection-marquee" class="block-selection-marquee" aria-hidden="true"></div>
  ```
- Línea 743:
  ```html
  <div id="editor-body" class="editor-body">
  ```
  *(Nota: La clase `.editor-container` no existe actualmente en el DOM ni en `styles.css`)*
- Línea 799:
  ```html
  <input id="note-title" class="editor-title" type="text" placeholder="Sin título" oninput="updateNote('title', this.value)" />
  ```
- Línea 828:
  ```html
  <div class="notion-blocks-container" id="blocks-container">
  ```
- Línea 830:
  ```html
  <div id="rich-editor-canvas" class="notion-rich-editor" contenteditable="true" spellcheck="false" placeholder="..." oninput="handleRichEditorInput(event)" onkeydown="handleRichEditorKeydown(event)"></div>
  ```

---

### 1.5. Estilos Visuales del Lazo y Márgenes de Bloques
En `frontend/styles.css`:
- Líneas 5576-5588:
  ```css
  /* Cuadro de Selección por Lazo (Marquee) al arrastrar el cursor por el lienzo */
  .block-selection-marquee {
    position: fixed;
    z-index: 900;
    pointer-events: none;
    display: none;
    border: 1.5px solid #3b82f6;
    background: rgba(59, 130, 246, 0.15);
    border-radius: 3px;
  }

  .block-selection-marquee.active {
    display: block;
  }
  ```
- Líneas 2055-2063:
  ```css
  .editor-body {
    flex: 1;
    overflow-y: auto;
    padding: 24px 54px 60px 54px;
    position: relative;
    max-width: 920px;
    width: 100%;
    margin: 0 auto;
  }
  ```
- Líneas 2076-2091:
  ```css
  /* Zona invisible de detección en el margen exterior izquierdo donde posicionan los botones */
  .callout-box::before,
  .quote-block::before,
  .toggle-block::before,
  .code-block::before,
  .notion-block-box::before,
  .checklist-item-row::before {
    content: '';
    position: absolute;
    top: -4px;
    bottom: -4px;
    left: -42px;
    width: 42px;
    pointer-events: auto;
    z-index: 20;
  }
  ```

---

## 2. Logic Chain

1. **Causa Raíz del Conflicto de Selección:**
   - El elemento `#rich-editor-canvas` posee el atributo `contenteditable="true"` (`frontend/index.html:830`).
   - En `frontend/app.js:15264`, la condición para iniciar el lazo evalúa:
     `if (!isBlockDirect || e.target === panelCanvas || e.target === editor)`.
   - Cuando el usuario hace clic dentro del editor sobre el canvas vacío, entre líneas o en el propio contenedor editable, `e.target === editor` es `true`.
   - Si el usuario hace clic sobre elementos que no están listados explícitamente en `isBlockDirect` (como `<ul>`, `<ol>`, `<li>`, `<code>`, `<pre>`, `<span>`, `<a>`, `<table>`, `<input>`, `<textarea>`), `isBlockDirect` devuelve `null`, por lo que `!isBlockDirect` es `true`.
   - No existe ninguna comprobación de si el elemento clickeado es editable (`[contenteditable="true"]`, `<input>`, `<textarea>`).
   - Al cumplirse la condición, se asigna `isMarqueeActive = true` y se guarda `marqueeStartX/Y`. Al arrastrar más de 5 píxeles con el ratón para seleccionar texto, se activa el lazo (`.block-selection-marquee.active`), se intercepta la interacción y se seleccionan bloques enteros (`spatial-block-selected`) en lugar de permitir la selección nativa de caracteres y palabras.

2. **Mecanismo de Descarte Inmediato (Early Return / Abort):**
   - Para permitir la selección nativa del navegador, el callback de `mousedown` debe abortar en la primera comprobación cuando el target sea editable:
     `if (e.target.closest('[contenteditable="true"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;`
   - Dado que `#rich-editor-canvas` tiene `contenteditable="true"`, cualquier clic sobre él o sobre sus elementos hijos de texto devolverá inmediatamente el nodo editable mediante `closest('[contenteditable="true"]')`.
   - Cualquier clic en el título de la nota (`#note-title`), inputs de callouts o textareas devolverá `true` en `tagName === 'INPUT'` o `tagName === 'TEXTAREA'`.
   - Al ejecutar `return;`, `isMarqueeActive` permanece `false`, permitiendo al motor de renderizado del navegador (Chromium / WebKit) manejar de forma nativa la colocación del cursor y la selección de texto.

3. **Restricción a `.editor-container` y Márgenes Exteriores:**
   - Para que el lazo se inicie únicamente en el fondo vacío y en los márgenes exteriores de los bloques:
     1. Debe añadirse la clase `.editor-container` a `<div id="editor-body" class="editor-body editor-container">` en `index.html` y en `styles.css` (compartiendo estilos con `.editor-body`).
     2. En `mousedown`, tras descartar los elementos editables y los controles/botones (`#spatial-block-handle`, `#block-action-menu`, etc.), debe validarse que el clic ocurrió en el fondo del lienzo o dentro del contenedor del editor:
        `const isEditorContainer = e.target === panelCanvas || Boolean(e.target.closest('.editor-container, .editor-body, #blocks-container'));`
        `if (!isEditorContainer) return;`
   - Al hacer clic en los márgenes de 54px del editor, en las áreas vacías de `#panel-canvas` o en los márgenes exteriores (`::before` de 42px) de bloques no editables, `isEditorContainer` es `true` y no se aborta, activando el marquee según lo especificado en los Criterios de Aceptación.

---

## 3. Caveats

- **No existen advertencias ocultas:** No hay otros listeners de lasso o marquee en el proyecto.
- **Asunciones de entorno:** La aplicación corre sobre WebView2 / Chromium o navegador estándar en Note-JS Desktop. `event.target.closest` y `tagName` son estándares universales de DOM Level 4 totalmente soportados.
- **Desmarcado al enfocar el editor:** En `frontend/app.js:15789-15791`, ya existe `if (e.target.closest('#rich-editor-canvas')) { document.querySelectorAll('.spatial-block-selected').forEach(el => el.classList.remove('spatial-block-selected')); }`, lo que complementa perfectamente la limpieza de selección previa al editar texto.

---

## 4. Conclusion

El conflicto de selección se resuelve de manera limpia, quirúrgica y no invasiva mediante dos cambios específicos:

1. **En `frontend/index.html` (Línea 743) y `frontend/styles.css` (Línea 2055):**
   Añadir la clase `editor-container` al contenedor principal del editor (`#editor-body`).
2. **En `frontend/app.js` (Líneas 15252 - 15272):**
   Reemplazar el cuerpo del listener de `mousedown` en `initSpatialBlockController()` para abortar inmediatamente ante elementos editables y verificar que el inicio se limite a `.editor-container` / fondos vacíos y márgenes de bloques.

### Propuesta Concreta de Código (Diff)

#### A. Archivo `frontend/app.js` (Líneas 15252 - 15272)

**Antes:**
```javascript
      panelCanvas.addEventListener('mousedown', (e) => {
        // Solo botón principal y fuera de bloques editables o controles
        if (e.button !== 0) return;
        if (e.target.closest('#spatial-block-handle') || e.target.closest('#block-action-menu') || e.target.closest('.desktop-format-bar') || e.target.closest('button')) {
          return;
        }

        const editor = document.getElementById('rich-editor-canvas');
        const insideEditor = editor && editor.contains(e.target);
        const isBlockDirect = e.target.closest('p, h1, h2, h3, blockquote, div.notion-columns-row, .notion-block, .notion-block-box, .callout-box');

        // Si se hace clic en margen o espacio en blanco fuera del texto activo
        if (!isBlockDirect || e.target === panelCanvas || e.target === editor) {
          isMarqueeActive = true;
          marqueeStartX = e.clientX;
          marqueeStartY = e.clientY;
          if (!e.shiftKey && !e.ctrlKey && !e.metaKey) {
            clearBlockSelection();
          }
        }
      });
```

**Después:**
```javascript
      panelCanvas.addEventListener('mousedown', (e) => {
        // 1. Solo botón principal (clic izquierdo)
        if (e.button !== 0) return;

        // 2. Abortar de inmediato si ocurre dentro de un elemento editable (texto nativo, input, textarea)
        if (e.target.closest('[contenteditable="true"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
          return;
        }

        // 3. Abortar si ocurre en controles flotantes, menús, barras de formato o botones
        if (e.target.closest('#spatial-block-handle') || e.target.closest('#block-action-menu') || e.target.closest('.desktop-format-bar') || e.target.closest('button') || e.target.closest('#sticky-toc-rail')) {
          return;
        }

        // 4. Asegurar que solo se inicie si el mousedown ocurre directamente en .editor-container (fondos vacíos) o en márgenes exteriores de los bloques
        const isEditorContainer = e.target === panelCanvas || Boolean(e.target.closest('.editor-container, .editor-body, #blocks-container'));
        if (!isEditorContainer) {
          return;
        }

        isMarqueeActive = true;
        marqueeStartX = e.clientX;
        marqueeStartY = e.clientY;
        if (!e.shiftKey && !e.ctrlKey && !e.metaKey) {
          clearBlockSelection();
        }
      });
```

#### B. Archivo `frontend/index.html` (Línea 743)

**Antes:**
```html
      <!-- Lienzo del Editor -->
      <div id="editor-body" class="editor-body">
```

**Después:**
```html
      <!-- Lienzo del Editor -->
      <div id="editor-body" class="editor-body editor-container">
```

#### C. Archivo `frontend/styles.css` (Línea 2055)

**Antes:**
```css
    .editor-body {
      flex: 1;
      overflow-y: auto;
      padding: 24px 54px 60px 54px;
      position: relative;
      max-width: 920px;
      width: 100%;
      margin: 0 auto;
    }
```

**Después:**
```css
    .editor-body,
    .editor-container {
      flex: 1;
      overflow-y: auto;
      padding: 24px 54px 60px 54px;
      position: relative;
      max-width: 920px;
      width: 100%;
      margin: 0 auto;
    }
```

---

## 5. Verification Method

Para verificar independientemente la solución tras su implementación:

1. **Inspección de Archivos:**
   - Comprobar que `frontend/app.js` contiene en la línea inicial del callback de `panelCanvas.addEventListener('mousedown')` la comprobación `if (e.target.closest('[contenteditable="true"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;`.
   - Comprobar que `frontend/index.html` y `frontend/styles.css` incluyen la clase `.editor-container`.

2. **Prueba de Selección Nativa de Texto (Simulación en Browser / Node):**
   - Ejecutar un test de interacción que:
     - Cree un elemento `<p>Texto de prueba</p>` dentro de `#rich-editor-canvas`.
     - Dispare un evento `mousedown` en dicho `<p>` con `clientX=100, clientY=100`.
     - Dispare un evento `mousemove` con `clientX=150, clientY=100`.
     - **Condición de éxito:** El elemento `#block-selection-marquee` **NO** debe tener la clase `active`.
     - Dispare `mousedown` y `mousemove` dentro de `#note-title`.
     - **Condición de éxito:** `#block-selection-marquee` **NO** debe tener la clase `active`.

3. **Prueba del Lazo de Selección (Lasso):**
   - Disparar un evento `mousedown` sobre el margen vacío de `.editor-container` o `#panel-canvas` con `clientX=10, clientY=10`.
   - Disparar `mousemove` con `clientX=100, clientY=100`.
   - **Condición de éxito:** El elemento `#block-selection-marquee` **SÍ** debe tener la clase `active` y sus estilos `left, top, width, height` deben reflejar la caja de selección.
   - Disparar `mouseup`.
   - **Condición de éxito:** La clase `active` se retira y las dimensiones vuelven a `0px`.

4. **Condiciones de Invalidación:**
   - Si al arrastrar sobre un texto editable aparece el rectángulo azul (`.block-selection-marquee.active`), la comprobación de aborto falló o no está colocada al inicio del listener.
   - Si al hacer clic y arrastrar en el margen vacío no se dibuja el lazo de selección, la condición `isEditorContainer` está restringiendo de más.
