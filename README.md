Note JS — Desktop Note-Taking App

Note JS is a desktop productivity and note-taking application (for Windows, Linux, and macOS PCs), inspired by the visual elegance of Apple Notes and the block-based power of Notion.
The project has been fully migrated and optimized for PC, utilizing Python on the backend with SQLite + Peewee ORM relational storage, an ultra-lightweight native desktop window via PyWebView (avoiding the excessive memory consumption of Electron), and a fast, reactive frontend built with Vanilla JavaScript (ES6+), HTML5, and CSS3.

🚀 Key Features

1. Hierarchical Folder & Subfolder Manager:

* Support for nested subfolders with unlimited levels.
* Drag & Drop reorganization (drag one folder over another to make it a subfolder or promote it to the root).
* Smooth visual animations for indentation and drop states.
* Custom emoji assignment for any folder.
* All notes always reside in the master "All notes" folder.

2. Smart Folders:

* Real-time dynamic filters based on SQLite ORM queries.
* Logical combination modes: Match all (AND) or Match any (OR).
* Supported filters: Tags (#tags), Modification/Creation dates, Task lists (completed/pending checklists), Attachments (photos, videos, audio, PDF, links), and lock state.
* Smart folders are virtual (they do not move or duplicate physical notes).

3. Notion-Style Block Editor:

* Independent blocks (headings, paragraphs, bulleted lists, checklists, quotes, callouts, syntax-highlighted code, dynamic tables, and Kanban boards).
* O(1) fractional ordering (Fractional Indexing with Base62) allowing block movement without reindexing the entire document.
* Local and external images with visual resizing and anchoring controls (float left, right, center).

4. Integrated Calendar & Reminders:

* Interactive calendar view on the home page.
* Task and reminder management with date, time, category, and completed status.
* Direct persistence in the SQLite database (reminders).

5. Version History & Restore Points:

* Automatic saving of historical versions in SQLite (note_history).
* Named manual restore points.
* Atomic rollback to any previous version with a single click.

6. Web Link Metadata (OpenGraph Previews):

* Automatic extraction of titles, cover images, descriptions, and favicons for rich link cards, with local caching (web_link_cache).

7. Math, Audio, and Digital Signatures:

* Real-time mathematical formulas rendered with KaTeX.
* Voice note recording and playback directly from the editor.
* Handwriting signature panel and stroke digitization.

📁 Project Architecture

Firebase and the mobile app
Gradient covers and the emoji are shared with Android. Refer to the covers contract and unification improvements. The mobile update includes a Room 19→20 migration and preservation of these fields in backups.
The Note JS menu groups creation, PDF opening, search, navigation, and account settings. The sidebar displays the synchronization status. Document tools are located in Page Options, featuring light and dark themes.
Mobile tables retain their dimensions, headers, stripes, and cell colors when edited and re-synced. They include + Row and + Column buttons, Tab navigation, and tabulated range pasting within the table. Tables downloaded by previous versions update upon receiving the cloud state, preserving pending local edits.
The desktop is registered as Note JS Desktop in the mobile project isentropic-tape-465216-c1. It uses the Enterprise Native base ai-studio-android-notas-e533a5f4-cda6-4bde-b5d4-c0acf42009aa, with real-time updates enabled and the existing users/{uid}/notes collections. The deployed mobile rules are maintained; this integration does not replace them.

1. Open Settings → My Account → Connect with Google. The login completes in the system browser.
2. Use the same account as on Android to receive its notes.
3. To upload your previous PC library, choose Sync local notes with this account. Notes from another account are never linked automatically.
4. New notes are linked to the active account. SQLite preserves pending changes, and retries occur upon regaining connection or reopening the app.

Title, canvas content, folder, tags, pinned status, and trash are shared. Conversion supports text, headings, lists, tasks, tables, and remote images/PDFs. Mobile blocks that are not yet editable are preserved with their original information. Special desktop tools outside the canvas and standalone reminders/calendars remain local in this first integration. Conflicts preserve both versions; a remote deletion preserves a local copy.

Attachments: the project does not yet have a Firebase Storage bucket. Notes with local PDFs or images remain pending and are still saved on this PC; other notes are synchronized. To share files, Storage must be enabled, its rules configured for users/{uid}/notes_media/, and storageAvailable updated in frontend/firebase-config.json. Billing was not enabled nor was storage provisioned as part of this change.

The official SDK is included in frontend/vendor/firebase-sdk.mjs, so the app opens without downloading dependencies. The client configuration is public; a service account is not included. The Firebase session is kept in the local webview/ profile, which is not distributed with the installer. The access handoff from the browser expires in five minutes and is consumed only once.

To rebuild the SDK: npm ci and npm run build:firebase. Tests: npm run test:firebase, the Python suite, and tests/firebase_client_smoke.cjs against Auth and Firestore Enterprise emulators. The browser test uses synthetic accounts and a temporary SQLite database. Standard listeners are used because real-time sync and offline functionality are product requirements.

The installer creates a new library on startup and preserves the existing one upon updating: it does not include the development database or the author's sessions.

To run the integration test, with Java available: npx -y firebase-tools@latest emulators:exec --project demo-notejs-desktop --only auth,firestore --config firebase.emulators.json "node tests/firebase_client_smoke.cjs". Python and Edge paths can be specified via NOTEJS_TEST_PYTHON and NOTEJS_TEST_BROWSER.

PDF on desktop

* Opening a PDF from the sidebar opens a local document without creating a note.
* Inside a note, File and PDF Viewer allows uploading a PDF or pasting a link.
* The viewer includes pages, zoom, per-page rotation, text search, selectable text via the Text button, freehand drawing, colors, and stroke undo.
* Save copy exports a PDF with drawings and rotations. On desktop, the location is chosen with the native dialog; in the browser, it downloads. Changes are saved in the copy, not automatically in the original attachment.
* The installer registers Note JS in "Open with" for .pdf. The executable also accepts NoteJS.exe "C:\Documents\file.pdf".
* Local documents work without the Internet. They are kept in attachments/pdfs/, next to the application database; that folder must be included when moving notes or making a manual backup. Limit: 50 MB per file.
* External links require the server to allow CORS access; if it doesn't, download the PDF and upload it as a local file. Searching requires text in the document: this implementation does not include OCR or editing the original text. Encrypted PDFs can be read with a password; modifying them depends on pdf-lib support.
* Locally included libraries: PDF.js 6.5.438 (Apache-2.0) and pdf-lib 1.17.1 (MIT), with their licenses in frontend/vendor/.

Verification: python -m unittest discover -s tests -p test_pdf_documents.py. The actual rendering and export test runs with node tests/pdf_reader_smoke.cjs; it requires Edge and Python, whose paths can be specified with NOTEJS_TEST_BROWSER and NOTEJS_TEST_PYTHON.

Notas/
│
├── desktop_app.py        # Native desktop window with PyWebView + Python-JS Bridge
├── backend.py            # Multithreaded HTTP server and REST API
├── server.py             # Entrypoint for local server
├── app.py                # Secondary entrypoint
├── models.py             # Relational data layer with SQLite + Peewee ORM
├── peewee.py             # Integrated Peewee ORM
├── requirements.txt      # Python dependencies
├── package.json          # npm configuration and scripts
│
├── run_desktop.bat       # Starts the desktop app in development mode (Windows 11)
├── run_server.bat        # Starts the local server in development mode (Windows 11)
├── build_exe.bat         # Recompiles NoteJS.exe with PyInstaller
├── build_linux.sh        # Compiler for Linux binaries
│
├── dist/
│   ├── NoteJS.exe        # Single compiled executable via PyInstaller
│   └── Instalador_NoteJS.exe # Single Windows installer
│
├── frontend/             # Complete frontend for PC
│   ├── index.html        # DOM structure and modals
│   ├── styles.css        # macOS / Notion design system
│   └── app.js            # Complete client and synchronization logic

💻 How to Run on Windows 11

🚀 Option 1: Direct Execution with the Executable (.exe) — Recommended
Double-click on dist/NoteJS.exe.

* The application will open in an ultra-lightweight native desktop window without requiring a terminal or active dependencies.
* All your notes, smart folders, and reminders will be automatically saved in notejs.db.

🛠️ Option 2: Development Mode (PyWebView)
To develop or modify the source code in real-time:

* Double-click on run_desktop.bat.
* The script automatically detects your Python installation on Windows 11 and launches the development window.

🌐 Option 3: Local Web Server Mode

* Double-click on run_server.bat.
* Open your browser at: http://localhost:3000

📦 Option 4: Recompile the .exe Executable
If you modify styles, HTML templates, JavaScript logic, or Python models and wish to generate a new .exe:

* Double-click on build_exe.bat.
* PyInstaller will repackage the optimized binary into dist\NoteJS.exe.

Distribution and maintenance
Windows exclusively maintains dist/NoteJS.exe and dist/Instalador_NoteJS.exe. build_exe.bat and npm run build:exe use NoteJS.spec as common configuration. Local data in dist/ is not part of the installer and should not be deleted when cleaning binaries.
Android is maintained in the sibling repository ../Notas; its development APK is generated at app/build/outputs/apk/debug/app-debug.apk. Refer to the cleanup and validation log.
