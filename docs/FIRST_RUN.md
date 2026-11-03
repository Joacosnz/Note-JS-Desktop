# Primera instalación de Note JS

Las instalaciones nuevas de Android y Windows comienzan con tres notas editables en **Primeros pasos**:

1. **Bienvenido a Note JS**: escribir a tu ritmo y trabajar sin conexión.
2. **Tu primera nota**: crear notas, usar bloques y elegir una foto de portada.
3. **Organizá tu espacio**: carpetas, búsqueda, papelera, sincronización y copias.

El catálogo compartido es `welcome_notes.json`. Android incluye una copia idéntica en sus assets; ambos clientes adaptan las instrucciones a sus controles. Las guías no tienen portadas ficticias. El calendario de escritorio usa el día actual y comienza sin recordatorios de ejemplo.

En Windows, `onboarding.initialize_first_run()` crea las notas y el marcador de primera ejecución en una misma transacción SQLite. Se ejecuta al arrancar la app nativa o el servidor. Una biblioteca que ya contiene notas, recordatorios o ajustes conserva su contenido. La base de datos es la fuente de datos al iniciar, incluso cuando está vacía, para evitar recuperar notas borradas desde la caché del navegador.

En Android, las guías se insertan en una transacción solo si la biblioteca está vacía y la preferencia de primera ejecución sigue activa. Después se marca la bienvenida como completada. Son locales por defecto para evitar subir automáticamente tutoriales a la cuenta. Se retiró la limpieza antigua que borraba notas por coincidencia de título.

Las actualizaciones conservan las bibliotecas existentes. Esta preparación no restablece los datos del desarrollador, del móvil ni de Firebase.

## Paquetes limpios

El ejecutable incluye código, recursos estáticos y el catálogo de bienvenida. El instalador copia únicamente el ejecutable y el icono. No se empaquetan `notejs.db`, adjuntos personales, perfiles WebView, sesiones ni historiales de prueba. El APK incluye el catálogo y recursos de la app; sus datos se generan en el almacenamiento privado al abrirlo.

El APK de depuración sirve para probar esta experiencia. La publicación en una tienda requiere el flujo de firma de producción correspondiente.
