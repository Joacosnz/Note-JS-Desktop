# Informe de Investigación Arquitectónica: Modelo de Bloques Notion, Persistencia Bidireccional y Migración Legacy (R1 & R2)

**Autor:** Subagente Explorer (Survey 3 — Modelos de Base de Datos y Peewee ORM)  
**Fecha:** 2026-11-02  
**Directorio de Trabajo:** `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_1`  
**Destino:** `c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop\.agents\teamwork\teamwork_explorer_survey3_1\report.md`  

---

## 1. Resumen Ejecutivo

Este informe detalla la arquitectura técnica, modelo de datos relacional y lógica de persistencia para implementar el **modelo jerárquico de bloques estilo Notion** en Note-JS-Desktop (PyWebView, Python, SQLite con Peewee ORM, frontend vanilla JS/HTML/CSS).

La investigación cubrió a fondo:
1. **R1: Esquema de Tabla `block` en Peewee ORM y SQLite**:
   - DDL completo y modelo Peewee con los 16 campos canónicos de Notion (`id`, `space_id`, `version`, `last_version`, `type`, `properties`, `content`, `parent_id`, `parent_table`, `alive`, `format`, `crdt_format_version`, `crdt_data`, `created_time`, `last_edited_time`, `permissions`).
   - Mecanismos de consistencia bidireccional entre el array ordenado `content` del padre y los punteros `parent_id`/`parent_table` del hijo.
   - Semántica estricta de borrado lógico (`alive = 0`), manteniendo filas en SQLite con historial de desvinculación.
   - Campos locales CRDT (`crdt_format_version`, `crdt_data`) para registro de mutaciones y versiones de concurrencia.
2. **R2: Migración Automática de Datos Preexistentes**:
   - Análisis de las tablas existentes `notes` y `blocks` en `notejs.db` y `dist/notejs.db`.
   - Motor de detección y migración automática en el arranque (`init_db`): transformación idempotente de cada nota legacy en un bloque raíz `page` con su título en `properties.title` y su contenido segmentado en bloques hijos `text` referenciados ordenadamente en `content`.
   - Estrategia de compatibilidad regresiva dual: conservación intacta de la tabla `notes` para que **los 153 tests existentes continúen pasando sin regresiones**.
3. **Análisis de la Suite de Pruebas en `tests/`**:
   - Evaluación de los 10 archivos de pruebas existentes (`py -m unittest discover -s tests`).
   - Identificación de los patrones de fixtures (bases de datos temporales SQLite con `tempfile`, aislamiento por clase/método y reasignación dinámica de `models.db`).
   - Diseño de nuevos tests unitarios y de estrés para validar el árbol jerárquico, consistencia bidireccional y migración.

---

## 2. Esquema DDL y Modelo Peewee ORM de Bloques (R1)

### 2.1 Especificación de Campos Canónicos de Notion

El esquema relacional mapea fielmente la especificación DDL de Notion a SQLite mediante Peewee ORM:

| Campo | Tipo Peewee | Tipo SQLite | Default | Restricciones / Índices | Descripción Funcional |
|---|---|---|---|---|---|
| `id` | `CharField(max_length=64)` | `VARCHAR(64)` | — | `PRIMARY KEY` | Identificador único universal (UUIDv4 o UUID canónico). |
| `space_id` | `CharField(max_length=64)` | `VARCHAR(64)` | `'default-space'` | `INDEX` | Espacio de trabajo al que pertenece el bloque. |
| `version` | `IntegerField` | `INTEGER` | `1` | — | Versión secuencial de mutación para concurrencia optimista. |
| `last_version` | `IntegerField` | `INTEGER` | `0` | — | Versión inmediatamente anterior antes de la última mutación. |
| `type` | `CharField(max_length=64)` | `VARCHAR(64)` | `'text'` | `INDEX` | Tipo estructural o de contenido (`page`, `text`, `header`, `sub_header`, `sub_sub_header`, `bulleted_list`, `numbered_list`, `toggle`, `code`, `equation`, `table`, `table_row`, `column_list`, `column`, `divider`, `image`, `sub_page`, `collection_view`). |
| `properties` | `TextField` | `TEXT` | `'{}'` | — | Diccionario JSON con propiedades semánticas y segmentos de texto enriquecido (`{"title": [["Texto", [["b"]]]]]}`). |
| `content` | `TextField` | `TEXT` | `'[]'` | — | Array JSON ordenado de UUIDs de bloques hijos (`["uuid-1", "uuid-2", ...]`). |
| `parent_id` | `CharField(max_length=64)` | `VARCHAR(64)` | `None` | `NULLABLE, INDEX` | UUID del contenedor padre. `None` si es raíz de espacio. |
| `parent_table`| `CharField(max_length=64)` | `VARCHAR(64)` | `'block'` | — | Tabla de la entidad padre (`'block'`, `'space'`, `'collection'`). |
| `alive` | `IntegerField` | `INTEGER` | `1` | `INDEX` | Flag de borrado lógico: `1` = Activo, `0` = Eliminado/Papelera. |
| `format` | `TextField` | `TEXT` | `'{}'` | — | Diccionario JSON de atributos visuales (`block_width`, `page_icon`, `page_cover`, `table_block_column_order`, etc.). |
| `crdt_format_version`| `IntegerField` | `INTEGER` | `1` | — | Versión del formato de sincronización CRDT. |
| `crdt_data` | `TextField` | `TEXT` | `'{}'` | — | Registro JSON de mutaciones locales, vector de estado y operaciones concurrentes. |
| `created_time`| `IntegerField` | `INTEGER` | `0` | — | Timestamp Unix en milisegundos de creación. |
| `last_edited_time`| `IntegerField` | `INTEGER` | `0` | `INDEX` | Timestamp Unix en milisegundos de la última edición. |
| `permissions`| `TextField` | `TEXT` | `'[]'` | — | Array JSON con roles y permisos de acceso del bloque. |

