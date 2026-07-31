#!/usr/bin/env bash
# Launcher para Linux/macOS (via uv)
set -e
cd "$(dirname "$0")"

# 'uv run' cria o .venv e instala as dependências automaticamente na 1ª vez,
# usando um Python gerenciado que já inclui tkinter.
exec uv run python annoying_popups.py "$@"
