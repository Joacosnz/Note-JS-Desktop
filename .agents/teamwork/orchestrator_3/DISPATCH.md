## 2026-11-02T01:40:10Z

Implementar en producción la arquitectura y modelo de datos jerárquico de bloques estilo Notion en Note-JS-Desktop (PyWebView, Python, SQLite con Peewee ORM, frontend vanilla JS/HTML/CSS), asegurando persistencia bidireccional, deserialización y serialización de tuplas de texto enriquecido, metadatos de formato, suite completa de tipos de bloques, migración automática de notas existentes y renderizado interactivo en el editor.

Working directory: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop
Integrity mode: development

## Referencias del Modelo de Bloques (Notion)
- Esquema DDL de bloque: `id` (UUID), `space_id`, `version`, `last_version`, `type`, `properties` (JSON con tuplas de rich text), `content` (JSON con array ordenado de UUIDs de bloques hijos), `parent_id`, `parent_table` ('block', 'collection', 'space'), `alive` (INTEGER 1/0), `format` (JSON con propiedades visuales), `crdt_format_version`, `crdt_data`, `created_time`, `last_edited_time`, `permissions`.
- Representación de rich text en `properties`: array de segmentos con tuplas de decoradores: `[["Texto", [["b"], ["h", "red"], ["i"], ["c"], ["a", url], ["e", latex]]]]`.
- Relación jerárquica bidireccional: el bloque contenedor almacena en `content` los IDs de sus hijos en orden de renderizado visual; cada bloque hijo referencia a su contenedor mediante `parent_id` y `parent_table`.

## Requirements

### R1. Esquema de Base de Datos y Persistencia Bidireccional
Implementar en Peewee ORM y SQLite (`notejs.db`) la tabla de bloques con el esquema completo extraído de Notion (`id`, `space_id`, `version`, `last_version`, `type`, `properties`, `content`, `parent_id`, `parent_table`, `alive`, `format`, `crdt_format_version`, `crdt_data`, `created_time`, `last_edited_time`, `permissions`).
Garantizar la consistencia de los punteros bidireccionales: cuando se añade, reordena o elimina un bloque hijo, se actualiza el array `content` del bloque padre y los campos `parent_id`/`parent_table` del hijo.
El borrado de bloques debe realizarse de forma lógica (`alive = 0`), manteniendo el historial de desvinculación sin eliminar físicamente las filas de la base de datos.
Los campos CRDT (`crdt_data`, `crdt_format_version`) deben persistirse en el esquema y registrar mutaciones y versiones locales para operaciones de edición y preparación de sincronización.

### R2. Migración Automática de Notas Existentes
Proporcionar un mecanismo de migración automática al inicializar la base de datos que detecte las notas preexistentes en `notejs.db` (tablas `note` / `noteblock`) y las transforme en la nueva estructura de bloques jerárquicos:
Cada nota existente se convierte en un bloque raíz de tipo `page`, con su título preservado en `properties.title`, y su contenido dividido y preservado en bloques hijos de tipo `text` referenciados ordenadamente en el array `content` de la página.

### R3. API Backend y Puente Nativo PyWebView
Exponer en `backend.py` (API REST) y en `desktop_app.py` (`window.pywebview.api`) operaciones completas para:
- Crear bloques (con asignación de UUIDv4, punteros de padre y actualización del array `content` del contenedor).
- Consultar un bloque y resolver su subárbol o mapa de registros (`recordMap` con bloques indexados por ID).
- Actualizar propiedades semánticas (`properties`), metadatos visuales (`format`) y versiones de concurrencia.
- Reordenar bloques hijos dentro de un bloque padre (`content`).
- Borrado lógico y restauración de bloques (`alive = 0` / `alive = 1`).

### R4. Suite Completa de Tipos de Bloques y Serialización de Rich Text
Soportar la suite completa de bloques identificada en el análisis:
- Estructurales y de diseño: `page`, `column_list`, `column`, `divider`.
- Texto y formato: `text`, `header`, `sub_header`, `sub_sub_header`, `bulleted_list`, `numbered_list`, `toggle`.
- Datos y código: `code` (con propiedad `language`), `equation` (LaTeX en tupla `["e", latex]`), `table` (con `table_row`, `table_block_column_order`, encabezados en `format`), `collection_view` / `collection_view_page`.
- Multimedia: `image` (con metadatos en `format`: `block_width`, `display_source`, etc.).
Serializar y deserializar fielmente la estructura de rich text en `properties` con soporte de decoradores: negrita (`["b"]`), itálica (`["i"]`), color/resaltado (`["h", color]`), código inline (`["c"]`), enlaces (`["a", url]`) y ecuaciones inline (`["e", latex]`).

