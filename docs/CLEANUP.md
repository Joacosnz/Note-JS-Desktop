# Limpieza final — 3 de noviembre de 2026

## Archivos de distribución

- Windows: `dist/NoteJS.exe` y `dist/Instalador_NoteJS.exe`.
- Android: `../Notas/app/build/outputs/apk/debug/app-debug.apk` (compilación de desarrollo).
- No se eliminan bases SQLite, adjuntos ni perfiles de sesión al limpiar ejecutables.

## Cambios

- Eliminados 15 ejecutables e instaladores anteriores, incluida la copia de la raíz.
- Eliminados 27 scripts de investigación de cachés personales de Notion. No eran dependencias de la aplicación ni de sus pruebas. El catálogo JSON se conserva porque PROJECT.md lo utiliza como referencia.
- Eliminadas 12 copias de configuración Android con sufijo `-1`, conservando las configuraciones activas y sus actualizaciones.
- Eliminados cinco archivos Kotlin que solo contenían declaraciones de paquete y comentarios sobre funciones retiradas.
- Eliminado un cálculo de configuración OAuth sin consumidores en Gradle y comentarios de dependencias desactivadas. Las dependencias activas y los recursos de iconos utilizados por Android se conservan.
- Centralizado el arranque del servidor en `server.main`; `app.py` y `main.py` siguen disponibles como adaptadores de compatibilidad.
- Centralizado el empaquetado Windows en `NoteJS.spec`, con comprobación de errores. El instalador se compila en `build/installer` y se mueve a `dist` al terminar correctamente.
- Corregidos los comandos npm para localizar un Python real cuando los alias de Microsoft Store no funcionan. Se puede configurar `NOTEJS_PYTHON`.
- Eliminada la caché bytecode Python versionada. Los cambios previos de calendario y soporte se conservaron.

## Validación de escritorio

- Suite Python completa: 446 pruebas aprobadas.
- Contratos de empaquetado después del cambio: suites de 17 y 28 pruebas aprobadas; ambas incluidas en las 446 de la suite completa final.
- Suite JavaScript: 17 pruebas aprobadas.
- `npm run build`: aprobado.
- PyInstaller e Inno Setup: compilaciones correctas.
- Arranque del ejecutable con datos aislados y respuesta HTTP de la interfaz incluida: aprobado.
- Edge: calendario con proveedor simulado, PDF (importación, lectura, dibujo y exportación), fotografías de portada y bienvenida: aprobados.
- Emuladores Firebase: acceso Microsoft mediante popup y redirección, sesión persistente, tablas móviles, conflictos, reinicio sin conexión y aislamiento de cuentas: aprobados.
- No se ejecutó una instalación sobre el perfil personal ni se accedió a cuentas reales para estas pruebas.

Los registros están en `.test-artifacts/cleanup-*.log`; el inventario de binarios retirados está en `.test-artifacts/removed-binaries.json`.

## Android

Suite final contra emuladores locales de Auth y Firestore: **92 pruebas aprobadas, cero fallos, cero errores y cero omitidas**. Registro: `.test-artifacts/cleanup-android-tests.log`.

Compilación del APK y del código de pruebas: aprobada. El APK final de desarrollo se generó en `../Notas/app/build/outputs/apk/debug/app-debug.apk`.

Los primeros intentos agotaron la memoria nativa de Java. La compilación terminó al separar las pruebas y usar `--max-workers=1 --no-parallel` y `-Dorg.gradle.jvmargs="-Xmx1024m -XX:ActiveProcessorCount=2 -XX:+UseSerialGC -Dfile.encoding=UTF-8"`.

La ejecución completa detectó que `NotesViewModelTest` no inicializaba WorkManager en Robolectric. Se añadió la inicialización de AndroidX Startup en la preparación del test, conservando las verificaciones funcionales.

La prueba de primera apertura usa un directorio de preferencias nuevo por ejecución. Los tiempos de espera de preparación de Firebase local se ampliaron para admitir el arranque en frío del emulador en una máquina con poca memoria.

No había un dispositivo ni un emulador Android conectado; la verificación de interacción en dispositivo queda fuera de la validación realizada.
