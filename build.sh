#!/usr/bin/env bash
# Gera o executável single-file (Linux/macOS) via build.py.
set -e
cd "$(dirname "$0")"

uv sync --group dev
uv run python build.py

echo
echo "Pronto: dist/annoying-popups"
