# Ecosistema Completo de Bloques Notion y Catálogo Arquitectónico por Familias

Sistema integral de bloques interactivos de Notion para Note JS, integrando el catálogo completo de 7 familias arquitectónicas y tipos de objeto de la API (excluyendo de forma estricta audio y video), un panel lateral deslizante con explorador y buscador de bloques, el inspector de Anatomía Universal del Bloque (Panel 1 con acciones rápidas, atajos y conversión), y vistas completas de bases de datos embebidas.

### User Review & Critical Decisions

> [!IMPORTANT]
> **Decisiones confirmadas por el usuario en Fase 1:**
> - **Acceso al Catálogo de Bloques**: Panel lateral desplegable con buscador en tiempo real, pestañas de filtrado por familias y acceso directo a los 30+ tipos de bloque.
> - **Vistas de Bases de Datos**: Vistas interactivas completas embebidas en el lienzo con pestañas de cambio rápido de vista (Tabla, Tablero Kanban, Cronograma/Timeline, Calendario, Lista, Galería, Gráfico, Formulario, Dashboard).
> - **Inspector de Anatomía Universal (Panel 1)**: Modal e inspector contextual con atajos de teclado y acciones de conversión rápida (*Turn into*, paleta de color de texto/fondo, duplicar, mover, copiar anclaje directo, sugerencias e IA).
> - **Restricción Negativa Estricta**: Exclusión total de bloques, comandos slash y botones de **Audio** y **Video** en toda la interfaz y catálogo.

---

### 1. Overview & Core Concept

- **Qué hace el sistema**: Transforma el editor de notas enriquecido en una suite completa de bloques Notion. Cada párrafo, llamada (*callout*), tabla simple, bloque de código, ecuación LaTeX, cita, bloque sincronizado y base de datos es un bloque modular de primer orden, etiquetado con identificador persistente (`data-block-id`) y orden fraccional base-62.
- **Público Objetivo**: Usuarios de Note JS que requieren crear wikis estructurados, especificaciones de ingeniería, apuntes matemáticos KaTeX, cuadros de mando y bases de datos relacionales sin fricción.
- **Valor Clave**: Fusión de la experiencia de edición minimalista estilo macOS/Notion con la potencia de un catálogo interactivo de bloques accesible con un clic o atajo (`Ctrl+Shift+B` o icono en la barra de herramientas), con atajos slash fluidos (`/`) y sin sobrecarga innecesaria de medios audiovisuales.

---

### 2. User Experience & Visual Design

#### A. Flujo de Usuario y Nuevos Componentes
1. **Panel Lateral Desplegable del Catálogo de Bloques**:
   - Se abre mediante un nuevo botón en la barra superior o cabecera del editor, o con el atajo `Ctrl+Shift+B`.
   - Incluye barra de búsqueda predictiva ("Buscar bloque, comando ej. /callout, /chart, o tipo API...").
   - Pestañas de filtrado rápido por familias: *Todas (48)*, *1. Básicos*, *2. En Línea*, *3. Código y Archivos (sin audio/video)*, *4. Bases de Datos y Vistas*, *5. Incrustaciones*, *6. Avanzados*, *7. Inteligencia Artificial*.
   - Al hacer clic en cualquier tarjeta del catálogo, se inserta inmediatamente el bloque interactivo correspondiente en la posición actual del cursor o al final de la nota.

2. **Inspector de Anatomía Universal de Bloque (Panel 1)**:
   - Accesible haciendo clic en el manejador de seis puntos (`⋮⋮`) o mediante `Cmd/Ctrl + /`.
   - Inspección visual interactiva de los 8 controles universales de Notion:
     - **Convertir en (Turn into)**: Párrafo, H1, H2, H3, Lista con viñetas, Lista numerada, Desplegable (Toggle), Cita, Destacado (Callout), Ecuación en bloque.
     - **Color**: Selector de 10 colores de texto y 10 colores de fondo (*Gris, Marrón, Naranja, Amarillo, Verde, Azul, Púrpura, Rosa, Rojo*).
     - **Duplicar (`Ctrl+D`)**: Clona el bloque inmediatamente con nuevo ID y clave de orden.
     - **Mover a (`/movera`)**: Selector rápido para reubicar el bloque dentro del documento o a otra nota.
     - **Copiar enlace al bloque**: Genera el ancla `#block-<id>` para vinculación cruzada.
     - **Eliminar (`Backspace`/`Delete`)**: Borrado seguro con confirmación y sincronización.
     - **Comentar / Sugerir (`Ctrl+Shift+M`)**: Abre el hilo de revisión o modo sugerencia de edición.
     - **Preguntar / Editar con IA**: Dispara herramientas contextuales de reformateo, corrección o síntesis.

