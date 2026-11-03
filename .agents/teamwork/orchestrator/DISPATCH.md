# Dispatch History

## 2026-11-02T12:23:25Z
From: 5836a6a4-0871-4891-b5f5-63fbf4772424
Content:
Evaluar e implementar en Note-JS-Desktop las capacidades, protocolo transaccional y tipos de bloques extraídos mediante ingeniería inversa sobre Notion que sirvan a la arquitectura del proyecto, según determine el equipo.

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
### R2. Catálogo de Tipos de Bloques Faltantes
### R3. Integración en el Editor y Frontend
### R4. Preservación de Compatibilidad y Suite de Pruebas