### R5. Renderizado Dinámico y Edición en el Frontend
Actualizar el editor en `frontend/` (HTML, CSS, JS vanilla) para renderizar dinámicamente el árbol de bloques a partir del mapa de registros / estructura de datos:
- Cada tipo de bloque debe renderizarse con su componente visual y comportamental correspondiente (incluyendo columnas lado a lado, listas ordenadas/desordenadas, bloques desplegables `toggle`, bloques de código con lenguaje, tablas con filas y columnas, fórmulas y bloques de imagen).
- Interpretar y renderizar los segmentos de texto enriquecido con sus decoraciones visuales correspondientes.
- Permitir la edición interactiva del contenido de los bloques, la inserción de nuevos bloques, el cambio de tipo de bloque y la reorganización de bloques hijos reflejando los cambios hacia el backend.

## Verification Resources
El proyecto cuenta con una suite de pruebas existente en `tests/` con 153 tests (`py -m unittest discover -s tests`).
El equipo debe basarse en y extender esta suite de pruebas, añadiendo tests automatizados para validar el esquema de base de datos, la migración de notas existentes, las operaciones de API de bloques, la serialización/deserialización de tuplas de texto enriquecido y el árbol jerárquico.

## Acceptance Criteria

### Schema & Persistence
- [ ] Database schema includes the full Notion-style `block` table with fields `id`, `space_id`, `version`, `last_version`, `type`, `properties`, `content`, `parent_id`, `parent_table`, `alive`, `format`, `crdt_format_version`, `crdt_data`, `created_time`, `last_edited_time`, and `permissions`.
- [ ] Bidirectional relationships are consistently maintained: child addition, reordering, and removal updates the parent's ordered `content` UUID array and the child's `parent_id` / `parent_table`.
- [ ] Deletion of a block performs a soft delete setting `alive = 0` without removing the record from SQLite.
- [ ] Local CRDT version and mutation metadata are stored and updated upon block edits.

### Data Migration
- [ ] An automated migration runs on startup when legacy note tables exist, converting each existing note into a root `page` block with its title in `properties` and child text blocks referenced in `content`.
- [ ] Existing notes retain all their textual data and titles intact after migration.
- [ ] The full test suite in `tests/` passes without regressions on existing note functionality.

### Backend & API
- [ ] Endpoints or native PyWebView API methods exist to create, fetch (with recordMap / subtree resolution), update (`properties`, `format`), reorder, and soft-delete blocks.
- [ ] Rich text serialization and deserialization correctly handles decorator tuples: bold (`["b"]`), italic (`["i"]`), highlight/color (`["h", color]`), code (`["c"]`), link (`["a", url]`), and inline equations (`["e", latex]`).

### Block Types & Editor Rendering
- [ ] The editor dynamically renders the full suite of block types: `page`, `column_list`, `column`, `divider`, `text`, `header`, `sub_header`, `sub_sub_header`, `bulleted_list`, `numbered_list`, `toggle`, `code`, `equation`, `table`, `table_row`, `collection_view` / `collection_view_page`, and `image`.
- [ ] Rich text formatting tuples in `properties` are accurately rendered with corresponding visual styling in the editor.
- [ ] Column blocks (`column_list`, `column`) render child blocks in side-by-side columns according to the hierarchy.
- [ ] Table blocks (`table`, `table_row`) render rows and columns according to `table_block_column_order` in `format`.
- [ ] New blocks can be created and edited interactively from the UI, persisting updates back to SQLite through the API.

### Test Automation
- [ ] Automated tests added to `tests/` verify block schema creation, CRUD operations, bidirectional parent-child consistency, legacy data migration, and rich-text parsing.
- [ ] All tests execute and pass via `py -m unittest discover -s tests`.