3. **Vistas de Bases de Datos Interactivas Embebidas**:
   - Cabecera con selector de vista (Segmented Tabs): `[⊞ Tabla]` `[▥ Tablero]` `[☵ Cronograma]` `[📅 Calendario]` `[☰ Lista]` `[▦ Galería]` `[📊 Gráfico]`.
   - Motor de arrastre drag-and-drop activo entre columnas (To Do, In Progress, Done) en la vista Kanban y reordenamiento de filas en la vista Tabla.
   - Filtros dinámicos por estado, etiquetas y cálculo de propiedades.

#### B. Identidad Visual y Anti-Slop (Tailwind & CSS Tokens)
- **Gama de Neutrales Sofisticados**: Fondo neutro de alta legibilidad (`#0F1115` en modo oscuro, `#F9FAFB` en modo claro), superficies secundarias limpias (`#181A20` / `#FFFFFF`), y bordes capilares sutiles (`1px solid rgba(255, 255, 255, 0.08)` / `rgba(0, 0, 0, 0.08)`).
- **Tipografía**: `Plus Jakarta Sans` para encabezados y controles de catálogo, `JetBrains Mono` con `tabular-nums` para etiquetas de API y atajos de teclado (`<kbd>`).
- **Disciplina Zero-Pill**: Metadatos limpios separados por puntos tipográficos (`·`), sin insignias innecesarias. Botones de acción con proporción horizontal equilibrada (`py-1.5 px-3`).
- **Respeto a la Restricción de Audio y Video**: Eliminación de chips, botones, visores o comandos relacionados con `/video` o `/audio`.

---

### 3. Key Product Decisions & Trade-Offs

- **Decisión 1: Integración del Catálogo en Panel Desplegable (Drawer) con Modo Flotante/Anclado**:
  - *Enfoque*: Implementar un cajón lateral derecho deslizable con transición fluida de $\le 200\text{ms}$ (`transform: translateX`), con opción de anclarlo o cerrarlo rápidamente con `Esc`.
  - *Por qué*: Mantiene el lienzo de escritura despejado mientras permite consultar la anatomía del bloque y explorar todas las opciones sin abandonar la edición.
  - *Alternativa descartada*: Modal centrado grande (bloqueaba el documento e impedía ver dónde aterrizaba el bloque).

- **Decisión 2: Supresión Total de Audio y Video en Toda la Pila**:
  - *Enfoque*: Excluir `audio` y `video` de las definiciones del catálogo (48 bloques en vez de 50), del modal de incrustaciones multimedia (`media-embed-modal`), del menú slash (`/audio`, `/video`), y de los mapeos de tipos de la API.
  - *Por qué*: Cumplimiento estricto de la directiva negativa del usuario.

- **Decisión 3: Arquitectura Híbrida de Renderizado de Bloques y Sincronización SQLite**:
  - *Enfoque*: Cada bloque inyectado posee atributos semánticos `data-block-id`, `data-block-type` y `data-sort-key`. Al modificar cualquier propiedad o reordenar, se actualiza el árbol local y se sincroniza en segundo plano mediante `collectAndSyncNoteBlocks` hacia la tabla `Block` de SQLite.
  - *Por qué*: Asegura persistencia instantánea y compatibilidad offline sin recargar la página.

---