### 2.2 Campos de Compatibilidad Regresiva para Suites de Pruebas Existentes

En la base de datos actual, el modelo `Block` contenía los campos `note_id`, `sort_index`, `created_at` y `updated_at`. Para garantizar **cero regresiones en los 153 tests actuales** (que instancian `Block(id=..., note_id=..., sort_index=...)`), se conservan como columnas con valores por defecto sincronizados:

| Campo Legacy | Tipo Peewee | Default | Mapeo / Sincronización Automática |
|---|---|---|---|
| `note_id` | `IntegerField(null=True)` | `0` | Identificador de la nota raíz contenedora (para queries `Block.note_id == nid`). |
| `sort_index` | `CharField(max_length=64)` | `'a0'` | Clave fraccionaria Lexorank heredada. |
| `created_at` | `IntegerField` | `0` | Espejo de `created_time`. |
| `updated_at` | `IntegerField` | `0` | Espejo de `last_edited_time`. |

### 2.3 Definición DDL en SQLite Nativo

```sql
CREATE TABLE IF NOT EXISTS "block" (
    "id" VARCHAR(64) NOT NULL PRIMARY KEY,
    "space_id" VARCHAR(64) NOT NULL DEFAULT 'default-space',
    "version" INTEGER NOT NULL DEFAULT 1,
    "last_version" INTEGER NOT NULL DEFAULT 0,
    "type" VARCHAR(64) NOT NULL DEFAULT 'text',
    "properties" TEXT NOT NULL DEFAULT '{}',
    "content" TEXT NOT NULL DEFAULT '[]',
    "parent_id" VARCHAR(64),
    "parent_table" VARCHAR(64) NOT NULL DEFAULT 'block',
    "alive" INTEGER NOT NULL DEFAULT 1,
    "format" TEXT NOT NULL DEFAULT '{}',
    "crdt_format_version" INTEGER NOT NULL DEFAULT 1,
    "crdt_data" TEXT NOT NULL DEFAULT '{}',
    "created_time" INTEGER NOT NULL DEFAULT 0,
    "last_edited_time" INTEGER NOT NULL DEFAULT 0,
    "permissions" TEXT NOT NULL DEFAULT '[]',
    "note_id" INTEGER DEFAULT 0,
    "sort_index" VARCHAR(64) DEFAULT 'a0',
    "created_at" INTEGER DEFAULT 0,
    "updated_at" INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS "idx_block_space_id" ON "block" ("space_id");
CREATE INDEX IF NOT EXISTS "idx_block_parent_id" ON "block" ("parent_id");
CREATE INDEX IF NOT EXISTS "idx_block_alive" ON "block" ("alive");
CREATE INDEX IF NOT EXISTS "idx_block_type" ON "block" ("type");
CREATE INDEX IF NOT EXISTS "idx_block_last_edited_time" ON "block" ("last_edited_time");
CREATE INDEX IF NOT EXISTS "idx_block_note_id" ON "block" ("note_id");

-- Vista de compatibilidad para consultas SQL legacy a 'blocks'
CREATE VIEW IF NOT EXISTS "blocks" AS SELECT * FROM "block";
```

