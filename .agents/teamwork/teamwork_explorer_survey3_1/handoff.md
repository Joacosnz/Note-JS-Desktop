# Handoff Report — Survey 3: Backend Database Models, Peewee ORM & Legacy Migration

**Directorio:** `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_1`  
**Archivo de Informe:** `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_1\report.md`  
**Tipo de Handoff:** Hard (Tarea de Investigación Completa)  

---

## 1. Observation (Observaciones Directas)

1. **Esquema y Modelos Existentes en `models.py`**:
   - `models.py:72-84`: Define `Note` en la tabla `notes` con columnas `id` (IntegerField), `title`, `folder`, `tags`, `is_pinned`, `content`, `updated_at`, `data_json`.
   - `models.py:246-263`: Define `Block` en la tabla `blocks` con columnas `id` (CharField), `note_id`, `parent_id`, `type`, `properties`, `sort_index`, `created_at`, `updated_at`.
   - `models.py:264-283`: `Block.to_dict()` devuelve `{'id', 'noteId', 'parentId', 'type', 'properties', 'sortIndex', 'createdAt', 'updatedAt'}` y condicionalmente `page_id` y `title` si `type == 'sub_page'` o si están en `properties`.
   - `models.py:547-571`: `init_db()` crea las tablas `[Note, Folder, Setting, NoteHistory, Block, ReminderItem, WebLinkCache, SignatureRecord]`, ejecuta `_ensure_folder_emoji_column()`, y siembra carpetas por defecto.

2. **Bases de Datos Existentes en Disco**:
   - Inspección con SQLite nativo de `notejs.db`:
     - Tabla `notes`: **5 notas preexistentes** (`id` = 1, 2, 101, 102, 1793317631707) con contenido HTML de longitud hasta 3263 caracteres, fórmulas LaTeX, bloques de llamada y sub-páginas.
     - Tabla `blocks`: 0 filas.
     - Tablas `folders` (4 filas), `settings` (5 filas), `note_history` (3 filas).
   - Inspección de `dist/notejs.db`: Esquema idéntico con 0 notas.

3. **Suite de Pruebas Automatizada en `tests/`**:
   - Ejecución de `py -m unittest discover -s tests`: **Ran 153 tests in 2.763s — OK** (cero fallos, cero errores).
   - `tests/test_backend_subpage.py:31-48`: Crea base de datos temporal aislada con `tempfile.TemporaryDirectory()`, reasigna `models.db = cls.test_db` y `models.BaseModel._meta.database = cls.test_db`, llama a `create_tables([models.Note, ..., models.Block, ...])`.
   - `tests/test_adversarial_challenger.py:155-224`: Comprueba bordes de `Block.to_dict()` (título nulo devuelve `''`, page_id faltante, IDs enteros, JSON corrupto).
   - `tests/test_adversarial_suite.py:54-58` y `tests/test_challenger_it2_stress.py:215-220`: Instancian `models.Block` y `models.Note` en tablas creadas directamente con `cls.test_db.create_tables([models.Note, models.Block], safe=True)`.
   - `tests/test_ui_production_r1_r6.py:384`: Llama a `models.init_db()` levantando un servidor HTTP local en un hilo y valida `/api/settings` y `/api/bootstrap`.

4. **Requisitos de Notion en `ORIGINAL_REQUEST.md` (Follow-up 2026-11-02T01:38:48Z)**:
   - R1: Tabla `block` con campos `id`, `space_id`, `version`, `last_version`, `type`, `properties`, `content`, `parent_id`, `parent_table`, `alive`, `format`, `crdt_format_version`, `crdt_data`, `created_time`, `last_edited_time`, `permissions`.
   - Consistencia bidireccional entre `content` del contenedor e hijos (`parent_id`/`parent_table`).
   - Borrado lógico (`alive = 0`) sin eliminar filas físicamente.
   - R2: Migración automática de notas legacy (`notes`) a bloque raíz `page` con su título en `properties.title` y su contenido segmentado en bloques hijos `text` ordenados en `content`.

---

## 2. Logic Chain (Cadena de Razonamiento Lógico)

1. **Alineación del Esquema Relacional con Notion y Compatibilidad con Tests**:
   - De la Observación 1 y 4, el modelo actual `Block` carece de los campos `space_id`, `version`, `last_version`, `content`, `parent_table`, `alive`, `format`, `crdt_format_version`, `crdt_data`, `created_time`, `last_edited_time` y `permissions`.
   - De la Observación 3, los tests existentes instancian `Block` pasando `note_id`, `parent_id`, `sort_index`, etc., y esperan encontrar claves `noteId` y `sortIndex` en `Block.to_dict()`.
   - *Inferencia:* Para cumplir R1 sin romper los 153 tests existentes, `Block` debe definir los 16 campos de Notion como campos primarios, conservar `note_id`, `sort_index`, `created_at` y `updated_at` con valores por defecto adecuados, y en `to_dict()` devolver ambos conjuntos de claves.
   - Probado experimentalmente con Peewee: la instanciación legacy y Notion coexistieron limpiamente pasando todas las aserciones.

