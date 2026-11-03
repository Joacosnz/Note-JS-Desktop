; Script de Instalación Profesional para Windows 11 — Note JS
#define MyAppName "Note JS"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Note JS Team"
#define MyAppURL "https://github.com/Joacosnz/Note-JS-Desktop"
#define MyAppExeName "NoteJS.exe"
#ifndef MyAppExeSource
  #define MyAppExeSource "dist\NoteJS.exe"
#endif

[Setup]
AppId={{D37E84B1-2856-427E-971E-7D47C35EA3A0}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\NoteJS
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Permite instalación sin permisos de administrador (en LocalAppData\Programs\NoteJS)
; o como Administrador (en Program Files\NoteJS) con diálogo interactivo
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=dist
OutputBaseFilename=Instalador_NoteJS
SetupIconFile=public\icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
CloseApplications=yes
RestartApplications=no
ChangesAssociations=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#MyAppExeSource}"; DestDir: "{app}"; Flags: ignoreversion
Source: "public\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
; Notes and Firebase sessions belong to the user and are created on first launch.

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Registry]
; Offer Note JS in Open With without replacing the user's default PDF reader.
Root: HKA; Subkey: "Software\Classes\.pdf\OpenWithProgids"; ValueType: string; ValueName: "NoteJS.PDF"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\NoteJS.PDF"; ValueType: string; ValueData: "Documento PDF de Note JS"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\NoteJS.PDF\DefaultIcon"; ValueType: string; ValueData: "{app}\icon.ico"
Root: HKA; Subkey: "Software\Classes\NoteJS.PDF\shell\open\command"; ValueType: string; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