### 4. Technical Architecture & Data Strategy

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Top Navigation & Tabs                           │
│  [🏠 Home]  [Nota 1 ×] [Nota 2 ×]  ...  [⚡ Modo Conc.] [📖 Catálogo]   │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           ▼                                                   ▼
┌──────────────────────────────────────┐  ┌────────────────────────────────────┐
│      Lienzo de Nota (Mac 3-Panel)    │  │    Panel Desplegable Catálogo      │
│  ┌────────────────────────────────┐  │  │  ┌──────────────────────────────┐  │
│  │ ⋮⋮ + Bloque Callout            │  │  │  │ 🔍 Buscar comando / atajo... │  │
│  │    [💡 Aviso importante...]    │  │  │  ├──────────────────────────────┤  │
│  ├────────────────────────────────┤  │  │  │ Familias:                    │  │
│  │ ⋮⋮ + Base de Datos Embebida     │  │  │  │ [Todas] [Básicos] [Línea]... │  │
│  │    [Tabla|Kanban|Cronograma]   │  │  │  ├──────────────────────────────┤  │
│  ├────────────────────────────────┤  │  │  │ Tarjetas Interactivas (48)   │  │
│  │ ⋮⋮ + Ecuación KaTeX / LaTeX    │  │  │  │  - Destacado (Callout)       │  │
│  └────────────────────────────────┘  │  │  │  - Vista Tablero (Kanban)    │  │
│                   │                  │  │  │  - Bloque de Código          │  │
│                   ▼                  │  │  │  - etc. (SIN audio ni video) │  │
│     Inspector Universal (Panel 1)    │  │  └──────────────────────────────┘  │
│   [Turn Into] [Color] [Duplicar]     │  └────────────────────────────────────┘
│   [Mover] [Anchor Link] [Eliminar]   │
└───────────────────┬──────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────────────────────────────┐
│              Sincronización Local & Backend Python + SQLite           │
│    - Tablas: Note, Folder, Block (id, note_id, type, sort_key, text)  │
│    - Reordenamiento fraccional base-62 sin recálculo masivo           │
└───────────────────────────────────────────────────────────────────────┘
```

#### Plan de Archivos a Modificar
1. `frontend/index.html`:
   - Agregar botón de apertura del Catálogo de Bloques (`#btn-top-block-catalog`) en la barra superior.
   - Agregar el panel deslizante `#panel-block-catalog` con buscador, selector de familias arquitectónicas, cuadrícula de tarjetas de bloques (excluyendo audio y video) y la sección de tipos API (30 tipos de objeto).
   - Agregar el menú contextual e inspector de **Anatomía Universal de Bloque (Panel 1)** (`#block-anatomy-inspector`) con controles de conversión, paleta de colores, duplicación y atajos.
   - Eliminar los botones de Video y Audio del modal `#media-embed-modal`.

2. `frontend/styles.css`:
   - Estilos del cajón lateral del catálogo (`.panel-block-catalog`), animaciones de entrada, tarjetas de familias con bordes temáticos sutiles (azul para básicos, cian para en línea, naranja para código/archivos, verde para bases de datos, magenta para incrustaciones, violeta para avanzados, rojo para IA).
   - Estilos del inspector de Anatomía Universal (Panel 1) con diseño oscuro pulido, etiquetas de atajos `<kbd>` y selector de colores.
   - Estilos refinados para todas las vistas de bases de datos embebidas (pestañas de vista, tablero Kanban, tabla, vista de lista).

3. `frontend/app.js`:
   - Registro de datos de los 48 bloques del catálogo con sus atajos, sintaxis markdown, tipo API y descripción.
   - Controlador de apertura y filtrado por familias y búsqueda reactiva en el catálogo.
   - Inserción directa de cualquier bloque al hacer clic en su tarjeta en el catálogo.
   - Implementación de las acciones del Inspector de Anatomía: `turnInto(block, targetType)`, `applyBlockColor(block, textColor, bgColor)`, `duplicateBlock(block)`, `copyBlockAnchor(block)`, `deleteBlock(block)`.
   - Vistas de bases de datos embebidas con conmutador de pestañas de vista y persistencia de tarjetas Kanban y filas de tabla.
   - Eliminación estricta de cualquier manejador o atajo `/audio` o `/video`.

4. `backend.py` y `models.py`:
   - Asegurar soporte en la tabla `Block` y sincronización para todos los nuevos tipos de bloque textuales y de base de datos.
