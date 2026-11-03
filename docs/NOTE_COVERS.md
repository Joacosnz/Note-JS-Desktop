# Portadas compartidas de Note JS

Android y escritorio comparten cinco degradados: `midnight`, `slate`, `forest`, `violet` y `rose`. Se guarda el identificador del diseño, nunca CSS arbitrario ni rutas locales.

Los campos opcionales de Firestore son `hasCover` (booleano), `coverPresetId` (uno de esos IDs), `coverPositionY` (entero de 0 a 100) e `icon` (texto de hasta 32 caracteres). Las notas antiguas siguen siendo válidas. El punto de entrada de escritorio es `frontend/note-cover-contract.mjs`; el de Android es `model/NoteCover.kt`.

En Android, **Elegir foto de portada** aparece antes del título y abre el selector de fotos del sistema. Se puede cambiar o quitar la imagen. La app conserva una copia privada de la foto elegida (hasta 20 MB), por lo que no depende de permisos temporales de la galería ni del archivo original. Se guarda con los demás cambios de la nota al salir del editor.

Las cuadrículas Android y escritorio muestran portada y título cuando la nota tiene portada. Cuando no tiene portada, muestran el título y una vista previa del contenido, sin reservar un espacio para una imagen. Las notas bloqueadas ocultan su contenido, foto y título. En Android la selección continúa disponible con una pulsación prolongada. La vista de lista conserva su comportamiento.

En escritorio, **Elegir foto de portada** y **Cambiar foto** abren el selector de archivos. La imagen se decodifica y prepara a un máximo de 2560 píxeles en su lado más largo. Una copia JPEG se guarda en `attachments/covers/` con un nombre basado en su contenido; SQLite conserva una URL relativa, independiente de la ruta del original y del puerto de la app. No se guardan imágenes grandes en `localStorage`. El encabezado permite cambiar o quitar la portada y la cuadrícula de inicio muestra solo portada y título. La exportación del proyecto incluye los archivos de portada. Las actualizaciones de texto desde Firestore conservan la foto local.

La migración Room 19→20 conserva las portadas anteriores y 20→21 añade `coverImageUri` sin borrar notas. Esta ruta es privada del dispositivo y **no se envía a Firestore**. Las actualizaciones de texto desde la nube conservan la foto local. Las copias ZIP incluyen las fotos en `note_covers/` y el snapshot estructurado guarda su nombre para resolver la ruta al restaurar. La extracción restringe los nombres y el tamaño de las imágenes.

Las fotos funcionan localmente en APK y EXE sin Firebase Storage. **La sincronización de los archivos de portada entre móvil y PC sigue pendiente de habilitar el almacenamiento remoto de adjuntos.** Firestore continúa compartiendo únicamente los metadatos de los degradados anteriores; otro dispositivo puede mostrar ese diseño de respaldo, no la fotografía local.

## Mejoras recomendadas

1. **Contrato de bloques versionado.** Mantener un mismo esquema de tablas, listas, matemáticas y adjuntos, con ejemplos que ambos clientes deban poder leer y volver a guardar. Hoy escritorio usa HTML/campos Notion y Android usa JSON de `NoteBlock`.
2. **Estado de sincronización por nota.** `syncEnabled` indica que la sincronización está activada, pero no confirma que la última edición haya llegado al servidor. Conviene mostrar pendiente, sincronizando, al día y error en los detalles de la nota, manteniendo la cuadrícula limitada a portada y título.
3. **Adjuntos compartidos.** Terminar Firebase Storage para fotos, audio y PDF. Es el requisito previo para sincronizar portadas fotográficas entre móvil y PC.
4. **Migraciones y copias de seguridad.** Añadir pruebas de apertura de bases antiguas y evitar que un camino de migración ausente termine en `fallbackToDestructiveMigration`.

## Reglas de Firebase

Las reglas conservan la separación por UID y validan también los campos de presentación en creación y actualización. Se verificaron valores inválidos en el emulador, sin utilizar las notas reales del usuario.

I've set up prototype Security Rules to keep the data in Firestore safe. They are designed to be secure for private notes owned by the signed-in user, with validated cover identifiers and bounded positions. However, you should review and verify them before broadly sharing your app. If you'd like, I can help you harden these rules.