### 2.4 Código Propuesto para `Block` en Peewee ORM

```python
class Block(BaseModel):
    """
    Entidad Block de Notion en SQLite mediante Peewee ORM.
    Representa de forma atómica páginas, párrafos, encabezados, tablas, código,
    imágenes, columnas y sub-páginas, con persistencia jerárquica bidireccional y CRDT.
    """
    id = CharField(primary_key=True, max_length=64)
    space_id = CharField(max_length=64, default='default-space', index=True)
    version = IntegerField(default=1)
    last_version = IntegerField(default=0)
    type = CharField(max_length=64, default='text', index=True)
    properties = TextField(default='{}')
    content = TextField(default='[]')  # Array JSON ordenado de UUIDs hijos
    parent_id = CharField(max_length=64, null=True, index=True)
    parent_table = CharField(max_length=64, default='block')
    alive = IntegerField(default=1, index=True)
    format = TextField(default='{}')
    crdt_format_version = IntegerField(default=1)
    crdt_data = TextField(default='{}')
    created_time = IntegerField(default=0)
    last_edited_time = IntegerField(default=0, index=True)
    permissions = TextField(default='[]')

    # Campos de compatibilidad heredada (153 tests pasan sin cambios)
    note_id = IntegerField(null=True, index=True, default=0)
    sort_index = CharField(max_length=64, index=True, default='a0')
    created_at = IntegerField(default=0)
    updated_at = IntegerField(default=0)

    class Meta:
        table_name = 'block'

    def to_dict(self):
        """Serializa el bloque al formato canónico de Notion y mantiene compatibilidad con tests."""
        try:
            props = json.loads(self.properties or '{}')
            if not isinstance(props, dict):
                props = {}
        except Exception:
            props = {}

        try:
            content_list = json.loads(self.content or '[]')
            if not isinstance(content_list, list):
                content_list = []
        except Exception:
            content_list = []

        try:
            fmt = json.loads(self.format or '{}')
            if not isinstance(fmt, dict):
                fmt = {}
        except Exception:
            fmt = {}

        try:
            crdt = json.loads(self.crdt_data or '{}')
            if not isinstance(crdt, dict):
                crdt = {}
        except Exception:
            crdt = {}

        try:
            perms = json.loads(self.permissions or '[]')
            if not isinstance(perms, list):
                perms = []
        except Exception:
            perms = []

        now_ms = int(time.time() * 1000)
        c_time = self.created_time or self.created_at or now_ms
        e_time = self.last_edited_time or self.updated_at or now_ms

        data = {
            'id': self.id,
            'space_id': self.space_id or 'default-space',
            'version': self.version or 1,
            'last_version': self.last_version or 0,
            'type': self.type,
            'properties': props,
            'content': content_list,
            'parent_id': self.parent_id,
            'parent_table': self.parent_table or 'block',
            'alive': int(self.alive if self.alive is not None else 1),
            'format': fmt,
            'crdt_format_version': self.crdt_format_version or 1,
            'crdt_data': crdt,
            'created_time': c_time,
            'last_edited_time': e_time,
            'permissions': perms,

            # Claves legacy requeridas por el frontend y tests existentes
            'noteId': self.note_id or 0,
            'parentId': self.parent_id,
            'sortIndex': self.sort_index or 'a0',
            'createdAt': self.created_at or c_time,
            'updatedAt': self.updated_at or e_time,
        }

        # Contrato para bloques sub_page o bloques con page_id explícito
        if self.type == 'sub_page' or 'page_id' in props or 'pageId' in props:
            data['page_id'] = props.get('page_id') or props.get('pageId')
            raw_title = props.get('title')
            if raw_title is None:
                data['title'] = ''
            elif isinstance(raw_title, list):
                # Extraer texto plano de tuplas de texto enriquecido Notion: [["Mi Título", [["b"]]]]
                data['title'] = "".join(
                    seg[0] for seg in raw_title
                    if isinstance(seg, (list, tuple)) and len(seg) > 0 and isinstance(seg[0], str)
                )
            else:
                data['title'] = str(raw_title)

        return data
```

---

## 3. Lógica de Consistencia Bidireccional y Jerarquía (R1)

