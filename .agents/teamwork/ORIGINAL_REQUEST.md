# Original User Request

## Initial Request — 2026-11-02T12:23:25Z

[Message] timestamp=2026-11-02T12:23:25Z sender=5836a6a4-0871-4891-b5f5-63fbf4772424 priority=MESSAGE_PRIORITY_HIGH content=Evaluar e implementar en Note-JS-Desktop las capacidades, protocolo transaccional y tipos de bloques extraídos mediante ingeniería inversa sobre Notion que sirvan a la arquitectura del proyecto, según determine el equipo.

Working directory: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop
Integrity mode: development

## Referencias Técnicas (Análisis REA de Notion)
- Protocolo transaccional de creación atómica: operación concurrente `op.set` (inicialización de bloque con UUIDv4, parent pointers, propiedades, format y CRDT) y `op.listAfter` / `op.insertChildrenAfter` (inserción de UUID en el array `content` del contenedor padre).
- Reglas estructurales del motor:
  - Bloques contenedores (`content: [UUID, ...]`): `text`, `to_do`, `bulleted_list`, `numbered_list`, `toggle`, `page`, `column_list`, `column`, `callout`, `quote`, `table`, etc.
  - Bloques hoja atómicos (`content: null`): `equation`, `divider`, `code`, `image`, `video`, `audio`, `file`, `pdf`, `bookmark`, `table_row`, etc.
  - Encabezados desplegables: `header`, `sub_header`, `sub_sub_header`, `header_4` se convierten en contenedores de hijos si `format.toggleable = true`.
- Catálogo de bloques extraídos:
  - Texto y encabezados: `text`, `header`, `sub_header`, `sub_sub_header`, `header_4`.
  - Listas y tareas: `bulleted_list`, `numbered_list`, `to_do`, `toggle`.
  - Citas y destacados: `quote`, `callout`.
  - Código y matemáticas: `code`, `equation`, `divider`.
  - Estructura y columnas: `page`, `column_list`, `column`.
  - Tablas: `table`, `table_row`.
  - Bloques sincronizados: `transclusion_container`, `transclusion_reference`.
  - Multimedia y archivos: `image`, `video`, `audio`, `file`, `pdf`, `bookmark`.
  - Bases de datos: `collection_view`.

## Requirements

### R1. Protocolo Transaccional y Reglas Estructurales de Creación
Implementar en el backend y modelos de persistencia el protocolo de creación atómica de bloques compuesto por `op.set` (inicialización de bloque con UUIDv4, punteros al contenedor, metadatos y CRDT) y `op.listAfter` / `op.insertChildrenAfter` (registro del UUID en el puntero `content` del contenedor padre).
Aplicar las reglas estructurales del motor de Notion que correspondan a la arquitectura de la aplicación: distinción entre bloques contenedores (`content: [UUID, ...]`) y nodos hoja atómicos (`content: null`), y soporte para encabezados desplegables cuando `format.toggleable = true`.

### R2. Catálogo de Tipos de Bloques Faltantes
Incorporar los tipos de bloques identificados en el análisis inverso de Notion que aporten valor a Note-JS-Desktop (tales como `header_4`, `quote`, `callout`, bloques sincronizados `transclusion_container`/`transclusion_reference`, y tipos multimedia/archivos `video`, `audio`, `file`, `pdf`, `bookmark`), definiendo sus esquemas de inicialización, propiedades y metadatos en `format` según los artefactos extraídos.

### R3. Integración en el Editor y Frontend
Integrar en la interfaz y el editor del frontend (`frontend/`) la visualización, componentes DOM y creación interactiva de los tipos de bloques incorporados, preservando las capacidades de edición y el manejo de rich text en `properties`.

### R4. Preservación de Compatibilidad y Suite de Pruebas
Garantizar que las nuevas adiciones no introduzcan regresiones en las funcionalidades existentes de Note-JS-Desktop, preservando la compatibilidad con el esquema actual de bloques y las notas existentes.

## Verification Resources
El proyecto cuenta con una suite de pruebas automatizadas en `tests/` ejecutable mediante `py -m unittest discover -s tests`.
El equipo debe basarse en esta infraestructura para implementar tests unitarios y de integración para las nuevas funcionalidades.

## Acceptance Criteria

### Schema & Transactional Protocol
- [ ] Atomic block creation executes the concurrent `op.set` (block record initialization with UUIDv4, parent pointers, and format) and `op.listAfter` (updating parent's `content` array) operations in database transactions.
- [ ] The structural rules differentiate container blocks (`content: [...]`) from atomic leaf nodes (`content: null`) as defined by the extracted Notion specifications.
- [ ] Toggleable headers (`header`, `sub_header`, `sub_sub_header`, `header_4`) function as container blocks when `format.toggleable = true`.

### Block Types & Editor
- [ ] Newly integrated block types (including `header_4`, `quote`, `callout`, and others selected by the team from the extracted catalog) initialize with the exact schema, `properties`, and `format` structures defined in the extracted specifications.
- [ ] Integrated block types are renderable and editable within the desktop editor UI (`frontend/`).
- [ ] Text styling and rich-text tuples in `properties.title` remain functional across newly added text-based block types.

### Test Automation & Regression Prevention
- [ ] Automated tests in `tests/` cover the transactional creation operations (`op.set`, `op.listAfter`), container/leaf validation, and newly added block schemas.
- [ ] The complete automated test suite (`py -m unittest discover -s tests`) passes with 100% success and 0 regressions on existing functionality.
