#!/usr/bin/env bash
set -e
echo "==============================================================="
echo "  Note JS - Compilacion Nativa Linux (PyWebView + Peewee ORM)"
echo "==============================================================="
echo "[1/2] Instalando dependencias (peewee, pywebview, pyinstaller)..."
pip3 install -r requirements.txt

echo "[2/2] Compilando binario con PyInstaller + PyWebView..."
pyinstaller --noconsole --onefile --add-data "frontend:frontend" --hidden-import peewee --hidden-import models --name "NoteJS" desktop_app.py

echo "==============================================================="
echo "  COMPILACION COMPLETADA: ./dist/NoteJS"
echo "==============================================================="
