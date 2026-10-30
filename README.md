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
