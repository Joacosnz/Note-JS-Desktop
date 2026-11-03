# Note JS — Aplicación de Notas Profesional para PC

**Note JS** es una aplicación de notas y productividad para escritorio (PC con Windows, Linux y macOS), inspirada en la elegancia visual de **Apple Notes** y la potencia de bloques de **Notion**.

El proyecto ha sido completamente migrado y optimizado para **PC**, utilizando **Python** en el backend con almacenamiento relacional **SQLite + Peewee ORM**, una ventana nativa de escritorio ultraligera mediante **PyWebView** (sin el consumo excesivo de memoria de Electron), y un frontend rápido y reactivo en **JavaScript Vanilla (ES6+), HTML5 y CSS3**.

---

## 🚀 Características Principales

1. **Gestor de Carpetas y Subcarpetas Jerárquicas**:
   - Soporte para subcarpetas anidadas con niveles ilimitados.
   - Reorganización mediante **Drag & Drop** (arrastrar una carpeta sobre otra para convertirla en subcarpeta o promoverla a la raíz).
   - Animación visual fluida de indentación y estado de soltado.
   - Asignación de emojis personalizados a cualquier carpeta.
   - Todas las notas residen siempre en la carpeta maestra *"Todas las notas"*.

2. **Carpetas Inteligentes (Smart Folders)**:
   - Filtros dinámicos en tiempo real basados en consultas SQLite ORM.
   - Modos de combinación lógica: **Coincidir con todos (AND)** o **Coincidir con cualquiera (OR)**.
   - Filtros soportados: Etiquetas (`#tags`), Fechas de modificación/creación, Listas de tareas (checklists completos/pendientes), Archivos adjuntos (fotos, videos, audio, PDF, enlaces) y estado de bloqueo.
   - Las carpetas inteligentes son virtuales (no mueven ni duplican notas físicas).

3. **Editor de Bloques Estilo Notion**:
   - Bloques independientes (encabezados, párrafos, listas con viñetas, checklists, citas, llamadas, código con resaltado de sintaxis, tablas dinámicas y tableros Kanban).
   - Ordenamiento fraccionario **O(1)** (*Fractional Indexing* con Base62) que permite mover bloques sin reindexar todo el documento.
   - Imágenes locales y externas con controles de redimensionamiento visual y anclaje (*float left, right, center*).

4. **Calendario y Recordatorios Integrados**:
   - Vista de calendario interactiva en la página de inicio.
   - Gestión de tareas y recordatorios con fecha, hora, categoría y estado completado.
   - Persistencia directa en base de datos SQLite (`reminders`).

5. **Historial de Versiones y Puntos de Restauración**:
   - Guardado automático de versiones históricas en SQLite (`note_history`).
   - Puntos de restauración manuales nombrados.
   - Reversión atómica a cualquier versión anterior con un solo clic.

6. **Metadatos de Enlaces Web (OpenGraph Previews)**:
   - Extracción automática de títulos, imágenes de portada, descripciones y favicons para tarjetas de enlaces enriquecidas, con almacenamiento en caché local (`web_link_cache`).

7. **Matemáticas, Audio y Firmas Digitales**:
   - Fórmulas matemáticas en tiempo real renderizadas con KaTeX.
   - Grabación y reproducción de notas de voz desde el propio editor.
   - Panel de firma manuscrita y digitalización de trazos.

---

## 📁 Arquitectura del Proyecto

### Firebase y la app móvil

Las portadas de degradado y el emoji se comparten con Android. Consulta [el contrato de portadas y las mejoras de unificación](docs/NOTE_COVERS.md). La actualización móvil incluye una migración Room 19→20 y conservación de estos campos en las copias de seguridad.

El menú **Note JS** agrupa creación, apertura de PDF, búsqueda, navegación y cuenta. La barra lateral muestra el estado de sincronización. Las herramientas del documento están en **Opciones de página**, con estilos claros y oscuros.

Las tablas móviles mantienen sus dimensiones, encabezados, franjas y colores de celda al editar y volver a sincronizar. Incluyen botones **+ Fila** y **+ Columna**, navegación con **Tab** y pegado de rangos tabulados dentro de la tabla. Las tablas descargadas por versiones anteriores se actualizan al recibir el estado de la nube, conservando las ediciones locales pendientes.

