@echo off
REM Roda o Annoying Ads em segundo plano no Windows (sem janela de console).
cd /d "%~dp0"

REM Garante venv + dependencias.
uv sync >nul 2>&1

REM pythonw = sem console; start = desanexado do terminal.
start "" ".venv\Scripts\pythonw.exe" annoying_popups.py %*

echo Rodando em segundo plano.
echo Para fechar: segure ESC por 5s  —  ou rode stop.bat