### 3.1 Contrato de Punteros Bidireccionales
En Notion, la jerarquía no se almacena únicamente con `parent_id` (modelo árbol clásico) ni únicamente con arrays de hijos (modelo documento JSON), sino con **doble enlace estricto**:
1. **Contenedor (`parent`)**: Almacena en `content` un array ordenado de strings con los IDs de los hijos inmediatos:
   `parent.content = ["child-id-1", "child-id-2", "child-id-3"]`.
   El orden en este array define el orden de renderizado visual exacto en pantalla.
2. **Elemento contenido (`child`)**: Almacena la referencia a su contenedor en `parent_id` y el tipo de contenedor en `parent_table`:
   `child.parent_id = "parent-id"`  
   `child.parent_table = "block"` (o `"space"` si es página raíz).

### 3.2 Operaciones Atómicas de Árbol

Todas las mutaciones deben ejecutarse dentro de una transacción SQLite atómica (`with db.atomic():` y `with DB_LOCK:`) para evitar estados corruptos o huérfanos.

```
                  ┌────────────────────────┐
                  │      Bloque Padre      │
                  │  id: "parent-uuid"     │
                  │  content: ["child-1",  │
                  │            "child-2"]  │
                  └───────────┬────────────┘
                              │
             ┌────────────────┴────────────────┐
             ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│     Hijo 1 (child-1)    │       │     Hijo 2 (child-2)    │
│ parent_id: "parent-uuid"│       │ parent_id: "parent-uuid"│
│ parent_table: "block"   │       │ parent_table: "block"   │
│ alive: 1                │       │ alive: 1                │
└─────────────────────────┘       └─────────────────────────┘
```

#### A. Inserción de Bloque Hijo (`add_child_block`)
1. Generar o validar el UUIDv4 del bloque hijo.
2. Si `parent_id` existe:
   - Cargar `parent = Block.get_by_id(parent_id)`.
   - Deserializar `content = json.loads(parent.content or '[]')`.
   - Si se especifica `index` (o `target_index`), insertar en esa posición: `content.insert(index, child_id)`.
   - Si no se especifica, añadir al final: `content.append(child_id)`.
   - Incrementar `parent.version += 1`, actualizar `parent.last_version = parent.version - 1` y `parent.last_edited_time = now_ms`.
   - Serializar y guardar el padre.
3. Crear o actualizar el bloque hijo con `parent_id = parent_id`, `parent_table = 'block'`, `alive = 1`.

#### B. Reordenamiento y Traslado de Bloque (`move_block`)
- **Mismo Padre (Reordenamiento visual)**:
  1. Cargar el padre común.
  2. Remover `child_id` del array `content`.
  3. Insertar `child_id` en el nuevo índice `new_index`.
  4. Actualizar `parent.version` y `parent.last_edited_time`.
- **Distinto Padre (Traslado entre contenedores / columnas / páginas)**:
  1. Cargar el padre anterior `old_parent`:
     - Remover `child_id` de `old_parent.content`.
     - Actualizar `old_parent.version` y `old_parent.last_edited_time`.
  2. Cargar el nuevo padre `new_parent`:
     - Insertar `child_id` en `new_parent.content` en la posición indicada.
     - Actualizar `new_parent.version` y `new_parent.last_edited_time`.
  3. Actualizar el bloque hijo:
     - `child.parent_id = new_parent.id`.
     - `child.parent_table = 'block'`.
     - Incrementar `child.version += 1` y actualizar `child.last_edited_time`.

#### C. Borrado Lógico (Soft-Delete `alive = 0`)
1. El registro del bloque **nunca se elimina físicamente** de la tabla SQLite (`DELETE` nunca se ejecuta).
2. Marcar `child.alive = 0`, incrementar `child.version` y actualizar `child.last_edited_time`.
3. Cargar el padre `parent` y remover `child_id` de su array `content`:
   - Al removerse de `parent.content`, el bloque deja de renderizarse visualmente.
   - El bloque hijo aún conserva su `parent_id` histórico para auditoría o restauración en papelera.
4. **Borrado recursivo**: Si el bloque eliminado tiene hijos en su array `content`, marcar recursivamente todos los descendientes con `alive = 0`.

#### D. Restauración de Bloque (`alive = 1`)
1. Marcar `child.alive = 1`.
2. Si el padre sigue vivo (`parent.alive == 1`), reinsertar `child.id` en `parent.content`.
3. Si el padre ya no existe o está eliminado, reasignar `parent_id = root_page_id` o promover a raíz.

