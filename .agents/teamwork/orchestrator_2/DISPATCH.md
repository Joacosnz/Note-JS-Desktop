## 2026-11-01T00:29:49Z

Actualizar la interfaz de usuario, navegación y configuración de Note-JS-Desktop según las especificaciones y referencias visuales provistas para un entorno de producción.

Working directory: c:\Users\Joaco\Documents\GitHub\Note-JS-Desktop
Integrity mode: development

Referencias:
- Imagen 1 (Estilo de pestañas y controles de ventana): C:/Users/Joaco/.gemini/antigravity/brain/a7b54704-e486-450a-8698-6616535160da/.user_uploaded/media_1793492072447_291e97ff.png
- Imagen 2 (Barra de edición/formato: solo + Insertar en amarillo, + centrado): C:/Users/Joaco/.gemini/antigravity/brain/a7b54704-e486-450a-8698-6616535160da/.user_uploaded/media_1793492163191_1126a933.png
- Imagen 3 (Nuevo icono oficial de la aplicación): C:/Users/Joaco/.gemini/antigravity/brain/a7b54704-e486-450a-8698-6616535160da/.user_uploaded/media_1793492278932_da6ebc7c.png

## Requirements

### R1. Estilos de Barra de Pestañas y Controles de Ventana
- Los botones de la barra de pestañas no deben tener fondo o borde amarillo permanente; el resaltado amarillo solo debe aplicarse al pulsar un botón o al situar el cursor encima (hover o estado activo/seleccionado).
- La apariencia de las pestañas y los botones de control de ventana (cerrar, minimizar y achicar/restaurar) debe coincidir con el diseño mostrado en la Imagen 1: pestañas redondeadas con icono, texto y botón cerrar ('x'), botón '+' para nueva pestaña y controles de ventana alineados a la derecha (menú/chevron, minimizar '-', maximizar/restaurar y cerrar 'x').

### R2. Unificación y Gestión de Carpetas
- Eliminar la duplicación de botones de crear carpeta en la interfaz.
- Los botones de crear carpeta no deben ser amarillos de forma permanente; solo deben mostrar color amarillo al hacer hover o al pulsarlos.
- Unificar los botones de "crear carpeta" y "crear carpeta inteligente" en una única acción unificada, donde crear una carpeta inteligente sea una opción elegible dentro del mismo modal o flujo de creación.

### R3. Acceso Rápido a Pantalla Completa de Recordatorios
- Añadir en la bandeja/panel de carpetas un acceso rápido visible para abrir la vista de recordatorios.
- Al activar este acceso, la interfaz debe reemplazar el área principal de contenido/editor para mostrar una vista a pantalla completa dedicada a recordatorios.

### R4. Barra de Edición, Formato y Botón de Ajustes
- En la barra de edición y formato (conforme a la Imagen 2), el botón "+ Insertar" debe ser el único elemento con color de acento amarillo; todos los demás botones de formato deben adoptar el color neutro del fondo del contenedor.
- El símbolo '+' en el botón "+ Insertar" debe estar centrado verticalmente con respecto al texto adyacente.
- El botón de ajustes debe consistir exclusivamente en un icono con el símbolo de engranaje (sin texto adicional).

### R5. Ubicación del Índice en la Vista de Notas
- En la vista de notas, el índice (tabla de contenidos) debe ubicarse fuera de la portada/banner y situarse en una columna o barra lateral fija en el costado derecho del editor, aprovechando el espacio libre disponible.

### R6. Icono de la Aplicación y Preferencia de Inicio
- Sustituir el icono oficial de la aplicación (en ventana, bandeja del sistema y assets correspondientes) por la imagen proporcionada en la Imagen 3.
- Añadir en la sección de Ajustes una opción de configuración para determinar el comportamiento de inicio de la aplicación, permitiendo al usuario elegir entre:
  1. "Iniciar siempre de cero" (sin notas abiertas, sin pestañas abiertas y sin carpetas seleccionadas).
  2. "Reanudar en la última nota visitada".
- El valor predeterminado configurado de fábrica al instalar o iniciar la aplicación debe ser "Iniciar siempre de cero".
- La aplicación debe persistir esta preferencia y aplicarla estrictamente en cada inicio.

## Verification Resources
- El equipo debe implementar pruebas automatizadas y verificaciones independientes (tests unitarios/e2e o scripts de prueba con runner) para validar la persistencia de configuración, la unificación del flujo de carpetas, el estado inicial al arrancar y los comportamientos interactivos de la interfaz.

## Acceptance Criteria

### Tabs & Window Controls
- [ ] Tab bar buttons display neutral backgrounds/borders by default and show yellow highlighting only when hovered or pressed/active.
- [ ] Tab bar layout, tab pills with close icon, adjacent '+' button, and window control buttons (chevron, minimize, maximize/restore, close) match the reference style in Image 1.
- [ ] Window control buttons trigger window minimize, maximize/restore, and close actions properly.

### Folders & Reminders
- [ ] Duplicate folder creation buttons in the interface are eliminated.
- [ ] Folder creation buttons display yellow styling only on hover or click.
- [ ] "Crear carpeta" and "Crear carpeta inteligente" are merged into a single button and dialog/form where smart folder is a toggleable option.
- [ ] A dedicated quick-access button/item in the folder tray switches the main content area into the full-screen reminders view.

### Formatting Bar, Settings Button & Note Index
- [ ] In the editor formatting toolbar, "+ Insertar" is the only button styled in yellow; all other toolbar buttons use neutral background matching the toolbar surface.
- [ ] The '+' character in "+ Insertar" is vertically aligned and centered with the "Insertar" label.
- [ ] The settings button is rendered solely as a gear icon without extra text.
- [ ] The note table of contents / index is rendered outside of the note cover and displayed in a fixed right-side column beside the editor.

### App Icon & Startup Preference
- [ ] Application window and taskbar icons are updated with the notebook graphic from Image 3.
- [ ] A setting exists in the Settings menu to toggle between "Iniciar siempre de cero" and "Reanudar en la última nota visitada".
- [ ] The default factory startup state is "Iniciar siempre de cero" (opening with no tabs, no open notes, and no folders selected).
- [ ] Setting "Reanudar en la última nota visitada" saves the last open note and restores it on the subsequent launch.


## 2026-11-01T01:55:44Z

Sentinel Liveness Check: Please update your progress.md and BRIEFING.md with current status of worker_m3 and Milestone 3 execution.
