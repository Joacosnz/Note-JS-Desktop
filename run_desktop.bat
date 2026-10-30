@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title Note JS — Escritorio (PyWebView + SQLite)
echo ========================================================
echo   Note JS — Iniciando Aplicación Nativa para Windows 11
echo ========================================================
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

"%PYTHON_EXE%" desktop_app.py
if %errorlevel% neq 0 (
    echo.
    echo Intentando con python en PATH...
    python desktop_app.py
)
pause
