"""Список предметов, которые в ОС ломаются (destruction.enabled и есть картинка broken) → docs/breakable.json.
Запуск: python3 tools/sync_breakable.py <путь к клону object-constructor>
Модели берут broken только для предметов из этого списка (models/_lib.py, make()).
"""
import glob
import json
import os
import sys

src = sys.argv[1] if len(sys.argv) > 1 else "../mrbobsterx-boop/object-constructor"
out = []
for f in sorted(glob.glob(os.path.join(src, "data", "objects", "*.json"))):
    d = json.load(open(f))
    de = d.get("destruction") or {}
    if de.get("enabled") and de.get("broken"):
        out.append(d["id"])
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
json.dump({"source": "object-constructor/data/objects/*.json: destruction.enabled && destruction.broken",
           "ids": out}, open(os.path.join(root, "docs", "breakable.json"), "w"), ensure_ascii=False, indent=1)
print(len(out), "ломающихся предметов → docs/breakable.json")