El escritorio está registrado como **Note JS Desktop** en el proyecto del móvil `isentropic-tape-465216-c1`. Utiliza la base Enterprise Native `ai-studio-android-notas-e533a5f4-cda6-4bde-b5d4-c0acf42009aa`, con actualizaciones en tiempo real habilitadas y las colecciones existentes `users/{uid}/notes`. Se mantienen las reglas desplegadas del móvil; esta integración no las reemplaza.

1. Abre **Ajustes → Mi Cuenta → Conectar con Google**. El acceso se completa en el navegador del sistema.
2. Usa la misma cuenta que en Android para recibir sus notas.
3. Para subir tu biblioteca anterior de la PC, elige **Sincronizar notas locales con esta cuenta**. Las notas de otra cuenta nunca se vinculan automáticamente.
4. Las notas nuevas se vinculan a la cuenta activa. SQLite conserva los cambios pendientes y se reintentan al recuperar la conexión o abrir de nuevo la app.

Se comparten título, contenido del lienzo, carpeta, etiquetas, fijado y papelera. La conversión admite texto, encabezados, listas, tareas, tablas e imágenes/PDF remotos. Los bloques móviles aún no editables se conservan con su información original. Las herramientas especiales del escritorio que están fuera del lienzo y los recordatorios/calendarios independientes siguen siendo locales en esta primera integración. Los conflictos conservan ambas versiones; una eliminación remota conserva una copia local.

**Adjuntos:** el proyecto todavía no tiene un bucket de Firebase Storage. Las notas con PDF o imágenes locales quedan pendientes y siguen guardadas en esta PC; las demás notas se sincronizan. Para compartir archivos hay que habilitar Storage, configurar sus reglas para `users/{uid}/notes_media/`, y actualizar `storageAvailable` en `frontend/firebase-config.json`. No se habilitó facturación ni se provisionó almacenamiento como parte de este cambio.

El SDK oficial está incluido en `frontend/vendor/firebase-sdk.mjs`, por lo que la app abre sin descargar dependencias. La configuración del cliente es pública; no se incluye una cuenta de servicio. La sesión de Firebase se conserva en el perfil local `webview/`, que no se distribuye con el instalador. El traspaso del acceso desde el navegador caduca en cinco minutos y se consume una sola vez.

Para reconstruir el SDK: `npm ci` y `npm run build:firebase`. Pruebas: `npm run test:firebase`, la suite Python, y `tests/firebase_client_smoke.cjs` contra emuladores Auth y Firestore Enterprise. La prueba de navegador usa cuentas sintéticas y una base SQLite temporal. Se usan listeners estándar porque la sincronización en tiempo real y el funcionamiento sin conexión son requisitos del producto.

El instalador crea una biblioteca nueva al iniciar y conserva la existente al actualizar: no incluye la base de datos de desarrollo ni las sesiones del autor.

Para ejecutar la prueba integral, con Java disponible: `npx -y firebase-tools@latest emulators:exec --project demo-notejs-desktop --only auth,firestore --config firebase.emulators.json "node tests/firebase_client_smoke.cjs"`. Las rutas de Python y Edge se pueden indicar mediante `NOTEJS_TEST_PYTHON` y `NOTEJS_TEST_BROWSER`.

### PDF en escritorio

