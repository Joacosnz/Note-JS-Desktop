# Google Calendar

En escritorio: **Recordatorios → Google Calendar → Conectar Google Calendar**.
Aceptá el permiso en el navegador, elegí un calendario y presioná **Sincronizar ahora**.
El permiso es independiente de la cuenta de Firebase usada para las notas.

Los recordatorios con fecha se representan como eventos de Calendar, con aviso de
15 minutos. Esto no conecta la lista de tareas de Google Tasks. Los elementos sin
fecha permanecen en Note JS. Se importan los eventos del calendario seleccionado.

Una vez iniciada la sincronización, se repite cada cinco minutos mientras la app
está abierta, después de guardar/eliminar un recordatorio y al recuperar conexión.
La selección del calendario queda recordada; al reconectar hay que iniciar la
sincronización nuevamente. Desconectar no borra los recordatorios existentes.

Los cambios se comparan con la última versión sincronizada. Si hay cambios en
ambos lados, se conserva cada versión y se indica un conflicto. Para resolverlo,
dejá los mismos título, fecha/hora, descripción, repetición y estado de completado
en ambos lados y volvé a sincronizar. Las actualizaciones usan ETag para detectar
cambios mientras Google responde. Un ID determinista evita duplicados si Google
crea un evento y se pierde la respuesta antes de guardarla localmente.

Los tokens de acceso se mantienen en memoria, nunca en SQLite, localStorage ni en
archivos. Hay que reconectar al reiniciar la app o cuando venza el permiso
(aproximadamente una hora). Esta versión no guarda un refresh token. Los vínculos
con eventos se guardan por cuenta y calendario dentro de SQLite.

Google Calendar API está habilitada en `isentropic-tape-465216-c1`. La autorización
solicita `calendar.events` y `calendar.calendarlist.readonly`. Google puede exigir
usuarios de prueba o verificación de la pantalla OAuth antes de permitir su uso
público; habilitar la API no equivale a esa verificación.

En Android se usa el proveedor nativo CalendarContract y el adaptador de
sincronización de Google. La cuenta de Google y la sincronización de Calendario
deben estar activadas en los ajustes del teléfono. Una cuenta de Firebase por sí
sola no configura el calendario de Android. Ya no se crea un calendario local
presentándolo como Google Calendar ni se cambia de cuenta silenciosamente.
WorkManager espera conexión y usa reintentos con demora creciente. La cola de
eliminaciones y las versiones base sobreviven al cierre de la app.

Validación: pruebas con SQLite temporal y respuestas simuladas de Calendar,
prueba de la interfaz real en Edge, pruebas de combinación de cambios en Android
y compilaciones de ambos clientes. No se modificaron eventos personales para
probar la integración ni se validó el consentimiento de un usuario real.
