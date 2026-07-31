@echo off
REM Launcher para Windows (via uv)
cd /d "%~dp0"

REM 'uv run' cria o .venv e instala as dependencias automaticamente na 1a vez.
REM Usa pythonw para nao abrir janela de console.
uv run pythonw annoying_popups.py %*