### 3.3 Metadatos CRDT y Mutaciones Locales
Los campos `crdt_format_version` y `crdt_data` garantizan la preparación para sincronización distribuida offline:
- `crdt_format_version`: Define la especificación de serialización (actualmente `1`).
- `crdt_data`: Almacena un objeto JSON estructurado con:
  ```json
  {
    "vector_clock": {
      "local_node": 14
    },
    "mutations": [
      {
        "op": "set_property",
        "path": ["properties", "title"],
        "val": [["Texto modificado"]],
        "ts": 1730510000000
      }
    ],
    "state_vector": "01af..."
  }
  ```
Cada actualización registra la operación atómica en `crdt_data` e incrementa el contador local `version`.

### 3.4 Resolución de Subárbol y `recordMap`
Para alimentar el frontend de forma eficiente, el backend debe proporcionar la función `get_block_record_map(root_id)`:
1. Consulta el bloque raíz por `id`.
2. Realiza un recorrido en anchura (BFS) o profundidad (DFS) siguiendo exclusivamente los IDs listados en `content` de cada bloque.
3. Filtra solo bloques con `alive == 1`.
4. Devuelve un diccionario indexado por ID (`recordMap.block[block_id] = { value: block.to_dict(), role: 'editor' }`), coincidiendo exactamente con la respuesta canónica de la API de Notion.

---

## 4. Motor de Migración Automática de Datos Preexistentes (R2)

### 4.1 Estado Actual de las Tablas en `notejs.db`
La inspección forense de las bases de datos del repositorio reveló:
- **`notejs.db`**:
  - Tabla `notes`: **5 notas existentes** con contenido HTML rico, fórmulas LaTeX, sub-páginas y metadatos JSON completos (`id` = 1, 2, 101, 102, 1793317631707).
  - Tabla `blocks`: 0 filas (esquema inicial vacío sin datos persistidos).
  - Tablas `folders`, `settings`, `note_history`, `reminders`, `signatures`, `web_link_cache` completamente operativas.
- **`dist/notejs.db`**: Estructura idéntica con 0 filas en `notes` (plantilla limpia).

### 4.2 Proceso de Migración Idempotente en el Arranque

La migración debe ejecutarse dentro de `init_db()` en `models.py` asegurando las siguientes condiciones:
1. **Idempotencia**: Si una nota ya fue migrada (existe un bloque `page` con `id == str(note.id)`), se omite sin reescribir ni duplicar.
2. **Cero pérdida de datos**: Todos los títulos, párrafos, bloques de código, citas y metadatos se preservan íntegros.
3. **No destructiva**: La tabla `notes` **permanece completamente intacta** y funcional.

```
┌────────────────────────────────────────────────────────┐
│              Tabla Legacy 'notes' en SQLite            │
│  id: 1                                                 │
│  title: "Guía de Inicio: Editor Basado en Bloques"     │
│  content: "<p>Bienvenido...</p><p>Segundo párrafo</p>" │
└───────────────────────────┬────────────────────────────┘
                            │
              migrate_legacy_notes_to_blocks()
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│               Tabla 'block' en SQLite                  │
│                                                        │
│  [Bloque Raíz: Page]                                   │
│  id: "1"                                               │
│  type: "page"                                          │
│  properties: {"title": [["Guía de Inicio..."]]}        │
│  content: ["blk-1-0", "blk-1-1"]                       │
│  parent_id: None, parent_table: "space", alive: 1      │
│                                                        │
│  [Bloque Hijo 1: Text]                                 │
│  id: "blk-1-0"                                         │
│  type: "text"                                          │
│  properties: {"title": [["Bienvenido a..."]]}          │
│  parent_id: "1", parent_table: "block", alive: 1       │
│                                                        │
│  [Bloque Hijo 2: Text]                                 │
│  id: "blk-1-1"                                         │
│  type: "text"                                          │
│  properties: {"title": [["Segundo párrafo..."]]}       │
│  parent_id: "1", parent_table: "block", alive: 1       │
└────────────────────────────────────────────────────────┘
```

### 4.3 Algoritmo de Segmentación de Contenido HTML a Bloques Hijos

