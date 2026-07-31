@echo off
REM Gera o executavel single-file (Windows) via build.py.
cd /d "%~dp0"

uv sync --group dev
uv run python build.py

echo.
echo Pronto: dist\annoying-popups.exe
