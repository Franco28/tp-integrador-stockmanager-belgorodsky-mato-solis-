#!/bin/bash
# Iniciador de StockManager para macOS. Se puede abrir desde Finder.
set -u
cd "$(dirname "$0")" || exit 1

PYTHON=""
for CANDIDATO in python3.15 python3.14 python3.13 python3.12 python3.11 python3.10 python3 python; do
    if command -v "$CANDIDATO" >/dev/null 2>&1 &&        "$CANDIDATO" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then
        PYTHON="$(command -v "$CANDIDATO")"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "No se encontró Python 3.10 o superior. Instalalo desde python.org."
    read -r -p "Presioná Enter para cerrar..." _
    exit 1
fi

"$PYTHON" scripts/iniciar_local.py
CODIGO=$?
if [ "$CODIGO" -ne 0 ]; then
    echo
    echo "La ejecución terminó con error ($CODIGO). Revisá el mensaje anterior."
    read -r -p "Presioná Enter para cerrar..." _
fi
exit "$CODIGO"