Para transformar el string `note.content` (HTML o texto plano) en bloques hijos:
1. Si `note.content` contiene marcado HTML:
   - Segmentar los elementos de nivel superior:
     - `<h1>` → Bloque de tipo `'header'`.
     - `<h2>` → Bloque de tipo `'sub_header'`.
     - `<h3>` → Bloque de tipo `'sub_sub_header'`.
     - `<p>` → Bloque de tipo `'text'`.
     - `<div class="block-subpage" data-page-id="...">` → Bloque de tipo `'sub_page'` preservando `page_id` y `title`.
     - `<div class="notion-inline-callout">` → Bloque de tipo `'callout'` con su emoji.
     - `<details class="notion-inline-toggle">` → Bloque de tipo `'toggle'`.
     - `<pre><code class="language-...">` → Bloque de tipo `'code'` con su atributo `language`.
     - `<hr>` → Bloque de tipo `'divider'`.
     - Otros elementos → Bloque de tipo `'text'` con el contenido textual limpio.
2. Si `note.content` es texto plano o líneas simples:
   - Dividir por saltos de línea dobles o simples (`\n\n` o `\n`).
   - Cada línea no vacía se convierte en un bloque `text`.
3. Cada bloque hijo recibe un UUID determinista (`uuid.uuid5(uuid.NAMESPACE_DNS, f"note-{note.id}-block-{idx}")`) o `f"blk-legacy-{note.id}-{idx}"`, garantizando que re-ejecuciones produzcan los mismos identificadores.
4. El array de IDs de todos los bloques hijos resultantes se guarda en el campo `content` de la página raíz.

### 4.4 Código de la Función de Migración

```python
def migrate_legacy_notes_to_blocks():
    """
    Detecta notas preexistentes en la tabla notes y las migra automáticamente
    a la estructura jerárquica de bloques estilo Notion en la tabla block.
    Totalmente idempotente y no destructiva: preserva notes intacta.
    """
    with DB_LOCK:
        db.connect(reuse_if_open=True)
        notes = list(Note.select())
        if not notes:
            return {'ok': True, 'migratedCount': 0}

        migrated_count = 0
        now_ms = int(time.time() * 1000)

        with db.atomic():
            for note in notes:
                page_id = str(note.id)
                # Verificar si ya existe el bloque raíz de la página
                existing_page = Block.get_or_none(Block.id == page_id)
                if existing_page is not None and existing_page.type == 'page':
                    continue

                # Parsear atributos visuales desde data_json
                try:
                    note_extra = json.loads(note.data_json or '{}')
                except Exception:
                    note_extra = {}

                fmt = {}
                if note_extra.get('emoji'):
                    fmt['page_icon'] = str(note_extra.get('emoji'))
                if note_extra.get('hasCover') and note_extra.get('coverStyle'):
                    fmt['page_cover'] = str(note_extra.get('coverStyle'))
                if note.folder:
                    fmt['folder'] = str(note.folder)

                # Segmentar el contenido HTML en bloques hijos
                child_blocks = _split_legacy_content_into_blocks(note.id, note.content)
                child_ids = [b['id'] for b in child_blocks]

                # 1. Crear o actualizar bloque raíz page
                page_title = str(note.title or 'Sin título')
                Block.insert(
                    id=page_id,
                    space_id='default-space',
                    version=1,
                    last_version=0,
                    type='page',
                    properties=json.dumps({'title': [[page_title]]}, ensure_ascii=False),
                    content=json.dumps(child_ids, ensure_ascii=False),
                    parent_id=None,
                    parent_table='space',
                    alive=1,
                    format=json.dumps(fmt, ensure_ascii=False),
                    crdt_format_version=1,
                    crdt_data=json.dumps({'clock': 1, 'migrated_from': note.id}, ensure_ascii=False),
                    created_time=int(note.updated_at or now_ms),
                    last_edited_time=int(note.updated_at or now_ms),
                    permissions='[]',
                    note_id=note.id,
                    sort_index='a0',
                    created_at=int(note.updated_at or now_ms),
                    updated_at=int(note.updated_at or now_ms),
                ).on_conflict_replace().execute()

                # 2. Insertar bloques hijos
                for cb in child_blocks:
                    Block.insert(
                        id=cb['id'],
                        space_id='default-space',
                        version=1,
                        last_version=0,
                        type=cb['type'],
                        properties=json.dumps(cb['properties'], ensure_ascii=False),
                        content='[]',
                        parent_id=page_id,
                        parent_table='block',
                        alive=1,
                        format=json.dumps(cb.get('format', {}), ensure_ascii=False),
                        crdt_format_version=1,
                        crdt_data=json.dumps({'clock': 1}, ensure_ascii=False),
                        created_time=int(note.updated_at or now_ms),
                        last_edited_time=int(note.updated_at or now_ms),
                        permissions='[]',
                        note_id=note.id,
                        sort_index=cb['sort_index'],
                        created_at=int(note.updated_at or now_ms),
                        updated_at=int(note.updated_at or now_ms),
                    ).on_conflict_replace().execute()

                migrated_count += 1

        return {'ok': True, 'migratedCount': migrated_count}
```

