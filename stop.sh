#!/usr/bin/env bash
# Botão de pânico: encerra o Annoying Ads mesmo que o ESC falhe.
cd "$(dirname "$0")"
killed=0

# 1) pelo PID salvo pelo run-bg.sh
if [ -f .annoying.pid ]; then
  PID=$(cat .annoying.pid)
  if kill "$PID" 2>/dev/null; then killed=1; fi
  rm -f .annoying.pid
fi

# 2) fallback por padrão — cobre execução via fonte e via binário.
#    Os padrões não batem com este próprio script (pasta 'annoying-popups'
#    vs script 'annoying_popups.py'; e -x casa só o nome exato do binário).
pkill -f 'annoying_popups\.py' 2>/dev/null && killed=1
pkill -x 'annoying-popups' 2>/dev/null && killed=1

if [ "$killed" = 1 ]; then
  echo "Pronto: pop-ups encerrados."
else
  echo "Nada rodando encontrado."
fi
