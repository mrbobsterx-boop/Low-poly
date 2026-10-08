#!/bin/bash
# Ставит Blender как модуль Python (bpy), чтобы модели и рендеры собирались скриптами:
#   python3 models/<категория>/<id>.py
# Только в облачных сессиях Claude Code. Повторный запуск ничего не ломает.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

BPY_VERSION="5.2.2"

if python3 -c "import bpy, sys; sys.exit(0 if bpy.app.version_string.startswith('${BPY_VERSION%.*}') else 1)" >/dev/null 2>&1; then
  echo "bpy уже установлен"
  exit 0
fi

if ! pip install --quiet "bpy==${BPY_VERSION}"; then
  echo "Не удалось поставить bpy ${BPY_VERSION} (нужен Python 3.13). Модели собрать здесь не получится." >&2
  exit 0
fi

python3 -c "import bpy; print('bpy', bpy.app.version_string)"