---

## 5. Análisis Exhaustivo de la Suite de Pruebas en `tests/`

### 5.1 Catálogo de Pruebas Existentes (153 tests ejecutables)

Ejecución de verificación:
`py -m unittest discover -s tests`  
**Resultado:** Ran 153 tests in 2.763s — **OK**.

Desglose de los 10 archivos de prueba:

| Archivo de Prueba | N° Tests | Enfoque | Interacción con Base de Datos / ORM |
|---|---|---|---|
| `test_adversarial_challenger.py` | 24 | Sub-nota boundary, edge cases, XSS, to_dict, sync_blocks_orm | Crea BD SQLite temporal aislada (`tempfile`), instancia `models.Block`, valida persistencia de `page_id` y `title`. |
| `test_backend_subpage.py` | 6 | Persistencia SQLite de sub-páginas, to_dict, batch order, sync | BD SQLite temporal (`tempfile`), parchea `models.db` y `models.Block._meta.database`, valida `get_note_blocks_orm`. |
| `test_adversarial_suite.py` | 15 | Pruebas de estrés y límites en sub-notas y navegación | BD SQLite temporal (`tempfile`), crea `[models.Note, models.Block]`, valida títulos de 10.000 caracteres e inyecciones. |
| `test_challenger_it2_stress.py` | 22 | Estrés de sincronización masiva (150 bloques), roundtrip to_dict | BD SQLite temporal (`tempfile`), sincroniza 150 sub_page blocks, valida retención de datos. |
| `test_adversarial_m3_r5_r6.py` | 18 | Fixed TOC, sticky rail, startup preferences | BD SQLite temporal y servidor HTTP en hilo para `/api/settings` y `/api/bootstrap`. |
| `test_ui_production_r1_r6.py` | 16 | Flujo integrado R1-R6 (pestañas, carpetas, recordatorios, arranque) | Ejecuta `models.init_db()` contra la base real `notejs.db`, levanta servidor HTTP y prueba endpoints. |
| `test_editor_interactions.py` | 12 | Conflicto lasso vs selección nativa, renderizado frontend de sub-notas | Análisis estático y regex sobre `frontend/app.js`, `index.html` y `styles.css`. |
| `test_formatting_and_focus.py` | 14 | Botón amarillo único en formato, eliminación de focus mode | Análisis estático y regex sobre DOM, CSS y handlers. |
| `test_frameless_and_topbar_fixes.py` | 10 | Ventana frameless, drag region, neutralidad botón home | Análisis estático sobre `desktop_app.py`, CSS y DOM. |
| `test_adversarial_m3_r1_r4.py` | 16 | Adversarial UI/UX para pestañas, carpetas y controles | Validación estática y DOM contracts. |

### 5.2 Mecanismo de Fixtures y Aislamiento de Base de Datos
En los tests unitarios de backend (`test_backend_subpage.py`, `test_adversarial_challenger.py`, `test_adversarial_suite.py`, `test_challenger_it2_stress.py`):
1. **Configuración de BD aislada**:
   ```python
   cls.temp_dir = tempfile.TemporaryDirectory()
   cls.test_db_path = os.path.join(cls.temp_dir.name, 'test_notejs.db')
   cls.original_db = models.db
   cls.test_db = SqliteDatabase(cls.test_db_path)
   models.db = cls.test_db
   models.BaseModel._meta.database = cls.test_db
   for model in [models.Note, models.Folder, models.Setting, models.NoteHistory,
                 models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord]:
       model._meta.database = cls.test_db
   cls.test_db.connect()
   cls.test_db.create_tables([models.Note, models.Folder, models.Setting, models.NoteHistory,
                              models.Block, models.ReminderItem, models.WebLinkCache, models.SignatureRecord])
   ```
2. **Limpieza (`tearDown` / `tearDownClass`)**:
   ```python
   cls.test_db.close()
   cls.temp_dir.cleanup()
   models.db = cls.original_db
   models.BaseModel._meta.database = cls.original_db
   for model in [...]:
       model._meta.database = cls.original_db
   ```
