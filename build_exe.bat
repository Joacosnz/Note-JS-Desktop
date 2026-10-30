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

echo [1/2] Verificando dependencias con %PYTHON_EXE%...
"%PYTHON_EXE%" -m pip install -r requirements.txt

echo.
echo [2/2] Compilando NoteJS.exe autónomo con PyInstaller...
"%PYINSTALLER_EXE%" --noconsole --onefile --add-data "frontend;frontend" --hidden-import peewee --hidden-import models --hidden-import backend --hidden-import webview.platforms.winforms --hidden-import webview.platforms.edgechromium --name "NoteJS" desktop_app.py

echo.
if exist "dist\NoteJS.exe" (
    echo ===============================================================
    echo   ✓ COMPILACIÓN COMPLETADA EXITOSAMENTE!
    echo   Tu ejecutable para Windows 11 está en: dist\NoteJS.exe
    echo ===============================================================
) else (
    echo ===============================================================
    echo   ✗ Hubo un problema al generar dist\NoteJS.exe
    echo ===============================================================
)
pause
