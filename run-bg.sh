#!/usr/bin/env bash
# Roda o Annoying Ads em segundo plano, desanexado do terminal.
# (pode fechar o terminal que continua rodando)
set -e
cd "$(dirname "$0")"

# Garante venv + dependências (Python gerenciado com tkinter).
uv sync >/dev/null 2>&1

# Lança direto pelo python do venv para termos o PID real do processo.
nohup ./.venv/bin/python annoying_popups.py "$@" >/dev/null 2>&1 &
PID=$!
echo "$PID" > .annoying.pid

echo "Rodando em segundo plano (PID $PID)."
echo "Para fechar: segure ESC por 5s  —  ou rode ./stop.sh"