- **Abrir PDF** en la barra lateral abre un documento local sin crear una nota.
- Dentro de una nota, **Archivo y Visor PDF** permite subir un PDF o pegar un enlace.
- El visor incluye páginas, zoom, rotación por página, búsqueda de texto, texto seleccionable mediante el botón **Texto**, dibujo a mano alzada, colores y deshacer trazos.
- **Guardar copia** exporta un PDF con los dibujos y las rotaciones. En escritorio se elige la ubicación con el diálogo nativo; en navegador se descarga. Los cambios se guardan en la copia, no automáticamente en el adjunto original.
- El instalador registra Note JS en **Abrir con** para `.pdf`. El ejecutable también acepta `NoteJS.exe "C:\\Documentos\\archivo.pdf"`.
- Los documentos locales funcionan sin Internet. Se conservan en `attachments/pdfs/`, junto a la base de datos de la aplicación; hay que incluir esa carpeta al trasladar las notas o hacer una copia manual. Límite: **50 MB por archivo**.
- Los enlaces externos requieren que el servidor permita acceso CORS; si no lo permite, descarga el PDF y súbelo como archivo local. La búsqueda requiere texto en el documento: esta implementación no incluye OCR ni edición del texto original. Los PDF cifrados pueden leerse con contraseña; su modificación depende del soporte de pdf-lib.
- Bibliotecas incluidas localmente: [PDF.js](https://mozilla.github.io/pdf.js/) 6.5.438 (Apache-2.0) y [pdf-lib](https://pdf-lib.js.org/) 1.17.1 (MIT), con sus licencias en `frontend/vendor/`.

Verificación: `python -m unittest discover -s tests -p test_pdf_documents.py`. La prueba real de renderizado y exportación se ejecuta con `node tests/pdf_reader_smoke.cjs`; requiere Edge y Python, cuyas rutas pueden indicarse con `NOTEJS_TEST_BROWSER` y `NOTEJS_TEST_PYTHON`.

```
Notas/
│
├── NoteJS.exe            # Ejecutable nativo para Windows 11 (Listo para usar)
├── desktop_app.py        # Ventana nativa de escritorio con PyWebView + Puente Python-JS
├── backend.py            # Servidor HTTP multihilo y API REST
├── server.py             # Entrypoint para servidor local
├── app.py                # Entrypoint secundario
├── models.py             # Capa de datos relacional con SQLite + Peewee ORM
├── peewee.py             # ORM Peewee integrado
├── requirements.txt      # Dependencias de Python
├── package.json          # Configuración y scripts npm
│
├── run_desktop.bat       # Inicia la app de escritorio en modo desarrollo (Windows 11)
├── run_server.bat        # Inicia el servidor local en modo desarrollo (Windows 11)
├── build_exe.bat         # Recompila NoteJS.exe con PyInstaller
├── build_linux.sh        # Compilador para binarios de Linux
│
├── dist/
│   └── NoteJS.exe        # Binario compilado con PyInstaller
│
├── frontend/             # Frontend completo para PC
│   ├── index.html        # Estructura del DOM y modales
│   ├── styles.css        # Sistema de diseño macOS / Notion
│   └── app.js            # Lógica completa de cliente y sincronización
│
└── android_legacy_backup/ # Archivo de seguridad con el código legacy de Android
```

---

## 💻 Cómo Ejecutar en Windows 11

### 🚀 Opción 1: Ejecución Directa con el Ejecutable (.exe) — Recomendada
Haz doble clic en **[`NoteJS.exe`](file:///C:/Users/Joaco/antigravity/Notas/NoteJS.exe)** (ubicado en la raíz del proyecto o en `dist/NoteJS.exe`).
- Se abrirá la aplicación en una ventana nativa ultraligera de escritorio sin requerir terminal ni dependencias activas.
- Todas tus notas, carpetas inteligentes y recordatorios se guardarán automáticamente en `notejs.db`.

---

### 🛠️ Opción 2: Modo Desarrollo (PyWebView)
Para desarrollar o modificar el código fuente en tiempo real:
- Haz doble clic sobre **[`run_desktop.bat`](file:///C:/Users/Joaco/antigravity/Notas/run_desktop.bat)**.
- El script detecta automáticamente tu instalación de Python en Windows 11 e inicia la ventana de desarrollo.

---

### 🌐 Opción 3: Modo Servidor Web Local
- Haz doble clic sobre **[`run_server.bat`](file:///C:/Users/Joaco/antigravity/Notas/run_server.bat)**.
- Abre tu navegador en: **`http://localhost:3000`**

---

### 📦 Opción 4: Recompilar el Ejecutable `.exe`
Si modificas los estilos, plantillas HTML, lógica JavaScript o modelos en Python y deseas generar un nuevo `.exe`:
- Haz doble clic sobre **[`build_exe.bat`](file:///C:/Users/Joaco/antigravity/Notas/build_exe.bat)**.
- PyInstaller reempaquetará el binario optimizado en `dist\NoteJS.exe`.
