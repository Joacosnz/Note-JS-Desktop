// Note JS — Frontend JavaScript (Conectado a Backend Python + SQLite)
const COVER_PRESETS = [
      'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)',
      'linear-gradient(135deg, #0f172a 0%, #334155 50%, #475569 100%)',
      'linear-gradient(135deg, #064e3b 0%, #059669 50%, #10b981 100%)',
      'linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #c084fc 100%)',
      'linear-gradient(135deg, #831843 0%, #db2777 50%, #f472b6 100%)'
    ];

    const EMOJI_PALETTE = ['📝', '💡', '🚀', '🔬', '📚', '🎯', '⚙️', '📂', '⚡', '📊', '🎨', '💻'];

    const MASTER_ALL_NOTES_FOLDER = 'Todas Las Notas';

    const DEFAULT_FOLDER_EMOJIS = {
      'Todas Las Notas': '🗂️',
      'Personal': '🏠',
      'Trabajo': '💼',
      'Universidad': '🎓',
      'Ideas': '💡'
    };

    const FOLDER_EMOJI_CATEGORIES = [
      {
        id: 'organizacion',
        label: 'Carpetas y Archivo',
        emojis: ['📁', '📂', '🗂️', '📋', '📌', '📍', '🔖', '🏷️', '📦', '🗄️', '🧾', '📑', '📓', '📔', '📕', '📗', '📘', '📙']
      },
      {
        id: 'trabajo',
        label: 'Trabajo y Estudio',
        emojis: ['💼', '🎓', '📚', '🔬', '🧪', '🔭', '💻', '⌨️', '🖥️', '⚙️', '🛠️', '📊', '📈', '📉', '🏢', '🏛️', '⚖️', '🧮']
      },
      {
        id: 'creatividad',
        label: 'Ideas y Proyectos',
        emojis: ['💡', '🚀', '🎨', '✨', '🎯', '⚡', '🔥', '🧠', '🧩', '🎬', '🎵', '📷', '🕹️', '🏆', '💎', '🪄', '🌟', '🧭']
      },
      {
        id: 'vida',
        label: 'Personal y Finanzas',
        emojis: ['🏠', '❤️', '🌱', '🌿', '☕', '🍎', '🏋️', '✈️', '🌍', '💰', '💳', '🏦', '🛒', '🎁', '🐾', '🔒', '🔑', '🛡️']
      }
    ];

    const QUICK_FOLDER_EMOJIS = ['📁', '📂', '🏠', '💼', '🎓', '💡', '🚀', '📚', '🔬', '💻', '🎨', '📊', '⚡', '🎯', '💰', '❤️'];

    const SLASH_TAXONOMY = [
      // 1. Bloques Básicos (Estructura y Texto)
      { id: 'text', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Texto', desc: 'Párrafo regular de texto sin formato (/text)', icon: '¶' },
      { id: 'subpage', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Página (Subpágina)', desc: 'Crea y anida una subpágina dentro de tu hoja actual (/page)', icon: '📄' },
      { id: 'todo', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Lista de tareas (To-do)', desc: 'Tareas con casillas de verificación ([] )', icon: '☑' },
      { id: 'bullet', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Lista con viñetas', desc: 'Puntos de viñeta (- o * )', icon: '•' },
      { id: 'numbered', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Lista numerada', desc: 'Lista ordenada jerárquica (1. )', icon: '1.' },
      { id: 'heading1', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Encabezado 1 (H1)', desc: 'Título principal grande (# )', icon: 'H1' },
      { id: 'heading2', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Encabezado 2 (H2)', desc: 'Subencabezado de sección medio (## )', icon: 'H2' },
      { id: 'heading3', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Encabezado 3 (H3)', desc: 'Subencabezado pequeño (### )', icon: 'H3' },
      { id: 'heading4', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Encabezado 4 (H4)', desc: 'Subencabezado menor (#### )', icon: 'H4' },
      { id: 'inline_toggle', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Lista desplegable (Toggle)', desc: 'Oculta y anida bloques dentro de un título colapsable (> )', icon: '▶' },
      { id: 'simple_table', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Tabla simple', desc: 'Filas y columnas estáticas para organizar texto visualmente', icon: '⊞' },
      { id: 'quote', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Cita (Quote)', desc: 'Texto con formato ampliado y borde vertical ("" )', icon: '❝' },
      { id: 'divider', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Divisor (Divider)', desc: 'Línea horizontal gris muy delgada para separar secciones (---)', icon: '—' },
      { id: 'callout', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Caja de llamada (Callout)', desc: 'Rectángulo resaltado con borde claro, fondo tenue y emoji (/callout)', icon: '💡' },
      { id: 'inline_callout', cat: '1. Bloques Básicos (Estructura y Texto)', title: 'Caja de llamada (Callout)', desc: 'Rectángulo resaltado con borde claro, fondo tenue y emoji', icon: '💡' },

      // 2. Bloques de Medios y Archivos
      { id: 'image', cat: '2. Bloques de Medios y Archivos', title: 'Imagen', desc: 'Sube una imagen o pega un enlace externo redimensionable', icon: '🖼️' },
      { id: 'video', cat: '2. Bloques de Medios y Archivos', title: 'Video', desc: 'Incrusta o reproduce un video (/video)', icon: '🎥' },
      { id: 'audio', cat: '2. Bloques de Medios y Archivos', title: 'Audio', desc: 'Incrusta un archivo o pista de audio (/audio)', icon: '🎵' },
      { id: 'file', cat: '2. Bloques de Medios y Archivos', title: 'Archivo', desc: 'Adjunta un archivo descargable (/file)', icon: '📎' },
      { id: 'pdf', cat: '2. Bloques de Medios y Archivos', title: 'Documento PDF', desc: 'Incrusta un visor o documento PDF (/pdf)', icon: '📑' },
      { id: 'bookmark', cat: '2. Bloques de Medios y Archivos', title: 'Marcador Web (Bookmark)', desc: 'Crea una tarjeta de vista previa de enlace web (/bookmark)', icon: '🔖' },
      { id: 'pdf_file', cat: '2. Bloques de Medios y Archivos', title: 'Archivo y PDF', desc: 'Incrusta un PDF para leerlo en la página o adjúntalo (/pdf)', icon: '📑' },
      { id: 'code', cat: '2. Bloques de Medios y Archivos', title: 'Código', desc: 'Caja para programadores con formato de sintaxis (```)', icon: '</>' },
      { id: 'catalog', cat: '2. Bloques de Medios y Archivos', title: 'Catálogo de Bloques Notion', desc: 'Abre el catálogo interactivo de 48 bloques y 7 familias (/catalog)', icon: '📖' },

      // 3. Bases de Datos
      { id: 'db_table', cat: '3. Bases de Datos (6 Vistas)', title: 'Base de Datos · Vista Tabla', desc: 'Tabla clásica con propiedades y Fórmulas 2.0', icon: '▦' },
      { id: 'db_board', cat: '3. Bases de Datos (6 Vistas)', title: 'Base de Datos · Tablero Kanban', desc: 'Tarjetas de tareas en columnas de colores según su estado', icon: '📊' },
      { id: 'db_gallery', cat: '3. Bases de Datos (6 Vistas)', title: 'Base de Datos · Galería', desc: 'Mosaico de tarjetas grandes con imagen o portada recortada', icon: '🖼️' },
      { id: 'db_list', cat: '3. Bases de Datos (6 Vistas)', title: 'Base de Datos · Lista minimalista', desc: 'Vista de lista limpia para lectura rápida de registros', icon: '☰' },
      { id: 'db_calendar', cat: '3. Bases de Datos (6 Vistas)', title: 'Base de Datos · Calendario', desc: 'Rejilla mensual con elementos ubicados por fecha', icon: '📅' },
      { id: 'db_timeline', cat: '3. Bases de Datos (6 Vistas)', title: 'Base de Datos · Cronograma (Timeline)', desc: 'Línea de tiempo horizontal para fases y entregas', icon: '⏳' },

      // 4. Incrustaciones (Embeds de aplicaciones externas)
      { id: 'embed_gdrive', cat: '4. Incrustaciones (Embeds Externos)', title: 'Google Drive', desc: 'Incrusta documentos de Google Docs, Sheets o Slides', icon: '📁' },
      { id: 'embed_gmaps', cat: '4. Incrustaciones (Embeds Externos)', title: 'Google Maps', desc: 'Mapa interactivo por ubicación o coordenadas', icon: '🗺️' },
      { id: 'embed_figma', cat: '4. Incrustaciones (Embeds Externos)', title: 'Figma / InVision', desc: 'Visor interactivo de prototipos y diseños UI', icon: '🎨' },
      { id: 'embed_typeform', cat: '4. Incrustaciones (Embeds Externos)', title: 'Typeform', desc: 'Formulario y encuesta interactiva embebida', icon: '📋' },
      { id: 'embed_codepen', cat: '4. Incrustaciones (Embeds Externos)', title: 'GitHub / CodePen', desc: 'Fragmentos de código interactivos y Gists', icon: '💻' },
      { id: 'embed_loom', cat: '4. Incrustaciones (Embeds Externos)', title: 'Loom', desc: 'Grabación de pantalla interactiva en página', icon: '📹' },

      // 5. Bloques Avanzados y de Automatización
      { id: 'toc', cat: '5. Bloques Avanzados y de Automatización', title: 'Índice de contenido (Table of contents)', desc: 'Rastrea todos los encabezados y crea enlaces directos (/toc)', icon: '📑' },
      { id: 'synced', cat: '5. Bloques Avanzados y de Automatización', title: 'Bloque Sincronizado (Synced block)', desc: 'Contorno rojo al editar; sincroniza en tiempo real entre páginas', icon: '🔄' },
      { id: 'button', cat: '5. Bloques Avanzados y de Automatización', title: 'Botón de Automatización (Button)', desc: 'Inyecta bloques, crea páginas en BD o edita propiedades en masa', icon: '⚡' },
      { id: 'katex', cat: '5. Bloques Avanzados y de Automatización', title: 'Ecuación matemática (LaTeX)', desc: 'Renderizado de fórmulas científicas en bloque ($$ecuación$$)', icon: '∑' },
      { id: 'inline_math', cat: '5. Bloques Avanzados y de Automatización', title: 'Ecuación matemática en línea', desc: 'Fórmula LaTeX integrada en el párrafo (Ctrl+Shift+E)', icon: '√x' },
      { id: 'breadcrumbs', cat: '5. Bloques Avanzados y de Automatización', title: 'Menú de migas de pan (Breadcrumbs)', desc: 'Barra de navegación con la ruta exacta de carpeta y páginas', icon: '🧭' },
      { id: 'columns', cat: '5. Bloques Avanzados y de Automatización', title: '2 Columnas Paralelas (/columns)', desc: 'Alinea bloques lado a lado con guía vertical gris al pasar el ratón', icon: '▥' },
      { id: 'columns3', cat: '5. Bloques Avanzados y de Automatización', title: '3 Columnas Paralelas (/3cols)', desc: 'Divide el ancho en 3 columnas independientes', icon: '▤' },
      { id: 'embed_note', cat: '5. Bloques Avanzados y de Automatización', title: 'Incrustar Nota Vinculada', desc: 'Acceso directo visual a otra nota del espacio de trabajo', icon: '🎴' },

      // Colores y Fondos
      { id: 'color_amber', cat: 'Colores y Resaltados', title: 'Color Ámbar', desc: 'Texto con acento ámbar /amber', icon: '🟡', isColor: true, color: 'amber' },
      { id: 'color_blue', cat: 'Colores y Resaltados', title: 'Color Azul', desc: 'Texto azul /blue', icon: '🔵', isColor: true, color: 'blue' },
      { id: 'color_green', cat: 'Colores y Resaltados', title: 'Color Verde', desc: 'Texto verde esmeralda /green', icon: '🟢', isColor: true, color: 'green' },
      { id: 'color_red', cat: 'Colores y Resaltados', title: 'Color Rojo', desc: 'Texto rojo suave /red', icon: '🔴', isColor: true, color: 'red' },
      { id: 'color_purple', cat: 'Colores y Resaltados', title: 'Color Púrpura', desc: 'Texto morado /purple', icon: '🟣', isColor: true, color: 'purple' },
      { id: 'bg_amber', cat: 'Colores y Resaltados', title: 'Fondo Ámbar', desc: 'Resaltado con fondo ámbar', icon: '🟨', isBg: true, color: 'amber_background' },
      { id: 'bg_green', cat: 'Colores y Resaltados', title: 'Fondo Verde', desc: 'Resaltado con fondo verde', icon: '🟩', isBg: true, color: 'green_background' },
      { id: 'bg_blue', cat: 'Colores y Resaltados', title: 'Fondo Azul', desc: 'Resaltado con fondo azul', icon: '🟦', isBg: true, color: 'blue_background' },
      { id: 'bg_red', cat: 'Colores y Resaltados', title: 'Fondo Rojo', desc: 'Resaltado con fondo rojo (/red background)', icon: '🟥', isBg: true, color: 'red_background' }
    ];

    const INITIAL_NOTES = [];

    const PANEL_WIDTH_DEFAULTS = {
      folders: 250,
      gallery: 300
    };

    const PANEL_WIDTH_LIMITS = {
      folders: { min: 170, max: 450 },
      gallery: { min: 220, max: 600 },
      editorMin: 340
    };

    const INITIAL_REMINDERS = [];

    let state = {
      isFocusMode: false,
      isGridView: false,
      isSuggestionMode: false,
      isRevisionsPanelOpen: false,
      isHistoryPanelOpen: false,
      activeNoteHistory: [],
      isRemindersActive: false,
      startupBehavior: (() => {
        try {
          const c = JSON.parse(localStorage.getItem('notejs_settings_cache') || '{}');
          return c.startupBehavior || 'clean';
        } catch (_) {
          return 'clean';
        }
      })(),
      activeNoteId: (() => {
        try {
          const c = JSON.parse(localStorage.getItem('notejs_settings_cache') || '{}');
          if (c.startupBehavior === 'resume') {
            const last = localStorage.getItem('notejs_last_visited_note');
            return last !== null ? Number(last) : null;
          }
        } catch (_) {}
        return null;
      })(),
      openTabIds: (() => {
        try {
          const c = JSON.parse(localStorage.getItem('notejs_settings_cache') || '{}');
          if (c.startupBehavior === 'resume') {
            const s = localStorage.getItem('notejs_open_tabs_v1');
            return s !== null ? JSON.parse(s) : [];
          }
        } catch (_) {}
        return [];
      })(),
      selectedCollection: 'ALL',
      selectedFolder: (() => {
        try {
          const c = JSON.parse(localStorage.getItem('notejs_settings_cache') || '{}');
          if (c.startupBehavior === 'resume') {
            return MASTER_ALL_NOTES_FOLDER;
          }
        } catch (_) {}
        return null;
      })(),
      selectedTag: null,
      notes: JSON.parse(localStorage.getItem('notejs_desktop_notion_v9') || 'null') || INITIAL_NOTES,
      folders: JSON.parse(localStorage.getItem('notejs_folders_v1') || 'null') || [MASTER_ALL_NOTES_FOLDER, 'Primeros pasos'],
      folderEmojis: JSON.parse(localStorage.getItem('notejs_folder_emojis_v1') || 'null') || { ...DEFAULT_FOLDER_EMOJIS },
      smartFolders: JSON.parse(localStorage.getItem('notejs_smart_folders_v1') || 'null') || {},
      panelWidths: JSON.parse(localStorage.getItem('notejs_panel_widths_v1') || 'null') || { ...PANEL_WIDTH_DEFAULTS },
      isHomeActive: true,
      isLightMode: false,
      accentColorMode: 'default',
      customAccentColor: '#f59e0b',
      themeMode: 'system',
      highContrast: false,
      enterCreatesBlock: true,
      showWordCount: true,
      language: 'es',
      typeStyleIndex: 0,
      homeNotesView: localStorage.getItem('notejs_home_notes_view') || 'grid',
      calendarYear: new Date().getFullYear(),
      calendarMonth: new Date().getMonth(),
      selectedCalendarDate: getTodayDateString(),
      eventsFilter: 'day',
      homeNotesSearchQuery: '',
      homeFolderFilter: null,
      collapsedParentFolders: JSON.parse(localStorage.getItem('notejs_collapsed_folders_v1') || '[]'),
      reminders: JSON.parse(localStorage.getItem('notejs_calendar_reminders_v1') || 'null') || INITIAL_REMINDERS
    };

    // Aplicar configuración inicial guardada en caché local para evitar parpadeos
    try {
      const cachedSettings = JSON.parse(localStorage.getItem('notejs_settings_cache') || '{}');
      if (cachedSettings.accentColorMode) state.accentColorMode = cachedSettings.accentColorMode;
      if (cachedSettings.customAccentColor) state.customAccentColor = cachedSettings.customAccentColor;
      if (cachedSettings.themeMode) state.themeMode = cachedSettings.themeMode;
      if (cachedSettings.highContrast) state.highContrast = (cachedSettings.highContrast === 'true' || cachedSettings.highContrast === true);
      if (cachedSettings.accentColorMode || cachedSettings.customAccentColor) {
        applyAccentColor(state.accentColorMode, state.customAccentColor, false);
      }
      if (cachedSettings.themeMode) {
        applyThemeMode(state.themeMode, false);
      }
      if (state.highContrast) {
        document.body.classList.add('high-contrast-mode');
      }
    } catch (_) {}

    const TRASH_FOLDER_KEY = '__TRASH__';

    function isTrashFolder(folderName) {
      return folderName === TRASH_FOLDER_KEY;
    }

    function isMasterAllNotesFolder(folderName) {
      if (!folderName) return false;
      return String(folderName).trim().toLowerCase() === 'todas las notas';
    }

    function getFolderDisplayName(folderPath) {
      if (!folderPath) return '';
      if (isTrashFolder(folderPath)) return 'Papelera';
      const parts = String(folderPath).split('/').map(s => s.trim()).filter(Boolean);
      return parts.length ? parts[parts.length - 1] : String(folderPath);
    }

    function getFolderParentPath(folderPath) {
      if (!folderPath || isMasterAllNotesFolder(folderPath) || isTrashFolder(folderPath)) return '';
      const parts = String(folderPath).split('/').map(s => s.trim()).filter(Boolean);
      return parts.length > 1 ? parts.slice(0, -1).join('/') : '';
    }

    function getFolderDepth(folderPath) {
      if (!folderPath || isMasterAllNotesFolder(folderPath) || isTrashFolder(folderPath)) return 0;
      const parts = String(folderPath).split('/').map(s => s.trim()).filter(Boolean);
      return Math.max(0, parts.length - 1);
    }

    function getSubfoldersOf(parentPath) {
      if (!parentPath || isMasterAllNotesFolder(parentPath) || isTrashFolder(parentPath)) return [];
      const prefix = parentPath + '/';
      return (state.folders || []).filter(f => f && f.startsWith(prefix));
    }

    function isSmartFolder(folderName) {
      if (!folderName || isMasterAllNotesFolder(folderName) || isTrashFolder(folderName)) return false;
      const clean = String(folderName).trim();
      if (state.smartFolders && typeof state.smartFolders === 'object' && state.smartFolders[clean]) {
        return true;
      }
      if (Array.isArray(state.folderItems)) {
        const found = state.folderItems.find(it => it && it.name === clean);
        if (found && found.isSmart) return true;
      }
      return false;
    }

    function getSmartFolderConfig(folderName) {
      if (!isSmartFolder(folderName)) return null;
      const clean = String(folderName).trim();
      let raw = state.smartFolders ? state.smartFolders[clean] : null;
      if ((!raw || typeof raw !== 'object') && Array.isArray(state.folderItems)) {
        const found = state.folderItems.find(it => it && it.name === clean);
        if (found && found.isSmart && found.smartConfig) {
          raw = found.smartConfig;
        }
      }
      if (!raw || typeof raw !== 'object') return null;
      return {
        matchMode: raw.matchMode === 'any' ? 'any' : 'all',
        rules: Array.isArray(raw.rules) ? raw.rules : []
      };
    }

    function extractNoteTagsList(note) {
      if (!note) return [];
      const set = new Set();
      const raw = note.tags || '';
      const arr = Array.isArray(raw) ? raw : String(raw).split(',');
      arr.forEach(t => {
        const clean = String(t || '').trim().toLowerCase().replace(/^#/, '');
        if (clean) set.add(clean);
      });
      const contentText = String(note.content || '').replace(/<[^>]*>?/gm, ' ');
      const inlineMatches = contentText.match(/(?:^|\s)#([a-zA-Z0-9_áéíóúñÁÉÍÓÚÑ-]{2,32})/g) || [];
      inlineMatches.forEach(m => {
        const clean = m.trim().replace(/^#/, '').toLowerCase();
        if (clean) set.add(clean);
      });
      return Array.from(set);
    }

    function getNotePreviewText(note) {
      let html = String(note.content || '');
      if (html.includes('cloud-table-toolbar')) {
        const template = document.createElement('template');
        template.innerHTML = html;
        template.content.querySelectorAll('.cloud-table-toolbar').forEach(toolbar => toolbar.remove());
        html = template.innerHTML;
      }
      return html.replace(/<\/t[dh]>/gi, ' · ').replace(/<[^>]*>?/gm, ' ').replace(/\s+/g, ' ').trim();
    }

    function extractNoteMentionsList(note) {
      if (!note) return [];
      const set = new Set();
      if (Array.isArray(note.mentions)) {
        note.mentions.forEach(u => {
          const clean = String(u || '').trim().toLowerCase().replace(/^@/, '');
          if (clean) set.add(clean);
        });
      }
      const combined = `${note.title || ''} ${String(note.content || '').replace(/<[^>]*>?/gm, ' ')} ${note.callout || ''} ${note.quote || ''}`;
      const matches = combined.match(/(?:^|\s)@([a-zA-Z0-9_.-]{2,32})/g) || [];
      matches.forEach(m => {
        const clean = m.trim().replace(/^@/, '').toLowerCase();
        if (clean) set.add(clean);
      });
      return Array.from(set);
    }

    function extractNoteSharedUsersList(note) {
      if (!note) return [];
      const set = new Set();
      if (Array.isArray(note.sharedWith)) {
        note.sharedWith.forEach(u => {
          const clean = String(u || '').trim().toLowerCase().replace(/^@/, '');
          if (clean) set.add(clean);
        });
      } else if (typeof note.sharedWith === 'string' && note.sharedWith.trim()) {
        note.sharedWith.split(',').forEach(u => {
          const clean = String(u || '').trim().toLowerCase().replace(/^@/, '');
          if (clean) set.add(clean);
        });
      }
      return Array.from(set);
    }

    function noteMatchesSmartRule(note, rule) {
      if (!note || !rule || !rule.type) return false;
      const type = String(rule.type);
      const condition = String(rule.condition || 'any');

      if (type === 'tags') {
        const noteTags = extractNoteTagsList(note);
        if (condition === 'untagged') {
          return noteTags.length === 0;
        }
        if (condition === 'any_tag') {
          return noteTags.length > 0;
        }
        const targetTags = (Array.isArray(rule.values) ? rule.values : String(rule.value || '').split(','))
          .map(t => String(t || '').trim().toLowerCase().replace(/^#/, ''))
          .filter(Boolean);
        if (!targetTags.length) {
          return false;
        }
        if (condition === 'all_selected') {
          return targetTags.every(t => noteTags.includes(t));
        }
        if (condition === 'none_selected') {
          return targetTags.every(t => !noteTags.includes(t));
        }
        // Por defecto: 'any_selected' (contiene cualquiera de las etiquetas indicadas)
        return targetTags.some(t => noteTags.includes(t));
      }

      if (type === 'date') {
        const field = rule.field === 'createdAt' ? 'createdAt' : 'updatedAt';
        const rawTs = Number(note[field] || note.updatedAt || note.id || Date.now());
        const noteDate = new Date(rawTs);
        const now = new Date();
        const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
        const startOfYesterday = startOfToday - 86400000;

        if (condition === 'today') {
          return rawTs >= startOfToday;
        }
        if (condition === 'yesterday') {
          return rawTs >= startOfYesterday && rawTs < startOfToday;
        }
        if (condition === 'last_7_days') {
          return rawTs >= (Date.now() - 7 * 86400000);
        }
        if (condition === 'last_30_days') {
          return rawTs >= (Date.now() - 30 * 86400000);
        }
        if (condition === 'custom_range') {
          let afterFrom = true;
          let beforeTo = true;
          if (rule.from) {
            const fromTs = new Date(rule.from + 'T00:00:00').getTime();
            if (!isNaN(fromTs)) afterFrom = rawTs >= fromTs;
          }
          if (rule.to) {
            const toTs = new Date(rule.to + 'T23:59:59').getTime();
            if (!isNaN(toTs)) beforeTo = rawTs <= toTs;
          }
          return afterFrom && beforeTo && !isNaN(noteDate.getTime());
        }
        return false;
      }

      if (type === 'checklists') {
        const list = (note.showChecklist && Array.isArray(note.checklists)) ? note.checklists : [];
        const html = String(note.content || '');
        const hasHtmlCheck = /type=["']checkbox["']|task-list-item/i.test(html);
        const hasChecklists = list.length > 0 || hasHtmlCheck;
        const hasUnchecked = list.some(item => !item.done) || /type=["']checkbox["'](?![^>]*checked)/i.test(html);
        const hasChecked = list.some(item => Boolean(item.done)) || /type=["']checkbox["'][^>]*checked/i.test(html);

        if (condition === 'none') return !hasChecklists;
        if (condition === 'unchecked') return hasChecklists && hasUnchecked;
        if (condition === 'checked') return hasChecklists && hasChecked;
        if (condition === 'both') return hasChecklists && hasUnchecked && hasChecked;
        // 'any'
        return hasChecklists;
      }

      if (type === 'attachments') {
        const html = String(note.content || '');
        const hasPhotosOrVideos = /note-image-block|<img\b|<video\b|\.(?:png|jpe?g|gif|webp|mp4|webm)/i.test(html);
        const hasPdf = /\.pdf\b|application\/pdf/i.test(html);
        const hasAudio = /<audio\b|\.(?:mp3|wav|ogg|m4a)\b/i.test(html);
        const hasDrawing = /<svg\b|<canvas\b|data:image\/svg\+xml/i.test(html) || Boolean(note.katex);
        const hasWebLinks = /<a\s+[^>]*href=|https?:\/\/[^\s<"]+|note-embedded-card/i.test(html);

        if (condition === 'photos_videos') return hasPhotosOrVideos;
        if (condition === 'pdfs') return hasPdf;
        if (condition === 'audio') return hasAudio;
        if (condition === 'drawings') return hasDrawing;
        if (condition === 'links') return hasWebLinks;
        // 'any'
        return hasPhotosOrVideos || hasPdf || hasAudio || hasDrawing || hasWebLinks;
      }

      if (type === 'shared') {
        const sharedUsers = extractNoteSharedUsersList(note);
        const isShared = Boolean(note.isShared) || sharedUsers.length > 0;
        if (condition === 'not_shared') return !isShared;
        if (condition === 'specific_user') {
          const targetUser = String(rule.value || '').trim().toLowerCase().replace(/^@/, '');
          if (!targetUser) return isShared;
          return sharedUsers.some(u => u.includes(targetUser));
        }
        // 'any_shared'
        return isShared;
      }

      if (type === 'pinned_locked') {
        const isPinned = Boolean(note.isPinned);
        const isLocked = Boolean(note.isLocked);
        if (condition === 'pinned') return isPinned;
        if (condition === 'locked') return isLocked;
        if (condition === 'not_locked') return !isLocked;
        if (condition === 'pinned_or_locked') return isPinned || isLocked;
        if (condition === 'not_pinned') return !isPinned;
        return isLocked;
      }

      if (type === 'mentions') {
        const mentions = extractNoteMentionsList(note);
        if (condition === 'no_mentions') return mentions.length === 0;
        if (condition === 'specific_mention') {
          const targetMention = String(rule.value || '').trim().toLowerCase().replace(/^@/, '');
          if (!targetMention) return mentions.length > 0;
          return mentions.some(m => m.includes(targetMention));
        }
        // 'any_mention'
        return mentions.length > 0;
      }

      return false;
    }

    function noteMatchesSmartFolder(note, folderName) {
      if (!note || note.isTrashed) return false;
      const cfg = getSmartFolderConfig(folderName);
      if (!cfg) return false;
      const rules = Array.isArray(cfg.rules) ? cfg.rules : [];
      if (!rules.length) return false;
      if (cfg.matchMode === 'any') {
        return rules.some(rule => noteMatchesSmartRule(note, rule));
      }
      return rules.every(rule => noteMatchesSmartRule(note, rule));
    }

    function formatSmartRuleSummary(rule) {
      if (!rule || !rule.type) return 'Regla activa';
      const type = rule.type;
      const cond = rule.condition || 'any';
      if (type === 'tags') {
        if (cond === 'untagged') return '🏷️ Sin etiquetas';
        if (cond === 'any_tag') return '🏷️ Con cualquier #tag';
        const val = String(rule.value || '').trim();
        const prefix = cond === 'all_selected' ? '🏷️ Todas:' : (cond === 'none_selected' ? '🏷️ Sin:' : '🏷️ Etiquetas:');
        return val ? `${prefix} #${val.split(',').map(s => s.trim().replace(/^#/, '')).filter(Boolean).join(', #')}` : '🏷️ Con etiquetas';
      }
      if (type === 'date') {
        const fieldLabel = rule.field === 'createdAt' ? 'Creada' : 'Modificada';
        const map = {
          today: 'Hoy',
          yesterday: 'Ayer',
          last_7_days: 'Últimos 7 días',
          last_30_days: 'Últimos 30 días',
          custom_range: `${rule.from || '...'} → ${rule.to || '...'}`
        };
        return `📅 ${fieldLabel}: ${map[cond] || 'Reciente'}`;
      }
      if (type === 'checklists') {
        const map = {
          any: '☑ Con listas de tareas',
          unchecked: '⬜ Tareas sin marcar',
          checked: '✅ Tareas marcadas',
          both: '☑ Marcadas y sin marcar',
          none: '🚫 Sin listas de tareas'
        };
        return map[cond] || '☑ Listas de tareas';
      }
      if (type === 'attachments') {
        const map = {
          any: '📎 Con archivos adjuntos',
          photos_videos: '🖼️ Fotos o videos',
          pdfs: '📄 Documentos PDF',
          audio: '🎙️ Audio',
          drawings: '✏️ Dibujos / fórmulas',
          links: '🔗 Enlaces web o notas incrustadas'
        };
        return map[cond] || '📎 Archivos adjuntos';
      }
      if (type === 'shared') {
        if (cond === 'not_shared') return '👤 No compartidas';
        if (cond === 'specific_user' && rule.value) return `👥 Compartida con @${String(rule.value).replace(/^@/, '')}`;
        return '👥 Notas compartidas';
      }
      if (type === 'pinned_locked') {
        const map = {
          locked: '🔒 Notas bloqueadas',
          not_locked: '🔓 Notas no bloqueadas',
          pinned: '📌 Notas fijadas',
          not_pinned: '📄 No fijadas',
          pinned_or_locked: '📌/🔒 Fijadas o bloqueadas'
        };
        return map[cond] || '🔒 Estado de bloqueo';
      }
      if (type === 'mentions') {
        if (cond === 'no_mentions') return '🔕 Sin menciones';
        if (cond === 'specific_mention' && rule.value) return `💬 Menciona a @${String(rule.value).replace(/^@/, '')}`;
        return '💬 Con @menciones';
      }
      return '⚙️ Filtro activo';
    }

    function getNoteFolders(note) {
      if (!note) return [MASTER_ALL_NOTES_FOLDER];
      const rawList = [];
      if (Array.isArray(note.folders)) {
        note.folders.forEach(f => {
          if (f && typeof f === 'string') rawList.push(f.trim());
        });
      }
      if (note.folder && typeof note.folder === 'string') {
        note.folder.split('|').forEach(part => {
          const clean = part.trim();
          if (clean) rawList.push(clean);
        });
      }
      const userFolders = [];
      const seen = new Set();
      rawList.forEach(f => {
        // Las carpetas inteligentes son referencias dinámicas, no contenedores físicos
        if (!f || isMasterAllNotesFolder(f) || isTrashFolder(f) || isSmartFolder(f)) return;
        if (!seen.has(f)) {
          seen.add(f);
          userFolders.push(f);
        }
      });
      return [MASTER_ALL_NOTES_FOLDER, ...userFolders];
    }

    function getNoteUserFolders(note) {
      return getNoteFolders(note).filter(f => !isMasterAllNotesFolder(f) && !isSmartFolder(f));
    }

    function getNotePrimaryDisplayFolder(note) {
      const userFolders = getNoteUserFolders(note);
      return userFolders.length > 0 ? userFolders[0] : MASTER_ALL_NOTES_FOLDER;
    }

    function setNoteFolders(note, foldersArr) {
      if (!note) return;
      const raw = Array.isArray(foldersArr)
        ? foldersArr
        : String(foldersArr || '').split('|');
      const userFolders = [];
      const seen = new Set();
      raw.forEach(f => {
        const clean = String(f || '').trim();
        if (!clean || isMasterAllNotesFolder(clean) || isTrashFolder(clean) || isSmartFolder(clean)) return;
        if (!seen.has(clean)) {
          seen.add(clean);
          userFolders.push(clean);
        }
      });
      note.folders = [MASTER_ALL_NOTES_FOLDER, ...userFolders];
      note.folder = userFolders.length > 0 ? userFolders.join(' | ') : MASTER_ALL_NOTES_FOLDER;
      persistNoteMetaOverlay();
    }

    function noteBelongsToFolder(note, targetFolder) {
      if (!note) return false;
      if (isTrashFolder(targetFolder)) {
        return Boolean(note.isTrashed);
      }
      if (note.isTrashed) return false;
      if (!targetFolder || isMasterAllNotesFolder(targetFolder)) {
        return true;
      }
      // Si es una Carpeta Inteligente, escanea dinámicamente todas las notas activas según sus reglas
      if (isSmartFolder(targetFolder)) {
        return noteMatchesSmartFolder(note, targetFolder);
      }
      const noteFolders = getNoteFolders(note);
      const prefix = targetFolder + '/';
      return noteFolders.some(f => f === targetFolder || f.startsWith(prefix));
    }

    function getActiveNotesList() {
      return (state.notes || []).filter(n => !n.isTrashed);
    }

    function getTrashedNotesList() {
      return (state.notes || []).filter(n => Boolean(n.isTrashed));
    }

    function persistNoteMetaOverlay() {
      try {
        const overlay = {};
        (state.notes || []).forEach(n => {
          if (!n || !n.id) return;
          overlay[n.id] = {
            isTrashed: Boolean(n.isTrashed),
            trashedAt: n.trashedAt || null,
            folders: getNoteFolders(n)
          };
        });
        localStorage.setItem('notejs_notes_meta_overlay_v1', JSON.stringify(overlay));
      } catch (_) {}
    }

    function applyNoteMetaOverlay(notesList) {
      if (!Array.isArray(notesList)) return;
      let overlay = {};
      try {
        overlay = JSON.parse(localStorage.getItem('notejs_notes_meta_overlay_v1') || '{}') || {};
      } catch (_) {
        overlay = {};
      }
      notesList.forEach(n => {
        if (!n || !n.id) return;
        const saved = overlay[n.id];
        if (saved) {
          if (typeof saved.isTrashed === 'boolean') n.isTrashed = saved.isTrashed;
          if (saved.trashedAt) n.trashedAt = saved.trashedAt;
          if (Array.isArray(saved.folders) && saved.folders.length) {
            setNoteFolders(n, saved.folders);
          } else {
            setNoteFolders(n, getNoteFolders(n));
          }
        } else {
          setNoteFolders(n, getNoteFolders(n));
        }
      });
    }

    function ensureMasterFolderFirst() {
      if (!state.smartFolders || typeof state.smartFolders !== 'object') {
        state.smartFolders = {};
      }
      // Limitación del sistema: Las carpetas inteligentes siempre viven en el nivel raíz (no admiten subcarpetas)
      const normalizedSmart = {};
      Object.keys(state.smartFolders).forEach(k => {
        const rootKey = String(k || '').split('/').map(s => s.trim()).filter(Boolean)[0] || '';
        if (rootKey && !isMasterAllNotesFolder(rootKey) && !isTrashFolder(rootKey)) {
          normalizedSmart[rootKey] = state.smartFolders[k];
        }
      });
      state.smartFolders = normalizedSmart;

      if (!Array.isArray(state.folders) || !state.folders.length) {
        state.folders = [MASTER_ALL_NOTES_FOLDER, 'Personal', 'Trabajo', 'Universidad', 'Ideas'];
      } else {
        const cleaned = [];
        state.folders.forEach(f => {
          if (!f || isMasterAllNotesFolder(f) || isTrashFolder(f)) return;
          const parts = String(f).split('/').map(s => s.trim()).filter(Boolean);
          if (!parts.length) return;
          if (normalizedSmart[parts[0]]) {
            // Si la raíz es una carpeta inteligente, forzar nivel raíz sin subcarpetas
            if (!cleaned.includes(parts[0])) cleaned.push(parts[0]);
          } else {
            cleaned.push(parts.join('/'));
          }
        });
        Object.keys(normalizedSmart).forEach(sf => {
          if (!cleaned.includes(sf)) cleaned.push(sf);
        });
        const sortedOthers = sortFoldersHierarchically(cleaned);
        state.folders = [MASTER_ALL_NOTES_FOLDER, ...sortedOthers];
      }
      if (state.folderEmojis && typeof state.folderEmojis === 'object') {
        state.folderEmojis[MASTER_ALL_NOTES_FOLDER] = '🗂️';
      }
    }

    function sortFoldersHierarchically(foldersList) {
      const unique = [];
      const seen = new Set();
      foldersList.forEach(f => {
        const clean = String(f || '').trim();
        if (clean && !isMasterAllNotesFolder(clean) && !isTrashFolder(clean) && !seen.has(clean)) {
          seen.add(clean);
          unique.push(clean);
        }
      });
      // Asegurar que si existe "Padre/Hijo" y "Padre" está en la lista, los hijos queden justo debajo de su padre
      const result = [];
      const visited = new Set();
      function visit(folderPath) {
        if (visited.has(folderPath)) return;
        visited.add(folderPath);
        result.push(folderPath);
        if (isSmartFolder(folderPath)) return;
        const directChildren = unique.filter(candidate => getFolderParentPath(candidate) === folderPath);
        directChildren.forEach(child => visit(child));
      }
      unique.filter(f => !getFolderParentPath(f) || !seen.has(getFolderParentPath(f))).forEach(root => visit(root));
      unique.forEach(f => visit(f));
      return result;
    }

    ensureMasterFolderFirst();
    applyNoteMetaOverlay(state.notes);

    function persistRemindersLocal() {
      try {
        localStorage.setItem('notejs_calendar_reminders_v1', JSON.stringify(state.reminders));
      } catch (_) {}
    }

    async function persistReminderToBackend(reminder) {
      if (!reminder) return;
      try {
        if (hasPyWebViewBridge() && typeof window.pywebview.api.save_reminder === 'function') {
          await window.pywebview.api.save_reminder(reminder);
          return;
        }
        await fetch('/api/reminders', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reminder })
        });
      } catch (_) {}
    }

    async function deleteReminderFromBackend(id) {
      try {
        if (hasPyWebViewBridge() && typeof window.pywebview.api.delete_reminder === 'function') {
          await window.pywebview.api.delete_reminder(id);
          return;
        }
        await fetch(`/api/reminders/${id}`, { method: 'DELETE' });
      } catch (_) {}
    }

    async function syncRemindersToBackend(list) {
      if (!Array.isArray(list) || list.length === 0) return;
      try {
        if (hasPyWebViewBridge() && typeof window.pywebview.api.sync_reminders === 'function') {
          await window.pywebview.api.sync_reminders(list);
          return;
        }
        await fetch('/api/reminders/sync', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reminders: list })
        });
      } catch (_) {}
    }

    async function fetchWebLinkMetadata(url) {
      if (!url) return null;
      try {
        if (hasPyWebViewBridge() && typeof window.pywebview.api.fetch_weblink_metadata === 'function') {
          const res = await window.pywebview.api.fetch_weblink_metadata(url);
          return res && res.ok ? res.metadata : null;
        }
        const res = await fetch(`/api/weblinks/metadata?url=${encodeURIComponent(url)}`);
        if (res.ok) {
          const data = await res.json();
          return data && data.ok ? data.metadata : null;
        }
      } catch (_) {}
      return null;
    }
    window.fetchWebLinkMetadata = fetchWebLinkMetadata;

    function getFolderEmoji(folderName) {
      if (!folderName) return '📁';
      if (isTrashFolder(folderName)) return '🗑️';
      if (isMasterAllNotesFolder(folderName)) return '🗂️';
      if (state.folderEmojis && typeof state.folderEmojis === 'object' && state.folderEmojis[folderName]) {
        return state.folderEmojis[folderName];
      }
      if (isSmartFolder(folderName)) return '⚙️';
      return DEFAULT_FOLDER_EMOJIS[folderName] || '📁';
    }

    function persistFoldersLocal() {
      ensureMasterFolderFirst();
      try {
        localStorage.setItem('notejs_folders_v1', JSON.stringify(state.folders));
        localStorage.setItem('notejs_folder_emojis_v1', JSON.stringify(state.folderEmojis));
        localStorage.setItem('notejs_smart_folders_v1', JSON.stringify(state.smartFolders || {}));
      } catch (_) {}
    }

    function saveFoldersToBackend() {
      ensureMasterFolderFirst();
      persistFoldersLocal();
      const payload = {
        folders: state.folders,
        folderEmojis: state.folderEmojis,
        smartFolders: state.smartFolders || {}
      };
      if (hasPyWebViewBridge() && typeof window.pywebview.api.save_folders === "function") {
        window.pywebview.api.save_folders(payload, state.folderEmojis).catch(() => {});
      } else {
        fetch("/api/folders", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        }).catch(() => {});
      }
    }

    /* Sincronización con Backend en Python (PyWebView Bridge + SQLite & Peewee ORM) */
    let syncTimeout = null;
    let resolveCloudLocalReady;
    const cloudLocalReady = new Promise(resolve => { resolveCloudLocalReady = resolve; });

    function hasPyWebViewBridge() {
      return Boolean(window.pywebview && window.pywebview.api);
    }

    function setSyncStatus(status) {
      const indicator = document.getElementById("save-status-indicator");
      if (!indicator) return;

      indicator.classList.remove("saving", "synced", "offline", "error");
      if (status === "saving") {
        indicator.classList.add("saving");
        indicator.title = "Guardando en SQLite (notejs.db)...";
      } else if (status === "synced") {
        indicator.classList.add("synced");
        indicator.title = "Sincronizado y guardado en SQLite (notejs.db)";
      } else {
        indicator.classList.add("offline");
        indicator.title = "Guardado localmente (desconectado o sin red)";
      }
    }

    async function initPythonBackendSync() {
      try {
        let data;
        if (hasPyWebViewBridge() && typeof window.pywebview.api.bootstrap === "function") {
          data = await window.pywebview.api.bootstrap();
        } else {
          const res = await fetch("/api/bootstrap", { cache: "no-store" });
          if (!res.ok) throw new Error("HTTP " + res.status);
          data = await res.json();
        }

        if (Array.isArray(data.folders) && data.folders.length > 0) {
          state.folders = data.folders;
        }

        if (data.folderEmojis && typeof data.folderEmojis === "object") {
          state.folderEmojis = {
            ...DEFAULT_FOLDER_EMOJIS,
            ...(state.folderEmojis || {}),
            ...data.folderEmojis
          };
        }
        if (Array.isArray(data.folderItems)) {
          state.folderItems = data.folderItems;
          data.folderItems.forEach(item => {
            if (item && item.name) {
              if (item.emoji) state.folderEmojis[item.name] = item.emoji;
              if (item.isSmart && item.smartConfig) {
                state.smartFolders[item.name] = item.smartConfig;
              }
            }
          });
        }
        if (data.smartFolders && typeof data.smartFolders === "object") {
          state.smartFolders = {
            ...(state.smartFolders || {}),
            ...data.smartFolders
          };
        }
        persistFoldersLocal();

        if (data.settings) {
          state.settings = data.settings;
          if (typeof data.settings.isLightMode !== "undefined") {
            state.isLightMode = (data.settings.isLightMode === "true" || data.settings.isLightMode === true);
            document.body.classList.toggle("light-mode", state.isLightMode);
          }
          if (data.settings.themeMode) {
            applyThemeMode(data.settings.themeMode, false);
          }
          if (data.settings.highContrast === "true" || data.settings.highContrast === true) {
            state.highContrast = true;
            document.body.classList.add("high-contrast-mode");
          }
          if (data.settings.accentColorMode || data.settings.customAccentColor) {
            applyAccentColor(data.settings.accentColorMode || 'default', data.settings.customAccentColor || '#f59e0b', false);
          }
        }

        if (data.settings && data.settings.customShortcuts) {
          try {
            const parsedShortcuts = typeof data.settings.customShortcuts === "string"
              ? JSON.parse(data.settings.customShortcuts)
              : data.settings.customShortcuts;
            if (parsedShortcuts && typeof parsedShortcuts === "object") {
              applyCustomShortcutsMap(parsedShortcuts, false);
            }
          } catch (_) {}
        }

        // R6: Comportamiento de Inicio de la Aplicación (Predeterminado de fábrica: Iniciar siempre de cero)
        const startupBehavior = (data.settings && data.settings.startupBehavior) || state.startupBehavior || 'clean';
        state.startupBehavior = startupBehavior;

        if (startupBehavior === 'clean') {
          state.openTabIds = [];
          state.activeNoteId = null;
          state.selectedFolder = null;
          state.isHomeActive = true;
        } else if (startupBehavior === 'resume') {
          const lastNoteId = Number((data.settings && data.settings.lastVisitedNoteId) || localStorage.getItem('notejs_last_visited_note'));
          if (lastNoteId && (data.notes || state.notes || []).some(n => n.id === lastNoteId && !n.isTrashed)) {
            state.activeNoteId = lastNoteId;
            state.openTabIds = [lastNoteId];
            state.isHomeActive = false;
          } else if (data.settings && data.settings.openTabIds) {
            try {
              const parsedTabs = typeof data.settings.openTabIds === "string"
                ? JSON.parse(data.settings.openTabIds)
                : data.settings.openTabIds;
              if (Array.isArray(parsedTabs) && parsedTabs.length > 0) {
                state.openTabIds = parsedTabs.map(Number).filter(Boolean);
                state.activeNoteId = state.openTabIds[0];
                state.isHomeActive = false;
              }
            } catch (_) {}
          }
        }

        if (data.settings && data.settings.panelWidths) {
          try {
            const parsedWidths = typeof data.settings.panelWidths === "string"
              ? JSON.parse(data.settings.panelWidths)
              : data.settings.panelWidths;
            if (parsedWidths && typeof parsedWidths === "object") {
              applyPanelWidths(parsedWidths, false);
            }
          } catch (_) {}
        }

        if (Array.isArray(data.reminders)) {
          state.reminders = data.reminders;
          persistRemindersLocal();
          if (state.isHomeActive) {
            renderHomeCalendar();
            renderHomeEventsList();
          }
        }

        if (Array.isArray(data.notes)) {
          applyNoteMetaOverlay(data.notes);
          state.notes = data.notes;
          localStorage.setItem("notejs_desktop_notion_v9", JSON.stringify(state.notes));
          const activeList = getActiveNotesList();
          if (state.activeNoteId && !activeList.some(n => n.id === state.activeNoteId)) {
            state.activeNoteId = activeList.length ? activeList[0].id : null;
          }
          ensureValidOpenTabs();
          renderFolders();
          renderNotesList();
          renderNoteTabs();
          if (state.isHomeActive) {
            renderHomePage();
          } else {
            loadActiveNote();
          }
          setSyncStatus("synced");
        }
      } catch (err) {
        setSyncStatus("offline");
      } finally {
        resolveCloudLocalReady();
      }
    }

    async function syncAllToPythonBackend() {
      const payload = {
        notes: state.notes,
        folders: state.folders,
        folderEmojis: state.folderEmojis,
        smartFolders: state.smartFolders || {},
        reminders: state.reminders || [],
        settings: {
          isLightMode: String(state.isLightMode),
          panelWidths: JSON.stringify(state.panelWidths || PANEL_WIDTH_DEFAULTS)
        },
        replaceAll: true
      };
      try {
        if (hasPyWebViewBridge() && typeof window.pywebview.api.sync_all === "function") {
          const res = await window.pywebview.api.sync_all(payload);
          setSyncStatus(res && res.ok ? "synced" : "offline");
          return;
        }
        const res = await fetch("/api/sync", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          setSyncStatus("synced");
        } else {
          setSyncStatus("offline");
        }
      } catch (_) {
        setSyncStatus("offline");
      }
    }

    async function syncNoteToPython(targetNote) {
      const note = targetNote || getActiveNote();
      if (!note) {
        setSyncStatus("synced");
        return;
      }
      recordLocalHistoryFallback(note, "Edición guardada");
      try {
        if (hasPyWebViewBridge() && typeof window.pywebview.api.save_note === "function") {
          const res = await window.pywebview.api.save_note(note);
          setSyncStatus(res && res.ok ? "synced" : "offline");
          if (state.isHistoryPanelOpen && note.id === state.activeNoteId) {
            refreshActiveNoteHistory();
          }
          return;
        }
        const res = await fetch("/api/notes", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ note })
        });
        if (res.ok) {
          setSyncStatus("synced");
          if (state.isHistoryPanelOpen && note.id === state.activeNoteId) {
            refreshActiveNoteHistory();
          }
        } else {
          setSyncStatus("offline");
          if (state.isHistoryPanelOpen && note.id === state.activeNoteId) {
            refreshActiveNoteHistory();
          }
        }
      } catch (_) {
        setSyncStatus("offline");
        if (state.isHistoryPanelOpen && note.id === state.activeNoteId) {
          refreshActiveNoteHistory();
        }
      }
    }

    function save(isUserTyping = false, targetNote = null) {
      setSyncStatus("saving");
      persistNoteMetaOverlay();
      localStorage.setItem("notejs_desktop_notion_v9", JSON.stringify(state.notes));

      if (syncTimeout) clearTimeout(syncTimeout);

      const noteToSave = targetNote || getActiveNote();
      if (window.NoteJSCloud) window.NoteJSCloud.changed();
      syncTimeout = setTimeout(() => {
        syncNoteToPython(noteToSave);
      }, isUserTyping ? 300 : 60);
    }

    function init() {
      ensureValidOpenTabs();
      initPanelResizers();
      initFocusSidebarPeek();
      initShortcutManager();
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      if (state.isHomeActive || !state.activeNoteId || !state.openTabIds || state.openTabIds.length === 0) {
        navigateToHome();
      } else {
        loadActiveNote();
      }
      renderSlashMenuItems("");
      document.addEventListener("selectionchange", handleSelectionChange);
      setupBlockDragAndDrop();
      setupRichEditorNoteDrop();
      setupTabBarDropTarget();
      attachEmbeddedNoteCardListeners();
      attachImageBlockListeners();
      setTimeout(renderAllInlineEquations, 120);
      initPythonBackendSync();
    }

    /* 1. Vista de Enfoque (Toggle ☰ / « / »), Menú Lateral Flotante ("Peek" Estilo Notion) y Divisores Redimensionables */
    let panelTransitionTimer = null;
    let focusPeekCloseTimer = null;
    let focusPeekReadyTimer = null;
    let focusPeekCooldownUntil = 0;

    function beginPanelTransition() {
      document.body.classList.remove('is-resizing-panels');
      document.body.classList.add('is-panel-animating');
    }

    function scheduleLayoutAdjustmentAfterTransition() {
      if (panelTransitionTimer) clearTimeout(panelTransitionTimer);
      panelTransitionTimer = setTimeout(() => {
        document.body.classList.remove('is-panel-animating');
        adjustEditorLayoutAfterTransition();
      }, 340);
    }

    function adjustEditorLayoutAfterTransition() {
      try {
        window.dispatchEvent(new Event('resize'));
      } catch (_) {}

      if (typeof handleSelectionChange === 'function') {
        handleSelectionChange();
      }

      const slashMenu = document.getElementById('slash-menu');
      if (slashMenu && slashMenu.classList.contains('open')) {
        const canvas = document.getElementById('rich-editor-canvas');
        if (canvas) {
          const rect = canvas.getBoundingClientRect();
          slashMenu.style.top = `${rect.top + 30}px`;
          slashMenu.style.left = `${Math.min(rect.left + 20, window.innerWidth - 340)}px`;
        }
      }
    }

    function checkFocusModeStateSync() {
      const folders = document.getElementById('panel-folders');
      const gallery = document.getElementById('panel-gallery');
      const toggleBtn = document.getElementById('btn-focus-mode');
      const tooltipLabel = document.getElementById('focus-toggle-tooltip-label');
      const sidebarCollapseBtn = document.getElementById('btn-collapse-sidebar');

      const isFoldersCollapsed = Boolean(folders && folders.classList.contains('collapsed'));
      const isGalleryCollapsed = Boolean(gallery && gallery.classList.contains('collapsed'));
      const bothCollapsed = isFoldersCollapsed && isGalleryCollapsed;

      state.isFocusMode = bothCollapsed;

      document.body.classList.toggle('is-sidebar-collapsed', isFoldersCollapsed);
      document.body.classList.toggle('is-focus-mode', bothCollapsed);

      if (toggleBtn) toggleBtn.classList.toggle('active', bothCollapsed);

      if (tooltipLabel) {
        tooltipLabel.textContent = isFoldersCollapsed
          ? 'Mantener barra lateral abierta'
          : 'Cerrar barra lateral';
      }
      if (sidebarCollapseBtn) {
        sidebarCollapseBtn.title = isFoldersCollapsed
          ? 'Mantener barra lateral abierta (Ctrl+\\)'
          : 'Cerrar barra lateral (Ctrl+\\)';
      }

      if (isFoldersCollapsed) {
        if (focusPeekReadyTimer) clearTimeout(focusPeekReadyTimer);
        focusPeekReadyTimer = setTimeout(() => {
          if (folders && folders.classList.contains('collapsed')) {
            folders.classList.add('focus-peek-ready');
          }
        }, 310);
      } else {
        if (focusPeekReadyTimer) clearTimeout(focusPeekReadyTimer);
        if (focusPeekCloseTimer) clearTimeout(focusPeekCloseTimer);
        if (folders) {
          folders.classList.remove('focus-peek-open');
          folders.classList.remove('focus-peek-ready');
        }
        document.body.classList.remove('is-focus-peek-open');
      }
    }

    function updatePanelRestoreButtons() {
      const folders = document.getElementById('panel-folders');
      const gallery = document.getElementById('panel-gallery');
      const btnReopen = document.getElementById('btn-reopen-panels');
      const reopenIcon = document.getElementById('reopen-panels-icon');

      const isFoldersCollapsed = Boolean(folders && folders.classList.contains('collapsed'));
      const isGalleryCollapsed = Boolean(gallery && gallery.classList.contains('collapsed'));

      if (!btnReopen) return;

      if (!isFoldersCollapsed && !isGalleryCollapsed) {
        btnReopen.style.display = 'none';
        return;
      }

      btnReopen.style.display = 'inline-flex';

      if (isFoldersCollapsed && isGalleryCollapsed) {
        // Están cerrados los 2: mostrar 2 flechas en el mismo icono
        btnReopen.title = 'Reabrir paneles cerrados (Carpetas y Notas)';
        if (reopenIcon) {
          reopenIcon.innerHTML = `
            <polyline points="7 18 13 12 7 6"></polyline>
            <polyline points="13 18 19 12 13 6"></polyline>
          `;
        }
      } else {
        // Está cerrado solo 1: mostrar 1 flecha en el mismo icono
        const panelName = isFoldersCollapsed ? 'panel de carpetas' : 'panel de notas';
        btnReopen.title = `Reabrir ${panelName}`;
        if (reopenIcon) {
          reopenIcon.innerHTML = `
            <polyline points="9 18 15 12 9 6"></polyline>
          `;
        }
      }
    }

    function handleReopenPanelsClick() {
      const folders = document.getElementById('panel-folders');
      const gallery = document.getElementById('panel-gallery');
      const isFoldersCollapsed = Boolean(folders && folders.classList.contains('collapsed'));
      const isGalleryCollapsed = Boolean(gallery && gallery.classList.contains('collapsed'));

      if (isFoldersCollapsed && isGalleryCollapsed) {
        toggleSidebar(true);
        toggleGallery(true);
      } else if (isFoldersCollapsed) {
        toggleSidebar(true);
      } else if (isGalleryCollapsed) {
        toggleGallery(true);
      }

      updatePanelRestoreButtons();
      checkFocusModeStateSync();
    }

    function openFocusSidebarPeek() {
      const folders = document.getElementById('panel-folders');
      if (!folders || !folders.classList.contains('collapsed')) return;
      if (Date.now() < focusPeekCooldownUntil) return;

      if (focusPeekCloseTimer) {
        clearTimeout(focusPeekCloseTimer);
        focusPeekCloseTimer = null;
      }

      if (!folders.classList.contains('focus-peek-ready')) {
        folders.classList.add('focus-peek-ready');
      }
      if (!folders.classList.contains('focus-peek-open')) {
        folders.classList.add('focus-peek-open');
        document.body.classList.add('is-focus-peek-open');
      }
    }

    function closeFocusSidebarPeek() {
      if (focusPeekCloseTimer) {
        clearTimeout(focusPeekCloseTimer);
        focusPeekCloseTimer = null;
      }
      const folders = document.getElementById('panel-folders');
      if (folders) {
        folders.classList.remove('focus-peek-open');
      }
      document.body.classList.remove('is-focus-peek-open');
    }

    function scheduleCloseFocusSidebarPeek(delayMs = 150) {
      if (focusPeekCloseTimer) clearTimeout(focusPeekCloseTimer);
      focusPeekCloseTimer = setTimeout(() => {
        if (document.body.classList.contains('is-dragging-note')) return;
        closeFocusSidebarPeek();
      }, delayMs);
    }

    function initFocusSidebarPeek() {
      const edgeSensor = document.getElementById('focus-sidebar-edge-sensor');
      const folders = document.getElementById('panel-folders');
      const toggleWrapper = document.getElementById('focus-toggle-btn-wrapper');

      if (edgeSensor) {
        edgeSensor.addEventListener('mouseenter', () => {
          openFocusSidebarPeek();
        });
        edgeSensor.addEventListener('mousemove', () => {
          openFocusSidebarPeek();
        });
      }

      if (toggleWrapper) {
        toggleWrapper.addEventListener('mouseenter', () => {
          if (folders && folders.classList.contains('collapsed')) {
            openFocusSidebarPeek();
          }
        });
        toggleWrapper.addEventListener('mouseleave', () => {
          if (folders && folders.classList.contains('collapsed') && folders.classList.contains('focus-peek-open')) {
            scheduleCloseFocusSidebarPeek(165);
          }
        });
      }

      if (folders) {
        folders.addEventListener('mouseenter', () => {
          if (folders.classList.contains('collapsed') && folders.classList.contains('focus-peek-open')) {
            if (focusPeekCloseTimer) {
              clearTimeout(focusPeekCloseTimer);
              focusPeekCloseTimer = null;
            }
          }
        });
        folders.addEventListener('mouseleave', (e) => {
          if (!folders.classList.contains('collapsed') || !folders.classList.contains('focus-peek-open')) return;
          if (toggleWrapper && e.relatedTarget && toggleWrapper.contains(e.relatedTarget)) return;
          scheduleCloseFocusSidebarPeek(145);
        });
      }

      document.addEventListener('mousemove', (e) => {
        if (!folders || !folders.classList.contains('collapsed')) return;

        // Si el ratón se acerca al extremo izquierdo de la pantalla (debajo de la barra de pestañas Chrome), abre el menú flotante
        if (e.clientX <= 16 && e.clientY >= 42) {
          openFocusSidebarPeek();
          return;
        }

        // Si el menú flotante está abierto y el ratón se aleja hacia la derecha fuera del menú y del botón superior
        if (folders.classList.contains('focus-peek-open')) {
          const rect = folders.getBoundingClientRect();
          const inSidebarBounds = (
            e.clientX <= rect.right + 14 &&
            e.clientY >= Math.max(38, rect.top - 48) &&
            e.clientY <= rect.bottom + 12
          );
          const inToggleBounds = Boolean(
            toggleWrapper &&
            e.target &&
            typeof e.target.closest === 'function' &&
            e.target.closest('#focus-toggle-btn-wrapper')
          );

          if (inSidebarBounds || inToggleBounds) {
            if (focusPeekCloseTimer) {
              clearTimeout(focusPeekCloseTimer);
              focusPeekCloseTimer = null;
            }
          } else {
            scheduleCloseFocusSidebarPeek(140);
          }
        }
      }, { passive: true });
    }

    function handleSidebarHeaderCollapseOrPin() {
      const folders = document.getElementById('panel-folders');
      if (!folders) return;
      // Si está en modo flotante (colapsado), el botón » fija la barra lateral abierta (restaura la vista normal)
      if (folders.classList.contains('collapsed')) {
        if (state.isFocusMode) {
          toggleFocusMode();
        } else {
          toggleSidebar(true);
        }
      } else {
        // Cuando está fija y el usuario pulsa « en la cabecera, colapsa los paneles como en Notion
        toggleFocusMode();
      }
    }

    function toggleFocusMode() {
      const folders = document.getElementById('panel-folders');
      const gallery = document.getElementById('panel-gallery');

      const isFullyCollapsed = Boolean(
        folders && folders.classList.contains('collapsed') &&
        gallery && gallery.classList.contains('collapsed')
      );
      const shouldCollapse = !isFullyCollapsed;
      state.isFocusMode = shouldCollapse;

      closeFocusSidebarPeek();
      if (folders) folders.classList.remove('focus-peek-ready');

      beginPanelTransition();

      if (shouldCollapse) {
        focusPeekCooldownUntil = Date.now() + 400;
        if (folders) folders.classList.add('collapsed');
        if (gallery) gallery.classList.add('collapsed');
        showToast('Vista de Enfoque activada · Acerca el cursor al borde izquierdo para ver el menú flotante', '⚡');
      } else {
        focusPeekCooldownUntil = 0;
        if (folders) folders.classList.remove('collapsed');
        if (gallery) gallery.classList.remove('collapsed');
        applyPanelWidths(state.panelWidths, false);
        showToast('Barra lateral fijada · Vista de Enfoque desactivada', '⚡');
      }

      checkFocusModeStateSync();
      updatePanelRestoreButtons();
      scheduleLayoutAdjustmentAfterTransition();
    }

    function toggleSidebar(forceExpand = null) {
      const folders = document.getElementById('panel-folders');
      if (!folders) return;

      const willExpand = forceExpand !== null ? Boolean(forceExpand) : folders.classList.contains('collapsed');
      closeFocusSidebarPeek();
      folders.classList.remove('focus-peek-ready');
      beginPanelTransition();

      if (willExpand) {
        focusPeekCooldownUntil = 0;
        folders.classList.remove('collapsed');
        applyPanelWidths(state.panelWidths, false);
        showToast('Barra de carpetas expandida', '📁');
      } else {
        focusPeekCooldownUntil = Date.now() + 400;
        folders.classList.add('collapsed');
        showToast('Barra de carpetas oculta · Acerca el cursor al borde izquierdo para abrirla flotante', '📁');
      }

      checkFocusModeStateSync();
      updatePanelRestoreButtons();
      scheduleLayoutAdjustmentAfterTransition();
    }

    function toggleGallery(forceExpand = null) {
      const gallery = document.getElementById('panel-gallery');
      if (!gallery) return;

      const willExpand = forceExpand !== null ? Boolean(forceExpand) : gallery.classList.contains('collapsed');
      beginPanelTransition();

      if (willExpand) {
        gallery.classList.remove('collapsed');
        applyPanelWidths(state.panelWidths, false);
        showToast('Galería de notas expandida', '🗂️');
      } else {
        gallery.classList.add('collapsed');
        showToast('Galería de notas oculta', '🗂️');
      }

      checkFocusModeStateSync();
      updatePanelRestoreButtons();
      scheduleLayoutAdjustmentAfterTransition();
    }

    function clampPanelWidth(panelKey, rawWidth) {
      const limits = PANEL_WIDTH_LIMITS[panelKey] || { min: 180, max: 500 };
      const numeric = Math.round(Number(rawWidth) || PANEL_WIDTH_DEFAULTS[panelKey] || 250);
      let clamped = Math.max(limits.min, Math.min(limits.max, numeric));

      const scaffold = document.getElementById('desktop-scaffold');
      const totalWidth = scaffold ? scaffold.clientWidth : window.innerWidth;
      if (totalWidth > 0) {
        const otherKey = panelKey === 'folders' ? 'gallery' : 'folders';
        const otherEl = document.getElementById(otherKey === 'folders' ? 'panel-folders' : 'panel-gallery');
        const isOtherCollapsed = Boolean(otherEl && otherEl.classList.contains('collapsed'));
        const otherWidth = isOtherCollapsed
          ? 0
          : ((state.panelWidths && Number(state.panelWidths[otherKey])) || PANEL_WIDTH_DEFAULTS[otherKey]);
        const historyPanel = document.getElementById('panel-history');
        const historyWidth = (historyPanel && state.isHistoryPanelOpen && !historyPanel.classList.contains('collapsed'))
          ? (historyPanel.offsetWidth || 320)
          : 0;
        const maxAvailable = totalWidth - otherWidth - historyWidth - PANEL_WIDTH_LIMITS.editorMin;
        if (maxAvailable >= limits.min) {
          clamped = Math.min(clamped, maxAvailable);
        }
      }
      return Math.max(limits.min, Math.round(clamped));
    }

    function persistPanelWidthsLocal() {
      try {
        localStorage.setItem('notejs_panel_widths_v1', JSON.stringify(state.panelWidths));
      } catch (_) {}
    }

    function savePanelWidthsToBackend() {
      persistPanelWidthsLocal();
      const serialized = JSON.stringify(state.panelWidths);
      if (hasPyWebViewBridge() && typeof window.pywebview.api.save_setting === 'function') {
        window.pywebview.api.save_setting('panelWidths', serialized).catch(() => {});
      } else {
        fetch('/api/settings', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ key: 'panelWidths', value: serialized })
        }).catch(() => {});
      }
    }

    function applyPanelWidths(widths = state.panelWidths, persist = false) {
      if (!state.panelWidths || typeof state.panelWidths !== 'object') {
        state.panelWidths = { ...PANEL_WIDTH_DEFAULTS };
      }

      const nextFolders = clampPanelWidth('folders', widths && widths.folders !== undefined ? widths.folders : state.panelWidths.folders);
      state.panelWidths.folders = nextFolders;
      const nextGallery = clampPanelWidth('gallery', widths && widths.gallery !== undefined ? widths.gallery : state.panelWidths.gallery);
      state.panelWidths.gallery = nextGallery;

      document.documentElement.style.setProperty('--folders-panel-width', `${nextFolders}px`);
      document.documentElement.style.setProperty('--gallery-panel-width', `${nextGallery}px`);

      const foldersSplitter = document.getElementById('splitter-folders-gallery');
      const foldersBadge = document.getElementById('resizer-badge-folders');
      if (foldersSplitter) {
        foldersSplitter.setAttribute('aria-valuenow', String(nextFolders));
        foldersSplitter.title = `Arrastra para ajustar Carpetas (${nextFolders} px) · Doble clic para restablecer (${PANEL_WIDTH_DEFAULTS.folders} px)`;
      }
      if (foldersBadge) {
        foldersBadge.textContent = `${nextFolders} px`;
      }

      const gallerySplitter = document.getElementById('splitter-gallery-editor');
      const galleryBadge = document.getElementById('resizer-badge-gallery');
      if (gallerySplitter) {
        gallerySplitter.setAttribute('aria-valuenow', String(nextGallery));
        gallerySplitter.title = `Arrastra para ajustar Galería (${nextGallery} px) · Doble clic para restablecer (${PANEL_WIDTH_DEFAULTS.gallery} px)`;
      }
      if (galleryBadge) {
        galleryBadge.textContent = `${nextGallery} px`;
      }

      if (persist) {
        savePanelWidthsToBackend();
      } else {
        persistPanelWidthsLocal();
      }
    }

    function resetPanelWidth(panelKey = 'all') {
      if (panelKey === 'folders') {
        applyPanelWidths({ ...state.panelWidths, folders: PANEL_WIDTH_DEFAULTS.folders }, true);
        showToast(`Ancho de Carpetas restablecido (${PANEL_WIDTH_DEFAULTS.folders} px)`, '↔️');
      } else if (panelKey === 'gallery') {
        applyPanelWidths({ ...state.panelWidths, gallery: PANEL_WIDTH_DEFAULTS.gallery }, true);
        showToast(`Ancho de Galería restablecido (${PANEL_WIDTH_DEFAULTS.gallery} px)`, '↔️');
      } else {
        applyPanelWidths({ ...PANEL_WIDTH_DEFAULTS }, true);
        showToast(`Anchos de paneles restablecidos (${PANEL_WIDTH_DEFAULTS.folders} px / ${PANEL_WIDTH_DEFAULTS.gallery} px)`, '↔️');
      }
    }

    function setPanelPresetWidth(panelKey, pxValue) {
      if (panelKey !== 'folders' && panelKey !== 'gallery') return;
      applyPanelWidths({ ...state.panelWidths, [panelKey]: pxValue }, true);
      const label = panelKey === 'folders' ? 'Carpetas' : 'Galería';
      showToast(`Ancho de ${label} ajustado a ${state.panelWidths[panelKey]} px`, '↔️');
    }

    function initPanelResizers() {
      applyPanelWidths(state.panelWidths, false);

      const resizers = document.querySelectorAll('.panel-resizer[data-resizer]');
      resizers.forEach(splitter => {
        const panelKey = splitter.getAttribute('data-resizer');
        const targetPanelId = panelKey === 'folders' ? 'panel-folders' : 'panel-gallery';

        let isDragging = false;
        let startX = 0;
        let startWidth = 0;

        const onPointerMove = (e) => {
          if (!isDragging) return;
          if (e.cancelable) e.preventDefault();
          const clientX = typeof e.clientX === 'number'
            ? e.clientX
            : (e.touches && e.touches[0] ? e.touches[0].clientX : startX);
          const deltaX = clientX - startX;
          const desiredWidth = startWidth + deltaX;
          applyPanelWidths({
            ...state.panelWidths,
            [panelKey]: desiredWidth
          }, false);
        };

        const onPointerUp = () => {
          if (!isDragging) return;
          isDragging = false;
          splitter.classList.remove('is-dragging');
          document.body.classList.remove('is-resizing-panels');
          window.removeEventListener('pointermove', onPointerMove);
          window.removeEventListener('pointerup', onPointerUp);
          window.removeEventListener('pointercancel', onPointerUp);
          savePanelWidthsToBackend();
        };

        splitter.addEventListener('pointerdown', (e) => {
          if (e.button !== undefined && e.button !== 0) return;
          if (state.isFocusMode) return;
          const panelEl = document.getElementById(targetPanelId);
          if (!panelEl || panelEl.classList.contains('collapsed')) return;

          e.preventDefault();
          closeCustomContextMenu();

          if (panelTransitionTimer) clearTimeout(panelTransitionTimer);
          document.body.classList.remove('is-panel-animating');

          isDragging = true;
          startX = e.clientX;
          startWidth = panelEl.getBoundingClientRect().width || state.panelWidths[panelKey] || PANEL_WIDTH_DEFAULTS[panelKey];

          splitter.classList.add('is-dragging');
          document.body.classList.add('is-resizing-panels');
          if (typeof splitter.setPointerCapture === 'function' && e.pointerId !== undefined) {
            try { splitter.setPointerCapture(e.pointerId); } catch (_) {}
          }

          window.addEventListener('pointermove', onPointerMove, { passive: false });
          window.addEventListener('pointerup', onPointerUp);
          window.addEventListener('pointercancel', onPointerUp);
        });

        splitter.addEventListener('dblclick', (e) => {
          e.preventDefault();
          e.stopPropagation();
          resetPanelWidth(panelKey);
        });

        splitter.addEventListener('keydown', (e) => {
          if (state.isFocusMode) return;
          const step = e.shiftKey ? 24 : 10;
          if (e.key === 'ArrowLeft') {
            e.preventDefault();
            applyPanelWidths({
              ...state.panelWidths,
              [panelKey]: (state.panelWidths[panelKey] || PANEL_WIDTH_DEFAULTS[panelKey]) - step
            }, true);
          } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            applyPanelWidths({
              ...state.panelWidths,
              [panelKey]: (state.panelWidths[panelKey] || PANEL_WIDTH_DEFAULTS[panelKey]) + step
            }, true);
          } else if (e.key === 'Home' || e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            resetPanelWidth(panelKey);
          }
        });
      });

      // Coordinar oyentes de fin de transición para ajustar layout al completar la animación
      const foldersEl = document.getElementById('panel-folders');
      const galleryEl = document.getElementById('panel-gallery');
      [foldersEl, galleryEl].forEach(panel => {
        if (panel) {
          panel.addEventListener('transitionend', (e) => {
            if (e.target === panel && (e.propertyName === 'width' || e.propertyName === 'max-width')) {
              document.body.classList.remove('is-panel-animating');
              adjustEditorLayoutAfterTransition();
            }
          });
        }
      });

      updatePanelRestoreButtons();

      window.addEventListener('resize', () => {
        if (!state.isFocusMode) {
          applyPanelWidths(state.panelWidths, false);
        }
      });
    }

    function handleSidebarFolderClick(folderName) {
      state.selectedFolder = folderName;
      state.selectedCollection = 'FOLDER';
      if (state.isHomeActive && !isTrashFolder(folderName)) {
        if (isMasterAllNotesFolder(folderName)) {
          clearHomeFolderFilter();
        } else {
          state.homeFolderFilter = folderName;
          renderHomeFoldersSearchRow();
          renderHomeNotesContent();
        }
        renderFolders();
        renderNotesList();
      } else {
        renderFolders();
        renderNotesList();
      }
    }

    function selectTrashFolder() {
      state.selectedFolder = TRASH_FOLDER_KEY;
      state.selectedCollection = 'TRASH';
      state.selectedTag = null;
      const gallery = document.getElementById('panel-gallery');
      if (gallery && gallery.classList.contains('collapsed')) {
        toggleGallery(true);
      }
      renderFolders();
      renderNotesList();
    }

    function toggleParentFolderCollapse(folderPath, event) {
      if (event) {
        event.stopPropagation();
        event.preventDefault();
      }
      if (!Array.isArray(state.collapsedParentFolders)) {
        state.collapsedParentFolders = [];
      }
      const idx = state.collapsedParentFolders.indexOf(folderPath);
      if (idx === -1) {
        state.collapsedParentFolders.push(folderPath);
      } else {
        state.collapsedParentFolders.splice(idx, 1);
      }
      try {
        localStorage.setItem('notejs_collapsed_folders_v1', JSON.stringify(state.collapsedParentFolders));
      } catch (_) {}
      renderFolders();
    }

    function isFolderHiddenByCollapsedAncestor(folderPath) {
      if (!folderPath || !Array.isArray(state.collapsedParentFolders) || !state.collapsedParentFolders.length) {
        return false;
      }
      return state.collapsedParentFolders.some(collapsedParent => folderPath.startsWith(collapsedParent + '/'));
    }

    /* Carpetas & Navegación (Soporte de Subcarpetas y Papelera en la Barra Lateral) */
    function renderFolders() {
      const container = document.getElementById('folders-list-container');
      if (!container) return;
      ensureMasterFolderFirst();
      const activeNotes = getActiveNotesList();
      const trashedNotes = getTrashedNotesList();

      const homeBtn = document.getElementById('fitem-sidebar-home');
      if (homeBtn) {
        homeBtn.classList.toggle('active', Boolean(state.isHomeActive && !state.isRemindersActive && !isTrashFolder(state.selectedFolder)));
      }

      const remindersBtn = document.getElementById('fitem-sidebar-reminders');
      const remindersBadge = document.getElementById('sidebar-reminders-count-badge');
      if (remindersBtn) {
        remindersBtn.classList.toggle('active', Boolean(state.isRemindersActive));
      }
      if (remindersBadge) {
        const pendingCount = (state.reminders || []).filter(r => !r.completed).length;
        remindersBadge.textContent = String(pendingCount);
      }

      const trashBtn = document.getElementById('fitem-sidebar-trash');
      const trashBadge = document.getElementById('trash-count-badge');
      if (trashBtn) {
        trashBtn.classList.toggle('active', Boolean(!state.isRemindersActive && isTrashFolder(state.selectedFolder)));
      }
      if (trashBadge) {
        trashBadge.textContent = String(trashedNotes.length);
      }

      container.innerHTML = state.folders.map(f => {
        const isMaster = isMasterAllNotesFolder(f);
        if (!isMaster && isFolderHiddenByCollapsedAncestor(f)) {
          return '';
        }
        const count = isMaster
          ? activeNotes.length
          : activeNotes.filter(n => noteBelongsToFolder(n, f)).length;
        const isAct = !isTrashFolder(state.selectedFolder) && state.selectedFolder !== null && !state.isRemindersActive && (
          isMaster
            ? ((state.isHomeActive && !state.homeFolderFilter && state.selectedFolder !== null) || (!state.isHomeActive && isMasterAllNotesFolder(state.selectedFolder)))
            : ((state.isHomeActive && state.homeFolderFilter === f) || (!state.isHomeActive && state.selectedFolder === f))
        );
        const folderEmoji = getFolderEmoji(f);
        const displayName = isMaster ? f : getFolderDisplayName(f);
        const depth = isMaster ? 0 : getFolderDepth(f);
        const subfolders = isMaster ? [] : getSubfoldersOf(f);
        const hasChildren = subfolders.length > 0;
        const isCollapsed = hasChildren && Array.isArray(state.collapsedParentFolders) && state.collapsedParentFolders.includes(f);

        const safeJsFolder = String(f).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        const safeHtmlFolder = String(f)
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;');
        const safeHtmlDisplayName = String(displayName)
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;');

        if (isMaster) {
          return `
            <button class="folder-item ${isAct ? 'active' : ''}" data-folder="${safeHtmlFolder}" data-master-folder="true" draggable="false" onclick="handleSidebarFolderClick('${safeJsFolder}')" title="Carpeta principal &quot;${safeHtmlFolder}&quot; (${count} notas) · Arrastra una subcarpeta aquí para moverla al nivel principal">
              <span class="folder-item-left">
                <span class="folder-emoji-badge" style="cursor:default;">${folderEmoji}</span>
                <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-weight:700;">${safeHtmlDisplayName}</span>
              </span>
              <span class="folder-item-right">
                <span class="folder-root-drop-badge">↑ Raíz</span>
                <span class="folder-count">${count}</span>
              </span>
            </button>
          `;
        }

        const isSmart = isSmartFolder(f);
        if (isSmart) {
          const smartCfg = getSmartFolderConfig(f);
          const rulesCount = smartCfg && Array.isArray(smartCfg.rules) ? smartCfg.rules.length : 0;
          const modeLabel = smartCfg && smartCfg.matchMode === 'any' ? 'OR' : 'AND';
          return `
            <button class="folder-item is-smart-folder-item ${isAct ? 'active' : ''}" data-folder="${safeHtmlFolder}" data-smart-folder="true" draggable="false" onclick="handleSidebarFolderClick('${safeJsFolder}')" title="Carpeta Inteligente &quot;${safeHtmlFolder}&quot; (${count} notas · ${rulesCount} reglas ${modeLabel}) · Consulta dinámica en tiempo real · Nivel raíz">
              <span class="folder-item-left">
                <span class="folder-emoji-badge smart-folder-emoji-badge" onclick="event.stopPropagation(); openSmartFolderModal('edit', '${safeJsFolder}');" title="Editar filtros de &quot;${safeHtmlFolder}&quot;">${folderEmoji}</span>
                <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${safeHtmlDisplayName}</span>
                <span class="smart-folder-sidebar-pill" title="Filtro dinámico (${modeLabel}) · Nivel raíz · No colaborativa">⚙️</span>
              </span>
              <span class="folder-item-right">
                <span class="folder-edit-emoji-hint" style="opacity:0.85;" onclick="event.stopPropagation(); openSmartFolderModal('edit', '${safeJsFolder}');" title="Configurar reglas de carpeta inteligente">⚙️</span>
                <span class="folder-count">${count}</span>
              </span>
            </button>
          `;
        }

        const indentPx = 10 + depth * 15;

        return `
          <button class="folder-item ${isAct ? 'active' : ''} ${depth > 0 ? 'is-subfolder-item' : ''}" data-folder="${safeHtmlFolder}" draggable="true" style="padding-left:${indentPx}px;" onclick="handleSidebarFolderClick('${safeJsFolder}')" title="Ver notas de &quot;${safeHtmlFolder}&quot; (${count} notas) · Arrastra sobre otra carpeta para convertirla en subcarpeta">
            <span class="folder-item-left">
              ${hasChildren ? `
                <span class="folder-tree-chevron ${isCollapsed ? 'collapsed' : ''}" onclick="toggleParentFolderCollapse('${safeJsFolder}', event)" title="${isCollapsed ? 'Expandir subcarpetas' : 'Contraer subcarpetas'}">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </span>
              ` : (depth > 0 ? '<span class="subfolder-tree-branch">└</span>' : '')}
              <span class="folder-emoji-badge" onclick="event.stopPropagation(); openFolderModal('emoji', '${safeJsFolder}');" title="Cambiar emoji de &quot;${safeHtmlFolder}&quot;">${folderEmoji}</span>
              <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${safeHtmlDisplayName}</span>
            </span>
            <span class="folder-item-right">
              <span class="folder-nest-drop-badge">↳ Subcarpeta</span>
              <span class="folder-add-subfolder-hint" onclick="event.stopPropagation(); openSubfolderModal('${safeJsFolder}');" title="Crear subcarpeta dentro de &quot;${safeHtmlDisplayName}&quot;">+</span>
              <span class="folder-edit-emoji-hint" onclick="event.stopPropagation(); openFolderModal('emoji', '${safeJsFolder}');" title="Personalizar icono emoji">😀</span>
              <span class="folder-count">${count}</span>
            </span>
          </button>
        `;
      }).join('');

      const folderSelectEl = document.getElementById('note-folder-select');
      if (folderSelectEl) {
        const activeNote = getActiveNote();
        const physicalFolders = state.folders.filter(f => !isSmartFolder(f));
        folderSelectEl.innerHTML = physicalFolders.map(f => {
          const safeHtmlFolder = String(f)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
          return `<option value="${safeHtmlFolder}">${getFolderEmoji(f)} ${safeHtmlFolder}</option>`;
        }).join('');
        if (activeNote) {
          folderSelectEl.value = getNotePrimaryDisplayFolder(activeNote);
        }
      }

      if (typeof renderNoteFoldersUI === 'function') {
        renderNoteFoldersUI();
      }

      attachFolderDropListeners();
    }

    function renderSidebarQuickNotes() {
      const listEl = document.getElementById('sidebar-recent-notes-container');
      const labelEl = document.getElementById('sidebar-pages-section-label');
      const homeBtn = document.getElementById('fitem-sidebar-home');
      if (homeBtn) {
        homeBtn.classList.toggle('active', Boolean(state.isHomeActive && !isTrashFolder(state.selectedFolder)));
      }
      if (!listEl) return;

      let notesToShow = [...getActiveNotesList()];
      if (state.selectedCollection === 'PINNED') {
        notesToShow = notesToShow.filter(n => n.isPinned);
        if (labelEl) labelEl.textContent = 'PÁGINAS FIJADAS';
      } else if (state.selectedCollection === 'FOLDER' && state.selectedFolder && !isTrashFolder(state.selectedFolder)) {
        notesToShow = notesToShow.filter(n => noteBelongsToFolder(n, state.selectedFolder));
        if (labelEl) labelEl.textContent = `EN ${String(getFolderDisplayName(state.selectedFolder)).toUpperCase()}`;
      } else if (state.selectedCollection === 'TAG' && state.selectedTag) {
        notesToShow = notesToShow.filter(n => {
          const raw = n.tags || '';
          const tagsArr = Array.isArray(raw)
            ? raw
            : raw.split(',').map(t => t.trim().toLowerCase().replace(/^#/, '')).filter(Boolean);
          return tagsArr.includes(state.selectedTag.toLowerCase());
        });
        if (labelEl) labelEl.textContent = `PÁGINAS #${String(state.selectedTag).toUpperCase()}`;
      } else {
        notesToShow.sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0));
        if (labelEl) labelEl.textContent = 'RECIENTES';
      }

      if (!notesToShow.length) {
        listEl.innerHTML = `<div style="padding:5px 8px; font-size:11.5px; color:var(--text-muted); font-style:italic;">Sin páginas en esta vista</div>`;
        return;
      }

      listEl.innerHTML = notesToShow.slice(0, 8).map(n => {
        const isSel = !state.isHomeActive && n.id === state.activeNoteId;
        const safeTitle = String(n.title || 'Nueva página')
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;');
        const emoji = n.emoji || '📝';
        return `
          <button type="button"
                  class="sidebar-note-item ${isSel ? 'active' : ''}"
                  onclick="handleGalleryNoteCardClick(event, ${n.id})"
                  title="${safeTitle}">
            <span class="sidebar-note-item-left">
              <span class="sidebar-note-emoji">${emoji}</span>
              <span class="sidebar-note-title">${safeTitle}</span>
            </span>
            ${n.isPinned ? '<span style="font-size:10px; opacity:0.75;">📌</span>' : ''}
          </button>
        `;
      }).join('');
    }

    function renderTagsInSidebar() {
      const container = document.getElementById('tags-list-container');
      if (!container) return;

      const tagCounts = {};
      state.notes.forEach(note => {
        const raw = note.tags || '';
        const tagsArr = Array.isArray(raw)
          ? raw
          : raw.split(',').map(t => t.trim().toLowerCase().replace(/^#/, '')).filter(Boolean);

        tagsArr.forEach(t => {
          if (t) {
            tagCounts[t] = (tagCounts[t] || 0) + 1;
          }
        });
      });

      const sortedTags = Object.keys(tagCounts).sort();
      if (!sortedTags.length) {
        container.innerHTML = `<div style="padding:6px 10px; font-size:11.5px; color:var(--text-muted); font-style:italic;">Sin etiquetas</div>`;
        return;
      }

      container.innerHTML = sortedTags.map(tag => {
        const count = tagCounts[tag];
        const isAct = (state.selectedTag === tag && state.selectedCollection === 'TAG');
        return `
          <button class="folder-item ${isAct ? 'active' : ''}" data-tag="${tag}" onclick="selectTag('${tag}')" title="Clic para filtrar · Suelta una nota aquí para añadir #${tag}">
            <span class="folder-item-left">
              <span style="color:var(--accent-amber); font-weight:800; font-size:13px;">#</span>
              <span>${tag}</span>
            </span>
            <span class="folder-count">${count}</span>
          </button>
        `;
      }).join('');
    }

    function selectTag(tag) {
      state.selectedTag = tag;
      state.selectedCollection = 'TAG';
      state.selectedFolder = null;
      document.getElementById('fitem-all').classList.remove('active');
      document.getElementById('fitem-pinned').classList.remove('active');
      renderFolders();
      renderNotesList();
    }

    let draggedSidebarFolderPath = null;
    let activeFolderDragGhostEl = null;
    let activeFolderNestPreviewTarget = null;
    let folderDragAutoExpandTimer = null;

    function clearFolderDragAutoExpandTimer() {
      if (folderDragAutoExpandTimer) {
        clearTimeout(folderDragAutoExpandTimer);
        folderDragAutoExpandTimer = null;
      }
    }

    function removeFolderNestPreviewSlot(immediate = false) {
      activeFolderNestPreviewTarget = null;
      clearFolderDragAutoExpandTimer();
      const existingSlots = document.querySelectorAll('.folder-nest-preview-slot');
      existingSlots.forEach(slot => {
        if (immediate) {
          slot.remove();
        } else {
          slot.classList.remove('open');
          slot.classList.add('closing');
          setTimeout(() => {
            if (slot.parentNode) slot.remove();
          }, 190);
        }
      });
    }

    function showFolderNestPreviewSlot(targetBtn, sourceFolderPath, targetFolderPath) {
      if (!targetBtn || !targetBtn.parentNode) return;
      const srcPath = String(sourceFolderPath || '').trim();
      const tgtPath = String(targetFolderPath || '').trim();
      if (!srcPath || !tgtPath) return;

      if (activeFolderNestPreviewTarget === tgtPath) {
        const currentSlot = targetBtn.parentNode.querySelector('.folder-nest-preview-slot:not(.closing)');
        if (currentSlot && currentSlot.previousElementSibling === targetBtn) {
          return;
        }
      }

      // Remove any previous preview slots immediately before inserting at the new target
      document.querySelectorAll('.folder-nest-preview-slot').forEach(el => el.remove());
      activeFolderNestPreviewTarget = tgtPath;

      const targetDepth = getFolderDepth(tgtPath);
      const previewIndentPx = 10 + (targetDepth + 1) * 15;
      const srcEmoji = getFolderEmoji(srcPath);
      const srcDisplayName = getFolderDisplayName(srcPath);

      const slot = document.createElement('div');
      slot.className = 'folder-nest-preview-slot';
      slot.setAttribute('aria-hidden', 'true');
      slot.style.paddingLeft = `${previewIndentPx}px`;
      slot.innerHTML = `
        <span class="folder-nest-preview-connector">└</span>
        <span class="folder-nest-preview-emoji">${srcEmoji}</span>
        <span class="folder-nest-preview-name">${escapeHtmlAttr(srcDisplayName)}</span>
        <span class="folder-nest-preview-pill">↳ Subcarpeta</span>
      `;

      targetBtn.insertAdjacentElement('afterend', slot);
      requestAnimationFrame(() => {
        slot.classList.add('open');
      });

      // Auto-expand collapsed parent folder if user hovers briefly while dragging a folder
      clearFolderDragAutoExpandTimer();
      if (Array.isArray(state.collapsedParentFolders) && state.collapsedParentFolders.includes(tgtPath)) {
        folderDragAutoExpandTimer = setTimeout(() => {
          if (draggedSidebarFolderPath && activeFolderNestPreviewTarget === tgtPath) {
            state.collapsedParentFolders = state.collapsedParentFolders.filter(p => p !== tgtPath);
            renderFolders();
            const refreshedTargetBtn = document.querySelector(`.folder-item[data-folder="${CSS.escape(tgtPath)}"]`);
            if (refreshedTargetBtn) {
              refreshedTargetBtn.classList.add('folder-nest-drag-over');
              activeFolderNestPreviewTarget = null;
              showFolderNestPreviewSlot(refreshedTargetBtn, srcPath, tgtPath);
            }
          }
        }, 520);
      }
    }

    function attachCustomFolderDragGhost(e, folderPath) {
      if (!e || !e.dataTransfer || typeof e.dataTransfer.setDragImage !== 'function') return;
      if (activeFolderDragGhostEl) {
        activeFolderDragGhostEl.remove();
        activeFolderDragGhostEl = null;
      }
      const ghost = document.createElement('div');
      ghost.className = 'note-drag-ghost folder-drag-ghost';
      const emoji = getFolderEmoji(folderPath);
      const displayName = getFolderDisplayName(folderPath);
      ghost.innerHTML = `
        <span>${emoji}</span>
        <span style="font-weight:700;">${escapeHtmlAttr(displayName)}</span>
        <span class="note-drag-ghost-folder">↳ Soltar sobre carpeta</span>
      `;
      document.body.appendChild(ghost);
      activeFolderDragGhostEl = ghost;
      e.dataTransfer.setDragImage(ghost, 16, 16);
    }

    function cleanupFolderDragStates() {
      draggedSidebarFolderPath = null;
      document.body.classList.remove('is-dragging-folder');
      removeFolderNestPreviewSlot(true);
      if (activeFolderDragGhostEl) {
        activeFolderDragGhostEl.remove();
        activeFolderDragGhostEl = null;
      }
      document.querySelectorAll('.folder-item.is-dragging-folder-source, .folder-item.folder-nest-drag-over, .folder-item.folder-root-drag-over, .folder-item.folder-drop-invalid').forEach(el => {
        el.classList.remove('is-dragging-folder-source', 'folder-nest-drag-over', 'folder-root-drag-over', 'folder-drop-invalid');
      });
      const secHeader = document.getElementById('folders-section-header');
      if (secHeader) secHeader.classList.remove('folder-root-drag-over');
    }

    function isFolderDragEvent(e) {
      if (draggedSidebarFolderPath) return true;
      if (e && e.dataTransfer && e.dataTransfer.types) {
        const types = Array.from(e.dataTransfer.types);
        if (types.includes('application/notejs-folder-path')) return true;
      }
      return false;
    }

    function extractDroppedFolderPath(e) {
      if (draggedSidebarFolderPath) return draggedSidebarFolderPath;
      if (e && e.dataTransfer) {
        const rawFolder = e.dataTransfer.getData('application/notejs-folder-path');
        if (rawFolder) return String(rawFolder).trim();
        const plain = e.dataTransfer.getData('text/plain');
        if (plain && String(plain).startsWith('folder:')) {
          return String(plain).slice('folder:'.length).trim();
        }
      }
      return null;
    }

    function canMoveFolderToParent(sourceFolder, targetParentFolder = '') {
      const src = String(sourceFolder || '').trim();
      const tgt = String(targetParentFolder || '').trim();
      if (!src || isMasterAllNotesFolder(src) || isTrashFolder(src)) return false;
      if (isTrashFolder(tgt)) return false;
      // Limitación del sistema: Las carpetas inteligentes no admiten subcarpetas ni pueden anidarse dentro de otras
      if (isSmartFolder(src) || isSmartFolder(tgt)) return false;
      const effectiveParent = isMasterAllNotesFolder(tgt) ? '' : tgt;
      if (src === effectiveParent) return false;
      if (effectiveParent && effectiveParent.startsWith(src + '/')) return false;
      const currentParent = getFolderParentPath(src);
      if (currentParent === effectiveParent) return false;
      const leaf = getFolderDisplayName(src);
      const candidatePath = effectiveParent ? `${effectiveParent}/${leaf}` : leaf;
      if (state.folders.some(f => f !== src && f.toLowerCase() === candidatePath.toLowerCase())) {
        return false;
      }
      return true;
    }

    function moveFolderHierarchy(sourceFolder, targetParentFolder = '') {
      const src = String(sourceFolder || '').trim();
      const rawTarget = String(targetParentFolder || '').trim();
      const targetParent = isMasterAllNotesFolder(rawTarget) ? '' : rawTarget;

      if (!src || isMasterAllNotesFolder(src) || isTrashFolder(src)) {
        showToast('La carpeta principal "Todas Las Notas" no se puede mover', '🔒');
        return false;
      }
      if (isSmartFolder(src)) {
        showToast('Las carpetas inteligentes siempre se ubican en el nivel raíz y no pueden ser subcarpetas', '⚙️');
        return false;
      }
      if (targetParent && isSmartFolder(targetParent)) {
        showToast('Las carpetas inteligentes no admiten subcarpetas', '⚙️');
        return false;
      }
      if (isTrashFolder(targetParent)) return false;
      if (src === targetParent) return false;

      if (targetParent && targetParent.startsWith(src + '/')) {
        showToast('No puedes mover una carpeta dentro de su propia subcarpeta', '⚠️');
        return false;
      }

      const leafName = getFolderDisplayName(src);
      const newPath = targetParent ? `${targetParent}/${leafName}` : leafName;

      if (newPath === src) {
        if (targetParent) {
          showToast(`"${leafName}" ya es subcarpeta de "${getFolderDisplayName(targetParent)}"`, '📂');
        } else {
          showToast(`"${leafName}" ya está en el nivel principal`, '📂');
        }
        return false;
      }

      if (state.folders.some(f => f !== src && f.toLowerCase() === newPath.toLowerCase())) {
        showToast(`Ya existe una carpeta llamada "${newPath}"`, '⚠️');
        return false;
      }

      const oldPrefix = src + '/';
      const newPrefix = newPath + '/';

      // 1. Actualizar rutas en state.folders (la carpeta y todas sus subcarpetas descendientes)
      state.folders = state.folders.map(f => {
        if (f === src) return newPath;
        if (f.startsWith(oldPrefix)) return newPrefix + f.slice(oldPrefix.length);
        return f;
      });

      // 2. Migrar iconos de emoji personalizados en state.folderEmojis
      if (state.folderEmojis && typeof state.folderEmojis === 'object') {
        const nextEmojis = {};
        Object.keys(state.folderEmojis).forEach(k => {
          if (k === src) {
            nextEmojis[newPath] = state.folderEmojis[k];
          } else if (k.startsWith(oldPrefix)) {
            nextEmojis[newPrefix + k.slice(oldPrefix.length)] = state.folderEmojis[k];
          } else {
            nextEmojis[k] = state.folderEmojis[k];
          }
        });
        state.folderEmojis = nextEmojis;
      }

      // 3. Actualizar estado de carpetas colapsadas y expandir automáticamente la carpeta destino
      if (Array.isArray(state.collapsedParentFolders)) {
        state.collapsedParentFolders = state.collapsedParentFolders
          .map(p => {
            if (p === src) return newPath;
            if (p.startsWith(oldPrefix)) return newPrefix + p.slice(oldPrefix.length);
            return p;
          })
          .filter(p => p !== targetParent);
        try {
          localStorage.setItem('notejs_collapsed_folders_v1', JSON.stringify(state.collapsedParentFolders));
        } catch (_) {}
      }

      // 4. Actualizar las carpetas asignadas en todas las notas que pertenecían a la carpeta o sus subcarpetas
      state.notes.forEach(n => {
        const currentFolders = getNoteUserFolders(n);
        let changed = false;
        const updated = currentFolders.map(f => {
          if (f === src) {
            changed = true;
            return newPath;
          }
          if (f.startsWith(oldPrefix)) {
            changed = true;
            return newPrefix + f.slice(oldPrefix.length);
          }
          return f;
        });
        if (changed) {
          setNoteFolders(n, updated);
          n.updatedAt = Date.now();
        }
      });

      // 5. Actualizar carpeta seleccionada y filtro activo de inicio si apuntaban a la ruta anterior
      if (state.selectedFolder === src) {
        state.selectedFolder = newPath;
      } else if (state.selectedFolder && state.selectedFolder.startsWith(oldPrefix)) {
        state.selectedFolder = newPrefix + state.selectedFolder.slice(oldPrefix.length);
      }

      if (state.homeFolderFilter === src) {
        state.homeFolderFilter = newPath;
      } else if (state.homeFolderFilter && state.homeFolderFilter.startsWith(oldPrefix)) {
        state.homeFolderFilter = newPrefix + state.homeFolderFilter.slice(oldPrefix.length);
      }

      // 6. Ordenar jerárquicamente y persistir en el sistema de almacenamiento (LocalStorage + SQLite/Peewee)
      ensureMasterFolderFirst();
      persistFoldersLocal();
      persistNoteMetaOverlay();
      localStorage.setItem('notejs_desktop_notion_v9', JSON.stringify(state.notes));
      setSyncStatus('saving');

      const movePayload = {
        sourceFolder: src,
        targetParentFolder: targetParent,
        folders: state.folders,
        folderEmojis: state.folderEmojis,
        notes: state.notes
      };

      if (hasPyWebViewBridge() && typeof window.pywebview.api.move_folder_hierarchy === 'function') {
        window.pywebview.api.move_folder_hierarchy(
          src,
          targetParent,
          state.folders,
          state.folderEmojis,
          state.notes
        ).then(res => setSyncStatus(res && res.ok ? 'synced' : 'offline')).catch(() => setSyncStatus('offline'));
      } else {
        fetch('/api/folders/move', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(movePayload)
        }).then(res => setSyncStatus(res.ok ? 'synced' : 'offline')).catch(() => {
          saveFoldersToBackend();
          syncAllToPythonBackend();
        });
      }

      // 7. Re-renderizar interfaz y resaltar la carpeta actualizada
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      if (state.isHomeActive) {
        renderHomePage();
      } else {
        loadActiveNote();
      }

      highlightFolderButtonOnDrop(newPath, 'data-folder');
      const fEmoji = getFolderEmoji(newPath);
      if (targetParent) {
        showToast(`"${fEmoji} ${leafName}" convertida en subcarpeta de "${getFolderDisplayName(targetParent)}"`, fEmoji);
      } else {
        showToast(`"${fEmoji} ${leafName}" movida al nivel principal`, fEmoji);
      }
      return true;
    }

    function extractDroppedNoteId(e) {
      if (draggedSidebarFolderPath) return null;
      let noteId = draggedListNoteId || draggedNoteCardId;
      if (!noteId && e && e.dataTransfer) {
        const rawFolder = e.dataTransfer.getData('application/notejs-folder-path');
        if (rawFolder) return null;
        const rawId = e.dataTransfer.getData('application/notejs-note-id') || e.dataTransfer.getData('text/plain');
        if (rawId && !String(rawId).startsWith('folder:')) {
          const parsed = Number(String(rawId).replace('note:', '').trim());
          if (parsed) noteId = parsed;
        }
      }
      return noteId ? Number(noteId) : null;
    }

    function highlightFolderButtonOnDrop(selectorVal, attrName = 'data-folder') {
      requestAnimationFrame(() => {
        const buttons = document.querySelectorAll(`.folder-item[${attrName}]`);
        buttons.forEach(btn => {
          if (btn.getAttribute(attrName) === selectorVal) {
            btn.classList.remove('folder-drop-success', 'folder-just-nested');
            void btn.offsetWidth;
            btn.classList.add('folder-drop-success', 'folder-just-nested');
            setTimeout(() => btn.classList.remove('folder-drop-success', 'folder-just-nested'), 750);
          }
        });
      });
    }

    function attachFolderDropListeners() {
      const clearOtherFolderHighlights = (activeBtn) => {
        document.querySelectorAll('.folder-item.folder-drag-over, .folder-item.folder-nest-drag-over, .folder-item.folder-root-drag-over, .folder-item.folder-drop-invalid').forEach(el => {
          if (el !== activeBtn) {
            el.classList.remove('folder-drag-over', 'folder-nest-drag-over', 'folder-root-drag-over', 'folder-drop-invalid');
          }
        });
        if (!activeBtn || !activeBtn.dataset || activeBtn.dataset.folder !== activeFolderNestPreviewTarget) {
          removeFolderNestPreviewSlot();
        }
      };

      const foldersListContainer = document.getElementById('folders-list-container');
      if (foldersListContainer) {
        foldersListContainer.ondragleave = function(e) {
          if (e.relatedTarget && foldersListContainer.contains(e.relatedTarget)) return;
          removeFolderNestPreviewSlot();
        };
      }

      // 0. Encabezado "CARPETAS" (#folders-section-header) como zona para promover una subcarpeta al nivel raíz
      const sectionHeader = document.getElementById('folders-section-header');
      if (sectionHeader) {
        sectionHeader.ondragenter = function(e) {
          if (!isFolderDragEvent(e)) return;
          e.preventDefault();
          e.stopPropagation();
          clearOtherFolderHighlights(null);
          if (draggedSidebarFolderPath && getFolderDepth(draggedSidebarFolderPath) > 0) {
            sectionHeader.classList.add('folder-root-drag-over');
          }
        };
        sectionHeader.ondragover = function(e) {
          if (!isFolderDragEvent(e)) return;
          e.preventDefault();
          e.stopPropagation();
          if (draggedSidebarFolderPath && getFolderDepth(draggedSidebarFolderPath) > 0) {
            if (e.dataTransfer) e.dataTransfer.dropEffect = 'move';
            sectionHeader.classList.add('folder-root-drag-over');
          } else {
            if (e.dataTransfer) e.dataTransfer.dropEffect = 'none';
          }
        };
        sectionHeader.ondragleave = function(e) {
          if (e.relatedTarget && sectionHeader.contains(e.relatedTarget)) return;
          sectionHeader.classList.remove('folder-root-drag-over');
        };
        sectionHeader.ondrop = function(e) {
          sectionHeader.classList.remove('folder-root-drag-over');
          const droppedFolder = extractDroppedFolderPath(e);
          if (!droppedFolder) return;
          e.preventDefault();
          e.stopPropagation();
          cleanupFolderDragStates();
          moveFolderHierarchy(droppedFolder, '');
        };
      }

      // 1. Carpetas específicas: arrastrar una carpeta sobre otra para convertirla en subcarpeta, o soltar una nota
      const folderButtons = document.querySelectorAll('.folder-item[data-folder]');
      folderButtons.forEach(btn => {
        const folderName = btn.dataset.folder;
        const isMaster = isMasterAllNotesFolder(folderName);

        if (!isMaster) {
          btn.ondragstart = function(e) {
            e.stopPropagation();
            closeCustomContextMenu();
            draggedSidebarFolderPath = folderName;
            if (e.dataTransfer) {
              e.dataTransfer.effectAllowed = 'move';
              e.dataTransfer.setData('application/notejs-folder-path', folderName);
              e.dataTransfer.setData('text/plain', 'folder:' + folderName);
            }
            attachCustomFolderDragGhost(e, folderName);
            document.body.classList.add('is-dragging-folder');
            setTimeout(() => {
              btn.classList.add('is-dragging-folder-source');
            }, 10);
          };

          btn.ondragend = function() {
            cleanupFolderDragStates();
          };
        }

        btn.ondragenter = function(e) {
          e.preventDefault();
          e.stopPropagation();
          clearOtherFolderHighlights(btn);

          if (isFolderDragEvent(e)) {
            const srcFolder = draggedSidebarFolderPath;
            if (srcFolder === folderName) {
              removeFolderNestPreviewSlot();
              return;
            }
            if (isMaster) {
              removeFolderNestPreviewSlot();
              if (srcFolder && getFolderDepth(srcFolder) > 0) {
                btn.classList.add('folder-root-drag-over');
              } else {
                btn.classList.add('folder-drop-invalid');
              }
            } else if (!srcFolder || canMoveFolderToParent(srcFolder, folderName)) {
              btn.classList.add('folder-nest-drag-over');
              if (srcFolder) {
                showFolderNestPreviewSlot(btn, srcFolder, folderName);
              }
            } else {
              removeFolderNestPreviewSlot();
              btn.classList.add('folder-drop-invalid');
            }
          } else {
            btn.classList.add('folder-drag-over');
          }
        };

        btn.ondragover = function(e) {
          e.preventDefault();
          e.stopPropagation();

          if (isFolderDragEvent(e)) {
            const srcFolder = draggedSidebarFolderPath;
            if (srcFolder === folderName) {
              if (e.dataTransfer) e.dataTransfer.dropEffect = 'none';
              removeFolderNestPreviewSlot();
              return;
            }
            if (isMaster) {
              removeFolderNestPreviewSlot();
              if (srcFolder && getFolderDepth(srcFolder) > 0) {
                if (e.dataTransfer) e.dataTransfer.dropEffect = 'move';
                if (!btn.classList.contains('folder-root-drag-over')) {
                  clearOtherFolderHighlights(btn);
                  btn.classList.add('folder-root-drag-over');
                }
              } else {
                if (e.dataTransfer) e.dataTransfer.dropEffect = 'none';
                btn.classList.add('folder-drop-invalid');
              }
            } else if (!srcFolder || canMoveFolderToParent(srcFolder, folderName)) {
              if (e.dataTransfer) e.dataTransfer.dropEffect = 'move';
              if (!btn.classList.contains('folder-nest-drag-over')) {
                clearOtherFolderHighlights(btn);
                btn.classList.add('folder-nest-drag-over');
              }
              if (srcFolder) {
                showFolderNestPreviewSlot(btn, srcFolder, folderName);
              }
            } else {
              if (e.dataTransfer) e.dataTransfer.dropEffect = 'none';
              removeFolderNestPreviewSlot();
              if (!btn.classList.contains('folder-drop-invalid')) {
                clearOtherFolderHighlights(btn);
                btn.classList.add('folder-drop-invalid');
              }
            }
          } else {
            if (e.dataTransfer) e.dataTransfer.dropEffect = 'move';
            if (!btn.classList.contains('folder-drag-over')) {
              clearOtherFolderHighlights(btn);
              btn.classList.add('folder-drag-over');
            }
          }
        };

        btn.ondragleave = function(e) {
          if (e.relatedTarget && btn.contains(e.relatedTarget)) return;
          btn.classList.remove('folder-drag-over', 'folder-nest-drag-over', 'folder-root-drag-over', 'folder-drop-invalid');
          if (activeFolderNestPreviewTarget === folderName) {
            removeFolderNestPreviewSlot();
          }
        };

        btn.ondrop = function(e) {
          e.preventDefault();
          e.stopPropagation();
          btn.classList.remove('folder-drag-over', 'folder-nest-drag-over', 'folder-root-drag-over', 'folder-drop-invalid');

          const droppedFolder = extractDroppedFolderPath(e);
          if (droppedFolder) {
            cleanupFolderDragStates();
            if (droppedFolder === folderName) return;
            if (isMaster) {
              if (getFolderDepth(droppedFolder) > 0) {
                moveFolderHierarchy(droppedFolder, '');
              } else {
                showToast('Arrastra la carpeta sobre otra carpeta para convertirla en subcarpeta', '📂');
              }
            } else {
              moveFolderHierarchy(droppedFolder, folderName);
            }
            return;
          }

          const noteId = extractDroppedNoteId(e);
          cleanupNoteListDragStates();
          if (!noteId) return;

          moveNoteToFolder(noteId, folderName);
        };
      });

      // 2. Colección "Notas fijadas" (#fitem-pinned) para fijar una nota al soltarla
      const pinnedBtn = document.getElementById('fitem-pinned');
      if (pinnedBtn) {
        pinnedBtn.title = 'Ver notas fijadas · Suelta una nota aquí para fijarla 📌';
        pinnedBtn.ondragenter = function(e) {
          e.preventDefault();
          e.stopPropagation();
          clearOtherFolderHighlights(pinnedBtn);
          pinnedBtn.classList.add('folder-drag-over');
        };
        pinnedBtn.ondragover = function(e) {
          e.preventDefault();
          e.stopPropagation();
          if (e.dataTransfer) e.dataTransfer.dropEffect = 'move';
          pinnedBtn.classList.add('folder-drag-over');
        };
        pinnedBtn.ondragleave = function(e) {
          if (e.relatedTarget && pinnedBtn.contains(e.relatedTarget)) return;
          pinnedBtn.classList.remove('folder-drag-over');
        };
        pinnedBtn.ondrop = function(e) {
          e.preventDefault();
          e.stopPropagation();
          pinnedBtn.classList.remove('folder-drag-over');

          const noteId = extractDroppedNoteId(e);
          cleanupNoteListDragStates();
          if (!noteId) return;

          const note = state.notes.find(n => n.id === noteId);
          if (!note) return;
          note.isPinned = true;
          note.updatedAt = Date.now();
          save(false, note);
          renderFolders();
          renderNotesList();
          if (state.activeNoteId === noteId) loadActiveNote();
          const pinnedBtnEl = document.getElementById('fitem-pinned');
          if (pinnedBtnEl) {
            pinnedBtnEl.classList.remove('folder-drop-success');
            void pinnedBtnEl.offsetWidth;
            pinnedBtnEl.classList.add('folder-drop-success');
            setTimeout(() => pinnedBtnEl.classList.remove('folder-drop-success'), 700);
          }
          showToast(`Nota "${note.title || 'Sin título'}" añadida a Notas fijadas`, '📌');
        };
      }

      // 3. Etiquetas en el panel izquierdo (.folder-item[data-tag]) para asignar etiqueta al soltar
      const tagButtons = document.querySelectorAll('.folder-item[data-tag]');
      tagButtons.forEach(btn => {
        const tagName = btn.dataset.tag;
        btn.ondragenter = function(e) {
          e.preventDefault();
          e.stopPropagation();
          clearOtherFolderHighlights(btn);
          btn.classList.add('folder-drag-over');
        };
        btn.ondragover = function(e) {
          e.preventDefault();
          e.stopPropagation();
          if (e.dataTransfer) e.dataTransfer.dropEffect = 'copy';
          btn.classList.add('folder-drag-over');
        };
        btn.ondragleave = function(e) {
          if (e.relatedTarget && btn.contains(e.relatedTarget)) return;
          btn.classList.remove('folder-drag-over');
        };
        btn.ondrop = function(e) {
          e.preventDefault();
          e.stopPropagation();
          btn.classList.remove('folder-drag-over');

          const noteId = extractDroppedNoteId(e);
          cleanupNoteListDragStates();
          if (!noteId) return;

          assignTagToNoteByDrop(noteId, tagName);
        };
      });
      // 4. Papelera (#fitem-sidebar-trash) para enviar una nota a la papelera al soltarla
      const trashBtn = document.getElementById('fitem-sidebar-trash');
      if (trashBtn) {
        trashBtn.ondragenter = function(e) {
          e.preventDefault();
          e.stopPropagation();
          clearOtherFolderHighlights(trashBtn);
          trashBtn.classList.add('folder-drag-over');
        };
        trashBtn.ondragover = function(e) {
          e.preventDefault();
          e.stopPropagation();
          if (e.dataTransfer) e.dataTransfer.dropEffect = 'move';
          trashBtn.classList.add('folder-drag-over');
        };
        trashBtn.ondragleave = function(e) {
          if (e.relatedTarget && trashBtn.contains(e.relatedTarget)) return;
          trashBtn.classList.remove('folder-drag-over');
        };
        trashBtn.ondrop = function(e) {
          e.preventDefault();
          e.stopPropagation();
          trashBtn.classList.remove('folder-drag-over');
          const noteId = extractDroppedNoteId(e);
          cleanupNoteListDragStates();
          if (!noteId) return;
          deleteNoteById(noteId);
        };
      }
    }

    function assignTagToNoteByDrop(noteId, tagName) {
      const note = state.notes.find(n => n.id === Number(noteId));
      if (!note || !tagName) return;
      const cleanTag = tagName.trim().toLowerCase().replace(/^#/, '');
      const existing = (note.tags || '')
        .split(',')
        .map(t => t.trim().replace(/^#/, ''))
        .filter(Boolean);
      if (existing.some(t => t.toLowerCase() === cleanTag)) {
        showToast(`La nota "${note.title || 'Sin título'}" ya tiene #${cleanTag}`, '🏷️');
        return;
      }
      existing.push(cleanTag);
      note.tags = existing.join(', ');
      note.updatedAt = Date.now();
      save(false, note);
      renderFolders();
      renderNotesList();
      if (state.activeNoteId === note.id) loadActiveNote();
      highlightFolderButtonOnDrop(tagName, 'data-tag');
      showToast(`Etiqueta #${cleanTag} añadida a "${note.title || 'Sin título'}"`, '🏷️');
    }

    function moveNoteToFolder(noteId, folderName, allowToggle = false) {
      const numericId = Number(noteId);
      const note = state.notes.find(n => n.id === numericId);
      if (!note || !folderName) return;

      if (isMasterAllNotesFolder(folderName)) {
        highlightFolderButtonOnDrop(folderName, 'data-folder');
        showToast(`Todas las notas pertenecen siempre a "${MASTER_ALL_NOTES_FOLDER}"`, '🗂️');
        return;
      }

      if (isSmartFolder(folderName)) {
        highlightFolderButtonOnDrop(folderName, 'data-folder');
        showToast(`"${folderName}" es una Carpeta Inteligente (filtro dinámico en tiempo real, no almacena notas físicamente)`, '⚙️');
        return;
      }

      const currentUserFolders = getNoteUserFolders(note);
      const alreadyInFolder = currentUserFolders.includes(folderName);

      if (alreadyInFolder && !allowToggle) {
        highlightFolderButtonOnDrop(folderName, 'data-folder');
        showToast(`La nota "${note.title || 'Sin título'}" ya pertenece a "${folderName}"`, '📂');
        return;
      }

      let updatedFolders;
      if (alreadyInFolder && allowToggle) {
        updatedFolders = currentUserFolders.filter(f => f !== folderName);
      } else {
        updatedFolders = [...currentUserFolders, folderName];
      }

      setNoteFolders(note, updatedFolders);
      note.updatedAt = Date.now();

      // Actualizar tarjetas incrustadas en el lienzo activo si hacen referencia a esta nota
      document.querySelectorAll(`.note-embedded-card[data-note-id="${numericId}"] .embedded-card-folder`).forEach(el => {
        el.textContent = getNotePrimaryDisplayFolder(note);
      });

      save(false, note);

      renderFolders();
      renderNotesList();
      if (state.isHomeActive) {
        renderHomeFoldersSearchRow();
        renderHomeNotesContent();
      }

      if (state.activeNoteId === numericId) {
        loadActiveNote();
      }

      highlightFolderButtonOnDrop(folderName, 'data-folder');
      const fEmoji = getFolderEmoji(folderName);
      if (alreadyInFolder && allowToggle) {
        showToast(`Carpeta "${fEmoji} ${folderName}" quitada de "${note.title || 'Sin título'}"`, '📂');
      } else {
        showToast(`Nota "${note.title || 'Sin título'}" añadida a ${fEmoji} ${folderName}`, fEmoji);
      }
    }

    function toggleNoteFolderMembership(noteId, folderName) {
      moveNoteToFolder(noteId, folderName, true);
      if (typeof renderNoteFoldersUI === 'function') {
        renderNoteFoldersUI();
      }
      if (typeof renderNoteFoldersPopoverContent === 'function') {
        renderNoteFoldersPopoverContent();
      }
    }

    function selectCollection(col) {
      state.selectedCollection = col;
      state.selectedFolder = null;
      state.selectedTag = null;
      document.getElementById('fitem-all')?.classList.toggle('active', col === 'ALL');
      document.getElementById('fitem-pinned')?.classList.toggle('active', col === 'PINNED');
      renderFolders();
      renderNotesList();
    }

    function selectFolder(folder) {
      state.selectedFolder = folder || MASTER_ALL_NOTES_FOLDER;
      state.selectedCollection = 'FOLDER';
      state.selectedTag = null;
      document.getElementById('fitem-all')?.classList.remove('active');
      document.getElementById('fitem-pinned')?.classList.remove('active');
      renderFolders();
      renderNotesList();
    }

    function setListViewMode(mode) {
      state.isGridView = (mode === 'grid');
      document.getElementById('vbtn-grid').classList.toggle('active', state.isGridView);
      document.getElementById('vbtn-list').classList.toggle('active', !state.isGridView);
      const container = document.getElementById('notes-list-container');
      container.className = 'notes-list-scroll ' + (state.isGridView ? 'grid-mode' : '');
    }

    function toggleNotesSearch(forceState) {
      const wrapper = document.getElementById('notes-search-wrapper');
      const btn = document.getElementById('btn-toggle-search');
      const input = document.getElementById('notes-search-input');
      if (!wrapper) return;

      const willOpen = typeof forceState === 'boolean' ? forceState : !wrapper.classList.contains('open');
      wrapper.classList.toggle('open', willOpen);
      if (btn) btn.classList.toggle('active', willOpen);

      if (willOpen) {
        setTimeout(() => {
          if (input) {
            input.focus();
            input.select();
          }
        }, 40);
      } else {
        if (input && input.value) {
          input.value = '';
          renderNotesList();
        }
      }
    }

    function clearAndCloseNotesSearch() {
      const input = document.getElementById('notes-search-input');
      if (input && input.value) {
        input.value = '';
        renderNotesList();
        input.focus();
      } else {
        toggleNotesSearch(false);
      }
    }

    function handleNotesSearchKeydown(e) {
      if (e.key === 'Escape') {
        e.preventDefault();
        const input = document.getElementById('notes-search-input');
        if (input) input.value = '';
        renderNotesList();
        toggleNotesSearch(false);
      }
    }

    /* ============================================================================
       BÚSQUEDA DENTRO DE LA NOTA (F3 / Ctrl+F estilo navegador)
       ============================================================================ */
    let inNoteSearchMatches = [];
    let inNoteSearchCurrentIdx = -1;

    function toggleInNoteSearch() {
      const bar = document.getElementById('in-note-search-bar');
      if (!bar) return;
      if (bar.style.display === 'none' || !bar.style.display) {
        openInNoteSearch();
      } else {
        closeInNoteSearch();
      }
    }

    function openInNoteSearch() {
      const bar = document.getElementById('in-note-search-bar');
      const input = document.getElementById('in-note-search-input');
      if (!bar) return;

      bar.style.display = 'block';
      setTimeout(() => {
        if (input) {
          input.focus();
          input.select();
          if (input.value) {
            handleInNoteSearch(input.value);
          }
        }
      }, 50);
    }

    function closeInNoteSearch() {
      const bar = document.getElementById('in-note-search-bar');
      if (bar) bar.style.display = 'none';
      unmarkInNoteSearch();
      inNoteSearchMatches = [];
      inNoteSearchCurrentIdx = -1;
      const counter = document.getElementById('in-note-search-counter');
      if (counter) counter.textContent = '0/0';
    }

    function unmarkInNoteSearch() {
      const canvas = document.getElementById('rich-editor-canvas');
      if (!canvas) return;
      const marks = canvas.querySelectorAll('mark.in-note-search-match');
      marks.forEach(mark => {
        const parent = mark.parentNode;
        if (parent) {
          parent.replaceChild(document.createTextNode(mark.textContent), mark);
          parent.normalize();
        }
      });
    }

    function handleInNoteSearch(query) {
      unmarkInNoteSearch();
      inNoteSearchMatches = [];
      inNoteSearchCurrentIdx = -1;

      const counter = document.getElementById('in-note-search-counter');
      const cleanQuery = (query || '').trim();

      if (!cleanQuery) {
        if (counter) counter.textContent = '0/0';
        return;
      }

      const canvas = document.getElementById('rich-editor-canvas');
      if (!canvas) return;

      const walker = document.createTreeWalker(canvas, NodeFilter.SHOW_TEXT, null, false);
      const textNodes = [];
      let currentNode;
      while ((currentNode = walker.nextNode())) {
        if (currentNode.nodeValue && currentNode.nodeValue.toLowerCase().includes(cleanQuery.toLowerCase())) {
          textNodes.push(currentNode);
        }
      }

      const lowerQuery = cleanQuery.toLowerCase();
      const qLen = cleanQuery.length;

      textNodes.forEach(node => {
        const text = node.nodeValue;
        let lower = text.toLowerCase();
        let idx = lower.indexOf(lowerQuery);
        if (idx === -1) return;

        const frag = document.createDocumentFragment();
        let lastIdx = 0;

        while (idx !== -1) {
          if (idx > lastIdx) {
            frag.appendChild(document.createTextNode(text.substring(lastIdx, idx)));
          }
          const mark = document.createElement('mark');
          mark.className = 'in-note-search-match';
          mark.textContent = text.substring(idx, idx + qLen);
          frag.appendChild(mark);

          lastIdx = idx + qLen;
          idx = lower.indexOf(lowerQuery, lastIdx);
        }

        if (lastIdx < text.length) {
          frag.appendChild(document.createTextNode(text.substring(lastIdx)));
        }

        if (node.parentNode) {
          node.parentNode.replaceChild(frag, node);
        }
      });

      inNoteSearchMatches = Array.from(canvas.querySelectorAll('mark.in-note-search-match'));

      if (inNoteSearchMatches.length > 0) {
        inNoteSearchCurrentIdx = 0;
        inNoteSearchMatches[0].classList.add('current-match');
        inNoteSearchMatches[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
        if (counter) counter.textContent = `1/${inNoteSearchMatches.length}`;
      } else {
        if (counter) counter.textContent = '0/0';
      }
    }

    function inNoteSearchNav(dir) {
      if (!inNoteSearchMatches.length) return;

      if (inNoteSearchCurrentIdx >= 0 && inNoteSearchMatches[inNoteSearchCurrentIdx]) {
        inNoteSearchMatches[inNoteSearchCurrentIdx].classList.remove('current-match');
      }

      const total = inNoteSearchMatches.length;
      inNoteSearchCurrentIdx = (inNoteSearchCurrentIdx + dir + total) % total;

      const targetMatch = inNoteSearchMatches[inNoteSearchCurrentIdx];
      if (targetMatch) {
        targetMatch.classList.add('current-match');
        targetMatch.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }

      const counter = document.getElementById('in-note-search-counter');
      if (counter) counter.textContent = `${inNoteSearchCurrentIdx + 1}/${total}`;
    }

    function handleInNoteSearchKeydown(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        inNoteSearchNav(e.shiftKey ? -1 : 1);
      } else if (e.key === 'Escape') {
        e.preventDefault();
        closeInNoteSearch();
      } else if (e.key === 'F3') {
        e.preventDefault();
        inNoteSearchNav(e.shiftKey ? -1 : 1);
      }
    }

    let smartFolderQuerySeq = 0;

    function buildNoteCardHtml(n, viewingTrash = false) {
      const isSel = !n.isTrashed && n.id === state.activeNoteId;
      const dateStr = new Date(n.trashedAt || n.updatedAt || Date.now()).toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
      const emoji = n.emoji || '📝';
      const cleanSnippet = getNotePreviewText(n);
      const noteTags = extractNoteTagsList(n);
      const tagsBadgesHtml = noteTags.slice(0, 2).map(t => `<span style="background:var(--accent-amber-soft); color:var(--accent-amber); padding:1px 5px; border-radius:4px; font-size:9.5px; font-weight:700;">#${t}</span>`).join(' ');

      const userFolders = getNoteUserFolders(n);
      const folderBadgesHtml = userFolders.length > 0
        ? userFolders.slice(0, 2).map(f => `<span class="note-card-folder-pill" title="Ubicación real: ${escapeHtmlAttr(f)}">${getFolderEmoji(f)} ${escapeHtmlAttr(getFolderDisplayName(f))}</span>`).join(' ') + (userFolders.length > 2 ? `<span class="note-card-folder-pill">+${userFolders.length - 2}</span>` : '')
        : `<span class="note-card-folder-pill" title="En Todas Las Notas">${getFolderEmoji(MASTER_ALL_NOTES_FOLDER)} ${MASTER_ALL_NOTES_FOLDER}</span>`;

      const cardColorMap = {
        amber: 'border-left: 4px solid #f59e0b; background: rgba(245, 158, 11, 0.07);',
        blue: 'border-left: 4px solid #3b82f6; background: rgba(59, 130, 246, 0.08);',
        green: 'border-left: 4px solid #10b981; background: rgba(16, 185, 129, 0.08);',
        purple: 'border-left: 4px solid #a855f7; background: rgba(168, 85, 247, 0.08);',
        rose: 'border-left: 4px solid #f43f5e; background: rgba(244, 63, 94, 0.08);'
      };
      const customCardStyle = (n.cardColor && cardColorMap[n.cardColor]) ? cardColorMap[n.cardColor] : '';
      const isOpenInTab = !n.isTrashed && Array.isArray(state.openTabIds) && state.openTabIds.includes(n.id);

      if (viewingTrash) {
        return `
          <div class="note-item-card trashed-note-card" 
               id="note-card-${n.id}" 
               data-note-id="${n.id}"
               style="${customCardStyle}"
               title="Nota en la papelera · Usa Restaurar para recuperarla o Eliminar definitivamente">
            <div class="note-card-inner">
              <div class="note-card-main-content" style="width:100%;">
                <div class="note-item-title" style="justify-content:space-between;">
                  <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; flex:1;">${emoji} ${n.title || 'Sin título'}</span>
                  <div style="display:inline-flex; align-items:center; gap:4px;">
                    <button type="button" class="btn-restore-note" onclick="event.stopPropagation(); restoreNoteFromTrash(${n.id})" title="Restaurar nota de la papelera">↺ Restaurar</button>
                    <button type="button" class="btn-icon-tiny btn-danger-tiny" style="opacity:1;" onclick="event.stopPropagation(); permanentlyDeleteNoteById(${n.id})" title="Eliminar definitivamente">✕</button>
                  </div>
                </div>
                <div class="note-item-snippet">${cleanSnippet || 'Nota sin texto'}</div>
                <div class="note-item-meta">
                  <div style="display:flex; align-items:center; gap:5px; overflow:hidden; flex-wrap:wrap;">
                    ${folderBadgesHtml}
                  </div>
                  <span class="tabular-nums">${dateStr}</span>
                </div>
              </div>
            </div>
          </div>
        `;
      }

      return `
        <div class="note-item-card ${isSel ? 'selected' : ''}" 
             id="note-card-${n.id}" 
             data-note-id="${n.id}"
             draggable="true"
             style="${customCardStyle}"
             onclick="handleGalleryNoteCardClick(event, ${n.id})" 
             onauxclick="if(event.button===1){event.preventDefault(); openNoteInBackgroundTab(${n.id});}"
             title="Clic para abrir en pestaña · Clic central o Ctrl+Clic para abrir en pestaña en segundo plano · Arrastra hacia una carpeta para asignarla">
          <div class="note-card-inner">
            <div class="note-card-left-controls">
              <div class="note-drag-handle" 
                   data-note-id="${n.id}" 
                   title="Arrastrar a una carpeta, barra de pestañas o reordenar nota"
                   onclick="event.stopPropagation()">
                <svg class="vertical-grip-icon" viewBox="0 0 10 16" width="10" height="15" fill="currentColor">
                  <circle cx="2.5" cy="2.5" r="1.4"/>
                  <circle cx="7.5" cy="2.5" r="1.4"/>
                  <circle cx="2.5" cy="8" r="1.4"/>
                  <circle cx="7.5" cy="8" r="1.4"/>
                  <circle cx="2.5" cy="13.5" r="1.4"/>
                  <circle cx="7.5" cy="13.5" r="1.4"/>
                </svg>
              </div>
              <button class="btn-icon-tiny btn-danger-tiny" draggable="false" onclick="event.stopPropagation(); deleteNoteById(${n.id})" title="Enviar a la papelera" aria-label="Enviar a la papelera">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>
            <div class="note-card-main-content">
              <div class="note-item-title" style="justify-content:space-between;">
                <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; flex:1;">${emoji} ${n.title || 'Sin título'}</span>
                <span style="display:inline-flex; align-items:center; gap:4px;">
                  ${isOpenInTab && !isSel ? '<span title="Abierta en pestaña superior" style="width:6px; height:6px; border-radius:50%; background:var(--accent-amber); display:inline-block;"></span>' : ''}
                  ${n.isShared ? '<span title="Nota compartida" style="font-size:10.5px;">👥</span>' : ''}
                  ${n.isLocked ? '<span title="Nota protegida / bloqueada" style="font-size:10.5px;">🔒</span>' : ''}
                  ${n.isPinned ? '📌' : ''}
                </span>
              </div>
              <div class="note-item-snippet">${cleanSnippet || 'Nota sin texto'}</div>
              <div class="note-item-meta">
                <div style="display:flex; align-items:center; gap:5px; overflow:hidden; flex-wrap:wrap;">
                  ${folderBadgesHtml}
                  ${tagsBadgesHtml}
                </div>
                <span class="tabular-nums">${dateStr}</span>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    async function triggerSmartFolderDatabaseQuery(folderName, smartCfg, searchQuery) {
      if (!folderName || !isSmartFolder(folderName)) return;
      const seq = ++smartFolderQuerySeq;
      state._activeSmartQuerySeq = seq;

      const rules = smartCfg && Array.isArray(smartCfg.rules) ? smartCfg.rules : [];
      const matchMode = smartCfg?.matchMode || 'all';

      try {
        let result = null;
        if (hasPyWebViewBridge() && typeof window.pywebview.api.query_smart_folder === 'function') {
          result = await window.pywebview.api.query_smart_folder(folderName, rules, matchMode);
        } else {
          const res = await fetch('/api/smart-folders/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ folder: folderName, rules: rules, matchMode: matchMode })
          });
          if (res.ok) {
            result = await res.json();
          }
        }

        if (state._activeSmartQuerySeq !== seq || state.selectedFolder !== folderName) {
          return;
        }

        if (result && result.ok && Array.isArray(result.notes)) {
          let stateChanged = false;
          result.notes.forEach(dbNote => {
            const idx = state.notes.findIndex(n => n.id === dbNote.id);
            if (idx >= 0) {
              if (JSON.stringify(state.notes[idx]) !== JSON.stringify(dbNote)) {
                state.notes[idx] = dbNote;
                stateChanged = true;
              }
            } else {
              state.notes.push(dbNote);
              stateChanged = true;
            }
          });

          const q = (typeof searchQuery === 'string' ? searchQuery : (document.getElementById('notes-search-input')?.value || '')).toLowerCase().trim();
          let dbFiltered = result.notes.filter(n => {
            if (q) {
              const text = `${n.title || ''} ${n.content || ''} ${getNoteFolders(n).join(' ')} ${n.tags || ''}`.toLowerCase();
              return text.includes(q);
            }
            return true;
          });

          const galleryTitleEl = document.getElementById('gallery-title');
          if (galleryTitleEl && state.selectedFolder === folderName) {
            galleryTitleEl.innerHTML = `<span style="margin-right:4px;">${getFolderEmoji(folderName)}</span> <span>${escapeHtmlAttr(folderName)}</span> <span class="smart-folder-badge-pill" title="Consulta dinámica verificada con SQLite">⚙️ Dinámica</span> <span style="font-size:11px; opacity:0.6; font-weight:normal; margin-left:4px;">(${dbFiltered.length})</span>`;
          }

          renderDynamicSmartFolderNotes(folderName, dbFiltered, smartCfg);
        }
      } catch (err) {
        console.warn('Consulta dinámica de carpeta inteligente en backend:', err);
      }
    }

    function renderDynamicSmartFolderNotes(folderName, notesList, smartCfg) {
      if (state.selectedFolder !== folderName) return;
      const container = document.getElementById('notes-list-container');
      if (!container) return;

      const safeSmartJs = String(folderName).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
      const modeText = smartCfg && smartCfg.matchMode === 'any' ? 'Cualquier filtro (OR)' : 'Todos los filtros (AND)';
      const rulesPillsHtml = ((smartCfg && smartCfg.rules) || []).map(r => `<span class="smart-banner-rule-chip">${escapeHtmlAttr(formatSmartRuleSummary(r))}</span>`).join('');
      const smartHeaderBanner = `
        <div class="smart-folder-gallery-banner">
          <div class="smart-folder-banner-top">
            <div class="smart-folder-banner-title">
              <span>⚙️ Consulta dinámica (${modeText})</span>
              <span class="smart-folder-limit-tag" title="No admite subcarpetas · No colaborativa">Raíz · Personal</span>
            </div>
            <button type="button" class="btn-edit-smart-rules" onclick="openSmartFolderModal('edit', '${safeSmartJs}')" title="Editar reglas de esta Carpeta Inteligente">Editar filtros</button>
          </div>
          <div class="smart-folder-banner-chips">
            ${rulesPillsHtml || '<span class="smart-banner-rule-chip">Sin reglas activas</span>'}
          </div>
        </div>
      `;

      if (!notesList.length) {
        const hasRules = Boolean(smartCfg && Array.isArray(smartCfg.rules) && smartCfg.rules.length > 0);
        container.innerHTML = smartHeaderBanner + `
          <div class="smart-folder-empty-state" style="text-align:center; padding:32px 16px; color:var(--text-muted); font-size:13px;">
            <div style="font-size:32px; margin-bottom:8px;">⚙️</div>
            <div style="font-weight:600; font-size:14px; margin-bottom:6px; color:var(--text-main);">
              ${hasRules ? 'Ninguna nota coincide con esta consulta dinámica' : 'Esta carpeta inteligente no tiene filtros definidos'}
            </div>
            <div style="font-size:12px; line-height:1.5; max-width:320px; margin:0 auto 16px auto; opacity:0.85;">
              ${hasRules
                ? `Se consultó la base de datos pero ninguna de tus notas cumple las condiciones configuradas para <strong>${escapeHtmlAttr(folderName)}</strong>.`
                : 'Configura una o más reglas (etiquetas, fechas, listas, archivos adjuntos) para consultar tus notas en tiempo real.'}
            </div>
            <button type="button" class="btn-edit-smart-rules" onclick="openSmartFolderModal('edit', '${safeSmartJs}')" style="display:inline-flex; align-items:center; gap:6px; margin:0 auto; padding:6px 14px; font-size:12px;">
              ⚙️ Configurar filtros
            </button>
          </div>
        `;
        return;
      }

      container.innerHTML = smartHeaderBanner + notesList.map(n => buildNoteCardHtml(n, false)).join('');
      attachNotesListReorderListeners();
      renderSidebarQuickNotes();
    }

    function renderNotesList() {
      const activeNote = getActiveNote();
      const currentFolder = state.selectedFolder || (activeNote ? getNotePrimaryDisplayFolder(activeNote) : MASTER_ALL_NOTES_FOLDER) || MASTER_ALL_NOTES_FOLDER;
      state.selectedFolder = currentFolder;
      const viewingTrash = isTrashFolder(currentFolder);
      const viewingSmart = !viewingTrash && isSmartFolder(currentFolder);

      const q = (document.getElementById('notes-search-input')?.value || '').toLowerCase().trim();
      let filtered = [];

      if (viewingTrash) {
        filtered = state.notes.filter(n => {
          if (!n.isTrashed) return false;
          if (q) {
            const text = `${n.title || ''} ${n.content || ''} ${getNoteFolders(n).join(' ')} ${n.tags || ''}`.toLowerCase();
            if (!text.includes(q)) return false;
          }
          return true;
        });
      } else if (viewingSmart) {
        // ⚙️ Carpeta Inteligente: Consulta dinámica en la base de datos SQLite según las condiciones definidas
        // En lugar de mostrar todas las notas por defecto.
        const smartCfg = getSmartFolderConfig(currentFolder);
        const hasRules = Boolean(smartCfg && Array.isArray(smartCfg.rules) && smartCfg.rules.length > 0);

        if (!hasRules) {
          // Si no tiene filtros definidos, la consulta dinámica devuelve 0 notas (NUNCA todas las notas por defecto)
          filtered = [];
        } else {
          // Evaluación dinámica inmediata en tiempo real sobre las notas actuales
          filtered = state.notes.filter(n => {
            if (!noteMatchesSmartFolder(n, currentFolder)) return false;
            if (q) {
              const text = `${n.title || ''} ${n.content || ''} ${getNoteFolders(n).join(' ')} ${n.tags || ''}`.toLowerCase();
              if (!text.includes(q)) return false;
            }
            return true;
          });
        }

        // Ejecutar consulta dinámica asíncrona directamente contra SQLite en el backend
        triggerSmartFolderDatabaseQuery(currentFolder, smartCfg, q);
      } else {
        // Carpeta física estándar o "Todas Las Notas"
        filtered = state.notes.filter(n => {
          if (!noteBelongsToFolder(n, currentFolder)) return false;
          if (q) {
            const text = `${n.title || ''} ${n.content || ''} ${getNoteFolders(n).join(' ')} ${n.tags || ''}`.toLowerCase();
            if (!text.includes(q)) return false;
          }
          return true;
        });
      }

      const galleryTitleEl = document.getElementById('gallery-title');
      if (galleryTitleEl) {
        if (viewingTrash) {
          galleryTitleEl.innerHTML = `<span style="margin-right:4px;">🗑️</span> <span>Papelera</span> <span style="font-size:11px; opacity:0.6; font-weight:normal; margin-left:4px;">(${filtered.length})</span>`;
        } else if (viewingSmart) {
          galleryTitleEl.innerHTML = `<span style="margin-right:4px;">${getFolderEmoji(currentFolder)}</span> <span>${escapeHtmlAttr(currentFolder)}</span> <span class="smart-folder-badge-pill" title="Consulta dinámica activa">⚙️ Dinámica</span> <span style="font-size:11px; opacity:0.6; font-weight:normal; margin-left:4px;">(${filtered.length})</span>`;
        } else {
          galleryTitleEl.innerHTML = `<span style="margin-right:4px;">${getFolderEmoji(currentFolder)}</span> <span>${escapeHtmlAttr(currentFolder)}</span> <span style="font-size:11px; opacity:0.6; font-weight:normal; margin-left:4px;">(${filtered.length})</span>`;
        }
      }

      const safeSmartJs = String(currentFolder).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
      let smartHeaderBanner = '';
      if (viewingSmart) {
        const smartCfg = getSmartFolderConfig(currentFolder) || { matchMode: 'all', rules: [] };
        const modeText = smartCfg.matchMode === 'any' ? 'Cualquier filtro (OR)' : 'Todos los filtros (AND)';
        const rulesPillsHtml = (smartCfg.rules || []).map(r => `<span class="smart-banner-rule-chip">${escapeHtmlAttr(formatSmartRuleSummary(r))}</span>`).join('');
        smartHeaderBanner = `
          <div class="smart-folder-gallery-banner">
            <div class="smart-folder-banner-top">
              <div class="smart-folder-banner-title">
                <span>⚙️ Consulta dinámica (${modeText})</span>
                <span class="smart-folder-limit-tag" title="No admite subcarpetas · No colaborativa">Raíz · Personal</span>
              </div>
              <button type="button" class="btn-edit-smart-rules" onclick="openSmartFolderModal('edit', '${safeSmartJs}')" title="Editar reglas de esta Carpeta Inteligente">Editar filtros</button>
            </div>
            <div class="smart-folder-banner-chips">
              ${rulesPillsHtml || '<span class="smart-banner-rule-chip">Sin reglas activas</span>'}
            </div>
          </div>
        `;
      }

      const container = document.getElementById('notes-list-container');
      if (!filtered.length) {
        if (viewingTrash) {
          container.innerHTML = `<div style="text-align:center; padding:32px 12px; color:var(--text-muted); font-size:12.5px;">La papelera está vacía</div>`;
        } else if (viewingSmart) {
          const smartCfg = getSmartFolderConfig(currentFolder) || { matchMode: 'all', rules: [] };
          const hasRules = Boolean(smartCfg.rules && smartCfg.rules.length > 0);
          container.innerHTML = smartHeaderBanner + `
            <div class="smart-folder-empty-state" style="text-align:center; padding:32px 16px; color:var(--text-muted); font-size:13px;">
              <div style="font-size:32px; margin-bottom:8px;">⚙️</div>
              <div style="font-weight:600; font-size:14px; margin-bottom:6px; color:var(--text-main);">
                ${hasRules ? 'Ninguna nota coincide con esta consulta dinámica' : 'Esta carpeta inteligente no tiene filtros definidos'}
              </div>
              <div style="font-size:12px; line-height:1.5; max-width:320px; margin:0 auto 16px auto; opacity:0.85;">
                ${hasRules
                  ? `Se consultó la base de datos pero ninguna de tus notas cumple las condiciones configuradas para <strong>${escapeHtmlAttr(currentFolder)}</strong>.`
                  : 'Configura una o más reglas (etiquetas, fechas, listas, archivos adjuntos) para consultar tus notas en tiempo real.'}
              </div>
              <button type="button" class="btn-edit-smart-rules" onclick="openSmartFolderModal('edit', '${safeSmartJs}')" style="display:inline-flex; align-items:center; gap:6px; margin:0 auto; padding:6px 14px; font-size:12px;">
                ⚙️ Configurar filtros
              </button>
            </div>
          `;
        } else {
          container.innerHTML = `<div style="text-align:center; padding:32px 12px; color:var(--text-muted); font-size:12.5px;">Sin notas en "${escapeHtmlAttr(currentFolder)}"</div>`;
        }
        return;
      }

      const trashHeaderBanner = viewingTrash ? `
        <div class="trash-gallery-banner">
          <span>Notas en la papelera (${filtered.length})</span>
          <button type="button" class="btn-empty-trash" onclick="emptyTrash()" title="Eliminar definitivamente todas las notas de la papelera">Vaciar papelera</button>
        </div>
      ` : smartHeaderBanner;

      container.innerHTML = trashHeaderBanner + filtered.map(n => buildNoteCardHtml(n, viewingTrash)).join('');

      if (!viewingTrash) {
        attachNotesListReorderListeners();
      }
      renderSidebarQuickNotes();
    }

    function pulseSidebarTrashButton() {
      requestAnimationFrame(() => {
        const trashBtn = document.getElementById('fitem-sidebar-trash');
        const trashBadge = document.getElementById('trash-count-badge');
        if (trashBtn) {
          trashBtn.classList.remove('trash-receive-pulse');
          void trashBtn.offsetWidth;
          trashBtn.classList.add('trash-receive-pulse');
          setTimeout(() => trashBtn.classList.remove('trash-receive-pulse'), 620);
        }
        if (trashBadge) {
          trashBadge.classList.remove('trash-badge-pop');
          void trashBadge.offsetWidth;
          trashBadge.classList.add('trash-badge-pop');
          setTimeout(() => trashBadge.classList.remove('trash-badge-pop'), 520);
        }
      });
    }

    function spawnNoteToTrashFlightAnimation(sourceEl, note) {
      if (!sourceEl || !note) return;
      const trashBtn = document.getElementById('fitem-sidebar-trash');
      const foldersPanel = document.getElementById('panel-folders');
      const isTrashVisible = Boolean(
        trashBtn &&
        (!foldersPanel || !foldersPanel.classList.contains('collapsed') || foldersPanel.classList.contains('focus-peek-open'))
      );
      if (!isTrashVisible) return;

      const srcRect = sourceEl.getBoundingClientRect();
      const dstRect = trashBtn.getBoundingClientRect();
      if (!srcRect.width || !dstRect.width) return;

      const flyer = document.createElement('div');
      flyer.className = 'note-to-trash-flyer';
      const emoji = note.emoji || '📝';
      const titleText = escapeHtmlAttr((note.title || 'Sin título').slice(0, 28));
      flyer.innerHTML = `
        <span class="note-to-trash-flyer-emoji">${emoji}</span>
        <span class="note-to-trash-flyer-title">${titleText}</span>
        <span class="note-to-trash-flyer-badge">🗑️</span>
      `;

      const startX = srcRect.left + Math.min(24, srcRect.width * 0.15);
      const startY = srcRect.top + srcRect.height * 0.5 - 16;
      const endX = dstRect.left + 18;
      const endY = dstRect.top + dstRect.height * 0.5 - 14;
      const deltaX = endX - startX;
      const deltaY = endY - startY;

      flyer.style.left = `${startX}px`;
      flyer.style.top = `${startY}px`;
      document.body.appendChild(flyer);

      requestAnimationFrame(() => {
        flyer.style.transform = `translate3d(${deltaX}px, ${deltaY}px, 0) scale(0.38) rotate(-6deg)`;
        flyer.style.opacity = '0.12';
      });

      setTimeout(() => {
        flyer.remove();
      }, 310);
    }

    function deleteNoteById(id) {
      const deletedId = Number(id);
      const note = state.notes.find(n => Number(n.id) === deletedId);
      if (!note) return;

      // Si ya estaba en la papelera, eliminar definitivamente
      if (note.isTrashed) {
        permanentlyDeleteNoteById(deletedId);
        return;
      }

      // Enviar la nota a la Papelera en el estado de inmediato
      note.isTrashed = true;
      note.trashedAt = Date.now();
      note.isPinned = false;

      const closedTabIdx = Array.isArray(state.openTabIds) ? state.openTabIds.indexOf(deletedId) : -1;
      if (Array.isArray(state.openTabIds)) {
        state.openTabIds = state.openTabIds.filter(tid => Number(tid) !== deletedId);
      }

      save(false, note);

      const finalizeTrashTransition = () => {
        const remainingActiveNotes = getActiveNotesList();
        if (!remainingActiveNotes.length) {
          state.openTabIds = [];
          state.activeNoteId = null;
          saveOpenTabsState();
          renderFolders();
          renderNotesList();
          renderNoteTabs();
          navigateToHome();
          pulseSidebarTrashButton();
          return;
        }

        if (Number(state.activeNoteId) === deletedId) {
          if (state.openTabIds.length > 0) {
            const nextIdx = Math.min(Math.max(0, closedTabIdx), state.openTabIds.length - 1);
            state.activeNoteId = state.openTabIds[nextIdx];
            saveOpenTabsState();
            renderFolders();
            renderNotesList();
            renderNoteTabs();
            loadActiveNote();
          } else {
            state.activeNoteId = null;
            saveOpenTabsState();
            renderFolders();
            renderNotesList();
            renderNoteTabs();
            navigateToHome();
          }
        } else {
          saveOpenTabsState();
          renderFolders();
          renderNotesList();
          renderNoteTabs();
          if (state.isHomeActive) {
            renderHomePage();
          }
        }
        pulseSidebarTrashButton();
      };

      const galleryCardEl = document.getElementById(`note-card-${deletedId}`);
      const homeCardEl = document.querySelector(`[data-home-note-id="${deletedId}"]`);
      const visibleSourceEl = (state.isHomeActive && homeCardEl) ? homeCardEl : (galleryCardEl || homeCardEl);

      showToast(`Nota "${note.title || 'Sin título'}" enviada a la papelera`, '🗑️');

      if (visibleSourceEl && ! visibleSourceEl.classList.contains('note-trashing-exit')) {
        spawnNoteToTrashFlightAnimation(visibleSourceEl, note);
        if (galleryCardEl) {
          const rect = galleryCardEl.getBoundingClientRect();
          galleryCardEl.style.maxHeight = `${rect.height}px`;
          void galleryCardEl.offsetWidth;
          galleryCardEl.classList.add('note-trashing-exit');
        }
        if (homeCardEl) {
          const rect = homeCardEl.getBoundingClientRect();
          homeCardEl.style.maxHeight = `${rect.height}px`;
          void homeCardEl.offsetWidth;
          homeCardEl.classList.add('note-trashing-exit');
        }
        setTimeout(finalizeTrashTransition, 265);
      } else {
        finalizeTrashTransition();
      }
    }

    function restoreNoteFromTrash(id) {
      const numericId = Number(id);
      const note = state.notes.find(n => Number(n.id) === numericId);
      if (!note) return;

      note.isTrashed = false;
      delete note.trashedAt;
      note.updatedAt = Date.now();
      setNoteFolders(note, getNoteFolders(note));

      save(false, note);
      showToast(`Nota "${note.title || 'Sin título'}" restaurada de la papelera`, '↺');

      const trashedCardEl = document.getElementById(`note-card-${numericId}`);
      const finalizeRestore = () => {
        renderFolders();
        renderNotesList();
        renderNoteTabs();
        if (state.isHomeActive) {
          renderHomePage();
        }
      };

      if (trashedCardEl && !trashedCardEl.classList.contains('note-restoring-exit')) {
        const rect = trashedCardEl.getBoundingClientRect();
        trashedCardEl.style.maxHeight = `${rect.height}px`;
        void trashedCardEl.offsetWidth;
        trashedCardEl.classList.add('note-restoring-exit');
        setTimeout(finalizeRestore, 240);
      } else {
        finalizeRestore();
      }
    }

    function permanentlyDeleteNoteById(id) {
      const deletedId = Number(id);
      const note = state.notes.find(n => Number(n.id) === deletedId);
      const noteTitle = note ? (note.title || 'Sin título') : 'Nota';
      if (window.NoteJSCloud) window.NoteJSCloud.deleted(note);

      state.notes = state.notes.filter(n => Number(n.id) !== deletedId);
      if (Array.isArray(state.openTabIds)) {
        state.openTabIds = state.openTabIds.filter(tid => Number(tid) !== deletedId);
      }

      if (hasPyWebViewBridge() && typeof window.pywebview.api.delete_note === "function") {
        window.pywebview.api.delete_note(deletedId).catch(() => {});
      } else {
        fetch("/api/notes/" + encodeURIComponent(deletedId), { method: "DELETE" }).catch(() => {});
      }

      persistNoteMetaOverlay();
      localStorage.setItem("notejs_desktop_notion_v9", JSON.stringify(state.notes));
      saveOpenTabsState();
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      if (state.isHomeActive) {
        renderHomePage();
      }
      showToast(`"${noteTitle}" eliminada definitivamente`, '🗑️');
    }

    function emptyTrash() {
      const trashed = getTrashedNotesList();
      if (!trashed.length) return;
      trashed.forEach(n => {
        if (window.NoteJSCloud) window.NoteJSCloud.deleted(n);
        if (hasPyWebViewBridge() && typeof window.pywebview.api.delete_note === "function") {
          window.pywebview.api.delete_note(n.id).catch(() => {});
        } else {
          fetch("/api/notes/" + encodeURIComponent(n.id), { method: "DELETE" }).catch(() => {});
        }
      });
      state.notes = state.notes.filter(n => !n.isTrashed);
      persistNoteMetaOverlay();
      localStorage.setItem("notejs_desktop_notion_v9", JSON.stringify(state.notes));
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      if (state.isHomeActive) {
        renderHomePage();
      }
      showToast('Papelera vaciada por completo', '🗑️');
    }

    /* Arrastrar y Soltar Notas (a Carpetas en Barra Lateral, Editor Rico o Reordenamiento en Galería) */
    let draggedListNoteId = null;
    let activeNoteDragGhostEl = null;

    function attachCustomNoteDragGhost(e, noteId) {
      if (!e || !e.dataTransfer || typeof e.dataTransfer.setDragImage !== 'function') return;
      const note = state.notes.find(n => n.id === Number(noteId));
      if (!note) return;

      if (activeNoteDragGhostEl) {
        activeNoteDragGhostEl.remove();
        activeNoteDragGhostEl = null;
      }

      const ghost = document.createElement('div');
      ghost.className = 'note-drag-ghost';
      const emoji = note.emoji || '📝';
      const titleText = (note.title || 'Sin título').slice(0, 26);
      const folderText = note.folder || 'General';
      ghost.innerHTML = `
        <span>${emoji}</span>
        <span style="overflow:hidden; text-overflow:ellipsis;">${titleText}</span>
        <span class="note-drag-ghost-folder">${getFolderEmoji(folderText)} ${folderText}</span>
      `;
      document.body.appendChild(ghost);
      activeNoteDragGhostEl = ghost;
      e.dataTransfer.setDragImage(ghost, 18, 18);
    }

    function attachNotesListReorderListeners() {
      const container = document.getElementById('notes-list-container');
      if (!container) return;

      const cards = container.querySelectorAll('.note-item-card');
      cards.forEach(card => {
        const noteId = Number(card.dataset.noteId);
        const handle = card.querySelector('.note-drag-handle');

        card.setAttribute('draggable', 'true');

        const onDragStart = function(e) {
          if (e.target && e.target.closest('.btn-danger-tiny')) {
            e.preventDefault();
            return;
          }
          draggedListNoteId = noteId;
          draggedNoteCardId = noteId; // Disponible para soltar en carpetas del panel izquierdo o en el editor
          if (e.dataTransfer) {
            e.dataTransfer.effectAllowed = 'copyMove';
            e.dataTransfer.setData('application/notejs-note-id', String(noteId));
            e.dataTransfer.setData('text/plain', 'note:' + noteId);
          }

          attachCustomNoteDragGhost(e, noteId);
          document.body.classList.add('is-dragging-note');

          setTimeout(() => {
            card.classList.add('is-reordering');
          }, 10);
        };

        const onDragEnd = function() {
          cleanupNoteListDragStates();
        };

        card.ondragstart = onDragStart;
        card.ondragend = onDragEnd;

        // Soporte adicional de arrastre táctil / long-press en dispositivos sin HTML5 DnD nativo
        if (handle) {
          setupLongPressReorder(handle, card, noteId);
        }

        // Eventos de destino sobre cada tarjeta de nota para reordenamiento en la galería central
        card.ondragover = function(e) {
          if (!draggedListNoteId || draggedListNoteId === noteId) return;
          e.preventDefault();
          if (e.dataTransfer) e.dataTransfer.dropEffect = 'move';

          const rect = card.getBoundingClientRect();
          const mid = rect.top + (rect.height / 2);
          card.classList.remove('drag-reorder-above', 'drag-reorder-below');
          if (e.clientY < mid) {
            card.classList.add('drag-reorder-above');
          } else {
            card.classList.add('drag-reorder-below');
          }
        };

        card.ondragleave = function(e) {
          if (e.relatedTarget && card.contains(e.relatedTarget)) return;
          card.classList.remove('drag-reorder-above', 'drag-reorder-below');
        };

        card.ondrop = function(e) {
          if (!draggedListNoteId || draggedListNoteId === noteId) return;
          e.preventDefault();
          const isAbove = card.classList.contains('drag-reorder-above');
          card.classList.remove('drag-reorder-above', 'drag-reorder-below');

          reorderNotesInState(draggedListNoteId, noteId, isAbove);
          cleanupNoteListDragStates();
        };
      });
    }

    function setupLongPressReorder(handle, card, noteId) {
      let pressTimer = null;
      let startX = 0;
      let startY = 0;
      let isLongPressActive = false;

      const onPointerMove = (e) => {
        const curX = e.clientX || (e.touches && e.touches[0]?.clientX) || 0;
        const curY = e.clientY || (e.touches && e.touches[0]?.clientY) || 0;

        if (!isLongPressActive) {
          if (Math.abs(curX - startX) > 8 || Math.abs(curY - startY) > 8) {
            clearTimeout(pressTimer);
            detachWindowPointerListeners();
          }
          return;
        }

        if (e.cancelable) e.preventDefault();
        const elemBelow = document.elementFromPoint(curX, curY);
        const targetCard = elemBelow?.closest('.note-item-card');
        const targetFolder = elemBelow?.closest('.folder-item[data-folder], #fitem-pinned, .folder-item[data-tag]');

        document.querySelectorAll('.drag-reorder-above, .drag-reorder-below').forEach(el => {
          if (el !== targetCard) el.classList.remove('drag-reorder-above', 'drag-reorder-below');
        });
        document.querySelectorAll('.folder-drag-over').forEach(el => {
          if (el !== targetFolder) el.classList.remove('folder-drag-over');
        });

        if (targetFolder) {
          targetFolder.classList.add('folder-drag-over');
        } else if (targetCard && targetCard !== card) {
          const rect = targetCard.getBoundingClientRect();
          const mid = rect.top + (rect.height / 2);
          targetCard.classList.remove('drag-reorder-above', 'drag-reorder-below');
          if (curY < mid) {
            targetCard.classList.add('drag-reorder-above');
          } else {
            targetCard.classList.add('drag-reorder-below');
          }
        }
      };

      const onPointerUp = (e) => {
        clearTimeout(pressTimer);
        detachWindowPointerListeners();
        if (isLongPressActive) {
          const curX = e.clientX || (e.changedTouches && e.changedTouches[0]?.clientX) || 0;
          const curY = e.clientY || (e.changedTouches && e.changedTouches[0]?.clientY) || 0;
          const elemBelow = document.elementFromPoint(curX, curY);
          const targetFolder = elemBelow?.closest('.folder-item[data-folder]');
          const targetPinned = elemBelow?.closest('#fitem-pinned');
          const targetTag = elemBelow?.closest('.folder-item[data-tag]');
          const targetCard = elemBelow?.closest('.note-item-card');

          if (targetFolder) {
            const folderName = targetFolder.dataset.folder;
            moveNoteToFolder(noteId, folderName);
          } else if (targetPinned) {
            const note = state.notes.find(n => n.id === noteId);
            if (note) {
              note.isPinned = true;
              note.updatedAt = Date.now();
              save(false, note);
              renderFolders();
              renderNotesList();
              if (state.activeNoteId === noteId) loadActiveNote();
              showToast(`Nota "${note.title || 'Sin título'}" añadida a Notas fijadas`, '📌');
            }
          } else if (targetTag) {
            assignTagToNoteByDrop(noteId, targetTag.dataset.tag);
          } else if (targetCard && targetCard !== card) {
            const targetId = Number(targetCard.dataset.noteId);
            const isAbove = targetCard.classList.contains('drag-reorder-above');
            reorderNotesInState(noteId, targetId, isAbove);
          }
        }
        isLongPressActive = false;
        cleanupNoteListDragStates();
      };

      const detachWindowPointerListeners = () => {
        window.removeEventListener('pointermove', onPointerMove);
        window.removeEventListener('pointerup', onPointerUp);
        window.removeEventListener('pointercancel', onPointerUp);
      };

      const onPointerDown = (e) => {
        // En escritorio (ratón), permitir que HTML5 Drag & Drop nativo opere sin interferencia
        if (e.pointerType === 'mouse') return;

        startX = e.clientX || (e.touches && e.touches[0]?.clientX) || 0;
        startY = e.clientY || (e.touches && e.touches[0]?.clientY) || 0;
        isLongPressActive = false;

        window.addEventListener('pointermove', onPointerMove, { passive: false });
        window.addEventListener('pointerup', onPointerUp);
        window.addEventListener('pointercancel', onPointerUp);

        pressTimer = setTimeout(() => {
          isLongPressActive = true;
          draggedListNoteId = noteId;
          draggedNoteCardId = noteId;
          document.body.classList.add('is-dragging-note');
          card.classList.add('long-press-active');
          if (navigator.vibrate) navigator.vibrate(40);
          showToast('Arrastra la nota hacia una carpeta o posición', '📁');
        }, 240);
      };

      card.addEventListener('pointerdown', onPointerDown);
    }

    function reorderNotesInState(sourceId, targetId, placeAbove) {
      const fromIdx = state.notes.findIndex(n => n.id === sourceId);
      const toIdx = state.notes.findIndex(n => n.id === targetId);
      if (fromIdx === -1 || toIdx === -1) return;

      const [movedNote] = state.notes.splice(fromIdx, 1);
      const currentToIdx = state.notes.findIndex(n => n.id === targetId);
      const targetPos = placeAbove ? currentToIdx : currentToIdx + 1;
      state.notes.splice(targetPos, 0, movedNote);

      save();
      renderNotesList();
      showToast(`Nota "${movedNote.title}" reordenada`, '↕️');
    }

    function cleanupNoteListDragStates() {
      draggedListNoteId = null;
      draggedNoteCardId = null;
      document.body.classList.remove('is-dragging-note');
      if (activeNoteDragGhostEl) {
        activeNoteDragGhostEl.remove();
        activeNoteDragGhostEl = null;
      }
      document.querySelectorAll('.is-reordering, .drag-reorder-above, .drag-reorder-below, .long-press-active, .zone-highlight, .drag-over-active, .folder-drag-over').forEach(el => {
        el.classList.remove('is-reordering', 'drag-reorder-above', 'drag-reorder-below', 'long-press-active', 'zone-highlight', 'drag-over-active', 'folder-drag-over');
      });
    }

    function getActiveNote() {
      if (!state.activeNoteId) return null;
      return state.notes.find(n => Number(n.id) === Number(state.activeNoteId)) || null;
    }

    function loadNote(pageId) {
      if (!pageId && pageId !== 0) {
        showToast('ID de nota inválido', '⚠️');
        return false;
      }
      const note = state.notes.find(n => String(n.id) === String(pageId) || Number(n.id) === Number(pageId));
      if (!note) {
        showToast('Nota no encontrada', '⚠️');
        return false;
      }
      if (note.isTrashed) {
        showToast('Restaura la nota desde la papelera para abrirla y editarla', '🗑️');
        return false;
      }
      selectNote(note.id);
      return true;
    }
    window.loadNote = loadNote;

    function selectNote(id) {
      const numericId = Number(id);
      const note = state.notes.find(n => n.id === numericId);
      if (!note) return;
      if (note.isTrashed) {
        showToast('Restaura la nota desde la papelera para abrirla y editarla', '🗑️');
        return;
      }
      // Register the destination before rendering tabs while leaving Home.
      // An empty tab list would otherwise switch Home back on during the transition.
      state.activeNoteId = numericId;
      if (state.isRemindersActive) {
        exitRemindersView();
      }
      if (state.isHomeActive) {
        exitHomeView();
      }
      try {
        localStorage.setItem('notejs_last_visited_note', String(numericId));
      } catch (_) {}
      saveSettingsPayload({ lastVisitedNoteId: numericId });

      if (isTrashFolder(state.selectedFolder)) {
        state.selectedFolder = MASTER_ALL_NOTES_FOLDER;
      }
      if (!Array.isArray(state.openTabIds)) state.openTabIds = [];
      if (!state.openTabIds.includes(numericId)) {
        state.openTabIds.push(numericId);
        saveOpenTabsState();
      }
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      loadActiveNote();
    }

    function loadActiveNote() {
      const targetNoteId = arguments.length > 0 ? arguments[0] : null;
      if (targetNoteId !== null && targetNoteId !== undefined) {
        state.activeNoteId = targetNoteId;
      }
      if (state.isRemindersActive) {
        exitRemindersView();
      }
      if (state.isHomeActive || !state.activeNoteId) {
        navigateToHome();
        return;
      }
      const note = getActiveNote();
      if (!note || note.isTrashed) {
        navigateToHome();
        return;
      }
      exitHomeView();
      try {
        localStorage.setItem('notejs_last_visited_note', String(note.id));
      } catch (_) {}
      saveSettingsPayload({ lastVisitedNoteId: note.id });

      if (Array.isArray(state.openTabIds) && !state.openTabIds.includes(note.id)) {
        state.openTabIds.push(note.id);
        saveOpenTabsState();
      }
      renderNoteTabs();

      // Migas de Pan
      const primaryFolder = getNotePrimaryDisplayFolder(note);
      const safePrimaryFolderJs = String(primaryFolder).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
      const parentNote = note.parentId ? state.notes.find(n => n.id === note.parentId) : null;
      let breadcrumbHtml = `<span class="notion-breadcrumb-link" onclick="selectFolder('${safePrimaryFolderJs}')">${getFolderEmoji(primaryFolder)} ${escapeHtmlAttr(primaryFolder)}</span>`;
      if (parentNote) {
        breadcrumbHtml += ` <span>/</span> <span class="notion-breadcrumb-link" onclick="selectNote(${parentNote.id})">${parentNote.emoji || '📄'} ${parentNote.title}</span>`;
      }
      breadcrumbHtml += ` <span>/</span> <span style="color:var(--text-primary); font-weight:600;">${note.emoji || '📝'} ${note.title || 'Sin título'}</span>`;
      document.getElementById('notion-breadcrumbs').innerHTML = breadcrumbHtml;

      // Portada
      const coverEl = document.getElementById('notion-cover');
      if (note.hasCover) {
        coverEl.classList.add('has-cover');
        coverEl.style.backgroundImage = note.coverStyle || COVER_PRESETS[0];
        document.getElementById('cover-btn-label').textContent = 'Quitar portada';
      } else {
        coverEl.classList.remove('has-cover');
        document.getElementById('cover-btn-label').textContent = 'Elegir foto de portada';
      }

      // Icono Emoji
      document.getElementById('page-emoji-display').textContent = note.emoji || '📝';

      // Título & Metadata
      document.getElementById('note-title').value = note.title || '';
      const folderSelectEl = document.getElementById('note-folder-select');
      if (folderSelectEl) {
        folderSelectEl.value = primaryFolder;
      }
      renderNoteFoldersUI();
      renderNoteTagsUI();
      const pinBtn = document.getElementById('btn-pin-note');
      if (pinBtn) {
        pinBtn.title = note.isPinned ? 'Desfijar nota (Ctrl+Shift+P)' : 'Fijar nota (Ctrl+Shift+P)';
        pinBtn.classList.toggle('active', Boolean(note.isPinned));
        if (note.isPinned) {
          pinBtn.style.borderColor = 'var(--border-hairline)';
          pinBtn.style.color = 'var(--text-primary)';
          pinBtn.style.background = 'var(--bg-elevated)';
        } else {
          pinBtn.style.borderColor = 'var(--border-hairline)';
          pinBtn.style.color = 'var(--text-secondary)';
          pinBtn.style.background = 'var(--bg-elevated)';
        }
      }
      document.getElementById('note-updated').textContent = new Date(note.updatedAt).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });

      // Lienzo Rich Text
      const editorCanvas = document.getElementById('rich-editor-canvas');
      const noteIdToFetch = String(note.id);
      editorCanvas.innerHTML = note.content || '';
      attachSubpageBlockListeners();
      setTimeout(renderAllInlineEquations, 30);

      // Cloud notes retain mobile block payloads in HTML for lossless round trips.
      if (!note.cloud) loadAndRenderRecordMap(noteIdToFetch, editorCanvas);

      // Activar manejadores de notas, imágenes, columnas, bloques sincronizados y TOC
      attachEmbeddedNoteCardListeners();
      attachImageBlockListeners();
      if (typeof tagAllEditorBlocks === 'function') tagAllEditorBlocks();
      if (typeof applyNoteAppearanceSettings === 'function') applyNoteAppearanceSettings(note);
      if (typeof attachColumnResizerListeners === 'function') attachColumnResizerListeners();
      if (typeof attachSyncedBlockListeners === 'function') attachSyncedBlockListeners();
      if (typeof refreshPageTableOfContents === 'function') setTimeout(refreshPageTableOfContents, 40);
    }

    function loadAndRenderRecordMap(noteIdToFetch, editorCanvas) {
      const note = state.notes.find(item => String(item.id) === String(noteIdToFetch));
      if (!note) return;
      const applyRecordMap = (rmap) => {
        if (rmap && rmap.block && typeof rmap.block === 'object') {
          state.activeRecordMap = rmap;
          let rootId = noteIdToFetch;
          if (!rmap.block[rootId]) {
            const pageEntryKey = Object.keys(rmap.block).find(k => {
              const b = rmap.block[k]?.value;
              return b && (b.type === 'page' || String(b.id) === noteIdToFetch);
            });
            if (pageEntryKey) rootId = pageEntryKey;
          }
          if (rmap.block[rootId] && Array.isArray(rmap.block[rootId]?.value?.content) && rmap.block[rootId].value.content.length > 0) {
            renderTreeFromRecordMap(rmap, rootId, editorCanvas);
            return true;
          }
        }
        return false;
      };

      if (hasPyWebViewBridge() && typeof window.pywebview.api.get_record_map === 'function') {
        try {
          const rmapResult = window.pywebview.api.get_record_map(noteIdToFetch);
          if (rmapResult && typeof rmapResult.then === 'function') {
            rmapResult.then(res => {
              const rmap = (res && res.block) ? res : (res && res.recordMap ? res.recordMap : null);
              if (rmap) applyRecordMap(rmap);
            }).catch(() => {});
          } else if (rmapResult && (rmapResult.block || rmapResult.recordMap)) {
            applyRecordMap(rmapResult.block ? rmapResult : rmapResult.recordMap);
          }
        } catch (_) {}
      } else {
        fetch(`/api/notes/${encodeURIComponent(noteIdToFetch)}/recordMap`)
          .then(r => r.ok ? r.json() : null)
          .then(data => {
            if (data && data.block) {
              applyRecordMap(data);
            }
          })
          .catch(() => {});
      }

      // Callout
      const calloutEl = document.getElementById('block-callout');
      if (note.showCallout) {
        calloutEl.style.display = 'flex';
        document.getElementById('callout-emoji').textContent = note.calloutEmoji || '💡';
        document.getElementById('callout-input').value = note.callout || '';
        const calloutColors = {
          amber: { bg: 'rgba(245, 158, 11, 0.15)', border: 'rgba(245, 158, 11, 0.35)' },
          blue: { bg: 'rgba(59, 130, 246, 0.15)', border: 'rgba(59, 130, 246, 0.38)' },
          green: { bg: 'rgba(16, 185, 129, 0.15)', border: 'rgba(16, 185, 129, 0.38)' },
          purple: { bg: 'rgba(168, 85, 247, 0.15)', border: 'rgba(168, 85, 247, 0.38)' },
          rose: { bg: 'rgba(244, 63, 94, 0.15)', border: 'rgba(244, 63, 94, 0.38)' }
        };
        const cTheme = calloutColors[note.calloutColor || 'amber'] || calloutColors.amber;
        calloutEl.style.background = cTheme.bg;
        calloutEl.style.borderColor = cTheme.border;
      } else {
        calloutEl.style.display = 'none';
      }

      // Quote
      const quoteEl = document.getElementById('block-quote');
      if (note.showQuote) {
        quoteEl.style.display = 'block';
        document.getElementById('quote-input').value = note.quote || '';
      } else {
        quoteEl.style.display = 'none';
      }

      // Toggle
      const toggleEl = document.getElementById('block-toggle');
      if (note.showToggle) {
        toggleEl.style.display = 'block';
        document.getElementById('toggle-header-input').value = note.toggleHeader || 'Lista colapsable (Toggle)';
        document.getElementById('toggle-body-input').value = note.toggleBody || '';
      } else {
        toggleEl.style.display = 'none';
      }

      // Code Block
      const codeEl = document.getElementById('block-code');
      if (note.showCode) {
        codeEl.style.display = 'block';
        document.getElementById('code-input').value = note.code || '';
      } else {
        codeEl.style.display = 'none';
      }

      // Kanban
      const kanbanEl = document.getElementById('block-kanban');
      if (note.showKanban) {
        kanbanEl.style.display = 'block';
        renderKanban(note);
      } else {
        kanbanEl.style.display = 'none';
      }

      // Table & Formulas 2.0
      const tableEl = document.getElementById('block-table');
      if (note.showTable) {
        tableEl.style.display = 'block';
        renderTable(note);
      } else {
        tableEl.style.display = 'none';
      }

      // Checklist
      const checkEl = document.getElementById('block-checklists');
      if (note.showChecklist) {
        checkEl.style.display = 'block';
        renderChecklists(note);
      } else {
        checkEl.style.display = 'none';
      }

      // KaTeX
      const katexEl = document.getElementById('block-katex');
      if (note.katex) {
        katexEl.style.display = 'block';
        document.getElementById('katex-formula-input').value = note.katex;
        renderKatexFormula(note.katex);
      } else {
        katexEl.style.display = 'none';
      }

      // Restaurar orden de bloques guardado y activar Drag & Drop
      restoreBlocksOrder();
      setupBlockDragAndDrop();

      // Si el panel derecho de Historial SQLite (Ctrl+H) está abierto, actualizar versiones de la nota activa
      closeHistoryPreview();
      if (state.isHistoryPanelOpen) {
        refreshActiveNoteHistory();
      }
    }

    function updateNote(field, val) {
      const note = getActiveNote();
      if (!note) return;
      if (field === 'folder') {
        if (isMasterAllNotesFolder(val)) {
          setNoteFolders(note, [MASTER_ALL_NOTES_FOLDER]);
        } else {
          const current = getNoteUserFolders(note);
          if (!current.includes(val)) {
            setNoteFolders(note, [...current, val]);
          }
        }
        renderNoteFoldersUI();
      } else {
        note[field] = val;
      }
      note.updatedAt = Date.now();
      save();
      renderFolders();
      renderNotesList();
      renderNoteTabs();
    }

    /* Selector Múltiple de Carpetas y Subcarpetas por Nota */
    function renderNoteFoldersUI() {
      const container = document.getElementById('note-folders-chips');
      if (!container) return;

      const note = getActiveNote();
      if (!note) {
        container.innerHTML = '';
        return;
      }

      const userFolders = getNoteUserFolders(note);
      const safeMasterJs = MASTER_ALL_NOTES_FOLDER.replace(/\\/g, '\\\\').replace(/'/g, "\\'");

      let html = `
        <span class="note-folder-chip master-folder-chip" onclick="selectFolder('${safeMasterJs}')" title="Toda nota pertenece siempre a &quot;${MASTER_ALL_NOTES_FOLDER}&quot;">
          <span>${getFolderEmoji(MASTER_ALL_NOTES_FOLDER)}</span>
          <span>${MASTER_ALL_NOTES_FOLDER}</span>
        </span>
      `;

      html += userFolders.map(f => {
        const safeJs = String(f).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        const safeHtml = escapeHtmlAttr(f);
        return `
          <span class="note-folder-chip" title="Asignada a &quot;${safeHtml}&quot; · Clic para filtrar carpeta">
            <span class="note-folder-chip-label" onclick="selectFolder('${safeJs}')">${getFolderEmoji(f)} ${safeHtml}</span>
            <button type="button" class="note-folder-chip-remove" onclick="event.stopPropagation(); removeNoteFolderChip('${safeJs}');" title="Quitar de &quot;${safeHtml}&quot;">✕</button>
          </span>
        `;
      }).join('');

      container.innerHTML = html;
    }

    function removeNoteFolderChip(folderName) {
      const note = getActiveNote();
      if (!note || isMasterAllNotesFolder(folderName)) return;
      const updated = getNoteUserFolders(note).filter(f => f !== folderName);
      setNoteFolders(note, updated);
      note.updatedAt = Date.now();
      save(false, note);
      renderNoteFoldersUI();
      renderNoteFoldersPopoverContent();
      renderFolders();
      renderNotesList();
      renderNoteTabs();
    }

    function toggleNoteFoldersPopover(event) {
      if (event) {
        event.stopPropagation();
      }
      const popover = document.getElementById('note-folders-popover');
      if (!popover) return;
      const isOpen = popover.style.display === 'block';
      if (isOpen) {
        closeNoteFoldersPopover();
      } else {
        renderNoteFoldersPopoverContent();
        popover.style.display = 'block';
      }
    }

    function closeNoteFoldersPopover() {
      const popover = document.getElementById('note-folders-popover');
      if (popover) {
        popover.style.display = 'none';
      }
    }

    function renderNoteFoldersPopoverContent() {
      const popover = document.getElementById('note-folders-popover');
      if (!popover) return;
      const note = getActiveNote();
      if (!note) return;

      ensureMasterFolderFirst();
      const assignedFolders = getNoteFolders(note);

      const physicalFolders = state.folders.filter(f => !isSmartFolder(f));
      const itemsHtml = physicalFolders.map(f => {
        const isMaster = isMasterAllNotesFolder(f);
        const isChecked = isMaster || assignedFolders.includes(f);
        const depth = isMaster ? 0 : getFolderDepth(f);
        const displayName = isMaster ? f : getFolderDisplayName(f);
        const safeJs = String(f).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        const safeHtml = escapeHtmlAttr(displayName);
        const indentPx = 8 + depth * 14;

        if (isMaster) {
          return `
            <div class="note-folder-popover-item master-locked" style="padding-left:${indentPx}px;" title="Todas las notas pertenecen siempre a Todas Las Notas">
              <span class="note-folder-check checked">✓</span>
              <span>${getFolderEmoji(f)}</span>
              <span style="flex:1; font-weight:700;">${safeHtml}</span>
              <span class="note-folder-locked-tag">Siempre</span>
            </div>
          `;
        }

        return `
          <button type="button" class="note-folder-popover-item ${isChecked ? 'active' : ''}" style="padding-left:${indentPx}px;" onclick="toggleNoteFolderMembership(${note.id}, '${safeJs}')">
            <span class="note-folder-check ${isChecked ? 'checked' : ''}">${isChecked ? '✓' : ''}</span>
            ${depth > 0 ? '<span class="subfolder-tree-branch">└</span>' : ''}
            <span>${getFolderEmoji(f)}</span>
            <span style="flex:1; text-align:left; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${safeHtml}</span>
          </button>
        `;
      }).join('');

      popover.innerHTML = `
        <div class="note-folders-popover-header">
          <span>Pertenece a 1 o más carpetas</span>
        </div>
        <div class="note-folders-popover-list">
          ${itemsHtml}
        </div>
        <div class="note-folders-popover-footer">
          <button type="button" class="note-folders-new-btn" onclick="closeNoteFoldersPopover(); openFolderModal('create');">+ Nueva carpeta o subcarpeta...</button>
        </div>
      `;
    }

    document.addEventListener('click', (e) => {
      const wrap = document.getElementById('note-folders-multi-wrap');
      if (wrap && !wrap.contains(e.target)) {
        closeNoteFoldersPopover();
      }
    });

    /* Manejo de Etiquetado Interactivo (Tag Chips) */
    function renderNoteTagsUI() {
      const container = document.getElementById('note-tags-chips');
      if (!container) return;

      const note = getActiveNote();
      if (!note) {
        container.innerHTML = '';
        return;
      }

      const raw = note.tags || '';
      const tagsArr = Array.isArray(raw)
        ? raw
        : raw.split(',').map(t => t.trim().toLowerCase().replace(/^#/, '')).filter(Boolean);

      let html = tagsArr.map(tag => `
        <span class="tag-chip">
          <span>#${tag}</span>
          <button class="tag-chip-remove" onclick="removeNoteTag('${tag}')" title="Eliminar etiqueta">✕</button>
        </span>
      `).join('');

      html += `
        <input id="add-tag-input" type="text" class="tag-add-input" placeholder="+ etiqueta..." onkeydown="handleAddTagKeyDown(event)" onblur="handleAddTagBlur(this.value)" />
      `;

      container.innerHTML = html;
    }

    function removeNoteTag(tagToRemove) {
      const note = getActiveNote();
      if (!note) return;

      const raw = note.tags || '';
      let tagsArr = Array.isArray(raw)
        ? raw
        : raw.split(',').map(t => t.trim().toLowerCase().replace(/^#/, '')).filter(Boolean);

      tagsArr = tagsArr.filter(t => t !== tagToRemove.toLowerCase());
      note.tags = tagsArr.join(', ');
      note.updatedAt = Date.now();
      save();
      renderNoteTagsUI();
      renderFolders();
      renderNotesList();
    }

    function handleAddTagKeyDown(e) {
      if (e.key === 'Enter' || e.key === ',') {
        e.preventDefault();
        addTagToActiveNote(e.target.value);
      }
    }

    function handleAddTagBlur(val) {
      if (val && val.trim()) {
        addTagToActiveNote(val);
      }
    }

    function addTagToActiveNote(val) {
      const newTag = val.trim().toLowerCase().replace(/^#/, '').replace(/,/g, '');
      if (!newTag) return;

      const note = getActiveNote();
      if (!note) return;

      const raw = note.tags || '';
      let tagsArr = Array.isArray(raw)
        ? raw
        : raw.split(',').map(t => t.trim().toLowerCase().replace(/^#/, '')).filter(Boolean);

      if (!tagsArr.includes(newTag)) {
        tagsArr.push(newTag);
        note.tags = tagsArr.join(', ');
        note.updatedAt = Date.now();
        save();
        renderNoteTagsUI();
        renderFolders();
        renderNotesList();
      }
    }

    /* 2. Motor de Texto Enriquecido & Macros Markdown en Vivo */
    function formatDoc(command, val = null) {
      const editor = document.getElementById('rich-editor-canvas');
      if (editor) {
        if (document.activeElement !== editor) {
          editor.focus();
        }
      }
      document.execCommand(command, false, val);
      syncRichEditor();
    }

    function insertInlineCode() {
      const sel = window.getSelection();
      if (sel && sel.rangeCount > 0) {
        const text = sel.toString() || 'código';
        document.execCommand('insertHTML', false, `<code>${text}</code>`);
        syncRichEditor();
      }
    }

    let syncBlocksDebounceTimer = null;

    function pdfViewerUrl(source, title = 'Documento.pdf') {
      return '/pdf-viewer.html?src=' + encodeURIComponent(source) + '&name=' + encodeURIComponent(title);
    }

    function createPdfEmbedHTML(source, title = 'Documento.pdf') {
      if (!source) return '<button type="button" onclick="openMediaEmbedModal(\'pdf\')">Seleccionar PDF</button>';
      if (!/^(https?:\/\/|\/(?!\/)|data:application\/pdf[;,])/i.test(source)) {
        return '<p>El enlace del PDF no es válido. Selecciona el archivo de nuevo.</p>';
      }
      return `<iframe class="notejs-pdf-frame" title="${escapeHtml(title)}" src="${escapeHtml(pdfViewerUrl(source, title))}" loading="lazy" style="width:100%;height:560px;border:1px solid var(--border-hairline);border-radius:8px;"></iframe>`;
    }

    function collectAndSyncNoteBlocks(noteId) {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor || !noteId) return;
      const blocks = [];
      Array.from(editor.children).forEach(el => {
        const id = el.getAttribute('data-block-id');
        if (id) {
          const isSubpage = el.classList.contains('block-subpage') || el.getAttribute('data-type') === 'sub_page';
          const btype = isSubpage ? 'sub_page' : (el.getAttribute('data-type') || el.tagName.toLowerCase());
          const blockObj = {
            id: id,
            noteId: noteId,
            parentId: el.getAttribute('data-parent-id') || null,
            sortIndex: el.getAttribute('data-sort-index') || 'a0',
            type: btype,
            properties: { text: el.innerText || '', html: el.innerHTML || '' }
          };
          if (isSubpage) {
            const pageId = el.getAttribute('data-page-id');
            const title = el.getAttribute('data-title') || el.querySelector('.subpage-title')?.innerText || '';
            blockObj.page_id = pageId;
            blockObj.title = title;
            blockObj.properties.page_id = pageId;
            blockObj.properties.title = title;
          }
          if (btype === 'pdf') {
            blockObj.properties.source = [[el.getAttribute('data-source') || '', []]];
            blockObj.properties.title = [[el.getAttribute('data-title') || 'Documento.pdf', []]];
          }
          blocks.push(blockObj);
        }
      });
      if (blocks.length > 0 && typeof apiSyncNoteBlocks === 'function') {
        apiSyncNoteBlocks(noteId, blocks);
      }
    }

    function syncRichEditor() {
      const note = getActiveNote();
      if (!note) return;
      const editor = document.getElementById('rich-editor-canvas');
      if (typeof tagAllEditorBlocks === 'function') tagAllEditorBlocks();
      const rawHtml = editor.innerHTML || '';
      note.content = rawHtml.replace(/<mark class="in-note-search-match[^"]*">([\s\S]*?)<\/mark>/gi, '$1');
      note.updatedAt = Date.now();
      save();
      renderNotesList();
      if (typeof refreshPageTableOfContents === 'function') {
        refreshPageTableOfContents();
      }
      clearTimeout(syncBlocksDebounceTimer);
      syncBlocksDebounceTimer = setTimeout(() => {
        collectAndSyncNoteBlocks(note.id);
      }, 500);
    }

    function handleRichEditorKeydown(e) {
      // Shortcuts
      if (e.ctrlKey || e.metaKey) {
        // Ctrl + Shift + E: Inserción de Ecuación Matemática en Línea KaTeX
        if (e.shiftKey && (e.key === 'e' || e.key === 'E')) {
          e.preventDefault();
          openInlineMathPopover();
          return;
        }
        if (e.key === 'b' || e.key === 'B') {
          e.preventDefault();
          formatDoc('bold');
          return;
        }
        if (e.key === 'i' || e.key === 'I') {
          e.preventDefault();
          formatDoc('italic');
          return;
        }
        if (e.key === 'u' || e.key === 'U') {
          e.preventDefault();
          formatDoc('underline');
          return;
        }
        if (e.key === 'e' || e.key === 'E') {
          e.preventDefault();
          insertInlineCode();
          return;
        }
        if (e.key === 'k' || e.key === 'K') {
          e.preventDefault();
          const url = prompt('Enlace URL:');
          if (url) formatDoc('createLink', url);
          return;
        }
        if (e.key === 'd' || e.key === 'D') {
          e.preventDefault();
          duplicateSelection();
          return;
        }
      }

      // Atajo Alt + Flecha Arriba / Abajo para mover la línea o párrafo actual
      if (e.altKey && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) {
        e.preventDefault();
        moveSelectedLine(e.key === 'ArrowUp' ? -1 : 1);
        return;
      }

      // Requisito Notion: Escribir asterisco '*' o guión '-' y espacio al inicio de línea -> Lista desordenada con viñetas
      if (e.key === ' ') {
        const sel = window.getSelection();
        if (sel && sel.rangeCount) {
          const node = sel.anchorNode;
          if (node && node.nodeType === Node.TEXT_NODE) {
            const textBefore = node.textContent.slice(0, sel.anchorOffset);
            if (/^(?:[\s\n\r\xa0]*)[*-]$/.test(textBefore) || /(?:^|[\n\r])[*-]$/.test(textBefore)) {
              e.preventDefault();
              const symbolIdx = Math.max(textBefore.lastIndexOf('*'), textBefore.lastIndexOf('-'));
              node.textContent = node.textContent.slice(0, symbolIdx) + node.textContent.slice(sel.anchorOffset);
              formatDoc('insertUnorderedList');
              return;
            }
            if (/^(?:[\s\n\r\xa0]*)1\.$/.test(textBefore) || /(?:^|[\n\r])1\.$/.test(textBefore)) {
              e.preventDefault();
              const numIdx = textBefore.lastIndexOf('1.');
              node.textContent = node.textContent.slice(0, numIdx) + node.textContent.slice(sel.anchorOffset);
              formatDoc('insertOrderedList');
              return;
            }
          }
        }
      }

      // Block-level Enter key handling
      if (e.key === 'Enter' && !e.shiftKey) {
        const sel = window.getSelection();
        if (sel && sel.rangeCount) {
          const anchor = sel.anchorNode;
          const editableEl = anchor ? (anchor.nodeType === Node.ELEMENT_NODE ? anchor.closest('[contenteditable="true"]') : anchor.parentElement?.closest('[contenteditable="true"]')) : null;
          const blockEl = editableEl ? editableEl.closest('[data-block-id]') : null;
          if (blockEl && blockEl.id !== 'rich-editor-canvas') {
            const btype = blockEl.getAttribute('data-type') || 'text';
            if (btype === 'code') {
              document.execCommand('insertLineBreak');
              e.preventDefault();
              return;
            }
            e.preventDefault();
            insertBlockBelow(blockEl);
            return;
          }
        }
      }

      // Block-level Backspace handling
      if (e.key === 'Backspace') {
        const sel = window.getSelection();
        if (sel && sel.rangeCount) {
          const anchor = sel.anchorNode;
          const editableEl = anchor ? (anchor.nodeType === Node.ELEMENT_NODE ? anchor.closest('[contenteditable="true"]') : anchor.parentElement?.closest('[contenteditable="true"]')) : null;
          const blockEl = editableEl ? editableEl.closest('[data-block-id]') : null;
          if (blockEl && blockEl.id !== 'rich-editor-canvas') {
            const btype = blockEl.getAttribute('data-type') || 'text';
            const textContent = editableEl.textContent.trim();
            if (textContent === '' && btype !== 'text' && btype !== 'p') {
              e.preventDefault();
              convertBlockType(blockEl.getAttribute('data-block-id'), 'text');
              return;
            } else if (textContent === '' && (btype === 'text' || btype === 'p')) {
              const prev = blockEl.previousElementSibling;
              if (prev && prev.getAttribute('data-block-id')) {
                e.preventDefault();
                deleteBlockElement(blockEl, prev);
                return;
              }
            }
          }
        }
      }

      // Triggers al teclear '/'
      if (e.key === '/') {
        openSlashMenu();
      } else if (e.key === 'Escape') {
        closeSlashMenu();
        closeInlineMathPopover();
      }
    }

    function duplicateSelection() {
      const sel = window.getSelection();
      if (!sel || !sel.rangeCount) return;
      const range = sel.getRangeAt(0);
      const text = range.toString();
      if (text) {
        document.execCommand('insertHTML', false, text + ' ' + text);
        syncRichEditor();
      }
    }

    function handleRichEditorInput(e) {
      const editor = document.getElementById('rich-editor-canvas');

      const target = e.target;
      const editableEl = (target && target.closest) ? target.closest('[contenteditable="true"]') : null;
      if (editableEl) {
        const blockEl = editableEl.closest('[data-block-id]');
        if (blockEl && blockEl.id !== 'rich-editor-canvas') {
          const blockId = blockEl.getAttribute('data-block-id');
          const propName = editableEl.getAttribute('data-property') || 'title';
          const tuples = htmlToRichTextTuples(editableEl);
          if (typeof state !== 'undefined' && state.activeRecordMap && state.activeRecordMap.block[blockId]) {
            if (!state.activeRecordMap.block[blockId].value.properties) {
              state.activeRecordMap.block[blockId].value.properties = {};
            }
            state.activeRecordMap.block[blockId].value.properties[propName] = tuples;
          }
          persistBlockUpdate(blockId, { properties: { [propName]: tuples } });
          const btype = blockEl.getAttribute('data-type');
          if (btype === 'header' || btype === 'sub_header' || btype === 'sub_sub_header') {
            if (typeof refreshPageTableOfContents === 'function') {
              refreshPageTableOfContents();
            }
          }
        }
      }

      // Live Markdown Triggers al pulsar espacio
      if (e.data === ' ') {
        applyLiveMarkdownTriggers();
      }

      syncRichEditor();
      renderAllInlineEquations();
    }

    function applyLiveMarkdownTriggers() {
      const sel = window.getSelection();
      if (!sel || !sel.rangeCount) return;
      const node = sel.anchorNode;
      if (!node || node.nodeType !== Node.TEXT_NODE) return;

      const text = node.textContent;
      const caretPos = sel.anchorOffset;
      const textBefore = text.slice(0, caretPos);

      // Requisito: Asterisco + dos espacios (*  ) -> Viñeta
      if (/\*\s\s$/.test(textBefore)) {
        node.textContent = textBefore.replace(/\*\s\s$/, '') + text.slice(caretPos);
        formatDoc('insertUnorderedList');
        return;
      }

      // 1. Block conversions al inicio de línea:
      // "# " -> H1
      if (/^#\s$/.test(textBefore)) {
        node.textContent = text.slice(caretPos);
        formatDoc('formatBlock', '<h1>');
        return;
      }
      // "## " -> H2
      if (/^##\s$/.test(textBefore)) {
        node.textContent = text.slice(caretPos);
        formatDoc('formatBlock', '<h2>');
        return;
      }
      // "### " -> H3
      if (/^###\s$/.test(textBefore)) {
        node.textContent = text.slice(caretPos);
        formatDoc('formatBlock', '<h3>');
        return;
      }
      // "- " o "* " -> Bullet list
      if (/^[-*]\s$/.test(textBefore)) {
        node.textContent = text.slice(caretPos);
        formatDoc('insertUnorderedList');
        return;
      }
      // "1. " -> Numbered list
      if (/^1\.\s$/.test(textBefore)) {
        node.textContent = text.slice(caretPos);
        formatDoc('insertOrderedList');
        return;
      }
      // "[] " o "[ ] " -> Checklist
      if (/^(\[\]|\[ \])\s$/.test(textBefore)) {
        node.textContent = text.slice(caretPos);
        insertChecklistBlock();
        return;
      }
      // "> " -> Toggle list
      if (/^>\s$/.test(textBefore)) {
        node.textContent = text.slice(caretPos);
        insertToggleBlock();
        return;
      }
      // '"" ' -> Quote
      if (/^""\s$/.test(textBefore)) {
        node.textContent = text.slice(caretPos);
        toggleQuoteBlock();
        return;
      }

      // 2. Inline Markdown token transformations:
      // **bold**
      const boldMatch = textBefore.match(/\*\*([^*]+)\*\*\s$/);
      if (boldMatch) {
        const replaceLen = boldMatch[0].length;
        const replaceWith = `<strong>${boldMatch[1]}</strong>&nbsp;`;
        replaceRangeWithHTML(node, caretPos - replaceLen, caretPos, replaceWith);
        return;
      }
      // *italic*
      const italicMatch = textBefore.match(/(?<!\*)\*([^*]+)\*\s$/);
      if (italicMatch) {
        const replaceLen = italicMatch[0].length;
        const replaceWith = `<em>${italicMatch[1]}</em>&nbsp;`;
        replaceRangeWithHTML(node, caretPos - replaceLen, caretPos, replaceWith);
        return;
      }
      // `code`
      const codeMatch = textBefore.match(/`([^`]+)`\s$/);
      if (codeMatch) {
        const replaceLen = codeMatch[0].length;
        const replaceWith = `<code>${codeMatch[1]}</code>&nbsp;`;
        replaceRangeWithHTML(node, caretPos - replaceLen, caretPos, replaceWith);
        return;
      }
      // ~strikethrough~
      const strikeMatch = textBefore.match(/~([^~]+)~\s$/);
      if (strikeMatch) {
        const replaceLen = strikeMatch[0].length;
        const replaceWith = `<del>${strikeMatch[1]}</del>&nbsp;`;
        replaceRangeWithHTML(node, caretPos - replaceLen, caretPos, replaceWith);
        return;
      }
      // $$formula$$ or $formula$ -> Ecuación Matemática KaTeX en línea
      const mathMatch = textBefore.match(/(?:\$\$([^\$]+)\$\$|\$([^\$\s][^\$]*[^\$\s]|\S)\$)\s?$/);
      if (mathMatch) {
        const raw = mathMatch[0];
        const formula = (mathMatch[1] || mathMatch[2] || '').trim();
        if (formula) {
          const replaceLen = raw.length;
          insertInlineKatexAtRange(node, caretPos - replaceLen, caretPos, formula);
          return;
        }
      }
    }

    function replaceRangeWithHTML(textNode, start, end, html) {
      const range = document.createRange();
      range.setStart(textNode, start);
      range.setEnd(textNode, end);
      range.deleteContents();
      const el = document.createElement('div');
      el.innerHTML = html;
      const frag = document.createDocumentFragment();
      let node, lastNode;
      while ((node = el.firstChild)) {
        lastNode = frag.appendChild(node);
      }
      range.insertNode(frag);
      if (lastNode) {
        const sel = window.getSelection();
        range.setStartAfter(lastNode);
        range.collapse(true);
        sel.removeAllRanges();
        sel.addRange(range);
      }
      syncRichEditor();
    }



    /* 4. Ecuaciones KaTeX en Línea (Ctrl+Shift+E) y Barra Flotante de Movimiento */
    let activeInlineKatexNode = null;
    let savedEditorRange = null;

    function openInlineMathPopover() {
      const popover = document.getElementById('inline-math-popover');
      const input = document.getElementById('inline-katex-input');
      const canvas = document.getElementById('rich-editor-canvas');
      const sel = window.getSelection();

      // Verificar si el cursor o selección está dentro de una ecuación existente
      let existingNode = null;
      if (sel && sel.anchorNode && canvas && canvas.contains(sel.anchorNode)) {
        let curr = sel.anchorNode.nodeType === Node.ELEMENT_NODE ? sel.anchorNode : sel.anchorNode.parentElement;
        existingNode = curr ? curr.closest('.inline-katex-node') : null;
      }

      if (existingNode) {
        activeInlineKatexNode = existingNode;
        input.value = existingNode.getAttribute('data-latex') || '';
      } else if (!activeInlineKatexNode) {
        // Guardar rango actual si está dentro del editor
        if (sel && sel.rangeCount > 0 && canvas && canvas.contains(sel.anchorNode)) {
          savedEditorRange = sel.getRangeAt(0).cloneRange();
          const selectedText = sel.toString().trim();
          input.value = selectedText || 'E = mc^2';
        } else {
          input.value = 'E = mc^2';
        }
      }

      updateInlineMathPreview(input.value);
      popover.classList.add('open');

      // Posicionar popover
      const rect = canvas.getBoundingClientRect();
      popover.style.top = `${Math.max(60, rect.top + 20)}px`;
      popover.style.left = `${Math.min(rect.left + 40, window.innerWidth - 410)}px`;

      setTimeout(() => {
        input.focus();
        input.select();
      }, 50);
    }

    function closeInlineMathPopover() {
      document.getElementById('inline-math-popover').classList.remove('open');
      activeInlineKatexNode = null;
    }

    function updateInlineMathPreview(latex) {
      const preview = document.getElementById('inline-katex-preview');
      const val = (latex || '').trim();
      if (!val) {
        preview.innerHTML = '<span style="color:var(--text-muted); font-size:12px;">Escribe una fórmula o macro (ej. E=mc^2, \\frac{a}{b}, \\ce{H2O})</span>';
        return;
      }
      if (window.katex) {
        try {
          window.katex.render(val, preview, { displayMode: false, throwOnError: false });
        } catch (_) {
          preview.textContent = val;
        }
      } else {
        preview.textContent = val;
      }
    }

    function insertMathSnippet(snippet) {
      const input = document.getElementById('inline-katex-input');
      const start = input.selectionStart || 0;
      const end = input.selectionEnd || 0;
      const cur = input.value;
      input.value = cur.slice(0, start) + snippet + cur.slice(end);
      input.focus();
      input.setSelectionRange(start + snippet.length, start + snippet.length);
      updateInlineMathPreview(input.value);
    }

    function saveInlineEquation() {
      const input = document.getElementById('inline-katex-input');
      const latex = (input.value || '').trim() || 'x';

      if (activeInlineKatexNode) {
        activeInlineKatexNode.setAttribute('data-latex', latex);
        activeInlineKatexNode.setAttribute('title', `Ecuación: ${latex} (haz clic para editar)`);
        if (window.katex) {
          try {
            window.katex.render(latex, activeInlineKatexNode, { displayMode: false, throwOnError: false });
          } catch (_) {
            activeInlineKatexNode.textContent = latex;
          }
        }
        activeInlineKatexNode = null;
      } else {
        const span = document.createElement('span');
        span.className = 'inline-equation notion-inline-equation inline-katex-node';
        span.contentEditable = 'false';
        span.setAttribute('data-latex', latex);
        span.setAttribute('title', `Ecuación: ${latex} (haz clic para editar)`);
        span.onclick = function(e) {
          e.stopPropagation();
          editInlineEquation(this);
        };
        if (window.katex) {
          try {
            window.katex.render(latex, span, { displayMode: false, throwOnError: false });
          } catch (_) {
            span.textContent = latex;
          }
        } else {
          span.textContent = latex;
        }

        const editor = document.getElementById('rich-editor-canvas');
        if (savedEditorRange && editor && editor.contains(savedEditorRange.startContainer)) {
          const sel = window.getSelection();
          sel.removeAllRanges();
          sel.addRange(savedEditorRange);
          savedEditorRange.deleteContents();
          savedEditorRange.insertNode(span);
          const space = document.createTextNode('\u00A0');
          span.after(space);
          const newRange = document.createRange();
          newRange.setStartAfter(space);
          newRange.collapse(true);
          sel.removeAllRanges();
          sel.addRange(newRange);
        } else if (editor) {
          editor.appendChild(span);
          editor.appendChild(document.createTextNode('\u00A0'));
        }
      }

      syncRichEditor();
      closeInlineMathPopover();
      showToast('Ecuación en línea insertada', '√x');
    }

    function turnCurrentInlineToBlockEquation() {
      const input = document.getElementById('inline-katex-input');
      const latex = (input.value || '').trim() || '\\int_{0}^{\\infty} e^{-x^2} dx';
      let parentBlockEl = null;
      if (activeInlineKatexNode) {
        parentBlockEl = activeInlineKatexNode.closest ? activeInlineKatexNode.closest('.notion-block') : null;
        activeInlineKatexNode.remove();
        activeInlineKatexNode = null;
      }
      closeInlineMathPopover();

      if (typeof window.createBlock === 'function' && parentBlockEl) {
        const parentId = parentBlockEl.getAttribute('data-parent-id') || (typeof state !== 'undefined' && state.activeNoteId ? String(state.activeNoteId) : null);
        window.createBlock({
          type: 'equation',
          parent_id: parentId,
          after_id: parentBlockEl.id,
          properties: { title: [[latex, []]] },
          crdt_data: typeof buildEquationCrdt === 'function' ? buildEquationCrdt(latex, 1) : {}
        });
        if (typeof showToast === 'function') showToast('Ecuación convertida a bloque', '∑');
        return;
      }

      const note = getActiveNote();
      if (note) {
        note.katex = latex;
        save();
        loadActiveNote();
      }
      if (typeof showToast === 'function') showToast('Ecuación convertida a bloque', '∑');
    }

    function editInlineEquation(spanNode) {
      activeInlineKatexNode = spanNode;
      const input = document.getElementById('inline-katex-input');
      input.value = spanNode.getAttribute('data-latex') || '';
      openInlineMathPopover();
    }

    function insertInlineKatexAtRange(textNode, start, end, latex) {
      const range = document.createRange();
      range.setStart(textNode, start);
      range.setEnd(textNode, end);
      range.deleteContents();

      const span = document.createElement('span');
      span.className = 'inline-katex-node';
      span.contentEditable = 'false';
      span.setAttribute('data-latex', latex);
      span.setAttribute('title', `Ecuación: ${latex} (haz clic para editar)`);
      span.onclick = function(e) {
        e.stopPropagation();
        editInlineEquation(this);
      };
      if (window.katex) {
        try {
          window.katex.render(latex, span, { displayMode: false, throwOnError: false });
        } catch (_) {
          span.textContent = latex;
        }
      } else {
        span.textContent = latex;
      }

      range.insertNode(span);
      const space = document.createTextNode('\u00A0');
      span.after(space);

      const sel = window.getSelection();
      range.setStartAfter(space);
      range.collapse(true);
      sel.removeAllRanges();
      sel.addRange(range);

      syncRichEditor();
    }

    function renderAllInlineEquations() {
      if (!window.katex) return;
      const nodes = document.querySelectorAll('.inline-katex-node, .notion-inline-equation, .inline-equation');
      nodes.forEach(node => {
        const latex = node.getAttribute('data-latex') || node.textContent;
        node.setAttribute('data-latex', latex);
        node.setAttribute('title', `Ecuación: ${latex} (haz clic para editar)`);
        node.onclick = function(e) {
          e.stopPropagation();
          editInlineEquation(this);
        };
        try {
          window.katex.render(latex, node, { displayMode: false, throwOnError: false });
        } catch (_) {}
      });
    }
    window.renderAllInlineEquations = renderAllInlineEquations;
    window.editInlineEquation = editInlineEquation;

    /* 5. Controles de Movimiento (Drag & Drop) y Eliminación de Bloques */
    let currentDraggedBlock = null;

    function setupBlockDragAndDrop() {
      const container = document.getElementById('blocks-container');
      if (!container) return;

      const blocks = Array.from(container.children).filter(el => el.id && el.id.startsWith('block-'));

      blocks.forEach(block => {
        // Eventos de destino (Drop target)
        block.ondragover = function(e) {
          if (!currentDraggedBlock || currentDraggedBlock === block) return;
          e.preventDefault();
          e.dataTransfer.dropEffect = 'move';

          const rect = block.getBoundingClientRect();
          const mid = rect.top + (rect.height / 2);
          block.classList.remove('drag-over-top', 'drag-over-bottom');
          if (e.clientY < mid) {
            block.classList.add('drag-over-top');
          } else {
            block.classList.add('drag-over-bottom');
          }
        };

        block.ondragleave = function(e) {
          block.classList.remove('drag-over-top', 'drag-over-bottom');
        };

        block.ondrop = function(e) {
          if (!currentDraggedBlock || currentDraggedBlock === block) return;
          e.preventDefault();
          const isTop = block.classList.contains('drag-over-top');
          block.classList.remove('drag-over-top', 'drag-over-bottom');

          if (isTop) {
            block.before(currentDraggedBlock);
          } else {
            block.after(currentDraggedBlock);
          }
          persistBlocksOrder();
          cleanupDragStates();
        };

        // Asignar eventos de arrastre a los botones/manijas
        const handles = block.querySelectorAll('.btn-drag-handle-btn, .block-drag-handle, .btn-side-drag');
        handles.forEach(handle => {
          handle.setAttribute('draggable', 'true');

          handle.ondragstart = function(e) {
            currentDraggedBlock = block;
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', block.id);
            setTimeout(() => {
              if (currentDraggedBlock) {
                currentDraggedBlock.classList.add('block-is-dragging');
              }
            }, 10);
          };

          handle.ondragend = function() {
            cleanupDragStates();
          };

          // Soporte de pulsación prolongada (Long-Press) para bloques
          setupLongPressBlockReorder(handle, block);
        });
      });

      // Permitir soltar al final del contenedor
      container.ondragover = function(e) {
        if (!currentDraggedBlock) return;
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
      };

      container.ondrop = function(e) {
        if (!currentDraggedBlock) return;
        if (e.target === container) {
          e.preventDefault();
          container.appendChild(currentDraggedBlock);
          persistBlocksOrder();
          cleanupDragStates();
        }
      };
    }

    function setupLongPressBlockReorder(handle, block) {
      let timer = null;
      let startY = 0;
      let isLongPressActive = false;

      handle.addEventListener('pointerdown', (e) => {
        startY = e.clientY || 0;
        isLongPressActive = false;
        timer = setTimeout(() => {
          isLongPressActive = true;
          currentDraggedBlock = block;
          block.classList.add('block-is-dragging');
          if (navigator.vibrate) navigator.vibrate(35);
          showToast('Modo reordenar bloque activo: arrastra arriba o abajo', '↕️');
        }, 260);
      });

      window.addEventListener('pointermove', (e) => {
        if (!isLongPressActive) {
          if (Math.abs((e.clientY || 0) - startY) > 8) clearTimeout(timer);
          return;
        }
        e.preventDefault();
        const target = document.elementFromPoint(e.clientX, e.clientY)?.closest('.callout-box, .quote-block, .toggle-block, .code-block, .notion-block-box');
        document.querySelectorAll('.drag-over-top, .drag-over-bottom').forEach(el => {
          if (el !== target) el.classList.remove('drag-over-top', 'drag-over-bottom');
        });
        if (target && target !== block) {
          const rect = target.getBoundingClientRect();
          if (e.clientY < rect.top + rect.height / 2) {
            target.classList.add('drag-over-top');
          } else {
            target.classList.add('drag-over-bottom');
          }
        }
      }, { passive: false });

      window.addEventListener('pointerup', (e) => {
        if (isLongPressActive) {
          const target = document.elementFromPoint(e.clientX, e.clientY)?.closest('.callout-box, .quote-block, .toggle-block, .code-block, .notion-block-box');
          if (target && target !== block) {
            const isTop = target.classList.contains('drag-over-top');
            if (isTop) target.before(block);
            else target.after(block);
            persistBlocksOrder();
          }
        }
        clearTimeout(timer);
        isLongPressActive = false;
        cleanupDragStates();
      });
    }

    function cleanupDragStates() {
      currentDraggedBlock = null;
      document.querySelectorAll('.block-is-dragging, .drag-over-top, .drag-over-bottom').forEach(el => {
        el.classList.remove('block-is-dragging', 'drag-over-top', 'drag-over-bottom');
      });
    }

    function persistBlocksOrder() {
      const note = getActiveNote();
      if (!note) return;
      const container = document.getElementById('blocks-container');
      if (!container) return;

      note.blocksOrder = Array.from(container.children)
        .filter(el => el.id && el.id.startsWith('block-'))
        .map(el => el.id);
      save();
    }

    function restoreBlocksOrder() {
      const note = getActiveNote();
      if (!note || !note.blocksOrder || !Array.isArray(note.blocksOrder)) return;
      const container = document.getElementById('blocks-container');
      if (!container) return;

      note.blocksOrder.forEach(id => {
        const el = document.getElementById(id);
        if (el && container.contains(el)) {
          container.appendChild(el);
        }
      });
    }

    function moveBlockElementUp(blockId) {
      const el = document.getElementById(blockId);
      if (!el) return;
      const prev = el.previousElementSibling;
      if (prev && prev.id !== 'rich-editor-canvas') {
        prev.before(el);
        persistBlocksOrder();
      }
    }

    function moveBlockElementDown(blockId) {
      const el = document.getElementById(blockId);
      if (!el) return;
      const next = el.nextElementSibling;
      if (next) {
        next.after(el);
        persistBlocksOrder();
      }
    }

    function deleteBlock(key) {
      const note = getActiveNote();
      if (!note) return;
      if (key === 'callout') note.showCallout = false;
      else if (key === 'quote') note.showQuote = false;
      else if (key === 'toggle') note.showToggle = false;
      else if (key === 'code') note.showCode = false;
      else if (key === 'kanban') note.showKanban = false;
      else if (key === 'table') note.showTable = false;
      else if (key === 'checklists') note.showChecklist = false;
      else if (key === 'katex') note.katex = '';
      save();
      loadActiveNote();
    }

    /* 6. Barra Flotante de Selección y Movimiento de Líneas */
    function handleSelectionChange() {
      const sel = window.getSelection();
      const bar = document.getElementById('floating-selection-bar');
      if (!bar) return;

      if (!sel || sel.isCollapsed || !sel.rangeCount) {
        bar.classList.remove('open');
        return;
      }

      const editor = document.getElementById('rich-editor-canvas');
      const anchor = sel.anchorNode;
      if (!anchor || !editor.contains(anchor)) {
        bar.classList.remove('open');
        return;
      }

      const range = sel.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) {
        bar.classList.remove('open');
        return;
      }

      bar.style.top = `${Math.max(10, rect.top - 38 + window.scrollY)}px`;
      bar.style.left = `${Math.max(10, Math.min(rect.left, window.innerWidth - 320))}px`;
      bar.classList.add('open');
    }

    function moveSelectedLine(dir) {
      const sel = window.getSelection();
      if (!sel || !sel.rangeCount) return;
      let node = sel.anchorNode;
      if (!node) return;
      if (node.nodeType === Node.TEXT_NODE) node = node.parentElement;

      const editor = document.getElementById('rich-editor-canvas');
      while (node && node.parentElement !== editor && node !== editor) {
        node = node.parentElement;
      }

      if (!node || node === editor) return;

      if (dir < 0 && node.previousElementSibling) {
        node.previousElementSibling.before(node);
      } else if (dir > 0 && node.nextElementSibling) {
        node.nextElementSibling.after(node);
      }
      syncRichEditor();
    }

    function deleteSelectionOrLine() {
      const sel = window.getSelection();
      if (sel && !sel.isCollapsed) {
        document.execCommand('delete');
        syncRichEditor();
      }
    }

    /* 5. Slash Command (/) con búsqueda y colores Notion */
    function openSlashMenu() {
      const menu = document.getElementById('slash-menu');
      menu.classList.add('open');
      const canvas = document.getElementById('rich-editor-canvas');
      const rect = canvas.getBoundingClientRect();
      menu.style.top = `${rect.top + 30}px`;
      menu.style.left = `${Math.min(rect.left + 20, window.innerWidth - 340)}px`;
      document.getElementById('slash-search-input').value = '';
      renderSlashMenuItems('');
      setTimeout(() => document.getElementById('slash-search-input').focus(), 50);
    }

    function closeSlashMenu() {
      document.getElementById('slash-menu').classList.remove('open');
    }

    function filterSlashMenu(q) {
      renderSlashMenuItems(q.toLowerCase().trim());
    }

    function renderSlashMenuItems(q) {
      const container = document.getElementById('slash-menu-items');
      const filtered = SLASH_TAXONOMY.filter(item => {
        if (!q) return true;
        return item.title.toLowerCase().includes(q) ||
               item.desc.toLowerCase().includes(q) ||
               item.id.includes(q) ||
               (item.cat && item.cat.toLowerCase().includes(q));
      });

      if (!filtered.length) {
        container.innerHTML = `<div style="text-align:center; padding:18px; color:var(--text-muted); font-size:12px;">Sin comandos encontrados</div>`;
        return;
      }

      let lastCat = '';
      let html = '';
      filtered.forEach(item => {
        const cat = item.cat || 'Bloques';
        if (cat !== lastCat) {
          lastCat = cat;
          html += `<div style="font-size:10px; font-weight:800; color:var(--text-muted); padding:7px 10px 3px; text-transform:uppercase; letter-spacing:0.05em; border-top:1px solid var(--border-hairline); margin-top:3px;">${cat}</div>`;
        }
        html += `
          <button class="slash-item" onclick="executeSlashCommand('${item.id}')">
            <span style="font-weight:700; width:22px; text-align:center;">${item.icon}</span>
            <div>
              <div style="font-weight:600;">${item.title}</div>
              <div class="slash-item-desc">${item.desc}</div>
            </div>
          </button>
        `;
      });
      container.innerHTML = html;
    }

    function scrollAndHighlightBlock(blockId, focusSelector = null) {
      setTimeout(() => {
        const el = document.getElementById(blockId);
        if (!el) return;
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        const origOutline = el.style.outline;
        el.style.outline = '2px solid var(--accent-amber)';
        el.style.outlineOffset = '2px';
        setTimeout(() => {
          el.style.outline = origOutline;
        }, 1200);
        if (focusSelector) {
          const focusEl = el.querySelector(focusSelector) || document.querySelector(focusSelector);
          if (focusEl && typeof focusEl.focus === 'function') {
            focusEl.focus();
          }
        }
      }, 60);
    }

    function executeSlashCommand(id) {
      closeSlashMenu();
      const note = getActiveNote();
      if (!note) return;

      const activeBlock = (typeof document !== 'undefined' && document.activeElement) ? document.activeElement.closest('.notion-block') : null;
      const activeBlockId = activeBlock ? activeBlock.getAttribute('data-block-id') : null;

      if (id === 'text') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'text');
        else formatDoc('formatBlock', '<p>');
      } else if (id === 'heading1') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'header');
        else formatDoc('formatBlock', '<h1>');
      } else if (id === 'heading2') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'sub_header');
        else formatDoc('formatBlock', '<h2>');
      } else if (id === 'heading3') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'sub_sub_header');
        else formatDoc('formatBlock', '<h3>');
      } else if (id === 'heading4') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'header_4');
        else formatDoc('formatBlock', '<h4>');
      } else if (id === 'todo') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'to_do');
        else insertChecklistBlock();
      } else if (id === 'bullet') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'bulleted_list');
        else formatDoc('insertUnorderedList');
      } else if (id === 'numbered') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'numbered_list');
        else formatDoc('insertOrderedList');
      } else if (id === 'toggle') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'toggle');
        else insertToggleBlock();
      } else if (id === 'inline_toggle') {
        insertInlineToggleElement();
      } else if (id === 'callout') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'callout');
        else toggleCalloutBlock(true);
      } else if (id === 'inline_callout') {
        insertInlineCalloutElement();
      } else if (id === 'simple_table') {
        insertSimpleTableBlock();
      } else if (id === 'quote') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'quote');
        else toggleQuoteBlock(true);
      } else if (id === 'video') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'video');
        else if (typeof openMediaEmbedModal === 'function') openMediaEmbedModal('video');
      } else if (id === 'audio') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'audio');
        else if (typeof openMediaEmbedModal === 'function') openMediaEmbedModal('audio');
      } else if (id === 'file') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'file');
        else if (typeof openMediaEmbedModal === 'function') openMediaEmbedModal('file');
      } else if (id === 'pdf') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'pdf');
        else if (typeof openMediaEmbedModal === 'function') openMediaEmbedModal('pdf');
      } else if (id === 'bookmark') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'bookmark');
        else if (typeof openMediaEmbedModal === 'function') openMediaEmbedModal('bookmark');
      } else if (id === 'code') {
        insertInlineCodeBlock();
      } else if (id === 'divider') {
        insertDividerElement();
      } else if (id === 'table' || id === 'db_table') {
        openDatabaseWithView('table');
      } else if (id === 'kanban' || id === 'db_board') {
        openDatabaseWithView('board');
      } else if (id === 'db_gallery') {
        openDatabaseWithView('gallery');
      } else if (id === 'db_list') {
        openDatabaseWithView('list');
      } else if (id === 'db_calendar') {
        openDatabaseWithView('calendar');
      } else if (id === 'db_timeline') {
        openDatabaseWithView('timeline');
      } else if (id === 'katex') {
        toggleKatexBlock(true);
      } else if (id === 'image') {
        openImageInsertModal();
      } else if (id === 'pdf_file') {
        openMediaEmbedModal('pdf');
      } else if (id === 'catalog') {
        toggleBlockCatalog(true);
      } else if (id.startsWith('embed_') && id !== 'embed_note') {
        openMediaEmbedModal(id.replace('embed_', ''));
      } else if (id === 'inline_math') {
        openInlineMathPopover();
      } else if (id === 'embed_note') {
        promptAddShortcut();
      } else if (id === 'subpage') {
        insertSubpageBlock();
      } else if (id === 'columns') {
        insertColumnsBlock(2);
      } else if (id === 'columns3') {
        insertColumnsBlock(3);
      } else if (id === 'toc') {
        insertTableOfContentsBlock();
      } else if (id === 'synced') {
        if (activeBlockId && typeof convertBlockType === 'function') convertBlockType(activeBlockId, 'transclusion_container');
        else insertSyncedBlock();
      } else if (id === 'button') {
        openMacroButtonModal();
      } else if (id === 'breadcrumbs') {
        insertBreadcrumbsBlock();
      } else if (id.startsWith('color_')) {
        const color = id.replace('color_', '');
        document.execCommand('foreColor', false, getNotionColorHex(color));
        syncRichEditor();
      } else if (id.startsWith('bg_')) {
        const color = id.replace('bg_', '');
        document.execCommand('hiliteColor', false, getNotionBgHex(color));
        syncRichEditor();
      }
    }

    function getNotionColorHex(color) {
      const map = { amber: '#f59e0b', blue: '#3b82f6', green: '#10b981', red: '#ef4444', purple: '#a855f7' };
      return map[color] || '#f59e0b';
    }
    function getNotionBgHex(color) {
      const map = { amber: 'rgba(245,158,11,0.25)', green: 'rgba(16,185,129,0.25)', blue: 'rgba(59,130,246,0.25)', red: 'rgba(239,68,68,0.25)' };
      return map[color] || 'rgba(245,158,11,0.25)';
    }

    /* 6. Tabla de Propiedades con Fórmulas 2.0 y Evaluación Dinámica */
    function togglePropertiesTableBlock(forceShow = false) {
      const note = getActiveNote();
      if (!note) return;
      note.showTable = forceShow ? true : !note.showTable;
      if (!note.tableRows || !note.tableRows.length) {
        note.tableRows = [
          { name: "Licencia de Servidor", status: "Listo", category: "Infra", date: "27 Oct", amount: 120 },
          { name: "Desarrollo de Bloques", status: "En Proceso", category: "Dev", date: "28 Oct", amount: 350 },
          { name: "Auditoría de Rendimiento", status: "Pendiente", category: "QA", date: "29 Oct", amount: 180 }
        ];
      }
      if (!note.tableFormula) {
        note.tableFormula = 'style(upper(prop("Nombre")), "b", "blue")';
      }
      save();
      loadActiveNote();
      if (note.showTable) {
        scrollAndHighlightBlock('block-table', '#properties-table-body input');
        showToast('Base de Datos Notion activa', '🗄️');
      }
    }

    function renderTable(note) {
      const tbody = document.getElementById('properties-table-body');
      if (!tbody) return;
      const rows = note.tableRows || [];
      const formulaExpr = note.tableFormula || 'style(upper(prop("Nombre")), "b", "blue")';

      tbody.innerHTML = rows.map((row, idx) => {
        const formulaHtml = evaluateFormula2(formulaExpr, row);
        return `
          <tr data-row-idx="${idx}" title="Clic derecho para opciones de fila">
            <td><input type="text" value="${row.name}" oninput="updateTableRow(${idx}, 'name', this.value)" /></td>
            <td><input type="text" value="${row.status}" oninput="updateTableRow(${idx}, 'status', this.value)" /></td>
            <td><input type="text" value="${row.category}" oninput="updateTableRow(${idx}, 'category', this.value)" /></td>
            <td><input type="text" value="${row.date}" oninput="updateTableRow(${idx}, 'date', this.value)" /></td>
            <td><input type="number" class="tabular-nums" style="text-align:right;" value="${row.amount || 0}" oninput="updateTableRow(${idx}, 'amount', Number(this.value))" /></td>
            <td style="vertical-align:middle;">${formulaHtml}</td>
            <td style="white-space:nowrap; text-align:center;">
              <button class="btn-icon-tiny" onclick="moveTableRow(${idx}, -1)" title="Subir fila">▲</button>
              <button class="btn-icon-tiny" onclick="moveTableRow(${idx}, 1)" title="Bajar fila">▼</button>
              <button class="btn-icon-tiny btn-danger-tiny" onclick="deleteTableRow(${idx})" title="Eliminar fila">🗑</button>
            </td>
          </tr>
        `;
      }).join('');

      // Cálculos al pie de tabla (Count, % Listo, Sum Total)
      const totalCount = rows.length;
      const doneCount = rows.filter(r => (r.status || '').toLowerCase().includes('listo') || (r.status || '').toLowerCase().includes('pagado') || (r.status || '').toLowerCase().includes('done')).length;
      const pctDone = totalCount > 0 ? Math.round((doneCount / totalCount) * 100) : 0;
      const sumTotal = rows.reduce((acc, r) => acc + (Number(r.amount) || 0), 0);

      document.getElementById('calc-count').textContent = `Conteo: ${totalCount}`;
      document.getElementById('calc-done-pct').textContent = `% Listo: ${pctDone}%`;
      document.getElementById('calc-sum-total').textContent = `Suma: $${sumTotal.toLocaleString()}`;

      if (typeof renderDatabaseActiveView === 'function') {
        renderDatabaseActiveView(note);
      }
    }

    function moveTableRow(idx, dir) {
      const note = getActiveNote();
      if (!note || !note.tableRows) return;
      const target = idx + dir;
      if (target < 0 || target >= note.tableRows.length) return;
      const item = note.tableRows.splice(idx, 1)[0];
      note.tableRows.splice(target, 0, item);
      save();
      renderTable(note);
    }

    function deleteTableRow(idx) {
      const note = getActiveNote();
      if (!note || !note.tableRows) return;
      note.tableRows.splice(idx, 1);
      save();
      renderTable(note);
    }

    function addTableRow() {
      const note = getActiveNote();
      if (!note) return;
      note.tableRows = note.tableRows || [];
      note.tableRows.push({ name: "Nuevo ítem", status: "Pendiente", category: "General", date: "27 Oct", amount: 100 });
      save();
      renderTable(note);
    }

    function updateTableRow(idx, field, val) {
      const note = getActiveNote();
      if (!note || !note.tableRows[idx]) return;
      note.tableRows[idx][field] = val;
      save();
      renderTable(note);
    }

    /* Evaluador de Fórmulas 2.0 Notion con style() */
    function evaluateFormula2(expression, row) {
      if (!expression || !expression.trim()) return '<span style="color:var(--text-muted);">-</span>';

      try {
        // Funciones del motor Notion Formulas 2.0
        const prop = (colName) => {
          const key = (colName || '').toLowerCase().trim();
          if (key === 'nombre' || key === 'name') return String(row.name || '');
          if (key === 'estado' || key === 'status') return String(row.status || '');
          if (key === 'categoría' || key === 'categoria' || key === 'category') return String(row.category || '');
          if (key === 'fecha' || key === 'date') return String(row.date || '');
          if (key === 'monto' || key === 'amount') return Number(row.amount || 0);
          return '';
        };

        const format = (val) => String(val);
        const concat = (...args) => args.join('');
        const join = (list, sep = ', ') => (Array.isArray(list) ? list.join(sep) : String(list));
        const substring = (str, start, end) => String(str).substring(start, end);
        const contains = (str, search) => String(str).toLowerCase().includes(String(search).toLowerCase());
        const replace = (str, pattern, replacement) => String(str).replace(new RegExp(pattern, 'i'), replacement);
        const replaceAll = (str, pattern, replacement) => String(str).replace(new RegExp(pattern, 'gi'), replacement);
        const padStart = (str, len, pad = '0') => String(str).padStart(len, pad);
        const padEnd = (str, len, pad = ' ') => String(str).padEnd(len, pad);
        const length = (str) => String(str).length;
        const lower = (str) => String(str).toLowerCase();
        const upper = (str) => String(str).toUpperCase();
        const iff = (condition, ifTrue, ifFalse) => (condition ? ifTrue : ifFalse);

        const style = (text, ...styles) => {
          const classes = styles.map(s => `fmt-${s}`).join(' ');
          return `<span class="formula-badge-cell ${classes}">${text}</span>`;
        };

        // Crear contexto de evaluación seguro
        const sanitizedExpr = expression.replace(/\bif\s*\(/g, 'iff(');
        const evaluator = new Function(
          'prop', 'format', 'concat', 'join', 'substring', 'contains', 'replace', 'replaceAll',
          'padStart', 'padEnd', 'length', 'lower', 'upper', 'iff', 'style',
          `return (${sanitizedExpr});`
        );

        const result = evaluator(
          prop, format, concat, join, substring, contains, replace, replaceAll,
          padStart, padEnd, length, lower, upper, iff, style
        );

        return result !== undefined && result !== null ? String(result) : '<span style="color:var(--text-muted);">-</span>';
      } catch (err) {
        return `<span style="color:var(--danger); font-size:11px;" title="${err.message}">⚠️ Error de fórmula</span>`;
      }
    }

    /* Modal de Fórmulas 2.0 */
    function openFormulaModal() {
      const note = getActiveNote();
      if (!note) return;
      const modal = document.getElementById('formula-modal');
      const input = document.getElementById('formula-expression-input');
      input.value = note.tableFormula || 'style(upper(prop("Nombre")), "b", "blue")';
      updateFormulaPreview();
      input.oninput = updateFormulaPreview;
      modal.classList.add('open');
    }

    function closeFormulaModal() {
      document.getElementById('formula-modal').classList.remove('open');
    }

    function updateFormulaPreview() {
      const note = getActiveNote();
      const expr = document.getElementById('formula-expression-input').value;
      const sampleRow = (note.tableRows && note.tableRows[0]) || { name: "Proyecto Alfa", status: "Listo", category: "Dev", date: "27 Oct", amount: 250 };
      const res = evaluateFormula2(expr, sampleRow);
      document.getElementById('formula-preview-result').innerHTML = res;
    }

    function setFormulaPreset(preset) {
      document.getElementById('formula-expression-input').value = preset;
      updateFormulaPreview();
    }

    function saveFormulaExpression() {
      const note = getActiveNote();
      if (!note) return;
      const expr = document.getElementById('formula-expression-input').value;
      note.tableFormula = expr;
      save();
      renderTable(note);
      closeFormulaModal();
    }

    /* Inserción y Drag & Drop Libre de Notas en Cualquier Lugar del Texto */
    let draggedNoteCardId = null;
    let cardBeingMovedFromEditor = null;
    let savedSelectionRange = null;

    function handleNoteCardDragStart(e, noteId) {
      draggedNoteCardId = noteId;
      e.dataTransfer.effectAllowed = 'copyMove';
      e.dataTransfer.setData('application/notejs-note-id', String(noteId));
      e.dataTransfer.setData('text/plain', 'note:' + noteId);

      const card = e.currentTarget;
      if (card) {
        setTimeout(() => {
          card.classList.add('is-being-dragged');
        }, 10);
      }
    }

    function handleNoteCardDragEnd(e) {
      draggedNoteCardId = null;
      cardBeingMovedFromEditor = null;
      document.querySelectorAll('.is-being-dragged').forEach(el => el.classList.remove('is-being-dragged'));
      document.querySelectorAll('.drag-over-active').forEach(el => el.classList.remove('drag-over-active'));
    }

    function generateEmbeddedNoteCardHtml(targetNote) {
      const escapedTitle = (targetNote.title || 'Sin título').replace(/"/g, '&quot;');
      const emoji = targetNote.emoji || '📝';
      const folder = targetNote.folder || 'General';
      const coverBg = (targetNote.hasCover && targetNote.coverStyle)
        ? targetNote.coverStyle
        : (targetNote.coverStyle || COVER_PRESETS[Math.abs(targetNote.id) % COVER_PRESETS.length]);

      return `
        <div class="note-embedded-card" 
             contenteditable="false" 
             data-note-id="${targetNote.id}" 
             draggable="true"
             style="background:${coverBg}; background-size:cover; background-position:center ${targetNote.coverPositionY ?? 50}%;" 
             title="Haz clic para abrir nota: ${escapedTitle}">
          <div class="embedded-card-top">
            <span class="embedded-card-badge">
              <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 3h6v6m0-6L10 14"/></svg>
              Acceso
            </span>
            <button class="btn-delete-embedded-card" title="Quitar este acceso del documento" aria-label="Eliminar acceso">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 6h18m-2 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </button>
          </div>
          <div class="embedded-card-bottom">
            <div class="embedded-card-title-row">
              <span class="embedded-card-emoji">${emoji}</span>
              <span class="embedded-card-title">${escapedTitle}</span>
            </div>
            <div class="embedded-card-meta">
              <span class="embedded-card-folder">${folder}</span>
              <span>· ↗ Abrir</span>
            </div>
          </div>
        </div>
      `.trim();
    }

    function setupRichEditorNoteDrop() {
      const canvas = document.getElementById('rich-editor-canvas');
      if (!canvas) return;

      canvas.ondragover = function(e) {
        const hasFiles = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0;
        const hasTypes = e.dataTransfer && Array.from(e.dataTransfer.types || []).includes('Files');
        if (!draggedNoteCardId && !hasFiles && !hasTypes) return;
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
        canvas.classList.add('drag-over-active');
      };

      canvas.ondragleave = function(e) {
        if (e.relatedTarget && canvas.contains(e.relatedTarget)) return;
        canvas.classList.remove('drag-over-active');
      };

      canvas.ondrop = function(e) {
        canvas.classList.remove('drag-over-active');

        // 1. Si el usuario suelta archivos de imagen locales desde su PC directamente en el lienzo
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          const imageFiles = Array.from(e.dataTransfer.files).filter(f => f.type && f.type.startsWith('image/'));
          if (imageFiles.length > 0) {
            e.preventDefault();
            e.stopPropagation();
            saveCaretRangeFromMouseEvent(e);
            imageFiles.forEach(file => {
              readAndInsertLocalImageFile(file);
            });
            return;
          }
        }

        // 2. Si el usuario suelta una tarjeta de nota para incrustarla
        let noteId = draggedNoteCardId;
        if (!noteId && e.dataTransfer) {
          const rawId = e.dataTransfer.getData('application/notejs-note-id') || e.dataTransfer.getData('text/plain');
          if (rawId) {
            const parsed = rawId.replace('note:', '');
            if (Number(parsed)) noteId = Number(parsed);
          }
        }
        if (!noteId) return;
        e.preventDefault();

        insertNoteCardAtDropPoint(Number(noteId), e);
        draggedNoteCardId = null;
      };
    }

    function insertNoteCardAtDropPoint(sourceId, e) {
      const activeNote = getActiveNote();
      if (!activeNote) return;

      if (activeNote.id === sourceId) {
        showToast('No puedes insertar la misma nota dentro de sí misma', '⚠️');
        return;
      }

      const targetNote = state.notes.find(n => n.id === sourceId);
      if (!targetNote) return;

      if (cardBeingMovedFromEditor) {
        cardBeingMovedFromEditor.remove();
        cardBeingMovedFromEditor = null;
      }

      const cardHtml = generateEmbeddedNoteCardHtml(targetNote);
      const canvas = document.getElementById('rich-editor-canvas');

      let range = null;
      if (document.caretRangeFromPoint) {
        range = document.caretRangeFromPoint(e.clientX, e.clientY);
      } else if (document.caretPositionFromPoint) {
        const pos = document.caretPositionFromPoint(e.clientX, e.clientY);
        if (pos && pos.offsetNode) {
          range = document.createRange();
          range.setStart(pos.offsetNode, pos.offset);
          range.collapse(true);
        }
      }

      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = `${cardHtml}&nbsp;`;
      const frag = document.createDocumentFragment();
      while (tempDiv.firstChild) {
        frag.appendChild(tempDiv.firstChild);
      }

      if (range && canvas.contains(range.startContainer)) {
        const existingCard = range.startContainer.nodeType === 1
          ? range.startContainer.closest('.note-embedded-card')
          : range.startContainer.parentElement?.closest('.note-embedded-card');

        if (existingCard) {
          existingCard.after(frag);
        } else {
          range.insertNode(frag);
        }
      } else {
        canvas.appendChild(frag);
      }

      syncRichEditor();
      showToast(`Acceso directo a "${targetNote.title}" insertado en este punto`, '📌');
    }

    function insertNoteCardAtSelection(sourceId, savedRange = null) {
      const activeNote = getActiveNote();
      if (!activeNote) return;

      if (activeNote.id === sourceId) {
        showToast('No puedes insertar la misma nota dentro de sí misma', '⚠️');
        return;
      }

      const targetNote = state.notes.find(n => n.id === sourceId);
      if (!targetNote) return;

      const cardHtml = generateEmbeddedNoteCardHtml(targetNote);
      const canvas = document.getElementById('rich-editor-canvas');

      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = `${cardHtml}&nbsp;`;
      const frag = document.createDocumentFragment();
      while (tempDiv.firstChild) {
        frag.appendChild(tempDiv.firstChild);
      }

      let inserted = false;
      if (savedRange && canvas.contains(savedRange.startContainer)) {
        savedRange.insertNode(frag);
        inserted = true;
      } else {
        const sel = window.getSelection();
        if (sel && sel.rangeCount > 0 && canvas.contains(sel.anchorNode)) {
          const r = sel.getRangeAt(0);
          r.insertNode(frag);
          inserted = true;
        }
      }

      if (!inserted) {
        canvas.appendChild(frag);
      }

      syncRichEditor();
      showToast(`Acceso vertical a "${targetNote.title}" insertado en el texto`, '📌');
    }

    function attachEmbeddedNoteCardListeners() {
      const canvas = document.getElementById('rich-editor-canvas');
      if (!canvas || canvas.dataset.delegatedNoteCards) return;
      canvas.dataset.delegatedNoteCards = 'true';

      canvas.addEventListener('click', (e) => {
        const delBtn = e.target.closest('.btn-delete-embedded-card');
        if (delBtn) {
          e.preventDefault();
          e.stopPropagation();
          const card = delBtn.closest('.note-embedded-card');
          if (card) {
            card.remove();
            syncRichEditor();
            showToast('Acceso directo eliminado del documento', '🗑️');
          }
          return;
        }

        const card = e.target.closest('.note-embedded-card');
        if (card) {
          e.preventDefault();
          e.stopPropagation();
          const targetId = Number(card.getAttribute('data-note-id'));
          if (targetId) {
            selectNote(targetId);
          }
        }
      });

      canvas.addEventListener('dragstart', (e) => {
        const card = e.target.closest('.note-embedded-card');
        if (card) {
          cardBeingMovedFromEditor = card;
          draggedNoteCardId = Number(card.getAttribute('data-note-id'));
          e.dataTransfer.effectAllowed = 'move';
          e.dataTransfer.setData('application/notejs-note-id', String(draggedNoteCardId));
          e.dataTransfer.setData('text/plain', 'note:' + draggedNoteCardId);
          card.classList.add('is-being-dragged');
        }
      });

      canvas.addEventListener('dragend', () => {
        cardBeingMovedFromEditor = null;
        draggedNoteCardId = null;
        document.querySelectorAll('.is-being-dragged').forEach(el => el.classList.remove('is-being-dragged'));
        canvas.classList.remove('drag-over-active');
      });
    }

    function renderSubpages(note) {
      // Compatibilidad: garantizar manejadores activos
      attachEmbeddedNoteCardListeners();
      attachSubpageBlockListeners();
    }

    // -------------------------------------------------------------------------
    // Notion Rich Text Tuple Engine & Full Block Suite (Milestone 3)
    // -------------------------------------------------------------------------

    const NOTION_COLOR_HEX_MAP = {
      default: 'inherit',
      gray: 'var(--text-muted, #9ca3af)',
      brown: '#92400e',
      orange: '#ea580c',
      yellow: 'var(--accent-amber, #f59e0b)',
      green: '#16a34a',
      teal: '#0d9488',
      blue: '#3b82f6',
      purple: '#a855f7',
      pink: '#ec4899',
      red: 'var(--danger, #ef4444)',
      gray_background: 'rgba(148, 163, 184, 0.25)',
      brown_background: 'rgba(146, 64, 14, 0.25)',
      orange_background: 'rgba(234, 88, 12, 0.25)',
      yellow_background: 'rgba(245, 158, 11, 0.25)',
      green_background: 'rgba(22, 163, 74, 0.25)',
      teal_background: 'rgba(13, 148, 136, 0.25)',
      blue_background: 'rgba(59, 130, 246, 0.25)',
      purple_background: 'rgba(168, 85, 247, 0.25)',
      pink_background: 'rgba(236, 72, 153, 0.25)',
      red_background: 'rgba(239, 68, 68, 0.25)'
    };

    function escapeHtml(str) {
      if (str == null) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    const DANGEROUS_URL_SCHEMES_JS = ['javascript:', 'data:', 'vbscript:', 'file:'];

    function sanitizeLinkUrl(rawUrl) {
      if (!rawUrl || typeof rawUrl !== 'string') return '#';
      const trimmed = rawUrl.trim();
      const lower = trimmed.toLowerCase();
      for (const scheme of DANGEROUS_URL_SCHEMES_JS) {
        if (lower.startsWith(scheme)) return '#';
      }
      return trimmed;
    }

    function parseRichTextToHtml(tuples) {
      if (!tuples) return '';
      if (typeof tuples === 'string') return escapeHtml(tuples);
      if (!Array.isArray(tuples)) return '';

      const output = [];

      for (const segment of tuples) {
        if (!segment) continue;
        if (typeof segment === 'string') {
          output.push(escapeHtml(segment));
          continue;
        }
        if (!Array.isArray(segment) || segment.length === 0) continue;

        const rawText = segment[0] != null ? String(segment[0]) : '';
        const decorators = Array.isArray(segment[1]) ? segment[1] : [];

        let hasEquation = false;
        let eqLatex = '';
        for (const dec of decorators) {
          if (Array.isArray(dec) && dec.length > 0 && dec[0] === 'e') {
            hasEquation = true;
            eqLatex = dec[1] != null ? String(dec[1]) : (rawText === '⁍' || rawText === '\u204d' ? '' : rawText);
            break;
          }
        }

        let inner = '';
        if (hasEquation) {
          const escapedFormula = escapeHtml(eqLatex);
          const tokenAttr = (rawText === '⁍' || rawText === '\u204d') ? ' data-token="⁍"' : '';
          inner = `<span class="inline-equation notion-inline-equation inline-katex-node"${tokenAttr} data-latex="${escapedFormula}" contenteditable="false">${escapedFormula}</span>`;
        } else {
          inner = escapeHtml(rawText);
        }

        for (const dec of decorators) {
          if (!Array.isArray(dec) || dec.length === 0) continue;
          const tag = String(dec[0]);
          switch (tag) {
            case 'b':
              inner = `<strong>${inner}</strong>`;
              break;
            case 'i':
              inner = `<em>${inner}</em>`;
              break;
            case '_':
              inner = `<u>${inner}</u>`;
              break;
            case 's':
              inner = `<s>${inner}</s>`;
              break;
            case 'c':
              inner = `<code>${inner}</code>`;
              break;
            case 'h': {
              const colorRaw = dec[1] != null ? String(dec[1]) : 'yellow';
              const cleanColor = colorRaw.replace(/[^a-zA-Z0-9_\-]/g, '');
              let styleAttr = '';
              if (cleanColor.endsWith('_background')) {
                const baseBg = cleanColor.replace('_background', '');
                const bgVal = NOTION_COLOR_HEX_MAP[cleanColor] || baseBg;
                styleAttr = `background-color: ${bgVal};`;
              } else {
                const colorVal = NOTION_COLOR_HEX_MAP[cleanColor] || cleanColor;
                styleAttr = `color: ${colorVal};`;
              }
              inner = `<mark style="${styleAttr}" class="notion-color-${cleanColor}" data-color="${cleanColor}">${inner}</mark>`;
              break;
            }
            case 'a': {
              const safeUrl = sanitizeLinkUrl(dec[1]);
              inner = `<a href="${escapeHtml(safeUrl)}" target="_blank" rel="noopener noreferrer">${inner}</a>`;
              break;
            }
            case 'e':
              break;
          }
        }

        output.push(inner);
      }

      return output.join('');
    }
    window.parseRichTextToHtml = parseRichTextToHtml;

    function htmlToRichTextTuples(nodeOrHtml) {
      if (!nodeOrHtml) return [];

      let root;
      if (typeof nodeOrHtml === 'string') {
        if (typeof document !== 'undefined') {
          root = document.createElement('div');
          root.innerHTML = nodeOrHtml;
        } else {
          return [[nodeOrHtml, []]];
        }
      } else if (nodeOrHtml.nodeType) {
        root = nodeOrHtml;
      } else {
        return [];
      }

      const segments = [];

      function extractColorFromElement(el) {
        if (!el || !el.getAttribute) return null;
        const dataColor = el.getAttribute('data-color');
        if (dataColor) return dataColor.trim();
        const cls = el.className || '';
        if (typeof cls === 'string') {
          for (const c of cls.split(/\s+/)) {
            if (c.startsWith('notion-color-')) {
              return c.substring('notion-color-'.length);
            }
            if (c.startsWith('notion-bg-')) {
              return c.substring('notion-bg-'.length);
            }
          }
        }
        const style = el.getAttribute('style') || '';
        const bgMatch = style.match(/background(?:-color)?\s*:\s*([^;]+)/i);
        if (bgMatch) {
          const c = bgMatch[1].trim().toLowerCase();
          return c.endsWith('_background') ? c : `${c}_background`;
        }
        const colorMatch = style.match(/(?:^|;)\s*color\s*:\s*([^;]+)/i);
        if (colorMatch) {
          return colorMatch[1].trim().toLowerCase();
        }
        return null;
      }

      function areDecoratorsEqual(d1, d2) {
        if (d1.length !== d2.length) return false;
        for (let i = 0; i < d1.length; i++) {
          const a = d1[i];
          const b = d2[i];
          if (a[0] !== b[0]) return false;
          if (a.length > 1 && a[1] !== b[1]) return false;
        }
        return true;
      }

      function traverse(node, currentStyles) {
        if (!node) return;

        if (node.nodeType === 3) {
          const text = node.nodeValue;
          if (!text) return;

          const decs = [];
          if (currentStyles.bold) decs.push(['b']);
          if (currentStyles.italic) decs.push(['i']);
          if (currentStyles.underline) decs.push(['_']);
          if (currentStyles.strike) decs.push(['s']);
          if (currentStyles.code) decs.push(['c']);
          if (currentStyles.color) decs.push(['h', currentStyles.color]);
          if (currentStyles.link) decs.push(['a', currentStyles.link]);
          if (currentStyles.equation) decs.push(['e', currentStyles.equation]);

          if (segments.length > 0) {
            const last = segments[segments.length - 1];
            const lastDecs = last[1] || [];
            if (areDecoratorsEqual(lastDecs, decs)) {
              last[0] += text;
              return;
            }
          }

          segments.push(decs.length > 0 ? [text, decs] : [text, []]);
          return;
        }

        if (node.nodeType === 1) {
          const tag = (node.tagName || '').toLowerCase();

          if (node.classList && (node.classList.contains('inline-equation') ||
                                 node.classList.contains('notion-inline-equation') ||
                                 node.classList.contains('inline-katex-node') ||
                                 node.hasAttribute('data-latex'))) {
            const formula = node.getAttribute('data-latex') || node.textContent || '';
            const isCanonicalToken = (node.getAttribute && (node.getAttribute('data-token') === '⁍' || node.getAttribute('data-token') === '\u204d'));
            const segText = isCanonicalToken ? '⁍' : formula;
            const decs = [];
            if (currentStyles.bold) decs.push(['b']);
            if (currentStyles.italic) decs.push(['i']);
            if (currentStyles.underline) decs.push(['_']);
            if (currentStyles.strike) decs.push(['s']);
            if (currentStyles.code) decs.push(['c']);
            if (currentStyles.color) decs.push(['h', currentStyles.color]);
            if (currentStyles.link) decs.push(['a', currentStyles.link]);
            decs.push(['e', formula]);
            segments.push([segText, decs]);
            return;
          }

          const nextStyles = { ...currentStyles };

          if (tag === 'strong' || tag === 'b') nextStyles.bold = true;
          if (tag === 'em' || tag === 'i') nextStyles.italic = true;
          if (tag === 'u') nextStyles.underline = true;
          if (tag === 's' || tag === 'del' || tag === 'strike') nextStyles.strike = true;
          if (tag === 'code') nextStyles.code = true;
          if (tag === 'a') nextStyles.link = node.getAttribute('href') || '#';

          if (tag === 'mark') {
            const color = extractColorFromElement(node) || 'yellow_background';
            nextStyles.color = color;
          } else if (tag === 'span') {
            const color = extractColorFromElement(node);
            if (color) nextStyles.color = color;
          }

          if (node.style) {
            const fw = node.style.fontWeight;
            if (fw === 'bold' || fw === 'bolder' || Number(fw) >= 600) nextStyles.bold = true;
            if (node.style.fontStyle === 'italic') nextStyles.italic = true;
            const td = node.style.textDecoration || '';
            if (td.includes('underline')) nextStyles.underline = true;
            if (td.includes('line-through')) nextStyles.strike = true;
          }

          if (tag === 'br') {
            if (segments.length > 0) {
              segments[segments.length - 1][0] += '\n';
            } else {
              segments.push(['\n', []]);
            }
            return;
          }

          for (let child = node.firstChild; child; child = child.nextSibling) {
            traverse(child, nextStyles);
          }
        }
      }

      traverse(root, {
        bold: false,
        italic: false,
        underline: false,
        strike: false,
        code: false,
        color: null,
        link: null,
        equation: null
      });

      return segments;
    }
    window.htmlToRichTextTuples = htmlToRichTextTuples;

    function getBlockPropertyPlainText(block, propName = 'title') {
      if (!block || !block.properties) {
        if (block && block[propName] != null) return String(block[propName]);
        return '';
      }
      const prop = block.properties[propName];
      if (prop == null) {
        if (block[propName] != null) return String(block[propName]);
        if (propName === 'title') {
          if (block.properties.text != null) return String(block.properties.text);
          if (block.properties.html != null) return String(block.properties.html).replace(/<[^>]+>/g, '');
        }
        return '';
      }
      if (Array.isArray(prop)) {
        return prop.map(seg => {
          if (!seg) return '';
          if (Array.isArray(seg)) {
            const raw = seg[0] != null ? String(seg[0]) : '';
            if (raw === '⁍' || raw === '\u204d') {
              const decs = Array.isArray(seg[1]) ? seg[1] : [];
              for (const d of decs) {
                if (Array.isArray(d) && d[0] === 'e' && d[1]) return String(d[1]);
              }
            }
            return raw;
          }
          return String(seg);
        }).join('');
      }
      return String(prop);
    }

    function buildEquationCrdt(latex, version = 1, clientId = 'user_local') {
      const cId = clientId || 'user_local';
      const v = Number(version) || 1;
      const str = String(latex || '');
      const rangeKey = `${cId},"start","end"`;
      return {
        title: {
          r: rangeKey,
          n: {
            [rangeKey]: {
              s: {
                x: cId,
                i: [
                  { t: 's' },
                  {
                    t: 't',
                    i: [cId, v],
                    o: 'start',
                    l: str.length,
                    c: str
                  },
                  { t: 'e' }
                ],
                l: ''
              },
              c: []
            }
          }
        }
      };
    }
    window.buildEquationCrdt = buildEquationCrdt;

    function getBlockPropertyHtml(block, propName = 'title') {
      if (!block || !block.properties) {
        if (block && block[propName] != null) return escapeHtml(String(block[propName]));
        return '';
      }
      const prop = block.properties[propName];
      if (prop == null) {
        if (block[propName] != null) return escapeHtml(String(block[propName]));
        if (propName === 'title') {
          if (block.properties.html != null) return String(block.properties.html);
          if (block.properties.text != null) return escapeHtml(String(block.properties.text));
        }
        return '';
      }
      if (Array.isArray(prop)) {
        return parseRichTextToHtml(prop);
      }
      if (typeof prop === 'string') {
        return escapeHtml(prop);
      }
      return '';
    }

    let blockSaveDebounceTimer = null;
    const pendingBlockUpdates = new Map();

    function persistBlockUpdate(blockId, updates) {
      if (!blockId || !updates) return;
      const existing = pendingBlockUpdates.get(blockId) || {};
      pendingBlockUpdates.set(blockId, { ...existing, ...updates });

      clearTimeout(blockSaveDebounceTimer);
      blockSaveDebounceTimer = setTimeout(() => {
        flushPendingBlockUpdates();
      }, 300);
    }

    function flushPendingBlockUpdates() {
      if (pendingBlockUpdates.size === 0) return;
      const entries = Array.from(pendingBlockUpdates.entries());
      pendingBlockUpdates.clear();

      for (const [blockId, updates] of entries) {
        if (hasPyWebViewBridge() && typeof window.pywebview.api.update_block === 'function') {
          try {
            window.pywebview.api.update_block(blockId, updates);
          } catch (err) {
            fallbackFetchUpdateBlock(blockId, updates);
          }
        } else {
          fallbackFetchUpdateBlock(blockId, updates);
        }
      }
    }
    if (typeof window !== 'undefined') {
      window.persistBlockUpdate = persistBlockUpdate;
    }

    function fallbackFetchUpdateBlock(blockId, updates) {
      fetch(`/api/blocks/${encodeURIComponent(blockId)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      }).catch(() => {});
    }

    function syncRecordMapChildrenOrder(container) {
      if (!container) return;
      const parentBlockEl = container.closest('[data-block-id]');
      const activeNote = typeof getActiveNote === 'function' ? getActiveNote() : null;
      const parentId = parentBlockEl ? parentBlockEl.getAttribute('data-block-id') : (activeNote ? String(activeNote.id) : null);
      if (!parentId) return;

      const childIds = Array.from(container.children)
        .map(c => c.getAttribute('data-block-id'))
        .filter(Boolean);

      if (typeof state !== 'undefined' && state.activeRecordMap && state.activeRecordMap.block[parentId]) {
        state.activeRecordMap.block[parentId].value.content = childIds;
        childIds.forEach(cid => {
          if (state.activeRecordMap.block[cid]) {
            state.activeRecordMap.block[cid].value.parent_id = parentId;
          }
        });
      }

      if (hasPyWebViewBridge() && typeof window.pywebview.api.reorder_block_children === 'function') {
        try {
          window.pywebview.api.reorder_block_children(parentId, childIds);
        } catch (_) {}
      } else {
        fetch(`/api/blocks/${encodeURIComponent(parentId)}/reorder`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: childIds })
        }).catch(() => {});
      }
    }

    function insertBlockBelow(blockEl, blockType = 'text') {
      const newId = 'blk-' + (typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).substring(2, 10));
      const activeNote = typeof getActiveNote === 'function' ? getActiveNote() : null;
      const newBlock = {
        id: newId,
        type: blockType,
        properties: { title: [['', []]] },
        content: [],
        alive: 1,
        parent_id: blockEl.getAttribute('data-parent-id') || (activeNote ? String(activeNote.id) : null),
        parent_table: 'block'
      };

      const newEl = renderBlock(newBlock);
      if (!newEl) return;

      blockEl.after(newEl);
      if (typeof state !== 'undefined' && state.activeRecordMap) {
        state.activeRecordMap.block[newId] = { value: newBlock, role: 'editor' };
        const parentId = newBlock.parent_id;
        if (parentId && state.activeRecordMap.block[parentId]) {
          const parentBlock = state.activeRecordMap.block[parentId].value;
          if (!Array.isArray(parentBlock.content)) parentBlock.content = [];
          const currentIdx = parentBlock.content.indexOf(blockEl.getAttribute('data-block-id'));
          if (currentIdx !== -1) {
            parentBlock.content.splice(currentIdx + 1, 0, newId);
          } else {
            parentBlock.content.push(newId);
          }
          if (hasPyWebViewBridge() && typeof window.pywebview.api.reorder_block_children === 'function') {
            try { window.pywebview.api.reorder_block_children(parentId, parentBlock.content); } catch (_) {}
          } else {
            fetch(`/api/blocks/${encodeURIComponent(parentId)}/reorder`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ content: parentBlock.content })
            }).catch(() => {});
          }
        }
      }

      if (hasPyWebViewBridge() && typeof window.pywebview.api.create_block === 'function') {
        try { window.pywebview.api.create_block(newBlock); } catch (_) {}
      } else {
        fetch('/api/blocks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newBlock)
        }).catch(() => {});
      }

      const editable = newEl.querySelector('[contenteditable="true"]') || newEl;
      if (editable && typeof editable.focus === 'function') editable.focus();
      syncRichEditor();
    }

    function deleteBlockElement(blockEl, focusTargetEl) {
      const blockId = blockEl.getAttribute('data-block-id');
      if (typeof state !== 'undefined' && state.activeRecordMap && state.activeRecordMap.block[blockId]) {
        state.activeRecordMap.block[blockId].value.alive = 0;
        const parentId = state.activeRecordMap.block[blockId].value.parent_id;
        if (parentId && state.activeRecordMap.block[parentId]) {
          const p = state.activeRecordMap.block[parentId].value;
          if (Array.isArray(p.content)) {
            p.content = p.content.filter(id => id !== blockId);
          }
        }
      }

      if (hasPyWebViewBridge() && typeof window.pywebview.api.soft_delete_block === 'function') {
        try { window.pywebview.api.soft_delete_block(blockId); } catch (_) {}
      } else {
        fetch(`/api/blocks/${encodeURIComponent(blockId)}`, {
          method: 'DELETE'
        }).catch(() => {});
      }

      blockEl.remove();
      if (focusTargetEl) {
        const editable = focusTargetEl.querySelector('[contenteditable="true"]') || focusTargetEl;
        if (editable && typeof editable.focus === 'function') {
          editable.focus();
          const sel = window.getSelection();
          if (sel) {
            const range = document.createRange();
            range.selectNodeContents(editable);
            range.collapse(false);
            sel.removeAllRanges();
            sel.addRange(range);
          }
        }
      }
      syncRichEditor();
    }

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

      const typeMap = {
        'turn-h4': 'header_4',
        'turn-quote': 'quote',
        'turn-callout': 'callout',
        'turn-todo': 'to_do',
        'turn-p': 'text',
        'turn-h1': 'header',
        'turn-h2': 'sub_header',
        'turn-h3': 'sub_sub_header',
        'turn-bullet': 'bulleted_list',
        'turn-num': 'numbered_list',
        'turn-toggle': 'toggle',
        'h4': 'header_4',
        'todo': 'to_do',
        'quote': 'quote',
        'callout': 'callout',
        'synced': 'transclusion_container'
      };
      const canonicalType = typeMap[newType] || newType;

      const activeNote = typeof getActiveNote === 'function' ? getActiveNote() : null;
      let blockData = (typeof state !== 'undefined' && state.activeRecordMap && state.activeRecordMap.block[blockId]?.value) || null;
      if (!blockData) {
        blockData = {
          id: blockId,
          type: canonicalType,
          properties: { title: htmlToRichTextTuples(blockEl) },
          content: [],
          alive: 1,
          parent_id: blockEl.getAttribute('data-parent-id') || (activeNote ? String(activeNote.id) : null),
          parent_table: 'block'
        };
      } else {
        blockData.type = canonicalType;
      }

      const isLeaf = ['equation', 'divider', 'code', 'image', 'video', 'audio', 'file', 'pdf', 'bookmark', 'table_row', 'transclusion_reference', 'sub_page'].includes(canonicalType);
      if (isLeaf && !(blockData.format && blockData.format.toggleable)) {
        blockData.content = null;
      } else if (!Array.isArray(blockData.content)) {
        blockData.content = [];
      }

      const newEl = renderBlock(blockData);
      if (!newEl) return;

      blockEl.replaceWith(newEl);
      persistBlockUpdate(blockId, { type: canonicalType });

      const editable = newEl.querySelector('[contenteditable="true"]') || newEl;
      if (editable && typeof editable.focus === 'function') editable.focus();
      if (typeof attachSubpageBlockListeners === 'function') attachSubpageBlockListeners();
      if (typeof refreshPageTableOfContents === 'function') refreshPageTableOfContents();
      syncRichEditor();
    }
    window.convertBlockType = convertBlockType;

    function renderBlock(block) {
      if (!block || !block.type) return null;
      switch (block.type) {
        case 'sub_page': {
          const div = document.createElement('div');
          div.className = 'block-subpage';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'sub_page');
          const pageId = block.page_id || (block.properties && (block.properties.page_id || block.properties.pageId)) || '';
          const title = block.title || (block.properties && block.properties.title) || 'Sin título';
          div.setAttribute('data-page-id', String(pageId));
          div.setAttribute('data-title', title);
          div.setAttribute('contenteditable', 'false');
          div.style.cursor = 'pointer';
          div.innerHTML = `<span class="subpage-icon">📄</span><span class="subpage-title">${title}</span>`;
          div.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            loadNote(pageId);
          };
          return div;
        }
        case 'page': {
          const div = document.createElement('div');
          div.className = 'block-subpage notion-block';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'page');
          const pageId = block.id || block.page_id || '';
          const title = (block.properties && getBlockPropertyPlainText(block, 'title')) || block.title || 'Sin título';
          div.setAttribute('data-page-id', String(pageId));
          div.setAttribute('data-title', title);
          div.setAttribute('contenteditable', 'false');
          div.style.cursor = 'pointer';
          div.innerHTML = `<span class="subpage-icon">📄</span><span class="subpage-title">${escapeHtml(title)}</span>`;
          div.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            loadNote(pageId);
          };
          return div;
        }
        case 'column_list': {
          const div = document.createElement('div');
          div.className = 'notion-block block-column-list notion-columns-row';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'column_list');
          return div;
        }
        case 'column': {
          const div = document.createElement('div');
          div.className = 'notion-block block-column notion-column-slot';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'column');
          const ratio = (block.format && typeof block.format.column_ratio === 'number') ? block.format.column_ratio : 0.5;
          div.style.flex = `${ratio} 1 0%`;
          div.style.minWidth = '60px';
          div.innerHTML = `<div class="notion-column-content block-column-content notion-block-children"></div>`;
          return div;
        }
        case 'divider': {
          const div = document.createElement('div');
          div.className = 'notion-block block-divider notion-divider-block';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'divider');
          div.setAttribute('contenteditable', 'false');
          div.innerHTML = `<hr class="notion-hr" />`;
          return div;
        }
        case 'text': {
          const div = document.createElement('div');
          div.className = 'notion-block block-text notion-block-text';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'text');
          const htmlContent = getBlockPropertyHtml(block, 'title');
          div.innerHTML = `<div class="notion-block-content" contenteditable="true" data-property="title">${htmlContent}</div><div class="notion-block-children"></div>`;
          return div;
        }
        case 'header': {
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          const htmlContent = getBlockPropertyHtml(block, 'title');
          if (block.format && block.format.toggleable) {
            const details = document.createElement('details');
            details.className = 'notion-block block-header block-header-toggle notion-block-toggle';
            details.id = id;
            details.setAttribute('data-block-id', id);
            details.setAttribute('data-type', 'header');
            details.setAttribute('data-toggleable', 'true');
            details.innerHTML = `<summary class="notion-toggle-summary block-header-toggle-summary"><span class="notion-toggle-arrow">▶</span><h1 class="notion-toggle-title block-header-toggle-title" contenteditable="true" data-property="title">${htmlContent}</h1></summary><div class="notion-toggle-content block-toggle-content notion-block-children"></div>`;
            return details;
          }
          const h = document.createElement('h1');
          h.className = 'notion-block block-header notion-block-header';
          h.id = id;
          h.setAttribute('data-block-id', id);
          h.setAttribute('data-type', 'header');
          h.setAttribute('contenteditable', 'true');
          h.setAttribute('data-property', 'title');
          h.innerHTML = htmlContent;
          return h;
        }
        case 'sub_header': {
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          const htmlContent = getBlockPropertyHtml(block, 'title');
          if (block.format && block.format.toggleable) {
            const details = document.createElement('details');
            details.className = 'notion-block block-sub-header block-header-toggle notion-block-toggle';
            details.id = id;
            details.setAttribute('data-block-id', id);
            details.setAttribute('data-type', 'sub_header');
            details.setAttribute('data-toggleable', 'true');
            details.innerHTML = `<summary class="notion-toggle-summary block-header-toggle-summary"><span class="notion-toggle-arrow">▶</span><h2 class="notion-toggle-title block-header-toggle-title" contenteditable="true" data-property="title">${htmlContent}</h2></summary><div class="notion-toggle-content block-toggle-content notion-block-children"></div>`;
            return details;
          }
          const h = document.createElement('h2');
          h.className = 'notion-block block-sub-header notion-block-sub-header';
          h.id = id;
          h.setAttribute('data-block-id', id);
          h.setAttribute('data-type', 'sub_header');
          h.setAttribute('contenteditable', 'true');
          h.setAttribute('data-property', 'title');
          h.innerHTML = htmlContent;
          return h;
        }
        case 'sub_sub_header': {
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          const htmlContent = getBlockPropertyHtml(block, 'title');
          if (block.format && block.format.toggleable) {
            const details = document.createElement('details');
            details.className = 'notion-block block-sub-sub-header block-header-toggle notion-block-toggle';
            details.id = id;
            details.setAttribute('data-block-id', id);
            details.setAttribute('data-type', 'sub_sub_header');
            details.setAttribute('data-toggleable', 'true');
            details.innerHTML = `<summary class="notion-toggle-summary block-header-toggle-summary"><span class="notion-toggle-arrow">▶</span><h3 class="notion-toggle-title block-header-toggle-title" contenteditable="true" data-property="title">${htmlContent}</h3></summary><div class="notion-toggle-content block-toggle-content notion-block-children"></div>`;
            return details;
          }
          const h = document.createElement('h3');
          h.className = 'notion-block block-sub-sub-header notion-block-sub-sub-header';
          h.id = id;
          h.setAttribute('data-block-id', id);
          h.setAttribute('data-type', 'sub_sub_header');
          h.setAttribute('contenteditable', 'true');
          h.setAttribute('data-property', 'title');
          h.innerHTML = htmlContent;
          return h;
        }
        case 'header_4': {
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          const htmlContent = getBlockPropertyHtml(block, 'title');
          if (block.format && block.format.toggleable) {
            const details = document.createElement('details');
            details.className = 'notion-block block-header-4 block-header-toggle notion-block-toggle';
            details.id = id;
            details.setAttribute('data-block-id', id);
            details.setAttribute('data-type', 'header_4');
            details.setAttribute('data-toggleable', 'true');
            details.innerHTML = `<summary class="notion-toggle-summary block-header-toggle-summary"><span class="notion-toggle-arrow">▶</span><h4 class="notion-toggle-title block-header-4-title" contenteditable="true" data-property="title">${htmlContent}</h4></summary><div class="notion-toggle-content block-toggle-content notion-block-children"></div>`;
            return details;
          }
          const h = document.createElement('h4');
          h.className = 'notion-block block-header-4 notion-block-header-4';
          h.id = id;
          h.setAttribute('data-block-id', id);
          h.setAttribute('data-type', 'header_4');
          h.setAttribute('contenteditable', 'true');
          h.setAttribute('data-property', 'title');
          h.innerHTML = htmlContent;
          return h;
        }
        case 'bulleted_list': {
          const div = document.createElement('div');
          div.className = 'notion-block block-bulleted-list notion-block-bulleted-list';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'bulleted_list');
          const htmlContent = getBlockPropertyHtml(block, 'title');
          div.innerHTML = `<span class="notion-bullet" contenteditable="false">•</span><div class="notion-block-content" contenteditable="true" data-property="title">${htmlContent}</div><div class="notion-block-children"></div>`;
          return div;
        }
        case 'numbered_list': {
          const div = document.createElement('div');
          div.className = 'notion-block block-numbered-list notion-block-numbered-list';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'numbered_list');
          const htmlContent = getBlockPropertyHtml(block, 'title');
          div.innerHTML = `<span class="notion-number-prefix" contenteditable="false">1.</span><div class="notion-block-content" contenteditable="true" data-property="title">${htmlContent}</div><div class="notion-block-children"></div>`;
          return div;
        }
        case 'toggle': {
          const details = document.createElement('details');
          details.className = 'notion-block block-toggle notion-block-toggle';
          details.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          details.setAttribute('data-block-id', details.id);
          details.setAttribute('data-type', 'toggle');
          const htmlContent = getBlockPropertyHtml(block, 'title');
          details.innerHTML = `<summary class="notion-toggle-summary block-toggle-summary"><span class="notion-toggle-arrow">▶</span><div class="notion-toggle-title" contenteditable="true" data-property="title">${htmlContent}</div></summary><div class="notion-toggle-content block-toggle-content notion-block-children"></div>`;
          return details;
        }
        case 'to_do': {
          const div = document.createElement('div');
          div.className = 'notion-block block-to-do notion-block-to-do';
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.id = id;
          div.setAttribute('data-block-id', id);
          div.setAttribute('data-type', 'to_do');
          const htmlContent = getBlockPropertyHtml(block, 'title');
          let isChecked = false;
          if (block.properties && block.properties.checked) {
            const chkProp = block.properties.checked;
            if (Array.isArray(chkProp) && chkProp[0]) {
              const firstVal = Array.isArray(chkProp[0]) ? chkProp[0][0] : chkProp[0];
              isChecked = (firstVal === 'Yes' || firstVal === true);
            } else if (chkProp === true || chkProp === 'Yes') {
              isChecked = true;
            }
          }
          div.innerHTML = `<div class="notion-to-do-row"><input type="checkbox" class="notion-to-do-checkbox" ${isChecked ? 'checked' : ''} contenteditable="false" /><div class="notion-to-do-title notion-block-content ${isChecked ? 'completed' : ''}" contenteditable="true" data-property="title">${htmlContent}</div></div><div class="block-to-do-children notion-block-children"></div>`;
          const chk = div.querySelector('.notion-to-do-checkbox');
          const titleEl = div.querySelector('.notion-to-do-title');
          if (chk) {
            chk.onchange = function(e) {
              const checked = Boolean(chk.checked !== undefined ? chk.checked : chk.hasAttribute('checked'));
              if (titleEl) {
                if (checked) {
                  titleEl.classList.add('completed');
                } else {
                  titleEl.classList.remove('completed');
                }
              }
              const val = checked ? 'Yes' : 'No';
              if (typeof state !== 'undefined' && state.activeRecordMap && state.activeRecordMap.block && state.activeRecordMap.block[id]) {
                const blk = state.activeRecordMap.block[id].value;
                if (blk) {
                  blk.properties = blk.properties || {};
                  blk.properties.checked = [[val, []]];
                }
              }
              if (typeof window !== 'undefined' && window.state && window.state.activeRecordMap && window.state.activeRecordMap.block && window.state.activeRecordMap.block[id]) {
                const blk = window.state.activeRecordMap.block[id].value;
                if (blk) {
                  blk.properties = blk.properties || {};
                  blk.properties.checked = [[val, []]];
                }
              }
              const updater = (typeof window !== 'undefined' && typeof window.persistBlockUpdate === 'function')
                ? window.persistBlockUpdate
                : (typeof persistBlockUpdate === 'function' ? persistBlockUpdate : null);
              if (typeof updater === 'function') {
                updater(id, { properties: { checked: [[val, []]] } });
              }
              if (typeof syncRichEditor === 'function') {
                syncRichEditor();
              }
            };
          }
          return div;
        }
        case 'quote': {
          const bq = document.createElement('blockquote');
          bq.className = 'notion-block block-quote notion-block-quote';
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          bq.id = id;
          bq.setAttribute('data-block-id', id);
          bq.setAttribute('data-type', 'quote');
          const htmlContent = getBlockPropertyHtml(block, 'title');
          bq.innerHTML = `<div class="notion-quote-content notion-block-content" contenteditable="true" data-property="title">${htmlContent}</div><div class="block-quote-children notion-block-children"></div>`;
          return bq;
        }
        case 'callout': {
          const div = document.createElement('div');
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          const bg = (block.format && block.format.block_color) || '';
          div.className = `notion-block block-callout notion-block-callout${bg ? ' notion-color-' + bg : ''}`;
          div.id = id;
          div.setAttribute('data-block-id', id);
          div.setAttribute('data-type', 'callout');
          const icon = (block.format && block.format.page_icon) || '💡';
          const htmlContent = getBlockPropertyHtml(block, 'title');
          div.innerHTML = `<div class="notion-callout-inner"><span class="notion-callout-icon" contenteditable="false">${escapeHtml(icon)}</span><div class="notion-callout-body notion-block-content" contenteditable="true" data-property="title">${htmlContent}</div></div><div class="block-callout-children notion-block-children"></div>`;
          return div;
        }
        case 'code': {
          const div = document.createElement('div');
          div.className = 'notion-block block-code notion-block-code';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'code');
          const rawCode = getBlockPropertyPlainText(block, 'title');
          const lang = getBlockPropertyPlainText(block, 'language') || 'python';
          div.innerHTML = `<div class="notion-code-header" contenteditable="false"><select class="notion-code-lang-select block-code-lang-select" data-block-id="${div.id}"><option value="javascript">JavaScript</option><option value="python">Python</option><option value="html">HTML</option><option value="css">CSS</option><option value="sql">SQL</option><option value="markdown">Markdown</option><option value="json">JSON</option><option value="typescript">TypeScript</option><option value="bash">Bash</option><option value="c">C / C++</option></select><button class="notion-code-copy-btn btn-secondary">Copiar</button></div><pre><code class="notion-code-body block-code-body" contenteditable="plaintext-only" spellcheck="false" data-property="title">${escapeHtml(rawCode)}</code></pre>`;
          const sel = div.querySelector('select');
          if (sel) sel.value = lang.toLowerCase();
          const copyBtn = div.querySelector('.notion-code-copy-btn');
          if (copyBtn) {
            copyBtn.onclick = (e) => {
              e.stopPropagation();
              const codeBody = div.querySelector('code');
              if (codeBody) {
                if (typeof navigator !== 'undefined' && navigator.clipboard) {
                  navigator.clipboard.writeText(codeBody.textContent).then(() => {
                    if (typeof showToast === 'function') showToast('Código copiado', '📋');
                  }).catch(() => {});
                }
              }
            };
          }
          return div;
        }
        case 'equation': {
          const div = document.createElement('div');
          div.className = 'notion-block block-equation notion-block-equation';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'equation');
          const latex = getBlockPropertyPlainText(block, 'title') || 'E = mc^2';

          div.innerHTML = `
            <div class="notion-equation-header-bar" contenteditable="false">
              <span style="font-weight:700; display:flex; align-items:center; gap:6px;">
                <span style="color:var(--accent-amber, #f59e0b); font-family:'JetBrains Mono', monospace; font-weight:800;">∑</span>
                <span>Ecuación Matemática (LaTeX)</span>
              </span>
              <div class="notion-equation-actions" style="display:flex; gap:6px;">
                <button type="button" class="btn-copy-latex" title="Copiar código LaTeX" style="padding:2px 8px; font-size:11px; background:transparent; border:1px solid var(--border-hairline, rgba(255,255,255,0.15)); border-radius:4px; color:var(--text-secondary, #9ca3af); cursor:pointer;">Copiar LaTeX</button>
                <button type="button" class="btn-toggle-edit" title="Editar fórmula" style="padding:2px 8px; font-size:11px; background:transparent; border:1px solid var(--border-hairline, rgba(255,255,255,0.15)); border-radius:4px; color:var(--text-secondary, #9ca3af); cursor:pointer;">Editar</button>
              </div>
            </div>
            <div class="notion-equation-display block-equation-display" contenteditable="false" data-latex="${escapeHtml(latex)}" title="Haz clic para editar la fórmula LaTeX">${escapeHtml(latex)}</div>
            <div class="notion-equation-popover block-equation-popover" style="display:none;" contenteditable="false">
              <textarea class="notion-equation-input notion-equation-textarea search-box tabular-nums" rows="3" data-block-id="${div.id}" placeholder="Fórmula LaTeX (ej. \\begin{cases} 2x+3y=10 \\\\ 4x-5y=-3 \\end{cases})">${escapeHtml(latex)}</textarea>
              <div class="notion-equation-snippets-row">
                <button type="button" class="math-chip-btn" data-snip="\\\\begin{cases} 2x + 3y = 10 \\\\\\\\ 4x - 5y = -3 \\\\end{cases}">Sistema</button>
                <button type="button" class="math-chip-btn" data-snip="\\\\begin{bmatrix} 1 & 0 \\\\\\\\ 0 & 1 \\\\end{bmatrix}">Matriz</button>
                <button type="button" class="math-chip-btn" data-snip="A^{-1} = \\\\frac{1}{|A|} \\\\cdot \\\\text{adj}(A)">Inversa</button>
                <button type="button" class="math-chip-btn" data-snip="\\\\vec{x} \\\\cdot \\\\vec{y} = \\\\|\\\\vec{x}\\\\| \\\\|\\\\vec{y}\\\\| \\\\cos(\\\\theta)">Vectores</button>
                <button type="button" class="math-chip-btn" data-snip="\\\\mathbb{R}^n = \\\\{ (x_1, \\\\dots, x_n) : x_i \\\\in \\\\mathbb{R} \\\\}">Conjuntos</button>
                <button type="button" class="math-chip-btn" data-snip="\\\\lim_{x \\\\to 0} \\\\frac{\\\\sin x}{x} = 1">Límite</button>
              </div>
              <div class="notion-equation-live-preview"></div>
              <div class="notion-equation-actions-row">
                <button type="button" class="btn-secondary btn-convert-inline" style="padding:3px 8px; font-size:11px;">Convertir a en línea</button>
                <div style="display:flex; gap:6px;">
                  <button type="button" class="btn-secondary btn-cancel-edit" style="padding:3px 8px; font-size:11px;">Cerrar</button>
                  <button type="button" class="btn-primary btn-save-equation" style="padding:3px 12px; font-size:11px;">Listo / Guardar (Ctrl+Enter)</button>
                </div>
              </div>
            </div>
          `;

          const disp = div.querySelector('.notion-equation-display');
          const pop = div.querySelector('.notion-equation-popover');
          const inp = div.querySelector('.notion-equation-input');
          const preview = div.querySelector('.notion-equation-live-preview');
          const btnCopy = div.querySelector('.btn-copy-latex');
          const btnToggle = div.querySelector('.btn-toggle-edit');
          const btnSave = div.querySelector('.btn-save-equation');
          const btnCancel = div.querySelector('.btn-cancel-edit');
          const btnConvert = div.querySelector('.btn-convert-inline');

          function renderDispMath(code) {
            const targetLatex = code != null ? String(code) : '';
            if (disp) {
              disp.setAttribute('data-latex', targetLatex);
              if (typeof window !== 'undefined' && window.katex) {
                try {
                  window.katex.render(targetLatex, disp, { displayMode: true, throwOnError: false });
                } catch (_) {
                  disp.textContent = targetLatex;
                }
              } else {
                disp.textContent = targetLatex;
              }
            }
          }

          function renderPreviewMath(code) {
            if (!preview) return;
            const targetLatex = code != null ? String(code) : '';
            if (typeof window !== 'undefined' && window.katex) {
              try {
                window.katex.render(targetLatex, preview, { displayMode: true, throwOnError: false });
              } catch (_) {
                preview.textContent = targetLatex;
              }
            } else {
              preview.textContent = targetLatex;
            }
          }

          function openEditor() {
            if (pop) {
              pop.style.display = 'block';
              if (inp) inp.focus();
              renderPreviewMath(inp ? inp.value : '');
            }
          }

          function closeEditor() {
            if (pop) pop.style.display = 'none';
          }

          function saveEquationVal() {
            if (!inp) return;
            const val = inp.value;
            renderDispMath(val);
            const crdtPayload = typeof buildEquationCrdt === 'function' ? buildEquationCrdt(val, (block.version || 1) + 1) : {};
            persistBlockUpdate(div.id, {
              properties: { title: [[val, []]] },
              crdt_data: crdtPayload,
              version: (block.version || 1) + 1
            });
            closeEditor();
            if (typeof showToast === 'function') showToast('Ecuación guardada', '∑');
          }

          if (disp && pop && inp) {
            disp.onclick = (e) => {
              e.stopPropagation();
              if (pop.style.display === 'none') openEditor();
              else closeEditor();
            };

            if (btnToggle) {
              btnToggle.onclick = (e) => {
                e.stopPropagation();
                if (pop.style.display === 'none') openEditor();
                else closeEditor();
              };
            }

            if (btnCopy) {
              btnCopy.onclick = (e) => {
                e.stopPropagation();
                const textToCopy = inp.value || (disp.getAttribute ? disp.getAttribute('data-latex') : '') || '';
                if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
                  navigator.clipboard.writeText(textToCopy);
                }
                if (typeof showToast === 'function') showToast('LaTeX copiado al portapapeles', '📋');
              };
            }

            if (btnCancel) {
              btnCancel.onclick = (e) => {
                e.stopPropagation();
                closeEditor();
              };
            }

            if (btnSave) {
              btnSave.onclick = (e) => {
                e.stopPropagation();
                saveEquationVal();
              };
            }

            if (btnConvert) {
              btnConvert.onclick = (e) => {
                e.stopPropagation();
                const formula = inp.value || (disp.getAttribute ? disp.getAttribute('data-latex') : '') || '';
                persistBlockUpdate(div.id, {
                  type: 'text',
                  properties: { title: [['⁍', [['e', formula]]]] },
                  crdt_data: typeof buildEquationCrdt === 'function' ? buildEquationCrdt(formula, (block.version || 1) + 1) : {}
                });
                if (typeof loadActiveNoteBlocks === 'function') loadActiveNoteBlocks();
                if (typeof showToast === 'function') showToast('Convertido a ecuación en línea', '√x');
              };
            }

            const chips = pop.querySelectorAll ? pop.querySelectorAll('.math-chip-btn') : [];
            if (chips && chips.forEach) {
              chips.forEach(chip => {
                chip.onclick = (e) => {
                  e.stopPropagation();
                  const snip = chip.getAttribute('data-snip');
                  if (!snip) return;
                  const start = inp.selectionStart || 0;
                  const end = inp.selectionEnd || 0;
                  const cur = inp.value || '';
                  inp.value = cur.slice(0, start) + snip + cur.slice(end);
                  inp.focus();
                  inp.setSelectionRange(start + snip.length, start + snip.length);
                  renderPreviewMath(inp.value);
                };
              });
            }

            inp.oninput = () => {
              const val = inp.value;
              renderDispMath(val);
              renderPreviewMath(val);
              const crdtPayload = typeof buildEquationCrdt === 'function' ? buildEquationCrdt(val, (block.version || 1) + 1) : {};
              persistBlockUpdate(div.id, {
                properties: { title: [[val, []]] },
                crdt_data: crdtPayload,
                version: (block.version || 1) + 1
              });
            };

            inp.onkeydown = (e) => {
              if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                saveEquationVal();
              } else if (e.key === 'Escape') {
                e.preventDefault();
                closeEditor();
              }
            };

            renderDispMath(latex);
          }
          return div;
        }
        case 'table': {
          const div = document.createElement('div');
          div.className = 'notion-block block-table notion-block-table-wrapper';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'table');
          div.innerHTML = `<div class="notion-table-scroll"><table class="notion-simple-table"><tbody class="notion-table-body block-table-body"></tbody></table></div>`;
          return div;
        }
        case 'table_row': {
          const tr = document.createElement('tr');
          tr.className = 'notion-block block-table-row notion-table-row';
          tr.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          tr.setAttribute('data-block-id', tr.id);
          tr.setAttribute('data-type', 'table_row');
          let colOrder = [];
          if (block.format && Array.isArray(block.format.table_block_column_order)) {
            colOrder = block.format.table_block_column_order;
          } else if (typeof state !== 'undefined' && state.activeRecordMap && block.parent_id && state.activeRecordMap.block[block.parent_id]) {
            const pFormat = state.activeRecordMap.block[block.parent_id].value?.format;
            if (pFormat && Array.isArray(pFormat.table_block_column_order)) {
              colOrder = pFormat.table_block_column_order;
            }
          }
          if (colOrder.length === 0 && block.properties && typeof block.properties === 'object') {
            colOrder = Object.keys(block.properties);
          }
          if (colOrder.length === 0) colOrder = ['col_1', 'col_2'];
          colOrder.forEach(colId => {
            const td = document.createElement('td');
            td.className = 'block-table-cell notion-table-cell';
            td.setAttribute('contenteditable', 'true');
            td.setAttribute('data-col-id', colId);
            td.setAttribute('data-property', colId);
            td.innerHTML = getBlockPropertyHtml(block, colId);
            tr.appendChild(td);
          });
          return tr;
        }
        case 'collection_view': {
          const div = document.createElement('div');
          div.className = 'notion-block block-collection-view';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'collection_view');
          const title = getBlockPropertyPlainText(block, 'title') || 'Vista de Colección';
          div.innerHTML = `<div class="collection-view-header" contenteditable="false"><span class="collection-view-icon">📊</span><span class="collection-view-title" contenteditable="true" data-property="title">${escapeHtml(title)}</span></div><div class="collection-view-body notion-block-children"></div>`;
          return div;
        }
        case 'collection_view_page': {
          const div = document.createElement('div');
          div.className = 'notion-block block-collection-view-page';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'collection_view_page');
          const title = getBlockPropertyPlainText(block, 'title') || 'Base de Datos de Página';
          div.innerHTML = `<div class="collection-view-header" contenteditable="false"><span class="collection-view-icon">📑</span><span class="collection-view-title" contenteditable="true" data-property="title">${escapeHtml(title)}</span></div><div class="collection-view-body notion-block-children"></div>`;
          return div;
        }
        case 'image': {
          const div = document.createElement('div');
          div.className = 'notion-block block-image notion-block-image';
          div.id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.setAttribute('data-block-id', div.id);
          div.setAttribute('data-type', 'image');
          const src = (block.format && block.format.display_source) ||
                      getBlockPropertyPlainText(block, 'source') ||
                      'https://images.unsplash.com/photo-1517842645767-c639042777db?w=800';
          const caption = getBlockPropertyHtml(block, 'caption');
          const width = (block.format && block.format.block_width) || 700;
          div.style.maxWidth = '100%';
          div.style.width = typeof width === 'number' ? `${width}px` : width;
          div.innerHTML = `<div class="notion-image-wrap" contenteditable="false"><img src="${escapeHtml(src)}" alt="${escapeHtml(getBlockPropertyPlainText(block, 'caption'))}" /><div class="notion-image-resizer left"></div><div class="notion-image-resizer right"></div></div><div class="notion-image-caption block-image-caption" contenteditable="true" data-property="caption" placeholder="Escribe un pie de foto...">${caption}</div>`;
          return div;
        }
        case 'transclusion_container': {
          const div = document.createElement('div');
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.className = 'notion-block block-transclusion-container notion-synced-block';
          div.id = id;
          div.setAttribute('data-block-id', id);
          div.setAttribute('data-type', 'transclusion_container');
          div.innerHTML = `<div class="notion-synced-header" contenteditable="false"><span class="notion-synced-badge">🔴 Bloque Sincronizado Original · ${escapeHtml(String(id).slice(-4))}</span><div class="notion-synced-actions"><button type="button" class="notion-synced-btn btn-copy-synced">🔗 Copiar referencia</button></div></div><div class="notion-synced-body notion-block-children"></div>`;
          const btnCopy = div.querySelector('.btn-copy-synced');
          if (btnCopy) {
            btnCopy.onclick = function(e) {
              e.preventDefault();
              e.stopPropagation();
              if (typeof copySyncedBlockReference === 'function') {
                copySyncedBlockReference(id);
              } else if (typeof navigator !== 'undefined' && navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(id);
                if (typeof showToast === 'function') showToast('ID de bloque sincronizado copiado', '🔗');
              }
            };
          }
          return div;
        }
        case 'transclusion_reference': {
          const div = document.createElement('div');
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.className = 'notion-block block-transclusion-reference notion-synced-block';
          div.id = id;
          div.setAttribute('data-block-id', id);
          div.setAttribute('data-type', 'transclusion_reference');
          const targetId = (block.format && block.format.copied_from_pointer && block.format.copied_from_pointer.id) ||
                           (block.format && block.format.transclusion_reference_pointer && block.format.transclusion_reference_pointer.id) || '';
          if (targetId) div.setAttribute('data-copied-from', targetId);
          div.innerHTML = `<div class="notion-synced-header" contenteditable="false"><span class="notion-synced-badge">🔴 Referencia Sincronizada · Referencia a ${escapeHtml(String(targetId || id).slice(-4))}</span><div class="notion-synced-actions"><button type="button" class="notion-synced-btn btn-unsync">Desvincular</button></div></div><div class="notion-synced-body notion-block-children"></div>`;
          const btnUnsync = div.querySelector('.btn-unsync');
          if (btnUnsync) {
            btnUnsync.onclick = function(e) {
              e.preventDefault();
              e.stopPropagation();
              if (typeof unsyncBlockInstance === 'function') {
                unsyncBlockInstance(div);
              }
            };
          }
          return div;
        }
        case 'video': {
          const div = document.createElement('div');
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.className = 'notion-block block-video notion-block-video';
          div.id = id;
          div.setAttribute('data-block-id', id);
          div.setAttribute('data-type', 'video');
          const src = (block.format && block.format.display_source) ||
                      getBlockPropertyPlainText(block, 'source') || '';
          const captionHtml = getBlockPropertyHtml(block, 'caption');
          div.innerHTML = `<div class="notion-media-player-wrap" contenteditable="false"><video src="${escapeHtml(src)}" controls style="max-width:100%; border-radius:6px;"></video></div><div class="notion-media-caption block-video-caption" contenteditable="true" data-property="caption" placeholder="Pie de video...">${captionHtml}</div>`;
          return div;
        }
        case 'audio': {
          const div = document.createElement('div');
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.className = 'notion-block block-audio notion-block-audio';
          div.id = id;
          div.setAttribute('data-block-id', id);
          div.setAttribute('data-type', 'audio');
          const src = (block.format && block.format.display_source) ||
                      getBlockPropertyPlainText(block, 'source') || '';
          const titleHtml = getBlockPropertyHtml(block, 'title');
          div.innerHTML = `<div class="notion-audio-wrap" contenteditable="false"><audio src="${escapeHtml(src)}" controls style="width:100%;"></audio></div><div class="notion-media-caption block-audio-title" contenteditable="true" data-property="title" placeholder="Título de audio...">${titleHtml}</div>`;
          return div;
        }
        case 'file': {
          const div = document.createElement('div');
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.className = 'notion-block block-file notion-block-file';
          div.id = id;
          div.setAttribute('data-block-id', id);
          div.setAttribute('data-type', 'file');
          div.setAttribute('contenteditable', 'false');
          const src = (block.format && block.format.display_source) ||
                      getBlockPropertyPlainText(block, 'source') || '#';
          const titleHtml = getBlockPropertyHtml(block, 'title') || 'Archivo adjunto';
          const size = getBlockPropertyPlainText(block, 'size') || (block.format && block.format.file_size) || '';
          div.innerHTML = `<a href="${escapeHtml(src)}" target="_blank" class="notion-file-link"><span class="notion-file-icon">📎</span><span class="notion-file-title" contenteditable="true" data-property="title">${titleHtml}</span>${size ? `<span class="notion-file-size">${escapeHtml(size)}</span>` : ''}</a>`;
          return div;
        }
        case 'pdf': {
          const div = document.createElement('div');
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.className = 'notion-block block-pdf notion-block-pdf';
          div.id = id;
          div.setAttribute('data-block-id', id);
          div.setAttribute('data-type', 'pdf');
          const src = (block.format && block.format.display_source) ||
                      getBlockPropertyPlainText(block, 'source') || '';
          div.innerHTML = `<div class="notion-pdf-wrap" contenteditable="false">${createPdfEmbedHTML(src, getBlockPropertyPlainText(block, 'title') || 'Documento.pdf')}</div>`;
          div.setAttribute('data-source', src);
          div.setAttribute('data-title', getBlockPropertyPlainText(block, 'title') || 'Documento.pdf');
          return div;
        }
        case 'bookmark': {
          const div = document.createElement('div');
          const id = block.id || ('blk-' + Math.random().toString(36).substring(2, 9));
          div.className = 'notion-block block-bookmark notion-block-bookmark';
          div.id = id;
          div.setAttribute('data-block-id', id);
          div.setAttribute('data-type', 'bookmark');
          const link = getBlockPropertyPlainText(block, 'link') ||
                       (block.format && block.format.bookmark_url) ||
                       getBlockPropertyPlainText(block, 'source') || 'https://';
          const titleHtml = getBlockPropertyHtml(block, 'title');
          const descHtml = getBlockPropertyHtml(block, 'description');
          div.innerHTML = `<a href="${escapeHtml(link)}" target="_blank" rel="noopener noreferrer" class="notion-bookmark-inner" contenteditable="false"><div class="notion-bookmark-content"><div class="notion-bookmark-title" contenteditable="true" data-property="title">${titleHtml || escapeHtml(link)}</div>${descHtml ? `<div class="notion-bookmark-desc" contenteditable="true" data-property="description">${descHtml}</div>` : ''}<div class="notion-bookmark-url">🔗 ${escapeHtml(link)}</div></div></a>`;
          return div;
        }
        case 'p':
        default: {
          const p = document.createElement('p');
          p.className = 'notion-block block-p';
          if (block.id) p.id = block.id;
          p.setAttribute('data-block-id', p.id || ('blk-' + Math.random().toString(36).substring(2, 9)));
          p.setAttribute('data-type', block.type || 'p');
          p.setAttribute('contenteditable', 'true');
          p.setAttribute('data-property', 'title');
          p.innerHTML = (block.properties && (block.properties.html || block.properties.text)) || getBlockPropertyHtml(block, 'title');
          return p;
        }
      }
    }
    window.renderBlock = renderBlock;

    function renderBlocks(blocks, container = null) {
      const target = container || document.getElementById('rich-editor-canvas');
      if (!target || !Array.isArray(blocks)) return;
      target.innerHTML = '';
      blocks.forEach(block => {
        const el = renderBlock(block);
        if (el) target.appendChild(el);
      });
      attachSubpageBlockListeners();
    }
    window.renderBlocks = renderBlocks;

    function attachSubpageBlockListeners() {
      const canvas = document.getElementById('rich-editor-canvas');
      if (!canvas) return;
      canvas.querySelectorAll('.block-subpage').forEach(el => {
        if (!el.dataset.subpageListenerAttached) {
          el.dataset.subpageListenerAttached = 'true';
          el.setAttribute('contenteditable', 'false');
          el.style.cursor = 'pointer';
          const pageId = el.getAttribute('data-page-id');
          el.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            loadNote(pageId);
          };
        }
      });
    }
    window.attachSubpageBlockListeners = attachSubpageBlockListeners;

    function renderTreeFromRecordMap(recordMap, rootId, container) {
      const mountTarget = container || document.getElementById('rich-editor-canvas');
      if (!mountTarget || !recordMap || !recordMap.block) return;

      const ancestors = new Set();
      mountTarget.innerHTML = '';

      function renderSubtree(blockId, parentElement) {
        if (!blockId || ancestors.has(blockId)) {
          return;
        }
        ancestors.add(blockId);
        try {
          const entry = recordMap.block[blockId];
          if (!entry || !entry.value) return;
          const block = entry.value;

          if (block.alive === 0 || block.alive === false) return;

          if (blockId === rootId) {
            if (Array.isArray(block.content)) {
              block.content.forEach(childId => renderSubtree(childId, parentElement));
            }
            return;
          }

          const blockEl = renderBlock(block);
          if (!blockEl) return;

          blockEl.setAttribute('data-block-id', block.id);
          blockEl.setAttribute('data-type', block.type);
          if (block.parent_id) {
            blockEl.setAttribute('data-parent-id', block.parent_id);
          }

          if (Array.isArray(block.content) && block.content.length > 0) {
            const childrenSlot = blockEl.querySelector(
              '.notion-block-children, .block-column-content, .notion-column-content, .block-toggle-content, .notion-toggle-content, .block-table-body, .notion-table-body, .block-quote-children, .block-callout-children, .block-to-do-children, .notion-synced-body'
            ) || blockEl;
            block.content.forEach(childId => renderSubtree(childId, childrenSlot));
          }

          if (block.type === 'transclusion_reference') {
            const targetId = (block.format && block.format.copied_from_pointer && block.format.copied_from_pointer.id) ||
                             (block.format && block.format.transclusion_reference_pointer && block.format.transclusion_reference_pointer.id);
            if (targetId && recordMap.block[targetId] && recordMap.block[targetId].value) {
              const targetBlock = recordMap.block[targetId].value;
              if (targetBlock.alive !== 0 && targetBlock.alive !== false && Array.isArray(targetBlock.content) && targetBlock.content.length > 0) {
                if (!ancestors.has(targetId)) {
                  ancestors.add(targetId);
                  try {
                    const syncedSlot = blockEl.querySelector('.notion-synced-body, .notion-block-children') || blockEl;
                    targetBlock.content.forEach(childId => renderSubtree(childId, syncedSlot));
                  } finally {
                    ancestors.delete(targetId);
                  }
                }
              }
            }
          }

          parentElement.appendChild(blockEl);
        } finally {
          ancestors.delete(blockId);
        }
      }

      renderSubtree(rootId, mountTarget);

      if (typeof attachSubpageBlockListeners === 'function') attachSubpageBlockListeners();
      if (typeof renderAllInlineEquations === 'function') renderAllInlineEquations();
      if (typeof attachColumnResizerListeners === 'function') attachColumnResizerListeners();
      if (typeof tagAllEditorBlocks === 'function') tagAllEditorBlocks();
      if (typeof refreshPageTableOfContents === 'function') refreshPageTableOfContents();
    }
    window.renderTreeFromRecordMap = renderTreeFromRecordMap;

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

    /* Modal Picker para seleccionar y vincular notas en el texto */
    let currentLinkerNotes = [];

    function promptAddShortcut() {
      const activeNote = getActiveNote();
      if (!activeNote) return;

      const sel = window.getSelection();
      const canvas = document.getElementById('rich-editor-canvas');
      if (sel && sel.rangeCount > 0 && canvas.contains(sel.anchorNode)) {
        savedSelectionRange = sel.getRangeAt(0).cloneRange();
      } else {
        savedSelectionRange = null;
      }

      currentLinkerNotes = state.notes.filter(n => n.id !== activeNote.id);

      if (!currentLinkerNotes.length) {
        showToast('No hay otras notas disponibles para incrustar', 'ℹ️');
        return;
      }

      openNoteLinkerModal();
    }

    function openNoteLinkerModal() {
      const modal = document.getElementById('note-linker-modal');
      if (!modal) return;
      document.getElementById('note-linker-search').value = '';
      filterNoteLinkerList('');
      modal.classList.add('open');
    }

    function closeNoteLinkerModal() {
      const modal = document.getElementById('note-linker-modal');
      if (modal) modal.classList.remove('open');
    }

    function filterNoteLinkerList(q) {
      const listEl = document.getElementById('note-linker-list');
      if (!listEl) return;

      const filtered = currentLinkerNotes.filter(n => {
        if (!q) return true;
        return (n.title || '').toLowerCase().includes(q.toLowerCase()) || (n.folder || '').toLowerCase().includes(q.toLowerCase());
      });

      if (!filtered.length) {
        listEl.innerHTML = `<div style="padding:20px; text-align:center; color:var(--text-muted); font-size:12px;">No se encontraron notas</div>`;
        return;
      }

      listEl.innerHTML = filtered.map(n => {
        const coverBg = (n.hasCover && n.coverStyle) ? n.coverStyle : (n.coverStyle || COVER_PRESETS[Math.abs(n.id) % COVER_PRESETS.length]);
        return `
          <div class="note-item-card" onclick="selectNoteToLink(${n.id})" style="display:flex; align-items:center; justify-content:space-between; padding:8px 12px; cursor:pointer;">
            <div style="display:flex; align-items:center; gap:10px;">
              <div style="width:28px; height:36px; border-radius:4px; background:${coverBg}; background-size:cover; background-position:center; display:flex; align-items:center; justify-content:center; font-size:16px; border:1px solid var(--border-hairline); flex-shrink:0;">
                ${n.emoji || '📝'}
              </div>
              <div>
                <div style="font-weight:700; font-size:13px; color:var(--text-primary);">${n.title || 'Sin título'}</div>
                <div style="font-size:11px; color:var(--text-muted);">${n.folder} · Actualizado recientemente</div>
              </div>
            </div>
            <button class="btn-primary" style="padding:4px 10px; font-size:11px;">+ Incrustar</button>
          </div>
        `;
      }).join('');
    }

    function selectNoteToLink(noteId) {
      closeNoteLinkerModal();
      insertNoteCardAtSelection(noteId, savedSelectionRange);
      savedSelectionRange = null;
    }

    function insertSubpageBlock() {
      const note = getActiveNote();
      if (!note) return;
      const title = prompt('Título de la nueva subpágina o nota vinculada:');
      if (!title || !title.trim()) return;

      const newId = Date.now();
      const subpage = {
        id: newId,
        title: title.trim(),
        emoji: '📄',
        hasCover: true,
        coverStyle: COVER_PRESETS[state.notes.length % COVER_PRESETS.length],
        content: `Subpágina vinculada creada desde "${note.title}". Escribe aquí tus notas o ejercicios resueltos.`,
        folder: note.folder,
        tags: 'subpagina',
        isPinned: false,
        updatedAt: Date.now(),
        parentId: note.id,
        subpages: [],
        revisions: [],
        showCallout: false,
        showKanban: false,
        showTable: false,
        tableFormula: '',
        tableRows: [],
        showChecklist: false,
        checklists: [],
        katex: ''
      };

      state.notes.push(subpage);

      const canvas = document.getElementById('rich-editor-canvas');
      const blkId = 'blk-' + Date.now();
      const subpageEl = renderBlock({
        id: blkId,
        type: 'sub_page',
        page_id: String(newId),
        title: subpage.title
      });

      let inserted = false;
      if (savedSelectionRange && canvas && canvas.contains(savedSelectionRange.startContainer)) {
        savedSelectionRange.insertNode(subpageEl);
        inserted = true;
      } else {
        const sel = window.getSelection();
        if (sel && sel.rangeCount > 0 && canvas && canvas.contains(sel.anchorNode)) {
          const r = sel.getRangeAt(0);
          r.insertNode(subpageEl);
          inserted = true;
        }
      }

      if (!inserted && canvas) {
        canvas.appendChild(subpageEl);
      }
      savedSelectionRange = null;

      attachSubpageBlockListeners();
      syncRichEditor();
      save();
      renderNotesList();
      showToast(`Subpágina "${subpage.title}" creada e insertada`, '📄');
    }

    /* Toast Notification Floating Chip */
    let toastTimer = null;
    function showToast(msg, icon = '✦') {
      let toast = document.getElementById('app-toast');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'app-toast';
        toast.className = 'toast-notification';
        document.body.appendChild(toast);
      }
      toast.innerHTML = `<span style="color:var(--accent-amber); font-weight:800; font-size:14px;">${icon}</span><span>${msg}</span>`;
      toast.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {
        toast.classList.remove('show');
      }, 2400);
    }

    /* Toggle Block */
    function insertToggleBlock() {
      const note = getActiveNote();
      if (!note) return;
      note.showToggle = true;
      save();
      loadActiveNote();
      const toggleEl = document.getElementById('block-toggle');
      if (toggleEl) toggleEl.classList.add('open');
      scrollAndHighlightBlock('block-toggle', '#toggle-header-input');
      showToast('Lista desplegable Toggle insertada', '▶');
    }
    function updateToggleHeader(val) {
      const note = getActiveNote();
      if (!note) return;
      note.toggleHeader = val;
      save();
    }
    function updateToggleBody(val) {
      const note = getActiveNote();
      if (!note) return;
      note.toggleBody = val;
      save();
    }

    /* Callout & Quote & Code */
    function toggleCalloutBlock(forceShow = false) {
      const note = getActiveNote();
      if (!note) return;
      note.showCallout = forceShow ? true : !note.showCallout;
      note.callout = note.callout || 'Nota destacada (Notion Callout).';
      save();
      loadActiveNote();
      if (note.showCallout) {
        scrollAndHighlightBlock('block-callout', '#callout-input');
        showToast('Bloque Callout insertado', '💡');
      }
    }
    function updateCalloutText(text) {
      const note = getActiveNote();
      if (!note) return;
      note.callout = text;
      save();
    }
    function changeCalloutEmoji() {
      const emojis = ['💡', '⚠️', '⭐', '📌', '🔍', '🎯'];
      const note = getActiveNote();
      if (!note) return;
      const idx = emojis.indexOf(note.calloutEmoji || '💡');
      note.calloutEmoji = emojis[(idx + 1) % emojis.length];
      save();
      loadActiveNote();
    }

    function toggleQuoteBlock(forceShow = false) {
      const note = getActiveNote();
      if (!note) return;
      note.showQuote = forceShow ? true : !note.showQuote;
      note.quote = note.quote || 'Cita de ejemplo...';
      save();
      loadActiveNote();
      if (note.showQuote) {
        scrollAndHighlightBlock('block-quote', '#quote-input');
        showToast('Bloque de cita insertado', '❝');
      }
    }
    function updateQuoteText(val) {
      const note = getActiveNote();
      if (!note) return;
      note.quote = val;
      save();
    }
    function updateCodeText(val) {
      const note = getActiveNote();
      if (!note) return;
      note.code = val;
      save();
    }
    function copyCodeBlock() {
      const code = document.getElementById('code-input').value;
      navigator.clipboard.writeText(code).then(() => showToast('Código copiado al portapapeles', '📋'));
    }

    /* Kanban Notion */
    function toggleKanbanBlock(forceShow = false) {
      const note = getActiveNote();
      if (!note) return;
      note.showKanban = forceShow ? true : !note.showKanban;
      if (!note.kanban || !note.kanban.length) {
        note.kanban = [
          { text: "Planificar sprint", status: "done" },
          { text: "Estructurar bloques", status: "in-progress" },
          { text: "Probar cálculos", status: "todo" }
        ];
      }
      save();
      loadActiveNote();
      if (note.showKanban) {
        scrollAndHighlightBlock('block-kanban');
        showToast('Tablero Kanban activo', '📊');
      }
    }

    let currentDraggingKanbanCardId = null;

    function escapeKanbanAttr(str) {
      return String(str || '').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    function escapeKanbanHtml(str) {
      return String(str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function normalizeKanbanNote(note) {
      if (!note) return;
      note.kanban = note.kanban || [];
      note.kanbanGroupBy = note.kanbanGroupBy || 'category';
      if (!Array.isArray(note.kanbanCollapsedLanes)) {
        note.kanbanCollapsedLanes = [];
      }
      if (!Array.isArray(note.kanbanCustomCategories)) {
        note.kanbanCustomCategories = [];
      }
      if (!Array.isArray(note.kanbanCustomAssignees)) {
        note.kanbanCustomAssignees = [];
      }

      note.kanban.forEach((c, idx) => {
        if (!c.id) {
          c.id = 'kc-' + Date.now() + '-' + idx + '-' + Math.random().toString(36).substr(2, 5);
        }
        if (!c.category || !c.category.trim()) {
          c.category = 'General';
        }
        if (!c.assignee || !c.assignee.trim()) {
          c.assignee = 'Sin Asignar';
        }
        if (!c.priority) {
          c.priority = 'Media';
        }
        if (!c.status) {
          c.status = 'todo';
        }
      });
    }

    function renderKanban(note) {
      if (!note) note = getActiveNote();
      if (!note) return;
      normalizeKanbanNote(note);

      const container = document.getElementById('kanban-board-container');
      if (!container) return;

      const cards = note.kanban || [];
      const todos = cards.filter(c => c.status === 'todo');
      const progress = cards.filter(c => c.status === 'in-progress');
      const dones = cards.filter(c => c.status === 'done');

      const groupBy = note.kanbanGroupBy || 'category';
      const collapsedLanes = new Set(note.kanbanCollapsedLanes || []);

      // Obtener lista de grupos según criterio
      let groups = [];
      if (groupBy === 'category') {
        const fromCards = cards.map(c => c.category).filter(Boolean);
        const combined = Array.from(new Set([...fromCards, ...(note.kanbanCustomCategories || [])]));
        if (combined.length === 0) {
          combined.push('Diseño UI', 'Desarrollo', 'Infraestructura', 'General');
        }
        groups = combined;
      } else if (groupBy === 'assignee') {
        const fromCards = cards.map(c => c.assignee).filter(Boolean);
        const combined = Array.from(new Set([...fromCards, ...(note.kanbanCustomAssignees || [])]));
        if (combined.length === 0) {
          combined.push('Ana', 'Carlos', 'Joaquín', 'Sin Asignar');
        }
        groups = combined;
      }

      function renderKanbanCardHtml(c) {
        const isDone = c.status === 'done';
        const priorityClass = (c.priority || 'Media').toLowerCase();
        const pIcon = c.priority === 'Alta' ? '🔴' : (c.priority === 'Baja' ? '🟢' : '🟡');

        return `
          <div class="kanban-card ${isDone ? 'status-done' : ''}"
               draggable="true"
               id="kanban-card-${c.id}"
               data-kanban-id="${escapeKanbanAttr(c.id)}"
               data-kanban-text="${escapeKanbanAttr(c.text)}"
               data-kanban-status="${c.status}"
               data-kanban-category="${escapeKanbanAttr(c.category)}"
               data-kanban-assignee="${escapeKanbanAttr(c.assignee)}"
               ondragstart="handleBlockKanbanCardDragStart(event, '${c.id}')"
               ondragend="handleBlockKanbanCardDragEnd(event)"
               title="Arrastra para mover entre columnas o filas · Clic derecho para opciones">
            <div class="kanban-card-top-row">
              <span class="kanban-card-title">${escapeKanbanHtml(c.text)}</span>
              <span class="kanban-card-drag-indicator" title="Manejador de arrastre">⋮⋮</span>
            </div>
            <div class="kanban-card-meta-row">
              <span class="kanban-badge-tag category-badge">🏷️ ${escapeKanbanHtml(c.category || 'General')}</span>
              <span class="kanban-badge-tag assignee-badge">👤 ${escapeKanbanHtml(c.assignee || 'Sin Asignar')}</span>
              <span class="kanban-badge-tag priority-${priorityClass}">${pIcon} ${escapeKanbanHtml(c.priority || 'Media')}</span>
            </div>
            <div class="kanban-card-actions">
              <div class="kanban-card-actions-left">
                <button type="button" class="btn-kanban-action" onclick="openKanbanCardModal('${c.id}')" title="Editar detalles de la tarea">✏️</button>
                ${c.status !== 'todo' ? `<button type="button" class="btn-kanban-action" onclick="moveKanbanCardStep('${c.id}', -1)" title="Retroceder estado">←</button>` : ''}
                ${c.status !== 'done' ? `<button type="button" class="btn-kanban-action" onclick="moveKanbanCardStep('${c.id}', 1)" title="Avanzar estado">→</button>` : ''}
              </div>
              <div class="kanban-card-actions-right">
                <button type="button" class="btn-kanban-action danger" onclick="deleteKanbanCardById('${c.id}')" title="Eliminar tarea">🗑</button>
              </div>
            </div>
          </div>
        `;
      }

      function renderDropzone(status, groupKey, poolCards) {
        const matchingCards = poolCards.filter(c => {
          if (c.status !== status) return false;
          if (groupBy === 'none') return true;
          const cardGroup = groupBy === 'category' ? (c.category || 'General') : (c.assignee || 'Sin Asignar');
          return cardGroup === groupKey;
        });

        const cardsMarkup = matchingCards.length > 0
          ? matchingCards.map(c => renderKanbanCardHtml(c)).join('')
          : `
            <div class="kanban-lane-empty-placeholder" onclick="openKanbanCardModal(null, '${status}', '${escapeKanbanAttr(groupKey === 'none' ? '' : groupKey)}')">
              <span>+ Añadir o soltar tarea aquí</span>
            </div>
          `;

        return `
          <div class="kanban-lane-dropzone"
               data-kanban-status="${status}"
               data-kanban-group="${escapeKanbanAttr(groupKey)}"
               ondragover="handleBlockKanbanDragOver(event)"
               ondragleave="handleBlockKanbanDragLeave(event)"
               ondrop="handleBlockKanbanDrop(event, '${status}', '${escapeKanbanAttr(groupKey)}')">
            ${cardsMarkup}
          </div>
        `;
      }

      let lanesHtml = '';
      if (groupBy !== 'none') {
        lanesHtml = `
          <div class="kanban-swimlanes-list">
            ${groups.map(groupName => {
              const isCollapsed = collapsedLanes.has(groupName);
              const groupCards = cards.filter(c => (groupBy === 'category' ? (c.category || 'General') : (c.assignee || 'Sin Asignar')) === groupName);
              const groupIcon = groupBy === 'category' ? '🏷️' : '👤';

              return `
                <div class="kanban-swimlane-row" data-swimlane-group="${escapeKanbanAttr(groupName)}">
                  <div class="kanban-swimlane-banner" onclick="toggleKanbanSwimlane('${escapeKanbanAttr(groupName)}')">
                    <div class="kanban-swimlane-banner-left">
                      <span class="kanban-swimlane-chevron">${isCollapsed ? '▶' : '▼'}</span>
                      <span class="kanban-swimlane-title">${groupIcon} ${escapeKanbanHtml(groupName)}</span>
                      <span class="kanban-swimlane-count-badge">(${groupCards.length} ${groupCards.length === 1 ? 'tarea' : 'tareas'})</span>
                    </div>
                    <div class="kanban-swimlane-banner-right">
                      <button type="button" class="kanban-swimlane-add-card-btn" onclick="event.stopPropagation(); openKanbanCardModal(null, 'todo', '${escapeKanbanAttr(groupName)}')">
                        + Tarea en esta fila
                      </button>
                    </div>
                  </div>
                  <div class="kanban-swimlane-body ${isCollapsed ? 'collapsed' : ''}">
                    ${renderDropzone('todo', groupName, groupCards)}
                    ${renderDropzone('in-progress', groupName, groupCards)}
                    ${renderDropzone('done', groupName, groupCards)}
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        `;
      } else {
        lanesHtml = `
          <div class="kanban-swimlane-body" style="padding:0; margin-top:4px;">
            ${renderDropzone('todo', 'none', cards)}
            ${renderDropzone('in-progress', 'none', cards)}
            ${renderDropzone('done', 'none', cards)}
          </div>
        `;
      }

      container.innerHTML = `
        <div class="kanban-toolbar-bar">
          <div class="kanban-toolbar-left">
            <span class="kanban-title-text">📊 Tablero Kanban con Filas (Swimlanes)</span>
            <div class="kanban-groupby-group">
              <label for="kanban-groupby-select">Filas por:</label>
              <select id="kanban-groupby-select" onchange="setKanbanGroupBy(this.value)">
                <option value="category" ${groupBy === 'category' ? 'selected' : ''}>🏷️ Categoría</option>
                <option value="assignee" ${groupBy === 'assignee' ? 'selected' : ''}>👤 Asignado</option>
                <option value="none" ${groupBy === 'none' ? 'selected' : ''}>⊞ Sin filas</option>
              </select>
            </div>
          </div>
          <div class="kanban-toolbar-right">
            ${groupBy !== 'none' ? `
              <button type="button" class="kanban-tool-btn" onclick="promptAddKanbanSwimlane()" title="Añadir una nueva fila horizontal">
                <span>➕</span>
                <span>Añadir Fila</span>
              </button>
              <button type="button" class="kanban-tool-btn" onclick="toggleAllKanbanSwimlanes()" title="Alternar colapso de todas las filas">
                <span>↕</span>
                <span>Alternar todo</span>
              </button>
            ` : ''}
            <button type="button" class="kanban-tool-btn primary" onclick="openKanbanCardModal()" title="Crear una nueva tarjeta">
              <span>+</span>
              <span>Nueva Tarea</span>
            </button>
          </div>
        </div>

        <div class="kanban-global-columns-bar">
          <div class="kanban-global-col-header col-todo">
            <span>⏳ Por Hacer</span>
            <span class="kanban-global-col-count" id="kcount-todo">${todos.length}</span>
          </div>
          <div class="kanban-global-col-header col-progress">
            <span>🔄 En Progreso</span>
            <span class="kanban-global-col-count" id="kcount-progress">${progress.length}</span>
          </div>
          <div class="kanban-global-col-header col-done">
            <span>✅ Completado</span>
            <span class="kanban-global-col-count" id="kcount-done">${dones.length}</span>
          </div>
        </div>

        ${lanesHtml}
      `;
    }

    function setKanbanGroupBy(groupByValue) {
      const note = getActiveNote();
      if (!note) return;
      note.kanbanGroupBy = groupByValue;
      note.kanbanCollapsedLanes = [];
      save();
      renderKanban(note);
      const label = groupByValue === 'category' ? 'Categoría' : (groupByValue === 'assignee' ? 'Asignado' : 'Sin filas');
      showToast(`Tablero agrupado por: ${label}`, '📊');
    }

    function toggleKanbanSwimlane(groupKey) {
      const note = getActiveNote();
      if (!note) return;
      note.kanbanCollapsedLanes = note.kanbanCollapsedLanes || [];
      const idx = note.kanbanCollapsedLanes.indexOf(groupKey);
      if (idx > -1) {
        note.kanbanCollapsedLanes.splice(idx, 1);
      } else {
        note.kanbanCollapsedLanes.push(groupKey);
      }
      save();
      renderKanban(note);
    }

    function toggleAllKanbanSwimlanes() {
      const note = getActiveNote();
      if (!note) return;
      const groupBy = note.kanbanGroupBy || 'category';
      if (groupBy === 'none') return;

      const cards = note.kanban || [];
      let groups = [];
      if (groupBy === 'category') {
        const fromCards = cards.map(c => c.category).filter(Boolean);
        groups = Array.from(new Set([...fromCards, ...(note.kanbanCustomCategories || [])]));
      } else {
        const fromCards = cards.map(c => c.assignee).filter(Boolean);
        groups = Array.from(new Set([...fromCards, ...(note.kanbanCustomAssignees || [])]));
      }

      note.kanbanCollapsedLanes = note.kanbanCollapsedLanes || [];
      if (note.kanbanCollapsedLanes.length >= groups.length && groups.length > 0) {
        note.kanbanCollapsedLanes = [];
        showToast('Todas las filas desplegadas', '📂');
      } else {
        note.kanbanCollapsedLanes = [...groups];
        showToast('Todas las filas plegadas', '📁');
      }
      save();
      renderKanban(note);
    }

    function promptAddKanbanSwimlane() {
      const note = getActiveNote();
      if (!note) return;
      const groupBy = note.kanbanGroupBy || 'category';
      if (groupBy === 'none') {
        showToast('Activa la agrupación por categoría o asignado primero', 'ℹ️');
        return;
      }

      const promptLabel = groupBy === 'category' ? 'Nombre de la nueva categoría (Fila):' : 'Nombre del asignado (Fila):';
      const name = prompt(promptLabel);
      if (!name || !name.trim()) return;
      const cleanName = name.trim();

      if (groupBy === 'category') {
        note.kanbanCustomCategories = note.kanbanCustomCategories || [];
        if (!note.kanbanCustomCategories.includes(cleanName)) {
          note.kanbanCustomCategories.push(cleanName);
        }
      } else {
        note.kanbanCustomAssignees = note.kanbanCustomAssignees || [];
        if (!note.kanbanCustomAssignees.includes(cleanName)) {
          note.kanbanCustomAssignees.push(cleanName);
        }
      }

      save();
      renderKanban(note);
      showToast(`Nueva fila creada: ${cleanName}`, '➕');
    }

    function handleBlockKanbanCardDragStart(e, cardId) {
      currentDraggingKanbanCardId = cardId;
      if (e.dataTransfer) {
        e.dataTransfer.setData('text/plain', cardId);
        e.dataTransfer.effectAllowed = 'move';
      }
      const el = document.getElementById(`kanban-card-${cardId}`);
      if (el) {
        el.classList.add('block-is-dragging');
      }
    }

    function handleBlockKanbanCardDragEnd(e) {
      if (currentDraggingKanbanCardId) {
        const el = document.getElementById(`kanban-card-${currentDraggingKanbanCardId}`);
        if (el) el.classList.remove('block-is-dragging');
      }
      currentDraggingKanbanCardId = null;
      document.querySelectorAll('.kanban-lane-dropzone.kanban-lane-drop-active').forEach(dz => {
        dz.classList.remove('kanban-lane-drop-active');
      });
    }

    function handleBlockKanbanDragOver(e) {
      e.preventDefault();
      if (e.dataTransfer) {
        e.dataTransfer.dropEffect = 'move';
      }
      const dropzone = e.target.closest('.kanban-lane-dropzone');
      if (dropzone && !dropzone.classList.contains('kanban-lane-drop-active')) {
        document.querySelectorAll('.kanban-lane-dropzone.kanban-lane-drop-active').forEach(dz => {
          if (dz !== dropzone) dz.classList.remove('kanban-lane-drop-active');
        });
        dropzone.classList.add('kanban-lane-drop-active');
      }
    }

    function handleBlockKanbanDragLeave(e) {
      const dropzone = e.target.closest('.kanban-lane-dropzone');
      if (dropzone && e.relatedTarget && !dropzone.contains(e.relatedTarget)) {
        dropzone.classList.remove('kanban-lane-drop-active');
      }
    }

    function handleBlockKanbanDrop(e, targetStatus, targetGroupKey) {
      e.preventDefault();
      document.querySelectorAll('.kanban-lane-dropzone.kanban-lane-drop-active').forEach(dz => {
        dz.classList.remove('kanban-lane-drop-active');
      });

      const cardId = (e.dataTransfer && e.dataTransfer.getData('text/plain')) || currentDraggingKanbanCardId;
      if (!cardId) return;

      const note = getActiveNote();
      if (!note || !note.kanban) return;

      const card = note.kanban.find(c => c.id === cardId || c.text === cardId);
      if (!card) return;

      card.status = targetStatus;

      // Si se suelta en una fila específica, actualizar la propiedad de agrupación
      const groupBy = note.kanbanGroupBy || 'category';
      if (targetGroupKey && targetGroupKey !== 'none') {
        if (groupBy === 'category') {
          card.category = targetGroupKey;
        } else if (groupBy === 'assignee') {
          card.assignee = targetGroupKey;
        }
      }

      currentDraggingKanbanCardId = null;
      save();
      renderKanban(note);

      const statusLabels = { todo: 'Por Hacer', 'in-progress': 'En Progreso', done: 'Completado' };
      showToast(`Tarjeta movida a ${statusLabels[targetStatus] || targetStatus}`, '📊');
    }

    function openKanbanCardModal(cardId, defaultStatus, defaultGroup) {
      const note = getActiveNote();
      if (!note) return;
      normalizeKanbanNote(note);

      const modal = document.getElementById('modal-kanban-card');
      if (!modal) return;

      const editIdInput = document.getElementById('kanban-card-edit-id');
      const titleText = document.getElementById('modal-kanban-title-text');
      const textInput = document.getElementById('kanban-input-text');
      const statusSelect = document.getElementById('kanban-input-status');
      const prioritySelect = document.getElementById('kanban-input-priority');
      const categoryInput = document.getElementById('kanban-input-category');
      const assigneeInput = document.getElementById('kanban-input-assignee');

      const card = cardId ? note.kanban.find(c => c.id === cardId || c.text === cardId) : null;

      if (card) {
        if (editIdInput) editIdInput.value = card.id;
        if (titleText) titleText.textContent = 'Editar Tarjeta del Tablero';
        if (textInput) textInput.value = card.text || '';
        if (statusSelect) statusSelect.value = card.status || 'todo';
        if (prioritySelect) prioritySelect.value = card.priority || 'Media';
        if (categoryInput) categoryInput.value = card.category || 'General';
        if (assigneeInput) assigneeInput.value = card.assignee || 'Sin Asignar';
      } else {
        if (editIdInput) editIdInput.value = '';
        if (titleText) titleText.textContent = 'Nueva Tarjeta del Tablero';
        if (textInput) textInput.value = '';
        if (statusSelect) statusSelect.value = defaultStatus || 'todo';
        if (prioritySelect) prioritySelect.value = 'Media';

        const groupBy = note.kanbanGroupBy || 'category';
        if (categoryInput) {
          categoryInput.value = (groupBy === 'category' && defaultGroup) ? defaultGroup : 'General';
        }
        if (assigneeInput) {
          assigneeInput.value = (groupBy === 'assignee' && defaultGroup) ? defaultGroup : 'Sin Asignar';
        }
      }

      modal.style.display = 'flex';
      setTimeout(() => textInput && textInput.focus(), 50);
    }

    function closeKanbanCardModal() {
      const modal = document.getElementById('modal-kanban-card');
      if (modal) modal.style.display = 'none';
    }

    function saveKanbanCardModal() {
      const note = getActiveNote();
      if (!note) return;
      normalizeKanbanNote(note);

      const editId = (document.getElementById('kanban-card-edit-id')?.value || '').trim();
      const text = (document.getElementById('kanban-input-text')?.value || '').trim();
      const status = document.getElementById('kanban-input-status')?.value || 'todo';
      const priority = document.getElementById('kanban-input-priority')?.value || 'Media';
      const category = (document.getElementById('kanban-input-category')?.value || 'General').trim() || 'General';
      const assignee = (document.getElementById('kanban-input-assignee')?.value || 'Sin Asignar').trim() || 'Sin Asignar';

      if (!text) {
        showToast('Escribe un título para la tarjeta', '⚠️');
        return;
      }

      if (editId) {
        const card = note.kanban.find(c => c.id === editId);
        if (card) {
          card.text = text;
          card.status = status;
          card.priority = priority;
          card.category = category;
          card.assignee = assignee;
          showToast('Tarjeta actualizada', '✏️');
        }
      } else {
        const newCard = {
          id: 'kc-' + Date.now() + '-' + Math.random().toString(36).substr(2, 6),
          text: text,
          status: status,
          priority: priority,
          category: category,
          assignee: assignee
        };
        note.kanban.push(newCard);
        showToast('Nueva tarjeta añadida al tablero', '📋');
      }

      closeKanbanCardModal();
      save();
      renderKanban(note);
    }

    function moveKanbanCardStep(cardId, dir) {
      const note = getActiveNote();
      if (!note || !note.kanban) return;
      const card = note.kanban.find(c => c.id === cardId || c.text === cardId);
      if (!card) return;

      const order = ['todo', 'in-progress', 'done'];
      const curIdx = order.indexOf(card.status || 'todo');
      const nextIdx = curIdx + dir;
      if (nextIdx >= 0 && nextIdx < order.length) {
        card.status = order[nextIdx];
        save();
        renderKanban(note);
      }
    }

    function deleteKanbanCardById(cardId) {
      const note = getActiveNote();
      if (!note || !note.kanban) return;
      note.kanban = note.kanban.filter(c => c.id !== cardId && c.text !== cardId);
      save();
      renderKanban(note);
      showToast('Tarjeta eliminada', '🗑');
    }

    // Funciones retrocompatibles para atajos y menús contextuales
    function addKanbanCard(status) {
      openKanbanCardModal(null, status || 'todo');
    }

    function moveKanbanCard(identifier, newStatus) {
      const note = getActiveNote();
      if (!note || !note.kanban) return;
      const card = note.kanban.find(c => c.id === identifier || c.text === identifier);
      if (card) {
        card.status = newStatus;
        save();
        renderKanban(note);
      }
    }

    function moveKanbanCardVertical(identifier, dir) {
      const note = getActiveNote();
      if (!note || !note.kanban) return;
      const idx = note.kanban.findIndex(c => c.id === identifier || c.text === identifier);
      if (idx === -1) return;
      const target = idx + dir;
      if (target < 0 || target >= note.kanban.length) return;
      const item = note.kanban.splice(idx, 1)[0];
      note.kanban.splice(target, 0, item);
      save();
      renderKanban(note);
    }

    function deleteKanbanCard(identifier) {
      deleteKanbanCardById(identifier);
    }

      /* Checklist Integrada en el Texto con Botón de Basura a la Izquierda y Enter Continuo */
      function insertChecklistBlock() {
        const note = getActiveNote();
        if (!note) return;
        note.showChecklist = true;
        note.checklists = note.checklists || [];
        const newIdx = note.checklists.length;
        note.checklists.push({ text: "", done: false });
        save();
        loadActiveNote();
        scrollAndHighlightBlock('block-checklists', '#checklist-input-' + newIdx);
        showToast('Tarea añadida a la lista Checklist', '☑');
      }

      function renderChecklists(note) {
        const container = document.getElementById('checklist-items');
        if (!container) return;

        const items = note.checklists || [];
        if (!items.length) {
          container.innerHTML = '';
          return;
        }

        container.innerHTML = items.map((item, idx) => `
          <div class="checklist-item-row" data-idx="${idx}" style="position:relative; display:flex; align-items:center; gap:10px; padding:3px 0;">
            <div class="block-floating-controls">
              <div class="btn-side-drag" draggable="true" title="Mover tarea">
                <svg class="vertical-grip-icon" viewBox="0 0 10 16" width="10" height="15" fill="currentColor">
                  <circle cx="2.5" cy="2.5" r="1.4"/><circle cx="7.5" cy="2.5" r="1.4"/>
                  <circle cx="2.5" cy="8" r="1.4"/><circle cx="7.5" cy="8" r="1.4"/>
                  <circle cx="2.5" cy="13.5" r="1.4"/><circle cx="7.5" cy="13.5" r="1.4"/>
                </svg>
              </div>
              <button class="btn-side-delete" onclick="removeCheckItem(${idx})" title="Eliminar tarea" aria-label="Eliminar tarea">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 6h18m-2 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  <line x1="10" y1="11" x2="10" y2="17"></line>
                  <line x1="14" y1="11" x2="14" y2="17"></line>
                </svg>
              </button>
            </div>
            <input type="checkbox" class="checklist-custom-checkbox" ${item.done ? 'checked' : ''} onchange="toggleCheckItem(${idx}, this.checked)" title="Marcar / Desmarcar tarea" />
            <input type="text" id="checklist-input-${idx}" class="checklist-text-input" value="${(item.text || '').replace(/"/g, '&quot;')}" placeholder="Escribe una tarea..." style="flex:1; background:transparent; border:none; color:var(--text-primary); font-family:inherit; font-size:14.5px; line-height:1.5; outline:none; ${item.done ? 'text-decoration:line-through; color:var(--text-muted);' : ''}" oninput="updateCheckItemText(${idx}, this.value)" onkeydown="handleChecklistKeyDown(event, ${idx})" />
          </div>
        `).join('');
      }

      function handleChecklistKeyDown(e, idx) {
        if (e.key === 'Enter') {
          e.preventDefault();
          addChecklistItemAfter(idx);
        } else if (e.key === 'Backspace' && e.target.value === '') {
          e.preventDefault();
          removeCheckItem(idx);
        } else if (e.key === 'ArrowUp' && e.target.selectionStart === 0) {
          if (idx > 0) {
            e.preventDefault();
            const prev = document.getElementById('checklist-input-' + (idx - 1));
            if (prev) prev.focus();
          }
        } else if (e.key === 'ArrowDown' && e.target.selectionEnd === e.target.value.length) {
          const next = document.getElementById('checklist-input-' + (idx + 1));
          if (next) {
            e.preventDefault();
            next.focus();
          }
        }
      }

      function addChecklistItemAfter(idx) {
        const note = getActiveNote();
        if (!note) return;
        note.checklists = note.checklists || [];
        const nextIdx = idx + 1;
        note.checklists.splice(nextIdx, 0, { text: "", done: false });
        save();
        renderChecklists(note);
        setTimeout(() => {
          const input = document.getElementById('checklist-input-' + nextIdx);
          if (input) input.focus();
        }, 30);
      }

      function toggleCheckItem(idx, checked) {
        const note = getActiveNote();
        if (!note || !note.checklists[idx]) return;
        note.checklists[idx].done = checked;
        save();
        renderChecklists(note);
      }

      function updateCheckItemText(idx, val) {
        const note = getActiveNote();
        if (!note || !note.checklists[idx]) return;
        note.checklists[idx].text = val;
        save();
      }

      function removeCheckItem(idx) {
        const note = getActiveNote();
        if (!note || !note.checklists) return;
        note.checklists.splice(idx, 1);
        if (!note.checklists.length) {
          note.showChecklist = false;
        }
        save();
        renderChecklists(note);
        const focusIdx = Math.max(0, idx - 1);
        const prevInput = document.getElementById('checklist-input-' + focusIdx);
        if (prevInput) {
          prevInput.focus();
        } else {
          const canvas = document.getElementById('rich-editor-canvas');
          if (canvas) canvas.focus();
        }
      }

    /* KaTeX */
    function toggleKatexBlock(forceShow = false) {
      const note = getActiveNote();
      if (!note) return;
      if (forceShow) {
        note.katex = note.katex || '\\int_{0}^{\\infty} e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}';
      } else {
        note.katex = note.katex ? '' : '\\int_{0}^{\\infty} e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}';
      }
      save();
      loadActiveNote();
      if (note.katex) {
        scrollAndHighlightBlock('block-katex', '#katex-formula-input');
        showToast('Bloque de ecuación KaTeX insertado', '∑');
      }
    }

    function setSampleKatex() {
      const note = getActiveNote();
      if (!note) return;
      note.katex = 'i\\hbar\\frac{\\partial}{\\partial t}\\Psi(\\mathbf{r},t) = \\hat{H}\\Psi(\\mathbf{r},t)';
      document.getElementById('katex-formula-input').value = note.katex;
      renderKatexFormula(note.katex);
      save();
    }

    function renderKatexFormula(latex) {
      const out = document.getElementById('katex-render-box');
      if (window.katex) {
        try {
          window.katex.render(latex || '\\text{Ecuación}', out, { displayMode: true, throwOnError: false });
        } catch (_) { out.textContent = latex; }
      } else { out.textContent = latex; }
    }

    function cycleTypographyStyle() {
      const styles = ['H1 (Título)', 'H2 (Encabezado)', 'H3 (Subtítulo)', 'Cuerpo'];
      state.typeStyleIndex = (state.typeStyleIndex + 1) % styles.length;
      const label = styles[state.typeStyleIndex];
      document.getElementById('current-type-label').textContent = label.split(' ')[0];
      if (state.typeStyleIndex === 0) formatDoc('formatBlock', '<h1>');
      else if (state.typeStyleIndex === 1) formatDoc('formatBlock', '<h2>');
      else if (state.typeStyleIndex === 2) formatDoc('formatBlock', '<h3>');
      else formatDoc('formatBlock', '<p>');
    }

    /* Portada & Emoji Handlers */
    function toggleCover() {
      const note = getActiveNote();
      if (!note) return;
      if (!note.hasCover) { chooseNoteCoverPhoto(note.id); return; }
      note.hasCover = false;
      note.updatedAt = Date.now();
      save();
      loadActiveNote();
    }

    function changeCoverImage() {
      chooseNoteCoverPhoto();
    }

    function changeEmojiIcon() {
      const note = getActiveNote();
      if (!note) return;
      const currentIdx = EMOJI_PALETTE.indexOf(note.emoji || '📝');
      const nextIdx = (currentIdx + 1) % EMOJI_PALETTE.length;
      note.emoji = EMOJI_PALETTE[nextIdx];
      save();
      renderNotesList();
      renderNoteTabs();
      loadActiveNote();
    }

    function togglePinActiveNote() {
      const note = getActiveNote();
      if (!note) return;
      note.isPinned = !note.isPinned;
      save();
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      loadActiveNote();
    }

    function deleteActiveNote() {
      const note = getActiveNote();
      if (!note) return;
      deleteNoteById(note.id);
    }

    function createNewNote(initialExtraFolder = null) {
      // Siempre se crea en la carpeta principal "Todas Las Notas"; si la carpeta activa es física, también se asigna a ella
      const initialFolders = [MASTER_ALL_NOTES_FOLDER];
      if (initialExtraFolder && !isMasterAllNotesFolder(initialExtraFolder) && !isTrashFolder(initialExtraFolder) && !isSmartFolder(initialExtraFolder)) {
        initialFolders.push(initialExtraFolder);
      }

      const newNote = {
        id: Date.now(),
        title: "Nueva nota",
        emoji: "📝",
        hasCover: false,
        coverStyle: COVER_PRESETS[0],
        content: "",
        folder: MASTER_ALL_NOTES_FOLDER,
        folders: initialFolders,
        isTrashed: false,
        tags: "",
        isPinned: (state.selectedCollection === 'PINNED'),
        updatedAt: Date.now(),
        parentId: null,
        subpages: [],
        revisions: [],
        showCallout: false,
        showKanban: false,
        kanban: [],
        showTable: false,
        tableFormula: 'style(upper(prop("Nombre")), "b", "blue")',
        tableRows: [],
        showChecklist: false,
        checklists: [],
        katex: ""
      };
      setNoteFolders(newNote, initialFolders);
      if (window.NoteJSCloud) window.NoteJSCloud.attachNew(newNote);

      state.notes.unshift(newNote);
      state.activeNoteId = newNote.id;
      state.selectedFolder = initialExtraFolder && !isMasterAllNotesFolder(initialExtraFolder)
        ? initialExtraFolder
        : MASTER_ALL_NOTES_FOLDER;

      if (state.isRemindersActive) {
        exitRemindersView();
      }
      if (state.isHomeActive) {
        exitHomeView();
      }

      if (!Array.isArray(state.openTabIds)) state.openTabIds = [];
      if (!state.openTabIds.includes(newNote.id)) {
        state.openTabIds.push(newNote.id);
      }
      saveOpenTabsState();
      save(false, newNote);
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      loadActiveNote();

      // Enfocar y seleccionar el título para nombrarla inmediatamente
      setTimeout(() => {
        const titleEl = document.getElementById('note-title');
        if (titleEl) {
          titleEl.focus();
          titleEl.select();
        }
      }, 60);
    }

    /* ============================================================================
       MODAL INTERACTIVO DE CARPETAS Y SUBCARPETAS CON ICONOS EMOJI PERSONALIZADOS
       ============================================================================ */
    let folderModalState = {
      mode: 'create', // 'create' | 'emoji' | 'edit'
      folderType: 'standard', // 'standard' | 'smart'
      targetFolder: null,
      parentFolder: '',
      selectedEmoji: '📁',
      activeCategoryId: 'organizacion'
    };

    function setFolderModalType(type) {
      const cleanType = (type === 'smart') ? 'smart' : 'standard';
      folderModalState.folderType = cleanType;

      const btnStandard = document.getElementById('ftype-btn-standard');
      const btnSmart = document.getElementById('ftype-btn-smart');
      if (btnStandard) btnStandard.classList.toggle('active', cleanType === 'standard');
      if (btnSmart) btnSmart.classList.toggle('active', cleanType === 'smart');

      const parentGroup = document.getElementById('folder-parent-select-group');
      const smartRulesContainer = document.getElementById('folder-smart-rules-container');
      const smartSwitchBar = document.getElementById('folder-modal-smart-switch-bar');
      const titleEl = document.getElementById('folder-modal-title');
      const subtitleEl = document.getElementById('folder-modal-subtitle');
      const submitBtnEl = document.getElementById('folder-modal-submit-btn');
      const emojiInputEl = document.getElementById('folder-custom-emoji-input');
      const headerIconEl = document.getElementById('folder-modal-header-icon');

      if (cleanType === 'smart') {
        if (parentGroup) parentGroup.style.display = 'none';
        if (smartRulesContainer) smartRulesContainer.style.display = 'block';
        if (smartSwitchBar) smartSwitchBar.style.display = 'none';

        if (titleEl) {
          titleEl.textContent = folderModalState.mode === 'edit'
            ? `Editar Carpeta Inteligente "${getFolderDisplayName(folderModalState.targetFolder)}"`
            : 'Nueva Carpeta Inteligente';
        }
        if (subtitleEl) {
          subtitleEl.textContent = 'Filtro dinámico de notas por etiquetas, fechas o tareas (no almacena notas físicamente)';
        }
        if (submitBtnEl) {
          submitBtnEl.textContent = '⚙️ Guardar Carpeta Inteligente';
        }

        if (emojiInputEl && (!emojiInputEl.value || emojiInputEl.value === '📁')) {
          emojiInputEl.value = '⚙️';
          folderModalState.selectedEmoji = '⚙️';
          if (headerIconEl) headerIconEl.textContent = '⚙️';
        }

        if (!smartFolderModalState.rules || !smartFolderModalState.rules.length) {
          smartFolderModalState.rules = [createDefaultSmartRule('tags')];
        }

        setSmartFolderMatchMode(smartFolderModalState.matchMode || 'all', false);
        renderSmartFolderRulesList();
        updateSmartFolderLivePreview();
      } else {
        if (parentGroup && folderModalState.mode !== 'emoji') parentGroup.style.display = 'block';
        if (smartRulesContainer) smartRulesContainer.style.display = 'none';
        if (smartSwitchBar && folderModalState.mode !== 'emoji') smartSwitchBar.style.display = 'flex';

        if (titleEl) {
          titleEl.textContent = folderModalState.mode === 'create'
            ? 'Nueva Carpeta Personalizada'
            : `Editar Carpeta "${getFolderDisplayName(folderModalState.targetFolder)}"`;
        }
        if (subtitleEl) {
          subtitleEl.textContent = 'Elige un icono de emoji personalizado y nombre; se guardará en SQLite';
        }
        if (submitBtnEl) {
          submitBtnEl.textContent = folderModalState.mode === 'create' ? '+ Crear carpeta' : 'Guardar carpeta';
        }

        if (emojiInputEl && emojiInputEl.value === '⚙️') {
          emojiInputEl.value = '📁';
          folderModalState.selectedEmoji = '📁';
          if (headerIconEl) headerIconEl.textContent = '📁';
        }
      }

      updateFolderModalPreview();
    }

    function promptNewFolder() {
      openFolderModal('create');
    }

    function openSubfolderModal(parentFolder) {
      closeCustomContextMenu();
      if (!parentFolder || isMasterAllNotesFolder(parentFolder) || isTrashFolder(parentFolder)) {
        openFolderModal('create');
        return;
      }
      openFolderModal('create', null, parentFolder);
    }

    function populateFolderParentSelect(selectedParent = '', excludeFolder = null) {
      const parentSelect = document.getElementById('folder-parent-select');
      if (!parentSelect) return;
      ensureMasterFolderFirst();
      const candidates = state.folders.filter(f => {
        if (!f || isMasterAllNotesFolder(f) || isTrashFolder(f) || isSmartFolder(f)) return false;
        if (excludeFolder && (f === excludeFolder || f.startsWith(excludeFolder + '/'))) return false;
        return true;
      });
      parentSelect.innerHTML = `<option value="">Ninguna (Carpeta principal en raíz)</option>` + candidates.map(f => {
        const safeHtml = escapeHtmlAttr(f);
        const isSel = f === selectedParent ? 'selected' : '';
        return `<option value="${safeHtml}" ${isSel}>${getFolderEmoji(f)} ${safeHtml}</option>`;
      }).join('');
      parentSelect.value = selectedParent || '';
    }

    function openFolderModal(mode = 'create', folderName = null, presetParentFolder = '') {
      closeCustomContextMenu();
      if (mode !== 'create' && isMasterAllNotesFolder(folderName)) {
        showToast('La carpeta principal "Todas Las Notas" no se puede modificar', '🔒');
        return;
      }
      const modal = document.getElementById('folder-custom-modal');
      if (!modal) return;

      folderModalState.mode = mode || 'create';
      folderModalState.targetFolder = folderName || null;
      const existingParent = folderName ? getFolderParentPath(folderName) : (presetParentFolder || '');
      folderModalState.parentFolder = existingParent;

      const isTargetSmart = Boolean(folderName && isSmartFolder(folderName));
      const initialType = isTargetSmart ? 'smart' : 'standard';

      if (initialType === 'smart') {
        const cfg = getSmartFolderConfig(folderName) || { matchMode: 'all', rules: [] };
        smartFolderModalState.mode = 'edit';
        smartFolderModalState.targetFolder = folderName;
        smartFolderModalState.emoji = getFolderEmoji(folderName) || '⚙️';
        smartFolderModalState.matchMode = cfg.matchMode === 'any' ? 'any' : 'all';
        smartFolderModalState.rules = (cfg.rules && cfg.rules.length)
          ? JSON.parse(JSON.stringify(cfg.rules))
          : [createDefaultSmartRule('tags')];
      } else {
        smartFolderModalState.mode = 'create';
        smartFolderModalState.targetFolder = null;
        smartFolderModalState.emoji = '⚙️';
        smartFolderModalState.matchMode = 'all';
        smartFolderModalState.rules = [createDefaultSmartRule('tags')];
      }

      const currentEmoji = folderName ? getFolderEmoji(folderName) : '📁';
      folderModalState.selectedEmoji = currentEmoji;

      const titleEl = document.getElementById('folder-modal-title');
      const subtitleEl = document.getElementById('folder-modal-subtitle');
      const headerIconEl = document.getElementById('folder-modal-header-icon');
      const emojiInputEl = document.getElementById('folder-custom-emoji-input');
      const nameInputEl = document.getElementById('folder-custom-name-input');
      const submitBtnEl = document.getElementById('folder-modal-submit-btn');
      const parentGroupEl = document.getElementById('folder-parent-select-group');

      populateFolderParentSelect(existingParent, mode === 'create' ? null : folderName);

      const smartSwitchBarEl = document.getElementById('folder-modal-smart-switch-bar');
      const smartSwitchLabelEl = document.getElementById('folder-modal-smart-switch-label');
      const smartSwitchBtnEl = document.getElementById('folder-modal-smart-switch-btn');

      if (mode === 'create') {
        if (titleEl) {
          titleEl.textContent = existingParent
            ? `Nueva Subcarpeta en "${existingParent}"`
            : 'Nueva Carpeta o Subcarpeta';
        }
        if (subtitleEl) subtitleEl.textContent = 'Elige nombre, carpeta superior opcional e icono emoji';
        if (submitBtnEl) submitBtnEl.textContent = existingParent ? '+ Crear subcarpeta' : '+ Crear carpeta';
        if (parentGroupEl) parentGroupEl.style.display = 'block';
        if (smartSwitchBarEl) smartSwitchBarEl.style.display = 'flex';
        if (smartSwitchLabelEl) smartSwitchLabelEl.textContent = '¿Prefieres un filtro dinámico por reglas (#tags, fechas, tareas)?';
        if (smartSwitchBtnEl) smartSwitchBtnEl.textContent = '⚙️ Crear Carpeta Inteligente';
        if (nameInputEl) {
          nameInputEl.value = '';
          nameInputEl.disabled = false;
        }
      } else if (mode === 'emoji') {
        if (titleEl) titleEl.textContent = `Icono Emoji de "${getFolderDisplayName(folderName)}"`;
        if (subtitleEl) subtitleEl.textContent = 'Haz clic en un emoji o escribe cualquiera personalizado para esta carpeta';
        if (submitBtnEl) submitBtnEl.textContent = 'Guardar icono emoji';
        if (parentGroupEl) parentGroupEl.style.display = 'none';
        if (smartSwitchBarEl) smartSwitchBarEl.style.display = 'none';
        if (nameInputEl) {
          nameInputEl.value = getFolderDisplayName(folderName) || '';
          nameInputEl.disabled = false;
        }
      } else {
        if (titleEl) titleEl.textContent = `Editar Carpeta "${getFolderDisplayName(folderName)}"`;
        if (subtitleEl) subtitleEl.textContent = 'Modifica el nombre, ubicación o icono de emoji personalizado de la carpeta';
        if (submitBtnEl) submitBtnEl.textContent = 'Guardar cambios';
        if (parentGroupEl) parentGroupEl.style.display = 'block';
        if (smartSwitchBarEl) smartSwitchBarEl.style.display = 'flex';
        if (smartSwitchLabelEl) smartSwitchLabelEl.textContent = 'Convertir esta carpeta en una Carpeta Inteligente (irreversible):';
        if (smartSwitchBtnEl) smartSwitchBtnEl.textContent = '⚙️ Convertir en Inteligente...';
        if (nameInputEl) {
          nameInputEl.value = getFolderDisplayName(folderName) || '';
          nameInputEl.disabled = false;
        }
      }

      if (headerIconEl) headerIconEl.textContent = currentEmoji;
      if (emojiInputEl) emojiInputEl.value = currentEmoji;

      renderFolderModalCategories();
      renderFolderModalEmojiGrid();
      updateFolderModalPreview();
      setFolderModalType(initialType);

      modal.classList.add('open');

      setTimeout(() => {
        if (mode === 'emoji' && emojiInputEl) {
          emojiInputEl.focus();
          emojiInputEl.select();
        } else if (nameInputEl) {
          nameInputEl.focus();
          nameInputEl.select();
        }
      }, 50);
    }

    function closeFolderModal() {
      const modal = document.getElementById('folder-custom-modal');
      if (modal) modal.classList.remove('open');
    }

    function renderFolderModalCategories() {
      const tabsEl = document.getElementById('folder-emoji-category-tabs');
      if (!tabsEl) return;

      const allTabs = [
        { id: 'ALL', label: '✨ Todos' },
        ...FOLDER_EMOJI_CATEGORIES.map(c => ({ id: c.id, label: c.label }))
      ];

      tabsEl.innerHTML = allTabs.map(tab => `
        <button type="button"
                class="folder-emoji-cat-btn ${folderModalState.activeCategoryId === tab.id ? 'active' : ''}"
                onclick="setFolderModalEmojiCategory('${tab.id}')">
          ${tab.label}
        </button>
      `).join('');
    }

    function setFolderModalEmojiCategory(catId) {
      folderModalState.activeCategoryId = catId;
      renderFolderModalCategories();
      renderFolderModalEmojiGrid();
    }

    function renderFolderModalEmojiGrid() {
      const gridEl = document.getElementById('folder-emoji-picker-grid');
      if (!gridEl) return;

      let emojisList = [];
      if (folderModalState.activeCategoryId === 'ALL') {
        const seen = new Set();
        FOLDER_EMOJI_CATEGORIES.forEach(cat => {
          cat.emojis.forEach(em => {
            if (!seen.has(em)) {
              seen.add(em);
              emojisList.push(em);
            }
          });
        });
      } else {
        const found = FOLDER_EMOJI_CATEGORIES.find(c => c.id === folderModalState.activeCategoryId) || FOLDER_EMOJI_CATEGORIES[0];
        emojisList = found ? found.emojis : [];
      }

      gridEl.innerHTML = emojisList.map(em => {
        const isSel = folderModalState.selectedEmoji === em;
        return `
          <button type="button"
                  class="folder-emoji-option-btn ${isSel ? 'selected' : ''}"
                  onclick="selectFolderModalEmoji('${em}')"
                  title="Elegir ${em}">
            ${em}
          </button>
        `;
      }).join('');
    }

    function selectFolderModalEmoji(emoji) {
      const clean = (emoji || '').trim() || '📁';
      folderModalState.selectedEmoji = clean;
      const emojiInputEl = document.getElementById('folder-custom-emoji-input');
      if (emojiInputEl) emojiInputEl.value = clean;
      const headerIconEl = document.getElementById('folder-modal-header-icon');
      if (headerIconEl) headerIconEl.textContent = clean;
      renderFolderModalEmojiGrid();
      updateFolderModalPreview();
    }

    function handleFolderCustomEmojiInput(rawVal) {
      const clean = (rawVal || '').trim() || '📁';
      folderModalState.selectedEmoji = clean;
      const headerIconEl = document.getElementById('folder-modal-header-icon');
      if (headerIconEl) headerIconEl.textContent = clean;
      renderFolderModalEmojiGrid();
      updateFolderModalPreview();
    }

    function handleFolderCustomNameInput() {
      updateFolderModalPreview();
    }

    function pickRandomFolderEmoji() {
      const allEmojis = [];
      FOLDER_EMOJI_CATEGORIES.forEach(cat => {
        cat.emojis.forEach(em => allEmojis.push(em));
      });
      const randomEmoji = allEmojis[Math.floor(Math.random() * allEmojis.length)] || '📁';
      selectFolderModalEmoji(randomEmoji);
    }

    function updateFolderModalPreview() {
      const previewEmojiEl = document.getElementById('folder-modal-preview-emoji');
      const previewNameEl = document.getElementById('folder-modal-preview-name');
      const nameInputEl = document.getElementById('folder-custom-name-input');
      const parentSelectEl = document.getElementById('folder-parent-select');
      const chosenParent = parentSelectEl ? parentSelectEl.value.trim() : '';
      const typedLeaf = (nameInputEl ? nameInputEl.value.trim().replace(/\//g, '-') : '') || (folderModalState.targetFolder ? getFolderDisplayName(folderModalState.targetFolder) : 'Nueva carpeta');
      const fullPreview = chosenParent ? `${chosenParent} / ${typedLeaf}` : typedLeaf;

      if (previewEmojiEl) previewEmojiEl.textContent = folderModalState.selectedEmoji || '📁';
      if (previewNameEl) previewNameEl.textContent = fullPreview;
    }

    function setFolderEmoji(folderName, emoji) {
      if (!folderName) return;
      closeCustomContextMenu();
      if (isMasterAllNotesFolder(folderName)) {
        showToast('El icono de "Todas Las Notas" no se puede cambiar', '🔒');
        return;
      }
      const cleanEmoji = (emoji || '').trim() || '📁';
      if (!state.folderEmojis || typeof state.folderEmojis !== 'object') {
        state.folderEmojis = { ...DEFAULT_FOLDER_EMOJIS };
      }
      state.folderEmojis[folderName] = cleanEmoji;
      persistFoldersLocal();

      renderFolders();
      renderNotesList();
      renderNoteTabs();

      if (hasPyWebViewBridge() && typeof window.pywebview.api.set_folder_emoji === 'function') {
        window.pywebview.api.set_folder_emoji(folderName, cleanEmoji).catch(() => {});
      } else {
        fetch('/api/folders/emoji', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ folder: folderName, emoji: cleanEmoji })
        }).catch(() => {});
      }
      saveFoldersToBackend();
      showToast(`Icono de "${folderName}" actualizado a ${cleanEmoji}`, cleanEmoji);
    }

    function submitFolderModal() {
      if (folderModalState.folderType === 'smart') {
        submitSmartFolderModal();
        return;
      }
      const nameInputEl = document.getElementById('folder-custom-name-input');
      const emojiInputEl = document.getElementById('folder-custom-emoji-input');
      const parentSelectEl = document.getElementById('folder-parent-select');
      const leafName = (nameInputEl ? nameInputEl.value.trim().replace(/\//g, '-') : '');
      const chosenParent = (folderModalState.mode === 'emoji')
        ? (folderModalState.targetFolder ? getFolderParentPath(folderModalState.targetFolder) : '')
        : (parentSelectEl ? parentSelectEl.value.trim() : '');
      const newName = chosenParent ? `${chosenParent}/${leafName}` : leafName;
      const chosenEmoji = (emojiInputEl ? emojiInputEl.value.trim() : '') || folderModalState.selectedEmoji || '📁';

      if (!leafName) {
        showToast('Escribe un nombre para la carpeta', '⚠️');
        if (nameInputEl) nameInputEl.focus();
        return;
      }

      if (isMasterAllNotesFolder(leafName) || isMasterAllNotesFolder(newName)) {
        showToast('El nombre "Todas Las Notas" está reservado para la carpeta principal', '🔒');
        return;
      }

      if (!state.folderEmojis || typeof state.folderEmojis !== 'object') {
        state.folderEmojis = { ...DEFAULT_FOLDER_EMOJIS };
      }

      if (folderModalState.mode === 'create') {
        if (state.folders.includes(newName)) {
          state.folderEmojis[newName] = chosenEmoji;
          saveFoldersToBackend();
          renderFolders();
          renderNotesList();
          closeFolderModal();
          showToast(`Icono de "${newName}" actualizado a ${chosenEmoji}`, chosenEmoji);
          return;
        }
        state.folders.push(newName);
        state.folderEmojis[newName] = chosenEmoji;
        // Si se creó como subcarpeta, asegurarse de que la carpeta padre esté expandida
        if (chosenParent && Array.isArray(state.collapsedParentFolders)) {
          state.collapsedParentFolders = state.collapsedParentFolders.filter(p => p !== chosenParent);
        }
        saveFoldersToBackend();
        renderFolders();
        renderNotesList();
        if (state.isHomeActive) {
          renderHomeFoldersSearchRow();
        }
        closeFolderModal();
        showToast(`${chosenParent ? 'Subcarpeta' : 'Carpeta'} "${chosenEmoji} ${newName}" creada`, chosenEmoji);
        return;
      }

      const oldName = folderModalState.targetFolder;
      if (!oldName || isMasterAllNotesFolder(oldName)) {
        closeFolderModal();
        return;
      }

      if (newName !== oldName && state.folders.includes(newName)) {
        showToast(`Ya existe una carpeta llamada "${newName}"`, '⚠️');
        return;
      }

      if (newName !== oldName) {
        const oldPrefix = oldName + '/';
        state.folders = state.folders.map(f => {
          if (f === oldName) return newName;
          if (f.startsWith(oldPrefix)) return newName + '/' + f.slice(oldPrefix.length);
          return f;
        });
        delete state.folderEmojis[oldName];
        state.folderEmojis[newName] = chosenEmoji;

        state.notes.forEach(n => {
          const currentFolders = getNoteUserFolders(n);
          const updated = currentFolders.map(f => {
            if (f === oldName) return newName;
            if (f.startsWith(oldPrefix)) return newName + '/' + f.slice(oldPrefix.length);
            return f;
          });
          setNoteFolders(n, updated);
        });
        if (state.selectedFolder === oldName) state.selectedFolder = newName;
        save();
      } else {
        state.folderEmojis[oldName] = chosenEmoji;
      }

      saveFoldersToBackend();
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      if (state.isHomeActive) {
        renderHomePage();
      } else {
        loadActiveNote();
      }
      closeFolderModal();
      showToast(`Carpeta "${chosenEmoji} ${newName}" guardada en SQLite`, chosenEmoji);
    }

    /* ============================================================================
       CONSTRUCTOR Y MOTOR DE CARPETAS INTELIGENTES (Apple Notes Smart Folders)
       ============================================================================ */
    let smartFolderModalState = {
      mode: 'create', // 'create' | 'edit'
      targetFolder: null,
      emoji: '⚙️',
      matchMode: 'all', // 'all' (AND) | 'any' (OR)
      rules: []
    };

    let pendingSmartConvertFolderName = null;

    const SMART_RULE_DEFINITIONS = {
      tags: {
        label: '🏷️ Etiquetas (#tags)',
        conditions: [
          { value: 'any_selected', label: 'Contiene cualquiera de estas etiquetas' },
          { value: 'all_selected', label: 'Contiene todas estas etiquetas' },
          { value: 'none_selected', label: 'No contiene estas etiquetas' },
          { value: 'any_tag', label: 'Con cualquier etiqueta' },
          { value: 'untagged', label: 'Notas sin ninguna etiqueta' }
        ]
      },
      date: {
        label: '📅 Fecha de creación / modificación',
        conditions: [
          { value: 'today', label: 'Hoy' },
          { value: 'yesterday', label: 'Ayer' },
          { value: 'last_7_days', label: 'Últimos 7 días' },
          { value: 'last_30_days', label: 'Últimos 30 días' },
          { value: 'custom_range', label: 'Rango de fechas personalizado' }
        ]
      },
      checklists: {
        label: '☑ Listas de tareas (Checklists)',
        conditions: [
          { value: 'any', label: 'Contiene listas de tareas' },
          { value: 'unchecked', label: 'Con ítems sin marcar (pendientes)' },
          { value: 'checked', label: 'Con ítems marcados (completados)' },
          { value: 'both', label: 'Con ítems marcados y sin marcar (ambos)' },
          { value: 'none', label: 'Sin listas de tareas' }
        ]
      },
      attachments: {
        label: '📎 Archivos adjuntos',
        conditions: [
          { value: 'any', label: 'Cualquier archivo adjunto o enlace' },
          { value: 'photos_videos', label: 'Incluye fotos o videos' },
          { value: 'pdfs', label: 'Incluye documentos PDF' },
          { value: 'audio', label: 'Incluye grabaciones de audio' },
          { value: 'drawings', label: 'Incluye dibujos o ecuaciones' },
          { value: 'links', label: 'Incluye enlaces web o notas incrustadas' }
        ]
      },
      shared: {
        label: '👥 Notas compartidas',
        conditions: [
          { value: 'any_shared', label: 'Compartida en general (con cualquiera)' },
          { value: 'specific_user', label: 'Compartida con usuario específico (@usuario)' },
          { value: 'not_shared', label: 'No compartidas (privadas)' }
        ]
      },
      pinned_locked: {
        label: '🔒 Estado de bloqueo y fijadas',
        conditions: [
          { value: 'locked', label: 'Notas protegidas por contraseña (Bloqueadas)' },
          { value: 'not_locked', label: 'Notas no protegidas (Sin candado)' },
          { value: 'pinned', label: 'Notas ancladas con chincheta (Fijadas)' },
          { value: 'not_pinned', label: 'Notas no fijadas' },
          { value: 'pinned_or_locked', label: 'Notas fijadas o bloqueadas' }
        ]
      },
      mentions: {
        label: '💬 Menciones (@tu_usuario)',
        conditions: [
          { value: 'any_mention', label: 'Contiene cualquier @mención' },
          { value: 'specific_mention', label: 'Menciona a un @usuario específico' },
          { value: 'no_mentions', label: 'Sin menciones' }
        ]
      }
    };

    function createDefaultSmartRule(type = 'tags') {
      if (type === 'tags') {
        const allTags = getAllKnownTagsList();
        return {
          id: 'sr-' + Date.now() + '-' + Math.floor(Math.random() * 999),
          type: 'tags',
          condition: 'any_selected',
          value: allTags[0] || 'importante'
        };
      }
      if (type === 'date') {
        const todayIso = new Date().toISOString().slice(0, 10);
        return {
          id: 'sr-' + Date.now() + '-' + Math.floor(Math.random() * 999),
          type: 'date',
          field: 'updatedAt',
          condition: 'last_7_days',
          from: todayIso,
          to: todayIso
        };
      }
      if (type === 'checklists') {
        return {
          id: 'sr-' + Date.now() + '-' + Math.floor(Math.random() * 999),
          type: 'checklists',
          condition: 'unchecked'
        };
      }
      if (type === 'attachments') {
        return {
          id: 'sr-' + Date.now() + '-' + Math.floor(Math.random() * 999),
          type: 'attachments',
          condition: 'any'
        };
      }
      if (type === 'shared') {
        return {
          id: 'sr-' + Date.now() + '-' + Math.floor(Math.random() * 999),
          type: 'shared',
          condition: 'any_shared',
          value: ''
        };
      }
      if (type === 'pinned_locked') {
        return {
          id: 'sr-' + Date.now() + '-' + Math.floor(Math.random() * 999),
          type: 'pinned_locked',
          condition: 'locked'
        };
      }
      if (type === 'mentions') {
        return {
          id: 'sr-' + Date.now() + '-' + Math.floor(Math.random() * 999),
          type: 'mentions',
          condition: 'any_mention',
          value: 'tu_usuario'
        };
      }
      return {
        id: 'sr-' + Date.now(),
        type: 'tags',
        condition: 'any_tag',
        value: ''
      };
    }

    function getAllKnownTagsList() {
      const set = new Set();
      (state.notes || []).forEach(n => {
        if (n && !n.isTrashed) {
          extractNoteTagsList(n).forEach(t => set.add(t));
        }
      });
      return Array.from(set).sort();
    }

    function switchFolderModalToSmart() {
      const currentMode = folderModalState.mode;
      const targetFolder = folderModalState.targetFolder;
      const typedName = (document.getElementById('folder-custom-name-input')?.value || '').trim();
      const chosenEmoji = (document.getElementById('folder-custom-emoji-input')?.value || '').trim() || '⚙️';
      closeFolderModal();

      if (currentMode === 'edit' && targetFolder && !isSmartFolder(targetFolder)) {
        openConvertStandardToSmartModal(targetFolder);
        return;
      }

      openSmartFolderModal('create', null, typedName, chosenEmoji === '📁' ? '⚙️' : chosenEmoji);
    }

    function openSmartFolderModal(mode = 'create', folderName = null, presetName = '', presetEmoji = '⚙️') {
      closeCustomContextMenu();
      const targetMode = mode === 'edit' ? 'edit' : 'create';
      openFolderModal(targetMode, folderName);
      setFolderModalType('smart');
      if (presetName) {
        const nameInput = document.getElementById('folder-custom-name-input') || document.getElementById('smart-folder-name-input');
        if (nameInput) nameInput.value = presetName;
      }
      if (presetEmoji && presetEmoji !== '📁') {
        selectFolderModalEmoji(presetEmoji);
      }
    }

    function closeSmartFolderModal() {
      const modal = document.getElementById('smart-folder-modal');
      if (modal) modal.classList.remove('open');
      closeFolderModal();
    }

    function handleSmartFolderEmojiInput(val) {
      const clean = String(val || '').trim() || '⚙️';
      smartFolderModalState.emoji = clean;
      const headerIcon = document.getElementById('smart-folder-modal-icon-preview') || document.getElementById('smart-folder-modal-icon') || document.getElementById('folder-modal-header-icon');
      if (headerIcon) headerIcon.textContent = clean;
    }

    function cycleSmartFolderEmoji() {
      const smartEmojis = ['⚙️', '⚡', '🔍', '🏷️', '📌', '☑️', '📎', '📅', '🔒', '👥', '✨', '🧠'];
      const current = smartFolderModalState.emoji || '⚙️';
      const idx = smartEmojis.indexOf(current);
      const next = smartEmojis[(idx + 1) % smartEmojis.length];
      const emojiInput = document.getElementById('folder-custom-emoji-input') || document.getElementById('smart-folder-emoji-input');
      if (emojiInput) emojiInput.value = next;
      handleSmartFolderEmojiInput(next);
    }

    function setSmartFolderMatchMode(mode, rerender = true) {
      smartFolderModalState.matchMode = mode === 'any' ? 'any' : 'all';
      const btnAll = document.getElementById('smart-logic-btn-all') || document.getElementById('smart-match-all-btn');
      const btnAny = document.getElementById('smart-logic-btn-any') || document.getElementById('smart-match-any-btn');
      if (btnAll) btnAll.classList.toggle('active', smartFolderModalState.matchMode === 'all');
      if (btnAny) btnAny.classList.toggle('active', smartFolderModalState.matchMode === 'any');

      const uBtnAll = document.getElementById('unified-smart-logic-btn-all');
      const uBtnAny = document.getElementById('unified-smart-logic-btn-any');
      if (uBtnAll) uBtnAll.classList.toggle('active', smartFolderModalState.matchMode === 'all');
      if (uBtnAny) uBtnAny.classList.toggle('active', smartFolderModalState.matchMode === 'any');

      if (rerender) {
        updateSmartFolderLivePreview();
      }
    }

    function addSmartFolderRuleRow(presetType = null) {
      const usedTypes = smartFolderModalState.rules.map(r => r.type);
      const allTypes = Object.keys(SMART_RULE_DEFINITIONS);
      const nextType = presetType || allTypes.find(t => !usedTypes.includes(t)) || 'tags';
      smartFolderModalState.rules.push(createDefaultSmartRule(nextType));
      renderSmartFolderRulesList();
      updateSmartFolderLivePreview();
    }

    function removeSmartFolderRuleRow(idx) {
      if (smartFolderModalState.rules.length <= 1) {
        showToast('Una carpeta inteligente debe tener al menos una regla activa', '⚙️');
        return;
      }
      smartFolderModalState.rules.splice(idx, 1);
      renderSmartFolderRulesList();
      updateSmartFolderLivePreview();
    }

    function updateSmartFolderRuleField(idx, field, value) {
      const rule = smartFolderModalState.rules[idx];
      if (!rule) return;
      if (field === 'type') {
        const replacement = createDefaultSmartRule(value);
        smartFolderModalState.rules[idx] = replacement;
        renderSmartFolderRulesList();
        updateSmartFolderLivePreview();
        return;
      }
      rule[field] = value;
      if (field === 'condition') {
        renderSmartFolderRulesList();
      }
      updateSmartFolderLivePreview();
    }

    function toggleTagInSmartRule(idx, tagName) {
      const rule = smartFolderModalState.rules[idx];
      if (!rule) return;
      const cleanTag = String(tagName || '').trim().toLowerCase().replace(/^#/, '');
      if (!cleanTag) return;
      const current = String(rule.value || '')
        .split(',')
        .map(s => s.trim().toLowerCase().replace(/^#/, ''))
        .filter(Boolean);
      const exists = current.includes(cleanTag);
      const next = exists ? current.filter(t => t !== cleanTag) : [...current, cleanTag];
      rule.value = next.join(', ');
      renderSmartFolderRulesList();
      updateSmartFolderLivePreview();
    }

    function renderSmartFolderRulesList() {
      const container = document.getElementById('unified-smart-folder-rules-list') || document.getElementById('smart-folder-rules-list');
      if (!container) return;

      const knownTags = getAllKnownTagsList();

      container.innerHTML = smartFolderModalState.rules.map((rule, idx) => {
        const def = SMART_RULE_DEFINITIONS[rule.type] || SMART_RULE_DEFINITIONS.tags;
        const typeOptionsHtml = Object.keys(SMART_RULE_DEFINITIONS).map(tKey => `
          <option value="${tKey}" ${rule.type === tKey ? 'selected' : ''}>${SMART_RULE_DEFINITIONS[tKey].label}</option>
        `).join('');

        const condOptionsHtml = def.conditions.map(c => `
          <option value="${c.value}" ${rule.condition === c.value ? 'selected' : ''}>${c.label}</option>
        `).join('');

        let extraParamsHtml = '';

        if (rule.type === 'tags' && ['any_selected', 'all_selected', 'none_selected'].includes(rule.condition)) {
          const selectedTags = String(rule.value || '')
            .split(',')
            .map(s => s.trim().toLowerCase().replace(/^#/, ''))
            .filter(Boolean);
          const tagPillsHtml = knownTags.map(t => {
            const isSel = selectedTags.includes(t);
            const safeT = escapeHtmlAttr(t);
            return `<button type="button" class="smart-rule-tag-pill ${isSel ? 'active' : ''}" onclick="toggleTagInSmartRule(${idx}, '${safeT}')">#${safeT}</button>`;
          }).join('');

          extraParamsHtml = `
            <div class="smart-rule-extra-row">
              <input type="text" class="smart-rule-text-input" value="${escapeHtmlAttr(rule.value || '')}" placeholder="Ej. trabajo, fisica, urgente (separadas por coma)" oninput="updateSmartFolderRuleField(${idx}, 'value', this.value)" />
              ${knownTags.length ? `<div class="smart-rule-tag-Suggestions">${tagPillsHtml}</div>` : ''}
            </div>
          `;
        } else if (rule.type === 'date') {
          const fieldSelectHtml = `
            <select class="smart-rule-subselect" onchange="updateSmartFolderRuleField(${idx}, 'field', this.value)">
              <option value="updatedAt" ${rule.field !== 'createdAt' ? 'selected' : ''}>Fecha de modificación</option>
              <option value="createdAt" ${rule.field === 'createdAt' ? 'selected' : ''}>Fecha de creación</option>
            </select>
          `;
          const rangeInputsHtml = rule.condition === 'custom_range' ? `
            <div class="smart-rule-date-range">
              <label>Desde: <input type="date" class="smart-rule-date-input" value="${escapeHtmlAttr(rule.from || '')}" onchange="updateSmartFolderRuleField(${idx}, 'from', this.value)" /></label>
              <label>Hasta: <input type="date" class="smart-rule-date-input" value="${escapeHtmlAttr(rule.to || '')}" onchange="updateSmartFolderRuleField(${idx}, 'to', this.value)" /></label>
            </div>
          ` : '';
          extraParamsHtml = `
            <div class="smart-rule-extra-row">
              ${fieldSelectHtml}
              ${rangeInputsHtml}
            </div>
          `;
        } else if (rule.type === 'shared' && rule.condition === 'specific_user') {
          extraParamsHtml = `
            <div class="smart-rule-extra-row">
              <input type="text" class="smart-rule-text-input" value="${escapeHtmlAttr(rule.value || '')}" placeholder="Nombre o @usuario (ej. @ana, @equipo)" oninput="updateSmartFolderRuleField(${idx}, 'value', this.value)" />
            </div>
          `;
        } else if (rule.type === 'mentions' && rule.condition === 'specific_mention') {
          extraParamsHtml = `
            <div class="smart-rule-extra-row">
              <input type="text" class="smart-rule-text-input" value="${escapeHtmlAttr(rule.value || '')}" placeholder="Usuario mencionado (ej. @tu_usuario)" oninput="updateSmartFolderRuleField(${idx}, 'value', this.value)" />
            </div>
          `;
        }

        return `
          <div class="smart-rule-row">
            <div class="smart-rule-main-controls">
              <span class="smart-rule-index-badge">#${idx + 1}</span>
              <select class="smart-rule-type-select" onchange="updateSmartFolderRuleField(${idx}, 'type', this.value)">
                ${typeOptionsHtml}
              </select>
              <select class="smart-rule-cond-select" onchange="updateSmartFolderRuleField(${idx}, 'condition', this.value)">
                ${condOptionsHtml}
              </select>
              <button type="button" class="smart-rule-delete-btn" onclick="removeSmartFolderRuleRow(${idx})" title="Quitar esta regla">✕</button>
            </div>
            ${extraParamsHtml}
          </div>
        `;
      }).join('');
    }

    function getDraftSmartFolderMatchingNotes() {
      const rules = Array.isArray(smartFolderModalState.rules) ? smartFolderModalState.rules : [];
      const matchMode = smartFolderModalState.matchMode === 'any' ? 'any' : 'all';
      const activeNotes = getActiveNotesList();
      if (!rules.length) return [];
      return activeNotes.filter(note => {
        if (matchMode === 'any') {
          return rules.some(r => noteMatchesSmartRule(note, r));
        }
        return rules.every(r => noteMatchesSmartRule(note, r));
      });
    }

    function updateSmartFolderLivePreview() {
      const countBadge = document.getElementById('unified-smart-folder-preview-count') || document.getElementById('smart-folder-preview-count');
      const listEl = document.getElementById('unified-smart-folder-preview-samples') || document.getElementById('smart-folder-preview-samples') || document.getElementById('smart-folder-preview-notes');
      if (!countBadge || !listEl) return;

      const matched = getDraftSmartFolderMatchingNotes();
      countBadge.textContent = `${matched.length} ${matched.length === 1 ? 'nota coincide en tiempo real' : 'notas coinciden en tiempo real'}`;

      if (!matched.length) {
        listEl.innerHTML = `<span class="smart-preview-empty">Ninguna nota activa cumple estas condiciones ahora mismo.</span>`;
        return;
      }

      listEl.innerHTML = matched.slice(0, 8).map(n => {
        const safeTitle = escapeHtmlAttr(n.title || 'Sin título');
        const origFolder = getNotePrimaryDisplayFolder(n);
        return `
          <span class="smart-preview-note-pill" title="Ubicación real: ${escapeHtmlAttr(origFolder)}">
            <span>${n.emoji || '📝'}</span>
            <span>${safeTitle}</span>
            <small>${escapeHtmlAttr(getFolderDisplayName(origFolder))}</small>
          </span>
        `;
      }).join('') + (matched.length > 8 ? `<span class="smart-preview-note-pill">+${matched.length - 8} más</span>` : '');
    }

    function submitSmartFolderModal() {
      const nameInput = document.getElementById('folder-custom-name-input') || document.getElementById('smart-folder-name-input');
      const emojiInput = document.getElementById('folder-custom-emoji-input') || document.getElementById('smart-folder-emoji-input');
      // Limitación: Una carpeta inteligente siempre se ubica en el nivel raíz (reemplazar '/')
      const cleanName = (nameInput ? nameInput.value.trim().replace(/\//g, '-') : '');
      const chosenEmoji = (emojiInput ? emojiInput.value.trim() : '') || smartFolderModalState.emoji || '⚙️';

      if (!cleanName) {
        showToast('Escribe un nombre para la Carpeta Inteligente', '⚠️');
        if (nameInput) nameInput.focus();
        return;
      }

      if (isMasterAllNotesFolder(cleanName) || isTrashFolder(cleanName)) {
        showToast('Ese nombre está reservado por el sistema', '🔒');
        return;
      }

      if (!smartFolderModalState.rules.length) {
        showToast('Añade al menos una regla para la Carpeta Inteligente', '⚠️');
        return;
      }

      if (!state.smartFolders || typeof state.smartFolders !== 'object') {
        state.smartFolders = {};
      }
      if (!state.folderEmojis || typeof state.folderEmojis !== 'object') {
        state.folderEmojis = { ...DEFAULT_FOLDER_EMOJIS };
      }

      const oldName = smartFolderModalState.mode === 'edit' ? smartFolderModalState.targetFolder : null;
      if (oldName && oldName !== cleanName && state.folders.some(f => f.toLowerCase() === cleanName.toLowerCase())) {
        showToast(`Ya existe una carpeta llamada "${cleanName}"`, '⚠️');
        return;
      }
      if (!oldName && state.folders.some(f => f.toLowerCase() === cleanName.toLowerCase()) && !isSmartFolder(cleanName)) {
        showToast(`Ya existe una carpeta estándar llamada "${cleanName}". Usa la opción de convertirla en inteligente.`, '⚠️');
        return;
      }

      if (oldName && oldName !== cleanName) {
        state.folders = state.folders.map(f => (f === oldName ? cleanName : f));
        delete state.smartFolders[oldName];
        delete state.folderEmojis[oldName];
      } else if (!state.folders.includes(cleanName)) {
        state.folders.push(cleanName);
      }

      const rulesCopy = JSON.parse(JSON.stringify(smartFolderModalState.rules));
      const matchMode = smartFolderModalState.matchMode === 'any' ? 'any' : 'all';

      state.smartFolders[cleanName] = {
        matchMode: matchMode,
        rules: rulesCopy
      };
      state.folderEmojis[cleanName] = chosenEmoji;

      state.selectedFolder = cleanName;
      state.selectedCollection = 'FOLDER';

      // Persistir de forma atómica y directa en la base de datos SQLite (Peewee ORM)
      const persistDirectToDB = async () => {
        try {
          if (hasPyWebViewBridge() && typeof window.pywebview.api.save_smart_folder === 'function') {
            await window.pywebview.api.save_smart_folder(cleanName, rulesCopy, matchMode, chosenEmoji, oldName);
          } else {
            await fetch('/api/smart-folders/save', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                name: cleanName,
                rules: rulesCopy,
                matchMode: matchMode,
                emoji: chosenEmoji,
                oldName: oldName
              })
            });
          }
        } catch (e) {
          console.warn('Persistencia directa de Carpeta Inteligente en SQLite:', e);
        }
      };
      persistDirectToDB();

      saveFoldersToBackend();
      renderFolders();
      renderNotesList();
      if (state.isHomeActive) {
        renderHomePage();
      }
      closeSmartFolderModal();
      showToast(
        smartFolderModalState.mode === 'edit'
          ? `Carpeta Inteligente "${chosenEmoji} ${cleanName}" actualizada en la base de datos`
          : `Carpeta Inteligente "${chosenEmoji} ${cleanName}" guardada en la base de datos`,
        chosenEmoji
      );
    }

    /* Conversión Irreversible de Carpeta Estándar a Carpeta Inteligente */
    function openConvertStandardToSmartModal(folderName) {
      closeCustomContextMenu();
      closeFolderModal();
      if (!folderName || isMasterAllNotesFolder(folderName) || isTrashFolder(folderName)) return;
      if (isSmartFolder(folderName)) {
        openSmartFolderModal('edit', folderName);
        return;
      }

      pendingSmartConvertFolderName = folderName;
      const modal = document.getElementById('smart-folder-convert-modal');
      const bodyEl = document.getElementById('smart-folder-convert-body');
      const descEl = document.getElementById('smart-convert-modal-desc');
      const tagPreviewEl = document.getElementById('smart-convert-tag-preview');
      if (!modal) return;

      const leafName = getFolderDisplayName(folderName);
      const generatedTag = leafName
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9_-]+/g, '-')
        .replace(/^-+|-+$/g, '') || 'carpeta';

      const prefix = folderName + '/';
      const affectedNotes = getActiveNotesList().filter(n => {
        const uFolders = getNoteUserFolders(n);
        return uFolders.some(f => f === folderName || f.startsWith(prefix));
      });

      if (bodyEl) {
        bodyEl.innerHTML = `
          <p style="margin:0 0 10px;">
            ¿Deseas convertir la carpeta estándar <strong>"${escapeHtmlAttr(folderName)}"</strong> (${affectedNotes.length} ${affectedNotes.length === 1 ? 'nota' : 'notas'}) en una <strong>Carpeta Inteligente</strong>?
          </p>
          <div class="smart-convert-warning-box">
            <div>• Las notas que contenía se moverán a la carpeta raíz <strong>"Todas Las Notas"</strong>.</div>
            <div>• Se les asignará automáticamente la etiqueta <span class="smart-convert-tag-chip">#${escapeHtmlAttr(generatedTag)}</span>.</div>
            <div>• <strong>Conversión irreversible:</strong> No hay un botón para deshacer el cambio automáticamente.</div>
          </div>
        `;
      }
      if (descEl) {
        descEl.innerHTML = `¿Deseas convertir la carpeta estándar <strong>"${escapeHtmlAttr(folderName)}"</strong> (${affectedNotes.length} ${affectedNotes.length === 1 ? 'nota' : 'notas'}) en una <strong>Carpeta Inteligente</strong>?`;
      }
      if (tagPreviewEl) {
        tagPreviewEl.textContent = '#' + generatedTag;
      }

      modal.classList.add('open');
    }

    function closeSmartFolderConvertModal() {
      const modal = document.getElementById('smart-folder-convert-modal');
      if (modal) modal.classList.remove('open');
      pendingSmartConvertFolderName = null;
    }

    function confirmConvertStandardToSmartFolder() {
      const folderName = pendingSmartConvertFolderName;
      closeSmartFolderConvertModal();
      if (!folderName || isMasterAllNotesFolder(folderName) || isTrashFolder(folderName)) return;

      const leafName = getFolderDisplayName(folderName);
      let rootSmartName = leafName;
      if (state.folders.some(f => f !== folderName && !f.startsWith(folderName + '/') && f.toLowerCase() === rootSmartName.toLowerCase())) {
        rootSmartName = `${leafName} (Inteligente)`;
      }

      const generatedTag = leafName
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9_-]+/g, '-')
        .replace(/^-+|-+$/g, '') || 'carpeta';

      const oldEmoji = getFolderEmoji(folderName);
      const prefix = folderName + '/';

      // 1. Mover las notas que contenía a la raíz ("Todas Las Notas") y asignarles la etiqueta #tag con el nombre de la carpeta anterior
      state.notes.forEach(n => {
        const userFolders = getNoteUserFolders(n);
        const wasInFolder = userFolders.some(f => f === folderName || f.startsWith(prefix));
        if (wasInFolder) {
          const remaining = userFolders.filter(f => f !== folderName && !f.startsWith(prefix));
          setNoteFolders(n, remaining);
          const currentTags = (n.tags || '')
            .split(',')
            .map(t => t.trim().replace(/^#/, ''))
            .filter(Boolean);
          if (!currentTags.some(t => t.toLowerCase() === generatedTag)) {
            currentTags.push(generatedTag);
            n.tags = currentTags.join(', ');
          }
          n.updatedAt = Date.now();
        }
      });

      // 2. Eliminar la carpeta estándar y sus subcarpetas, y crear la Carpeta Inteligente en la raíz
      state.folders = state.folders.filter(f => f !== folderName && !f.startsWith(prefix));
      if (!state.folders.includes(rootSmartName)) {
        state.folders.push(rootSmartName);
      }

      if (state.folderEmojis) {
        Object.keys(state.folderEmojis).forEach(k => {
          if (k === folderName || k.startsWith(prefix)) delete state.folderEmojis[k];
        });
      }
      state.folderEmojis[rootSmartName] = oldEmoji === '📁' ? '⚙️' : oldEmoji;

      if (!state.smartFolders || typeof state.smartFolders !== 'object') {
        state.smartFolders = {};
      }
      state.smartFolders[rootSmartName] = {
        matchMode: 'all',
        rules: [
          {
            id: 'sr-conv-' + Date.now(),
            type: 'tags',
            condition: 'any_selected',
            value: generatedTag
          }
        ]
      };

      state.selectedFolder = rootSmartName;
      state.selectedCollection = 'FOLDER';

      const convRules = [
        {
          id: 'sr-conv-' + Date.now(),
          type: 'tags',
          condition: 'any_selected',
          value: generatedTag
        }
      ];

      save();
      const persistConvToDB = async () => {
        try {
          if (hasPyWebViewBridge() && typeof window.pywebview.api.save_smart_folder === 'function') {
            await window.pywebview.api.save_smart_folder(rootSmartName, convRules, 'all', state.folderEmojis[rootSmartName] || '⚙️');
          } else {
            await fetch('/api/smart-folders/save', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                name: rootSmartName,
                rules: convRules,
                matchMode: 'all',
                emoji: state.folderEmojis[rootSmartName] || '⚙️'
              })
            });
          }
        } catch (_) {}
      };
      persistConvToDB();
      saveFoldersToBackend();
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      if (state.isHomeActive) {
        renderHomePage();
      } else {
        loadActiveNote();
      }

      showToast(`"${rootSmartName}" convertida en Carpeta Inteligente con #${generatedTag}`, '⚙️');
    }

    /* Acciones rápidas para probar filtros de notas compartidas y bloqueadas desde el menú contextual */
    function ctxToggleLockNote(noteId) {
      closeCustomContextMenu();
      const note = state.notes.find(n => n.id === Number(noteId));
      if (!note) return;
      note.isLocked = !note.isLocked;
      note.updatedAt = Date.now();
      save(false, note);
      renderFolders();
      renderNotesList();
      if (state.activeNoteId === note.id) loadActiveNote();
      showToast(note.isLocked ? `Nota "${note.title}" protegida con candado 🔒` : `Candado quitado de "${note.title}"`, note.isLocked ? '🔒' : '🔓');
    }

    function ctxToggleShareNote(noteId) {
      closeCustomContextMenu();
      const note = state.notes.find(n => n.id === Number(noteId));
      if (!note) return;
      if (note.isShared) {
        note.isShared = false;
        note.sharedWith = '';
        showToast(`Nota "${note.title}" dejó de compartirse`, '👤');
      } else {
        const who = prompt('Compartir nota con usuarios (ej. @ana, @carlos):', note.sharedWith || '@equipo');
        if (who === null) return;
        note.isShared = true;
        note.sharedWith = who.trim() || '@equipo';
        showToast(`Nota "${note.title}" compartida con ${note.sharedWith}`, '👥');
      }
      note.updatedAt = Date.now();
      save(false, note);
      renderFolders();
      renderNotesList();
      if (state.activeNoteId === note.id) loadActiveNote();
    }

    /* ============================================================================
       SISTEMA DE AJUSTES MULTISECCIÓN ESTILO NOTION & PERSONALIZACIÓN DE COLOR
       ============================================================================ */

    function getContrastColor(hex) {
      if (!hex || hex.length < 7) return '#090a0d';
      try {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
        return (yiq >= 150) ? '#090a0d' : '#ffffff';
      } catch (_) {
        return '#090a0d';
      }
    }

    function hexToRgba(hex, alpha) {
      if (!hex || hex.length < 7) return `rgba(245, 158, 11, ${alpha})`;
      try {
        const r = parseInt(hex.slice(1, 3), 16) || 0;
        const g = parseInt(hex.slice(3, 5), 16) || 0;
        const b = parseInt(hex.slice(5, 7), 16) || 0;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
      } catch (_) {
        return `rgba(245, 158, 11, ${alpha})`;
      }
    }

    function detectSystemAccentColor() {
      try {
        const testDiv = document.createElement('div');
        testDiv.style.color = 'AccentColor';
        testDiv.style.display = 'none';
        document.body.appendChild(testDiv);
        const comp = window.getComputedStyle(testDiv).color;
        document.body.removeChild(testDiv);
        if (comp && comp.startsWith('rgb')) {
          const match = comp.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
          if (match) {
            const r = parseInt(match[1]);
            const g = parseInt(match[2]);
            const b = parseInt(match[3]);
            return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
          }
        }
      } catch (_) {}
      return '#0078d4'; // Fallback a azul característico de Windows 11 Fluent
    }

    function saveSettingsPayload(payload) {
      if (!state.settings) state.settings = {};
      Object.assign(state.settings, payload);
      try {
        localStorage.setItem('notejs_settings_cache', JSON.stringify(state.settings));
      } catch (_) {}

      if (hasPyWebViewBridge() && typeof window.pywebview.api.save_settings === "function") {
        window.pywebview.api.save_settings(payload).catch(() => {});
      } else {
        fetch("/api/settings", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        }).catch(() => {});
      }
    }

    function applyAccentColor(mode, customHex, persist = true) {
      state.accentColorMode = mode || 'default';
      let hex = '#f59e0b'; // por defecto amarillo Apple Notes
      if (state.accentColorMode === 'system') {
        hex = detectSystemAccentColor();
      } else if (state.accentColorMode === 'custom' && customHex) {
        hex = customHex;
        state.customAccentColor = customHex;
      }

      const root = document.documentElement;
      root.style.setProperty('--accent-amber', hex);
      root.style.setProperty('--accent-amber-soft', hexToRgba(hex, 0.14));
      root.style.setProperty('--accent-amber-border', hexToRgba(hex, 0.38));
      root.style.setProperty('--btn-amber-fg', getContrastColor(hex));
      root.style.setProperty('--app-accent-color', hex);

      if (persist) {
        saveSettingsPayload({
          accentColorMode: state.accentColorMode,
          customAccentColor: hex
        });
      }
    }

    function selectAccentMode(mode) {
      let hex = '#f59e0b';
      if (mode === 'system') {
        hex = detectSystemAccentColor();
      } else if (mode === 'custom') {
        hex = state.customAccentColor || '#8b5cf6';
      }
      applyAccentColor(mode, hex, true);
      updateAccentColorUI();
      const label = mode === 'default' ? 'Amarillo por defecto' : (mode === 'system' ? 'Colores del Sistema (Windows 11)' : 'Personalizado');
      showToast(`Color aplicado: ${label}`, '🎨');
    }

    function pickCustomColor(hex) {
      if (!hex || !/^#[0-9a-fA-F]{6}$/.test(hex)) return;
      state.customAccentColor = hex;
      applyAccentColor('custom', hex, true);
      updateAccentColorUI();
    }

    function updateAccentColorUI() {
      const mode = state.accentColorMode || 'default';
      const customHex = state.customAccentColor || (mode === 'system' ? detectSystemAccentColor() : '#f59e0b');

      const btnDef = document.getElementById('btn-colormode-default');
      const btnSys = document.getElementById('btn-colormode-system');
      const btnCus = document.getElementById('btn-colormode-custom');
      if (btnDef) btnDef.classList.toggle('active', mode === 'default');
      if (btnSys) btnSys.classList.toggle('active', mode === 'system');
      if (btnCus) btnCus.classList.toggle('active', mode === 'custom');

      const indicator = document.getElementById('custom-color-indicator');
      if (indicator) indicator.style.background = customHex;

      const colorInput = document.getElementById('notion-color-input');
      if (colorInput) colorInput.value = customHex;

      const hexText = document.getElementById('notion-color-hex-text');
      if (hexText) hexText.value = customHex.toUpperCase();

      document.querySelectorAll('.notion-swatch').forEach(sw => {
        const swColor = sw.style.getPropertyValue('--c').trim().toLowerCase();
        sw.classList.toggle('active', swColor === customHex.toLowerCase());
      });
    }

    function applyThemeMode(mode, persist = true) {
      state.themeMode = mode || 'system';
      if (state.themeMode === 'system') {
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        state.isLightMode = !prefersDark;
      } else {
        state.isLightMode = (state.themeMode === 'light');
      }
      document.body.classList.toggle('light-mode', state.isLightMode);
      if (persist) {
        saveSettingsPayload({
          themeMode: state.themeMode,
          isLightMode: String(state.isLightMode)
        });
      }
    }

    function toggleTheme() {
      state.isLightMode = !state.isLightMode;
      state.themeMode = state.isLightMode ? 'light' : 'dark';
      document.body.classList.toggle('light-mode', state.isLightMode);
      saveSettingsPayload({
        themeMode: state.themeMode,
        isLightMode: String(state.isLightMode)
      });
      const themeSelect = document.getElementById('setting-theme-select');
      if (themeSelect) themeSelect.value = state.themeMode;
      showToast(state.isLightMode ? 'Tema Claro activado' : 'Tema Oscuro activado', '🌓');
    }

    function handleThemeSelectChange(value) {
      applyThemeMode(value, true);
    }

    function handleContrastSelectChange(value) {
      state.highContrast = (value === 'high');
      document.body.classList.toggle('high-contrast-mode', state.highContrast);
      saveSettingsPayload({
        highContrast: String(state.highContrast)
      });
    }

    function handleEnterBlockToggle(checked) {
      state.enterCreatesBlock = checked;
      saveSettingsPayload({
        enterCreatesBlock: String(checked)
      });
    }

    function handleWordCountToggle(checked) {
      state.showWordCount = checked;
      const countBar = document.getElementById('editor-word-count-bar');
      if (countBar) countBar.style.display = checked ? 'flex' : 'none';
      saveSettingsPayload({
        showWordCount: String(checked)
      });
    }

    function handleLanguageChange(lang) {
      state.language = lang;
      saveSettingsPayload({
        language: lang
      });
      showToast(`Idioma guardado: ${lang === 'es' ? 'Español' : 'English'}`, '🌐');
    }

    function handleTextDirectionToggle(checked) {
      const canvas = document.getElementById('rich-editor-canvas');
      if (canvas) {
        canvas.setAttribute('dir', checked ? 'rtl' : 'ltr');
      }
    }

    function handleKatexToggle(checked) {
      state.enableKatex = checked;
      saveSettingsPayload({
        enableKatex: String(checked)
      });
      showToast(`Fórmulas KaTeX: ${checked ? 'Activadas' : 'Desactivadas'}`, '∑');
    }

    function optimizeLocalDatabase() {
      showToast('Optimizando base de datos SQLite (VACUUM)...', '⚡');
      if (hasPyWebViewBridge() && typeof window.pywebview.api.bootstrap === "function") {
        window.pywebview.api.bootstrap().then(() => {
          showToast('Base de datos SQLite optimizada con éxito', '✅');
        }).catch(() => {
          showToast('Optimización completada', '✅');
        });
      } else {
        fetch('/api/bootstrap').then(() => {
          showToast('Base de datos SQLite optimizada con éxito', '✅');
        }).catch(() => {
          showToast('Optimización completada', '✅');
        });
      }
    }

    function switchSettingsSection(sectionId) {
      const navItems = document.querySelectorAll('.notion-nav-item');
      navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.section === sectionId);
      });
      const panes = document.querySelectorAll('.notion-section-pane');
      panes.forEach(pane => {
        pane.classList.toggle('active', pane.id === `notion-sec-${sectionId}`);
      });
    }

    function filterSettingsSections(query) {
      const q = String(query || '').toLowerCase().trim();
      const rows = document.querySelectorAll('.notion-setting-row');
      if (!q) {
        rows.forEach(r => r.style.display = '');
        const groups = document.querySelectorAll('.notion-settings-group');
        groups.forEach(g => g.style.display = '');
        return;
      }
      let firstMatchSection = null;
      rows.forEach(r => {
        const keys = (r.dataset.searchKeys || '') + ' ' + (r.textContent || '');
        const match = keys.toLowerCase().includes(q);
        r.style.display = match ? 'flex' : 'none';
        if (match && !firstMatchSection) {
          const pane = r.closest('.notion-section-pane');
          if (pane) {
            firstMatchSection = pane.id.replace('notion-sec-', '');
          }
        }
      });
      if (firstMatchSection) {
        switchSettingsSection(firstMatchSection);
      }
    }

    function handleStartupBehaviorChange(value) {
      const cleanVal = (value === 'resume') ? 'resume' : 'clean';
      state.startupBehavior = cleanVal;
      saveSettingsPayload({ startupBehavior: cleanVal });
      showToast(cleanVal === 'clean' ? 'Inicio: Iniciar siempre de cero' : 'Inicio: Reanudar en la última nota visitada', '⚙️');
    }

    function openSettingsModal() {
      const modal = document.getElementById('settings-modal');
      if (!modal) return;
      modal.classList.add('open');

      const startupSelect = document.getElementById('setting-startup-behavior');
      if (startupSelect) {
        startupSelect.value = state.startupBehavior || (state.settings && state.settings.startupBehavior) || 'clean';
      }

      const themeSelect = document.getElementById('setting-theme-select');
      if (themeSelect) themeSelect.value = state.themeMode || (state.isLightMode ? 'light' : 'dark');

      const contrastSelect = document.getElementById('setting-contrast-select');
      if (contrastSelect) contrastSelect.value = state.highContrast ? 'high' : 'off';

      const summary = document.getElementById('settings-account-summary');
      if (summary) {
        const activeNotes = getActiveNotesList();
        const trashedNotes = getTrashedNotesList();
        summary.textContent = `${activeNotes.length} notas activas · ${state.folders.length} carpetas · ${trashedNotes.length} en papelera`;
      }

      updateAccentColorUI();
    }

    function closeSettingsModal() {
      const modal = document.getElementById('settings-modal');
      if (modal) modal.classList.remove('open');
    }

    /* Control del Menú Desplegable "+ Insertar" */
    function toggleInsertDropdown(e) {
      if (e) {
        e.stopPropagation();
      }
      const dropdown = document.getElementById('insert-blocks-dropdown');
      const btn = document.getElementById('btn-insert-dropdown');
      if (!dropdown) return;

      const willOpen = !dropdown.classList.contains('open');
      if (willOpen) {
        // Guardar posición del cursor en el editor antes de abrir el menú
        const sel = window.getSelection();
        const canvas = document.getElementById('rich-editor-canvas');
        if (sel && sel.rangeCount > 0 && canvas && canvas.contains(sel.anchorNode)) {
          savedEditorRange = sel.getRangeAt(0).cloneRange();
          savedSelectionRange = sel.getRangeAt(0).cloneRange();
        }
      }

      dropdown.classList.toggle('open', willOpen);
      if (btn) btn.classList.toggle('active', willOpen);
    }

    function closeInsertDropdown() {
      const dropdown = document.getElementById('insert-blocks-dropdown');
      const btn = document.getElementById('btn-insert-dropdown');
      if (dropdown) dropdown.classList.remove('open');
      if (btn) btn.classList.remove('active');
    }

    /* ============================================================================
       MENÚ CONTEXTUAL DE CLIC DERECHO PARA TODOS LOS CUADROS, TARJETAS Y BLOQUES
       ============================================================================ */
    let activeCtxTargetEl = null;
    let activeCtxEmbeddedCard = null;

    function closeCustomContextMenu() {
      const menu = document.getElementById('custom-context-menu');
      if (menu) {
        menu.classList.remove('open');
        menu.setAttribute('aria-hidden', 'true');
      }
      if (activeCtxTargetEl) {
        activeCtxTargetEl.classList.remove('ctx-target-highlight');
        activeCtxTargetEl = null;
      }
    }

    function positionContextMenu(menu, clientX, clientY) {
      menu.style.left = '0px';
      menu.style.top = '0px';
      menu.classList.add('open');
      menu.setAttribute('aria-hidden', 'false');

      const rect = menu.getBoundingClientRect();
      const pad = 10;
      let x = clientX;
      let y = clientY;

      if (x + rect.width > window.innerWidth - pad) {
        x = Math.max(pad, window.innerWidth - rect.width - pad);
      }
      if (y + rect.height > window.innerHeight - pad) {
        y = Math.max(pad, window.innerHeight - rect.height - pad);
      }

      menu.style.left = `${x}px`;
      menu.style.top = `${y}px`;
    }

    function openCustomContextMenu(clientX, clientY, targetEl, htmlContent) {
      closeCustomContextMenu();
      const menu = document.getElementById('custom-context-menu');
      if (!menu) return;

      if (targetEl) {
        activeCtxTargetEl = targetEl;
        targetEl.classList.add('ctx-target-highlight');
      }

      menu.innerHTML = htmlContent;
      positionContextMenu(menu, clientX, clientY);
    }

    /* Acciones Contextuales para Cuadros de Notas (.note-item-card) */
    function ctxDuplicateNote(noteId) {
      closeCustomContextMenu();
      const orig = state.notes.find(n => n.id === Number(noteId));
      if (!orig) return;

      const copy = JSON.parse(JSON.stringify(orig));
      copy.id = Date.now();
      copy.title = `${orig.title || 'Sin título'} (Copia)`;
      copy.updatedAt = Date.now();

      const idx = state.notes.findIndex(n => n.id === Number(noteId));
      state.notes.splice(idx + 1, 0, copy);
      state.activeNoteId = copy.id;
      if (!Array.isArray(state.openTabIds)) state.openTabIds = [];
      const tabOrigIdx = state.openTabIds.indexOf(Number(noteId));
      if (tabOrigIdx !== -1) {
        state.openTabIds.splice(tabOrigIdx + 1, 0, copy.id);
      } else {
        state.openTabIds.push(copy.id);
      }
      saveOpenTabsState();
      save(false, copy);
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      loadActiveNote();
      showToast(`Cuadro "${orig.title}" duplicado en nueva pestaña`, '📑');
    }

    function ctxTogglePinNote(noteId) {
      closeCustomContextMenu();
      const note = state.notes.find(n => n.id === Number(noteId));
      if (!note) return;
      note.isPinned = !note.isPinned;
      note.updatedAt = Date.now();
      save(false, note);
      renderFolders();
      renderNotesList();
      renderNoteTabs();
      if (state.activeNoteId === note.id) loadActiveNote();
      showToast(note.isPinned ? 'Nota fijada arriba' : 'Nota desfijada', '📌');
    }

    function ctxRenameNote(noteId) {
      closeCustomContextMenu();
      const note = state.notes.find(n => n.id === Number(noteId));
      if (!note) return;
      const newTitle = prompt('Nuevo título para la nota:', note.title || '');
      if (newTitle !== null && newTitle.trim()) {
        note.title = newTitle.trim();
        note.updatedAt = Date.now();
        save(false, note);
        renderNotesList();
        renderNoteTabs();
        if (state.activeNoteId === note.id) loadActiveNote();
        showToast('Título actualizado', '✏️');
      }
    }

    function ctxCycleNoteEmoji(noteId) {
      closeCustomContextMenu();
      const note = state.notes.find(n => n.id === Number(noteId));
      if (!note) return;
      const curIdx = EMOJI_PALETTE.indexOf(note.emoji || '📝');
      note.emoji = EMOJI_PALETTE[(curIdx + 1) % EMOJI_PALETTE.length];
      note.updatedAt = Date.now();
      save(false, note);
      renderNotesList();
      renderNoteTabs();
      if (state.activeNoteId === note.id) loadActiveNote();
      showToast(`Icono cambiado a ${note.emoji}`, note.emoji);
    }

    function ctxSetNoteCardColor(noteId, colorKey) {
      closeCustomContextMenu();
      const note = state.notes.find(n => n.id === Number(noteId));
      if (!note) return;
      note.cardColor = colorKey || '';
      note.updatedAt = Date.now();
      save(false, note);
      renderNotesList();
      showToast(colorKey ? 'Color del cuadro actualizado' : 'Color del cuadro restablecido', '🎨');
    }

    function ctxMoveNoteStep(noteId, dir) {
      closeCustomContextMenu();
      const idx = state.notes.findIndex(n => n.id === Number(noteId));
      if (idx === -1) return;
      const targetIdx = idx + dir;
      if (targetIdx < 0 || targetIdx >= state.notes.length) return;
      const [moved] = state.notes.splice(idx, 1);
      state.notes.splice(targetIdx, 0, moved);
      save();
      renderNotesList();
      showToast('Posición del cuadro actualizada', '↕️');
    }

    function ctxCopyNoteContent(noteId) {
      closeCustomContextMenu();
      const note = state.notes.find(n => n.id === Number(noteId));
      if (!note) return;
      const plain = (note.content || '').replace(/<[^>]*>?/gm, '').trim();
      const textToCopy = `${note.emoji || '📝'} ${note.title || 'Sin título'}\n\n${plain}`;
      navigator.clipboard.writeText(textToCopy).then(() => {
        showToast('Contenido de la nota copiado al portapapeles', '📋');
      });
    }

    function ctxEmbedNoteIntoActive(noteId) {
      closeCustomContextMenu();
      insertNoteCardAtSelection(Number(noteId));
    }

    /* Acciones Contextuales para Cuadros Incrustados (.note-embedded-card) */
    function ctxOpenEmbeddedCard(noteId) {
      closeCustomContextMenu();
      selectNote(Number(noteId));
    }

    function ctxChangeEmbeddedCardCover(presetIdx) {
      const card = activeCtxEmbeddedCard;
      closeCustomContextMenu();
      if (!card) return;
      const bg = COVER_PRESETS[presetIdx % COVER_PRESETS.length];
      card.style.background = bg;
      const targetId = Number(card.getAttribute('data-note-id'));
      const targetNote = state.notes.find(n => n.id === targetId);
      if (targetNote) {
        targetNote.hasCover = true;
        targetNote.coverStyle = bg;
        save(false, targetNote);
      }
      syncRichEditor();
      showToast('Portada del cuadro actualizada', '🎨');
    }

    function ctxDuplicateEmbeddedCard() {
      const card = activeCtxEmbeddedCard;
      closeCustomContextMenu();
      if (!card) return;
      const clone = card.cloneNode(true);
      clone.classList.remove('ctx-target-highlight');
      card.after(clone);
      syncRichEditor();
      showToast('Cuadro incrustado duplicado', '📑');
    }

    function ctxRemoveEmbeddedCard() {
      const card = activeCtxEmbeddedCard;
      closeCustomContextMenu();
      if (!card) return;
      card.remove();
      syncRichEditor();
      showToast('Cuadro eliminado del documento', '🗑');
    }

    /* Acciones Contextuales para Tarjetas Kanban (.kanban-card) */
    function ctxEditKanbanCard(identifier) {
      closeCustomContextMenu();
      const note = getActiveNote();
      if (!note || !note.kanban) return;
      const card = note.kanban.find(c => c.id === identifier || c.text === identifier);
      if (!card) return;
      openKanbanCardModal(card.id);
    }

    function ctxDuplicateKanbanCard(identifier) {
      closeCustomContextMenu();
      const note = getActiveNote();
      if (!note || !note.kanban) return;
      const idx = note.kanban.findIndex(c => c.id === identifier || c.text === identifier);
      if (idx === -1) return;
      const orig = note.kanban[idx];
      note.kanban.splice(idx + 1, 0, {
        id: 'kc-' + Date.now() + '-' + Math.random().toString(36).substr(2, 6),
        text: `${orig.text} (copia)`,
        status: orig.status,
        category: orig.category || 'General',
        assignee: orig.assignee || 'Sin Asignar',
        priority: orig.priority || 'Media'
      });
      save();
      renderKanban(note);
      showToast('Tarea Kanban duplicada', '📑');
    }

    /* Acciones Contextuales para Filas de la Tabla de Propiedades (#block-table tr) */
    function ctxInsertTableRowAt(idx, placeAbove) {
      closeCustomContextMenu();
      const note = getActiveNote();
      if (!note) return;
      note.tableRows = note.tableRows || [];
      const insertPos = placeAbove ? idx : idx + 1;
      note.tableRows.splice(insertPos, 0, {
        name: "Nuevo ítem",
        status: "Pendiente",
        category: "General",
        date: new Date().toLocaleDateString('es-ES', { day: '2-digit', month: 'short' }),
        amount: 100
      });
      save();
      renderTable(note);
      showToast(placeAbove ? 'Fila insertada arriba' : 'Fila insertada abajo', '➕');
    }

    function ctxDuplicateTableRow(idx) {
      closeCustomContextMenu();
      const note = getActiveNote();
      if (!note || !note.tableRows || !note.tableRows[idx]) return;
      const copy = JSON.parse(JSON.stringify(note.tableRows[idx]));
      copy.name = `${copy.name} (Copia)`;
      note.tableRows.splice(idx + 1, 0, copy);
      save();
      renderTable(note);
      showToast('Fila de tabla duplicada', '📑');
    }

    function ctxSetTableRowStatus(idx, newStatus) {
      closeCustomContextMenu();
      const note = getActiveNote();
      if (!note || !note.tableRows || !note.tableRows[idx]) return;
      note.tableRows[idx].status = newStatus;
      save();
      renderTable(note);
      showToast(`Estado cambiado a "${newStatus}"`, '✅');
    }

    /* Acciones Contextuales para Cuadros de Bloques Notion (#block-*) */
    function ctxSetCalloutColor(colorKey) {
      closeCustomContextMenu();
      const note = getActiveNote();
      if (!note) return;
      note.calloutColor = colorKey;
      save();
      loadActiveNote();
      showToast('Color del cuadro Callout actualizado', '🎨');
    }

    function ctxMarkAllChecklists(doneState) {
      closeCustomContextMenu();
      const note = getActiveNote();
      if (!note || !note.checklists) return;
      note.checklists.forEach(item => { item.done = doneState; });
      save();
      renderChecklists(note);
      showToast(doneState ? 'Todas las tareas marcadas' : 'Tareas desmarcadas', '☑️');
    }

    function ctxClearCompletedChecklists() {
      closeCustomContextMenu();
      const note = getActiveNote();
      if (!note || !note.checklists) return;
      note.checklists = note.checklists.filter(item => !item.done);
      if (!note.checklists.length) note.showChecklist = false;
      save();
      loadActiveNote();
      showToast('Tareas completadas eliminadas', '🧹');
    }

    function ctxDuplicateChecklistItem(idx) {
      closeCustomContextMenu();
      const note = getActiveNote();
      if (!note || !note.checklists || !note.checklists[idx]) return;
      const orig = note.checklists[idx];
      note.checklists.splice(idx + 1, 0, { text: orig.text, done: orig.done });
      save();
      renderChecklists(note);
      showToast('Tarea duplicada', '📑');
    }

    /* Acciones Contextuales para Carpetas (.folder-item[data-folder]) */
    function ctxCreateNoteInFolder(folderName) {
      closeCustomContextMenu();
      createNewNote(folderName);
    }

    function ctxRenameFolder(oldName) {
      closeCustomContextMenu();
      if (isMasterAllNotesFolder(oldName)) {
        showToast('La carpeta principal "Todas Las Notas" no puede cambiar de nombre', '🔒');
        return;
      }
      if (isSmartFolder(oldName)) {
        openSmartFolderModal('edit', oldName);
        return;
      }
      openFolderModal('edit', oldName);
    }

    function ctxDeleteFolder(folderName) {
      closeCustomContextMenu();
      if (isMasterAllNotesFolder(folderName)) {
        showToast('La carpeta principal "Todas Las Notas" no se puede eliminar', '🔒');
        return;
      }
      const wasSmart = isSmartFolder(folderName);
      const prefix = folderName + '/';
      state.folders = state.folders.filter(f => f !== folderName && !f.startsWith(prefix));
      if (state.folderEmojis) {
        Object.keys(state.folderEmojis).forEach(k => {
          if (k === folderName || k.startsWith(prefix)) {
            delete state.folderEmojis[k];
          }
        });
      }
      if (state.smartFolders && state.smartFolders[folderName]) {
        delete state.smartFolders[folderName];
      }
      if (!wasSmart) {
        state.notes.forEach(n => {
          const remaining = getNoteUserFolders(n).filter(f => f !== folderName && !f.startsWith(prefix));
          setNoteFolders(n, remaining);
        });
      }
      if (state.selectedFolder === folderName || (state.selectedFolder && state.selectedFolder.startsWith(prefix))) {
        selectFolder(MASTER_ALL_NOTES_FOLDER);
      }
      save();
      if (wasSmart) {
        const deleteDirectFromDB = async () => {
          try {
            if (hasPyWebViewBridge() && typeof window.pywebview.api.delete_smart_folder === 'function') {
              await window.pywebview.api.delete_smart_folder(folderName);
            } else {
              await fetch('/api/smart-folders/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: folderName })
              });
            }
          } catch (e) {
            console.warn('Eliminación directa de carpeta inteligente en SQLite:', e);
          }
        };
        deleteDirectFromDB();
      }
      saveFoldersToBackend();
      renderFolders();
      renderNotesList();
      if (state.isHomeActive) {
        renderHomePage();
      } else {
        loadActiveNote();
      }
      if (wasSmart) {
        showToast(`Carpeta Inteligente "${folderName}" eliminada (tus notas originales siguen intactas)`, '⚙️');
      } else {
        showToast(`Carpeta "${folderName}" eliminada`, '🗑');
      }
    }

    /* Detector Global de Clic Derecho (contextmenu) sobre todos los Cuadros */
    document.addEventListener('contextmenu', function(e) {
      // -1. Pestaña de Nota en la Barra Superior (.note-tab-item[data-tab-note-id])
      const noteTabEl = e.target.closest('.note-tab-item[data-tab-note-id]');
      if (noteTabEl) {
        e.preventDefault();
        e.stopPropagation();
        const noteId = Number(noteTabEl.getAttribute('data-tab-note-id'));
        const note = state.notes.find(n => n.id === noteId);
        if (!note) return;
        const tabIdx = state.openTabIds.indexOf(noteId);
        const hasRightTabs = tabIdx !== -1 && tabIdx < state.openTabIds.length - 1;
        const hasOtherTabs = state.openTabIds.length > 1;

        const html = `
          <div class="ctx-menu-header">
            <span>${note.emoji || '📝'} ${note.title || 'Sin título'}</span>
            <span class="ctx-menu-header-sub">Pestaña</span>
          </div>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); createNewNote();">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">➕</span><span class="ctx-menu-label">Nueva nota en pestaña</span></span>
            <span class="ctx-menu-kbd">${getShortcutDisplayCombo('new_note')}</span>
          </button>
          <button class="ctx-menu-item" onclick="ctxDuplicateNote(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📑</span><span class="ctx-menu-label">Duplicar nota en pestaña</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxRenameNote(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✏️</span><span class="ctx-menu-label">Renombrar título</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxTogglePinNote(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📌</span><span class="ctx-menu-label">${note.isPinned ? 'Desfijar nota' : 'Fijar nota'}</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); closeNoteTab(${noteId});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✕</span><span class="ctx-menu-label">Cerrar pestaña</span></span>
            <span class="ctx-menu-kbd">${getShortcutDisplayCombo('close_tab')}</span>
          </button>
          ${hasOtherTabs ? `
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); closeOtherNoteTabs(${noteId});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗂️</span><span class="ctx-menu-label">Cerrar las demás pestañas</span></span>
          </button>` : ''}
          ${hasRightTabs ? `
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); closeRightNoteTabs(${noteId});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">➡️</span><span class="ctx-menu-label">Cerrar pestañas a la derecha</span></span>
          </button>` : ''}
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); closeAllNoteTabs();">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🏠</span><span class="ctx-menu-label">Cerrar todas las pestañas (Ir a Inicio)</span></span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, noteTabEl, html);
        return;
      }

      // 0. Bloque de Imagen Redimensionable en el Editor (.note-image-block)
      const imageBlock = e.target.closest('.note-image-block');
      if (imageBlock) {
        e.preventDefault();
        e.stopPropagation();
        activeCtxImageBlock = imageBlock;
        const curWidth = imageBlock.getAttribute('data-width') || '75%';
        const curAlign = imageBlock.getAttribute('data-align') || 'center';
        const captionText = imageBlock.querySelector('.note-image-caption')?.getAttribute('data-caption') || '';

        const html = `
          <div class="ctx-menu-header">
            <span>🖼️ Bloque de Imagen (${curWidth})</span>
            <span class="ctx-menu-header-sub">Redimensionable</span>
          </div>
          <button class="ctx-menu-item" onclick="ctxZoomImageBlock()">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🔍</span><span class="ctx-menu-label">Ver a tamaño completo (Lightbox)</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxEditImageBlockInModal()">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🔗</span><span class="ctx-menu-label">Cambiar URL / ruta o propiedades</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxPromptImageCaption()">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✏️</span><span class="ctx-menu-label">${captionText ? 'Editar pie de imagen' : 'Añadir pie de imagen'}</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxDuplicateImageBlock()">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📑</span><span class="ctx-menu-label">Duplicar bloque de imagen</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <div class="ctx-menu-section-label">Redimensionar ancho rápido</div>
          <div class="ctx-menu-chips-row">
            ${['25%', '50%', '75%', '100%'].map(w => `<button class="ctx-menu-chip ${curWidth === w ? 'active' : ''}" onclick="ctxSetImageBlockWidth('${w}')">${w}</button>`).join('')}
          </div>
          <div class="ctx-menu-section-label">Alineación en el documento</div>
          <div class="ctx-menu-chips-row">
            <button class="ctx-menu-chip ${curAlign === 'left' ? 'active' : ''}" onclick="ctxSetImageBlockAlign('left')">⬅ Izquierda</button>
            <button class="ctx-menu-chip ${curAlign === 'center' ? 'active' : ''}" onclick="ctxSetImageBlockAlign('center')">⬌ Centro</button>
            <button class="ctx-menu-chip ${curAlign === 'right' ? 'active' : ''}" onclick="ctxSetImageBlockAlign('right')">➡ Derecha</button>
          </div>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item danger" onclick="ctxDeleteImageBlock()">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗑</span><span class="ctx-menu-label">Eliminar imagen del documento</span></span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, imageBlock, html);
        return;
      }

      // 1. Cuadro de Nota Incrustada en el Editor (.note-embedded-card)
      const embeddedCard = e.target.closest('.note-embedded-card');
      if (embeddedCard) {
        e.preventDefault();
        e.stopPropagation();
        activeCtxEmbeddedCard = embeddedCard;
        const noteId = Number(embeddedCard.getAttribute('data-note-id'));
        const targetNote = state.notes.find(n => n.id === noteId);
        const title = targetNote ? (targetNote.title || 'Sin título') : 'Nota incrustada';

        const html = `
          <div class="ctx-menu-header">
            <span>🎴 ${title}</span>
            <span class="ctx-menu-header-sub">Acceso</span>
          </div>
          <button class="ctx-menu-item" onclick="ctxOpenEmbeddedCard(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">↗</span><span class="ctx-menu-label">Abrir nota vinculada</span></span>
          </button>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); openNoteInBackgroundTab(${noteId});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗂️</span><span class="ctx-menu-label">Abrir en pestaña en segundo plano</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxCycleNoteEmoji(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">😀</span><span class="ctx-menu-label">Cambiar icono emoji</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxDuplicateEmbeddedCard()">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📑</span><span class="ctx-menu-label">Duplicar cuadro aquí</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxCopyNoteContent(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📋</span><span class="ctx-menu-label">Copiar contenido de la nota</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <div class="ctx-menu-section-label">Cambiar portada del cuadro</div>
          <div class="ctx-color-dot-row">
            ${COVER_PRESETS.map((bg, i) => `<button class="ctx-color-dot" style="background:${bg};" onclick="ctxChangeEmbeddedCardCover(${i})" title="Portada ${i + 1}"></button>`).join('')}
          </div>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item danger" onclick="ctxRemoveEmbeddedCard()">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗑</span><span class="ctx-menu-label">Quitar cuadro del documento</span></span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, embeddedCard, html);
        return;
      }

      // 2. Cuadro de Nota en la Galería / Lista o Cuadrícula (.note-item-card)
      const noteCard = e.target.closest('.note-item-card[data-note-id]');
      if (noteCard) {
        e.preventDefault();
        e.stopPropagation();
        const noteId = Number(noteCard.getAttribute('data-note-id'));
        const note = state.notes.find(n => n.id === noteId);
        if (!note) return;

        if (note.isTrashed) {
          const html = `
            <div class="ctx-menu-header">
              <span>🗑️ ${note.emoji || '📝'} ${note.title || 'Sin título'}</span>
              <span class="ctx-menu-header-sub">En papelera</span>
            </div>
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); restoreNoteFromTrash(${noteId});">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">↺</span><span class="ctx-menu-label">Restaurar nota</span></span>
            </button>
            <div class="ctx-menu-divider"></div>
            <button class="ctx-menu-item danger" onclick="closeCustomContextMenu(); permanentlyDeleteNoteById(${noteId});">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✕</span><span class="ctx-menu-label">Eliminar definitivamente</span></span>
            </button>
          `;
          openCustomContextMenu(e.clientX, e.clientY, noteCard, html);
          return;
        }

        const assignedFolders = getNoteFolders(note);
        const folderChips = state.folders.filter(f => !isSmartFolder(f)).map(f => {
          const isMaster = isMasterAllNotesFolder(f);
          const isAssigned = isMaster || assignedFolders.includes(f);
          const safeFolder = f.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
          return `<button class="ctx-menu-chip ${isAssigned ? 'active' : ''}" onclick="closeCustomContextMenu(); toggleNoteFolderMembership(${noteId}, '${safeFolder}')" title="${isMaster ? 'Siempre pertenece a Todas Las Notas' : 'Clic para añadir o quitar de esta carpeta'}">${isAssigned ? '✓ ' : ''}${getFolderEmoji(f)} ${f}</button>`;
        }).join('');

        const canEmbed = state.activeNoteId !== noteId;

        const html = `
          <div class="ctx-menu-header">
            <span>${note.emoji || '📝'} ${note.title || 'Sin título'}</span>
          </div>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); selectNote(${noteId});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📖</span><span class="ctx-menu-label">Abrir nota en pestaña</span></span>
            <span class="ctx-menu-kbd">Enter</span>
          </button>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); openNoteInBackgroundTab(${noteId});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗂️</span><span class="ctx-menu-label">Abrir en pestaña en segundo plano</span></span>
            <span class="ctx-menu-kbd">Ctrl+Clic</span>
          </button>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); selectNote(${noteId}); toggleHistoryPanel(true);">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🕒</span><span class="ctx-menu-label">Historial de ediciones (SQLite)</span></span>
            <span class="ctx-menu-kbd">${getShortcutDisplayCombo('toggle_history')}</span>
          </button>
          <button class="ctx-menu-item" onclick="ctxTogglePinNote(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📌</span><span class="ctx-menu-label">${note.isPinned ? 'Desfijar nota' : 'Fijar nota arriba'}</span></span>
            <span class="ctx-menu-kbd">${getShortcutDisplayCombo('pin_note')}</span>
          </button>
          <button class="ctx-menu-item" onclick="ctxToggleLockNote(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">${note.isLocked ? '🔓' : '🔒'}</span><span class="ctx-menu-label">${note.isLocked ? 'Quitar bloqueo de nota' : 'Bloquear / Proteger nota'}</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxToggleShareNote(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">👥</span><span class="ctx-menu-label">${note.isShared ? `Compartida (${note.sharedWith || '@equipo'}) · Dejar de compartir` : 'Compartir nota con @usuario...'}</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxDuplicateNote(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📑</span><span class="ctx-menu-label">Duplicar cuadro de nota</span></span>
            <span class="ctx-menu-kbd">${getShortcutDisplayCombo('duplicate_note')}</span>
          </button>
          ${canEmbed ? `
          <button class="ctx-menu-item" onclick="ctxEmbedNoteIntoActive(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🔗</span><span class="ctx-menu-label">Incrustar en la nota actual</span></span>
            <span class="ctx-menu-kbd">${getShortcutDisplayCombo('embed_note')}</span>
          </button>` : ''}
          <button class="ctx-menu-item" onclick="ctxRenameNote(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✏️</span><span class="ctx-menu-label">Renombrar título</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxCycleNoteEmoji(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">😀</span><span class="ctx-menu-label">Cambiar icono (${note.emoji || '📝'})</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxCopyNoteContent(${noteId})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📋</span><span class="ctx-menu-label">Copiar texto al portapapeles</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <div class="ctx-menu-section-label">Color del cuadro</div>
          <div class="ctx-color-dot-row">
            <button class="ctx-color-dot" style="background:#272a33;" onclick="ctxSetNoteCardColor(${noteId}, '')" title="Por defecto"></button>
            <button class="ctx-color-dot" style="background:#f59e0b;" onclick="ctxSetNoteCardColor(${noteId}, 'amber')" title="Ámbar"></button>
            <button class="ctx-color-dot" style="background:#3b82f6;" onclick="ctxSetNoteCardColor(${noteId}, 'blue')" title="Azul"></button>
            <button class="ctx-color-dot" style="background:#10b981;" onclick="ctxSetNoteCardColor(${noteId}, 'green')" title="Esmeralda"></button>
            <button class="ctx-color-dot" style="background:#a855f7;" onclick="ctxSetNoteCardColor(${noteId}, 'purple')" title="Púrpura"></button>
            <button class="ctx-color-dot" style="background:#f43f5e;" onclick="ctxSetNoteCardColor(${noteId}, 'rose')" title="Rosa"></button>
          </div>
          <div class="ctx-menu-section-label">Carpetas asignadas (clic para añadir/quitar)</div>
          <div class="ctx-menu-chips-row">${folderChips}</div>
          <div class="ctx-menu-divider"></div>
          <div style="display:flex; gap:4px; padding:2px 6px;">
            <button class="ctx-menu-chip" style="flex:1; text-align:center;" onclick="ctxMoveNoteStep(${noteId}, -1)">▲ Subir</button>
            <button class="ctx-menu-chip" style="flex:1; text-align:center;" onclick="ctxMoveNoteStep(${noteId}, 1)">▼ Bajar</button>
          </div>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item danger" onclick="closeCustomContextMenu(); deleteNoteById(${noteId});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗑</span><span class="ctx-menu-label">Enviar a la papelera</span></span>
            <span class="ctx-menu-kbd">${getShortcutDisplayCombo('delete_note')}</span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, noteCard, html);
        return;
      }

      // 3. Cuadro de Tarea Kanban (.kanban-card)
      const kanbanCard = e.target.closest('.kanban-card');
      if (kanbanCard) {
        e.preventDefault();
        e.stopPropagation();
        const cardId = kanbanCard.getAttribute('data-kanban-id') || '';
        const rawText = kanbanCard.getAttribute('data-kanban-text') || kanbanCard.querySelector('span')?.textContent || '';
        const safeText = rawText.replace(/'/g, "\\'").replace(/"/g, '&quot;');
        const safeId = cardId.replace(/'/g, "\\'").replace(/"/g, '&quot;');

        const html = `
          <div class="ctx-menu-header">
            <span>📊 Tarea Kanban</span>
          </div>
          <button class="ctx-menu-item" onclick="ctxEditKanbanCard('${safeId || safeText}')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✏️</span><span class="ctx-menu-label">Editar propiedades y detalles</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxDuplicateKanbanCard('${safeId || safeText}')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📑</span><span class="ctx-menu-label">Duplicar tarea</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <div class="ctx-menu-section-label">Mover a columna</div>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); moveKanbanCard('${safeId || safeText}', 'todo')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">⏳</span><span class="ctx-menu-label">Por Hacer</span></span>
          </button>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); moveKanbanCard('${safeId || safeText}', 'in-progress')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🔄</span><span class="ctx-menu-label">En Progreso</span></span>
          </button>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); moveKanbanCard('${safeId || safeText}', 'done')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✅</span><span class="ctx-menu-label">Completado</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <div style="display:flex; gap:4px; padding:2px 6px;">
            <button class="ctx-menu-chip" style="flex:1; text-align:center;" onclick="closeCustomContextMenu(); moveKanbanCardVertical('${safeId || safeText}', -1)">▲ Subir</button>
            <button class="ctx-menu-chip" style="flex:1; text-align:center;" onclick="closeCustomContextMenu(); moveKanbanCardVertical('${safeId || safeText}', 1)">▼ Bajar</button>
          </div>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item danger" onclick="closeCustomContextMenu(); deleteKanbanCard('${safeId || safeText}')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗑</span><span class="ctx-menu-label">Eliminar tarea</span></span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, kanbanCard, html);
        return;
      }

      // 4. Fila de la Tabla de Propiedades (#block-table tbody tr[data-row-idx])
      const tableRow = e.target.closest('#properties-table-body tr[data-row-idx]');
      if (tableRow) {
        e.preventDefault();
        e.stopPropagation();
        const idx = Number(tableRow.getAttribute('data-row-idx'));
        const note = getActiveNote();
        const rowObj = (note && note.tableRows && note.tableRows[idx]) ? note.tableRows[idx] : {};

        const html = `
          <div class="ctx-menu-header">
            <span>▦ Fila: ${rowObj.name || '#' + (idx + 1)}</span>
          </div>
          <button class="ctx-menu-item" onclick="ctxInsertTableRowAt(${idx}, true)">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">⬆️</span><span class="ctx-menu-label">Insertar fila arriba</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxInsertTableRowAt(${idx}, false)">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">⬇️</span><span class="ctx-menu-label">Insertar fila abajo</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxDuplicateTableRow(${idx})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📑</span><span class="ctx-menu-label">Duplicar esta fila</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <div class="ctx-menu-section-label">Cambiar estado rápido</div>
          <div class="ctx-menu-chips-row">
            <button class="ctx-menu-chip" onclick="ctxSetTableRowStatus(${idx}, 'Listo')">✅ Listo</button>
            <button class="ctx-menu-chip" onclick="ctxSetTableRowStatus(${idx}, 'En Proceso')">⏳ En Proceso</button>
            <button class="ctx-menu-chip" onclick="ctxSetTableRowStatus(${idx}, 'Pendiente')">📌 Pendiente</button>
            <button class="ctx-menu-chip" onclick="ctxSetTableRowStatus(${idx}, 'Pagado')">💳 Pagado</button>
          </div>
          <div style="display:flex; gap:4px; padding:2px 6px;">
            <button class="ctx-menu-chip" style="flex:1; text-align:center;" onclick="closeCustomContextMenu(); moveTableRow(${idx}, -1)">▲ Subir fila</button>
            <button class="ctx-menu-chip" style="flex:1; text-align:center;" onclick="closeCustomContextMenu(); moveTableRow(${idx}, 1)">▼ Bajar fila</button>
          </div>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); openFormulaModal();">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✨</span><span class="ctx-menu-label">Configurar Fórmula 2.0</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item danger" onclick="closeCustomContextMenu(); deleteTableRow(${idx});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗑</span><span class="ctx-menu-label">Eliminar fila</span></span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, tableRow, html);
        return;
      }

      // 5. Fila de Checklist (.checklist-item-row)
      const checkRow = e.target.closest('.checklist-item-row[data-idx]');
      if (checkRow) {
        e.preventDefault();
        e.stopPropagation();
        const idx = Number(checkRow.getAttribute('data-idx'));
        const note = getActiveNote();
        const item = (note && note.checklists && note.checklists[idx]) ? note.checklists[idx] : { done: false };

        const html = `
          <div class="ctx-menu-header">
            <span>☑ Tarea Checklist</span>
          </div>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); toggleCheckItem(${idx}, ${!item.done});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">${item.done ? '⬜' : '✅'}</span><span class="ctx-menu-label">${item.done ? 'Marcar como pendiente' : 'Marcar como completada'}</span></span>
          </button>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); addChecklistItemAfter(${idx});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">➕</span><span class="ctx-menu-label">Añadir tarea debajo</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxDuplicateChecklistItem(${idx})">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📑</span><span class="ctx-menu-label">Duplicar tarea</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item" onclick="ctxMarkAllChecklists(true)">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">☑️</span><span class="ctx-menu-label">Completar todas las tareas</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxClearCompletedChecklists()">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🧹</span><span class="ctx-menu-label">Limpiar tareas completadas</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item danger" onclick="closeCustomContextMenu(); removeCheckItem(${idx});">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗑</span><span class="ctx-menu-label">Eliminar tarea</span></span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, checkRow, html);
        return;
      }

      // 6. Ecuación KaTeX en Línea (.inline-katex-node)
      const inlineKatex = e.target.closest('.inline-katex-node');
      if (inlineKatex) {
        e.preventDefault();
        e.stopPropagation();
        activeInlineKatexNode = inlineKatex;
        const latex = inlineKatex.getAttribute('data-latex') || '';
        const safeLatex = latex.replace(/'/g, "\\'");

        const html = `
          <div class="ctx-menu-header">
            <span>√x Ecuación KaTeX</span>
          </div>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); editInlineEquation(activeInlineKatexNode);">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✏️</span><span class="ctx-menu-label">Editar ecuación</span></span>
          </button>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); document.getElementById('inline-katex-input').value='${safeLatex}'; turnCurrentInlineToBlockEquation();">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📐</span><span class="ctx-menu-label">Convertir en cuadro de bloque</span></span>
          </button>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); navigator.clipboard.writeText('${safeLatex}'); showToast('LaTeX copiado', '📋');">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📋</span><span class="ctx-menu-label">Copiar código LaTeX</span></span>
          </button>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item danger" onclick="closeCustomContextMenu(); if(activeInlineKatexNode){activeInlineKatexNode.remove(); syncRichEditor(); showToast('Ecuación eliminada', '🗑');}">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗑</span><span class="ctx-menu-label">Eliminar ecuación</span></span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, inlineKatex, html);
        return;
      }

      // 7. Cuadros de Bloques Notion (#block-callout, #block-quote, #block-toggle, #block-code, #block-kanban, #block-table, #block-katex)
      const notionBlock = e.target.closest('#block-callout, #block-quote, #block-toggle, #block-code, #block-kanban, #block-table, #block-katex');
      if (notionBlock) {
        e.preventDefault();
        e.stopPropagation();
        const blockId = notionBlock.id;
        const blockKey = blockId.replace('block-', '');

        const blockNames = {
          callout: '💡 Cuadro Callout',
          quote: '❝ Cuadro de Cita',
          toggle: '▶ Cuadro Desplegable Toggle',
          code: '</> Cuadro de Código',
          kanban: '📊 Cuadro Tablero Kanban',
          table: '▦ Cuadro Tabla & Fórmulas 2.0',
          katex: '∑ Cuadro Ecuación KaTeX'
        };

        let specificOptions = '';
        if (blockKey === 'callout') {
          specificOptions = `
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); changeCalloutEmoji();">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">😀</span><span class="ctx-menu-label">Cambiar icono del Callout</span></span>
            </button>
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); navigator.clipboard.writeText(document.getElementById('callout-input').value); showToast('Texto copiado', '📋');">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📋</span><span class="ctx-menu-label">Copiar texto del cuadro</span></span>
            </button>
            <div class="ctx-menu-section-label">Color del cuadro Callout</div>
            <div class="ctx-color-dot-row">
              <button class="ctx-color-dot" style="background:#f59e0b;" onclick="ctxSetCalloutColor('amber')" title="Ámbar"></button>
              <button class="ctx-color-dot" style="background:#3b82f6;" onclick="ctxSetCalloutColor('blue')" title="Azul"></button>
              <button class="ctx-color-dot" style="background:#10b981;" onclick="ctxSetCalloutColor('green')" title="Verde"></button>
              <button class="ctx-color-dot" style="background:#a855f7;" onclick="ctxSetCalloutColor('purple')" title="Púrpura"></button>
              <button class="ctx-color-dot" style="background:#f43f5e;" onclick="ctxSetCalloutColor('rose')" title="Rosa"></button>
            </div>
          `;
        } else if (blockKey === 'quote') {
          specificOptions = `
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); navigator.clipboard.writeText(document.getElementById('quote-input').value); showToast('Cita copiada', '📋');">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📋</span><span class="ctx-menu-label">Copiar texto de la cita</span></span>
            </button>
          `;
        } else if (blockKey === 'toggle') {
          specificOptions = `
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); document.getElementById('block-toggle').classList.toggle('open');">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">▶</span><span class="ctx-menu-label">Expandir / Colapsar detalle</span></span>
            </button>
          `;
        } else if (blockKey === 'code') {
          specificOptions = `
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); copyCodeBlock();">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📋</span><span class="ctx-menu-label">Copiar código al portapapeles</span></span>
            </button>
          `;
        } else if (blockKey === 'kanban') {
          specificOptions = `
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); addKanbanCard('todo');">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">➕</span><span class="ctx-menu-label">Nueva tarea en Por Hacer</span></span>
            </button>
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); addKanbanCard('in-progress');">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">⚡</span><span class="ctx-menu-label">Nueva tarea en En Progreso</span></span>
            </button>
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); addKanbanCard('done');">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✅</span><span class="ctx-menu-label">Nueva tarea en Completado</span></span>
            </button>
          `;
        } else if (blockKey === 'table') {
          specificOptions = `
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); addTableRow();">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">➕</span><span class="ctx-menu-label">Añadir nueva fila</span></span>
            </button>
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); openFormulaModal();">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✨</span><span class="ctx-menu-label">Configurar Fórmula 2.0</span></span>
            </button>
          `;
        } else if (blockKey === 'katex') {
          specificOptions = `
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); setSampleKatex();">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🔬</span><span class="ctx-menu-label">Cargar ejemplo físico</span></span>
            </button>
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); navigator.clipboard.writeText(document.getElementById('katex-formula-input').value); showToast('Fórmula copiada', '📋');">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📋</span><span class="ctx-menu-label">Copiar código LaTeX</span></span>
            </button>
          `;
        }

        const html = `
          <div class="ctx-menu-header">
            <span>${blockNames[blockKey] || 'Cuadro de Bloque'}</span>
          </div>
          ${specificOptions}
          <div class="ctx-menu-divider"></div>
          <div style="display:flex; gap:4px; padding:2px 6px;">
            <button class="ctx-menu-chip" style="flex:1; text-align:center;" onclick="closeCustomContextMenu(); moveBlockElementUp('${blockId}')">▲ Subir cuadro</button>
            <button class="ctx-menu-chip" style="flex:1; text-align:center;" onclick="closeCustomContextMenu(); moveBlockElementDown('${blockId}')">▼ Bajar cuadro</button>
          </div>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item danger" onclick="closeCustomContextMenu(); deleteBlock('${blockKey}');">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗑</span><span class="ctx-menu-label">Eliminar cuadro</span></span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, notionBlock, html);
        return;
      }

      // 8. Cuadros de Carpetas en la Barra Lateral (.folder-item[data-folder])
      const folderBtn = e.target.closest('.folder-item[data-folder]');
      if (folderBtn) {
        e.preventDefault();
        e.stopPropagation();
        const folderName = folderBtn.getAttribute('data-folder');
        const safeFolder = folderName.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        const currentEmoji = getFolderEmoji(folderName);

        if (isMasterAllNotesFolder(folderName)) {
          const html = `
            <div class="ctx-menu-header">
              <span>${currentEmoji} Carpeta Principal: ${folderName}</span>
            </div>
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); handleSidebarFolderClick('${safeFolder}');">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">${currentEmoji}</span><span class="ctx-menu-label">Ver todas las notas</span></span>
            </button>
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); createNewNote();">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📝</span><span class="ctx-menu-label">Crear nueva nota</span></span>
            </button>
          `;
          openCustomContextMenu(e.clientX, e.clientY, folderBtn, html);
          return;
        }

        const quickEmojisHtml = QUICK_FOLDER_EMOJIS.slice(0, 12).map(em => `
          <button type="button"
                  class="ctx-emoji-quick-btn ${currentEmoji === em ? 'active' : ''}"
                  onclick="setFolderEmoji('${safeFolder}', '${em}')"
                  title="Asignar icono ${em}">
            ${em}
          </button>
        `).join('');

        if (isSmartFolder(folderName)) {
          const smartCfg = getSmartFolderConfig(folderName) || { matchMode: 'all', rules: [] };
          const rulesSummaryHtml = (smartCfg.rules || []).map(r => `<span class="ctx-menu-chip active" style="pointer-events:none;">${escapeHtmlAttr(formatSmartRuleSummary(r))}</span>`).join('');
          const html = `
            <div class="ctx-menu-header">
              <span>${currentEmoji} ${folderName}</span>
              <span class="ctx-menu-header-sub">⚙️ Inteligente (${smartCfg.matchMode === 'any' ? 'OR' : 'AND'})</span>
            </div>
            <button class="ctx-menu-item" onclick="closeCustomContextMenu(); selectFolder('${safeFolder}');">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">${currentEmoji}</span><span class="ctx-menu-label">Ver notas que cumplen el filtro</span></span>
            </button>
            <button class="ctx-menu-item" onclick="openSmartFolderModal('edit', '${safeFolder}')">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">⚙️</span><span class="ctx-menu-label">Editar reglas y condiciones...</span></span>
            </button>
            <div class="ctx-menu-section-label">Reglas activas (Nivel raíz · No colaborativa)</div>
            <div class="ctx-menu-chips-row">${rulesSummaryHtml || '<span class="ctx-menu-chip">Sin reglas</span>'}</div>
            <div class="ctx-menu-section-label">Iconos rápidos</div>
            <div class="ctx-emoji-quick-row">
              ${quickEmojisHtml}
            </div>
            <div class="ctx-menu-divider"></div>
            <button class="ctx-menu-item danger" onclick="ctxDeleteFolder('${safeFolder}')">
              <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗑</span><span class="ctx-menu-label">Eliminar filtro inteligente (conserva las notas)</span></span>
            </button>
          `;
          openCustomContextMenu(e.clientX, e.clientY, folderBtn, html);
          return;
        }

        const html = `
          <div class="ctx-menu-header">
            <span>${currentEmoji} Carpeta: ${folderName}</span>
          </div>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); selectFolder('${safeFolder}');">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">${currentEmoji}</span><span class="ctx-menu-label">Abrir carpeta</span></span>
          </button>
          <button class="ctx-menu-item" onclick="openSubfolderModal('${safeFolder}')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📂</span><span class="ctx-menu-label">Crear subcarpeta dentro de "${getFolderDisplayName(folderName)}"</span></span>
          </button>
          ${getFolderDepth(folderName) > 0 ? `
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); moveFolderHierarchy('${safeFolder}', '')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">⬆️</span><span class="ctx-menu-label">Mover al nivel principal (sacar de "${getFolderDisplayName(getFolderParentPath(folderName))}")</span></span>
          </button>` : ''}
          <button class="ctx-menu-item" onclick="ctxCreateNoteInFolder('${safeFolder}')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">📝</span><span class="ctx-menu-label">Nueva nota asignada a "${getFolderDisplayName(folderName)}"</span></span>
          </button>
          <button class="ctx-menu-item" onclick="openFolderModal('emoji', '${safeFolder}')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">😀</span><span class="ctx-menu-label">Personalizar icono emoji...</span></span>
          </button>
          <button class="ctx-menu-item" onclick="ctxRenameFolder('${safeFolder}')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">✏️</span><span class="ctx-menu-label">Renombrar o mover carpeta</span></span>
          </button>
          <button class="ctx-menu-item" onclick="openConvertStandardToSmartModal('${safeFolder}')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">⚙️</span><span class="ctx-menu-label">Convertir en Carpeta Inteligente...</span></span>
          </button>
          <div class="ctx-menu-section-label">Iconos rápidos de carpeta</div>
          <div class="ctx-emoji-quick-row">
            ${quickEmojisHtml}
          </div>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item danger" onclick="ctxDeleteFolder('${safeFolder}')">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">🗑</span><span class="ctx-menu-label">Eliminar carpeta</span></span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, folderBtn, html);
        return;
      }

      // 9. Divisores Redimensionables de Paneles (.panel-resizer)
      const resizerEl = e.target.closest('.panel-resizer[data-resizer]');
      if (resizerEl) {
        e.preventDefault();
        e.stopPropagation();
        const panelKey = resizerEl.getAttribute('data-resizer');
        const isFolders = panelKey === 'folders';
        const panelLabel = isFolders ? 'Panel de Carpetas' : 'Panel de Galería';
        const currentPx = (state.panelWidths && state.panelWidths[panelKey]) || PANEL_WIDTH_DEFAULTS[panelKey];
        const defaultPx = PANEL_WIDTH_DEFAULTS[panelKey];
        const presets = isFolders
          ? [
              { label: 'Compacto (190px)', px: 190 },
              { label: 'Estándar (250px)', px: 250 },
              { label: 'Amplio (330px)', px: 330 }
            ]
          : [
              { label: 'Compacto (240px)', px: 240 },
              { label: 'Estándar (300px)', px: 300 },
              { label: 'Amplio (420px)', px: 420 }
            ];

        const html = `
          <div class="ctx-menu-header">
            <span>↔️ ${panelLabel}</span>
            <span class="ctx-menu-header-sub">${currentPx} px</span>
          </div>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); resetPanelWidth('${panelKey}');">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">↺</span><span class="ctx-menu-label">Restablecer ancho (${defaultPx} px)</span></span>
            <span class="ctx-menu-kbd">2×Clic</span>
          </button>
          <div class="ctx-menu-section-label">Tamaños predefinidos</div>
          <div class="ctx-menu-chips-row">
            ${presets.map(p => `
              <button class="ctx-menu-chip ${currentPx === p.px ? 'active' : ''}" onclick="closeCustomContextMenu(); setPanelPresetWidth('${panelKey}', ${p.px});">${p.label}</button>
            `).join('')}
          </div>
          <div class="ctx-menu-divider"></div>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); ${isFolders ? 'toggleSidebar()' : 'toggleGallery()'};">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">${isFolders ? '📁' : '🗂️'}</span><span class="ctx-menu-label">${isFolders ? 'Ocultar barra de carpetas' : 'Ocultar panel de notas'}</span></span>
            <span class="ctx-menu-kbd">${isFolders ? 'Alt+1' : 'Alt+2'}</span>
          </button>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); resetPanelWidth('all');">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">⚖️</span><span class="ctx-menu-label">Restablecer todos los paneles</span></span>
          </button>
          <button class="ctx-menu-item" onclick="closeCustomContextMenu(); toggleFocusMode();">
            <span class="ctx-menu-item-left"><span class="ctx-menu-icon">⚡</span><span class="ctx-menu-label">Vista de Enfoque</span></span>
            <span class="ctx-menu-kbd">Ctrl+\\</span>
          </button>
        `;
        openCustomContextMenu(e.clientX, e.clientY, resizerEl, html);
        return;
      }

      // Si se hace clic derecho fuera de un cuadro, cerrar cualquier menú contextual abierto
      closeCustomContextMenu();
    });

    /* ============================================================================
       GESTOR DE ATAJOS DE TECLADO GLOBALES (ShortcutManager)
       ============================================================================ */
    const DEFAULT_SHORTCUTS_REGISTRY = [
      {
        id: 'navigate_home',
        title: 'Ir a página de inicio',
        desc: 'Abre la vista de página de inicio de la app estilo Chrome',
        icon: '🏠',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Alt+H',
        altCombo: 'Ctrl+Shift+H',
        tooltipBase: 'Página de inicio',
        action: () => {
          navigateToHome();
        }
      },
      {
        id: 'navigate_reminders',
        title: 'Ver recordatorios a pantalla completa',
        desc: 'Abre el panel de recordatorios y calendario a pantalla completa',
        icon: '📅',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Alt+R',
        altCombo: 'Ctrl+Shift+R',
        tooltipBase: 'Recordatorios a pantalla completa',
        action: () => {
          navigateToReminders();
        }
      },
      {
        id: 'new_note',
        title: 'Crear nueva nota en pestaña',
        desc: 'Crea una nota en la carpeta activa, la abre en una pestaña y enfoca el título',
        icon: '📝',
        category: 'Gestión de Notas',
        scope: 'global',
        defaultCombo: 'Ctrl+N',
        altCombo: 'Alt+N',
        tooltipBase: 'Crear nueva nota en pestaña',
        action: () => {
          createNewNote();
          showToast('Nueva nota creada en pestaña', '📝');
        }
      },
      {
        id: 'close_tab',
        title: 'Cerrar pestaña de nota actual',
        desc: 'Cierra la pestaña activa de la barra superior y cambia a la pestaña contigua',
        icon: '🗂️',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Alt+W',
        tooltipBase: 'Cerrar pestaña actual',
        action: () => {
          closeNoteTab(state.activeNoteId);
        }
      },
      {
        id: 'next_tab',
        title: 'Siguiente pestaña abierta',
        desc: 'Cambia inmediatamente a la siguiente nota abierta en la barra de pestañas',
        icon: '➡️',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Alt+ArrowRight',
        tooltipBase: 'Siguiente pestaña abierta',
        action: () => {
          cycleOpenNoteTab(1);
        }
      },
      {
        id: 'prev_tab',
        title: 'Pestaña abierta anterior',
        desc: 'Cambia inmediatamente a la nota anterior abierta en la barra de pestañas',
        icon: '⬅️',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Alt+ArrowLeft',
        tooltipBase: 'Pestaña abierta anterior',
        action: () => {
          cycleOpenNoteTab(-1);
        }
      },
      {
        id: 'search_notes',
        title: 'Buscar en notas',
        desc: 'Despliega la barra de búsqueda de la galería y enfoca el filtro',
        icon: '🔍',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Ctrl+F',
        tooltipBase: 'Buscar en notas',
        action: () => {
          if (state.isFocusMode) {
            toggleFocusMode();
          }
          toggleNotesSearch(true);
        }
      },
      {
        id: 'open_shortcuts',
        title: 'Abrir Gestor de Atajos de Teclado',
        desc: 'Muestra este panel interactivo con todos los atajos de la aplicación',
        icon: '⌨️',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Ctrl+/',
        altCombo: 'F1',
        tooltipBase: 'Abrir Gestor de Atajos de Teclado',
        action: () => {
          const modal = document.getElementById('shortcuts-modal');
          if (modal && modal.classList.contains('open')) {
            closeShortcutsModal();
          } else {
            openShortcutsModal();
          }
        }
      },
      {
        id: 'toggle_focus',
        title: 'Alternar Vista de Enfoque',
        desc: 'Oculta o muestra suavemente los paneles laterales para redactar sin distracciones',
        icon: '⚡',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Ctrl+\\',
        tooltipBase: 'Vista de Enfoque',
        action: () => {
          toggleFocusMode();
        }
      },
      {
        id: 'toggle_sidebar',
        title: 'Alternar barra lateral de carpetas',
        desc: 'Oculta o muestra suavemente la barra lateral izquierda de carpetas',
        icon: '📁',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Alt+1',
        tooltipBase: 'Alternar barra lateral de carpetas',
        action: () => {
          toggleSidebar();
        }
      },
      {
        id: 'toggle_gallery',
        title: 'Alternar panel de galería de notas',
        desc: 'Oculta o muestra suavemente el panel central con la lista de notas',
        icon: '🗂️',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Alt+2',
        tooltipBase: 'Alternar galería de notas',
        action: () => {
          toggleGallery();
        }
      },
      {
        id: 'toggle_history',
        title: 'Alternar Historial de Ediciones (SQLite)',
        desc: 'Muestra u oculta el panel derecho con las versiones de la nota actual para previsualizar o revertir',
        icon: '🕒',
        category: 'Gestión de Notas',
        scope: 'global',
        defaultCombo: 'Ctrl+H',
        tooltipBase: 'Historial de Ediciones SQLite',
        action: () => {
          toggleHistoryPanel();
        }
      },
      {
        id: 'toggle_view',
        title: 'Alternar Vista Lista / Cuadrícula',
        desc: 'Cambia la galería central entre tarjetas en lista o cuadrícula',
        icon: '▦',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Ctrl+Shift+L',
        tooltipBase: 'Alternar Vista Lista / Cuadrícula',
        action: () => {
          setListViewMode(state.isGridView ? 'list' : 'grid');
          showToast(state.isGridView ? 'Vista Cuadrícula activa' : 'Vista Lista activa', '▦');
        }
      },
      {
        id: 'toggle_theme',
        title: 'Alternar Tema Claro / Oscuro',
        desc: 'Conmuta la paleta visual entre modo oscuro macOS y modo claro',
        icon: '🌗',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Ctrl+Shift+D',
        tooltipBase: 'Alternar Tema Claro / Oscuro',
        action: () => {
          toggleTheme();
          showToast(state.isLightMode ? 'Tema Claro activado' : 'Tema Oscuro activado', '🌗');
        }
      },
      {
        id: 'open_settings',
        title: 'Abrir Ajustes de PC',
        desc: 'Abre la ventana de configuración y exportación PyWebView + SQLite',
        icon: '⚙️',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Ctrl+,',
        tooltipBase: 'Ajustes de PC',
        action: () => {
          openSettingsModal();
        }
      },
      {
        id: 'next_note',
        title: 'Siguiente nota en la galería',
        desc: 'Selecciona la nota inferior en la lista o colección activa',
        icon: '⬇️',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Ctrl+Alt+ArrowDown',
        tooltipBase: 'Siguiente nota',
        action: () => {
          navigateAdjacentNote(1);
        }
      },
      {
        id: 'prev_note',
        title: 'Nota anterior en la galería',
        desc: 'Selecciona la nota superior en la lista o colección activa',
        icon: '⬆️',
        category: 'Global y Navegación',
        scope: 'global',
        defaultCombo: 'Ctrl+Alt+ArrowUp',
        tooltipBase: 'Nota anterior',
        action: () => {
          navigateAdjacentNote(-1);
        }
      },
      {
        id: 'new_folder',
        title: 'Crear nueva carpeta',
        desc: 'Añade una nueva categoría en el panel izquierdo de carpetas',
        icon: '📁',
        category: 'Gestión de Notas',
        scope: 'global',
        defaultCombo: 'Alt+Shift+N',
        tooltipBase: 'Añadir carpeta',
        action: () => {
          promptNewFolder();
        }
      },
      {
        id: 'pin_note',
        title: 'Fijar / Desfijar nota actual',
        desc: 'Ancla o desancla la nota activa en la colección de Notas fijadas',
        icon: '📌',
        category: 'Gestión de Notas',
        scope: 'global',
        defaultCombo: 'Ctrl+Shift+P',
        tooltipBase: 'Fijar / Desfijar nota',
        action: () => {
          togglePinActiveNote();
          const active = getActiveNote();
          if (active) {
            showToast(active.isPinned ? 'Nota fijada' : 'Nota desfijada', '📌');
          }
        }
      },
      {
        id: 'duplicate_note',
        title: 'Duplicar nota actual',
        desc: 'Crea una copia exacta de la nota que estás editando',
        icon: '📑',
        category: 'Gestión de Notas',
        scope: 'global',
        defaultCombo: 'Alt+Shift+D',
        tooltipBase: 'Duplicar nota actual',
        action: () => {
          if (state.activeNoteId) {
            ctxDuplicateNote(state.activeNoteId);
          }
        }
      },
      {
        id: 'delete_note',
        title: 'Eliminar nota actual',
        desc: 'Borra la nota activa de SQLite + Peewee y selecciona la siguiente',
        icon: '🗑',
        category: 'Gestión de Notas',
        scope: 'global',
        defaultCombo: 'Ctrl+Shift+Backspace',
        tooltipBase: 'Eliminar nota actual',
        action: () => {
          deleteActiveNote();
          showToast('Nota eliminada', '🗑');
        }
      },
      {
        id: 'insert_menu',
        title: 'Abrir menú "+ Insertar" bloques',
        desc: 'Despliega el selector de bloques Notion, tablas y herramientas',
        icon: '➕',
        category: 'Editor y Bloques',
        scope: 'global',
        defaultCombo: 'Ctrl+Shift+I',
        tooltipBase: 'Insertar bloques y herramientas',
        action: () => {
          toggleInsertDropdown();
        }
      },
      {
        id: 'insert_image',
        title: 'Insertar Bloque de Imagen Redimensionable',
        desc: 'Abre el gestor para insertar una imagen por URL web, ruta local de PC o archivo',
        icon: '🖼️',
        category: 'Editor y Bloques',
        scope: 'global',
        defaultCombo: 'Alt+Shift+I',
        tooltipBase: 'Insertar Bloque de Imagen Redimensionable',
        action: () => {
          openImageInsertModal();
        }
      },
      {
        id: 'inline_math',
        title: 'Insertar Ecuación KaTeX en línea',
        desc: 'Abre el editor flotante de fórmulas científicas LaTeX / mhchem',
        icon: '√x',
        category: 'Editor y Bloques',
        scope: 'global',
        defaultCombo: 'Ctrl+Shift+E',
        tooltipBase: 'Ecuación en línea KaTeX',
        action: () => {
          openInlineMathPopover();
        }
      },
      {
        id: 'insert_checklist',
        title: 'Insertar Lista Checklist',
        desc: 'Añade una tarea interactiva con casilla de verificación',
        icon: '☑',
        category: 'Editor y Bloques',
        scope: 'global',
        defaultCombo: 'Ctrl+Shift+C',
        tooltipBase: 'Insertar Lista Checklist',
        action: () => {
          insertChecklistBlock();
        }
      },
      {
        id: 'insert_kanban',
        title: 'Insertar Tablero Kanban',
        desc: 'Activa el tablero de proyectos Por Hacer / En Progreso / Completado',
        icon: '📊',
        category: 'Editor y Bloques',
        scope: 'global',
        defaultCombo: 'Ctrl+Shift+K',
        tooltipBase: 'Insertar Tablero Kanban',
        action: () => {
          toggleKanbanBlock(true);
        }
      },
      {
        id: 'insert_table',
        title: 'Insertar Tabla & Fórmulas 2.0',
        desc: 'Activa la tabla de propiedades con evaluador dinámico style()',
        icon: '▦',
        category: 'Editor y Bloques',
        scope: 'global',
        defaultCombo: 'Ctrl+Shift+T',
        tooltipBase: 'Insertar Tabla & Fórmulas 2.0',
        action: () => {
          togglePropertiesTableBlock(true);
        }
      },
      {
        id: 'embed_note',
        title: 'Incrustar Acceso a otra Nota',
        desc: 'Abre el vinculador para insertar una tarjeta de nota dentro del texto',
        icon: '🔗',
        category: 'Editor y Bloques',
        scope: 'global',
        defaultCombo: 'Ctrl+Shift+M',
        tooltipBase: 'Incrustar Acceso a otra Nota',
        action: () => {
          promptAddShortcut();
        }
      },
      {
        id: 'format_bold',
        title: 'Formato Negrita (B)',
        desc: 'Aplica o quita negrita al texto seleccionado en el editor',
        icon: 'B',
        category: 'Editor y Bloques',
        scope: 'editor',
        defaultCombo: 'Ctrl+B',
        tooltipBase: 'Negrita',
        action: () => {
          formatDoc('bold');
        }
      },
      {
        id: 'format_italic',
        title: 'Formato Cursiva (I)',
        desc: 'Aplica o quita cursiva al texto seleccionado en el editor',
        icon: 'I',
        category: 'Editor y Bloques',
        scope: 'editor',
        defaultCombo: 'Ctrl+I',
        tooltipBase: 'Cursiva',
        action: () => {
          formatDoc('italic');
        }
      },
      {
        id: 'format_underline',
        title: 'Formato Subrayado (U)',
        desc: 'Aplica o quita subrayado al texto seleccionado en el editor',
        icon: 'U',
        category: 'Editor y Bloques',
        scope: 'editor',
        defaultCombo: 'Ctrl+U',
        tooltipBase: 'Subrayado',
        action: () => {
          formatDoc('underline');
        }
      },
      {
        id: 'move_line_up',
        title: 'Subir línea o párrafo',
        desc: 'Desplaza el bloque o párrafo actual una posición hacia arriba',
        icon: '↑',
        category: 'Editor y Bloques',
        scope: 'editor',
        defaultCombo: 'Alt+ArrowUp',
        tooltipBase: 'Subir línea',
        action: () => {
          moveSelectedLine(-1);
        }
      },
      {
        id: 'move_line_down',
        title: 'Bajar línea o párrafo',
        desc: 'Desplaza el bloque o párrafo actual una posición hacia abajo',
        icon: '↓',
        category: 'Editor y Bloques',
        scope: 'editor',
        defaultCombo: 'Alt+ArrowDown',
        tooltipBase: 'Bajar línea',
        action: () => {
          moveSelectedLine(1);
        }
      }
    ];

    let customShortcutsMap = {};
    let activeShortcutCategoryFilter = 'ALL';
    let recordingShortcutId = null;

    function initShortcutManager() {
      try {
        const saved = localStorage.getItem('notejs_custom_shortcuts_v1');
        if (saved) {
          const parsed = JSON.parse(saved);
          if (parsed && typeof parsed === 'object') {
            customShortcutsMap = parsed;
          }
        }
      } catch (_) {
        customShortcutsMap = {};
      }
      syncShortcutsToUI();
    }

    function applyCustomShortcutsMap(mapObj, persistLocal = true) {
      customShortcutsMap = { ...mapObj };
      if (persistLocal) {
        localStorage.setItem('notejs_custom_shortcuts_v1', JSON.stringify(customShortcutsMap));
        const settingsPayload = { customShortcuts: JSON.stringify(customShortcutsMap) };
        if (hasPyWebViewBridge() && typeof window.pywebview.api.save_settings === "function") {
          window.pywebview.api.save_settings(settingsPayload).catch(() => {});
        } else {
          fetch("/api/settings", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(settingsPayload)
          }).catch(() => {});
        }
      }
      syncShortcutsToUI();
    }

    function getActiveShortcutCombo(shortcutId) {
      const item = DEFAULT_SHORTCUTS_REGISTRY.find(s => s.id === shortcutId);
      if (!item) return '';
      return customShortcutsMap[shortcutId] || item.defaultCombo;
    }

    function formatKeyNameForDisplay(keyPart) {
      const map = {
        ArrowUp: '↑',
        ArrowDown: '↓',
        ArrowLeft: '←',
        ArrowRight: '→',
        Backspace: '⌫',
        Delete: 'Supr',
        Escape: 'Esc',
        ' ': 'Espacio'
      };
      return map[keyPart] || keyPart;
    }

    function getShortcutDisplayCombo(shortcutId) {
      const raw = getActiveShortcutCombo(shortcutId);
      if (!raw) return '';
      return raw
        .split('+')
        .map(part => formatKeyNameForDisplay(part))
        .join('+');
    }

    function renderComboKeycapsHtml(comboStr, altComboStr = '') {
      const renderSingle = (str) => {
        const parts = str.split('+');
        return `<span class="kbd-combo-group">${parts
          .map((p, idx) => {
            const label = formatKeyNameForDisplay(p);
            return `<kbd class="kbd-keycap">${label}</kbd>${idx < parts.length - 1 ? '<span class="kbd-plus">+</span>' : ''}`;
          })
          .join('')}</span>`;
      };
      if (altComboStr) {
        return `${renderSingle(comboStr)} <span style="font-size:10px; color:var(--text-muted); margin:0 2px;">o</span> ${renderSingle(altComboStr)}`;
      }
      return renderSingle(comboStr);
    }

    function syncShortcutsToUI() {
      // Actualizar todos los <kbd data-shortcut-badge="...">
      document.querySelectorAll('[data-shortcut-badge]').forEach(el => {
        const id = el.getAttribute('data-shortcut-badge');
        const display = getShortcutDisplayCombo(id);
        if (display) {
          el.textContent = display;
        }
      });

      // Actualizar todos los botones con [data-shortcut-tooltip="..."]
      document.querySelectorAll('[data-shortcut-tooltip]').forEach(el => {
        const id = el.getAttribute('data-shortcut-tooltip');
        const item = DEFAULT_SHORTCUTS_REGISTRY.find(s => s.id === id);
        if (!item) return;
        const display = getShortcutDisplayCombo(id);
        const alt = (!customShortcutsMap[id] && item.altCombo) ? ` / ${item.altCombo}` : '';
        el.setAttribute('title', `${item.tooltipBase} (${display}${alt})`);
      });

      // Actualizar placeholder del buscador de notas
      const searchInput = document.getElementById('notes-search-input');
      if (searchInput) {
        searchInput.setAttribute('placeholder', `Buscar por título o contenido... (${getShortcutDisplayCombo('search_notes')})`);
      }
    }

    function navigateAdjacentNote(direction) {
      const cards = Array.from(document.querySelectorAll('#notes-list-container .note-item-card[data-note-id]'));
      if (!cards.length) return;
      const ids = cards.map(c => Number(c.getAttribute('data-note-id')));
      const curIdx = ids.indexOf(Number(state.activeNoteId));
      const nextIdx = curIdx === -1 ? 0 : (curIdx + direction + ids.length) % ids.length;
      selectNote(ids[nextIdx]);
    }

    function normalizeKeyboardEventToCombo(e) {
      const mods = [];
      if (e.ctrlKey || e.metaKey) mods.push('Ctrl');
      if (e.altKey) mods.push('Alt');
      if (e.shiftKey) mods.push('Shift');

      const ignoredKeys = ['Control', 'Meta', 'Alt', 'Shift', 'CapsLock', 'OS'];
      if (ignoredKeys.includes(e.key)) {
        return null;
      }

      let keyName = e.key;
      if (keyName.length === 1) {
        // Normalizar letras a mayúsculas y símbolos comunes
        keyName = keyName.toUpperCase();
      }
      if (e.code === 'Slash' && (e.ctrlKey || e.metaKey) && !e.shiftKey) {
        keyName = '/';
      } else if (e.code === 'Backslash' && (e.ctrlKey || e.metaKey)) {
        keyName = '\\';
      } else if (e.code === 'Comma' && (e.ctrlKey || e.metaKey)) {
        keyName = ',';
      }

      return [...mods, keyName].join('+');
    }

    function openShortcutsModal() {
      recordingShortcutId = null;
      const modal = document.getElementById('shortcuts-modal');
      if (!modal) return;
      modal.classList.add('open');
      renderShortcutsModal();
      setTimeout(() => {
        const input = document.getElementById('shortcuts-search-input');
        if (input) input.focus();
      }, 40);
    }

    function closeShortcutsModal() {
      recordingShortcutId = null;
      const modal = document.getElementById('shortcuts-modal');
      if (modal) modal.classList.remove('open');
    }

    function setShortcutsCategoryFilter(cat) {
      activeShortcutCategoryFilter = cat;
      document.querySelectorAll('#shortcuts-category-tabs .shortcut-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-cat') === cat);
      });
      renderShortcutsModal();
    }

    function startShortcutRebind(shortcutId, ev) {
      if (ev) ev.stopPropagation();
      recordingShortcutId = (recordingShortcutId === shortcutId) ? null : shortcutId;
      renderShortcutsModal();
    }

    function executeRegisteredShortcut(shortcutId) {
      const item = DEFAULT_SHORTCUTS_REGISTRY.find(s => s.id === shortcutId);
      if (!item) return;
      closeShortcutsModal();
      setTimeout(() => {
        item.action();
      }, 40);
    }

    function resetShortcutsToDefault() {
      recordingShortcutId = null;
      applyCustomShortcutsMap({}, true);
      renderShortcutsModal();
      showToast('Atajos de teclado restablecidos por defecto', '↺');
    }

    function renderShortcutsModal() {
      const container = document.getElementById('shortcuts-list-container');
      if (!container) return;

      const query = (document.getElementById('shortcuts-search-input')?.value || '').toLowerCase().trim();

      const filtered = DEFAULT_SHORTCUTS_REGISTRY.filter(item => {
        if (activeShortcutCategoryFilter !== 'ALL' && item.category !== activeShortcutCategoryFilter) {
          return false;
        }
        if (!query) return true;
        const activeCombo = getActiveShortcutCombo(item.id).toLowerCase();
        const altCombo = (item.altCombo || '').toLowerCase();
        return (
          item.title.toLowerCase().includes(query) ||
          item.desc.toLowerCase().includes(query) ||
          item.category.toLowerCase().includes(query) ||
          activeCombo.includes(query) ||
          altCombo.includes(query)
        );
      });

      const countLabel = document.getElementById('shortcuts-count-label');
      if (countLabel) {
        countLabel.textContent = `(${filtered.length} de ${DEFAULT_SHORTCUTS_REGISTRY.length} atajos registrados)`;
      }

      if (!filtered.length) {
        container.innerHTML = `
          <div style="text-align:center; padding:36px 16px; color:var(--text-muted); font-size:13px;">
            No se encontraron atajos que coincidan con tu búsqueda.
          </div>
        `;
        return;
      }

      const categories = ['Global y Navegación', 'Gestión de Notas', 'Editor y Bloques'];
      container.innerHTML = categories
        .map(cat => {
          const groupItems = filtered.filter(i => i.category === cat);
          if (!groupItems.length) return '';

          const rowsHtml = groupItems
            .map(item => {
              const isRecording = recordingShortcutId === item.id;
              const combo = getActiveShortcutCombo(item.id);
              const hasAlt = !customShortcutsMap[item.id] && item.altCombo ? item.altCombo : '';
              const isGlobal = item.scope === 'global';

              return `
                <div class="shortcut-item-row ${isRecording ? 'recording' : ''}">
                  <div class="shortcut-item-info">
                    <div class="shortcut-item-icon">${item.icon}</div>
                    <div class="shortcut-item-text">
                      <div class="shortcut-item-title">
                        <span>${item.title}</span>
                        <span class="shortcut-scope-pill ${isGlobal ? 'global' : ''}">${isGlobal ? 'Global' : 'Editor'}</span>
                      </div>
                      <div class="shortcut-item-desc">${item.desc}</div>
                    </div>
                  </div>
                  <div class="shortcut-item-controls">
                    ${isRecording
                      ? `<span style="font-size:11.5px; font-weight:700; color:var(--accent-amber);">Presiona combinación (Esc cancela)...</span>`
                      : renderComboKeycapsHtml(combo, hasAlt)
                    }
                    <button class="shortcut-action-btn ${isRecording ? 'recording' : ''}" onclick="startShortcutRebind('${item.id}', event)" title="Personalizar combinación de teclas">
                      ${isRecording ? 'Grabando...' : 'Reasignar'}
                    </button>
                    <button class="shortcut-action-btn" onclick="executeRegisteredShortcut('${item.id}')" title="Ejecutar esta acción ahora">
                      ▶ Ejecutar
                    </button>
                  </div>
                </div>
              `;
            })
            .join('');

          return `
            <div class="shortcuts-group-block">
              <div class="shortcuts-group-title">
                <span>${cat}</span>
                <span>${groupItems.length} atajos</span>
              </div>
              ${rowsHtml}
            </div>
          `;
        })
        .join('');
    }

    document.addEventListener('click', function(e) {
      const btn = document.getElementById('btn-insert-dropdown');
      const dropdown = document.getElementById('insert-blocks-dropdown');
      if (dropdown && btn && !btn.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('open');
        btn.classList.remove('active');
      }

      const tabPickerBtn = document.getElementById('btn-tab-picker');
      const tabPickerDropdown = document.getElementById('note-tab-picker-dropdown');
      if (tabPickerDropdown && tabPickerBtn && !tabPickerBtn.contains(e.target) && !tabPickerDropdown.contains(e.target)) {
        closeTabPickerDropdown();
      }

      const ctxMenu = document.getElementById('custom-context-menu');
      if (ctxMenu && ctxMenu.classList.contains('open') && !ctxMenu.contains(e.target)) {
        closeCustomContextMenu();
      }
    });

    /* Captura Global de Atajos de Teclado (window capture phase) */
    window.addEventListener('keydown', function(e) {
      // 1. Si el usuario está grabando un nuevo atajo en el Gestor de Atajos (#shortcuts-modal)
      if (recordingShortcutId) {
        if (e.key === 'Escape') {
          e.preventDefault();
          e.stopPropagation();
          recordingShortcutId = null;
          renderShortcutsModal();
          return;
        }
        const newCombo = normalizeKeyboardEventToCombo(e);
        if (!newCombo) return;

        // Requerir al menos un modificador (Ctrl, Alt, Shift) o tecla de función F1-F12
        const hasModifier = e.ctrlKey || e.metaKey || e.altKey || /^F\d+$/.test(e.key);
        if (!hasModifier) {
          showToast('Usa al menos Ctrl, Alt o Cmd junto con una tecla', '⚠️');
          return;
        }

        e.preventDefault();
        e.stopPropagation();

        const updatedMap = { ...customShortcutsMap, [recordingShortcutId]: newCombo };
        const rebId = recordingShortcutId;
        recordingShortcutId = null;
        applyCustomShortcutsMap(updatedMap, true);
        renderShortcutsModal();

        const targetItem = DEFAULT_SHORTCUTS_REGISTRY.find(s => s.id === rebId);
        showToast(`Atajo "${targetItem ? targetItem.title : rebId}" asignado a ${newCombo}`, '⌨️');
        return;
      }

      // 2. Tecla Escape global: cerrar menús y modales abiertos por orden de prioridad
      if (e.key === 'Escape') {
        const ctxMenu = document.getElementById('custom-context-menu');
        if (ctxMenu && ctxMenu.classList.contains('open')) {
          e.preventDefault();
          closeCustomContextMenu();
          return;
        }
        const smartConvertModal = document.getElementById('smart-folder-convert-modal');
        if (smartConvertModal && smartConvertModal.classList.contains('open')) {
          e.preventDefault();
          closeSmartFolderConvertModal();
          return;
        }
        const smartModal = document.getElementById('smart-folder-modal');
        if (smartModal && smartModal.classList.contains('open')) {
          e.preventDefault();
          closeSmartFolderModal();
          return;
        }
        const folderModal = document.getElementById('folder-custom-modal');
        if (folderModal && folderModal.classList.contains('open')) {
          e.preventDefault();
          closeFolderModal();
          return;
        }
        const shortcutsModal = document.getElementById('shortcuts-modal');
        if (shortcutsModal && shortcutsModal.classList.contains('open')) {
          e.preventDefault();
          closeShortcutsModal();
          return;
        }
        const settingsModal = document.getElementById('settings-modal');
        if (settingsModal && settingsModal.classList.contains('open')) {
          e.preventDefault();
          closeSettingsModal();
          return;
        }
        const formulaModal = document.getElementById('formula-modal');
        if (formulaModal && formulaModal.classList.contains('open')) {
          e.preventDefault();
          closeFormulaModal();
          return;
        }
        const linkerModal = document.getElementById('note-linker-modal');
        if (linkerModal && linkerModal.classList.contains('open')) {
          e.preventDefault();
          closeNoteLinkerModal();
          return;
        }
        const lightboxModal = document.getElementById('image-lightbox-modal');
        if (lightboxModal && lightboxModal.classList.contains('open')) {
          e.preventDefault();
          closeImageLightbox();
          return;
        }
        const imageInsertModal = document.getElementById('image-insert-modal');
        if (imageInsertModal && imageInsertModal.classList.contains('open')) {
          e.preventDefault();
          closeImageInsertModal();
          return;
        }
        const insertDropdown = document.getElementById('insert-blocks-dropdown');
        if (insertDropdown && insertDropdown.classList.contains('open')) {
          e.preventDefault();
          closeInsertDropdown();
          return;
        }
        const slashMenu = document.getElementById('slash-menu');
        if (slashMenu && slashMenu.classList.contains('open')) {
          e.preventDefault();
          closeSlashMenu();
          return;
        }
        const mathPopover = document.getElementById('inline-math-popover');
        if (mathPopover && mathPopover.classList.contains('open')) {
          e.preventDefault();
          closeInlineMathPopover();
          return;
        }
        const previewDrawer = document.getElementById('history-preview-drawer');
        if (previewDrawer && previewDrawer.style.display !== 'none') {
          e.preventDefault();
          closeHistoryPreview();
          return;
        }
        const inNoteBar = document.getElementById('in-note-search-bar');
        if (inNoteBar && inNoteBar.style.display !== 'none' && inNoteBar.style.display !== '') {
          e.preventDefault();
          closeInNoteSearch();
          return;
        }
        const appearancePopover = document.getElementById('page-appearance-popover');
        if (appearancePopover && appearancePopover.classList.contains('open')) {
          e.preventDefault();
          closePageAppearancePopover();
          return;
        }
        if (state.isHistoryPanelOpen) {
          e.preventDefault();
          toggleHistoryPanel(false);
          return;
        }
        return;
      }

      // 2.5 Atajo F3 para buscar dentro de la nota actual (estilo navegador)
      if (e.key === 'F3') {
        e.preventDefault();
        e.stopPropagation();
        const bar = document.getElementById('in-note-search-bar');
        if (bar && bar.style.display !== 'none' && bar.style.display !== '' && inNoteSearchMatches.length > 0) {
          inNoteSearchNav(e.shiftKey ? -1 : 1);
        } else {
          openInNoteSearch();
        }
        return;
      }

      // 3. Evaluar si la combinación presionada coincide con algún atajo global registrado
      const pressedCombo = normalizeKeyboardEventToCombo(e);
      if (!pressedCombo) return;

      const matched = DEFAULT_SHORTCUTS_REGISTRY.find(item => {
        const activeCombo = getActiveShortcutCombo(item.id);
        if (activeCombo.toLowerCase() === pressedCombo.toLowerCase()) return true;
        if (!customShortcutsMap[item.id] && item.altCombo && item.altCombo.toLowerCase() === pressedCombo.toLowerCase()) {
          return true;
        }
        return false;
      });

      if (!matched) return;

      // Si el atajo es de ámbito 'editor', solo interceptarlo cuando el foco está en el lienzo del editor
      if (matched.scope === 'editor') {
        const canvas = document.getElementById('rich-editor-canvas');
        if (!canvas || !canvas.contains(document.activeElement)) {
          return;
        }
      }

      e.preventDefault();
      e.stopPropagation();
      matched.action();
    }, true);

    /* ============================================================================
       PANEL LATERAL DERECHO OCULTABLE: HISTORIAL DE EDICIONES SQLITE (Ctrl+H)
       ============================================================================ */
    function getLocalHistoryFallbackMap() {
      try {
        const raw = localStorage.getItem('notejs_history_fallback_v1');
        return raw ? JSON.parse(raw) : {};
      } catch (_) {
        return {};
      }
    }

    function saveLocalHistoryFallbackMap(mapObj) {
      try {
        localStorage.setItem('notejs_history_fallback_v1', JSON.stringify(mapObj));
      } catch (_) {}
    }

    function stripHtmlToPlainText(htmlStr) {
      if (!htmlStr) return '';
      const temp = document.createElement('div');
      temp.innerHTML = htmlStr;
      temp.querySelectorAll('.note-embedded-card, .note-image-toolbar, .img-size-badge').forEach(el => el.remove());
      return (temp.textContent || temp.innerText || '').replace(/\s+/g, ' ').trim();
    }

    function recordLocalHistoryFallback(note, summary = 'Edición guardada', force = false) {
      if (!note || !note.id) return;
      const map = getLocalHistoryFallbackMap();
      const key = String(note.id);
      const list = Array.isArray(map[key]) ? map[key] : [];
      const now = Date.now();
      const snapClone = JSON.parse(JSON.stringify(note));

      if (list.length > 0 && !force) {
        const latest = list[0];
        const sameContent =
          latest.title === note.title &&
          latest.folder === note.folder &&
          latest.tags === note.tags &&
          latest.content === note.content;
        if (sameContent) return;

        if (now - (latest.createdAt || 0) < 12000 && latest.summary === 'Edición guardada') {
          latest.title = note.title || 'Sin título';
          latest.folder = note.folder || 'Personal';
          latest.tags = note.tags || '';
          latest.content = note.content || '';
          latest.createdAt = now;
          latest.snapshot = snapClone;
          map[key] = list;
          saveLocalHistoryFallbackMap(map);
          return;
        }
      }

      const newEntry = {
        id: now + Math.floor(Math.random() * 999),
        noteId: note.id,
        title: note.title || 'Sin título',
        folder: note.folder || 'Personal',
        tags: note.tags || '',
        content: note.content || '',
        summary: list.length === 0 ? 'Versión inicial' : summary,
        createdAt: now,
        snapshot: snapClone
      };

      list.unshift(newEntry);
      map[key] = list.slice(0, 40);
      saveLocalHistoryFallbackMap(map);
    }

    function toggleHistoryPanel(forceState) {
      const panel = document.getElementById('panel-history');
      if (!panel) return;

      const nextState = typeof forceState === 'boolean' ? forceState : !state.isHistoryPanelOpen;
      state.isHistoryPanelOpen = nextState;
      panel.classList.toggle('collapsed', !nextState);

      const topBtn = document.getElementById('btn-top-history');
      const formatBtn = document.getElementById('btn-format-history');
      if (topBtn) topBtn.classList.toggle('active', nextState);
      if (formatBtn) formatBtn.classList.toggle('active', nextState);

      if (nextState) {
        refreshActiveNoteHistory();
        showToast('Historial de ediciones abierto (Ctrl+H)', '🕒');
      } else {
        closeHistoryPreview();
      }
    }

    async function refreshActiveNoteHistory() {
      const note = getActiveNote();
      if (!note) return;

      const subtitle = document.getElementById('history-note-subtitle');
      if (subtitle) {
        subtitle.textContent = `${note.emoji || '📝'} ${note.title || 'Sin título'} · SQLite`;
      }

      let historyList = [];
      try {
        let data = null;
        if (hasPyWebViewBridge() && typeof window.pywebview.api.get_note_history === 'function') {
          data = await window.pywebview.api.get_note_history(note.id);
        } else {
          const res = await fetch(`/api/notes/${note.id}/history`, { cache: 'no-store' });
          if (res.ok) {
            data = await res.json();
          }
        }
        if (data && data.ok && Array.isArray(data.history)) {
          historyList = data.history;
        }
      } catch (_) {}

      if (!historyList.length) {
        recordLocalHistoryFallback(note, 'Versión inicial', false);
        const map = getLocalHistoryFallbackMap();
        historyList = map[String(note.id)] || [];
      }

      state.activeNoteHistory = historyList;
      renderHistoryTimeline();
    }

    async function createManualNoteSnapshot() {
      const note = getActiveNote();
      if (!note) return;

      note.updatedAt = Date.now();
      const summaryLabel = 'Punto de restauración manual';
      recordLocalHistoryFallback(note, summaryLabel, true);

      try {
        let data = null;
        if (hasPyWebViewBridge() && typeof window.pywebview.api.create_note_snapshot === 'function') {
          data = await window.pywebview.api.create_note_snapshot(note, summaryLabel);
        } else {
          const res = await fetch(`/api/notes/${note.id}/history`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ note, summary: summaryLabel })
          });
          if (res.ok) {
            data = await res.json();
          }
        }

        if (data && data.ok && Array.isArray(data.history)) {
          state.activeNoteHistory = data.history;
          setSyncStatus('synced');
        } else {
          const map = getLocalHistoryFallbackMap();
          state.activeNoteHistory = map[String(note.id)] || [];
        }
      } catch (_) {
        const map = getLocalHistoryFallbackMap();
        state.activeNoteHistory = map[String(note.id)] || [];
      }

      renderHistoryTimeline();
      showToast('Punto de restauración guardado en SQLite', '💾');
    }

    function formatRelativeHistoryTime(ts) {
      if (!ts) return 'Hace instantes';
      const diffSec = Math.max(0, Math.floor((Date.now() - Number(ts)) / 1000));
      if (diffSec < 15) return 'Justo ahora';
      if (diffSec < 60) return `Hace ${diffSec} seg`;
      const diffMin = Math.floor(diffSec / 60);
      if (diffMin < 60) return `Hace ${diffMin} min`;
      const diffHr = Math.floor(diffMin / 60);
      if (diffHr < 24) return `Hace ${diffHr} h`;
      const d = new Date(Number(ts));
      return d.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
    }

    function previewHistoryVersion(versionId) {
      const ver = state.activeNoteHistory.find(v => Number(v.id) === Number(versionId));
      if (!ver) return;

      state.previewingVersionId = Number(versionId);
      const drawer = document.getElementById('history-preview-drawer');
      const titleEl = document.getElementById('history-preview-title');
      const metaEl = document.getElementById('history-preview-meta');
      const bodyEl = document.getElementById('history-preview-body');
      const revertBtn = document.getElementById('history-preview-revert-btn');

      if (!drawer || !titleEl || !metaEl || !bodyEl || !revertBtn) return;

      const snap = ver.snapshot || {};
      const dateStr = new Date(Number(ver.createdAt || Date.now())).toLocaleString('es-ES', {
        day: '2-digit',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });

      const plainText = stripHtmlToPlainText(ver.content || snap.content || '') || '(Sin texto en el lienzo principal)';
      const activeBlocks = [];
      if (snap.showCallout) activeBlocks.push('💡 Callout');
      if (snap.showQuote) activeBlocks.push('❝ Cita');
      if (snap.showToggle) activeBlocks.push('▶ Toggle');
      if (snap.showCode) activeBlocks.push('</> Código');
      if (snap.showKanban) activeBlocks.push(`📊 Kanban (${(snap.kanban || []).length})`);
      if (snap.showTable) activeBlocks.push(`▦ Tabla (${(snap.tableRows || []).length} filas)`);
      if (snap.showChecklist) activeBlocks.push(`☑ Checklist (${(snap.checklists || []).length})`);
      if (snap.katex) activeBlocks.push('∑ KaTeX');

      titleEl.textContent = `${snap.emoji || '📝'} ${ver.title || 'Sin título'}`;
      metaEl.textContent = `Versión #${ver.id} · ${dateStr} · Carpeta: ${ver.folder || 'Personal'}`;
      bodyEl.textContent = plainText + (activeBlocks.length ? `\n\n[Bloques activos: ${activeBlocks.join(', ')}]` : '');
      revertBtn.onclick = () => revertToHistoryVersion(ver.id);

      drawer.style.display = 'flex';
      renderHistoryTimeline();
    }

    function closeHistoryPreview() {
      state.previewingVersionId = null;
      const drawer = document.getElementById('history-preview-drawer');
      if (drawer) drawer.style.display = 'none';
      if (state.isHistoryPanelOpen) {
        renderHistoryTimeline();
      }
    }

    async function revertToHistoryVersion(versionId) {
      const note = getActiveNote();
      if (!note) return;

      const targetVer = state.activeNoteHistory.find(v => Number(v.id) === Number(versionId));
      if (!targetVer) return;

      let restoredNoteObj = null;
      let updatedHistory = null;

      try {
        let data = null;
        if (hasPyWebViewBridge() && typeof window.pywebview.api.revert_note_version === 'function') {
          data = await window.pywebview.api.revert_note_version(note.id, versionId);
        } else {
          const res = await fetch(`/api/notes/${note.id}/revert`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ versionId })
          });
          if (res.ok) {
            data = await res.json();
          }
        }

        if (data && data.ok && data.note) {
          restoredNoteObj = data.note;
          updatedHistory = data.history;
          setSyncStatus('synced');
        }
      } catch (_) {}

      // Fallback local si el servidor estuvo offline
      if (!restoredNoteObj) {
        recordLocalHistoryFallback(note, 'Respaldo previo a reversión', true);
        const snap = targetVer.snapshot && Object.keys(targetVer.snapshot).length ? targetVer.snapshot : targetVer;
        restoredNoteObj = {
          ...JSON.parse(JSON.stringify(snap)),
          id: note.id,
          title: targetVer.title || snap.title || 'Sin título',
          folder: targetVer.folder || snap.folder || 'Personal',
          tags: targetVer.tags !== undefined ? targetVer.tags : (snap.tags || ''),
          content: targetVer.content !== undefined ? targetVer.content : (snap.content || ''),
          updatedAt: Date.now()
        };
        recordLocalHistoryFallback(restoredNoteObj, `Revertido a versión #${versionId}`, true);
        const map = getLocalHistoryFallbackMap();
        updatedHistory = map[String(note.id)] || [];
      }

      // Actualizar la nota en state.notes
      const idx = state.notes.findIndex(n => n.id === note.id);
      if (idx !== -1) {
        state.notes[idx] = { ...state.notes[idx], ...restoredNoteObj, id: note.id };
      }
      localStorage.setItem('notejs_desktop_notion_v9', JSON.stringify(state.notes));

      closeHistoryPreview();
      renderFolders();
      renderNotesList();
      loadActiveNote();

      if (Array.isArray(updatedHistory)) {
        state.activeNoteHistory = updatedHistory;
        renderHistoryTimeline();
      } else {
        refreshActiveNoteHistory();
      }

      showToast(`Nota revertida a la versión del ${new Date(Number(targetVer.createdAt || Date.now())).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}`, '↺');
    }

    async function deleteHistoryVersion(versionId, ev) {
      if (ev) ev.stopPropagation();
      const note = getActiveNote();
      if (!note) return;

      try {
        if (hasPyWebViewBridge() && typeof window.pywebview.api.delete_note_version === 'function') {
          const data = await window.pywebview.api.delete_note_version(note.id, versionId);
          if (data && data.ok && Array.isArray(data.history)) {
            state.activeNoteHistory = data.history;
          }
        } else {
          const res = await fetch(`/api/notes/${note.id}/history/${versionId}`, { method: 'DELETE' });
          if (res.ok) {
            const data = await res.json();
            if (data && data.ok && Array.isArray(data.history)) {
              state.activeNoteHistory = data.history;
            }
          }
        }
      } catch (_) {}

      const map = getLocalHistoryFallbackMap();
      if (Array.isArray(map[String(note.id)])) {
        map[String(note.id)] = map[String(note.id)].filter(v => Number(v.id) !== Number(versionId));
        saveLocalHistoryFallbackMap(map);
      }

      if (state.previewingVersionId === Number(versionId)) {
        closeHistoryPreview();
      }
      refreshActiveNoteHistory();
      showToast('Versión eliminada del historial', '🗑');
    }

    function renderHistoryTimeline() {
      const container = document.getElementById('history-list-container');
      const countEl = document.getElementById('history-version-count');
      if (!container) return;

      const list = Array.isArray(state.activeNoteHistory) ? state.activeNoteHistory : [];
      if (countEl) {
        countEl.textContent = `${list.length} ${list.length === 1 ? 'versión en SQLite' : 'versiones en SQLite'}`;
      }

      if (!list.length) {
        container.innerHTML = `
          <div style="text-align:center; padding:28px 14px; color:var(--text-muted); font-size:12px; line-height:1.5;">
            <div style="font-size:22px; margin-bottom:6px;">🕒</div>
            <div>Aún no hay versiones registradas para esta nota.</div>
            <div style="margin-top:4px; font-size:11px;">Edita la nota o pulsa <strong>+ Guardar versión actual</strong> para crear un punto de restauración en SQLite.</div>
          </div>
        `;
        return;
      }

      container.innerHTML = list.map((ver, idx) => {
        const isLatest = idx === 0;
        const isPreviewing = state.previewingVersionId === Number(ver.id);
        const isManual = String(ver.summary || '').toLowerCase().includes('manual') || String(ver.summary || '').toLowerCase().includes('revertido');
        const timeFormatted = new Date(Number(ver.createdAt || Date.now())).toLocaleTimeString('es-ES', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        });
        const relTime = formatRelativeHistoryTime(ver.createdAt);
        const plainSnippet = stripHtmlToPlainText(ver.content || (ver.snapshot && ver.snapshot.content) || '') || 'Sin contenido de texto...';
        const charCount = plainSnippet === 'Sin contenido de texto...' ? 0 : plainSnippet.length;
        const snap = ver.snapshot || {};

        const blockBadges = [];
        if (snap.showKanban) blockBadges.push('📊 Kanban');
        if (snap.showTable) blockBadges.push('▦ Tabla');
        if (snap.katex) blockBadges.push('∑ KaTeX');
        if (snap.showChecklist) blockBadges.push('☑ Checklist');

        return `
          <div class="history-version-card ${isLatest ? 'current-version' : ''} ${isPreviewing ? 'previewing' : ''}">
            <div class="history-card-top">
              <span class="history-version-badge ${isLatest ? 'latest' : (isManual ? 'manual' : '')}">
                ${isLatest ? '● Actual en SQLite' : (isManual ? '★ Punto clave' : `Versión #${list.length - idx}`)}
              </span>
              <div style="display:flex; align-items:center; gap:4px;">
                <span class="history-card-time tabular-nums" title="${timeFormatted}">${relTime} · ${timeFormatted}</span>
                ${list.length > 1 ? `<button class="history-btn-delete" onclick="deleteHistoryVersion(${ver.id}, event)" title="Eliminar esta versión de SQLite">✕</button>` : ''}
              </div>
            </div>

            <div class="history-card-summary">
              <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${ver.summary || 'Edición guardada'}</span>
            </div>

            <div class="history-card-snippet">${plainSnippet.slice(0, 130)}</div>

            <div class="history-card-tags-row">
              <span class="history-mini-pill">📁 ${ver.folder || 'Personal'}</span>
              <span class="history-mini-pill tabular-nums">${charCount} car.</span>
              ${blockBadges.map(b => `<span class="history-mini-pill">${b}</span>`).join('')}
            </div>

            <div class="history-card-actions">
              <button class="history-btn-preview" onclick="previewHistoryVersion(${ver.id})" title="Previsualizar el contenido completo de esta versión">
                👁️ Vista previa
              </button>
              <button class="history-btn-revert" onclick="revertToHistoryVersion(${ver.id})" title="Restaurar la nota a esta versión guardada en SQLite">
                ↺ ${isLatest ? 'Recargar versión' : 'Revertir aquí'}
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    /* ============================================================================
       BLOQUES DE IMAGEN REDIMENSIONABLES EN EL LIENZO (URL Web, Ruta Local PC, Pegado y Arrastre)
       ============================================================================ */
    let imageModalState = {
      tab: 'url',
      resolvedDataUri: '',
      rawSource: '',
      width: '75%',
      align: 'center',
      editingBlockEl: null
    };
    let activeCtxImageBlock = null;
    let imageSourceDebounceTimer = null;

    const SAMPLE_IMAGE_PRESETS = {
      architecture: {
        caption: 'Figura 1: Arquitectura de 3 Capas en Note JS (PyWebView + SQLite & Peewee ORM)',
        dataUri: 'data:image/svg+xml;utf8,' + encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="880" height="420" viewBox="0 0 880 420">
          <defs>
            <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#0f172a"/>
              <stop offset="100%" stop-color="#1e293b"/>
            </linearGradient>
            <linearGradient id="amber" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stop-color="#f59e0b"/>
              <stop offset="100%" stop-color="#fbbf24"/>
            </linearGradient>
          </defs>
          <rect width="880" height="420" rx="18" fill="url(#bg)"/>
          <text x="440" y="48" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="20" font-weight="800" text-anchor="middle">Arquitectura Desktop: PyWebView + SQLite &amp; Peewee ORM</text>
          <rect x="55" y="95" width="220" height="250" rx="14" fill="#1e293b" stroke="#3b82f6" stroke-width="2.5"/>
          <text x="165" y="138" fill="#60a5fa" font-family="system-ui, sans-serif" font-size="16" font-weight="700" text-anchor="middle">Frontend Lienzo Rico</text>
          <text x="165" y="175" fill="#cbd5e1" font-family="monospace" font-size="13" text-anchor="middle">Bloques Notion + KaTeX</text>
          <text x="165" y="205" fill="#cbd5e1" font-family="monospace" font-size="13" text-anchor="middle">Imágenes Redimensionables</text>
          <text x="165" y="235" fill="#cbd5e1" font-family="monospace" font-size="13" text-anchor="middle">Fórmulas 2.0 &amp; Kanban</text>
          <rect x="330" y="95" width="220" height="250" rx="14" fill="#1e293b" stroke="#f59e0b" stroke-width="2.5"/>
          <text x="440" y="138" fill="#fbbf24" font-family="system-ui, sans-serif" font-size="16" font-weight="700" text-anchor="middle">Puente PyWebView</text>
          <text x="440" y="175" fill="#cbd5e1" font-family="monospace" font-size="13" text-anchor="middle">window.pywebview.api</text>
          <text x="440" y="205" fill="#cbd5e1" font-family="monospace" font-size="13" text-anchor="middle">Resolución Rutas PC</text>
          <text x="440" y="235" fill="#cbd5e1" font-family="monospace" font-size="13" text-anchor="middle">Sin Electron (Nativo)</text>
          <rect x="605" y="95" width="220" height="250" rx="14" fill="#1e293b" stroke="#10b981" stroke-width="2.5"/>
          <text x="715" y="138" fill="#34d399" font-family="system-ui, sans-serif" font-size="16" font-weight="700" text-anchor="middle">SQLite + Peewee WAL</text>
          <text x="715" y="175" fill="#cbd5e1" font-family="monospace" font-size="13" text-anchor="middle">notejs.db (Transaccional)</text>
          <text x="715" y="205" fill="#cbd5e1" font-family="monospace" font-size="13" text-anchor="middle">Historial Ctrl+H</text>
          <text x="715" y="235" fill="#cbd5e1" font-family="monospace" font-size="13" text-anchor="middle">Snapshots Instantáneos</text>
          <path d="M 275 220 L 330 220" stroke="url(#amber)" stroke-width="4"/>
          <path d="M 550 220 L 605 220" stroke="url(#amber)" stroke-width="4"/>
        </svg>`)
      },
      circuit: {
        caption: 'Figura 2: Distribución de Probabilidad Cuántica y Oscilador Armónico',
        dataUri: 'data:image/svg+xml;utf8,' + encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="860" height="400" viewBox="0 0 860 400">
          <rect width="860" height="400" rx="16" fill="#090d16"/>
          <g stroke="#1e293b" stroke-width="1">
            <line x1="60" y1="80" x2="800" y2="80"/><line x1="60" y1="160" x2="800" y2="160"/>
            <line x1="60" y1="240" x2="800" y2="240"/><line x1="60" y1="320" x2="800" y2="320"/>
            <line x1="200" y1="40" x2="200" y2="360"/><line x1="430" y1="40" x2="430" y2="360"/><line x1="660" y1="40" x2="660" y2="360"/>
          </g>
          <path d="M 60 320 Q 245 315 310 180 T 430 65 T 550 180 T 800 320" fill="rgba(59,130,246,0.18)" stroke="#3b82f6" stroke-width="3.5"/>
          <path d="M 60 240 C 160 90, 290 390, 430 240 C 570 90, 700 390, 800 240" fill="none" stroke="#f59e0b" stroke-width="3" stroke-dasharray="8 5"/>
          <text x="430" y="38" fill="#e2e8f0" font-family="monospace" font-size="16" font-weight="700" text-anchor="middle">|Ψ(x,t)|² — Densidad de Estado Cuántico</text>
        </svg>`)
      },
      workspace: {
        caption: 'Fotografía de referencia: Entorno de ingeniería y documentación técnica',
        dataUri: 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1000&q=80'
      }
    };

    function escapeHtmlAttr(str) {
      return String(str || '')
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    }

    function saveCaretRangeFromMouseEvent(e) {
      const canvas = document.getElementById('rich-editor-canvas');
      if (!canvas) return;
      let range = null;
      if (document.caretRangeFromPoint && e) {
        range = document.caretRangeFromPoint(e.clientX, e.clientY);
      } else if (document.caretPositionFromPoint && e) {
        const pos = document.caretPositionFromPoint(e.clientX, e.clientY);
        if (pos && pos.offsetNode) {
          range = document.createRange();
          range.setStart(pos.offsetNode, pos.offset);
          range.collapse(true);
        }
      }
      if (range && canvas.contains(range.startContainer)) {
        savedEditorRange = range;
      }
    }

    function isLikelyLocalFilePath(rawStr) {
      if (!rawStr) return false;
      const s = rawStr.trim().replace(/^["']|["']$/g, '');
      if (/^file:\/\//i.test(s)) return true;
      if (/^[a-zA-Z]:[\\/]/.test(s)) return true;
      if (/^\\\\[^\\]+/.test(s)) return true;
      if (/^(?:\/|~\/|\.\.?\/).+\.(?:png|jpe?g|gif|webp|svg|bmp|ico|avif)$/i.test(s)) return true;
      if (/^[^https?:].+\.(?:png|jpe?g|gif|webp|svg|bmp|ico|avif)$/i.test(s) && !s.startsWith('data:image/')) return true;
      return false;
    }

    function isLikelyDirectImageUrl(rawStr) {
      if (!rawStr) return false;
      const s = rawStr.trim();
      if (s.startsWith('data:image/')) return true;
      if (/^https?:\/\/[^\s]+\.(?:png|jpe?g|gif|webp|svg|bmp|ico|avif)(?:\?[^\s]*)?(#[^\s]*)?$/i.test(s)) return true;
      if (/^https?:\/\/images\.unsplash\.com\/photo-[^\s]+$/i.test(s)) return true;
      return false;
    }

    async function resolveImageSourceInput(rawInput) {
      const cleaned = (rawInput || '').trim().replace(/^["']|["']$/g, '');
      if (!cleaned) {
        return { ok: false, error: 'Introduce una URL de imagen o una ruta local' };
      }

      if (cleaned.startsWith('data:image/') || cleaned.startsWith('blob:')) {
        return { ok: true, dataUri: cleaned, rawSource: cleaned, sourceType: 'data' };
      }

      if (/^https?:\/\//i.test(cleaned)) {
        return { ok: true, dataUri: cleaned, rawSource: cleaned, sourceType: 'url' };
      }

      // Ruta local del sistema: resolver mediante PyWebView o endpoint Python /api/images/resolve
      try {
        let data = null;
        if (hasPyWebViewBridge() && typeof window.pywebview.api.resolve_local_image === 'function') {
          data = await window.pywebview.api.resolve_local_image(cleaned);
        } else {
          const res = await fetch('/api/images/resolve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: cleaned })
          });
          data = await res.json();
        }
        if (data && data.ok && data.dataUri) {
          return {
            ok: true,
            dataUri: data.dataUri,
            rawSource: data.resolvedPath || cleaned,
            fileName: data.fileName || '',
            sourceType: 'local'
          };
        }
        return {
          ok: false,
          error: (data && data.error) || `No se pudo leer la imagen en la ruta local: ${cleaned}`
        };
      } catch (err) {
        return {
          ok: false,
          error: `Error al procesar ruta local: ${cleaned}`
        };
      }
    }

    function openImageInsertModal(existingBlockEl = null) {
      const modal = document.getElementById('image-insert-modal');
      if (!modal) return;

      const canvas = document.getElementById('rich-editor-canvas');
      const sel = window.getSelection();
      if (!existingBlockEl && sel && sel.rangeCount > 0 && canvas && canvas.contains(sel.anchorNode)) {
        savedEditorRange = sel.getRangeAt(0).cloneRange();
      }

      imageModalState.editingBlockEl = existingBlockEl || null;
      const titleEl = document.getElementById('image-modal-title');
      const confirmBtn = document.getElementById('btn-confirm-insert-image');
      const srcInput = document.getElementById('image-source-input');
      const capInput = document.getElementById('image-caption-input');

      if (existingBlockEl) {
        const currentImg = existingBlockEl.querySelector('.note-image-el');
        const currentSrc = currentImg ? currentImg.getAttribute('src') : '';
        const rawSrc = existingBlockEl.getAttribute('data-raw-source') || currentSrc;
        const currentCap = existingBlockEl.querySelector('.note-image-caption')?.getAttribute('data-caption') || '';
        const currentWidth = existingBlockEl.getAttribute('data-width') || '75%';
        const currentAlign = existingBlockEl.getAttribute('data-align') || 'center';

        imageModalState.resolvedDataUri = currentSrc;
        imageModalState.rawSource = rawSrc;
        imageModalState.width = currentWidth;
        imageModalState.align = currentAlign;

        if (titleEl) titleEl.textContent = 'Editar Bloque de Imagen Redimensionable';
        if (confirmBtn) confirmBtn.textContent = 'Guardar cambios en la imagen';
        if (srcInput) srcInput.value = rawSrc.startsWith('data:image/') ? '' : rawSrc;
        if (capInput) capInput.value = currentCap;
        setImageModalWidth(currentWidth);
        setImageModalAlign(currentAlign);
        renderImageModalPreview(currentSrc, rawSrc.startsWith('data:image/') ? 'Imagen embebida (Data URI)' : rawSrc);
      } else {
        imageModalState.resolvedDataUri = '';
        imageModalState.rawSource = '';
        imageModalState.width = '75%';
        imageModalState.align = 'center';

        if (titleEl) titleEl.textContent = 'Insertar Bloque de Imagen Redimensionable';
        if (confirmBtn) confirmBtn.textContent = '+ Insertar en el documento';
        if (srcInput) srcInput.value = '';
        if (capInput) capInput.value = '';
        setImageModalWidth('75%');
        setImageModalAlign('center');
        renderImageModalPreview('', 'Esperando URL o ruta local...');
      }

      switchImageModalTab('url');
      modal.classList.add('open');
      setTimeout(() => {
        if (srcInput) srcInput.focus();
      }, 45);
    }

    function closeImageInsertModal() {
      const modal = document.getElementById('image-insert-modal');
      if (modal) modal.classList.remove('open');
      imageModalState.editingBlockEl = null;
    }

    function switchImageModalTab(tab) {
      imageModalState.tab = tab;
      const tabUrl = document.getElementById('img-tab-url');
      const tabFile = document.getElementById('img-tab-file');
      const panelUrl = document.getElementById('img-panel-url');
      const panelFile = document.getElementById('img-panel-file');
      if (tabUrl) tabUrl.classList.toggle('active', tab === 'url');
      if (tabFile) tabFile.classList.toggle('active', tab === 'file');
      if (panelUrl) panelUrl.style.display = tab === 'url' ? 'block' : 'none';
      if (panelFile) panelFile.style.display = tab === 'file' ? 'block' : 'none';
    }

    function setImageModalWidth(widthVal) {
      imageModalState.width = widthVal;
      document.querySelectorAll('#image-modal-width-pills .img-pill-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-width') === widthVal);
      });
    }

    function setImageModalAlign(alignVal) {
      imageModalState.align = alignVal;
      document.querySelectorAll('#image-modal-align-pills .img-pill-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-align') === alignVal);
      });
    }

    function handleImageSourceInput(val) {
      clearTimeout(imageSourceDebounceTimer);
      const trimmed = (val || '').trim();
      if (!trimmed) {
        imageModalState.resolvedDataUri = '';
        imageModalState.rawSource = '';
        renderImageModalPreview('', 'Esperando URL o ruta local...');
        return;
      }
      imageSourceDebounceTimer = setTimeout(() => {
        resolveAndPreviewImageInput();
      }, 260);
    }

    async function resolveAndPreviewImageInput() {
      const srcInput = document.getElementById('image-source-input');
      const raw = srcInput ? srcInput.value.trim() : '';
      if (!raw) return;

      const statusEl = document.getElementById('image-preview-status');
      if (statusEl) statusEl.textContent = 'Procesando imagen...';

      const res = await resolveImageSourceInput(raw);
      if (res.ok && res.dataUri) {
        imageModalState.resolvedDataUri = res.dataUri;
        imageModalState.rawSource = res.rawSource || raw;
        const capInput = document.getElementById('image-caption-input');
        if (capInput && !capInput.value && res.fileName) {
          capInput.value = res.fileName;
        }
        renderImageModalPreview(
          res.dataUri,
          res.sourceType === 'local' ? `Ruta local procesada: ${res.fileName || res.rawSource}` : 'URL lista para insertar'
        );
      } else {
        renderImageModalPreview('', res.error || 'No se pudo cargar la imagen', true);
      }
    }

    function renderImageModalPreview(dataUri, statusText, isError = false) {
      const stage = document.getElementById('image-modal-preview-stage');
      const statusEl = document.getElementById('image-preview-status');
      if (statusEl) {
        statusEl.textContent = statusText || '';
        statusEl.style.color = isError ? 'var(--danger)' : 'var(--accent-amber)';
      }
      if (!stage) return;

      if (!dataUri) {
        stage.innerHTML = `
          <div style="color:${isError ? 'var(--danger)' : 'var(--text-muted)'}; font-size:12px; text-align:center; padding:22px 12px;">
            ${isError ? '⚠️ ' + escapeHtmlAttr(statusText) : 'Pega una URL de imagen, introduce una ruta local o elige un ejemplo rápido para previsualizar.'}
          </div>
        `;
        return;
      }

      stage.innerHTML = `<img id="image-modal-preview-img" src="${escapeHtmlAttr(dataUri)}" alt="Vista previa" />`;
      const imgEl = document.getElementById('image-modal-preview-img');
      if (imgEl) {
        imgEl.onload = () => {
          if (statusEl) {
            statusEl.textContent = `${statusText} (${imgEl.naturalWidth}×${imgEl.naturalHeight} px)`;
            statusEl.style.color = 'var(--success)';
          }
        };
        imgEl.onerror = () => {
          if (statusEl) {
            statusEl.textContent = 'No se pudo cargar la imagen desde esa URL';
            statusEl.style.color = 'var(--danger)';
          }
        };
      }
    }

    function applySampleImagePreset(key) {
      const preset = SAMPLE_IMAGE_PRESETS[key];
      if (!preset) return;
      imageModalState.resolvedDataUri = preset.dataUri;
      imageModalState.rawSource = preset.dataUri.startsWith('http') ? preset.dataUri : `preset:${key}`;
      const srcInput = document.getElementById('image-source-input');
      const capInput = document.getElementById('image-caption-input');
      if (srcInput) {
        srcInput.value = preset.dataUri.startsWith('http') ? preset.dataUri : `[Diagrama SVG Integrado: ${key}]`;
      }
      if (capInput) {
        capInput.value = preset.caption;
      }
      renderImageModalPreview(preset.dataUri, 'Ejemplo cargado y listo para insertar');
    }

    function triggerHiddenImageFileInput() {
      const fileInput = document.getElementById('image-file-picker');
      if (fileInput) {
        fileInput.value = '';
        fileInput.click();
      }
    }

    async function openNativeOrBrowserFilePicker() {
      if (hasPyWebViewBridge() && typeof window.pywebview.api.pick_local_image === 'function') {
        try {
          const res = await window.pywebview.api.pick_local_image();
          if (res && res.ok && res.dataUri) {
            imageModalState.resolvedDataUri = res.dataUri;
            imageModalState.rawSource = res.resolvedPath || res.fileName || 'archivo_local';
            const srcInput = document.getElementById('image-source-input');
            const capInput = document.getElementById('image-caption-input');
            if (srcInput && res.resolvedPath) srcInput.value = res.resolvedPath;
            if (capInput && !capInput.value && res.fileName) capInput.value = res.fileName;
            renderImageModalPreview(res.dataUri, `Archivo nativo cargado: ${res.fileName || ''}`);
            return;
          }
        } catch (_) {}
      }
      triggerHiddenImageFileInput();
    }

    function handleImageFilePickerChange(e) {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      loadModalFileIntoPreview(file);
    }

    function handleModalDropzoneDragOver(e) {
      e.preventDefault();
      e.stopPropagation();
      const dz = document.getElementById('image-modal-dropzone');
      if (dz) dz.classList.add('drag-over');
    }

    function handleModalDropzoneDragLeave(e) {
      e.preventDefault();
      const dz = document.getElementById('image-modal-dropzone');
      if (dz) dz.classList.remove('drag-over');
    }

    function handleModalDropzoneDrop(e) {
      e.preventDefault();
      e.stopPropagation();
      const dz = document.getElementById('image-modal-dropzone');
      if (dz) dz.classList.remove('drag-over');
      const file = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
      if (file) {
        loadModalFileIntoPreview(file);
      }
    }

    function loadModalFileIntoPreview(file) {
      if (!file.type || !file.type.startsWith('image/')) {
        renderImageModalPreview('', 'El archivo seleccionado no es una imagen válida', true);
        return;
      }
      const reader = new FileReader();
      reader.onload = (ev) => {
        const dataUri = ev.target.result;
        imageModalState.resolvedDataUri = dataUri;
        imageModalState.rawSource = file.name;
        const srcInput = document.getElementById('image-source-input');
        const capInput = document.getElementById('image-caption-input');
        if (srcInput) srcInput.value = file.name;
        if (capInput && !capInput.value) {
          capInput.value = file.name.replace(/\.[^/.]+$/, '');
        }
        renderImageModalPreview(dataUri, `Archivo local procesado: ${file.name}`);
      };
      reader.readAsDataURL(file);
    }

    async function confirmInsertImageBlock() {
      const srcInput = document.getElementById('image-source-input');
      const capInput = document.getElementById('image-caption-input');
      const rawVal = srcInput ? srcInput.value.trim() : '';
      const caption = capInput ? capInput.value.trim() : '';

      let finalDataUri = imageModalState.resolvedDataUri;
      let finalRawSource = imageModalState.rawSource || rawVal;

      if (!finalDataUri && rawVal && !rawVal.startsWith('[Diagrama SVG')) {
        const res = await resolveImageSourceInput(rawVal);
        if (!res.ok || !res.dataUri) {
          renderImageModalPreview('', res.error || 'No se pudo procesar la ruta o URL de la imagen', true);
          showToast(res.error || 'Ruta o URL de imagen inválida', '⚠️');
          return;
        }
        finalDataUri = res.dataUri;
        finalRawSource = res.rawSource || rawVal;
      }

      if (!finalDataUri) {
        showToast('Selecciona o pega primero una URL o ruta local de imagen', '⚠️');
        return;
      }

      if (imageModalState.editingBlockEl) {
        updateExistingImageBlockElement(imageModalState.editingBlockEl, {
          src: finalDataUri,
          rawSource: finalRawSource,
          caption,
          width: imageModalState.width || '75%',
          align: imageModalState.align || 'center'
        });
        closeImageInsertModal();
        syncRichEditor();
        showToast('Bloque de imagen actualizado', '🖼️');
        return;
      }

      insertImageBlockIntoEditor({
        src: finalDataUri,
        rawSource: finalRawSource,
        caption,
        width: imageModalState.width || '75%',
        align: imageModalState.align || 'center'
      });
      closeImageInsertModal();
    }

    function generateResizableImageBlockHtml({ src, rawSource = '', caption = '', width = '75%', align = 'center' }) {
      const blockId = 'img-block-' + Date.now() + '-' + Math.floor(Math.random() * 1000);
      const safeSrc = escapeHtmlAttr(src);
      const safeRaw = escapeHtmlAttr(rawSource && !rawSource.startsWith('data:image/') ? rawSource : '');
      const safeCap = escapeHtmlAttr(caption);
      const safeWidth = escapeHtmlAttr(width || '75%');
      const safeAlign = escapeHtmlAttr(align || 'center');
      const hasCap = Boolean(caption && caption.trim());

      return `
        <div class="note-image-block" id="${blockId}" contenteditable="false" data-width="${safeWidth}" data-align="${safeAlign}" data-raw-source="${safeRaw}">
          <div class="note-image-figure" style="width:${safeWidth};">
            <div class="note-image-toolbar">
              <button type="button" class="img-tool-btn ${safeWidth === '25%' ? 'active' : ''}" data-img-action="width" data-val="25%" title="Ancho 25%">25%</button>
              <button type="button" class="img-tool-btn ${safeWidth === '50%' ? 'active' : ''}" data-img-action="width" data-val="50%" title="Ancho 50%">50%</button>
              <button type="button" class="img-tool-btn ${safeWidth === '75%' ? 'active' : ''}" data-img-action="width" data-val="75%" title="Ancho 75%">75%</button>
              <button type="button" class="img-tool-btn ${safeWidth === '100%' ? 'active' : ''}" data-img-action="width" data-val="100%" title="Ancho 100%">100%</button>
              <div class="img-tool-sep"></div>
              <button type="button" class="img-tool-btn ${safeAlign === 'left' ? 'active' : ''}" data-img-action="align" data-val="left" title="Alinear a la izquierda">⬅</button>
              <button type="button" class="img-tool-btn ${safeAlign === 'center' ? 'active' : ''}" data-img-action="align" data-val="center" title="Centrar imagen">⬌</button>
              <button type="button" class="img-tool-btn ${safeAlign === 'right' ? 'active' : ''}" data-img-action="align" data-val="right" title="Alinear a la derecha">➡</button>
              <div class="img-tool-sep"></div>
              <button type="button" class="img-tool-btn" data-img-action="caption" title="Editar leyenda / pie de foto">✏️</button>
              <button type="button" class="img-tool-btn" data-img-action="edit" title="Cambiar URL o ruta local">🔗</button>
              <button type="button" class="img-tool-btn" data-img-action="zoom" title="Ampliar imagen (Lightbox)">🔍</button>
              <button type="button" class="img-tool-btn danger" data-img-action="delete" title="Eliminar bloque de imagen">🗑</button>
            </div>
            <div class="note-image-wrapper">
              <div class="img-resize-handle left" data-dir="left" title="Arrastra hacia los lados para redimensionar la imagen"></div>
              <img class="note-image-el" src="${safeSrc}" alt="${safeCap || 'Imagen del documento'}" draggable="false" />
              <div class="img-resize-handle right" data-dir="right" title="Arrastra hacia los lados para redimensionar la imagen"></div>
              <span class="img-size-badge">${safeWidth}</span>
            </div>
            <div class="note-image-caption ${hasCap ? '' : 'empty-caption'}" data-caption="${safeCap}" title="Haz clic para editar el pie de imagen">
              ${hasCap ? safeCap : '+ Añadir pie de imagen...'}
            </div>
          </div>
        </div>
      `.trim();
    }

    function insertImageBlockIntoEditor(opts) {
      const canvas = document.getElementById('rich-editor-canvas');
      if (!canvas) return;

      const blockHtml = generateResizableImageBlockHtml(opts);
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = `${blockHtml}<p><br></p>`;
      const frag = document.createDocumentFragment();
      let insertedBlock = null;
      while (tempDiv.firstChild) {
        if (!insertedBlock && tempDiv.firstChild.nodeType === 1 && tempDiv.firstChild.classList.contains('note-image-block')) {
          insertedBlock = tempDiv.firstChild;
        }
        frag.appendChild(tempDiv.firstChild);
      }

      let placed = false;
      if (savedEditorRange && canvas.contains(savedEditorRange.startContainer)) {
        const existingBlock = savedEditorRange.startContainer.nodeType === 1
          ? savedEditorRange.startContainer.closest('.note-image-block, .note-embedded-card')
          : savedEditorRange.startContainer.parentElement?.closest('.note-image-block, .note-embedded-card');
        if (existingBlock) {
          existingBlock.after(frag);
        } else {
          savedEditorRange.deleteContents();
          savedEditorRange.insertNode(frag);
        }
        placed = true;
      } else {
        const sel = window.getSelection();
        if (sel && sel.rangeCount > 0 && canvas.contains(sel.anchorNode)) {
          const r = sel.getRangeAt(0);
          r.deleteContents();
          r.insertNode(frag);
          placed = true;
        }
      }

      if (!placed) {
        canvas.appendChild(frag);
      }

      savedEditorRange = null;
      syncRichEditor();
      if (insertedBlock) {
        setTimeout(() => {
          insertedBlock.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 40);
      }
      showToast('Imagen insertada como bloque redimensionable', '🖼️');
    }

    function updateExistingImageBlockElement(blockEl, { src, rawSource, caption, width, align }) {
      if (!blockEl) return;
      const fig = blockEl.querySelector('.note-image-figure');
      const img = blockEl.querySelector('.note-image-el');
      const badge = blockEl.querySelector('.img-size-badge');
      const capEl = blockEl.querySelector('.note-image-caption');

      if (src && img) img.setAttribute('src', src);
      if (rawSource !== undefined) {
        blockEl.setAttribute('data-raw-source', rawSource.startsWith('data:image/') ? '' : rawSource);
      }
      if (width) {
        blockEl.setAttribute('data-width', width);
        if (fig) fig.style.width = width;
        if (badge) badge.textContent = width;
        blockEl.querySelectorAll('.img-tool-btn[data-img-action="width"]').forEach(btn => {
          btn.classList.toggle('active', btn.getAttribute('data-val') === width);
        });
      }
      if (align) {
        blockEl.setAttribute('data-align', align);
        blockEl.querySelectorAll('.img-tool-btn[data-img-action="align"]').forEach(btn => {
          btn.classList.toggle('active', btn.getAttribute('data-val') === align);
        });
      }
      if (caption !== undefined && capEl) {
        const cleanCap = caption.trim();
        capEl.setAttribute('data-caption', cleanCap);
        capEl.textContent = cleanCap || '+ Añadir pie de imagen...';
        capEl.classList.toggle('empty-caption', !cleanCap);
        if (img) img.setAttribute('alt', cleanCap || 'Imagen del documento');
      }
    }

    function readAndInsertLocalImageFile(file) {
      if (!file || !file.type || !file.type.startsWith('image/')) return;
      const reader = new FileReader();
      reader.onload = (ev) => {
        const dataUri = ev.target.result;
        const defaultCaption = (file.name || '').replace(/\.[^/.]+$/, '');
        insertImageBlockIntoEditor({
          src: dataUri,
          rawSource: file.name || 'archivo_local',
          caption: defaultCaption,
          width: '75%',
          align: 'center'
        });
      };
      reader.readAsDataURL(file);
    }

    function openImageLightbox(src, caption = '') {
      const modal = document.getElementById('image-lightbox-modal');
      const img = document.getElementById('image-lightbox-img');
      const cap = document.getElementById('image-lightbox-caption');
      if (!modal || !img) return;
      img.src = src;
      if (cap) cap.textContent = caption || 'Vista ampliada de imagen';
      modal.classList.add('open');
    }

    function closeImageLightbox() {
      const modal = document.getElementById('image-lightbox-modal');
      if (modal) modal.classList.remove('open');
    }

    function promptEditImageBlockCaption(blockEl) {
      if (!blockEl) return;
      const capEl = blockEl.querySelector('.note-image-caption');
      const current = capEl ? (capEl.getAttribute('data-caption') || '') : '';
      const nextCap = prompt('Pie de imagen / Leyenda (deja vacío para quitar):', current);
      if (nextCap === null) return;
      updateExistingImageBlockElement(blockEl, { caption: nextCap });
      syncRichEditor();
      showToast('Pie de imagen actualizado', '✏️');
    }

    /* Eventos delegados en #rich-editor-canvas para redimensionar con el ratón, barra flotante y pegado inteligente */
    function attachImageBlockListeners() {
      const canvas = document.getElementById('rich-editor-canvas');
      if (!canvas || canvas.dataset.delegatedImageBlocks) return;
      canvas.dataset.delegatedImageBlocks = 'true';

      // 1. Pegado inteligente (Ctrl+V): Archivos de imagen del portapapeles, URLs directas de imagen o rutas locales de PC
      canvas.addEventListener('paste', async (e) => {
        const clipboard = e.clipboardData;
        if (!clipboard) return;

        // A) Verificar si el portapapeles contiene un archivo/blob binario de imagen (ej. captura de pantalla)
        const items = Array.from(clipboard.items || []);
        const imageItem = items.find(it => it.type && it.type.startsWith('image/'));
        if (imageItem) {
          const file = imageItem.getAsFile();
          if (file) {
            e.preventDefault();
            e.stopPropagation();
            const sel = window.getSelection();
            if (sel && sel.rangeCount > 0 && canvas.contains(sel.anchorNode)) {
              savedEditorRange = sel.getRangeAt(0).cloneRange();
            }
            readAndInsertLocalImageFile(file);
            return;
          }
        }

        // B) Verificar si el texto pegado es una URL de imagen o una ruta local de imagen en el PC
        const pastedText = (clipboard.getData('text/plain') || '').trim();
        if (!pastedText || pastedText.includes('\n')) return;

        if (isLikelyDirectImageUrl(pastedText)) {
          e.preventDefault();
          e.stopPropagation();
          const sel = window.getSelection();
          if (sel && sel.rangeCount > 0 && canvas.contains(sel.anchorNode)) {
            savedEditorRange = sel.getRangeAt(0).cloneRange();
          }
          insertImageBlockIntoEditor({
            src: pastedText,
            rawSource: pastedText,
            caption: '',
            width: '75%',
            align: 'center'
          });
          return;
        }

        if (isLikelyLocalFilePath(pastedText)) {
          e.preventDefault();
          e.stopPropagation();
          const sel = window.getSelection();
          if (sel && sel.rangeCount > 0 && canvas.contains(sel.anchorNode)) {
            savedEditorRange = sel.getRangeAt(0).cloneRange();
          }
          const res = await resolveImageSourceInput(pastedText);
          if (res && res.ok && res.dataUri) {
            insertImageBlockIntoEditor({
              src: res.dataUri,
              rawSource: res.rawSource || pastedText,
              caption: res.fileName || '',
              width: '75%',
              align: 'center'
            });
          } else {
            // Si la ruta local no existe en el disco, abrir el modal con la ruta precargada para que el usuario la verifique
            openImageInsertModal();
            const srcInput = document.getElementById('image-source-input');
            if (srcInput) srcInput.value = pastedText;
            renderImageModalPreview('', (res && res.error) || `No se encontró el archivo local: ${pastedText}`, true);
          }
        }
      });

      // 2. Clics en la barra de herramientas del bloque de imagen, leyenda o doble clic para zoom
      canvas.addEventListener('click', (e) => {
        const toolBtn = e.target.closest('.img-tool-btn');
        if (toolBtn) {
          e.preventDefault();
          e.stopPropagation();
          const blockEl = toolBtn.closest('.note-image-block');
          if (!blockEl) return;
          const action = toolBtn.getAttribute('data-img-action');
          const val = toolBtn.getAttribute('data-val');

          if (action === 'width' && val) {
            updateExistingImageBlockElement(blockEl, { width: val });
            syncRichEditor();
            showToast(`Ancho de imagen ajustado a ${val}`, '↔️');
          } else if (action === 'align' && val) {
            updateExistingImageBlockElement(blockEl, { align: val });
            syncRichEditor();
          } else if (action === 'caption') {
            promptEditImageBlockCaption(blockEl);
          } else if (action === 'edit') {
            openImageInsertModal(blockEl);
          } else if (action === 'zoom') {
            const img = blockEl.querySelector('.note-image-el');
            const cap = blockEl.querySelector('.note-image-caption')?.getAttribute('data-caption') || '';
            if (img) openImageLightbox(img.src, cap);
          } else if (action === 'delete') {
            blockEl.remove();
            syncRichEditor();
            showToast('Bloque de imagen eliminado', '🗑');
          }
          return;
        }

        const captionEl = e.target.closest('.note-image-caption');
        if (captionEl) {
          e.preventDefault();
          e.stopPropagation();
          const blockEl = captionEl.closest('.note-image-block');
          if (blockEl) promptEditImageBlockCaption(blockEl);
          return;
        }

        const clickedBlock = e.target.closest('.note-image-block');
        document.querySelectorAll('#rich-editor-canvas .note-image-block.selected').forEach(el => {
          if (el !== clickedBlock) el.classList.remove('selected');
        });
        if (clickedBlock) {
          clickedBlock.classList.add('selected');
        }
      });

      canvas.addEventListener('dblclick', (e) => {
        const wrapper = e.target.closest('.note-image-wrapper');
        if (wrapper && !e.target.closest('.img-resize-handle')) {
          e.preventDefault();
          e.stopPropagation();
          const blockEl = wrapper.closest('.note-image-block');
          const img = blockEl?.querySelector('.note-image-el');
          const cap = blockEl?.querySelector('.note-image-caption')?.getAttribute('data-caption') || '';
          if (img) openImageLightbox(img.src, cap);
        }
      });

      // 3. Redimensionamiento fluido arrastrando las manijas laterales (.img-resize-handle.left / .right)
      canvas.addEventListener('pointerdown', (e) => {
        const handle = e.target.closest('.img-resize-handle');
        if (!handle) return;

        e.preventDefault();
        e.stopPropagation();

        const blockEl = handle.closest('.note-image-block');
        const figureEl = blockEl?.querySelector('.note-image-figure');
        const badgeEl = blockEl?.querySelector('.img-size-badge');
        if (!blockEl || !figureEl) return;

        const dir = handle.getAttribute('data-dir') === 'left' ? -1 : 1;
        const startX = e.clientX;
        const startWidthPx = figureEl.getBoundingClientRect().width;
        const canvasWidthPx = Math.max(240, canvas.clientWidth);
        const align = blockEl.getAttribute('data-align') || 'center';
        const multiplier = align === 'center' ? 2 : 1;

        blockEl.classList.add('is-resizing', 'selected');

        const onPointerMove = (moveEv) => {
          moveEv.preventDefault();
          const deltaX = (moveEv.clientX - startX) * dir * multiplier;
          const nextPx = Math.max(140, Math.min(canvasWidthPx, Math.round(startWidthPx + deltaX)));
          const nextPct = Math.max(15, Math.min(100, Math.round((nextPx / canvasWidthPx) * 100)));

          figureEl.style.width = `${nextPx}px`;
          blockEl.setAttribute('data-width', `${nextPx}px`);
          if (badgeEl) {
            badgeEl.textContent = `${nextPx}px (${nextPct}%)`;
          }
          blockEl.querySelectorAll('.img-tool-btn[data-img-action="width"]').forEach(btn => {
            btn.classList.remove('active');
          });
        };

        const onPointerUp = () => {
          window.removeEventListener('pointermove', onPointerMove);
          window.removeEventListener('pointerup', onPointerUp);
          window.removeEventListener('pointercancel', onPointerUp);
          blockEl.classList.remove('is-resizing');
          syncRichEditor();
        };

        window.addEventListener('pointermove', onPointerMove, { passive: false });
        window.addEventListener('pointerup', onPointerUp);
        window.addEventListener('pointercancel', onPointerUp);
      });
    }

    /* Acciones del Menú Contextual de Clic Derecho para Bloques de Imagen (.note-image-block) */
    function ctxSetImageBlockWidth(w) {
      const block = activeCtxImageBlock;
      closeCustomContextMenu();
      if (!block) return;
      updateExistingImageBlockElement(block, { width: w });
      syncRichEditor();
      showToast(`Ancho de imagen ajustado a ${w}`, '↔️');
    }

    function ctxSetImageBlockAlign(align) {
      const block = activeCtxImageBlock;
      closeCustomContextMenu();
      if (!block) return;
      updateExistingImageBlockElement(block, { align });
      syncRichEditor();
      showToast('Alineación de imagen actualizada', '🖼️');
    }

    function ctxPromptImageCaption() {
      const block = activeCtxImageBlock;
      closeCustomContextMenu();
      if (!block) return;
      promptEditImageBlockCaption(block);
    }

    function ctxEditImageBlockInModal() {
      const block = activeCtxImageBlock;
      closeCustomContextMenu();
      if (!block) return;
      openImageInsertModal(block);
    }

    function ctxZoomImageBlock() {
      const block = activeCtxImageBlock;
      closeCustomContextMenu();
      if (!block) return;
      const img = block.querySelector('.note-image-el');
      const cap = block.querySelector('.note-image-caption')?.getAttribute('data-caption') || '';
      if (img) openImageLightbox(img.src, cap);
    }

    function ctxDuplicateImageBlock() {
      const block = activeCtxImageBlock;
      closeCustomContextMenu();
      if (!block) return;
      const clone = block.cloneNode(true);
      clone.id = 'img-block-' + Date.now() + '-' + Math.floor(Math.random() * 1000);
      clone.classList.remove('ctx-target-highlight', 'selected', 'is-resizing');
      block.after(clone);
      syncRichEditor();
      showToast('Bloque de imagen duplicado', '📑');
    }

    function ctxDeleteImageBlock() {
      const block = activeCtxImageBlock;
      closeCustomContextMenu();
      if (!block) return;
      block.remove();
      syncRichEditor();
      showToast('Bloque de imagen eliminado', '🗑');
    }

    /* ============================================================================
       SISTEMA DE PESTAÑAS MÚLTIPLES EN LA BARRA SUPERIOR (.note-tabs-bar-wrapper)
       ============================================================================ */
    let draggedTabNoteId = null;

    function ensureValidOpenTabs() {
      const validIds = new Set(getActiveNotesList().map(n => Number(n.id)));
      if (!Array.isArray(state.openTabIds)) {
        state.openTabIds = [];
      }
      // Filtrar IDs que existan (y no estén en la papelera) preservando el orden
      const seen = new Set();
      state.openTabIds = state.openTabIds
        .map(Number)
        .filter(id => {
          if (!validIds.has(id) || seen.has(id)) return false;
          seen.add(id);
          return true;
        });

      const activeId = (state.activeNoteId !== null && state.activeNoteId !== undefined) ? Number(state.activeNoteId) : null;
      if (activeId !== null && validIds.has(activeId) && !state.openTabIds.includes(activeId)) {
        state.openTabIds.push(activeId);
      }
      if (!state.openTabIds.length) {
        state.activeNoteId = null;
        state.isHomeActive = true;
      }
    }

    function saveOpenTabsState() {
      ensureValidOpenTabs();
      try {
        localStorage.setItem('notejs_open_tabs_v1', JSON.stringify(state.openTabIds));
      } catch (_) {}

      const settingsPayload = { openTabIds: JSON.stringify(state.openTabIds) };
      if (hasPyWebViewBridge() && typeof window.pywebview.api.save_settings === 'function') {
        window.pywebview.api.save_settings(settingsPayload).catch(() => {});
      } else {
        fetch('/api/settings', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(settingsPayload)
        }).catch(() => {});
      }
    }

    function renderNoteTabs() {
      const listEl = document.getElementById('note-tabs-list');
      if (!listEl) return;

      ensureValidOpenTabs();

      const isHome = Boolean(state.isHomeActive);
      const homeBtn = document.getElementById('btn-top-home');
      if (homeBtn) {
        homeBtn.classList.toggle('active', isHome);
        homeBtn.setAttribute('aria-pressed', isHome ? 'true' : 'false');
      }

      if (!state.openTabIds.length) {
        listEl.innerHTML = '';
        return;
      }

      listEl.innerHTML = state.openTabIds.map(tabNoteId => {
        const note = state.notes.find(n => n.id === Number(tabNoteId) && !n.isTrashed);
        if (!note) return '';
        const isActive = !isHome && Number(state.activeNoteId) === Number(note.id);
        const emoji = note.emoji || '📝';
        const title = note.title || 'Sin título';
        const safeTitle = escapeHtmlAttr(title);
        const safeFolder = escapeHtmlAttr(getNotePrimaryDisplayFolder(note));

        return `
          <div class="note-tab-item ${isActive ? 'active' : ''}"
               role="tab"
               aria-selected="${isActive ? 'true' : 'false'}"
               data-tab-note-id="${note.id}"
               draggable="true"
               onclick="switchNoteTab(${note.id})"
               onauxclick="if(event.button===1){event.preventDefault(); closeNoteTab(${note.id}, event);}"
               title="${safeTitle} (${safeFolder}) · Clic para activar · Clic central o ✕ para cerrar pestaña">
            <span class="note-tab-emoji">${emoji}</span>
            <span class="note-tab-title">${safeTitle}</span>
            ${note.isPinned ? '<span class="note-tab-pin-dot" title="Nota fijada">📌</span>' : ''}
            <button type="button"
                    class="note-tab-close"
                    onclick="closeNoteTab(${note.id}, event)"
                    title="Cerrar pestaña (Alt+W)"
                    aria-label="Cerrar pestaña ${safeTitle}">✕</button>
          </div>
        `;
      }).join('');

      attachNoteTabsDragListeners();

      // Asegurar que la pestaña activa sea visible en el contenedor con scroll horizontal
      requestAnimationFrame(() => {
        const activeTabEl = listEl.querySelector('.note-tab-item.active');
        if (activeTabEl && typeof activeTabEl.scrollIntoView === 'function') {
          activeTabEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
        }
      });

      const pickerDropdown = document.getElementById('note-tab-picker-dropdown');
      if (pickerDropdown && pickerDropdown.classList.contains('open')) {
        renderTabPickerDropdownItems();
      }
    }

    /* Navegación a Página de Inicio estilo Google Chrome */
    function navigateToHome() {
      if (state.isRemindersActive) {
        exitRemindersView();
      }
      state.isHomeActive = true;
      if (isTrashFolder(state.selectedFolder)) {
        state.selectedFolder = MASTER_ALL_NOTES_FOLDER;
      }
      const scaffold = document.getElementById('desktop-scaffold');
      if (scaffold) {
        scaffold.classList.add('is-home-active');
      }

      const homeBtn = document.getElementById('btn-top-home');
      if (homeBtn) {
        homeBtn.classList.add('active');
        homeBtn.setAttribute('aria-pressed', 'true');
      }

      const homeView = document.getElementById('home-page-view');
      const formatBar = document.querySelector('.desktop-format-bar');
      const notionCover = document.getElementById('notion-cover');
      const editorBody = document.getElementById('editor-body');

      if (homeView) homeView.style.display = 'flex';
      if (formatBar) formatBar.style.display = 'none';
      if (notionCover) notionCover.style.display = 'none';
      if (editorBody) editorBody.style.display = 'none';

      renderFolders();
      renderNoteTabs();
      renderHomePage();
    }

    function exitHomeView() {
      if (!state.isHomeActive) return;
      state.isHomeActive = false;
      const scaffold = document.getElementById('desktop-scaffold');
      if (scaffold) {
        scaffold.classList.remove('is-home-active');
      }

      const homeBtn = document.getElementById('btn-top-home');
      if (homeBtn) {
        homeBtn.classList.remove('active');
        homeBtn.setAttribute('aria-pressed', 'false');
      }

      const homeView = document.getElementById('home-page-view');
      const formatBar = document.querySelector('.desktop-format-bar');
      const notionCover = document.getElementById('notion-cover');
      const editorBody = document.getElementById('editor-body');

      if (homeView) homeView.style.display = 'none';
      if (!state.isRemindersActive) {
        if (formatBar) formatBar.style.display = 'flex';
        if (notionCover) notionCover.style.display = '';
        if (editorBody) editorBody.style.display = 'block';
      }

      if (!state.selectedFolder || isTrashFolder(state.selectedFolder)) {
        state.selectedFolder = MASTER_ALL_NOTES_FOLDER;
      }

      renderFolders();
      renderNotesList();
      renderNoteTabs();
    }

    /* Modos de vista de notas en Inicio: Cuadrícula y Lista */
    function setHomeNotesView(mode) {
      state.homeNotesView = (mode === 'list') ? 'list' : 'grid';
      try {
        localStorage.setItem('notejs_home_notes_view', state.homeNotesView);
      } catch (_) {}
      renderHomePage();
    }

    function handleHomeNotesSearch(e) {
      const val = (e && e.target ? e.target.value : '');
      state.homeNotesSearchQuery = val.toLowerCase().trim();
      const clearBtn = document.getElementById('home-hero-search-clear');
      if (clearBtn) {
        clearBtn.style.display = state.homeNotesSearchQuery ? 'inline-flex' : 'none';
      }
      renderHomeFoldersSearchRow();
      renderHomeNotesContent();
    }

    function clearHomeNotesSearch() {
      state.homeNotesSearchQuery = '';
      const input = document.getElementById('home-notes-search-input');
      if (input) {
        input.value = '';
        input.focus();
      }
      const clearBtn = document.getElementById('home-hero-search-clear');
      if (clearBtn) clearBtn.style.display = 'none';
      renderHomeFoldersSearchRow();
      renderHomeNotesContent();
    }

    function renderHomeFoldersSearchRow() {
      const rowEl = document.getElementById('home-folders-search-results');
      if (!rowEl) return;

      ensureMasterFolderFirst();
      const activeNotes = getActiveNotesList();
      const q = (state.homeNotesSearchQuery || '').toLowerCase().trim();
      const foldersList = Array.isArray(state.folders) ? state.folders : [];
      const matchingFolders = q
        ? foldersList.filter(f => f.toLowerCase().includes(q))
        : foldersList;

      if (!matchingFolders.length && q) {
        rowEl.innerHTML = `<span class="home-folder-search-empty">Sin carpetas que coincidan con "${escapeHtmlAttr(q)}"</span>`;
        return;
      }

      const chipsHtml = matchingFolders.map(folderName => {
        const isMaster = isMasterAllNotesFolder(folderName);
        const emoji = getFolderEmoji(folderName);
        const count = isMaster
          ? activeNotes.length
          : activeNotes.filter(n => noteBelongsToFolder(n, folderName)).length;
        const isActive = isMaster
          ? !state.homeFolderFilter
          : state.homeFolderFilter === folderName;
        const safeName = escapeHtmlAttr(folderName);
        const safeJs = String(folderName).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        const clickHandler = isMaster
          ? `clearHomeFolderFilter()`
          : `setHomeFolderFilter('${safeJs}')`;
        return `
          <button type="button" class="home-folder-chip ${isActive ? 'active' : ''}" onclick="${clickHandler}" title="Filtrar por ${safeName}">
            <span>${emoji}</span>
            <span>${safeName}</span>
            <span class="home-folder-chip-count">${count}</span>
          </button>
        `;
      }).join('');

      rowEl.innerHTML = chipsHtml;
    }

    function setHomeFolderFilter(folder) {
      state.homeFolderFilter = (state.homeFolderFilter === folder) ? null : folder;
      renderHomeFoldersSearchRow();
      renderHomeNotesContent();
    }

    function clearHomeFolderFilter() {
      state.homeFolderFilter = null;
      renderHomeFoldersSearchRow();
      renderHomeNotesContent();
    }

    const SPANISH_MONTH_NAMES = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];

    const SPANISH_WEEKDAY_NAMES = [
      'Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'
    ];

    function getMonthName(monthIdx) {
      return SPANISH_MONTH_NAMES[monthIdx] || '';
    }

    function formatCalendarDateTitle(dateStr) {
      if (!dateStr) return '';
      const parts = dateStr.split('-');
      if (parts.length !== 3) return dateStr;
      const year = Number(parts[0]);
      const month = Number(parts[1]) - 1;
      const day = Number(parts[2]);
      const dateObj = new Date(year, month, day);
      const weekday = SPANISH_WEEKDAY_NAMES[dateObj.getDay()];
      const monthName = SPANISH_MONTH_NAMES[month];
      return `${weekday}, ${day} de ${monthName} de ${year}`;
    }

    function getTodayDateString() {
      const d = new Date();
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }

    function renderHomePage() {
      const container = document.getElementById('home-page-view');
      if (!container) return;

      const hour = new Date().getHours();
      let greeting = '¡Buenas noches!';
      if (hour >= 6 && hour < 12) greeting = '¡Buenos días!';
      else if (hour >= 12 && hour < 20) greeting = '¡Buenas tardes!';

      const activeNotes = getActiveNotesList();
      const totalNotes = activeNotes.length;
      const pinnedNotes = activeNotes.filter(n => n.isPinned).length;
      const totalFolders = state.folders.length;
      const todayStr = getTodayDateString();
      const totalEventsToday = (state.reminders || []).filter(r => r.date === todayStr && !r.completed).length;

      container.innerHTML = `
        <div class="home-page-header">
          <div class="home-page-header-top">
            <div class="home-page-badge">
              <span>🏠</span>
              <span>Espacio de Inicio</span>
            </div>
            <div class="home-stats-pills">
              <span class="home-stat-pill"><strong>${totalNotes}</strong> notas</span>
              <span class="home-stat-pill"><strong>${totalFolders}</strong> carpetas</span>
              <span class="home-stat-pill"><strong>${pinnedNotes}</strong> fijadas</span>
              <span class="home-stat-pill" style="border-color:var(--accent-amber-border); color:var(--accent-amber);">
                <strong>${totalEventsToday}</strong> pendientes hoy
              </span>
            </div>
          </div>
          <h1 class="home-page-title">${greeting} Bienvenido a tu espacio de notas</h1>
          <p class="home-page-subtitle">Tus ideas, apuntes y tareas en un mismo lugar.</p>
        </div>

        <!-- BARRA DE BÚSQUEDA GRANDE DE NOTAS Y CARPETAS -->
        <div class="home-hero-search-section">
          <div class="home-hero-search-bar">
            <svg class="home-hero-search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input
              type="text"
              id="home-notes-search-input"
              class="home-hero-search-input"
              placeholder="Buscar notas o carpetas por título, contenido o etiquetas..."
              value="${escapeHtmlAttr(state.homeNotesSearchQuery || '')}"
              autocomplete="off"
              oninput="handleHomeNotesSearch(event)"
            />
            <button
              type="button"
              id="home-hero-search-clear"
              class="home-hero-search-clear"
              style="display:${state.homeNotesSearchQuery ? 'inline-flex' : 'none'};"
              onclick="clearHomeNotesSearch()"
              title="Limpiar búsqueda"
            >✕</button>
          </div>
          <div class="home-folders-filter-bar" id="home-folders-search-results"></div>
        </div>

        <!-- SECCIÓN: TODAS LAS NOTAS (Conmutador Cuadrícula / Lista y botón + para crear nota nueva) -->
        <section class="home-all-notes-section">
          <div class="home-notes-section-header">
            <div class="home-notes-header-left">
              <div class="home-section-title" style="margin:0;">
                <span style="font-size:18px;">📚</span>
                <span>Todas las notas</span>
                <span class="home-count-badge" id="home-notes-count-badge">(${totalNotes})</span>
              </div>
              <button type="button" class="home-add-note-plus-btn" onclick="createNewNote()" title="Crear una nota nueva en Todas Las Notas" aria-label="Crear una nota nueva">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </button>
            </div>

            <div class="home-notes-header-controls">
              <!-- Conmutador de Vista (Cuadrícula / Lista) -->
              <div class="home-view-mode-toggle" role="group" aria-label="Cambiar vista de notas">
                <button type="button" class="home-view-toggle-btn ${state.homeNotesView === 'grid' ? 'active' : ''}" onclick="setHomeNotesView('grid')" title="Vista en Cuadrícula">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                    <rect x="3" y="3" width="8" height="8" rx="2"></rect>
                    <rect x="13" y="3" width="8" height="8" rx="2"></rect>
                    <rect x="3" y="13" width="8" height="8" rx="2"></rect>
                    <rect x="13" y="13" width="8" height="8" rx="2"></rect>
                  </svg>
                  <span>Cuadrícula</span>
                </button>
                <button type="button" class="home-view-toggle-btn ${state.homeNotesView === 'list' ? 'active' : ''}" onclick="setHomeNotesView('list')" title="Vista en Lista">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round">
                    <line x1="4" y1="6" x2="20" y2="6"></line>
                    <line x1="4" y1="12" x2="20" y2="12"></line>
                    <line x1="4" y1="18" x2="20" y2="18"></line>
                  </svg>
                  <span>Lista</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Contenedor dinámico de notas -->
          <div id="home-notes-content-container"></div>
        </section>

        <!-- SECCIÓN: DEBAJO DE TODO ESO - CALENDARIO COMPACTO (IZQUIERDA) + EVENTOS / RECORDATORIOS (DERECHA) -->
        <section class="home-calendar-schedule-section">
          <div class="home-calendar-schedule-header">
            <div class="home-calendar-schedule-title">
              <span class="home-calendar-title-icon">📅</span>
              <div>
                <h2 class="home-calendar-heading">Calendario y Recordatorios</h2>
                <p class="home-calendar-subheading">Selecciona un día en el calendario de la izquierda para ver y gestionar tus eventos y recordatorios programados.</p>
              </div>
            </div>
          </div>

          <div class="home-calendar-schedule-body">
            <!-- COLUMNA IZQUIERDA: CALENDARIO COMPACTO (no muy grande) -->
            <div class="home-calendar-left-col">
              <div class="home-mini-calendar-card">
                <!-- Barra superior de navegación del mes -->
                <div class="home-cal-nav-bar">
                  <div class="home-cal-month-title" id="home-cal-month-title">
                    ${getMonthName(state.calendarMonth)} ${state.calendarYear}
                  </div>
                  <div class="home-cal-controls">
                    <button type="button" class="home-cal-nav-btn" onclick="navigateHomeCalendarMonth(-1)" title="Mes anterior">‹</button>
                    <button type="button" class="home-cal-today-pill" onclick="goToHomeCalendarToday()" title="Ir a hoy">Hoy</button>
                    <button type="button" class="home-cal-nav-btn" onclick="navigateHomeCalendarMonth(1)" title="Mes siguiente">›</button>
                  </div>
                </div>

                <!-- Cabecera de días de la semana -->
                <div class="home-cal-weekdays-row">
                  <span>Lu</span><span>Ma</span><span>Mi</span><span>Ju</span><span>Vi</span><span>Sá</span><span>Do</span>
                </div>

                <!-- Rejilla de días del mes -->
                <div id="home-calendar-days-grid" class="home-cal-days-grid"></div>

                <!-- Leyenda del calendario -->
                <div class="home-cal-legend">
                  <span class="cal-legend-item"><span class="cal-dot-sample has-events"></span> Con eventos</span>
                  <span class="cal-legend-item"><span class="cal-dot-sample is-today"></span> Hoy</span>
                  <span class="cal-legend-item"><span class="cal-dot-sample is-selected"></span> Seleccionado</span>
                </div>
              </div>
            </div>

            <!-- COLUMNA DERECHA: EVENTOS Y RECORDATORIOS DEL USUARIO -->
            <div class="home-calendar-right-col">
              <div class="home-events-panel-card">
                <div class="home-events-header">
                  <div class="home-events-date-info">
                    <div class="home-events-header-badge-row">
                      <span class="home-events-date-badge" id="home-events-relative-badge">Fecha</span>
                      <span class="home-events-count-pill" id="home-events-count-pill">0 eventos</span>
                    </div>
                    <h3 class="home-events-date-title" id="home-events-date-title">
                      ${formatCalendarDateTitle(state.selectedCalendarDate || todayStr)}
                    </h3>
                  </div>
                  <div class="home-events-actions">
                    <button type="button" class="home-add-event-btn" onclick="openNewEventModal('${state.selectedCalendarDate || todayStr}')">
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                      <span>Añadir Evento</span>
                    </button>
                  </div>
                </div>

                <!-- Pestañas de filtro de eventos -->
                <div class="home-events-filter-bar">
                  <button type="button" class="home-event-filter-tab ${state.eventsFilter === 'day' ? 'active' : ''}" onclick="setEventsFilter('day')">
                    <span>Día seleccionado</span>
                  </button>
                  <button type="button" class="home-event-filter-tab ${state.eventsFilter === 'all_pending' ? 'active' : ''}" onclick="setEventsFilter('all_pending')">
                    <span>Todos los pendientes</span>
                    <span class="home-filter-tab-count">${(state.reminders || []).filter(r => !r.completed).length}</span>
                  </button>
                </div>

                <!-- Lista de eventos interactivos -->
                <div id="home-events-list-container" class="home-events-list-container"></div>
              </div>
            </div>
          </div>
        </section>
      `;

      renderHomeFoldersSearchRow();
      renderHomeNotesContent();
      renderHomeCalendar();
      renderHomeEventsList();
    }

    function renderHomeNotesContent() {
      const container = document.getElementById('home-notes-content-container');
      if (!container) return;

      const activeNotes = getActiveNotesList();
      const q = (state.homeNotesSearchQuery || '').toLowerCase().trim();
      let notesToDisplay = [...activeNotes];

      if (state.homeFolderFilter) {
        notesToDisplay = notesToDisplay.filter(n => noteBelongsToFolder(n, state.homeFolderFilter));
      }

      if (q) {
        notesToDisplay = notesToDisplay.filter(n => {
          const text = `${n.title || ''} ${n.content || ''} ${getNoteFolders(n).join(' ')} ${n.tags || ''}`.toLowerCase();
          return text.includes(q);
        });
      }

      const countBadge = document.getElementById('home-notes-count-badge');
      if (countBadge) {
        countBadge.textContent = `(${notesToDisplay.length} de ${activeNotes.length})`;
      }

      if (!notesToDisplay.length) {
        container.innerHTML = `
          <div style="text-align:center; padding:36px 16px; color:var(--text-muted); font-size:13px;">
            <span style="font-size:28px; display:block; margin-bottom:8px;">🔍</span>
            No se encontraron notas con el filtro aplicado.
            ${state.homeFolderFilter || q ? '<div style="margin-top:10px;"><button class="home-event-filter-tab" onclick="clearHomeFolderFilter(); clearHomeNotesSearch();">Restablecer filtros</button></div>' : ''}
          </div>
        `;
        return;
      }

      if (state.homeNotesView === 'list') {
        // Vista de Lista (Tabla)
        const rowsHtml = notesToDisplay.map(n => {
          const emoji = n.emoji || '📝';
          const title = escapeHtmlAttr(n.title || 'Sin título');
          const userFolders = getNoteUserFolders(n);
          const folderLabel = userFolders.length > 0
            ? userFolders.map(f => `${getFolderEmoji(f)} ${escapeHtmlAttr(f)}`).join(' · ')
            : `${getFolderEmoji(MASTER_ALL_NOTES_FOLDER)} ${MASTER_ALL_NOTES_FOLDER}`;
          const rawTags = (n.tags || '').split(',').map(t => t.trim().replace(/^#/, '')).filter(Boolean);
          const tagsHtml = rawTags.slice(0, 2).map(t => `<span class="home-grid-tag-pill">#${escapeHtmlAttr(t)}</span>`).join(' ');
          const dateStr = new Date(n.updatedAt || Date.now()).toLocaleDateString('es-ES', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });

          return `
            <div class="home-list-row" data-home-note-id="${n.id}" onclick="selectNote(${n.id})" title="Abrir nota &quot;${title}&quot;">
              <div class="home-list-cell-title">
                <span style="font-size:16px;">${emoji}</span>
                <span class="note-title-text">${title}</span>
                ${n.isPinned ? '<span title="Nota fijada">📌</span>' : ''}
              </div>
              <div class="home-list-cell-folder">
                <span>${folderLabel}</span>
              </div>
              <div class="home-list-cell-tags">
                ${tagsHtml || '<span style="opacity:0.4;">—</span>'}
              </div>
              <div class="home-list-cell-date">${dateStr}</div>
              <div class="home-list-cell-action" style="display:flex; align-items:center; gap:6px; justify-content:flex-end;">
                <button type="button" class="btn-icon-tiny btn-danger-tiny" style="opacity:0.75;" onclick="event.stopPropagation(); deleteNoteById(${n.id});" title="Enviar a la papelera">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                </button>
                <span style="color:var(--accent-amber); font-size:12px; font-weight:700;">↗</span>
              </div>
            </div>
          `;
        }).join('');

        container.innerHTML = `
          <div class="home-notes-list-view">
            <div class="home-list-table-header">
              <span>Nota</span>
              <span>Carpetas</span>
              <span>Etiquetas</span>
              <span>Última edición</span>
              <span></span>
            </div>
            ${rowsHtml}
          </div>
        `;
      } else {
        // Vista de Cuadrícula (Cards)
        const cardsHtml = notesToDisplay.map(n => {
          const title = escapeHtmlAttr(n.isLocked ? 'Nota protegida' : (n.title || 'Sin título'));
          const background = escapeHtmlAttr(noteCoverBackground(n));
          const position = Number.isFinite(n.coverPositionY) ? Math.min(100, Math.max(0, n.coverPositionY)) : 50;
          const hasCover = n.hasCover && !n.isLocked;
          const previewTemplate = document.createElement('template');
          previewTemplate.innerHTML = n.isLocked ? '' : getNotePreviewText(n);
          const preview = escapeHtmlAttr(n.isLocked ? 'Contenido protegido' : (previewTemplate.content.textContent.trim() || 'Nota sin contenido'));
          return `
            <button type="button" class="home-grid-card" data-home-note-id="${n.id}" onclick="selectNote(${n.id})" title="Abrir &quot;${title}&quot;">
              ${hasCover ? `<span class="home-grid-card-cover" style="background:${background};background-size:cover;background-position:center ${position}%;"></span>` : ''}
              <span class="home-grid-card-title">${title}</span>
              ${hasCover ? '' : `<span class="home-grid-card-content-preview">${preview}</span>`}
            </button>
          `;
        }).join('');

        container.innerHTML = `
          <div class="home-notes-grid-view">
            ${cardsHtml}
          </div>
        `;
      }
    }

    /* Lógica del Calendario Compacto */
    function renderHomeCalendar() {
      const gridEl = document.getElementById('home-calendar-days-grid');
      const titleEl = document.getElementById('home-cal-month-title');
      if (!gridEl) return;

      const year = state.calendarYear;
      const month = state.calendarMonth;

      if (titleEl) {
        titleEl.textContent = `${getMonthName(month)} ${year}`;
      }

      const todayStr = getTodayDateString();
      const selectedStr = state.selectedCalendarDate || todayStr;

      // Días totales en el mes
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      // Primer día de la semana (Lunes = 0, Domingo = 6 en formato europeo/español)
      let firstDay = new Date(year, month, 1).getDay();
      firstDay = (firstDay === 0) ? 6 : firstDay - 1;

      // Días del mes anterior para relleno
      const daysInPrevMonth = new Date(year, month, 0).getDate();

      let cellsHtml = '';

      // Celdas del mes anterior
      for (let i = firstDay - 1; i >= 0; i--) {
        const prevDay = daysInPrevMonth - i;
        const prevMonth = (month === 0) ? 11 : month - 1;
        const prevYear = (month === 0) ? year - 1 : year;
        const dateStr = `${prevYear}-${String(prevMonth + 1).padStart(2, '0')}-${String(prevDay).padStart(2, '0')}`;
        const hasEvents = (state.reminders || []).some(r => r.date === dateStr);

        cellsHtml += `
          <div class="home-cal-day-cell is-outside-month ${dateStr === selectedStr ? 'is-selected' : ''}" 
               data-date="${dateStr}" 
               onclick="selectHomeCalendarDate('${dateStr}')">
            <span>${prevDay}</span>
            ${hasEvents ? '<span class="cal-event-dot-marker"></span>' : ''}
          </div>
        `;
      }

      // Celdas del mes actual
      for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const isToday = (dateStr === todayStr);
        const isSelected = (dateStr === selectedStr);
        const hasEvents = (state.reminders || []).some(r => r.date === dateStr);

        cellsHtml += `
          <div class="home-cal-day-cell ${isToday ? 'is-today' : ''} ${isSelected ? 'is-selected' : ''}" 
               data-date="${dateStr}" 
               onclick="selectHomeCalendarDate('${dateStr}')" 
               title="${day} de ${getMonthName(month)} de ${year}${hasEvents ? ' · Tiene eventos programados' : ''}">
            <span>${day}</span>
            ${hasEvents ? '<span class="cal-event-dot-marker"></span>' : ''}
          </div>
        `;
      }

      // Celdas del mes siguiente para completar la cuadrícula (múltiplo de 7)
      const totalCells = firstDay + daysInMonth;
      const remainingCells = (totalCells % 7 === 0) ? 0 : 7 - (totalCells % 7);
      for (let day = 1; day <= remainingCells; day++) {
        const nextMonth = (month === 11) ? 0 : month + 1;
        const nextYear = (month === 11) ? year + 1 : year;
        const dateStr = `${nextYear}-${String(nextMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const hasEvents = (state.reminders || []).some(r => r.date === dateStr);

        cellsHtml += `
          <div class="home-cal-day-cell is-outside-month ${dateStr === selectedStr ? 'is-selected' : ''}" 
               data-date="${dateStr}" 
               onclick="selectHomeCalendarDate('${dateStr}')">
            <span>${day}</span>
            ${hasEvents ? '<span class="cal-event-dot-marker"></span>' : ''}
          </div>
        `;
      }

      gridEl.innerHTML = cellsHtml;
    }

    function navigateHomeCalendarMonth(delta) {
      let m = state.calendarMonth + delta;
      let y = state.calendarYear;
      if (m < 0) {
        m = 11;
        y -= 1;
      } else if (m > 11) {
        m = 0;
        y += 1;
      }
      state.calendarMonth = m;
      state.calendarYear = y;
      renderHomeCalendar();
    }

    function goToHomeCalendarToday() {
      const today = new Date();
      state.calendarYear = today.getFullYear();
      state.calendarMonth = today.getMonth();
      state.selectedCalendarDate = getTodayDateString();
      renderHomeCalendar();
      renderHomeEventsList();
    }

    function selectHomeCalendarDate(dateStr) {
      state.selectedCalendarDate = dateStr;
      renderHomeCalendar();
      renderHomeEventsList();
    }

    function setEventsFilter(filter) {
      state.eventsFilter = (filter === 'all_pending') ? 'all_pending' : 'day';
      const tabs = document.querySelectorAll('.home-event-filter-tab');
      tabs.forEach(tab => {
        const isDayTab = tab.textContent.includes('Día');
        tab.classList.toggle('active', (state.eventsFilter === 'day' && isDayTab) || (state.eventsFilter === 'all_pending' && !isDayTab));
      });
      renderHomeEventsList();
    }

    /* Renderizado de Eventos y Recordatorios */
    function renderHomeEventsList() {
      const container = document.getElementById('home-events-list-container');
      const titleEl = document.getElementById('home-events-date-title');
      const badgeEl = document.getElementById('home-events-relative-badge');
      const countEl = document.getElementById('home-events-count-pill');
      if (!container) return;

      const todayStr = getTodayDateString();
      const selectedStr = state.selectedCalendarDate || todayStr;

      // Actualizar cabecera de la fecha
      if (titleEl) {
        titleEl.textContent = (state.eventsFilter === 'all_pending') 
          ? 'Todos los recordatorios pendientes'
          : formatCalendarDateTitle(selectedStr);
      }

      if (badgeEl) {
        if (state.eventsFilter === 'all_pending') {
          badgeEl.textContent = 'Agenda Global';
        } else if (selectedStr === todayStr) {
          badgeEl.textContent = 'Hoy';
        } else {
          badgeEl.textContent = 'Día Seleccionado';
        }
      }

      let eventsToShow = [];
      if (state.eventsFilter === 'all_pending') {
        eventsToShow = (state.reminders || [])
          .filter(r => !r.completed)
          .sort((a, b) => (a.date || '').localeCompare(b.date || ''));
      } else {
        eventsToShow = (state.reminders || []).filter(r => r.date === selectedStr);
      }

      if (countEl) {
        countEl.textContent = `${eventsToShow.length} evento${eventsToShow.length === 1 ? '' : 's'}`;
      }

      if (!eventsToShow.length) {
        const isDay = state.eventsFilter === 'day';
        container.innerHTML = `
          <div class="home-events-empty-state">
            <span class="home-events-empty-icon">🗓️</span>
            <div>
              <strong>${isDay ? 'No hay eventos ni recordatorios para este día' : 'No tienes recordatorios pendientes'}</strong>
              <div style="font-size:11.5px; opacity:0.75; margin-top:2px;">
                ${isDay ? 'Aprovecha tu jornada libre o añade un recordatorio para esta fecha.' : '¡Todo al día! Tu agenda está despejada.'}
              </div>
            </div>
            ${isDay ? `
              <button type="button" class="home-add-event-btn" onclick="openNewEventModal('${selectedStr}')" style="margin-top:6px;">
                <span>+ Crear recordatorio para este día</span>
              </button>
            ` : ''}
          </div>
        `;
        return;
      }

      const categoryClassMap = {
        'Trabajo': 'cat-trabajo',
        'Desarrollo': 'cat-desarrollo',
        'Urgente': 'cat-urgente',
        'Personal': 'cat-personal',
        'Universidad': 'cat-universidad',
        'Reunión': 'cat-trabajo'
      };

      container.innerHTML = eventsToShow.map(ev => {
        const catClass = categoryClassMap[ev.category] || '';
        const safeTitle = escapeHtmlAttr(ev.title || 'Recordatorio');
        const isCompleted = Boolean(ev.completed);

        return `
          <div class="home-event-card ${isCompleted ? 'completed' : ''}" id="event-card-${ev.id}">
            <div class="home-event-card-left">
              <button type="button" 
                      class="home-event-checkbox" 
                      onclick="toggleHomeReminder(${ev.id})" 
                      title="${isCompleted ? 'Marcar como pendiente' : 'Marcar como completado'}"
                      aria-label="Alternar estado de evento">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </button>
              <div class="home-event-info">
                <span class="home-event-title">${safeTitle}</span>
                <div class="home-event-meta-row">
                  ${ev.time ? `<span>🕒 ${escapeHtmlAttr(ev.time)}</span>` : '<span>🕒 Todo el día</span>'}
                  ${state.eventsFilter === 'all_pending' ? `<span>📅 ${escapeHtmlAttr(ev.date)}</span>` : ''}
                  ${ev.category ? `<span class="home-event-category-pill ${catClass}">${escapeHtmlAttr(ev.category)}</span>` : ''}
                </div>
              </div>
            </div>
            <button type="button" class="home-event-delete-btn" onclick="deleteHomeReminder(${ev.id})" title="Eliminar recordatorio" aria-label="Eliminar recordatorio">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        `;
      }).join('');
    }

    function toggleHomeReminder(id) {
      const numId = Number(id);
      const reminder = (state.reminders || []).find(r => r.id === numId);
      if (!reminder) return;
      reminder.completed = !reminder.completed;
      persistRemindersLocal();
      persistReminderToBackend(reminder);
      renderHomeCalendar();
      renderHomeEventsList();
      const remindersBadge = document.getElementById('sidebar-reminders-count-badge');
      if (remindersBadge) {
        const pendingCount = (state.reminders || []).filter(r => !r.completed).length;
        remindersBadge.textContent = String(pendingCount);
      }
      if (state.isRemindersActive) {
        renderRemindersPageView();
      }
      showToast(reminder.completed ? 'Recordatorio marcado como completado' : 'Recordatorio marcado como pendiente', '✓');
    }

    function deleteHomeReminder(id) {
      const numId = Number(id);
      state.reminders = (state.reminders || []).filter(r => r.id !== numId);
      persistRemindersLocal();
      deleteReminderFromBackend(numId);
      renderHomeCalendar();
      renderHomeEventsList();
      const remindersBadge = document.getElementById('sidebar-reminders-count-badge');
      if (remindersBadge) {
        const pendingCount = (state.reminders || []).filter(r => !r.completed).length;
        remindersBadge.textContent = String(pendingCount);
      }
      if (state.isRemindersActive) {
        renderRemindersPageView();
      }
      showToast('Recordatorio eliminado', '🗑️');
    }

    /* Modal para Crear Evento o Recordatorio */
    function openNewEventModal(prefilledDate) {
      const modal = document.getElementById('modal-add-event');
      if (!modal) return;
      modal.style.display = 'flex';

      const dateInput = document.getElementById('event-input-date');
      const titleInput = document.getElementById('event-input-title');
      const timeInput = document.getElementById('event-input-time');

      if (dateInput) {
        dateInput.value = prefilledDate || state.selectedCalendarDate || getTodayDateString();
      }
      if (titleInput) {
        titleInput.value = '';
        setTimeout(() => titleInput.focus(), 60);
      }
      if (timeInput) {
        timeInput.value = '10:00 - 11:00';
      }
    }

    function closeNewEventModal() {
      const modal = document.getElementById('modal-add-event');
      if (modal) modal.style.display = 'none';
    }

    function saveNewHomeEvent() {
      const titleInput = document.getElementById('event-input-title');
      const dateInput = document.getElementById('event-input-date');
      const timeInput = document.getElementById('event-input-time');
      const catInput = document.getElementById('event-input-category');

      const title = (titleInput?.value || '').trim();
      const date = dateInput?.value || getTodayDateString();
      const time = (timeInput?.value || '').trim() || 'Todo el día';
      const category = catInput?.value || 'Trabajo';

      if (!title) {
        showToast('Por favor introduce un título para el evento.', '⚠️');
        return;
      }

      const newEvent = {
        id: Date.now(),
        title,
        date,
        time,
        category,
        completed: false
      };

      if (!Array.isArray(state.reminders)) state.reminders = [];
      state.reminders.push(newEvent);
      persistRemindersLocal();
      persistReminderToBackend(newEvent);

      state.selectedCalendarDate = date;

      // Sincronizar mes del calendario con la fecha del nuevo evento
      const parts = date.split('-');
      if (parts.length === 3) {
        state.calendarYear = Number(parts[0]);
        state.calendarMonth = Number(parts[1]) - 1;
      }

      closeNewEventModal();
      renderHomeCalendar();
      renderHomeEventsList();
      const remindersBadge = document.getElementById('sidebar-reminders-count-badge');
      if (remindersBadge) {
        const pendingCount = (state.reminders || []).filter(r => !r.completed).length;
        remindersBadge.textContent = String(pendingCount);
      }
      if (state.isRemindersActive) {
        renderRemindersPageView();
      }
      showToast(`Recordatorio "${title}" guardado en el calendario`, '📅');
    }

    function handleGalleryNoteCardClick(event, noteId) {
      const numericId = Number(noteId);
      if (event && (event.ctrlKey || event.metaKey || event.shiftKey)) {
        event.preventDefault();
        openNoteInBackgroundTab(numericId);
        return;
      }
      selectNote(numericId);
    }

    function switchNoteTab(noteId) {
      const numericId = Number(noteId);
      if (!state.notes.some(n => n.id === numericId)) return;
      if (state.isRemindersActive) {
        exitRemindersView();
      }
      if (state.isHomeActive) {
        exitHomeView();
        state.activeNoteId = numericId;
        renderNotesList();
        renderNoteTabs();
        loadActiveNote();
        return;
      }
      if (state.activeNoteId === numericId) return;
      selectNote(numericId);
    }

    function openNoteInBackgroundTab(noteId) {
      const numericId = Number(noteId);
      const note = state.notes.find(n => n.id === numericId);
      if (!note) return;

      ensureValidOpenTabs();
      const alreadyOpen = state.openTabIds.includes(numericId);
      if (!alreadyOpen) {
        state.openTabIds.push(numericId);
        saveOpenTabsState();
        renderNoteTabs();
        renderNotesList();
        showToast(`Pestaña abierta: "${note.title || 'Sin título'}"`, '🗂️');
      } else {
        switchNoteTab(numericId);
      }
    }

    function closeNoteTab(noteId, event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      if (!noteId && noteId !== 0) {
        if (state.activeNoteId) {
          noteId = state.activeNoteId;
        } else {
          return;
        }
      }
      const numericId = Number(noteId);
      ensureValidOpenTabs();

      const idx = state.openTabIds.indexOf(numericId);
      if (idx === -1) return;

      state.openTabIds.splice(idx, 1);

      // Si se cerraron todas las pestañas, volver directamente a la página de Inicio
      if (state.openTabIds.length === 0) {
        state.activeNoteId = null;
        state.isHomeActive = true;
        saveOpenTabsState();
        renderNotesList();
        renderNoteTabs();
        navigateToHome();
        showToast('Todas las notas cerradas. En página de inicio', '🏠');
        return;
      }

      // Si la pestaña cerrada era la activa, cambiar a la contigua
      if (Number(state.activeNoteId) === numericId) {
        const nextIdx = Math.min(idx, state.openTabIds.length - 1);
        state.activeNoteId = state.openTabIds[nextIdx];
        saveOpenTabsState();
        renderNotesList();
        renderNoteTabs();
        loadActiveNote();
      } else {
        saveOpenTabsState();
        renderNotesList();
        renderNoteTabs();
      }
    }

    function closeAllNoteTabs() {
      state.openTabIds = [];
      state.activeNoteId = null;
      state.isHomeActive = true;
      saveOpenTabsState();
      renderNotesList();
      renderNoteTabs();
      navigateToHome();
      showToast('Todas las notas cerradas. En página de inicio', '🏠');
    }

    function closeOtherNoteTabs(keepNoteId) {
      const numericId = Number(keepNoteId);
      if (!state.notes.some(n => n.id === numericId)) return;
      state.openTabIds = [numericId];
      state.activeNoteId = numericId;
      saveOpenTabsState();
      renderNotesList();
      renderNoteTabs();
      loadActiveNote();
      showToast('Se cerraron las demás pestañas', '🗂️');
    }

    function closeRightNoteTabs(fromNoteId) {
      const numericId = Number(fromNoteId);
      ensureValidOpenTabs();
      const idx = state.openTabIds.indexOf(numericId);
      if (idx === -1 || idx >= state.openTabIds.length - 1) return;

      state.openTabIds = state.openTabIds.slice(0, idx + 1);
      if (!state.openTabIds.includes(Number(state.activeNoteId))) {
        state.activeNoteId = numericId;
        loadActiveNote();
      }
      saveOpenTabsState();
      renderNotesList();
      renderNoteTabs();
      showToast('Pestañas a la derecha cerradas', '🗂️');
    }

    function cycleOpenNoteTab(direction) {
      ensureValidOpenTabs();
      if (state.openTabIds.length <= 1) return;
      const curIdx = state.openTabIds.indexOf(Number(state.activeNoteId));
      const nextIdx = (curIdx + direction + state.openTabIds.length) % state.openTabIds.length;
      selectNote(state.openTabIds[nextIdx]);
    }

    function toggleTabPickerDropdown(event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      const dropdown = document.getElementById('note-tab-picker-dropdown');
      const btn = document.getElementById('btn-tab-picker');
      if (!dropdown) return;

      const willOpen = !dropdown.classList.contains('open');
      if (willOpen) {
        renderTabPickerDropdownItems();
        dropdown.classList.add('open');
        if (btn) btn.classList.add('active');
      } else {
        closeTabPickerDropdown();
      }
    }

    function closeTabPickerDropdown() {
      const dropdown = document.getElementById('note-tab-picker-dropdown');
      const btn = document.getElementById('btn-tab-picker');
      if (dropdown) dropdown.classList.remove('open');
      if (btn) btn.classList.remove('active');
    }

    function renderTabPickerDropdownItems() {
      const dropdown = document.getElementById('note-tab-picker-dropdown');
      if (!dropdown) return;

      ensureValidOpenTabs();
      const openSet = new Set(state.openTabIds.map(Number));
      const closedNotes = state.notes.filter(n => !openSet.has(Number(n.id)));
      const openNotes = state.notes.filter(n => openSet.has(Number(n.id)));

      let html = `
        <button class="tab-picker-item" onclick="closeTabPickerDropdown(); createNewNote();">
          <span style="display:flex; align-items:center; gap:7px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
            <span>➕</span>
            <strong>Crear nueva nota en pestaña</strong>
          </span>
          <span class="tab-picker-item-meta">${getShortcutDisplayCombo('new_note')}</span>
        </button>
      `;

      if (closedNotes.length > 0) {
        html += `<div class="tab-picker-section-title">Abrir nota existente en pestaña (${closedNotes.length})</div>`;
        html += closedNotes.map(n => `
          <button class="tab-picker-item" onclick="closeTabPickerDropdown(); selectNote(${n.id});">
            <span style="display:flex; align-items:center; gap:7px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
              <span>${n.emoji || '📝'}</span>
              <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${escapeHtmlAttr(n.title || 'Sin título')}</span>
            </span>
            <span class="tab-picker-item-meta">${getFolderEmoji(n.folder || 'Personal')} ${escapeHtmlAttr(n.folder || 'Personal')}</span>
          </button>
        `).join('');
      }

      if (openNotes.length > 0) {
        html += `<div class="tab-picker-section-title">Pestañas activas (${openNotes.length})</div>`;
        html += openNotes.map(n => `
          <button class="tab-picker-item already-open" onclick="closeTabPickerDropdown(); selectNote(${n.id});">
            <span style="display:flex; align-items:center; gap:7px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
              <span>${n.emoji || '📝'}</span>
              <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${escapeHtmlAttr(n.title || 'Sin título')}</span>
            </span>
            <span class="tab-picker-item-meta">${Number(state.activeNoteId) === Number(n.id) ? '● Activa' : 'Abierta'}</span>
          </button>
        `).join('');
      }

      dropdown.innerHTML = html;
    }

    function attachNoteTabsDragListeners() {
      const listEl = document.getElementById('note-tabs-list');
      if (!listEl) return;

      const tabs = listEl.querySelectorAll('.note-tab-item[data-tab-note-id]');
      tabs.forEach(tabEl => {
        const tabNoteId = Number(tabEl.getAttribute('data-tab-note-id'));

        tabEl.ondragstart = (e) => {
          if (e.target && e.target.closest('.note-tab-close')) {
            e.preventDefault();
            return;
          }
          draggedTabNoteId = tabNoteId;
          draggedNoteCardId = tabNoteId;
          if (e.dataTransfer) {
            e.dataTransfer.effectAllowed = 'copyMove';
            e.dataTransfer.setData('application/notejs-tab-id', String(tabNoteId));
            e.dataTransfer.setData('application/notejs-note-id', String(tabNoteId));
            e.dataTransfer.setData('text/plain', 'note:' + tabNoteId);
          }
        };

        tabEl.ondragend = () => {
          draggedTabNoteId = null;
          draggedNoteCardId = null;
          listEl.querySelectorAll('.tab-drag-over-left, .tab-drag-over-right').forEach(el => {
            el.classList.remove('tab-drag-over-left', 'tab-drag-over-right');
          });
        };

        tabEl.ondragover = (e) => {
          e.preventDefault();
          e.stopPropagation();
          const rect = tabEl.getBoundingClientRect();
          const placeBefore = e.clientX < rect.left + rect.width / 2;
          tabEl.classList.toggle('tab-drag-over-left', placeBefore);
          tabEl.classList.toggle('tab-drag-over-right', !placeBefore);
        };

        tabEl.ondragleave = () => {
          tabEl.classList.remove('tab-drag-over-left', 'tab-drag-over-right');
        };

        tabEl.ondrop = (e) => {
          e.preventDefault();
          e.stopPropagation();
          const placeBefore = tabEl.classList.contains('tab-drag-over-left');
          tabEl.classList.remove('tab-drag-over-left', 'tab-drag-over-right');

          const sourceId = draggedTabNoteId || extractDroppedNoteId(e);
          draggedTabNoteId = null;
          cleanupNoteListDragStates();
          if (!sourceId || sourceId === tabNoteId) return;

          ensureValidOpenTabs();
          const existingIdx = state.openTabIds.indexOf(Number(sourceId));
          if (existingIdx !== -1) {
            state.openTabIds.splice(existingIdx, 1);
          }
          const targetIdx = state.openTabIds.indexOf(tabNoteId);
          const insertIdx = placeBefore ? targetIdx : targetIdx + 1;
          state.openTabIds.splice(Math.max(0, insertIdx), 0, Number(sourceId));
          state.activeNoteId = Number(sourceId);
          saveOpenTabsState();
          renderNotesList();
          renderNoteTabs();
          loadActiveNote();
        };
      });
    }

    function setupTabBarDropTarget() {
      const wrapper = document.getElementById('note-tabs-bar-wrapper');
      if (!wrapper) return;

      wrapper.addEventListener('dragover', (e) => {
        if (e.target.closest('.note-tab-item')) return;
        e.preventDefault();
        wrapper.classList.add('tab-bar-drag-over');
      });

      wrapper.addEventListener('dragleave', (e) => {
        if (e.relatedTarget && wrapper.contains(e.relatedTarget)) return;
        wrapper.classList.remove('tab-bar-drag-over');
      });

      wrapper.addEventListener('drop', (e) => {
        wrapper.classList.remove('tab-bar-drag-over');
        if (e.target.closest('.note-tab-item')) return;
        e.preventDefault();

        const droppedId = draggedTabNoteId || extractDroppedNoteId(e);
        draggedTabNoteId = null;
        cleanupNoteListDragStates();
        if (!droppedId) return;

        selectNote(Number(droppedId));
      });
    }

    window.addEventListener('scroll', closeCustomContextMenu, true);
    window.addEventListener('resize', closeCustomContextMenu);

    /* ============================================================================
       ARQUITECTURA ESPACIAL Y MANIPULACIÓN DE ELEMENTOS EN NOTION PARA PC
       ============================================================================ */

    // 1. Menú de Apariencia de Página (•••): Fuentes, Texto Pequeño, Ancho Completo y Sticky TOC
    function togglePageAppearancePopover(event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      const popover = document.getElementById('page-appearance-popover');
      if (!popover) return;
      const willOpen = !popover.classList.contains('open');
      if (willOpen) {
        const note = getActiveNote();
        if (note) applyNoteAppearanceSettings(note);
        popover.classList.add('open');
      } else {
        popover.classList.remove('open');
      }
    }

    function closePageAppearancePopover() {
      const popover = document.getElementById('page-appearance-popover');
      if (popover) popover.classList.remove('open');
    }

    function applyNoteAppearanceSettings(note) {
      if (!note) return;
      const editorBody = document.getElementById('editor-body');
      const coverEl = document.getElementById('notion-cover');

      const font = note.pageFont || 'sans';
      const isSmall = Boolean(note.smallText);
      const isFullWidth = Boolean(note.fullWidth);
      const showStickyToc = note.showStickyToc !== false;

      if (editorBody) {
        editorBody.classList.remove('font-sans', 'font-serif', 'font-mono');
        editorBody.classList.add(`font-${font}`);
        editorBody.classList.toggle('is-small-text', isSmall);
        editorBody.classList.toggle('is-full-width', isFullWidth);
      }

      if (coverEl) {
        const posY = typeof note.coverPositionY === 'number' ? note.coverPositionY : 50;
        coverEl.style.backgroundPosition = `center ${posY}%`;
      }

      // Actualizar controles del popover
      ['sans', 'serif', 'mono'].forEach(f => {
        const card = document.getElementById(`font-card-${f}`);
        if (card) card.classList.toggle('active', f === font);
      });

      const swSmall = document.getElementById('switch-small-text');
      if (swSmall) {
        swSmall.classList.toggle('active', isSmall);
        swSmall.setAttribute('aria-checked', String(isSmall));
      }

      const swFull = document.getElementById('switch-full-width');
      if (swFull) {
        swFull.classList.toggle('active', isFullWidth);
        swFull.setAttribute('aria-checked', String(isFullWidth));
      }

      const swToc = document.getElementById('switch-sticky-toc');
      if (swToc) {
        swToc.classList.toggle('active', showStickyToc);
        swToc.setAttribute('aria-checked', String(showStickyToc));
      }

      const tocRail = document.getElementById('sticky-toc-rail');
      if (tocRail) {
        tocRail.classList.toggle('hidden-rail', !showStickyToc);
      }
    }

    function setPageFontFamily(fontKey) {
      const note = getActiveNote();
      if (!note) return;
      note.pageFont = fontKey || 'sans';
      note.updatedAt = Date.now();
      applyNoteAppearanceSettings(note);
      save(false, note);
      const names = { sans: 'Sans-Serif (Predeterminado)', serif: 'Serif Editorial', mono: 'Monoespaciado Técnico' };
      showToast(`Tipografía cambiada a ${names[note.pageFont] || fontKey}`, 'Aa');
    }

    function togglePageSmallText() {
      const note = getActiveNote();
      if (!note) return;
      note.smallText = !note.smallText;
      note.updatedAt = Date.now();
      applyNoteAppearanceSettings(note);
      save(false, note);
      showToast(note.smallText ? 'Texto pequeño activado' : 'Tamaño de texto estándar', '🔡');
    }

    function togglePageFullWidth() {
      const note = getActiveNote();
      if (!note) return;
      note.fullWidth = !note.fullWidth;
      note.updatedAt = Date.now();
      applyNoteAppearanceSettings(note);
      save(false, note);
      showToast(note.fullWidth ? 'Ancho completo (Full width) activado' : 'Ancho centrado de lectura (~712px)', '↔️');
    }

    function togglePageStickyToc() {
      const note = getActiveNote();
      if (!note) return;
      note.showStickyToc = note.showStickyToc === false ? true : false;
      note.updatedAt = Date.now();
      applyNoteAppearanceSettings(note);
      refreshPageTableOfContents();
      save(false, note);
      showToast(note.showStickyToc ? 'Índice flotante lateral visible' : 'Índice flotante lateral oculto', '📑');
    }

    function resetPageAppearanceDefaults() {
      const note = getActiveNote();
      if (!note) return;
      note.pageFont = 'sans';
      note.smallText = false;
      note.fullWidth = false;
      note.showStickyToc = true;
      note.coverPositionY = 50;
      note.updatedAt = Date.now();
      applyNoteAppearanceSettings(note);
      refreshPageTableOfContents();
      save(false, note);
      showToast('Diseño de página restablecido a valores originales', '↺');
    }

    function copyCurrentNoteLink() {
      const note = getActiveNote();
      if (!note) return;
      const url = `${window.location.origin}${window.location.pathname}#note-${note.id}`;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(() => {
          showToast('Enlace a la nota copiado al portapapeles', '🔗');
        }).catch(() => {
          showToast(`Enlace: #note-${note.id}`, '🔗');
        });
      } else {
        showToast(`Enlace: #note-${note.id}`, '🔗');
      }
    }

    // 3. Tabla de Contenidos Flotante Lateral (Sticky Right-Rail TOC) y Bloque /toc
    function collectEditorHeadings() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return [];
      const nodes = Array.from(editor.querySelectorAll('h1, h2, h3'));
      return nodes.map((el, idx) => {
        const tag = el.tagName.toLowerCase();
        const level = tag === 'h1' ? 1 : (tag === 'h2' ? 2 : 3);
        const text = (el.textContent || '').trim() || `Encabezado ${idx + 1}`;
        el.setAttribute('data-heading-idx', String(idx));
        return { idx, level, tag, text, el };
      });
    }

    function refreshPageTableOfContents() {
      const headings = collectEditorHeadings();
      const note = getActiveNote();
      const railEl = document.getElementById('sticky-toc-rail');
      const barsEl = document.getElementById('sticky-toc-bars');
      const listEl = document.getElementById('sticky-toc-list');

      if (railEl && barsEl && listEl) {
        const shouldShowRail = note ? (note.showStickyToc !== false) : true;
        if (!shouldShowRail || headings.length === 0) {
          railEl.classList.add('hidden-rail');
        } else {
          railEl.classList.remove('hidden-rail');
          barsEl.innerHTML = headings.map((h, i) => `
            <span class="sticky-toc-bar-line level-${h.level} ${i === 0 ? 'active' : ''}" data-toc-bar="${h.idx}"></span>
          `).join('');
          listEl.innerHTML = headings.map(h => `
            <div class="sticky-toc-item toc-h${h.level}" onclick="scrollToHeadingByIndex(${h.idx})" title="${escapeHtmlAttr(h.text)}">
              ${escapeHtmlAttr(h.text)}
            </div>
          `).join('');
        }
      }

      // Actualizar también bloques /toc embebidos en el lienzo
      const editor = document.getElementById('rich-editor-canvas');
      if (editor) {
        const tocBlocks = editor.querySelectorAll('.notion-toc-block');
        tocBlocks.forEach(block => {
          const linksContainer = block.querySelector('.notion-toc-block-links');
          if (!linksContainer) return;
          if (headings.length === 0) {
            linksContainer.innerHTML = `<div style="font-size:12px; color:var(--text-muted); font-style:italic;">Añade encabezados H1, H2 o H3 en el documento para poblar automáticamente este índice.</div>`;
          } else {
            linksContainer.innerHTML = headings.map(h => {
              const indent = (h.level - 1) * 16;
              return `
                <div class="notion-toc-block-link" style="padding-left:${6 + indent}px;" onclick="scrollToHeadingByIndex(${h.idx})">
                  <span style="font-size:10px; color:var(--text-muted); font-weight:700;">H${h.level}</span>
                  <span>${escapeHtmlAttr(h.text)}</span>
                </div>
              `;
            }).join('');
          }
        });
      }
    }

    function scrollToHeadingByIndex(idx) {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const target = editor.querySelector(`[data-heading-idx="${idx}"]`) || editor.querySelectorAll('h1, h2, h3')[idx];
      if (!target) return;
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      target.classList.add('spatial-block-selected');
      setTimeout(() => target.classList.remove('spatial-block-selected'), 1100);

      document.querySelectorAll('.sticky-toc-bar-line').forEach(el => {
        el.classList.toggle('active', el.getAttribute('data-toc-bar') === String(idx));
      });
      document.querySelectorAll('.sticky-toc-item').forEach((el, i) => {
        el.classList.toggle('active', i === Number(idx));
      });
    }

    function toggleTocExpanded(e) {
      if (e) e.stopPropagation();
      const rail = document.getElementById('sticky-toc-rail');
      if (rail) {
        rail.classList.toggle('is-expanded');
      }
    }

    function initTocScrollSpy() {
      const editorBody = document.getElementById('editor-body');
      if (!editorBody) return;

      editorBody.addEventListener('scroll', () => {
        const headings = collectEditorHeadings();
        if (!headings.length) return;

        const bodyRect = editorBody.getBoundingClientRect();
        let activeIdx = 0;

        for (let i = 0; i < headings.length; i++) {
          const hRect = headings[i].el.getBoundingClientRect();
          if (hRect.top - bodyRect.top <= 140) {
            activeIdx = headings[i].idx;
          } else {
            break;
          }
        }

        document.querySelectorAll('.sticky-toc-bar-line').forEach(el => {
          el.classList.toggle('active', el.getAttribute('data-toc-bar') === String(activeIdx));
        });
        document.querySelectorAll('.sticky-toc-item').forEach((el, i) => {
          el.classList.toggle('active', i === Number(activeIdx));
        });
      }, { passive: true });

      document.addEventListener('click', (e) => {
        const rail = document.getElementById('sticky-toc-rail');
        if (rail && !rail.contains(e.target)) {
          rail.classList.remove('is-expanded');
        }
      });
    }

    function insertTableOfContentsBlock() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const tocEl = document.createElement('div');
      tocEl.className = 'notion-toc-block';
      tocEl.setAttribute('contenteditable', 'false');
      tocEl.innerHTML = `
        <div class="notion-toc-block-header">
          <span>📑 Tabla de Contenidos Automática</span>
          <button type="button" class="btn-icon-tiny btn-danger-tiny" onclick="this.closest('.notion-toc-block').remove(); syncRichEditor();" title="Eliminar bloque de índice">🗑</button>
        </div>
        <div class="notion-toc-block-links"></div>
      `;
      const pAfter = document.createElement('p');
      pAfter.innerHTML = '<br>';
      editor.appendChild(tocEl);
      editor.appendChild(pAfter);
      refreshPageTableOfContents();
      syncRichEditor();
      tocEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      showToast('Bloque Tabla de Contenidos (/toc) insertado', '📑');
    }

    // 4. Sistema de Columnas Paralelas Redimensionables (/columns y Drag & Drop a bordes laterales)
    function createColumnSlotElement(initialHtml = '<p>Escribe en esta columna...</p>') {
      const slot = document.createElement('div');
      slot.className = 'notion-column-slot';
      slot.setAttribute('contenteditable', 'true');
      slot.style.flex = '1 1 50%';
      slot.innerHTML = initialHtml;
      return slot;
    }

    function createColumnResizerElement() {
      const resizer = document.createElement('div');
      resizer.className = 'notion-column-resizer';
      resizer.setAttribute('contenteditable', 'false');
      resizer.title = 'Arrastra horizontalmente para ajustar el ancho de las columnas';
      return resizer;
    }

    function insertColumnsBlock(numCols = 2) {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const count = Math.max(2, Math.min(4, Number(numCols) || 2));
      const row = document.createElement('div');
      row.className = 'notion-columns-row';
      row.setAttribute('data-columns-count', String(count));

      const share = (100 / count).toFixed(2);
      for (let i = 0; i < count; i++) {
        if (i > 0) {
          row.appendChild(createColumnResizerElement());
        }
        const slot = createColumnSlotElement(`<p><strong>Columna ${i + 1}</strong></p><p>Redacta o arrastra bloques aquí...</p>`);
        slot.style.flex = `1 1 ${share}%`;
        row.appendChild(slot);
      }

      const trailingP = document.createElement('p');
      trailingP.innerHTML = '<br>';
      editor.appendChild(row);
      editor.appendChild(trailingP);

      attachColumnResizerListeners();
      syncRichEditor();
      row.scrollIntoView({ behavior: 'smooth', block: 'center' });
      showToast(`Retícula de ${count} columnas redimensionables creada`, '▥');
    }

    function attachColumnResizerListeners() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const resizers = editor.querySelectorAll('.notion-column-resizer');
      resizers.forEach(resizer => {
        if (resizer.dataset.boundResizer === 'true') return;
        resizer.dataset.boundResizer = 'true';

        resizer.addEventListener('mousedown', (e) => {
          e.preventDefault();
          e.stopPropagation();
          const prevSlot = resizer.previousElementSibling;
          const nextSlot = resizer.nextElementSibling;
          const row = resizer.closest('.notion-columns-row');
          if (!prevSlot || !nextSlot || !row) return;

          resizer.classList.add('resizing');
          const rowWidth = row.getBoundingClientRect().width || 600;
          const startX = e.clientX;
          const prevStartW = prevSlot.getBoundingClientRect().width;
          const nextStartW = nextSlot.getBoundingClientRect().width;
          const combinedW = prevStartW + nextStartW;

          const onMove = (moveEvt) => {
            const dx = moveEvt.clientX - startX;
            const minPx = 120;
            const newPrevW = Math.max(minPx, Math.min(combinedW - minPx, prevStartW + dx));
            const newNextW = combinedW - newPrevW;
            const prevPct = ((newPrevW / rowWidth) * 100).toFixed(2);
            const nextPct = ((newNextW / rowWidth) * 100).toFixed(2);
            prevSlot.style.flex = `1 1 ${prevPct}%`;
            nextSlot.style.flex = `1 1 ${nextPct}%`;
          };

          const onUp = () => {
            resizer.classList.remove('resizing');
            window.removeEventListener('mousemove', onMove);
            window.removeEventListener('mouseup', onUp);
            syncRichEditor();
          };

          window.addEventListener('mousemove', onMove);
          window.addEventListener('mouseup', onUp);
        });
      });
    }

    // 5. Bloques Sincronizados (Synced Blocks) con Marco Rojo Coral (#ef4444)
    let copiedSyncedBlockBuffer = null;

    function insertSyncedBlock(existingSyncId = null, initialHtml = null) {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const syncId = existingSyncId || ('sync-' + Date.now() + '-' + Math.floor(Math.random() * 1000));
      const bodyContent = initialHtml || '<p><strong>Bloque Sincronizado en Vivo:</strong> Cualquier edición dentro de este marco rojo coral se replica automáticamente en todas las notas que compartan esta referencia.</p>';

      const block = document.createElement('div');
      block.className = 'notion-synced-block';
      block.setAttribute('data-synced-id', syncId);
      block.innerHTML = `
        <div class="notion-synced-header" contenteditable="false">
          <span class="notion-synced-badge">🔴 Bloque sincronizado · ID ${syncId.slice(-4)}</span>
          <div class="notion-synced-actions">
            <button type="button" class="notion-synced-btn" onclick="copySyncedBlockReference('${syncId}')">🔗 Copiar referencia sincronizada</button>
            <button type="button" class="notion-synced-btn" onclick="unsyncBlockInstance(this)">Desvincular</button>
          </div>
        </div>
        <div class="notion-synced-body" contenteditable="true">${bodyContent}</div>
      `;

      const trailingP = document.createElement('p');
      trailingP.innerHTML = '<br>';
      editor.appendChild(block);
      editor.appendChild(trailingP);

      attachSyncedBlockListeners();
      syncRichEditor();
      block.scrollIntoView({ behavior: 'smooth', block: 'center' });
      showToast('Bloque Sincronizado con halo rojo coral creado', '🔄');
    }

    // Nota: copySyncedBlockReference legacy unificado en window.copySyncedBlockReference
    function pasteCopiedSyncedBlock() {
      if (!copiedSyncedBlockBuffer) {
        showToast('Primero copia una referencia desde un Bloque Sincronizado', 'ℹ️');
        return;
      }
      insertSyncedBlock(copiedSyncedBlockBuffer.syncId, copiedSyncedBlockBuffer.html);
    }

    // Nota: unsyncBlockInstance legacy unificado en window.unsyncBlockInstance

    function propagateSyncedBlockChange(syncId, updatedInnerHtml, sourceEl) {
      if (!syncId) return;
      if (copiedSyncedBlockBuffer && copiedSyncedBlockBuffer.syncId === syncId) {
        copiedSyncedBlockBuffer.html = updatedInnerHtml;
      }

      // 1. Actualizar otras instancias en el DOM actual
      const currentEditor = document.getElementById('rich-editor-canvas');
      if (currentEditor) {
        currentEditor.querySelectorAll(`.notion-synced-block[data-synced-id="${syncId}"] .notion-synced-body`).forEach(body => {
          if (body !== sourceEl && body.innerHTML !== updatedInnerHtml) {
            body.innerHTML = updatedInnerHtml;
          }
        });
      }

      // 2. Propagar a todas las demás notas en state.notes que contengan data-synced-id
      const activeId = state.activeNoteId;
      state.notes.forEach(note => {
        if (note.id === activeId || !note.content || !note.content.includes(syncId)) return;
        const temp = document.createElement('div');
        temp.innerHTML = note.content;
        let changed = false;
        temp.querySelectorAll(`.notion-synced-block[data-synced-id="${syncId}"] .notion-synced-body`).forEach(b => {
          if (b.innerHTML !== updatedInnerHtml) {
            b.innerHTML = updatedInnerHtml;
            changed = true;
          }
        });
        if (changed) {
          note.content = temp.innerHTML;
          note.updatedAt = Date.now();
          save(false, note);
        }
      });
    }

    function attachSyncedBlockListeners() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      editor.querySelectorAll('.notion-synced-block').forEach(block => {
        const syncId = block.getAttribute('data-synced-id');
        const body = block.querySelector('.notion-synced-body');
        if (!body || body.dataset.boundSync === 'true') return;
        body.dataset.boundSync = 'true';
        body.addEventListener('input', () => {
          propagateSyncedBlockChange(syncId, body.innerHTML, body);
          syncRichEditor();
        });
      });
    }

    // 6. Botones de Automatización (Button Block)
    let editingMacroButtonEl = null;

    const MACRO_BUTTON_PRESETS = {
      tasks: `<div style="padding:10px 12px; border-left:3px solid #3b82f6; background:rgba(59,130,246,0.08); border-radius:6px; margin:8px 0;"><strong>☑ Rutina del {{HOY}} ({{HORA}})</strong><ul><li>[ ] Revisar prioridades clave del bloque</li><li>[ ] Documentar avances en Note JS</li><li>[ ] Sincronizar entregables pendientes</li></ul></div>`,
      meeting: `<h2>📅 Minuta de Sesión — {{HOY}} ({{HORA}})</h2><p><strong>Participantes:</strong> Equipo de Producto &amp; Ingeniería</p><p><strong>Acuerdos clave:</strong></p><ul><li>Punto de acción 1</li><li>Punto de acción 2</li></ul>`,
      columns2: `<div class="notion-columns-row" data-columns-count="2"><div class="notion-column-slot" contenteditable="true" style="flex:1 1 50%;"><p><strong>🎯 Objetivos ({{HOY}})</strong></p><p>Describe las metas aquí...</p></div><div class="notion-column-resizer" contenteditable="false"></div><div class="notion-column-slot" contenteditable="true" style="flex:1 1 50%;"><p><strong>📝 Notas y Bloqueos</strong></p><p>Registra observaciones...</p></div></div>`,
      callout: `<div style="padding:12px 14px; border-radius:8px; background:rgba(245,158,11,0.14); border:1px solid rgba(245,158,11,0.4); margin:8px 0;">💡 <strong>Nota rápida ({{HOY}} - {{HORA}}):</strong> Escribe tu recordatorio aquí...</div>`,
      custom: `<p>✨ Nuevo bloque generado automáticamente el <strong>{{HOY}}</strong> a las <strong>{{HORA}}</strong>.</p>`
    };

    function openMacroButtonModal(existingBlockEl = null) {
      editingMacroButtonEl = existingBlockEl || null;
      const modal = document.getElementById('macro-button-modal');
      if (!modal) return;

      const emojiInput = document.getElementById('macro-btn-emoji-input');
      const labelInput = document.getElementById('macro-btn-label-input');
      const posSelect = document.getElementById('macro-btn-position-select');
      const presetSelect = document.getElementById('macro-btn-preset-select');
      const tplInput = document.getElementById('macro-btn-template-input');
      const confirmChk = document.getElementById('macro-btn-confirm-checkbox');

      if (existingBlockEl) {
        if (emojiInput) emojiInput.value = existingBlockEl.getAttribute('data-macro-emoji') || '⚡';
        if (labelInput) labelInput.value = existingBlockEl.getAttribute('data-macro-label') || 'Insertar plantilla rápida';
        if (posSelect) posSelect.value = existingBlockEl.getAttribute('data-macro-pos') || 'below';
        if (presetSelect) presetSelect.value = 'custom';
        if (tplInput) tplInput.value = decodeURIComponent(existingBlockEl.getAttribute('data-macro-template') || '');
        if (confirmChk) confirmChk.checked = existingBlockEl.getAttribute('data-macro-confirm') === 'true';
      } else {
        if (emojiInput) emojiInput.value = '⚡';
        if (labelInput) labelInput.value = 'Insertar checklist diario';
        if (posSelect) posSelect.value = 'below';
        if (presetSelect) presetSelect.value = 'tasks';
        if (tplInput) tplInput.value = MACRO_BUTTON_PRESETS.tasks;
        if (confirmChk) confirmChk.checked = false;
      }

      modal.classList.add('open');
    }

    function closeMacroButtonModal() {
      const modal = document.getElementById('macro-button-modal');
      if (modal) modal.classList.remove('open');
      editingMacroButtonEl = null;
    }

    function applyMacroButtonPreset(presetKey) {
      const tplInput = document.getElementById('macro-btn-template-input');
      const labelInput = document.getElementById('macro-btn-label-input');
      if (tplInput && MACRO_BUTTON_PRESETS[presetKey]) {
        tplInput.value = MACRO_BUTTON_PRESETS[presetKey];
      }
      const defaultLabels = {
        tasks: 'Insertar checklist diario',
        meeting: 'Crear minuta de reunión',
        columns2: 'Desplegar 2 columnas de trabajo',
        callout: 'Añadir aviso destacado',
        custom: 'Ejecutar bloque personalizado'
      };
      if (labelInput && defaultLabels[presetKey]) {
        labelInput.value = defaultLabels[presetKey];
      }
    }

    function buildMacroButtonBlockElement(emoji, label, position, templateHtml, requireConfirm) {
      const wrapper = document.createElement('div');
      wrapper.className = 'notion-macro-button-block';
      wrapper.setAttribute('contenteditable', 'false');
      wrapper.setAttribute('data-macro-emoji', emoji);
      wrapper.setAttribute('data-macro-label', label);
      wrapper.setAttribute('data-macro-pos', position);
      wrapper.setAttribute('data-macro-template', encodeURIComponent(templateHtml));
      wrapper.setAttribute('data-macro-confirm', String(Boolean(requireConfirm)));

      wrapper.innerHTML = `
        <button type="button" class="notion-macro-trigger-btn" onclick="executeMacroButtonBlock(this)">
          <span>${escapeHtmlAttr(emoji)}</span>
          <span>${escapeHtmlAttr(label)}</span>
        </button>
        <button type="button" class="notion-macro-config-btn" onclick="openMacroButtonModal(this.closest('.notion-macro-button-block'))" title="Configurar pasos del botón">⚙️</button>
      `;
      return wrapper;
    }

    function saveMacroButtonConfig() {
      const emoji = (document.getElementById('macro-btn-emoji-input')?.value || '⚡').trim() || '⚡';
      const label = (document.getElementById('macro-btn-label-input')?.value || 'Ejecutar acción').trim();
      const position = document.getElementById('macro-btn-position-select')?.value || 'below';
      const templateHtml = document.getElementById('macro-btn-template-input')?.value || MACRO_BUTTON_PRESETS.custom;
      const requireConfirm = Boolean(document.getElementById('macro-btn-confirm-checkbox')?.checked);

      const newBlock = buildMacroButtonBlockElement(emoji, label, position, templateHtml, requireConfirm);
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;

      if (editingMacroButtonEl && editor.contains(editingMacroButtonEl)) {
        editingMacroButtonEl.replaceWith(newBlock);
      } else {
        const trailingP = document.createElement('p');
        trailingP.innerHTML = '<br>';
        editor.appendChild(newBlock);
        editor.appendChild(trailingP);
      }

      closeMacroButtonModal();
      syncRichEditor();
      showToast(`Botón de automatización "${label}" listo`, emoji);
    }

    function executeMacroButtonBlock(triggerBtn) {
      const block = triggerBtn ? triggerBtn.closest('.notion-macro-button-block') : null;
      const editor = document.getElementById('rich-editor-canvas');
      if (!block || !editor) return;

      const label = block.getAttribute('data-macro-label') || 'Automatización';
      const pos = block.getAttribute('data-macro-pos') || 'below';
      const rawTemplate = decodeURIComponent(block.getAttribute('data-macro-template') || '');
      const requireConfirm = block.getAttribute('data-macro-confirm') === 'true';

      if (requireConfirm) {
        const ok = window.confirm(`¿Ejecutar el flujo del botón "${label}"?`);
        if (!ok) return;
      }

      const now = new Date();
      const fechaStr = now.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' });
      const horaStr = now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
      const hydratedHtml = rawTemplate
        .replace(/\{\{HOY\}\}/gi, fechaStr)
        .replace(/\{\{HORA\}\}/gi, horaStr);

      const note = getActiveNote();

      // Modo 1: Crear nueva página y registro en la Base de Datos
      if (pos === 'create_db_page' && note) {
        const plainTitle = hydratedHtml.replace(/<[^>]*>?/gm, '').trim() || `Página generada (${fechaStr})`;
        note.showTable = true;
        note.tableRows = note.tableRows || [];
        note.tableRows.unshift({
          name: plainTitle.slice(0, 60),
          status: 'En Proceso',
          category: 'Automatización',
          date: now.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' }),
          amount: 100
        });
        save();
        loadActiveNote();
        showToast(`Nueva página "${plainTitle.slice(0, 32)}" creada en la Base de Datos`, '🗄️');
        return;
      }

      // Modo 2: Editar propiedades de forma masiva en la Base de Datos
      if (pos === 'bulk_mark_done' && note) {
        note.showTable = true;
        note.tableRows = note.tableRows || [];
        note.tableRows.forEach(r => { r.status = 'Listo'; });
        save();
        loadActiveNote();
        showToast('Propiedades actualizadas masivamente: todos los registros marcados como "Listo"', '✅');
        return;
      }

      // Modo 3: Inyectar múltiples bloques de texto en la posición elegida
      const temp = document.createElement('div');
      temp.innerHTML = hydratedHtml;
      const nodes = Array.from(temp.childNodes);

      if (pos === 'above') {
        nodes.forEach(n => block.before(n));
      } else if (pos === 'top') {
        nodes.reverse().forEach(n => editor.prepend(n));
      } else if (pos === 'bottom') {
        nodes.forEach(n => editor.appendChild(n));
      } else {
        let ref = block;
        nodes.forEach(n => {
          ref.after(n);
          ref = n;
        });
      }

      attachColumnResizerListeners();
      attachSyncedBlockListeners();
      refreshPageTableOfContents();
      syncRichEditor();
      showToast(`Flujo "${label}" ejecutado`, '⚡');
    }

    // 6B. Bloques Básicos y Avanzados en el Lienzo (Tablas Simples, Toggles, Callouts, Divisores, Código, Migas de Pan)
    function insertDividerElement() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const hr = document.createElement('hr');
      hr.className = 'notion-divider';
      const pAfter = document.createElement('p');
      pAfter.innerHTML = '<br>';
      editor.appendChild(hr);
      editor.appendChild(pAfter);
      syncRichEditor();
      showToast('Línea divisoria insertada', '—');
    }

    function insertInlineCalloutElement() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const callout = document.createElement('div');
      callout.className = 'notion-inline-callout';
      callout.innerHTML = `
        <span class="notion-inline-callout-emoji" contenteditable="false" onclick="cycleInlineCalloutEmoji(this)" title="Clic para cambiar icono">💡</span>
        <div class="notion-inline-callout-body" contenteditable="true"><strong>Consejo o nota destacada:</strong> Escribe aquí una advertencia, recordatorio o apunte clave...</div>
      `;
      const pAfter = document.createElement('p');
      pAfter.innerHTML = '<br>';
      editor.appendChild(callout);
      editor.appendChild(pAfter);
      syncRichEditor();
      callout.scrollIntoView({ behavior: 'smooth', block: 'center' });
      showToast('Caja de llamada (Callout) insertada', '💡');
    }

    function cycleInlineCalloutEmoji(emojiSpan) {
      if (!emojiSpan) return;
      const icons = ['💡', '⚠️', '📌', '🚀', '🔥', '✅', '🧠', '📘', '🎯'];
      const cur = emojiSpan.textContent.trim();
      const next = icons[(icons.indexOf(cur) + 1) % icons.length];
      emojiSpan.textContent = next;
      syncRichEditor();
    }

    function insertInlineToggleElement() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const details = document.createElement('details');
      details.className = 'notion-inline-toggle';
      details.open = true;
      details.innerHTML = `
        <summary><span class="notion-inline-toggle-arrow">▶</span><span>Lista desplegable (Toggle): Haz clic en la flecha para ocultar o expandir</span></summary>
        <div class="notion-inline-toggle-content" contenteditable="true">
          <p>Contenido anidado dentro del Toggle. También puedes arrastrar otros bloques aquí con la guía azul indentada.</p>
        </div>
      `;
      const pAfter = document.createElement('p');
      pAfter.innerHTML = '<br>';
      editor.appendChild(details);
      editor.appendChild(pAfter);
      syncRichEditor();
      details.scrollIntoView({ behavior: 'smooth', block: 'center' });
      showToast('Lista desplegable (Toggle) insertada', '▶');
    }

    function insertSimpleTableBlock() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const wrapper = document.createElement('div');
      wrapper.className = 'notion-simple-table-block';
      wrapper.innerHTML = `
        <table class="notion-simple-table">
          <thead>
            <tr>
              <th>Columna A</th>
              <th>Columna B</th>
              <th>Columna C</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Dato 1</td>
              <td>Descripción</td>
              <td>Observación</td>
            </tr>
            <tr>
              <td>Dato 2</td>
              <td>Descripción</td>
              <td>Observación</td>
            </tr>
          </tbody>
        </table>
        <div class="notion-simple-table-controls" contenteditable="false">
          <button type="button" class="btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="addSimpleTableRow(this)">+ Fila</button>
          <button type="button" class="btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="addSimpleTableCol(this)">+ Columna</button>
          <button type="button" class="btn-secondary" style="padding:2px 8px; font-size:11px; color:var(--danger);" onclick="this.closest('.notion-simple-table-block').remove(); syncRichEditor();">🗑 Eliminar tabla</button>
        </div>
      `;
      const pAfter = document.createElement('p');
      pAfter.innerHTML = '<br>';
      editor.appendChild(wrapper);
      editor.appendChild(pAfter);
      syncRichEditor();
      wrapper.scrollIntoView({ behavior: 'smooth', block: 'center' });
      showToast('Tabla simple estática insertada', '⊞');
    }

    function addSimpleTableRow(btn) {
      const block = btn ? btn.closest('.notion-simple-table-block') : null;
      const tbody = block ? block.querySelector('tbody') : null;
      const firstRow = block ? block.querySelector('tr') : null;
      if (!tbody || !firstRow) return;
      const colCount = firstRow.children.length;
      const tr = document.createElement('tr');
      for (let i = 0; i < colCount; i++) {
        const td = document.createElement('td');
        td.textContent = 'Nueva celda';
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
      syncRichEditor();
    }

    function addSimpleTableCol(btn) {
      const block = btn ? btn.closest('.notion-simple-table-block') : null;
      if (!block) return;
      const rows = block.querySelectorAll('tr');
      rows.forEach((tr, idx) => {
        const cell = document.createElement(idx === 0 ? 'th' : 'td');
        cell.textContent = idx === 0 ? `Columna ${tr.children.length + 1}` : 'Celda';
        tr.appendChild(cell);
      });
      syncRichEditor();
    }

    function insertInlineCodeBlock() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const block = document.createElement('div');
      block.className = 'notion-media-embed-block';
      block.innerHTML = `
        <div class="notion-media-embed-header" contenteditable="false">
          <div style="display:flex; align-items:center; gap:8px;">
            <span>&lt;/&gt; Bloque de Código</span>
            <select class="search-box" style="padding:2px 6px; font-size:11px;" onchange="syncRichEditor()">
              <option>JavaScript / TypeScript</option>
              <option>Python</option>
              <option>SQL</option>
              <option>HTML / CSS</option>
              <option>Bash / Shell</option>
            </select>
          </div>
          <button type="button" class="btn-secondary" style="padding:2px 8px; font-size:11px;" onclick="navigator.clipboard.writeText(this.closest('.notion-media-embed-block').querySelector('pre').innerText); showToast('Código copiado', '📋');">📋 Copiar</button>
        </div>
        <pre contenteditable="true" style="margin:0; padding:12px 14px; font-family:var(--font-mono); font-size:12.5px; color:#38bdf8; background:#0d1117; overflow-x:auto; outline:none;">// Escribe o pega tu código con sintaxis aquí
function procesarBloquesNotion(bloques) {
  return bloques.filter(b => b.activo);
}</pre>
      `;
      const pAfter = document.createElement('p');
      pAfter.innerHTML = '<br>';
      editor.appendChild(block);
      editor.appendChild(pAfter);
      syncRichEditor();
      block.scrollIntoView({ behavior: 'smooth', block: 'center' });
      showToast('Bloque de código insertado', '</>');
    }

    function insertBreadcrumbsBlock() {
      const editor = document.getElementById('rich-editor-canvas');
      const note = getActiveNote();
      if (!editor || !note) return;
      const parentNote = note.parentId ? state.notes.find(n => n.id === note.parentId) : null;
      const folderEmoji = getFolderEmoji(note.folder || 'Personal');

      const crumb = document.createElement('div');
      crumb.className = 'notion-breadcrumbs-block';
      crumb.setAttribute('contenteditable', 'false');
      crumb.innerHTML = `
        <span style="cursor:pointer;" onclick="selectFolder('${escapeHtmlAttr(note.folder || 'Personal')}')">${folderEmoji} ${escapeHtmlAttr(note.folder || 'Personal')}</span>
        ${parentNote ? `<span>/</span><span style="cursor:pointer;" onclick="selectNote(${parentNote.id})">${parentNote.emoji || '📄'} ${escapeHtmlAttr(parentNote.title)}</span>` : ''}
        <span>/</span>
        <strong style="color:var(--text-primary);">${note.emoji || '📝'} ${escapeHtmlAttr(note.title || 'Sin título')}</strong>
      `;
      const pAfter = document.createElement('p');
      pAfter.innerHTML = '<br>';
      editor.appendChild(crumb);
      editor.appendChild(pAfter);
      syncRichEditor();
      showToast('Bloque de Migas de Pan (Breadcrumbs) insertado', '🧭');
    }

    // 6C. Bases de Datos Multi-Vista (6 Vistas: Tabla, Tablero Kanban, Galería, Lista, Calendario y Cronograma)
    function openDatabaseWithView(viewKey = 'table') {
      const note = getActiveNote();
      if (!note) return;
      note.showTable = true;
      note.dbActiveView = viewKey;
      if (!note.tableRows || !note.tableRows.length) {
        note.tableRows = [
          { name: "Arquitectura de Bloques PC", status: "Listo", category: "Core UI", date: "27 Oct", amount: 320 },
          { name: "Sincronización Halo Rojo", status: "En Proceso", category: "Frontend", date: "28 Oct", amount: 450 },
          { name: "Vistas de Base de Datos", status: "Pendiente", category: "Datos", date: "29 Oct", amount: 280 }
        ];
      }
      save();
      loadActiveNote();
      switchDatabaseView(viewKey);
      scrollAndHighlightBlock('block-table');
      const labels = {
        table: 'Tabla',
        board: 'Tablero Kanban',
        gallery: 'Galería Visual',
        list: 'Lista Minimalista',
        calendar: 'Calendario',
        timeline: 'Cronograma',
        chart: 'Gráfico Estadístico',
        form: 'Formulario de Captura',
        dash: 'Panel de Control'
      };
      showToast(`Base de Datos abierta en vista ${labels[viewKey] || viewKey}`, '🗄️');
    }

    function switchDatabaseView(viewKey) {
      const note = getActiveNote();
      if (!note) return;
      note.dbActiveView = viewKey || 'table';
      save(false, note);
      renderDatabaseActiveView(note);
    }

    let draggingKanbanRowIndex = null;

    function handleKanbanCardDragStart(e, rowIndex) {
      draggingKanbanRowIndex = rowIndex;
      e.dataTransfer.setData('text/plain', String(rowIndex));
      e.dataTransfer.effectAllowed = 'move';
      if (e.target && e.target.classList) {
        e.target.classList.add('block-is-dragging');
      }
    }

    function handleKanbanCardDrop(e, targetStatus) {
      e.preventDefault();
      const note = getActiveNote();
      if (!note || !note.tableRows || draggingKanbanRowIndex === null) return;
      const row = note.tableRows[draggingKanbanRowIndex];
      if (row) {
        row.status = targetStatus;
        save(false, note);
        renderDatabaseActiveView(note);
        showToast(`Tarjeta movida a "${targetStatus}"`, '📊');
      }
      draggingKanbanRowIndex = null;
    }

    function submitDbFormRow(e) {
      e.preventDefault();
      const note = getActiveNote();
      if (!note) return;
      const nameInput = document.getElementById('db-form-name');
      const statusInput = document.getElementById('db-form-status');
      const catInput = document.getElementById('db-form-category');
      const dateInput = document.getElementById('db-form-date');
      const amountInput = document.getElementById('db-form-amount');

      const name = (nameInput?.value || '').trim();
      if (!name) {
        showToast('Introduce un nombre para el registro', '⚠️');
        return;
      }

      if (!Array.isArray(note.tableRows)) note.tableRows = [];
      note.tableRows.push({
        name,
        status: statusInput?.value || 'Pendiente',
        category: catInput?.value || 'General',
        date: dateInput?.value || 'Hoy',
        amount: Number(amountInput?.value || 0)
      });

      save(false, note);
      showToast('Registro guardado en la Base de Datos', '✅');
      switchDatabaseView('table');
    }

    function renderDatabaseActiveView(note) {
      if (!note) return;
      const view = note.dbActiveView || 'table';
      const tablePanel = document.getElementById('db-view-panel-table');
      const dynPanel = document.getElementById('db-view-panel-dynamic');
      const tabs = document.querySelectorAll('#db-view-tabs .db-view-tab');

      tabs.forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-db-view') === view);
      });

      if (!tablePanel || !dynPanel) return;

      if (view === 'table') {
        tablePanel.style.display = 'block';
        dynPanel.style.display = 'none';
        return;
      }

      tablePanel.style.display = 'none';
      dynPanel.style.display = 'block';
      const rows = note.tableRows || [];

      if (view === 'board') {
        const cols = [
          { key: 'Pendiente', color: '#f59e0b', items: [] },
          { key: 'En Proceso', color: '#3b82f6', items: [] },
          { key: 'Listo', color: '#10b981', items: [] }
        ];

        rows.forEach((r, idx) => {
          const st = (r.status || '').toLowerCase();
          if (st.includes('listo') || st.includes('pagado') || st.includes('completado') || st.includes('done')) {
            cols[2].items.push({ row: r, originalIndex: idx });
          } else if (st.includes('proceso') || st.includes('progreso') || st.includes('in progress')) {
            cols[1].items.push({ row: r, originalIndex: idx });
          } else {
            cols[0].items.push({ row: r, originalIndex: idx });
          }
        });

        dynPanel.innerHTML = `
          <div class="kanban-board">
            ${cols.map(col => `
              <div class="kanban-column"
                   ondragover="event.preventDefault(); event.dataTransfer.dropEffect='move';"
                   ondrop="handleKanbanCardDrop(event, '${col.key}')"
                   style="min-height:220px; transition: background 0.15s ease;">
                <div class="kanban-col-header" style="color:${col.color}; display:flex; justify-content:space-between; align-items:center;">
                  <span style="font-weight:800; font-size:12.5px;">● ${col.key}</span>
                  <span class="tabular-nums" style="background:rgba(255,255,255,0.08); padding:2px 6px; border-radius:99px; font-size:11px;">${col.items.length}</span>
                </div>
                <div style="display:flex; flex-direction:column; gap:8px; margin-top:8px;">
                  ${col.items.map(item => `
                    <div class="kanban-card"
                         draggable="true"
                         ondragstart="handleKanbanCardDragStart(event, ${item.originalIndex})"
                         ondragend="this.classList.remove('block-is-dragging')"
                         style="padding:10px 12px; border-radius:8px; background:var(--bg-surface); border:1px solid var(--border-subtle); cursor:grab; box-shadow:0 2px 6px rgba(0,0,0,0.18);">
                      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                        <span style="font-weight:700; font-size:12.5px; color:var(--text-primary);">${escapeHtmlAttr(item.row.name)}</span>
                        <span style="font-size:10px; opacity:0.6;">⋮⋮</span>
                      </div>
                      <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px; color:var(--text-muted);">
                        <span style="background:rgba(255,255,255,0.06); padding:2px 6px; border-radius:4px;">🏷️ ${escapeHtmlAttr(item.row.category || 'General')}</span>
                        <span class="tabular-nums" style="font-weight:700; color:var(--text-secondary);">$${Number(item.row.amount || 0).toLocaleString()}</span>
                      </div>
                    </div>
                  `).join('') || `<div style="font-size:11.5px; color:var(--text-muted); padding:16px 8px; text-align:center; border:1px dashed var(--border-subtle); border-radius:6px;">Arrastra tarjetas aquí</div>`}
                </div>
              </div>
            `).join('')}
          </div>
        `;
      } else if (view === 'gallery') {
        dynPanel.innerHTML = `
          <div class="db-gallery-grid">
            ${rows.map((row, idx) => {
              const bg = COVER_PRESETS[idx % COVER_PRESETS.length];
              return `
                <div class="db-gallery-card">
                  <div class="db-gallery-card-cover" style="background-image:${bg};">
                    <span style="background:rgba(15,23,42,0.75); color:#fff; font-size:10px; font-weight:700; padding:2px 7px; border-radius:99px;">${escapeHtmlAttr(row.status || 'Activo')}</span>
                  </div>
                  <div class="db-gallery-card-body">
                    <div style="font-weight:800; font-size:13px; color:var(--text-primary); margin-bottom:4px;">${escapeHtmlAttr(row.name)}</div>
                    <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-muted);">
                      <span>${escapeHtmlAttr(row.category || 'General')} · ${escapeHtmlAttr(row.date || 'Hoy')}</span>
                      <strong style="color:var(--text-secondary);">$${Number(row.amount || 0).toLocaleString()}</strong>
                    </div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        `;
      } else if (view === 'list') {
        dynPanel.innerHTML = `
          <div class="db-list-container">
            ${rows.map(row => `
              <div class="db-list-row">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span>📄</span>
                  <strong style="font-size:13px; color:var(--text-primary);">${escapeHtmlAttr(row.name)}</strong>
                </div>
                <div style="display:flex; align-items:center; gap:10px; font-size:11.5px; color:var(--text-muted);">
                  <span style="padding:2px 7px; border-radius:99px; background:var(--bg-elevated); color:var(--text-secondary); font-weight:700;">${escapeHtmlAttr(row.status)}</span>
                  <span>${escapeHtmlAttr(row.category)}</span>
                  <span class="tabular-nums">${escapeHtmlAttr(row.date)}</span>
                  <strong class="tabular-nums" style="color:var(--text-primary);">$${Number(row.amount || 0).toLocaleString()}</strong>
                </div>
              </div>
            `).join('')}
          </div>
        `;
      } else if (view === 'calendar') {
        const days = ['Lun 25', 'Mar 26', 'Mié 27', 'Jue 28', 'Vie 29', 'Sáb 30', 'Dom 31'];
        dynPanel.innerHTML = `
          <div class="db-calendar-grid">
            ${days.map((d, i) => {
              const dayNum = d.split(' ')[1];
              const matches = rows.filter((r, rIdx) => (r.date || '').includes(dayNum) || (rIdx % 7 === i));
              return `
                <div class="db-calendar-cell">
                  <div style="font-weight:800; color:var(--text-muted); margin-bottom:5px;">${d}</div>
                  ${matches.map(m => `
                    <div style="padding:3px 6px; margin-bottom:3px; border-radius:4px; background:rgba(59,130,246,0.18); border-left:2px solid #3b82f6; font-size:10.5px; font-weight:700; color:var(--text-primary); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                      ${escapeHtmlAttr(m.name)}
                    </div>
                  `).join('')}
                </div>
              `;
            }).join('')}
          </div>
        `;
      } else if (view === 'timeline') {
        dynPanel.innerHTML = `
          <div class="db-timeline-list">
            ${rows.map((row, idx) => {
              const offset = (idx * 18) % 55;
              const width = Math.max(30, 75 - offset);
              const barColor = (row.status || '').toLowerCase().includes('listo') ? '#10b981' : ((row.status || '').toLowerCase().includes('proceso') ? '#3b82f6' : '#f59e0b');
              return `
                <div class="db-timeline-row">
                  <div style="font-size:12px; font-weight:700; color:var(--text-primary); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${escapeHtmlAttr(row.name)}</div>
                  <div class="db-timeline-bar-track">
                    <div class="db-timeline-bar-fill" style="margin-left:${offset}%; width:${width}%; background:${barColor};">
                      ${escapeHtmlAttr(row.date || 'Oct')} · ${escapeHtmlAttr(row.status)}
                    </div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        `;
      } else if (view === 'chart') {
        const totalRows = rows.length;
        const totalAmount = rows.reduce((s, r) => s + (Number(r.amount) || 0), 0);
        const completedCount = rows.filter(r => (r.status || '').toLowerCase().includes('listo')).length;
        const avgAmount = totalRows ? Math.round(totalAmount / totalRows) : 0;

        // Agrupar por categoría
        const catMap = {};
        rows.forEach(r => {
          const cat = r.category || 'General';
          catMap[cat] = (catMap[cat] || 0) + (Number(r.amount) || 0);
        });
        const categories = Object.keys(catMap);
        const maxVal = Math.max(1, ...Object.values(catMap));
        const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#06b6d4'];

        dynPanel.innerHTML = `
          <div class="db-chart-container">
            <div class="chart-kpi-grid">
              <div class="chart-kpi-card">
                <div class="chart-kpi-label">Registros Totales</div>
                <div class="chart-kpi-value">${totalRows}</div>
              </div>
              <div class="chart-kpi-card">
                <div class="chart-kpi-label">Presupuesto Acumulado</div>
                <div class="chart-kpi-value" style="color:#10b981;">$${totalAmount.toLocaleString()}</div>
              </div>
              <div class="chart-kpi-card">
                <div class="chart-kpi-label">Tasa de Entrega</div>
                <div class="chart-kpi-value" style="color:#3b82f6;">${totalRows ? Math.round((completedCount / totalRows) * 100) : 0}%</div>
              </div>
              <div class="chart-kpi-card">
                <div class="chart-kpi-label">Promedio por Registro</div>
                <div class="chart-kpi-value" style="color:#f59e0b;">$${avgAmount.toLocaleString()}</div>
              </div>
            </div>

            <div class="chart-bars-wrap">
              <div style="font-weight:800; font-size:13px; color:var(--text-primary); margin-bottom:6px;">
                Distribución de Presupuesto por Categoría
              </div>
              ${categories.map((cat, idx) => {
                const val = catMap[cat];
                const pct = Math.round((val / maxVal) * 100);
                const color = colors[idx % colors.length];
                return `
                  <div class="chart-bar-item">
                    <div class="chart-bar-header">
                      <span>🏷️ ${escapeHtmlAttr(cat)}</span>
                      <span class="tabular-nums" style="color:${color};">$${val.toLocaleString()} (${pct}%)</span>
                    </div>
                    <div class="chart-bar-track">
                      <div class="chart-bar-fill" style="width:${pct}%; background:${color};"></div>
                    </div>
                  </div>
                `;
              }).join('') || `<div style="color:var(--text-muted); font-size:12px; padding:8px;">Sin datos para graficar</div>`}
            </div>
          </div>
        `;
      } else if (view === 'form') {
        dynPanel.innerHTML = `
          <div class="db-form-container">
            <div style="margin-bottom:14px; text-align:center;">
              <h4 style="margin:0; font-size:16px; font-weight:800; color:var(--text-primary);">Formulario de Captura para Base de Datos</h4>
              <p style="margin:4px 0 0; font-size:12px; color:var(--text-muted);">Completa los campos para inyectar un nuevo registro estructurado</p>
            </div>
            <form onsubmit="submitDbFormRow(event)">
              <div style="display:flex; flex-direction:column; gap:12px;">
                <div>
                  <label style="font-size:11.5px; font-weight:700; color:var(--text-muted); display:block; margin-bottom:4px;">Nombre del elemento *</label>
                  <input id="db-form-name" type="text" class="search-box" style="width:100%;" placeholder="Ej. Lanzamiento Beta, Auditoría de Seguridad..." required />
                </div>
                <div class="db-form-grid">
                  <div>
                    <label style="font-size:11.5px; font-weight:700; color:var(--text-muted); display:block; margin-bottom:4px;">Estado</label>
                    <select id="db-form-status" class="search-box" style="width:100%; cursor:pointer;">
                      <option value="Pendiente">Pendiente</option>
                      <option value="En Proceso">En Proceso</option>
                      <option value="Listo">Listo</option>
                    </select>
                  </div>
                  <div>
                    <label style="font-size:11.5px; font-weight:700; color:var(--text-muted); display:block; margin-bottom:4px;">Categoría</label>
                    <input id="db-form-category" type="text" class="search-box" style="width:100%;" placeholder="Ej. Core UI, Backend, Marketing" value="General" />
                  </div>
                </div>
                <div class="db-form-grid">
                  <div>
                    <label style="font-size:11.5px; font-weight:700; color:var(--text-muted); display:block; margin-bottom:4px;">Fecha</label>
                    <input id="db-form-date" type="text" class="search-box" style="width:100%;" placeholder="Ej. 29 Oct, 15 Nov" value="Hoy" />
                  </div>
                  <div>
                    <label style="font-size:11.5px; font-weight:700; color:var(--text-muted); display:block; margin-bottom:4px;">Monto ($ USD)</label>
                    <input id="db-form-amount" type="number" class="search-box" style="width:100%;" placeholder="0" value="100" />
                  </div>
                </div>
                <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:10px;">
                  <button type="button" class="btn-secondary" onclick="switchDatabaseView('table')">Cancelar</button>
                  <button type="submit" class="btn-primary">+ Añadir registro a la Base de Datos</button>
                </div>
              </div>
            </form>
          </div>
        `;
      } else if (view === 'dash') {
        const totalRows = rows.length;
        const totalAmount = rows.reduce((s, r) => s + (Number(r.amount) || 0), 0);
        const completedRows = rows.filter(r => (r.status || '').toLowerCase().includes('listo'));
        const pendingRows = rows.filter(r => !(r.status || '').toLowerCase().includes('listo'));

        dynPanel.innerHTML = `
          <div class="db-dash-grid">
            <div class="db-dash-card">
              <div>
                <span class="chart-kpi-label">Centro de Control</span>
                <h4 style="margin:4px 0 0; font-size:16px; font-weight:800; color:var(--text-primary);">Dashboard Multi-Vista</h4>
              </div>
              <div style="font-size:12px; color:var(--text-muted);">
                Gestión centralizada de tus notas, tareas y presupuestos con cálculo en tiempo real.
              </div>
              <div style="display:flex; gap:6px;">
                <button class="btn-primary" style="padding:4px 10px; font-size:11px;" onclick="switchDatabaseView('form')">+ Nuevo registro</button>
                <button class="btn-secondary" style="padding:4px 10px; font-size:11px;" onclick="switchDatabaseView('board')">Ver Kanban</button>
              </div>
            </div>

            <div class="db-dash-card">
              <span class="chart-kpi-label">Estado de Entregas</span>
              <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <span class="chart-kpi-value" style="color:#10b981;">${completedRows.length} Listas</span>
                <span style="font-size:12px; color:var(--text-muted);">${pendingRows.length} Pendientes</span>
              </div>
              <div class="chart-bar-track">
                <div class="chart-bar-fill" style="width:${totalRows ? Math.round((completedRows.length / totalRows) * 100) : 0}%; background:#10b981;"></div>
              </div>
            </div>

            <div class="db-dash-card">
              <span class="chart-kpi-label">Presupuesto Comprometido</span>
              <div class="chart-kpi-value" style="color:#3b82f6;">$${totalAmount.toLocaleString()}</div>
              <div style="font-size:11px; color:var(--text-muted);">Fórmulas 2.0 y agregación en tiempo real</div>
            </div>

            <div class="db-dash-card">
              <span class="chart-kpi-label">Accesos Rápidos</span>
              <div style="display:flex; flex-wrap:wrap; gap:6px;">
                <button class="btn-secondary" style="padding:3px 8px; font-size:11px;" onclick="switchDatabaseView('table')">▦ Tabla</button>
                <button class="btn-secondary" style="padding:3px 8px; font-size:11px;" onclick="switchDatabaseView('chart')">📈 Gráfico</button>
                <button class="btn-secondary" style="padding:3px 8px; font-size:11px;" onclick="switchDatabaseView('timeline')">⏳ Cronograma</button>
                <button class="btn-secondary" style="padding:3px 8px; font-size:11px;" onclick="toggleBlockCatalog(true)">📖 Catálogo 48 Bloques</button>
              </div>
            </div>
          </div>
        `;
      }
    }

    // 6D. Bloques de Archivos (PDF) e Incrustaciones Externas (Drive, Maps, Figma, Typeform, GitHub/CodePen, Loom)
    let currentMediaEmbedType = 'pdf';

    const EMBED_TYPE_META = {
      pdf: { icon: '📑', title: 'Documento PDF o Archivo Adjunto', placeholder: 'https://ejemplo.com/documento.pdf o sube un PDF local' },
      gdrive: { icon: '📁', title: 'Google Drive (Docs, Sheets, Slides)', placeholder: 'https://docs.google.com/document/d/...' },
      gmaps: { icon: '🗺️', title: 'Google Maps Interactivo', placeholder: 'Madrid, España o enlace de Google Maps' },
      figma: { icon: '🎨', title: 'Diseño de Figma / InVision', placeholder: 'https://www.figma.com/file/...' },
      typeform: { icon: '📋', title: 'Formulario de Typeform', placeholder: 'https://form.typeform.com/to/...' },
      codepen: { icon: '💻', title: 'Fragmento de GitHub / CodePen', placeholder: 'https://codepen.io/... o https://github.com/...' },
      loom: { icon: '📹', title: 'Grabación de Pantalla de Loom', placeholder: 'https://www.loom.com/share/...' }
    };

    function openMediaEmbedModal(type = 'pdf') {
      const modal = document.getElementById('media-embed-modal');
      if (!modal) return;
      selectMediaEmbedType(type);
      const urlInput = document.getElementById('media-embed-url-input');
      const titleInput = document.getElementById('media-embed-title-input');
      if (urlInput) urlInput.value = '';
      if (titleInput) titleInput.value = '';
      modal.classList.add('open');
      setTimeout(() => { if (urlInput) urlInput.focus(); }, 40);
    }

    function closeMediaEmbedModal() {
      const modal = document.getElementById('media-embed-modal');
      if (modal) modal.classList.remove('open');
    }

    function selectMediaEmbedType(type) {
      currentMediaEmbedType = EMBED_TYPE_META[type] ? type : 'pdf';
      const meta = EMBED_TYPE_META[currentMediaEmbedType];
      const iconEl = document.getElementById('media-embed-modal-icon');
      const titleEl = document.getElementById('media-embed-modal-title');
      const urlInput = document.getElementById('media-embed-url-input');
      if (iconEl) iconEl.textContent = meta.icon;
      if (titleEl) titleEl.textContent = meta.title;
      if (urlInput) urlInput.placeholder = meta.placeholder;

      document.querySelectorAll('#embed-provider-chips [data-embed-type]').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-embed-type') === currentMediaEmbedType);
      });
      const fileInput = document.getElementById('media-embed-file-input');
      if (fileInput) fileInput.accept = currentMediaEmbedType === 'pdf' ? 'application/pdf,.pdf' : '';
    }

    async function handleMediaEmbedFileUpload(fileInput) {
      const file = fileInput && fileInput.files && fileInput.files[0];
      if (!file) return;
      if (currentMediaEmbedType === 'pdf') {
        fileInput.disabled = true;
        try {
          const result = await uploadPdfFile(file);
          document.getElementById('media-embed-url-input').value = result.url;
          document.getElementById('media-embed-title-input').value = result.name;
          showToast('PDF importado. Pulsa Insertar para adjuntarlo.', '📑');
        } catch (error) { showToast(error.message, '📑'); }
        finally { fileInput.disabled = false; fileInput.value = ''; }
        return;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        const urlInput = document.getElementById('media-embed-url-input');
        const titleInput = document.getElementById('media-embed-title-input');
        if (urlInput) urlInput.value = e.target.result;
        if (titleInput && !titleInput.value) titleInput.value = file.name;
      };
      reader.readAsDataURL(file);
    }

    function confirmInsertMediaEmbedBlock() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const rawUrl = (document.getElementById('media-embed-url-input')?.value || '').trim();
      const customTitle = (document.getElementById('media-embed-title-input')?.value || '').trim();
      const meta = EMBED_TYPE_META[currentMediaEmbedType] || EMBED_TYPE_META.pdf;
      const displayTitle = customTitle || meta.title;

      const block = document.createElement('div');
      block.className = 'notion-media-embed-block';
      block.setAttribute('contenteditable', 'false');

      let bodyHtml = '';
      if (currentMediaEmbedType === 'pdf') {
        if (!rawUrl || document.getElementById('media-embed-file-input')?.disabled) {
          showToast('Selecciona un PDF y espera a que termine de importar.', '📑');
          return;
        }
        bodyHtml = createPdfEmbedHTML(rawUrl, displayTitle);
        block.classList.add('notion-block', 'block-pdf');
        block.setAttribute('data-type', 'pdf');
        block.setAttribute('data-source', rawUrl);
        block.setAttribute('data-title', displayTitle);
      } else if (currentMediaEmbedType === 'gmaps') {
        const q = encodeURIComponent(rawUrl || 'Puerta del Sol, Madrid');
        bodyHtml = `<iframe src="https://maps.google.com/maps?q=${q}&t=&z=13&ie=UTF8&iwloc=&output=embed" style="width:100%; height:270px; border:none; border-radius:7px;" loading="lazy"></iframe>`;
      } else {
        const safeHref = rawUrl || 'https://notion.so';
        bodyHtml = `
          <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; padding:14px; background:var(--bg-elevated); border-radius:8px;">
            <div style="display:flex; align-items:center; gap:10px; min-width:0;">
              <span style="font-size:24px;">${meta.icon}</span>
              <div style="min-width:0;">
                <div style="font-weight:800; font-size:13px; color:var(--text-primary);">${escapeHtmlAttr(displayTitle)}</div>
                <div style="font-size:11px; color:var(--text-muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">Visor interactivo conectado · ${escapeHtmlAttr(safeHref)}</div>
              </div>
            </div>
            <a href="${escapeHtmlAttr(safeHref)}" target="_blank" rel="noopener noreferrer" class="btn-secondary" style="padding:4px 10px; font-size:11px; text-decoration:none;">↗ Abrir visor</a>
          </div>
        `;
      }

      block.innerHTML = `
        <div class="notion-media-embed-header">
          <span>${meta.icon} ${escapeHtmlAttr(displayTitle)}</span>
          <button type="button" class="btn-icon-tiny btn-danger-tiny" onclick="this.closest('.notion-media-embed-block').remove(); syncRichEditor();" title="Eliminar bloque">🗑</button>
        </div>
        <div class="notion-media-embed-body">${bodyHtml}</div>
      `;

      const pAfter = document.createElement('p');
      pAfter.innerHTML = '<br>';
      editor.appendChild(block);
      editor.appendChild(pAfter);

      closeMediaEmbedModal();
      syncRichEditor();
      block.scrollIntoView({ behavior: 'smooth', block: 'center' });
      showToast(`${meta.title} insertado en la página`, meta.icon);
    }

    // 7. Arquitectura de Bloques Notion, Indexación Fraccionaria y Drag & Drop con Guías Azules
    const BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

    function generateKeyBetween(a, b) {
      if (a && b && a >= b) return a + "V";
      if (!a && !b) return "a0";
      if (!a) {
        let prefix = "";
        for (let i = 0; i < b.length; i++) {
          const char = b[i];
          const idx = BASE62.indexOf(char);
          if (idx > 0) {
            return prefix + BASE62[Math.floor(idx / 2)];
          }
          prefix += char;
        }
        return "0" + (b || "");
      }
      if (!b) {
        const head = a[0] && BASE62.includes(a[0]) ? a[0] : "a";
        const idx = BASE62.indexOf(head);
        if (idx < BASE62.length - 1) {
          return BASE62[Math.floor((idx + BASE62.length) / 2)];
        }
        return a + "V";
      }

      let prefix = "";
      let i = 0;
      while (true) {
        const charA = i < a.length && BASE62.includes(a[i]) ? a[i] : "0";
        const charB = i < b.length && BASE62.includes(b[i]) ? b[i] : "z";
        const idxA = BASE62.indexOf(charA);
        const idxB = BASE62.indexOf(charB);

        if (idxB - idxA > 1) {
          const midIdx = Math.floor((idxA + idxB) / 2);
          return prefix + BASE62[midIdx];
        } else if (idxB - idxA === 1) {
          prefix += charA;
          i++;
          const tailA = i < a.length && BASE62.includes(a[i]) ? a[i] : "0";
          const idxTailA = BASE62.indexOf(tailA);
          if (idxTailA < BASE62.length - 1) {
            return prefix + BASE62[Math.floor((idxTailA + BASE62.length) / 2)];
          } else {
            return prefix + "V";
          }
        } else {
          prefix += charA;
          i++;
          if (i >= a.length && i >= b.length) {
            return prefix + "V";
          }
        }
      }
    }

    async function apiUpdateBlockOrder(blockId, prevId, nextId, parentId, noteId) {
      try {
        if (window.pywebview && window.pywebview.api && window.pywebview.api.update_block_order) {
          return await window.pywebview.api.update_block_order(blockId, prevId, nextId, parentId, noteId);
        }
        const res = await fetch('/api/blocks/order', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ blockId, prevId, nextId, parentId, noteId })
        });
        return await res.json();
      } catch (err) {
        console.warn('Block order update fallback:', err);
        return { ok: false, error: String(err) };
      }
    }

    async function apiUpdateBatchBlocks(moves) {
      try {
        if (window.pywebview && window.pywebview.api && window.pywebview.api.update_batch_blocks_order) {
          return await window.pywebview.api.update_batch_blocks_order(moves);
        }
        const res = await fetch('/api/blocks/batch', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ moves })
        });
        return await res.json();
      } catch (err) {
        console.warn('Batch block update fallback:', err);
        return { ok: false, error: String(err) };
      }
    }

    async function apiSyncNoteBlocks(noteId, blocksData) {
      try {
        if (window.pywebview && window.pywebview.api && window.pywebview.api.sync_note_blocks) {
          return await window.pywebview.api.sync_note_blocks(noteId, blocksData);
        }
        const res = await fetch(`/api/notes/${noteId}/blocks/sync`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ blocks: blocksData })
        });
        return await res.json();
      } catch (err) {
        return { ok: false, error: String(err) };
      }
    }

    function ensureBlockMetadata(blockEl, parentId = null) {
      if (!blockEl) return;
      if (!blockEl.getAttribute('data-block-id')) {
        const uid = 'blk-' + Math.random().toString(36).substring(2, 9) + '-' + Date.now().toString(36);
        blockEl.setAttribute('data-block-id', uid);
      }
      if (!blockEl.getAttribute('data-sort-index')) {
        const prev = blockEl.previousElementSibling;
        const next = blockEl.nextElementSibling;
        const prevIdx = prev?.getAttribute('data-sort-index') || null;
        const nextIdx = next?.getAttribute('data-sort-index') || null;
        blockEl.setAttribute('data-sort-index', generateKeyBetween(prevIdx, nextIdx));
      }
      if (parentId) {
        blockEl.setAttribute('data-parent-id', parentId);
      }
    }

    function tagAllEditorBlocks() {
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      let prevIdx = null;
      Array.from(editor.children).forEach(child => {
        if (!child.getAttribute('data-block-id')) {
          const uid = 'blk-' + Math.random().toString(36).substring(2, 9) + '-' + Date.now().toString(36);
          child.setAttribute('data-block-id', uid);
        }
        if (!child.getAttribute('data-sort-index')) {
          const newIdx = generateKeyBetween(prevIdx, null);
          child.setAttribute('data-sort-index', newIdx);
          prevIdx = newIdx;
        } else {
          prevIdx = child.getAttribute('data-sort-index');
        }
      });
    }

    // Selección en Lote (Multi-selección & Marquee / Lazo)
    const selectedBlockEls = new Set();

    function clearBlockSelection() {
      selectedBlockEls.forEach(el => el.classList.remove('spatial-block-selected'));
      selectedBlockEls.clear();
    }

    function selectBlock(el, addToSelection = false) {
      if (!addToSelection) {
        clearBlockSelection();
      }
      if (el) {
        selectedBlockEls.add(el);
        el.classList.add('spatial-block-selected');
      }
    }

    function toggleBlockInSelection(el) {
      if (!el) return;
      if (selectedBlockEls.has(el)) {
        selectedBlockEls.delete(el);
        el.classList.remove('spatial-block-selected');
      } else {
        selectedBlockEls.add(el);
        el.classList.add('spatial-block-selected');
      }
    }

    function selectBlockRange(targetEl) {
      if (!targetEl) return;
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;
      const allBlocks = Array.from(editor.children);
      if (selectedBlockEls.size === 0) {
        selectBlock(targetEl);
        return;
      }
      const firstSelected = Array.from(selectedBlockEls)[0];
      const idxA = allBlocks.indexOf(firstSelected);
      const idxB = allBlocks.indexOf(targetEl);
      if (idxA === -1 || idxB === -1) {
        selectBlock(targetEl, true);
        return;
      }
      const start = Math.min(idxA, idxB);
      const end = Math.max(idxA, idxB);
      for (let i = start; i <= end; i++) {
        selectBlock(allBlocks[i], true);
      }
    }

    let activeSpatialBlockEl = null;
    let spatialDragState = {
      dragging: false,
      sourceEls: [],
      targetEl: null,
      dropMode: null // 'above' | 'below' | 'indent' | 'left-col' | 'right-col'
    };

    function getSpatialBlockFromEventTarget(target) {
      if (!target) return null;
      const editor = document.getElementById('rich-editor-canvas');
      const blocksContainer = document.getElementById('blocks-container');

      const specialBlock = target.closest('.notion-block[id^="block-"], .notion-block-box[id^="block-"], .callout-box[id^="block-"], .quote-block[id^="block-"], .toggle-block[id^="block-"], .code-block[id^="block-"]');
      if (specialBlock && blocksContainer && blocksContainer.contains(specialBlock)) {
        return specialBlock;
      }

      if (!editor || !editor.contains(target) || target === editor) return null;

      const colSlot = target.closest('.notion-column-slot');
      if (colSlot && editor.contains(colSlot) && target !== colSlot) {
        let node = target;
        while (node && node.parentElement !== colSlot && node !== colSlot) {
          node = node.parentElement;
        }
        if (node && node.parentElement === colSlot) return node;
      }

      let curr = target;
      while (curr && curr.parentElement !== editor && curr !== editor) {
        curr = curr.parentElement;
      }
      if (curr && curr.parentElement === editor) {
        return curr;
      }
      return null;
    }

    function positionSpatialHandleForBlock(blockEl) {
      const handle = document.getElementById('spatial-block-handle');
      if (!handle || !blockEl) return;
      const rect = blockEl.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) {
        handle.classList.remove('visible');
        return;
      }
      activeSpatialBlockEl = blockEl;
      ensureBlockMetadata(blockEl);
      const topPx = Math.max(76, Math.min(window.innerHeight - 40, rect.top + 2));
      const leftPx = Math.max(8, rect.left - 46);
      handle.style.top = `${topPx}px`;
      handle.style.left = `${leftPx}px`;
      handle.classList.add('visible');
    }

    function handleSpatialAddBlockClick(event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;

      const insertAbove = event && Boolean(event.altKey);
      const newP = document.createElement('p');
      newP.innerHTML = '<br>';

      if (activeSpatialBlockEl && editor.contains(activeSpatialBlockEl)) {
        if (insertAbove) {
          activeSpatialBlockEl.before(newP);
        } else {
          activeSpatialBlockEl.after(newP);
        }
      } else {
        editor.appendChild(newP);
      }

      ensureBlockMetadata(newP);

      // Colocar cursor dentro del nuevo bloque y abrir menú Slash
      const range = document.createRange();
      range.selectNodeContents(newP);
      range.collapse(true);
      const sel = window.getSelection();
      if (sel) {
        sel.removeAllRanges();
        sel.addRange(range);
      }
      syncRichEditor();
      openSlashMenu();

      const activeNote = getActiveNote();
      if (activeNote) {
        const prevIdx = newP.previousElementSibling?.getAttribute('data-sort-index') || null;
        const nextIdx = newP.nextElementSibling?.getAttribute('data-sort-index') || null;
        apiUpdateBlockOrder(
          newP.getAttribute('data-block-id'),
          newP.previousElementSibling?.getAttribute('data-block-id'),
          newP.nextElementSibling?.getAttribute('data-block-id'),
          newP.getAttribute('data-parent-id'),
          activeNote.id
        );
      }
    }

    function handleSpatialGripClick(event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }
      if (!activeSpatialBlockEl) return;

      if (event && event.shiftKey) {
        selectBlockRange(activeSpatialBlockEl);
        return;
      }
      if (event && (event.ctrlKey || event.metaKey)) {
        toggleBlockInSelection(activeSpatialBlockEl);
        return;
      }

      openBlockActionMenu(activeSpatialBlockEl);
    }

    let lastAppliedColorStyle = { type: 'bg', value: 'rgba(59, 130, 246, 0.16)' };

    function openBlockActionMenu(blockEl) {
      const menu = document.getElementById('block-action-menu');
      const handle = document.getElementById('spatial-block-handle');
      if (!menu || !blockEl) return;

      if (!selectedBlockEls.has(blockEl)) {
        clearBlockSelection();
        selectBlock(blockEl);
      }

      const handleRect = handle ? handle.getBoundingClientRect() : blockEl.getBoundingClientRect();
      menu.innerHTML = `
        <div class="block-menu-section-label">Manejador de Bloque (${selectedBlockEls.size > 1 ? selectedBlockEls.size + ' seleccionados' : '1 bloque'})</div>
        
        <!-- 1. Convertir en (Turn into) -->
        <div style="font-size:10px; font-weight:800; color:var(--text-muted); padding:3px 8px 1px; text-transform:uppercase;">1. Convertir en (Turn into)</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:2px; padding:2px;">
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-p')">
            <span>¶ Texto</span>
          </button>
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-h1')">
            <span>H1 Título 1</span>
          </button>
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-h2')">
            <span>H2 Título 2</span>
          </button>
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-h3')">
            <span>H3 Título 3</span>
          </button>
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-h4')">
            <span>H4 Título 4</span>
          </button>
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-todo')">
            <span>☑ Tarea To-do</span>
          </button>
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-bullet')">
            <span>• Viñetas</span>
          </button>
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-num')">
            <span>1. Numerada</span>
          </button>
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-toggle')">
            <span>▶ Desplegable</span>
          </button>
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-quote')">
            <span>❝ Cita</span>
          </button>
          <button type="button" class="block-menu-item" style="padding:4px 6px; font-size:11.5px;" onclick="executeBlockMenuAction('turn-callout')">
            <span>💡 Callout</span>
          </button>
        </div>

        <div class="page-appearance-divider"></div>

        <!-- 2. Color (Texto y Fondo) -->
        <div style="font-size:10px; font-weight:800; color:var(--text-muted); padding:3px 8px 1px; text-transform:uppercase;">2. Color del bloque</div>
        <div class="block-menu-color-dots">
          <button type="button" class="block-color-dot" style="background:transparent;" onclick="executeBlockMenuAction('color-reset')" title="Predeterminado">✕</button>
          <button type="button" class="block-color-dot" style="background:rgba(59,130,246,0.3);" onclick="executeBlockMenuAction('bg-blue')" title="Fondo Azul"></button>
          <button type="button" class="block-color-dot" style="background:rgba(245,158,11,0.3);" onclick="executeBlockMenuAction('bg-amber')" title="Fondo Ámbar"></button>
          <button type="button" class="block-color-dot" style="background:rgba(16,185,129,0.3);" onclick="executeBlockMenuAction('bg-green')" title="Fondo Verde"></button>
          <button type="button" class="block-color-dot" style="background:rgba(239,68,68,0.3);" onclick="executeBlockMenuAction('bg-red')" title="Fondo Rojo"></button>
          <button type="button" class="block-color-dot" style="background:rgba(168,85,247,0.3);" onclick="executeBlockMenuAction('bg-purple')" title="Fondo Púrpura"></button>
          <button type="button" class="block-color-dot" style="background:rgba(236,72,153,0.3);" onclick="executeBlockMenuAction('bg-pink')" title="Fondo Rosa"></button>
          <button type="button" class="block-color-dot" style="background:rgba(148,163,184,0.3);" onclick="executeBlockMenuAction('bg-gray')" title="Fondo Gris"></button>
        </div>

        <div class="page-appearance-divider"></div>

        <!-- 3. Duplicar -->
        <button type="button" class="block-menu-item" onclick="executeBlockMenuAction('duplicate')">
          <span>📑 Duplicar bloque (Duplicate)</span>
          <span class="ctx-menu-kbd">Ctrl+D</span>
        </button>

        <!-- 4. Mover a -->
        <button type="button" class="block-menu-item" onclick="executeBlockMenuAction('move-up')">
          <span>⬆️ Mover bloque arriba</span>
          <span class="ctx-menu-kbd">Ctrl+⇧+↑</span>
        </button>
        <button type="button" class="block-menu-item" onclick="executeBlockMenuAction('move-down')">
          <span>⬇️ Mover bloque abajo</span>
          <span class="ctx-menu-kbd">Ctrl+⇧+↓</span>
        </button>
        <button type="button" class="block-menu-item" onclick="executeBlockMenuAction('split-cols')">
          <span>▥ Crear 2 columnas al lado</span>
          <span class="ctx-menu-kbd">/cols</span>
        </button>
        <button type="button" class="block-menu-item" onclick="executeBlockMenuAction('wrap-synced')">
          <span>🔄 Envolver en Bloque Sincronizado</span>
          <span class="ctx-menu-kbd">Halo rojo</span>
        </button>
        ${copiedSyncedBlockBuffer ? `
        <button type="button" class="block-menu-item" onclick="closeBlockActionMenu(); pasteCopiedSyncedBlock();">
          <span>🔗 Pegar referencia sincronizada aquí</span>
        </button>` : ''}

        <!-- 5. Copiar enlace al bloque -->
        <button type="button" class="block-menu-item" onclick="executeBlockMenuAction('copy-anchor')">
          <span>🔗 Copiar enlace al bloque (Anchor URL)</span>
          <span class="ctx-menu-kbd">#block-id</span>
        </button>

        <!-- 7. Comentar / Sugerir -->
        <button type="button" class="block-menu-item" onclick="executeBlockMenuAction('comment')">
          <span>💬 Comentar / Sugerir ediciones</span>
          <span class="ctx-menu-kbd">Ctrl+⇧+M</span>
        </button>

        <div class="page-appearance-divider"></div>

        <!-- 6. Eliminar -->
        <button type="button" class="block-menu-item danger" onclick="executeBlockMenuAction('delete')">
          <span>🗑 Eliminar bloque(s)</span>
          <span class="ctx-menu-kbd">Del</span>
        </button>
      `;

      menu.classList.add('open');
      const menuRect = menu.getBoundingClientRect();
      const left = Math.max(10, Math.min(handleRect.left, window.innerWidth - menuRect.width - 14));
      const top = Math.max(10, Math.min(handleRect.bottom + 6, window.innerHeight - menuRect.height - 14));
      menu.style.left = `${left}px`;
      menu.style.top = `${top}px`;
    }

    function closeBlockActionMenu() {
      const menu = document.getElementById('block-action-menu');
      if (menu) menu.classList.remove('open');
    }

    function transformBlockTag(blockEl, newTagName) {
      if (!blockEl || !blockEl.parentElement) return null;
      const replacement = document.createElement(newTagName);
      replacement.innerHTML = blockEl.innerHTML || blockEl.textContent || '';
      if (blockEl.style.backgroundColor) {
        replacement.style.backgroundColor = blockEl.style.backgroundColor;
        replacement.style.padding = blockEl.style.padding;
        replacement.style.borderRadius = blockEl.style.borderRadius;
      }
      replacement.setAttribute('data-block-id', blockEl.getAttribute('data-block-id') || ('blk-' + Date.now()));
      replacement.setAttribute('data-sort-index', blockEl.getAttribute('data-sort-index') || 'a0');
      blockEl.replaceWith(replacement);
      activeSpatialBlockEl = replacement;
      syncRichEditor();
      return replacement;
    }

    function executeBlockMenuAction(action) {
      const targets = selectedBlockEls.size > 0 ? Array.from(selectedBlockEls) : (activeSpatialBlockEl ? [activeSpatialBlockEl] : []);
      closeBlockActionMenu();
      if (targets.length === 0) return;

      const editor = document.getElementById('rich-editor-canvas');

      targets.forEach(block => {
        const isSpecialBlock = block.id && block.id.startsWith('block-');

        if (action === 'duplicate' && !isSpecialBlock) {
          const clone = block.cloneNode(true);
          clone.classList.remove('spatial-block-selected');
          const newId = 'blk-' + Math.random().toString(36).substring(2, 9) + '-' + Date.now().toString(36);
          clone.setAttribute('data-block-id', newId);
          const nextIdx = block.nextElementSibling?.getAttribute('data-sort-index') || null;
          clone.setAttribute('data-sort-index', generateKeyBetween(block.getAttribute('data-sort-index'), nextIdx));
          block.after(clone);
          showToast('Bloque duplicado (Ctrl+D)', '📑');
        } else if (action === 'delete') {
          if (isSpecialBlock) {
            const key = block.id.replace('block-', '');
            deleteBlock(key);
          } else {
            block.remove();
          }
          showToast('Bloque eliminado', '🗑');
        } else if (action === 'copy-anchor') {
          const id = block.getAttribute('data-block-id') || block.id || ('blk-' + Date.now());
          block.setAttribute('data-block-id', id);
          const anchorUrl = window.location.origin + window.location.pathname + '#' + id;
          if (navigator.clipboard) {
            navigator.clipboard.writeText(anchorUrl);
          }
          showToast(`Enlace al bloque copiado: #${id}`, '🔗');
        } else if (action === 'comment') {
          const commentText = prompt('Escribe un comentario o sugerencia para este bloque:');
          if (commentText) {
            const commentPill = document.createElement('span');
            commentPill.style.display = 'inline-flex';
            commentPill.style.alignItems = 'center';
            commentPill.style.gap = '4px';
            commentPill.style.fontSize = '11px';
            commentPill.style.background = 'rgba(245, 158, 11, 0.18)';
            commentPill.style.color = '#f59e0b';
            commentPill.style.border = '1px solid rgba(245, 158, 11, 0.35)';
            commentPill.style.padding = '1px 6px';
            commentPill.style.borderRadius = '4px';
            commentPill.style.marginLeft = '8px';
            commentPill.contentEditable = 'false';
            commentPill.innerHTML = `💬 ${escapeHtmlAttr(commentText)} <button type="button" onclick="this.parentElement.remove(); syncRichEditor();" style="border:none; background:transparent; color:#f59e0b; cursor:pointer; font-size:10px; padding:0 2px;">✕</button>`;
            block.appendChild(commentPill);
            showToast('Comentario añadido al bloque', '💬');
          }
        } else if (action.startsWith('turn-') && !isSpecialBlock) {
          const bId = block.getAttribute('data-block-id');
          if (bId && typeof convertBlockType === 'function') {
            convertBlockType(bId, action);
          } else if (action === 'turn-h4') {
            transformBlockTag(block, 'h4');
          } else if (action === 'turn-todo') {
            const wrap = document.createElement('div');
            wrap.className = 'notion-todo-item';
            wrap.innerHTML = `<input type="checkbox" onchange="syncRichEditor()"> <span contenteditable="true">${block.innerHTML || 'Nueva tarea'}</span>`;
            wrap.setAttribute('data-block-id', block.getAttribute('data-block-id') || ('blk-' + Date.now()));
            block.replaceWith(wrap);
          } else if (action === 'turn-bullet') {
            const ul = document.createElement('ul');
            ul.innerHTML = `<li>${block.innerHTML || 'Elemento con viñeta'}</li>`;
            ul.setAttribute('data-block-id', block.getAttribute('data-block-id') || ('blk-' + Date.now()));
            block.replaceWith(ul);
          } else if (action === 'turn-num') {
            const ol = document.createElement('ol');
            ol.innerHTML = `<li>${block.innerHTML || 'Elemento numerado'}</li>`;
            ol.setAttribute('data-block-id', block.getAttribute('data-block-id') || ('blk-' + Date.now()));
            block.replaceWith(ol);
          } else if (action === 'turn-toggle') {
            const details = document.createElement('details');
            details.className = 'notion-inline-toggle';
            details.open = true;
            details.innerHTML = `<summary style="cursor:pointer; font-weight:700;">${block.textContent || 'Título desplegable'}</summary><div class="notion-inline-toggle-content" style="padding-left:18px; margin-top:6px;"><p><br></p></div>`;
            details.setAttribute('data-block-id', block.getAttribute('data-block-id') || ('blk-' + Date.now()));
            block.replaceWith(details);
          } else if (action === 'turn-callout') {
            const callout = document.createElement('div');
            callout.className = 'notion-inline-callout';
            callout.style.background = 'rgba(245, 158, 11, 0.08)';
            callout.style.border = '1px solid rgba(245, 158, 11, 0.28)';
            callout.style.borderRadius = '8px';
            callout.style.padding = '12px';
            callout.style.margin = '8px 0';
            callout.style.display = 'flex';
            callout.style.gap = '10px';
            callout.innerHTML = `<span style="font-size:20px;">💡</span><div contenteditable="true" style="flex:1;">${block.innerHTML || 'Contenido destacado...'}</div>`;
            callout.setAttribute('data-block-id', block.getAttribute('data-block-id') || ('blk-' + Date.now()));
            block.replaceWith(callout);
          } else {
            const map = { 'turn-p': 'p', 'turn-h1': 'h1', 'turn-h2': 'h2', 'turn-h3': 'h3', 'turn-h4': 'h4', 'turn-quote': 'blockquote' };
            const tag = map[action] || 'p';
            transformBlockTag(block, tag);
          }
          showToast('Bloque transformado', '🔄');
        } else if (action === 'color-reset') {
          block.style.backgroundColor = '';
          block.style.color = '';
          block.style.padding = '';
          block.style.borderRadius = '';
          lastAppliedColorStyle = { type: 'reset' };
          showToast('Color restablecido', '✕');
        } else if (action.startsWith('bg-')) {
          const bgMap = {
            'bg-blue': 'rgba(59, 130, 246, 0.16)',
            'bg-amber': 'rgba(245, 158, 11, 0.16)',
            'bg-green': 'rgba(16, 185, 129, 0.16)',
            'bg-red': 'rgba(239, 68, 68, 0.16)',
            'bg-purple': 'rgba(168, 85, 247, 0.16)',
            'bg-pink': 'rgba(236, 72, 153, 0.16)',
            'bg-gray': 'rgba(148, 163, 184, 0.16)'
          };
          const val = bgMap[action] || '';
          block.style.backgroundColor = val;
          block.style.padding = val ? '8px 12px' : '';
          block.style.borderRadius = val ? '7px' : '';
          lastAppliedColorStyle = { type: 'bg', value: val };
          showToast('Fondo aplicado al bloque', '🎨');
        } else if (action === 'move-up') {
          if (block.previousElementSibling) {
            block.previousElementSibling.before(block);
          }
        } else if (action === 'move-down') {
          if (block.nextElementSibling) {
            block.nextElementSibling.after(block);
          }
        }
      });

      clearBlockSelection();
      syncRichEditor();
    }

    function combineBlocksIntoSideBySideColumns(sourceElements, targetEl, placeLeft) {
      if (!sourceElements || sourceElements.length === 0 || !targetEl) return;
      const validSources = sourceElements.filter(el => el !== targetEl && !el.contains(targetEl));
      if (validSources.length === 0) return;

      validSources.forEach(el => el.classList.remove('spatial-block-selected'));

      const existingRow = targetEl.classList.contains('notion-columns-row')
        ? targetEl
        : targetEl.closest('.notion-columns-row');

      if (existingRow) {
        const newSlot = createColumnSlotElement('');
        validSources.forEach(el => newSlot.appendChild(el));
        const resizer = createColumnResizerElement();
        if (placeLeft) {
          existingRow.prepend(resizer);
          existingRow.prepend(newSlot);
        } else {
          existingRow.appendChild(resizer);
          existingRow.appendChild(newSlot);
        }
        const slots = existingRow.querySelectorAll(':scope > .notion-column-slot');
        const share = (100 / Math.max(1, slots.length)).toFixed(2);
        slots.forEach(s => { s.style.flex = `1 1 ${share}%`; });
        attachColumnResizerListeners();
        syncRichEditor();
        showToast('Columna paralela añadida a la fila', '▥');
        return;
      }

      const row = document.createElement('div');
      row.className = 'notion-columns-row';
      row.setAttribute('data-columns-count', '2');

      const slotA = createColumnSlotElement('');
      const slotB = createColumnSlotElement('');
      const resizer = createColumnResizerElement();

      targetEl.replaceWith(row);
      if (placeLeft) {
        validSources.forEach(el => slotA.appendChild(el));
        slotB.appendChild(targetEl);
      } else {
        slotA.appendChild(targetEl);
        validSources.forEach(el => slotB.appendChild(el));
      }
      row.appendChild(slotA);
      row.appendChild(resizer);
      row.appendChild(slotB);

      attachColumnResizerListeners();
      syncRichEditor();
      showToast('2 columnas creadas mediante guía vertical azul', '▥');
    }

    function nestBlocksInsideTarget(sourceElements, targetEl) {
      if (!sourceElements || sourceElements.length === 0 || !targetEl) return;
      const validSources = sourceElements.filter(el => el !== targetEl && !el.contains(targetEl));
      if (validSources.length === 0) return;

      validSources.forEach(el => el.classList.remove('spatial-block-selected'));

      const toggleBody = targetEl.querySelector?.('.notion-inline-toggle-content');
      const calloutBody = targetEl.querySelector?.('.notion-inline-callout-body');
      const syncedBody = targetEl.querySelector?.('.notion-synced-body');
      const targetBlockId = targetEl.getAttribute('data-block-id') || targetEl.id || null;

      validSources.forEach(sourceEl => {
        sourceEl.setAttribute('data-parent-id', targetBlockId || '');
        if (toggleBody) {
          targetEl.open = true;
          toggleBody.appendChild(sourceEl);
        } else if (calloutBody) {
          calloutBody.appendChild(sourceEl);
        } else if (syncedBody) {
          syncedBody.appendChild(sourceEl);
        } else {
          sourceEl.style.marginLeft = '28px';
          sourceEl.style.borderLeft = '2px solid rgba(59, 130, 246, 0.35)';
          sourceEl.style.paddingLeft = '10px';
          targetEl.after(sourceEl);
        }
      });

      syncRichEditor();
      showToast(validSources.length > 1 ? `${validSources.length} bloques anidados` : 'Bloque anidado', '↳');
    }

    function reorderBlocksWithFractionalIndexing(blocksToMove, targetEl, dropMode) {
      if (!blocksToMove || blocksToMove.length === 0 || !targetEl) return;
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;

      // Ordenar por su posición DOM original para preservar la secuencia exacta
      blocksToMove.sort((a, b) => (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1));

      // Limpiar estilos de anidamiento si se mueven a nivel raíz
      blocksToMove.forEach(b => {
        b.style.marginLeft = '';
        b.style.borderLeft = '';
        b.style.paddingLeft = '';
        b.removeAttribute('data-parent-id');
      });

      if (dropMode === 'above') {
        // Insertar justo antes de targetEl
        blocksToMove.forEach(b => targetEl.before(b));
      } else if (dropMode === 'below') {
        // Insertar justo después de targetEl preservando orden
        let anchor = targetEl;
        blocksToMove.forEach(b => {
          anchor.after(b);
          anchor = b;
        });
      }

      // Calcular nuevos índices fraccionarios secuenciales O(1)
      const firstMoved = blocksToMove[0];
      const lastMoved = blocksToMove[blocksToMove.length - 1];
      const prevBoundary = firstMoved.previousElementSibling?.getAttribute('data-sort-index') || null;
      const nextBoundary = lastMoved.nextElementSibling?.getAttribute('data-sort-index') || null;

      let currentPrev = prevBoundary;
      const moves = [];
      const activeNote = getActiveNote();
      const noteId = activeNote ? activeNote.id : 0;

      blocksToMove.forEach((block, idx) => {
        // Clave estrictamente mayor que currentPrev y menor que nextBoundary
        const newKey = generateKeyBetween(currentPrev, nextBoundary);
        block.setAttribute('data-sort-index', newKey);
        currentPrev = newKey;
        moves.push({
          id: block.getAttribute('data-block-id'),
          sortIndex: newKey,
          parentId: block.getAttribute('data-parent-id') || null,
          noteId: noteId,
          type: block.tagName.toLowerCase()
        });
      });

      syncRichEditor();
      if (moves.length === 1) {
        apiUpdateBlockOrder(moves[0].id, prevBoundary, nextBoundary, moves[0].parentId, noteId);
      } else {
        apiUpdateBatchBlocks(moves);
      }

      if (typeof syncRecordMapChildrenOrder === 'function') {
        const container = (blocksToMove[0] && blocksToMove[0].parentElement) || editor;
        syncRecordMapChildrenOrder(container);
      }
    }

    function initSpatialBlockController() {
      const panelCanvas = document.getElementById('panel-canvas');
      const handle = document.getElementById('spatial-block-handle');
      const gripBtn = document.getElementById('spatial-btn-grip');
      const dropGuide = document.getElementById('spatial-drop-guide');
      const ghostPill = document.getElementById('spatial-drag-ghost-pill');
      const marquee = document.getElementById('block-selection-marquee');
      if (!panelCanvas || !handle || !gripBtn || !dropGuide) return;

      // Mostrar el controlador ⋮⋮ dinámicamente al pasar el cursor sobre cualquier bloque del lienzo
      panelCanvas.addEventListener('mousemove', (e) => {
        if (spatialDragState.dragging) return;
        if (handle.contains(e.target) || e.target.closest('#block-action-menu')) return;
        const block = getSpatialBlockFromEventTarget(e.target);
        if (block) {
          positionSpatialHandleForBlock(block);
        } else if (!e.target.closest('#spatial-block-handle')) {
          handle.classList.remove('visible');
        }
      });

      // Selección por Lazo (Marquee) en el espacio en blanco del lienzo
      let isMarqueeActive = false;
      let marqueeStartX = 0;
      let marqueeStartY = 0;

      panelCanvas.addEventListener('mousedown', (e) => {
        // Abortar de inmediato si ocurre dentro de un elemento editable (texto nativo, input, textarea)
        if (e.target.closest('[contenteditable="true"]') || e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        // Solo botón principal y fuera de bloques editables o controles
        if (e.button !== 0) return;
        if (e.target.closest('#spatial-block-handle') || e.target.closest('#block-action-menu') || e.target.closest('.desktop-format-bar') || e.target.closest('button') || e.target.closest('#sticky-toc-rail')) {
          return;
        }

        // Asegurar que lasso selection solo se active si e.target es panelCanvas o dentro del fondo vacío de .editor-container o márgenes exteriores
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

      // Iniciar arrastre espacial desde el icono de 6 puntos (⋮⋮)
      gripBtn.addEventListener('mousedown', (e) => {
        if (e.button !== 0 || !activeSpatialBlockEl) return;
        const startX = e.clientX;
        const startY = e.clientY;
        const sourceBlock = activeSpatialBlockEl;

        // Si el bloque clickeado ya forma parte de un lote seleccionado, arrastrar todo el lote
        let elementsToDrag = [];
        if (selectedBlockEls.has(sourceBlock) && selectedBlockEls.size > 1) {
          elementsToDrag = Array.from(selectedBlockEls);
        } else {
          clearBlockSelection();
          selectBlock(sourceBlock);
          elementsToDrag = [sourceBlock];
        }

        const onMouseMove = (moveEvt) => {
          const dist = Math.hypot(moveEvt.clientX - startX, moveEvt.clientY - startY);
          if (!spatialDragState.dragging && dist > 5) {
            spatialDragState.dragging = true;
            spatialDragState.sourceEls = elementsToDrag;
            closeBlockActionMenu();
            elementsToDrag.forEach(el => el.classList.add('spatial-block-selected'));

            if (ghostPill) {
              ghostPill.classList.add('visible');
              ghostPill.innerHTML = elementsToDrag.length > 1
                ? `<svg viewBox="0 0 10 16" width="11" height="15" fill="currentColor"><circle cx="2.5" cy="2.5" r="1.4"/><circle cx="7.5" cy="2.5" r="1.4"/><circle cx="2.5" cy="8" r="1.4"/><circle cx="7.5" cy="8" r="1.4"/><circle cx="2.5" cy="13.5" r="1.4"/><circle cx="7.5" cy="13.5" r="1.4"/></svg> <span>Moviendo ${elementsToDrag.length} bloques</span>`
                : `<svg viewBox="0 0 10 16" width="11" height="15" fill="currentColor"><circle cx="2.5" cy="2.5" r="1.4"/><circle cx="7.5" cy="2.5" r="1.4"/><circle cx="2.5" cy="8" r="1.4"/><circle cx="7.5" cy="8" r="1.4"/><circle cx="2.5" cy="13.5" r="1.4"/><circle cx="7.5" cy="13.5" r="1.4"/></svg> <span>Mover bloque</span>`;
            }
          }
          if (!spatialDragState.dragging) return;

          if (ghostPill) {
            ghostPill.style.left = `${moveEvt.clientX}px`;
            ghostPill.style.top = `${moveEvt.clientY}px`;
          }

          const elemBelow = document.elementFromPoint(moveEvt.clientX, moveEvt.clientY);
          const candidate = getSpatialBlockFromEventTarget(elemBelow);
          if (!candidate || elementsToDrag.includes(candidate) || elementsToDrag.some(el => el.contains(candidate))) {
            dropGuide.classList.remove('visible', 'guide-vertical', 'guide-indented');
            spatialDragState.targetEl = null;
            return;
          }

          const rect = candidate.getBoundingClientRect();
          const relX = moveEvt.clientX - rect.left;
          const relY = moveEvt.clientY - rect.top;
          const edgeThreshold = Math.min(68, rect.width * 0.16);
          const indentZoneStart = edgeThreshold + 12;
          const indentZoneEnd = Math.min(rect.width * 0.42, 220);

          spatialDragState.targetEl = candidate;
          dropGuide.classList.add('visible');
          dropGuide.classList.remove('guide-vertical', 'guide-indented');

          const isSpecial = (candidate.id && candidate.id.startsWith('block-'));

          // 1. Zonas laterales izquierda/derecha -> Guía Vertical Azul para dividir pantalla y crear columna
          if (!isSpecial && relX <= edgeThreshold) {
            spatialDragState.dropMode = 'left-col';
            dropGuide.classList.add('guide-vertical');
            dropGuide.style.left = `${rect.left - 3}px`;
            dropGuide.style.top = `${rect.top}px`;
            dropGuide.style.width = '4px';
            dropGuide.style.height = `${rect.height}px`;
          } else if (!isSpecial && relX >= rect.width - edgeThreshold) {
            spatialDragState.dropMode = 'right-col';
            dropGuide.classList.add('guide-vertical');
            dropGuide.style.left = `${rect.right - 1}px`;
            dropGuide.style.top = `${rect.top}px`;
            dropGuide.style.width = '4px';
            dropGuide.style.height = `${rect.height}px`;
          } else if (!isSpecial && relY >= rect.height * 0.5 && relX >= indentZoneStart && relX <= indentZoneEnd) {
            // 2. Zona inferior indentada -> Guía Horizontal Más Corta (Indentada) para anidar bloque dentro de otro
            spatialDragState.dropMode = 'indent';
            dropGuide.classList.add('guide-indented');
            dropGuide.style.left = `${rect.left + 32}px`;
            dropGuide.style.top = `${rect.bottom - 1}px`;
            dropGuide.style.width = `${Math.max(80, rect.width - 32)}px`;
            dropGuide.style.height = '3px';
          } else if (relY < rect.height / 2) {
            // 3. Guía Horizontal Completa Superior
            spatialDragState.dropMode = 'above';
            dropGuide.style.left = `${rect.left}px`;
            dropGuide.style.top = `${rect.top - 2}px`;
            dropGuide.style.width = `${rect.width}px`;
            dropGuide.style.height = '3px';
          } else {
            // 4. Guía Horizontal Completa Inferior
            spatialDragState.dropMode = 'below';
            dropGuide.style.left = `${rect.left}px`;
            dropGuide.style.top = `${rect.bottom - 1}px`;
            dropGuide.style.width = `${rect.width}px`;
            dropGuide.style.height = '3px';
          }
        };

        const onMouseUp = () => {
          window.removeEventListener('mousemove', onMouseMove);
          window.removeEventListener('mouseup', onMouseUp);

          if (ghostPill) ghostPill.classList.remove('visible');

          if (!spatialDragState.dragging) return;
          dropGuide.classList.remove('visible', 'guide-vertical', 'guide-indented');

          const { sourceEls, targetEl, dropMode } = spatialDragState;
          spatialDragState.dragging = false;
          spatialDragState.sourceEls = [];
          spatialDragState.targetEl = null;

          if (sourceEls && sourceEls.length > 0 && targetEl && !sourceEls.includes(targetEl)) {
            if (dropMode === 'left-col') {
              combineBlocksIntoSideBySideColumns(sourceEls, targetEl, true);
            } else if (dropMode === 'right-col') {
              combineBlocksIntoSideBySideColumns(sourceEls, targetEl, false);
            } else if (dropMode === 'indent') {
              nestBlocksInsideTarget(sourceEls, targetEl);
            } else if (dropMode === 'above' || dropMode === 'below') {
              reorderBlocksWithFractionalIndexing(sourceEls, targetEl, dropMode);
            }
          }
        };

        window.addEventListener('mousemove', onMouseMove);
        window.addEventListener('mouseup', onMouseUp);
      });
    }

    // 8. Navegación Estructural de Bloques por Teclado (Esc, Flechas, Ctrl+Shift+Flechas, Ctrl+D) y Buscador Universal (Ctrl+P / Ctrl+K)
    let universalSearchIndex = 0;
    let universalSearchMatches = [];

    function openUniversalSearchModal() {
      const modal = document.getElementById('universal-search-modal');
      const input = document.getElementById('universal-search-input');
      if (!modal || !input) return;
      modal.classList.add('open');
      input.value = '';
      universalSearchIndex = 0;
      renderUniversalSearchResults('');
      setTimeout(() => input.focus(), 40);
    }

    function closeUniversalSearchModal() {
      const modal = document.getElementById('universal-search-modal');
      if (modal) modal.classList.remove('open');
    }

    function openQuickFindModal() {
      openUniversalSearchModal();
    }

    function closeQuickFindModal() {
      closeUniversalSearchModal();
    }

    window.openQuickFindModal = openQuickFindModal;
    window.closeQuickFindModal = closeQuickFindModal;

    function renderUniversalSearchResults(query) {
      const container = document.getElementById('universal-search-results');
      if (!container) return;
      const q = (query || '').toLowerCase().trim();
      const items = [];

      // 1. Notas activas del espacio de trabajo
      getActiveNotesList().forEach(n => {
        const title = n.title || 'Sin título';
        const folder = getNotePrimaryDisplayFolder(n);
        const foldersText = getNoteFolders(n).join(' ');
        const tagsText = n.tags || '';
        if (!q || title.toLowerCase().includes(q) || foldersText.toLowerCase().includes(q) || tagsText.toLowerCase().includes(q) || (n.content || '').toLowerCase().includes(q)) {
          items.push({
            type: 'note',
            icon: n.emoji || '📝',
            title: title,
            meta: `Nota · ${folder}`,
            action: () => { closeUniversalSearchModal(); selectNote(n.id); }
          });
        }
      });

      // 2. Carpetas y Carpetas Inteligentes
      (state.folders || []).forEach(folderName => {
        const isSmart = isSmartFolder(folderName);
        const displayName = getFolderDisplayName(folderName);
        if (!q || folderName.toLowerCase().includes(q) || displayName.toLowerCase().includes(q)) {
          const count = getActiveNotesList().filter(n => noteBelongsToFolder(n, folderName)).length;
          items.push({
            type: 'folder',
            icon: getFolderEmoji(folderName),
            title: folderName,
            meta: isSmart ? `Carpeta Inteligente ⚙️ (${count} notas)` : `Carpeta (${count} notas)`,
            action: () => {
              closeUniversalSearchModal();
              if (state.isHomeActive) {
                exitHomeView();
              }
              selectFolder(folderName);
            }
          });
        }
      });

      // 3. Encabezados H1-H3 de la nota activa
      const headings = collectEditorHeadings();
      headings.forEach(h => {
        if (!q || h.text.toLowerCase().includes(q)) {
          items.push({
            type: 'heading',
            icon: `H${h.level}`,
            title: h.text,
            meta: 'Ir a sección en la nota activa',
            action: () => { closeUniversalSearchModal(); scrollToHeadingByIndex(h.idx); }
          });
        }
      });

      // 4. Acciones espaciales y las 5 categorías de bloques
      const quickCommands = [
        { icon: '▥', title: 'Insertar 2 Columnas Paralelas (/columns)', meta: '5. Bloques Avanzados', fn: () => insertColumnsBlock(2) },
        { icon: '▤', title: 'Insertar 3 Columnas Paralelas (/3cols)', meta: '5. Bloques Avanzados', fn: () => insertColumnsBlock(3) },
        { icon: '📑', title: 'Insertar Índice de Contenido (/toc)', meta: '5. Bloques Avanzados', fn: () => insertTableOfContentsBlock() },
        { icon: '🔄', title: 'Crear Bloque Sincronizado (/synced)', meta: '5. Bloques Avanzados', fn: () => insertSyncedBlock() },
        { icon: '⚡', title: 'Configurar Botón de Automatización (/button)', meta: '5. Bloques Avanzados', fn: () => openMacroButtonModal() },
        { icon: '🧭', title: 'Insertar Menú de Migas de Pan (/breadcrumbs)', meta: '5. Bloques Avanzados', fn: () => insertBreadcrumbsBlock() },
        { icon: '⊞', title: 'Insertar Tabla Simple Estática (/simple)', meta: '1. Bloques Básicos', fn: () => insertSimpleTableBlock() },
        { icon: '💡', title: 'Insertar Caja de Llamada (/callout)', meta: '1. Bloques Básicos', fn: () => insertInlineCalloutElement() },
        { icon: '🖼️', title: 'Abrir Base de Datos en Vista Galería (/gallery)', meta: '3. Bases de Datos', fn: () => openDatabaseWithView('gallery') },
        { icon: '⏳', title: 'Abrir Base de Datos en Vista Cronograma (/timeline)', meta: '3. Bases de Datos', fn: () => openDatabaseWithView('timeline') },
        { icon: '📑', title: 'Incrustar Archivo PDF o App Externa (/embed)', meta: '2 y 4. Medios y Embeds', fn: () => openMediaEmbedModal('pdf') },
        { icon: '📖', title: 'Abrir Catálogo de 48 Bloques (/catalog)', meta: 'Catálogo de Bloques', fn: () => toggleBlockCatalog(true) },
        { icon: '🔍', title: 'Ver Anatomía Universal del Bloque (Panel 1)', meta: 'Anatomía y Atajos', fn: () => openBlockAnatomyModal() },
        { icon: '↔️', title: 'Alternar Ancho Completo de Página (Full width)', meta: 'Diseño de página', fn: () => togglePageFullWidth() },
        { icon: '🔡', title: 'Alternar Texto Pequeño (Small text)', meta: 'Diseño de página', fn: () => togglePageSmallText() }
      ];
      quickCommands.forEach(cmd => {
        if (!q || cmd.title.toLowerCase().includes(q) || cmd.meta.toLowerCase().includes(q)) {
          items.push({
            type: 'cmd',
            icon: cmd.icon,
            title: cmd.title,
            meta: cmd.meta,
            action: () => { closeUniversalSearchModal(); cmd.fn(); }
          });
        }
      });

      universalSearchMatches = items.slice(0, 20);
      if (universalSearchIndex >= universalSearchMatches.length) universalSearchIndex = 0;

      if (universalSearchMatches.length === 0) {
        container.innerHTML = `<div style="padding:20px; text-align:center; color:var(--text-muted); font-size:12.5px;">No se encontraron notas, secciones ni comandos para "${escapeHtmlAttr(query)}"</div>`;
        return;
      }

      container.innerHTML = universalSearchMatches.map((item, i) => `
        <div class="universal-search-item ${i === universalSearchIndex ? 'active' : ''}" onclick="executeUniversalSearchItem(${i})">
          <div style="display:flex; align-items:center; gap:10px; min-width:0;">
            <span style="font-weight:800; font-size:14px; width:24px; text-align:center;">${item.icon}</span>
            <span style="font-size:13px; font-weight:600; color:var(--text-primary); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${escapeHtmlAttr(item.title)}</span>
          </div>
          <span style="font-size:11px; color:var(--text-muted); flex-shrink:0;">${escapeHtmlAttr(item.meta)}</span>
        </div>
      `).join('');
    }

    function executeUniversalSearchItem(idx) {
      const item = universalSearchMatches[idx];
      if (item && typeof item.action === 'function') {
        item.action();
      }
    }

    function handleUniversalSearchKeydown(e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (universalSearchMatches.length > 0) {
          universalSearchIndex = (universalSearchIndex + 1) % universalSearchMatches.length;
          renderUniversalSearchResults(e.target.value);
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (universalSearchMatches.length > 0) {
          universalSearchIndex = (universalSearchIndex - 1 + universalSearchMatches.length) % universalSearchMatches.length;
          renderUniversalSearchResults(e.target.value);
        }
      } else if (e.key === 'Enter') {
        e.preventDefault();
        executeUniversalSearchItem(universalSearchIndex);
      } else if (e.key === 'Escape') {
        e.preventDefault();
        closeUniversalSearchModal();
      }
    }

    function initStructuralKeyboardShortcuts() {
      window.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && !e.shiftKey && (e.key.toLowerCase() === 'p' || e.key.toLowerCase() === 'k')) {
          const sel = window.getSelection();
          if (e.key.toLowerCase() === 'p' || !sel || sel.isCollapsed) {
            e.preventDefault();
            openUniversalSearchModal();
            return;
          }
        }

        if (e.key === 'Escape') {
          const searchModal = document.getElementById('universal-search-modal');
          if (searchModal && searchModal.classList.contains('open')) {
            closeUniversalSearchModal();
            return;
          }
          const macroModal = document.getElementById('macro-button-modal');
          if (macroModal && macroModal.classList.contains('open')) {
            closeMacroButtonModal();
            return;
          }
          const mediaModal = document.getElementById('media-embed-modal');
          if (mediaModal && mediaModal.classList.contains('open')) {
            closeMediaEmbedModal();
            return;
          }
          closePageAppearancePopover();
          closeBlockActionMenu();

          const editor = document.getElementById('rich-editor-canvas');
          const sel = window.getSelection();
          if (editor && sel && sel.rangeCount > 0 && editor.contains(sel.anchorNode)) {
            const block = getSpatialBlockFromEventTarget(sel.anchorNode.nodeType === 3 ? sel.anchorNode.parentElement : sel.anchorNode);
            if (block) {
              e.preventDefault();
              document.querySelectorAll('.spatial-block-selected').forEach(el => el.classList.remove('spatial-block-selected'));
              block.classList.add('spatial-block-selected');
              activeSpatialBlockEl = block;
              editor.blur();
              showToast('Bloque seleccionado (Usa ↑/↓, Ctrl+Shift+↑/↓, Ctrl+D o Supr)', '🟦');
              return;
            }
          } else {
            document.querySelectorAll('.spatial-block-selected').forEach(el => el.classList.remove('spatial-block-selected'));
          }
        }

        const selectedBlock = document.querySelector('.spatial-block-selected');
        if (selectedBlock && document.activeElement !== document.getElementById('rich-editor-canvas')) {
          if (e.key === 'ArrowUp' && !e.ctrlKey && !e.metaKey) {
            const prev = selectedBlock.previousElementSibling;
            if (prev) {
              e.preventDefault();
              selectedBlock.classList.remove('spatial-block-selected');
              prev.classList.add('spatial-block-selected');
              activeSpatialBlockEl = prev;
              prev.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
            return;
          }
          if (e.key === 'ArrowDown' && !e.ctrlKey && !e.metaKey) {
            const next = selectedBlock.nextElementSibling;
            if (next) {
              e.preventDefault();
              selectedBlock.classList.remove('spatial-block-selected');
              next.classList.add('spatial-block-selected');
              activeSpatialBlockEl = next;
              next.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
            return;
          }
          if (e.key === 'Enter') {
            e.preventDefault();
            selectedBlock.classList.remove('spatial-block-selected');
            const editor = document.getElementById('rich-editor-canvas');
            if (editor) {
              editor.focus();
              const range = document.createRange();
              range.selectNodeContents(selectedBlock);
              range.collapse(false);
              const sel = window.getSelection();
              if (sel) {
                sel.removeAllRanges();
                sel.addRange(range);
              }
            }
            return;
          }
          if (e.key === 'Delete' || e.key === 'Backspace') {
            e.preventDefault();
            activeSpatialBlockEl = selectedBlock;
            executeBlockMenuAction('delete');
            return;
          }
        }

        if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) {
          const target = selectedBlock || activeSpatialBlockEl;
          if (target) {
            e.preventDefault();
            activeSpatialBlockEl = target;
            executeBlockMenuAction(e.key === 'ArrowUp' ? 'move-up' : 'move-down');
            target.classList.add('spatial-block-selected');
            return;
          }
        }

        if ((e.ctrlKey || e.metaKey) && e.shiftKey && ['0', '1', '2', '3'].includes(e.key)) {
          const sel = window.getSelection();
          const editor = document.getElementById('rich-editor-canvas');
          const fromCaret = (editor && sel && sel.rangeCount > 0 && editor.contains(sel.anchorNode))
            ? getSpatialBlockFromEventTarget(sel.anchorNode.nodeType === 3 ? sel.anchorNode.parentElement : sel.anchorNode)
            : null;
          const target = fromCaret || selectedBlock || activeSpatialBlockEl;
          if (target) {
            e.preventDefault();
            activeSpatialBlockEl = target;
            const actionMap = { '0': 'turn-p', '1': 'turn-h1', '2': 'turn-h2', '3': 'turn-h3' };
            executeBlockMenuAction(actionMap[e.key]);
            return;
          }
        }

        // Atajo Alt+B: Abrir / Cerrar Catálogo de Bloques Notion
        if (e.altKey && (e.key === 'b' || e.key === 'B')) {
          e.preventDefault();
          toggleBlockCatalog();
          return;
        }

        // Atajo Cmd/Ctrl + / : Abrir Menú de Bloque o Inspector de Anatomía Universal
        if ((e.ctrlKey || e.metaKey) && (e.key === '/' || e.key === '¿')) {
          e.preventDefault();
          const target = selectedBlock || activeSpatialBlockEl || getSpatialBlockFromEventTarget(document.activeElement);
          if (target) {
            openBlockActionMenu(target);
          } else {
            openBlockAnatomyModal();
          }
          return;
        }

        // Atajo Cmd/Ctrl + Shift + H: Aplicar automáticamente el último color utilizado
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'h' || e.key === 'H')) {
          e.preventDefault();
          const target = selectedBlock || activeSpatialBlockEl;
          if (target) {
            applyLastColorToBlock(target);
          }
          return;
        }

        // Tecla Escape: Cerrar modales abiertos
        if (e.key === 'Escape') {
          const catalog = document.getElementById('panel-block-catalog');
          if (catalog && catalog.classList.contains('open')) {
            toggleBlockCatalog(false);
            return;
          }
          const anatomyModal = document.getElementById('modal-block-anatomy');
          if (anatomyModal && anatomyModal.classList.contains('open')) {
            closeBlockAnatomyModal();
            return;
          }
        }
      });

      document.addEventListener('mousedown', (e) => {
        if (!e.target.closest('#page-appearance-popover') && !e.target.closest('#btn-page-appearance')) {
          closePageAppearancePopover();
        }
        if (!e.target.closest('#block-action-menu') && !e.target.closest('#spatial-block-handle')) {
          closeBlockActionMenu();
        }
        if (e.target.closest('#rich-editor-canvas')) {
          document.querySelectorAll('.spatial-block-selected').forEach(el => el.classList.remove('spatial-block-selected'));
        }
      });
    }

    /* ==========================================================================
       14. CATÁLOGO COMPLETO DE BLOQUES NOTION (48 Bloques · 7 Familias · 30 API)
       ========================================================================== */
    const NOTION_API_ENUM_TYPES = [
      'bookmark', 'breadcrumb', 'bulleted_list_item', 'callout', 'child_database',
      'child_page', 'column', 'column_list', 'divider', 'embed',
      'equation', 'file', 'heading_1', 'heading_2', 'heading_3',
      'heading_4', 'image', 'link_preview', 'numbered_list_item', 'paragraph',
      'pdf', 'quote', 'synced_block', 'table', 'table_of_contents',
      'table_row', 'template', 'to_do', 'toggle', 'transcription',
      'unsupported'
    ];

    const NOTION_BLOCK_CATALOG = [
      // 1. Básicos (14)
      { id: 'text', name: 'Texto', enName: 'Text', family: 'basicos', familyName: 'Básicos', icon: '¶', desc: 'Párrafo de texto plano estándar con soporte para estilos enriquecidos, colores de fondo y organización en columnas.', cmd: '/texto · /sin formato', shortcut: 'Cmd/Ctrl+Alt+0', api: 'paragraph' },
      { id: 'heading_1', name: 'Encabezado 1', enName: 'Heading 1', family: 'basicos', familyName: 'Básicos', icon: 'H1', desc: 'El encabezado de mayor tamaño para títulos de sección; puede convertirse en encabezado desplegable.', cmd: '/e1 · /# · /h1', shortcut: '# + Espacio · Cmd+Alt+1', api: 'heading_1' },
      { id: 'heading_2', name: 'Encabezado 2', enName: 'Heading 2', family: 'basicos', familyName: 'Básicos', icon: 'H2', desc: 'Subencabezado mediano para estructurar apartados secundarios e indexarlos en la tabla de contenidos.', cmd: '/e2 · /## · /h2', shortcut: '## + Espacio · Cmd+Alt+2', api: 'heading_2' },
      { id: 'heading_3', name: 'Encabezado 3 y 4', enName: 'H3 / H4', family: 'basicos', familyName: 'Básicos', icon: 'H3', desc: 'Subencabezado pequeño para divisiones de tercer nivel (la API también define el tipo heading_4).', cmd: '/e3 · /### · /h3', shortcut: '### + Espacio · Cmd+Alt+3', api: 'heading_3, heading_4' },
      { id: 'to_do', name: 'Lista de tareas', enName: 'To-do', family: 'basicos', familyName: 'Básicos', icon: '☑', desc: 'Casillas de verificación interactivas para seguimiento de tareas pendientes y listas de control.', cmd: '/tarea · /todo', shortcut: '[] + Espacio · Cmd+Alt+4', api: 'to_do' },
      { id: 'bulleted_list_item', name: 'Lista con viñetas', enName: 'Bulleted list', family: 'basicos', familyName: 'Básicos', icon: '•', desc: 'Elementos de lista con viñetas que admiten anidación jerárquica mediante la tecla Tabulador.', cmd: '/viñeta · /bullet', shortcut: '- / * / + Espacio · Cmd+Alt+5', api: 'bulleted_list_item' },
      { id: 'numbered_list_item', name: 'Lista numerada', enName: 'Numbered list', family: 'basicos', familyName: 'Básicos', icon: '1.', desc: 'Lista secuencial que numera automáticamente en formato arábigo, alfabético o romano según nivel.', cmd: '/num', shortcut: '1. / a. / i. + Espacio · Cmd+Alt+6', api: 'numbered_list_item' },
      { id: 'toggle', name: 'Lista desplegable', enName: 'Toggle', family: 'basicos', familyName: 'Básicos', icon: '▶', desc: 'Contenedor colapsable para anidar bloques ocultos. Cmd/Ctrl+Alt+T abre o cierra todos los desplegables.', cmd: '/desplegable · /toggle', shortcut: '> + Espacio · Cmd+Alt+7', api: 'toggle' },
      { id: 'child_page', name: 'Página', enName: 'Sub-page', family: 'basicos', familyName: 'Básicos', icon: '📄', desc: 'Inserta una subpágina dentro de la página actual, permitiendo jerarquías y wikis de anidación infinita.', cmd: '/página · /page', shortcut: 'Cmd/Ctrl+Alt+9', api: 'child_page' },
      { id: 'callout', name: 'Destacado', enName: 'Callout', family: 'basicos', familyName: 'Básicos', icon: '💡', desc: 'Caja resaltada con borde, color de fondo e icono/emoji personalizable para notas, avisos y advertencias.', cmd: '/callout', shortcut: 'Menú / o Convertir en', api: 'callout' },
      { id: 'quote', name: 'Cita', enName: 'Quote', family: 'basicos', familyName: 'Básicos', icon: '❝', desc: 'Bloque estilizado con línea lateral vertical y tipografía mayor para separar citas del resto del texto.', cmd: '/cita', shortcut: '" + Espacio', api: 'quote' },
      { id: 'divider', name: 'Divisor', enName: 'Divider', family: 'basicos', familyName: 'Básicos', icon: '—', desc: 'Línea gris horizontal delgada que divide visualmente bloques y secciones temáticas.', cmd: '/div', shortcut: '--- (tres guiones)', api: 'divider' },
      { id: 'table', name: 'Tabla simple', enName: 'Simple Table', family: 'basicos', familyName: 'Básicos', icon: '⊞', desc: 'Cuadrícula visual de filas y columnas con encabezados coloreados, combinación de celdas y opción Turn into Database.', cmd: '/table', shortcut: 'Tab · Cmd+R / Cmd+D', api: 'table, table_row' },
      { id: 'page_link', name: 'Enlace a página', enName: 'Link to page', family: 'basicos', familyName: 'Básicos', icon: '↗', desc: 'Crea un bloque de acceso directo que apunta a cualquier otra página existente en el espacio de trabajo.', cmd: '/enlace', shortcut: 'Menú /', api: 'child_page' },

      // 2. En Línea (5)
      { id: 'mention_user', name: 'Mencionar persona o página', enName: 'Mention user/page', family: 'linea', familyName: 'En Línea', icon: '@', desc: 'Etiqueta a un miembro del equipo (enviando notificación) o enlaza dinámicamente otra página dentro de una oración.', cmd: '/mención', shortcut: '@nombre · @página', api: 'paragraph' },
      { id: 'date_reminder', name: 'Fecha o recordatorio', enName: 'Date / Reminder', family: 'linea', familyName: 'En Línea', icon: '📅', desc: 'Inserta marcas de tiempo dinámicas o recordatorios programados que disparan alertas en el espacio de trabajo.', cmd: '/fecha · /recordatorio', shortcut: '@hoy · @mañana', api: 'paragraph' },
      { id: 'emoji_picker', name: 'Selector de Emoji', enName: 'Emoji picker', family: 'linea', familyName: 'En Línea', icon: '😄', desc: 'Abre el cuadro de emojis en línea e incluye un botón (+) para subir emojis personalizados al espacio.', cmd: '/emoji', shortcut: ':nombre · Ctrl+Cmd+Espacio', api: 'paragraph' },
      { id: 'inline_math', name: 'Ecuación integrada', enName: 'Inline Equation', family: 'linea', familyName: 'En Línea', icon: '∑', desc: 'Renderiza expresiones y símbolos matemáticos en sintaxis TeX/LaTeX directamente dentro de un párrafo.', cmd: '/ecuación', shortcut: '$$fórmula$$', api: 'equation' },
      { id: 'link_preview', name: 'Mención de enlace', enName: 'Link Preview', family: 'linea', familyName: 'En Línea', icon: '🔗', desc: 'Muestra enlaces externos sincronizados en tiempo real con estado en vivo (GitHub, Jira, Slack, Asana, Zoom).', cmd: 'Paste as mention / preview', shortcut: 'Pegar URL (Cmd/Ctrl+V)', api: 'link_preview' },

      // 3. Multimedia y Código (5) - ESTRICTAMENTE SIN AUDIO NI VIDEO
      { id: 'image', name: 'Imagen', enName: 'Image', family: 'multimedia', familyName: 'Multimedia', icon: '🖼️', desc: 'Sube imágenes desde tu equipo, pega un enlace externo o busca fotografías gratuitas en el catálogo de Unsplash.', cmd: '/imagen', shortcut: 'Subir · URL · Unsplash', api: 'image' },
      { id: 'code', name: 'Bloque de Código', enName: 'Code', family: 'multimedia', familyName: 'Multimedia', icon: '</>', desc: 'Editor con resaltado de sintaxis (TypeScript, SQL, Shell, Swift, YAML, XML, WebAssembly, C#, Java, etc.).', cmd: '/código', shortcut: 'Cmd/Ctrl+Alt+8', api: 'paragraph' },
      { id: 'file', name: 'Archivo', enName: 'File', family: 'multimedia', familyName: 'Multimedia', icon: '📎', desc: 'Almacena cualquier tipo de documento o paquete descargable exactamente en la sección deseada de la página.', cmd: '/archivo', shortcut: 'Arrastrar y soltar archivo', api: 'file' },
      { id: 'pdf', name: 'Documento PDF', enName: 'PDF', family: 'multimedia', familyName: 'Multimedia', icon: '📑', desc: 'Incrusta un visor completo de archivos PDF dentro de la página mediante subida local o enlace web.', cmd: '/pdf', shortcut: 'Subir o pegar URL', api: 'pdf' },
      { id: 'bookmark', name: 'Marcador web', enName: 'Bookmark', family: 'multimedia', familyName: 'Multimedia', icon: '🔖', desc: 'Genera una tarjeta visual clicable con el título, descripción, miniatura y dominio de cualquier dirección URL.', cmd: '/marcar', shortcut: 'Pegar URL -> Paste as bookmark', api: 'bookmark' },

      // 4. Bases de Datos y Vistas (10)
      { id: 'db_table', name: 'Vista de Tabla', enName: 'Table View', family: 'bases_datos', familyName: 'Bases de Datos', icon: '▦', desc: 'Base de datos clásica donde cada fila es una página con propiedades, cálculos por columna, filtros y congelación.', cmd: '/Table view', shortcut: 'Botón expande página', api: 'child_database' },
      { id: 'db_board', name: 'Vista de Tablero', enName: 'Board / Kanban', family: 'bases_datos', familyName: 'Bases de Datos', icon: '📊', desc: 'Agrupa tarjetas por estado, prioridad o persona asignada con vista previa de portada y conteos por columna.', cmd: '/Board view · /board', shortcut: 'Agrupación y subgrupos', api: 'child_database' },
      { id: 'db_timeline', name: 'Vista de Cronograma', enName: 'Timeline', family: 'bases_datos', familyName: 'Bases de Datos', icon: '⏳', desc: 'Diagrama cronológico tipo Gantt con barras de fechas estirables, dependencias y tabla lateral desplegable.', cmd: '/Timeline view', shortcut: 'Escala: horas a años', api: 'child_database' },
      { id: 'db_calendar', name: 'Vista de Calendario', enName: 'Calendar View', family: 'bases_datos', familyName: 'Bases de Datos', icon: '📅', desc: 'Ubica páginas según su propiedad Fecha (eventos de uno o varios días) con sincronización en tiempo real.', cmd: '/Calendar view', shortcut: 'Vista mensual o semanal', api: 'child_database' },
      { id: 'db_list', name: 'Vista de Lista', enName: 'List View', family: 'bases_datos', familyName: 'Bases de Datos', icon: '☰', desc: 'Formato minimalista ideal para repositorios de documentos, notas de reuniones y wikis con propiedades a la derecha.', cmd: '/List view', shortcut: 'Apertura en 1 clic', api: 'child_database' },
      { id: 'db_gallery', name: 'Vista de Galería', enName: 'Gallery View', family: 'bases_datos', familyName: 'Bases de Datos', icon: '🖼️', desc: 'Cuadrícula visual que muestra imágenes de portada, primer bloque de contenido o propiedad Files & media.', cmd: '/Gallery view', shortcut: 'Tarjetas S / M / L', api: 'child_database' },
      { id: 'db_chart', name: 'Vista de Gráfico', enName: 'Chart View', family: 'bases_datos', familyName: 'Bases de Datos', icon: '📈', desc: 'Grafica hasta 200 grupos y 50 subgrupos en tiempo real con inspección drilldown y exportación a PNG/SVG.', cmd: '/chart', shortcut: 'Barras · Línea · Dona · Número', api: 'child_database' },
      { id: 'db_dash', name: 'Vista de Panel', enName: 'Dashboard View', family: 'bases_datos', familyName: 'Bases de Datos', icon: '🗂️', desc: 'Centro de control con Modo Edición/Vista y filtros globales multi-base con widgets interactivos.', cmd: '/dash', shortcut: 'Hasta 12 widgets (4/fila)', api: 'child_database' },
      { id: 'db_form', name: 'Formulario', enName: 'Form View', family: 'bases_datos', familyName: 'Bases de Datos', icon: '📋', desc: 'Captura respuestas web o internas como filas de base de datos con preguntas obligatorias y alertas por correo.', cmd: '/form', shortcut: 'Lógica condicional y automatización', api: 'child_database' },
      { id: 'db_map', name: 'Vista de Mapa y Vista de Feed', enName: 'Map & Feed View', family: 'bases_datos', familyName: 'Bases de Datos', icon: '📍', desc: 'Mapa interactivo con hasta 100 pines geográficos (/map) o flujo lineal tipo blog con comentarios y vistas.', cmd: '/map · /Feed view', shortcut: 'Propiedad Place · Tarjetas', api: 'child_database' },

      // 5. Incrustaciones (4)
      { id: 'embed_universal', name: 'Incrustación Universal', enName: '+1,900 apps', family: 'incrustaciones', familyName: 'Incrustaciones', icon: '🌐', desc: 'Integra +1,900 dominios vía Iframely (Canva, Miro, Excalidraw, Tableau, Tally, Replit) con barras de redimensionado.', cmd: '/insertar · /embed', shortcut: 'URL https -> Create Embed', api: 'embed' },
      { id: 'embed_gdrive', name: 'Google Drive y Google Maps', enName: 'Drive & Maps', family: 'incrustaciones', familyName: 'Incrustaciones', icon: '🔺', desc: 'Incrusta Docs, Sheets y Slides buscando directo en Drive o inserta mapas interactivos de Google Maps.', cmd: '/drive · /maps', shortcut: 'Browse Google Drive', api: 'embed' },
      { id: 'embed_figma', name: 'Figma, Framer, Invision y Whimsical', enName: 'Design Embeds', family: 'incrustaciones', familyName: 'Incrustaciones', icon: '🎨', desc: 'Muestra archivos de diseño de Figma, prototipos de Framer/Invision y mapas mentales o flujos de Whimsical.', cmd: '/figma · /framer · /whimsical', shortcut: 'Prototipos y lienzos en vivo', api: 'embed' },
      { id: 'embed_dev', name: 'GitHub Gist, CodePen, Loom y Typeform', enName: 'Dev & Forms', family: 'incrustaciones', familyName: 'Incrustaciones', icon: '💻', desc: 'Incrusta código desde GitHub/CodePen, grabaciones interactivas de Loom y encuestas de Typeform.', cmd: '/gist · /codepen · /loom · /tweet', shortcut: 'tweet + Intro', api: 'embed' },

      // 6. Avanzados (6)
      { id: 'toc', name: 'Tabla de contenidos', enName: 'Table of contents', family: 'avanzados', familyName: 'Avanzados', icon: '📑', desc: 'Genera un índice automático con enlaces de salto a todos los encabezados presentes en la página.', cmd: '/indice', shortcut: 'Enlaces a H1, H2, H3', api: 'table_of_contents' },
      { id: 'macro_button', name: 'Botón de automatización', enName: 'Button', family: 'avanzados', familyName: 'Avanzados', icon: '⚡', desc: 'Ejecuta flujos automatizados con un clic: inserta bloques predefinidos o añade/edita páginas en bases de datos.', cmd: '/botón · /plantilla', shortcut: 'Ejecución en 1 clic', api: 'template' },
      { id: 'breadcrumbs', name: 'Ruta de navegación', enName: 'Breadcrumb', family: 'avanzados', familyName: 'Avanzados', icon: '🧭', desc: 'Muestra automáticamente la ruta de páginas padre para ubicar dónde vive el documento actual en el espacio.', cmd: '/ruta', shortcut: 'Jerarquía automática', api: 'breadcrumb' },
      { id: 'synced', name: 'Bloque sincronizado', enName: 'Synced Block', family: 'avanzados', familyName: 'Avanzados', icon: '🔄', desc: 'Espeja contenido idéntico en múltiples páginas con halo rojo; cualquier edición se actualiza en todas las ubicaciones en vivo.', cmd: '/synced', shortcut: 'Copiar y sincronizar', api: 'synced_block' },
      { id: 'columns', name: 'Columnas', enName: 'Column List & Column', family: 'avanzados', familyName: 'Avanzados', icon: '▥', desc: 'Divide el ancho de la página en columnas paralelas para maquetar textos, tablas e imágenes lado a lado.', cmd: '/columns', shortcut: 'Arrastrar ⋮⋮ al borde lateral', api: 'column_list, column' },
      { id: 'latex', name: 'Bloque de Ecuación', enName: 'LaTeX / TeX', family: 'avanzados', familyName: 'Avanzados', icon: '∫', desc: 'Bloque dedicado para expresiones matemáticas y científicas centradas utilizando notación TeX completa.', cmd: '/mat · /latex', shortcut: '$$ en bloque', api: 'equation' },

    ];

    let catalogCurrentFamily = 'all';
    let catalogSearchQuery = '';
    let catalogActiveApiFilter = null;

    function toggleBlockCatalog(forceState) {
      const drawer = document.getElementById('panel-block-catalog');
      if (!drawer) return;
      const isOpen = typeof forceState === 'boolean' ? forceState : !drawer.classList.contains('open');
      drawer.classList.toggle('open', isOpen);
      if (isOpen) {
        renderCatalogCards();
        renderCatalogApiChips();
        const input = document.getElementById('catalog-search-input');
        if (input) setTimeout(() => { input.focus(); }, 60);
      }
    }

    function filterCatalogByFamily(familyKey) {
      catalogCurrentFamily = familyKey;
      catalogActiveApiFilter = null;
      document.querySelectorAll('#catalog-family-tabs .catalog-family-tab').forEach(tab => {
        tab.classList.toggle('active', tab.getAttribute('data-family') === familyKey);
      });
      renderCatalogCards();
    }

    function handleCatalogSearch(query) {
      catalogSearchQuery = (query || '').toLowerCase().trim();
      const clearBtn = document.getElementById('catalog-search-clear');
      if (clearBtn) clearBtn.style.display = catalogSearchQuery ? 'inline-block' : 'none';
      renderCatalogCards();
    }

    function clearCatalogSearch() {
      const input = document.getElementById('catalog-search-input');
      if (input) input.value = '';
      catalogSearchQuery = '';
      const clearBtn = document.getElementById('catalog-search-clear');
      if (clearBtn) clearBtn.style.display = 'none';
      renderCatalogCards();
    }

    function filterCatalogByApiType(apiType) {
      if (catalogActiveApiFilter === apiType) {
        catalogActiveApiFilter = null;
      } else {
        catalogActiveApiFilter = apiType;
      }
      document.querySelectorAll('#catalog-api-chips .catalog-api-enum-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-api') === catalogActiveApiFilter);
      });
      renderCatalogCards();
    }

    function renderCatalogCards() {
      const grid = document.getElementById('catalog-cards-grid');
      const countEl = document.getElementById('catalog-count-badge');
      const bannerText = document.getElementById('catalog-banner-text');
      if (!grid) return;

      const familyDescriptions = {
        all: '<strong>Todas las Familias:</strong> Mapa completo de los bloques interactivos de Notion agrupados en sus 6 familias arquitectónicas y vinculados a sus tipos de objeto en la API. Haz clic en cualquier tarjeta para insertarlo directamente en tu nota.',
        basicos: '<strong>1. Bloques Básicos:</strong> Estructura esencial de página (párrafos, títulos H1–H4, listas ordenadas y viñetas, citas, toggles, tablas simples y subpáginas).',
        linea: '<strong>2. Bloques En Línea:</strong> Elementos semánticos integrados dentro del flujo de texto (menciones dinámicas, fechas con alertas, selector de emojis, ecuaciones matemáticas KaTeX y previsualizaciones de enlaces).',
        multimedia: '<strong>3. Multimedia y Código:</strong> Imágenes interactivas redimensionables, resaltado de código multilenguaje, visores de archivos PDF y marcadores web.',
        bases_datos: '<strong>4. Bases de Datos y Vistas:</strong> Sistemas estructurados con 10 vistas interactivas (Tabla, Tablero Kanban, Cronograma, Calendario, Lista, Galería, Gráfico estadístico, Dashboard, Formulario y Mapa/Feed).',
        incrustaciones: '<strong>5. Incrustaciones:</strong> Conexión con más de 1,900 aplicaciones web (Google Drive, Google Maps, prototipos de Figma, repositorios GitHub, CodePen y Typeform).',
        avanzados: '<strong>6. Avanzados:</strong> Bloques con comportamiento reactivo (Índices automáticos ToC, botones de automatización, migas de pan, bloques sincronizados con halo rojo, columnas paralelas y LaTeX científico).'
      };

      if (bannerText && familyDescriptions[catalogCurrentFamily]) {
        bannerText.innerHTML = familyDescriptions[catalogCurrentFamily];
      }

      let filtered = NOTION_BLOCK_CATALOG.filter(b => {
        if (catalogCurrentFamily !== 'all' && b.family !== catalogCurrentFamily) return false;
        if (catalogActiveApiFilter && !b.api.toLowerCase().includes(catalogActiveApiFilter.toLowerCase())) return false;
        if (catalogSearchQuery) {
          const hay = `${b.name} ${b.enName} ${b.desc} ${b.cmd} ${b.shortcut} ${b.api} ${b.familyName}`.toLowerCase();
          if (!hay.includes(catalogSearchQuery)) return false;
        }
        return true;
      });

      if (countEl) {
        countEl.textContent = `Mostrando ${filtered.length} de ${NOTION_BLOCK_CATALOG.length} grupos de bloques`;
      }

      if (filtered.length === 0) {
        grid.innerHTML = `
          <div style="grid-column: 1 / -1; padding: 40px 16px; text-align: center; color: var(--text-muted);">
            <div style="font-size: 26px; margin-bottom: 8px;">🔍</div>
            <div style="font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 4px;">No se encontraron bloques</div>
            <div style="font-size: 12px;">Prueba a cambiar el término de búsqueda o selecciona otra familia arquitectónica.</div>
          </div>
        `;
        return;
      }

      grid.innerHTML = filtered.map(b => {
        const familyBadgeClass = `badge-family-${b.family}`;
        return `
          <div class="catalog-block-card" onclick="insertBlockFromCatalog('${b.id}')" title="Haz clic para insertar este bloque en la página">
            <div>
              <div class="catalog-card-header">
                <div class="catalog-card-icon-box">${escapeHtmlAttr(b.icon)}</div>
                <div class="catalog-card-title-group">
                  <div class="catalog-card-title">${escapeHtmlAttr(b.name)} <span style="font-size:11.5px; opacity:0.75; font-weight:500;">(${escapeHtmlAttr(b.enName)})</span></div>
                  <span class="catalog-card-badge ${familyBadgeClass}">${escapeHtmlAttr(b.familyName)}</span>
                </div>
              </div>
              <p class="catalog-card-desc" style="margin-top:8px;">${escapeHtmlAttr(b.desc)}</p>
            </div>

            <div class="catalog-card-footer">
              <div class="catalog-card-cmd-row">
                ${b.cmd.split('·').map(c => `<span class="catalog-cmd-pill">${escapeHtmlAttr(c.trim())}</span>`).join('')}
              </div>
              <div class="catalog-card-meta-row">
                <span class="catalog-shortcut-badge">${escapeHtmlAttr(b.shortcut)}</span>
                <span class="catalog-api-pill">API: ${escapeHtmlAttr(b.api)}</span>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderCatalogApiChips() {
      const container = document.getElementById('catalog-api-chips');
      if (!container) return;
      container.innerHTML = NOTION_API_ENUM_TYPES.map((type, idx) => {
        const isActive = catalogActiveApiFilter === type;
        return `
          <button type="button" class="catalog-api-enum-btn ${isActive ? 'active' : ''}" data-api="${type}" onclick="filterCatalogByApiType('${type}')">
            <span>${idx + 1}. ${type}</span>
          </button>
        `;
      }).join('');
    }

    function insertBlockFromCatalog(blockKey) {
      toggleBlockCatalog(false);
      const editor = document.getElementById('rich-editor-canvas');
      if (!editor) return;

      if (blockKey === 'text') {
        const p = document.createElement('p');
        p.innerHTML = '<br>';
        editor.appendChild(p);
        p.focus();
      } else if (blockKey === 'heading_1') {
        const h1 = document.createElement('h1');
        h1.textContent = 'Encabezado 1';
        editor.appendChild(h1);
      } else if (blockKey === 'heading_2') {
        const h2 = document.createElement('h2');
        h2.textContent = 'Encabezado 2';
        editor.appendChild(h2);
      } else if (blockKey === 'heading_3') {
        const h3 = document.createElement('h3');
        h3.textContent = 'Encabezado 3';
        editor.appendChild(h3);
      } else if (blockKey === 'to_do') {
        insertChecklistBlock();
        return;
      } else if (blockKey === 'bulleted_list_item') {
        const ul = document.createElement('ul');
        ul.innerHTML = '<li>Elemento de lista con viñeta</li>';
        editor.appendChild(ul);
      } else if (blockKey === 'numbered_list_item') {
        const ol = document.createElement('ol');
        ol.innerHTML = '<li>1. Primer elemento de lista</li>';
        editor.appendChild(ol);
      } else if (blockKey === 'toggle') {
        insertInlineToggleElement();
        return;
      } else if (blockKey === 'child_page') {
        insertSubpageBlock();
        return;
      } else if (blockKey === 'callout') {
        insertInlineCalloutElement();
        return;
      } else if (blockKey === 'quote') {
        const q = document.createElement('blockquote');
        q.textContent = 'Cita estilizada con tipografía ampliada';
        editor.appendChild(q);
      } else if (blockKey === 'divider') {
        insertDividerElement();
        return;
      } else if (blockKey === 'table') {
        insertSimpleTableBlock();
        return;
      } else if (blockKey === 'page_link') {
        promptAddShortcut();
        return;
      } else if (blockKey === 'image') {
        openImageInsertModal();
        return;
      } else if (blockKey === 'code') {
        insertInlineCodeBlock();
        return;
      } else if (blockKey === 'pdf' || blockKey === 'file') {
        openMediaEmbedModal('pdf');
        return;
      } else if (blockKey.startsWith('db_')) {
        const v = blockKey.replace('db_', '');
        openDatabaseWithView(v);
        return;
      } else if (blockKey.startsWith('embed_')) {
        const embedType = blockKey === 'embed_gdrive' ? 'gdrive' : (blockKey === 'embed_figma' ? 'figma' : (blockKey === 'embed_dev' ? 'codepen' : 'pdf'));
        openMediaEmbedModal(embedType);
        return;
      } else if (blockKey === 'toc') {
        insertTableOfContentsBlock();
        return;
      } else if (blockKey === 'macro_button') {
        openMacroButtonModal();
        return;
      } else if (blockKey === 'breadcrumbs') {
        insertBreadcrumbsBlock();
        return;
      } else if (blockKey === 'synced') {
        insertSyncedBlock();
        return;
      } else if (blockKey === 'columns') {
        insertColumnsBlock(2);
        return;
      } else if (blockKey === 'latex') {
        toggleKatexBlock(true);
        return;
      } else if (blockKey === 'inline_math') {
        openInlineMathPopover();
        return;
      } else {
        const p = document.createElement('p');
        p.innerHTML = `<span class="notion-block-badge">API: ${escapeHtmlAttr(blockKey)}</span> <br>`;
        editor.appendChild(p);
      }

      syncRichEditor();
      showToast(`Bloque insertado desde el catálogo`, '📖');
    }

    /* ==========================================================================
       15. PANEL 1: ANATOMÍA UNIVERSAL DE UN BLOQUE EN EL LIENZO
       ========================================================================== */
    function openBlockAnatomyModal() {
      const modal = document.getElementById('modal-block-anatomy');
      if (modal) {
        modal.classList.add('open');
      }
    }

    function closeBlockAnatomyModal() {
      const modal = document.getElementById('modal-block-anatomy');
      if (modal) {
        modal.classList.remove('open');
      }
    }

    function setAnatomyInspectionTab(tabId) {
      document.querySelectorAll('#modal-block-anatomy .anatomy-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
      });
      const tips = {
        handle: 'Manejador (⋮⋮): Aparece al pasar el cursor. Arrástralo para mover o crear columnas. Haz clic para el menú de 8 opciones completas.',
        slash: 'Menú Slash (/): Escribe "/" en cualquier bloque vacío para desplegar el menú flotante de bloques Notion y comandos de color.',
        add: 'Añadir Bloque (+): Haz clic en "+" para insertar un nuevo bloque abajo. Usa Option/Alt + clic para insertar arriba.',
        format: 'Formato Enriquecido: Selecciona cualquier fragmento de texto para mostrar la barra flotante con negrita, cursiva, código y enlaces.'
      };
      showToast(tips[tabId] || 'Control seleccionado', '🔍');
    }

    function runAnatomyAction(actionKey) {
      if (actionKey === 'turn_into') {
        showToast('Convertir en: Transforma este bloque en Tarea, H1, H2, Cita o Desplegable', '🔄');
      } else if (actionKey === 'comment') {
        showToast('Comentarios: Inserta un hilo de debate o sugerencias de edición', '💬');
      } else if (actionKey === 'add_below') {
        showToast('+ Añadir: Inserta un bloque directamente debajo (o Alt+Clic para arriba)', '+');
      } else if (actionKey === 'grip_click') {
        showToast('⋮⋮ Manejador: Despliega Convertir en, Color, Duplicar, Mover a, Anchor URL y Eliminar', '⋮⋮');
      } else {
        showToast(`Formato "${actionKey}" aplicado en previsualización`, 'Aa');
      }
    }

    function runAnatomyMenuCard(actionKey) {
      const explanations = {
        turn_into: 'Convertir en: Permite mutar el bloque conservando todo su contenido original (/convertir).',
        color: 'Color: Aplica uno de los 10 colores de texto o 10 fondos disponibles. Usa /predeterminado para limpiar.',
        duplicate: 'Duplicar: Clona instantáneamente el bloque (o selección múltiple) con nuevo ID inmutable (Cmd/Ctrl+D).',
        move: 'Mover a: Reubica el bloque o muévelo arriba/abajo entre secciones del documento.',
        copy_link: 'Copiar enlace al bloque: Genera una URL de anclaje directo (#block-id) para citar este párrafo exacto.',
        delete: 'Eliminar: Borra el bloque del lienzo y actualiza el árbol de nodos en SQLite (Del / Backspace).',
        comment: 'Comentar / Sugerir: Abre un hilo de notas al margen sin alterar el texto original (Cmd+Mayús+M).',
        synced: 'Bloque Sincronizado: Espeja contenido idéntico en múltiples páginas con marco visual distintivo (/synced).'
      };
      showToast(explanations[actionKey] || 'Acción de bloque Notion', 'ℹ️');
    }

    function applyLastColorToBlock(blockEl) {
      if (!blockEl) return;
      if (lastAppliedColorStyle.type === 'bg' && lastAppliedColorStyle.value) {
        blockEl.style.backgroundColor = lastAppliedColorStyle.value;
        blockEl.style.padding = '8px 12px';
        blockEl.style.borderRadius = '7px';
        showToast('Último color de fondo aplicado (Cmd+⇧+H)', '🎨');
      } else if (lastAppliedColorStyle.type === 'color' && lastAppliedColorStyle.value) {
        blockEl.style.color = lastAppliedColorStyle.value;
        showToast('Último color de texto aplicado (Cmd+⇧+H)', '🎨');
      } else {
        blockEl.style.backgroundColor = 'rgba(59, 130, 246, 0.16)';
        blockEl.style.padding = '8px 12px';
        blockEl.style.borderRadius = '7px';
        showToast('Color azul aplicado (Cmd+⇧+H)', '🎨');
      }
      syncRichEditor();
    }

    /* ==========================================================================
       16. GESTOR DE VENTANA NATIVA DE ESCRITORIO (PyWebView + API)
       ========================================================================== */
    async function minimizeWindow() {
      if (window.pywebview && window.pywebview.api && typeof window.pywebview.api.minimize_window === 'function') {
        try {
          return await window.pywebview.api.minimize_window();
        } catch (e) {
          console.warn('pywebview minimize error:', e);
        }
      }
      try {
        const res = await fetch('/api/window/minimize', { method: 'POST' });
        return await res.json();
      } catch (e) {
        console.warn('API window minimize error:', e);
      }
    }

    async function toggleMaximizeWindow() {
      let isMax = false;
      if (window.pywebview && window.pywebview.api && typeof window.pywebview.api.toggle_maximize_window === 'function') {
        try {
          const res = await window.pywebview.api.toggle_maximize_window();
          isMax = Boolean(res && res.action === 'maximize');
          updateMaximizeIcon(isMax);
          return res;
        } catch (e) {
          console.warn('pywebview maximize error:', e);
        }
      }
      try {
        const res = await fetch('/api/window/maximize', { method: 'POST' });
        const data = await res.json();
        isMax = Boolean(data && data.action === 'maximize');
        updateMaximizeIcon(isMax);
        return data;
      } catch (e) {
        console.warn('API window maximize error:', e);
      }
    }

    async function closeWindow() {
      if (window.pywebview && window.pywebview.api && typeof window.pywebview.api.close_window === 'function') {
        try {
          return await window.pywebview.api.close_window();
        } catch (e) {
          console.warn('pywebview close error:', e);
        }
      }
      try {
        const res = await fetch('/api/window/close', { method: 'POST' });
        return await res.json();
      } catch (e) {
        console.warn('API window close error:', e);
      }
    }

    function updateMaximizeIcon(isMaximized) {
      const btn = document.getElementById('btn-win-maximize');
      const icon = document.getElementById('svg-win-maximize-icon');
      if (!btn) return;
      if (isMaximized) {
        btn.title = 'Restaurar';
        btn.setAttribute('aria-label', 'Restaurar');
        if (icon) {
          icon.innerHTML = `<rect x="5" y="3" width="16" height="16" rx="2" ry="2"></rect><polyline points="3 7 3 21 17 21"></polyline>`;
        }
      } else {
        btn.title = 'Maximizar';
        btn.setAttribute('aria-label', 'Maximizar');
        if (icon) {
          icon.innerHTML = `<rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>`;
        }
      }
    }

    function toggleWinMenu(e) {
      if (e) e.stopPropagation();
      openSettingsModal();
    }

    function initTopBarWindowControls() {
      const topBar = document.querySelector('.top-bar');
      if (!topBar) return;

      // Doble clic en espacio vacío de la barra para maximizar/restaurar
      topBar.addEventListener('dblclick', (e) => {
        if (!e.target.closest('button, .note-tab-item, #window-controls-bar, input, select, textarea')) {
          toggleMaximizeWindow();
        }
      });

      // Evitar que el clic en botones interactivos dispare arrastre de ventana en PyWebView
      topBar.addEventListener('mousedown', (e) => {
        if (e.target.closest('button, .note-tab-item, #window-controls-bar, input, select, textarea')) {
          e.stopPropagation();
        }
      });
    }

    /* ==========================================================================
       17. VISTA DE RECORDATORIOS Y AGENDA A PANTALLA COMPLETA (R3)
       ========================================================================== */
    function navigateToReminders() {
      state.isRemindersActive = true;
      state.isHomeActive = false;

      const scaffold = document.getElementById('desktop-scaffold');
      if (scaffold) {
        scaffold.classList.add('is-reminders-active');
        scaffold.classList.remove('is-home-active');
      }

      const remindersBtn = document.getElementById('fitem-sidebar-reminders');
      if (remindersBtn) {
        remindersBtn.classList.add('active');
        remindersBtn.setAttribute('aria-pressed', 'true');
      }

      const homeBtn = document.getElementById('btn-top-home');
      if (homeBtn) {
        homeBtn.classList.remove('active');
        homeBtn.setAttribute('aria-pressed', 'false');
      }

      const homeView = document.getElementById('home-page-view');
      const remindersView = document.getElementById('reminders-page-view');
      const formatBar = document.querySelector('.desktop-format-bar');
      const notionCover = document.getElementById('notion-cover');
      const editorBody = document.getElementById('editor-body');

      if (homeView) homeView.style.display = 'none';
      if (remindersView) remindersView.style.display = 'flex';
      if (formatBar) formatBar.style.display = 'none';
      if (notionCover) notionCover.style.display = 'none';
      if (editorBody) editorBody.style.display = 'none';

      renderFolders();
      renderNoteTabs();
      renderRemindersPageView();
    }

    function exitRemindersView() {
      if (!state.isRemindersActive) return;
      state.isRemindersActive = false;

      const scaffold = document.getElementById('desktop-scaffold');
      if (scaffold) {
        scaffold.classList.remove('is-reminders-active');
      }

      const remindersBtn = document.getElementById('fitem-sidebar-reminders');
      if (remindersBtn) {
        remindersBtn.classList.remove('active');
        remindersBtn.setAttribute('aria-pressed', 'false');
      }

      const remindersView = document.getElementById('reminders-page-view');
      if (remindersView) remindersView.style.display = 'none';

      renderFolders();
      renderNoteTabs();
    }

    function setRemindersTab(tab) {
      state.remindersTab = tab;
      renderRemindersPageView();
    }

    function renderRemindersPageView() {
      const container = document.getElementById('reminders-page-view');
      if (!container) return;

      const totalCount = (state.reminders || []).length;
      const pendingList = (state.reminders || []).filter(r => !r.completed);
      const completedList = (state.reminders || []).filter(r => r.completed);
      const todayStr = getTodayDateString();
      const todayCount = (state.reminders || []).filter(r => r.date === todayStr && !r.completed).length;

      const currentTab = state.remindersTab || 'all';

      let filteredReminders = [...(state.reminders || [])];
      if (currentTab === 'pending') {
        filteredReminders = pendingList;
      } else if (currentTab === 'completed') {
        filteredReminders = completedList;
      }

      filteredReminders.sort((a, b) => {
        if (a.completed !== b.completed) return a.completed ? 1 : -1;
        return (a.date || '').localeCompare(b.date || '');
      });

      const categoryClassMap = {
        'Trabajo': 'cat-trabajo',
        'Desarrollo': 'cat-desarrollo',
        'Urgente': 'cat-urgente',
        'Personal': 'cat-personal',
        'Universidad': 'cat-universidad',
        'Reunión': 'cat-trabajo'
      };

      container.innerHTML = `
        <div class="reminders-full-header">
          <div class="reminders-full-title-wrap">
            <span class="reminders-full-icon-badge">📅</span>
            <div>
              <h2 style="margin:0; font-size:22px; font-weight:800; color:var(--text-primary); letter-spacing:-0.02em;">Recordatorios y Agenda</h2>
              <span style="font-size:12.5px; color:var(--text-muted);">Gestiona tus tareas programadas, citas y plazos de entrega</span>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:10px;">
            <button type="button" class="btn-primary" onclick="openNewEventModal('${todayStr}')" style="display:inline-flex; align-items:center; gap:6px; padding:7px 14px; font-size:12.5px; font-weight:700;">
              <span>+ Nuevo Recordatorio</span>
            </button>
          </div>
        </div>

        <!-- Estadísticas Rápidas -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(160px, 1fr)); gap:14px; margin-bottom:20px;">
          <div style="background:var(--bg-surface); border:1px solid var(--border-hairline); border-radius:10px; padding:12px 16px; display:flex; flex-direction:column; gap:4px;">
            <span style="font-size:11px; font-weight:700; color:var(--text-muted); text-transform:uppercase;">Total Recordatorios</span>
            <span style="font-size:24px; font-weight:800; color:var(--text-primary);">${totalCount}</span>
          </div>
          <div style="background:var(--bg-surface); border:1px solid var(--border-hairline); border-radius:10px; padding:12px 16px; display:flex; flex-direction:column; gap:4px;">
            <span style="font-size:11px; font-weight:700; color:var(--accent-amber); text-transform:uppercase;">Pendientes</span>
            <span style="font-size:24px; font-weight:800; color:var(--accent-amber);">${pendingList.length}</span>
          </div>
          <div style="background:var(--bg-surface); border:1px solid var(--border-hairline); border-radius:10px; padding:12px 16px; display:flex; flex-direction:column; gap:4px;">
            <span style="font-size:11px; font-weight:700; color:#10b981; text-transform:uppercase;">Completados</span>
            <span style="font-size:24px; font-weight:800; color:#10b981;">${completedList.length}</span>
          </div>
          <div style="background:var(--bg-surface); border:1px solid var(--border-hairline); border-radius:10px; padding:12px 16px; display:flex; flex-direction:column; gap:4px;">
            <span style="font-size:11px; font-weight:700; color:#3b82f6; text-transform:uppercase;">Para Hoy</span>
            <span style="font-size:24px; font-weight:800; color:#3b82f6;">${todayCount}</span>
          </div>
        </div>

        <!-- Pestañas de Filtro -->
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; border-bottom:1px solid var(--border-hairline); padding-bottom:8px;">
          <div style="display:flex; gap:6px;">
            <button type="button" class="btn-secondary ${currentTab === 'all' ? 'active' : ''}" onclick="setRemindersTab('all')" style="font-size:12px; padding:5px 12px; border-radius:6px;">Todos (${totalCount})</button>
            <button type="button" class="btn-secondary ${currentTab === 'pending' ? 'active' : ''}" onclick="setRemindersTab('pending')" style="font-size:12px; padding:5px 12px; border-radius:6px;">Pendientes (${pendingList.length})</button>
            <button type="button" class="btn-secondary ${currentTab === 'completed' ? 'active' : ''}" onclick="setRemindersTab('completed')" style="font-size:12px; padding:5px 12px; border-radius:6px;">Completados (${completedList.length})</button>
          </div>
        </div>

        <!-- Lista de Recordatorios -->
        <div class="reminders-full-cards-list" style="display:flex; flex-direction:column; gap:10px; max-width:900px;">
          ${filteredReminders.length === 0 ? `
            <div style="text-align:center; padding:48px 20px; background:var(--bg-surface); border:1px dashed var(--border-hairline); border-radius:12px;">
              <span style="font-size:32px; display:block; margin-bottom:10px;">🎉</span>
              <strong style="font-size:15px; color:var(--text-primary); display:block;">No hay recordatorios en esta sección</strong>
              <span style="font-size:12px; color:var(--text-muted); display:block; margin-top:4px;">Crea uno nuevo con el botón superior para organizar tu agenda.</span>
            </div>
          ` : filteredReminders.map(ev => {
            const catClass = categoryClassMap[ev.category] || '';
            const safeTitle = escapeHtmlAttr(ev.title || 'Recordatorio');
            const isCompleted = Boolean(ev.completed);

            return `
              <div class="home-event-card ${isCompleted ? 'completed' : ''}" id="reminders-card-${ev.id}" style="padding:12px 16px; border-radius:10px; background:var(--bg-surface); border:1px solid var(--border-hairline);">
                <div class="home-event-card-left" style="display:flex; align-items:center; gap:12px; flex:1; min-width:0;">
                  <button type="button" 
                          class="home-event-checkbox" 
                          onclick="toggleHomeReminder(${ev.id})" 
                          title="${isCompleted ? 'Marcar como pendiente' : 'Marcar como completado'}"
                          aria-label="Alternar estado de evento">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </button>
                  <div class="home-event-info" style="min-width:0;">
                    <span class="home-event-title" style="font-size:13.5px; font-weight:600; color:var(--text-primary); ${isCompleted ? 'text-decoration:line-through; opacity:0.6;' : ''}">${safeTitle}</span>
                    <div class="home-event-meta-row" style="display:flex; align-items:center; gap:10px; margin-top:4px; font-size:11.5px; color:var(--text-muted);">
                      ${ev.time ? `<span>🕒 ${escapeHtmlAttr(ev.time)}</span>` : '<span>🕒 Todo el día</span>'}
                      ${ev.date ? `<span>📅 ${escapeHtmlAttr(ev.date)}</span>` : ''}
                      ${ev.category ? `<span class="home-event-category-pill ${catClass}">${escapeHtmlAttr(ev.category)}</span>` : ''}
                    </div>
                  </div>
                </div>
                <button type="button" class="home-event-delete-btn" onclick="deleteHomeReminder(${ev.id})" title="Eliminar recordatorio" aria-label="Eliminar recordatorio">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    window.NoteJSLocal = {
      ready: cloudLocalReady,
      masterFolder: MASTER_ALL_NOTES_FOLDER,
      getNotes: () => state.notes,
      async persist(note, refresh = false) {
        const result = await (hasPyWebViewBridge() && typeof window.pywebview.api.save_note === 'function'
          ? window.pywebview.api.save_note(note)
          : fetch('/api/notes', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({note})}).then(response => {if (!response.ok) throw new Error('No se pudo guardar la nota en esta PC.'); return response.json();}));
        if (!result.ok) throw new Error(result.error || 'No se pudo guardar la nota en esta PC.');
        const index = state.notes.findIndex(item => item.id === note.id);
        if (index < 0) state.notes.unshift(note); else state.notes[index] = note;
        const folder = note.folders?.find(value => value !== MASTER_ALL_NOTES_FOLDER) || note.folder;
        if (folder && !state.folders.includes(folder)) { state.folders.push(folder); persistFoldersLocal(); saveFoldersToBackend(); }
        persistNoteMetaOverlay();
        localStorage.setItem('notejs_desktop_notion_v9',JSON.stringify(state.notes));
        if (refresh) {
          renderFolders(); renderNotesList(); renderNoteTabs();
          if (state.activeNoteId === note.id) loadActiveNote();
          if (state.isHomeActive) renderHomePage();
        }
      }
    };

    // Exponer funciones en window para unittests y llamadas globales
    window.minimizeWindow = minimizeWindow;
    window.toggleMaximizeWindow = toggleMaximizeWindow;
    window.closeWindow = closeWindow;
    window.updateMaximizeIcon = updateMaximizeIcon;
    window.toggleWinMenu = toggleWinMenu;
    window.navigateToReminders = navigateToReminders;
    window.exitRemindersView = exitRemindersView;
    window.renderRemindersPageView = renderRemindersPageView;
    window.setRemindersTab = setRemindersTab;
    window.setFolderModalType = setFolderModalType;
    window.handleStartupBehaviorChange = handleStartupBehaviorChange;
    window.toggleTocExpanded = toggleTocExpanded;

    window.addEventListener('DOMContentLoaded', () => {
      initTopBarWindowControls();
      initTocScrollSpy();
      initSpatialBlockController();
      initStructuralKeyboardShortcuts();
      setTimeout(() => {
        const note = getActiveNote();
        if (note) applyNoteAppearanceSettings(note);
        refreshPageTableOfContents();
        attachColumnResizerListeners();
        attachSyncedBlockListeners();
      }, 160);
    });

    window.addEventListener('pywebviewready', initPythonBackendSync);
    window.addEventListener('DOMContentLoaded', init);




