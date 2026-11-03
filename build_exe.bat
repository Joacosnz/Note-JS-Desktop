@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title Compilador Note JS a .exe (PyWebView + SQLite + Peewee ORM)
echo ===============================================================
echo   Note JS - Compilador a .exe para Windows 11
echo ===============================================================
echo.

:: Detectar intérprete de Python real en Windows 11
set "PYTHON_EXE="
if exist "%LOCALAPPDATA%\Python\pythoncore-3.15-64\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Python\pythoncore-3.15-64\python.exe"
) else if exist "%LOCALAPPDATA%\Python\bin\python.exe" (
    set "PYTHON_EXE=%LOCALAPPDATA%\Python\bin\python.exe"
) else if exist "C:\Python312\python.exe" (
    set "PYTHON_EXE=C:\Python312\python.exe"
) else if exist "C:\Python311\python.exe" (
    set "PYTHON_EXE=C:\Python311\python.exe"
) else (
    set "PYTHON_EXE=python"
)

:: Detectar PyInstaller
set "PYINSTALLER_EXE="
if exist "%LOCALAPPDATA%\Python\pythoncore-3.15-64\Scripts\pyinstaller.exe" (
    set "PYINSTALLER_EXE=%LOCALAPPDATA%\Python\pythoncore-3.15-64\Scripts\pyinstaller.exe"
) else (
    set "PYINSTALLER_EXE=%PYTHON_EXE% -m PyInstaller"
)

:: Detectar Inno Setup
set "ISCC_EXE="
if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" (
    set "ISCC_EXE=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "ISCC_EXE=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "ISCC_EXE=C:\Program Files\Inno Setup 6\ISCC.exe"
)

echo [1/3] Verificando dependencias con %PYTHON_EXE%...
"%PYTHON_EXE%" -m pip install -r requirements.txt

echo.
echo [2/3] Compilando NoteJS.exe autónomo con PyInstaller...
if exist "node_modules\.bin\esbuild.cmd" (
    call npm run build:firebase
    if errorlevel 1 exit /b 1
)
"%PYINSTALLER_EXE%" --noconsole --onefile --icon="public\icon.ico" --add-data "frontend;frontend" --add-data "public;public" --add-data "welcome_notes.json;." --hidden-import peewee --hidden-import models --hidden-import backend --hidden-import webview.platforms.winforms --hidden-import webview.platforms.edgechromium --name "NoteJS" desktop_app.py

echo.
echo [3/3] Generando instalador para usuarios (Instalador_NoteJS.exe)...
if defined ISCC_EXE (
    "%ISCC_EXE%" installer.iss
) else (
    echo [AVISO] Inno Setup no encontrado. Omitiendo generacion de Instalador_NoteJS.exe.
)

echo.
if exist "dist\Instalador_NoteJS.exe" (
    echo ===============================================================
    echo   [OK] INSTALADOR Y EJECUTABLE CREADOS EXITOSAMENTE!
    echo   Instalador para usuarios: dist\Instalador_NoteJS.exe
    echo   Ejecutable autonomo directo: dist\NoteJS.exe
    echo ===============================================================
) else if exist "dist\NoteJS.exe" (
    echo ===============================================================
    echo   [OK] EJECUTABLE CREADO: dist\NoteJS.exe
    echo ===============================================================
) else (
    echo ===============================================================
    echo   [ERROR] Hubo un problema al generar los binarios.
    echo ===============================================================
)
if "%~1"=="" pause