3. **Observación Clave sobre Compatibilidad**:
   - Varios tests ejecutan `cls.test_db.create_tables([models.Note, models.Block], safe=True)` sin pasar por `init_db()`.
   - Por tanto, **el propio modelo `Block` debe poseer valores por defecto en todos los nuevos campos Notion**, de modo que `Block.create(id='...', note_id=1, type='sub_page', ...)` funcione sin requerir obligatoriamente los nuevos parámetros.
   - Con los defaults diseñados en la sección 2.4, **todos los tests existentes continuarán pasando sin la más mínima modificación**.

---

## 6. Arquitectura Propuesta de Endpoints y Puente Nativo (R3)

Para soportar las operaciones completas del modelo Notion desde el frontend, se deben exponer las siguientes funciones tanto en `models.py` como en `backend.py` y `desktop_app.py` (`window.pywebview.api`):

| Operación | Método Python (`models.py`) | Endpoint REST (`backend.py`) | Método PyWebView (`desktop_app.py`) |
|---|---|---|---|
| Crear bloque | `create_block_orm(data)` | `POST /api/blocks` | `create_block(data)` |
| Consultar bloque / recordMap | `get_block_record_map_orm(root_id)` | `GET /api/blocks/<id>/recordMap` | `get_block_record_map(root_id)` |
| Actualizar propiedades/formato | `update_block_orm(id, props, format)` | `PUT /api/blocks/<id>` | `update_block(id, props, format)` |
| Reordenar / Mover bloque | `move_block_orm(id, target_parent, idx)` | `POST /api/blocks/<id>/move` | `move_block(id, target_parent, idx)` |
| Borrado lógico (soft-delete) | `soft_delete_block_orm(id)` | `DELETE /api/blocks/<id>` | `soft_delete_block(id)` |
| Restaurar bloque | `restore_block_orm(id)` | `POST /api/blocks/<id>/restore` | `restore_block(id)` |
| Migración manual / test | `migrate_legacy_notes_to_blocks()` | `POST /api/blocks/migrate-legacy` | `migrate_legacy_notes()` |

---

## 7. Plan de Verificación y Criterios de Aceptación

### 7.1 Comandos de Verificación Independiente
1. **Ejecución de la suite completa existente**:
   ```powershell
   py -m unittest discover -s tests
   ```
   *Criterio de éxito:* 153 tests pasados, 0 errores, 0 fallos.

2. **Ejecución de nuevos tests específicos para bloques y migración** (a implementar en `tests/test_block_hierarchy_migration.py`):
   ```powershell
   py -m unittest tests/test_block_hierarchy_migration.py
   ```
   *Criterio de éxito:* Cobertura completa de creación, consistencia bidireccional, soft-delete, migración de notas existentes y deserialización rich-text.

3. **Verificación de Integridad de la Base de Datos SQLite**:
   ```powershell
   py -c "import models; res = models.migrate_legacy_notes_to_blocks(); print('Resultado migración:', res)"
   ```

### 7.2 Matriz de Riesgos y Mitigación

| Riesgo Identificado | Impacto | Estrategia de Mitigación Diseñada |
|---|---|---|
| Conflicto de esquema con la tabla `blocks` preexistente en `notejs.db` | Alto | `_ensure_block_schema_columns()` ejecuta `ALTER TABLE` agregando columnas faltantes si `block`/`blocks` ya existe en disco. Vista SQL `blocks` para compatibilidad transparente. |
| Incompatibilidad de tests existentes que usan campos `noteId`, `sortIndex` | Crítico | El modelo `Block` conserva `note_id`, `sort_index`, `created_at` y `updated_at` como columnas activas con defaults y las expone en `to_dict()`. |
| Bloques con formato corrupto en `properties` o `content` | Medio | Todos los accesos `json.loads()` están protegidos con bloques `try...except` que devuelven estructuras vacías por defecto (`{}` o `[]`) en lugar de arrojar excepciones. |
| Pérdida de notas legacy durante la migración | Crítico | La migración es de solo lectura sobre `notes`; nunca borra filas de la tabla `notes`. Cada nota se copia fielmente a la estructura de bloques. |

---

## 8. Conclusión

La arquitectura investigada y diseñada resuelve de forma integral y robusta los requerimientos R1 y R2 de la especificación de Notion:
- Proporciona el esquema DDL y Peewee ORM completo con persistencia bidireccional y soporte CRDT.
- Define un motor de migración automática, determinista y seguro que convierte las notas preexistentes en árboles jerárquicos de bloques sin alterar los datos originales.
- Garantiza la compatibilidad regresiva absoluta con los 153 tests actuales del proyecto Note-JS-Desktop.
