# Hardening de Note JS Desktop y Android

Fecha: 2026-11-03 (America/Buenos_Aires). Alcance: estado local de `Note-JS-Desktop` y `Notas`, incluidos cambios previos del usuario. No se desplegaron reglas ni se publicaron binarios. Esta revisión es una línea base técnica, no una auditoría completa, certificación ISO ni informe SOC 2.

## Referencias y criterio

- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001): gestión de riesgos y controles de seguridad.
- [ISO/IEC 27701:2025](https://www.iso.org/standard/27701): sistema de gestión de privacidad. Se usa la edición 2025, no se presupone que la extensión 2019 siga siendo la referencia elegida.
- [AICPA Trust Services Criteria 2017, puntos de enfoque revisados 2022](https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022): seguridad, disponibilidad, integridad, confidencialidad y privacidad.

El mapeo siguiente expresa contribución técnica a objetivos de control, no equivalencia normativa ni satisfacción integral de cláusulas. La aplicabilidad formal requiere alcance, evaluación de riesgos y acceso al texto normativo completo.

## Cambios y evidencia

| Riesgo observado | Tratamiento aplicado | Objetivo de control |
| --- | --- | --- |
| API local sin autenticación escuchaba en `0.0.0.0` | Default loopback; `run_server` rechaza interfaces remotas y el handler rechaza clientes no locales | SOC 2 CC6; ISO 27001 control de acceso y redes |
| CORS `*` y ausencia de control global de origen | Sin CORS abierto; Host/puerto exactos, Origin exacto, rechazo de fetch entre sitios y DNS rebinding | SOC 2 CC6; ISO 27001 protección de aplicaciones |
| Lecturas sin límite global de cuerpo | Máximo 72 MiB, timeout de conexión de 30 s, rechazo de framing ambiguo/longitudes inválidas | SOC 2 disponibilidad; ISO 27001 capacidad y configuración |
| Descarga del código incluía SQLite, PDFs y portadas personales | ZIP de distribución excluye base y adjuntos | SOC 2 confidencialidad/privacidad; ISO 27701 minimización y divulgación |
| Android permitía backup con reglas vacías | `allowBackup=false`; exclusión de todos los dominios privados en backup y transferencia de dispositivo | ISO 27701 protección de datos personales; SOC 2 confidencialidad |
| Android no explicitaba política de tráfico claro | `usesCleartextTraffic=false` | ISO 27001 seguridad de comunicaciones |
| Respuestas sin política uniforme de navegador | nosniff, SAMEORIGIN, no-referrer y CORP same-origin | Protección de datos y aplicaciones |

La API sigue siendo una interfaz de confianza local: procesos del mismo equipo pueden acceder a ella. No se diseñó para hosting remoto ni usuarios múltiples. Los controles de origen no sustituyen autenticación ni protegen contra XSS ejecutado dentro del origen autorizado. Los límites actuales tampoco constituyen protección completa contra agotamiento por concurrencia.

## Verificación reproducible

Desde Desktop, con Python instalado:

```text
python -m unittest discover -s tests -p test_security_hardening.py
python -m unittest discover -s tests -p test_pdf_documents.py
python -m unittest discover -s tests -p test_google_calendar.py
python -m unittest discover -s tests -p test_cover_images.py
npm run test:firebase
npm audit --omit=dev --json
```

Resultado local: 5 pruebas nuevas de seguridad, 5 de PDF, 17 de calendario, 3 de portadas y 17 de JavaScript aprobadas (47 total). Las pruebas nuevas ejercitan HTTP real con puerto efímero y un ZIP con datos sintéticos; no modifican notas del usuario. Audit de producción npm: cero avisos devueltos; no cubre Python, Gradle, binarios ni dependencias vendorizadas. `git diff --check` aprobado en ambos repositorios.

Android: `gradle :app:processDebugResources --offline` aprobado con JDK y SDK locales (BUILD SUCCESSFUL; manifiesto y recursos procesados). La compilación de recursos no sustituye pruebas en dispositivo de backup/restauración y transporte. Pendiente validar login, sincronización, importación/compartir y recuperación en dispositivos API 24 y 31+.

## Efectos funcionales

- El servidor deja de estar disponible por LAN. No publicar esta API mediante proxy; requiere un diseño de autenticación antes de admitir uso remoto.
- Descargar el proyecto ya no sirve de copia de seguridad personal. Usar los flujos explícitos de exportación/backup de la app.
- Android no migrará notas locales ni credenciales mediante backup automático del sistema. Los backups explícitos Drive/OneDrive son flujos separados y requieren revisión propia. Asegurar una copia explícita recuperable antes de cambiar de dispositivo.
- URLs HTTP sin TLS en Android pueden dejar de cargar; usar HTTPS. No se agregó una excepción global para emuladores.
- Los EXE/APK existentes no incorporan estas modificaciones hasta reconstruirlos y distribuirlos.

## Registro de riesgos pendientes

Responsables propuestos por rol; todavía deben asignarse a personas y aprobar fechas. Prioridad P1 = antes de una publicación con afirmaciones de seguridad; P2 = siguiente ciclo de hardening.

| Prioridad | Pendiente / evidencia actual | Responsable propuesto | Criterio de cierre |
| --- | --- | --- | --- |
| P1 | Datos SQLite locales y adjuntos: no se acreditó cifrado de aplicación ni ciclo de vida de claves | Ingeniería | Modelo de amenaza; protección por OS/keystore; migración y recuperación probadas sin pérdida de datos |
| P1 | Firestore, Storage, IAM y App Check: no se verificó configuración desplegada | Administrador cloud | Exportar configuración sin secretos; probar usuario anónimo/A/B, denegación cruzada y esquema; revisar privilegios y enforcement |
| P1 | Identidad de firma debug embebida en `app/build.gradle.kts` y keystore debug presente | Release engineering | Mantener debug fuera de producción; verificar certificados autorizados, release signing privado y restricciones de API; evaluar rotación de registros debug |
| P1 | Repo Desktop contiene `notejs.db` versionada; no se inspeccionaron sus contenidos | Mantenedor | Determinar si contiene datos reales; retirar datos de futuras distribuciones e historial mediante procedimiento aprobado, con backup y evaluación de exposición |
| P1 | Retención y eliminación en notas, historial, adjuntos, Drive/OneDrive, calendario y Firestore no verificadas de extremo a extremo | Privacidad + ingeniería | Inventario, finalidad, plazo por categoría y prueba de exportación/eliminación/revocación en todos los destinos |
| P1 | Auditoría de paquetes incompleta fuera de npm | Ingeniería | SBOM Python/Android/vendor, escaneo con fecha, triaje y política de actualizaciones |
| P2 | FileProvider permite raíces amplias de files/cache (`file_paths.xml`) | Android | Inventariar rutas de exportación y reducirlas con pruebas de compartir PDF/imagen/backup |
| P2 | Logs de excepciones e identificadores en calendario; sin inventario completo de logs | Ingeniería | Evitar tokens, contenido e identificadores personales; pruebas de redacción y retención definida |
| P2 | SSRF en captura de metadatos, sanitización HTML/XSS, puente PyWebView e importación ZIP requieren revisión dedicada | Ingeniería | Pruebas adversariales de redirecciones/red privada, scripts, navegación y traversal |
| P2 | No se acreditaron límites globales de concurrencia, sesiones ni autenticación local | Desktop | Evaluar token de sesión y límites sin romper handoffs OAuth, frontend y puente nativo |

## Proceso operativo necesario para SOC 2 / ISO

1. Responsable de seguridad define alcance, activos, proveedores, clasificación y registro de riesgos; aprueba tratamiento y declaración de aplicabilidad para ISO 27001.
2. Responsable de privacidad registra categorías de datos, finalidades, roles, destinatarios, transferencias, plazos y mecanismos de derechos. Evalúa necesidad de análisis de impacto y acuerdos con proveedores.
3. Administrador cloud exige MFA a administradores, mínimo privilegio, revisión periódica y retiro de accesos; conserva evidencia de las revisiones.
4. Ingeniería exige revisión de cambios, pruebas de seguridad en CI, análisis de secretos/dependencias y artefactos trazables firmados. No almacenar tokens, dumps ni datos personales en evidencias.
5. Operaciones define backup cifrado y prueba restauración, RPO/RTO, alertas y respuesta a incidentes. Ensaya revocación de sesiones/claves, contención y recuperación.
6. Dirección revisa métricas y riesgos; realiza auditoría interna y acciones correctivas. La atestación SOC 2 y certificación ISO requieren sus evaluaciones independientes correspondientes.

Conservar por versión: commit/diff revisado, resultados de pruebas, inventario de dependencias, aprobación de riesgos, configuración desplegada y resultado de restauración. Definir acceso y retención de evidencias según política; no se inventa aquí un plazo normativo universal.
