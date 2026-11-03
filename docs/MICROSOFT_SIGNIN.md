# Cuentas Microsoft en escritorio

**Mi cuenta → Conectar con Microsoft** usa `OAuthProvider('microsoft.com')` con `tenant: common` y selección explícita de cuenta, igual que el cliente Android. El proveedor existente se comprobó habilitado mediante una consulta de solo lectura; no se modificaron su configuración ni sus secretos.

En la aplicación PyWebView se abre una ventana de autenticación con marco nativo y sin puente a las funciones locales (`js_api`). Firebase completa allí el flujo OAuth por redirección y restaura la sesión mediante `getRedirectResult`. Ambas ventanas comparten el perfil local de Firebase. Una notificación de finalización, sin tokens, hace que la principal guarde la nota activa y se recargue para restaurar la sesión mediante el SDK. En un navegador normal se usa una ventana emergente. La persistencia local mantiene la cuenta al reiniciar. Google conserva su acceso existente mediante navegador externo.

La redirección evita transferir tokens Microsoft mediante el puente de Google: Firebase requiere realizar el flujo OAuth completo para ese proveedor. No se incluyen secretos de Azure ni credenciales de administración en el ejecutable. Tampoco se solicitan permisos adicionales de correo, calendario o archivos.

Las notas usan el UID de Firebase de la sesión activa. No se fusionan cuentas por coincidencia de correo. Si Firebase indica que una dirección ya pertenece a otro método de acceso, la interfaz invita a entrar con el método original.

## Comprobaciones

- Proveedor Microsoft habilitado en el proyecto real (lectura de `name` y `enabled` únicamente).
- Pruebas de proveedor, elección de flujo y mensajes de error.
- Navegador real con Firebase Auth/Firestore emulados: popup Microsoft, redirección de escritorio, notas sincronizadas con el UID correspondiente, persistencia de sesión, cierre y cambio de cuenta.
- La autorización con credenciales Microsoft reales no forma parte de las pruebas automatizadas.

Referencia: [Firebase: autenticación con Microsoft](https://firebase.google.com/docs/auth/web/microsoft-oauth).