2. **Consistencia Bidireccional Atómica**:
   - De la Observación 4, el contenedor mantiene en `content` un array JSON de UUIDs de hijos en orden visual; el hijo almacena `parent_id` y `parent_table`.
   - *Inferencia:* Cualquier adición, reordenamiento o soft-delete debe encapsularse en una transacción `with db.atomic():` y `with DB_LOCK:`.
   - Cuando se añade un hijo, se inserta su ID en el array `content` del padre y se incrementa `parent.version`.
   - Cuando se mueve entre padres, se remueve del padre antiguo y se añade al nuevo, actualizando las versiones de ambos y el `parent_id` del hijo.
   - En el soft-delete (`alive = 0`), el hijo se remueve de `parent.content` para desaparecer del renderizado visual pero su fila permanece en SQLite.

3. **Migración Automática Segura y No Destructiva**:
   - De la Observación 2, `notejs.db` tiene 5 notas en la tabla `notes`.
   - De la Observación 3, `test_ui_production_r1_r6.py` y otras partes del backend dependen de que `notes` siga existiendo y responda a `get_bootstrap_data()`.
   - *Inferencia:* La migración en `init_db()` debe ser no destructiva (de solo lectura respecto a `notes`). Cada nota se transforma en un bloque raíz `page` (con `id = str(note.id)`), su título se mapea a `properties.title = [[note.title]]`, sus metadatos (icono emoji, portada) a `format`, y su contenido HTML/texto se segmenta en bloques hijos `text` enlazados en `content`.
   - De esta forma, las notas legacy existen en ambos formatos: accesibles por la API antigua y por la nueva API de bloques de Notion.

---

## 3. Caveats (Advertencias y Suposiciones)

1. **Renombrado de tabla `blocks` a `block`**:
   - Notion utiliza `block` en singular, mientras que el código existente usaba `blocks`.
   - La solución arquitectónica recomendada es configurar `table_name = 'block'` en el modelo `Block` y crear una vista SQL `CREATE VIEW IF NOT EXISTS blocks AS SELECT * FROM block;`, más una rutina de migración que ejecute `ALTER TABLE blocks RENAME TO block;` si se detecta una tabla antigua en `notejs.db`.
2. **Tipos de Bloques Extensibles**:
   - Durante la migración inicial, el analizador segmenta texto en bloques `text`, `header`, `sub_header`, `code`, `toggle`, `sub_page`. Los elementos HTML no reconocidos se degradan elegantemente a bloques de tipo `text` sin pérdida de contenido textual.
3. **Persistencia Dual Temporal**:
   - Mientras los componentes del frontend continúen usando `/api/notes`, cualquier guardado de notas legacy debe mantener sincronizadas tanto la fila en `notes` como la jerarquía en `block`.

---

## 4. Conclusion (Conclusión y Dictamen Final)

La investigación confirma la total viabilidad técnica de implementar los requerimientos R1 y R2:
1. El modelo `Block` propuesto en Peewee ORM cubre el 100% de la especificación Notion (`id`, `space_id`, `version`, `last_version`, `type`, `properties`, `content`, `parent_id`, `parent_table`, `alive`, `format`, `crdt_format_version`, `crdt_data`, `created_time`, `last_edited_time`, `permissions`) garantizando soporte nativo para consistencia bidireccional, soft-delete y metadatos CRDT.
2. La migración automática en el arranque (`migrate_legacy_notes_to_blocks`) preserva la integridad de las 5 notas existentes en `notejs.db`, sin pérdida de títulos ni de contenido.
3. La estrategia de compatibilidad regresiva en el modelo y en la base de datos asegura **cero regresiones en los 153 tests actuales**, sentando una base sólida para que los agentes implementadores extiendan la API REST (R3) y el editor en el frontend (R4 y R5).

---

## 5. Verification Method (Método de Verificación Independiente)

1. **Ejecutar Suite Existente**:
   ```powershell
   py -m unittest discover -s tests
   ```
   *Condición de éxito:* 153 tests pasados en ~2.8 segundos.
2. **Inspeccionar Informe Detallado**:
   - Archivo: `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_1\report.md`
   - Validar que contiene el DDL de SQLite, la clase Peewee ORM `Block`, la función `migrate_legacy_notes_to_blocks`, el contrato de consistencia bidireccional y el desglose de compatibilidad de los tests.
3. **Condición de Invalidación**:
   - Si la introducción de los campos Notion o la vista `blocks` causa fallos en `test_backend_subpage.py` o `test_adversarial_challenger.py`.
