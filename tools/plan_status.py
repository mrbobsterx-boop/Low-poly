"""Чек-лист моделей по плану ОС: docs/plan.json (node tools/sync_plan.js) + что уже готово в export/ → docs/PLAN.md.
Запуск: python3 tools/plan_status.py
"""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
plan = json.load(open(os.path.join(ROOT, "docs", "plan.json")))
done = {f[:-4] for f in os.listdir(os.path.join(ROOT, "export")) if f.endswith("_idle.glb")}   # модели из Tripo после обработки
cats = {}
for o in plan:
    cats.setdefault(o["cat"], []).append(o)
total = sum(1 for o in plan for v in o["variants"] if not v["skip"])
ready = sum(1 for o in plan for v in o["variants"] if not v["skip"] and f"{o['id']}_{v['slug']}_idle" in done)
L = ["# План моделей (из ОС: tools/object-plan)", "",
     "Источник — план объектов ОС (`object-constructor/tools/object-plan/js/0[3-5]-data-*.js`), выгрузка — "
     "`node tools/sync_plan.js <ОС>` → `docs/plan.json`, этот файл — `python3 tools/plan_status.py`.", "",
     "Правила автора: **только idle**, каждый вариант — отдельно (`<id>_<вариант>_idle`); «сломанные/испорченные» "
     "и состояния (открыт, занят, пустой) — пропуск; размер — из ОС (если в плане другой — спросить автора); "
     "модели — из Tripo по картинкам ОС, обработка — `docs/TRIPO.md`; сначала по одному варианту на объект.", "",
     f"Готово: **{ready} из {total}** вариантов.", ""]
mism = [o for o in plan if o["size_mismatch"]]
if mism:
    L += ["## Размер в плане ≠ ОС — **берём из плана** (решение автора 2026-10-08; в ОС поправить)", "",
          "| id | План, см (берём) | ОС, см |", "|---|---|---|"]
    L += [f"| `{o['id']}` | {o['plan_size'][0]} × {o['plan_size'][1]} | {o['os_size'][0]} × {o['os_size'][1]} |" for o in mism]
    L.append("")
for cat, objs in cats.items():
    L += [f"## `{cat}`", "", "| id | Название | Размер (ОС), см | Варианты → файл | |", "|---|---|---|---|---|"]
    for o in objs:
        sz = o["size"]
        vs = []
        for v in o["variants"]:
            if v["skip"]:
                vs.append(f"~~{v['name']}~~")
            else:
                mark = "☑" if f"{o['id']}_{v['slug']}_idle" in done else "☐"
                vs.append(f"{mark} {v['name']} → `{v['slug']}`")
        warn = "размер из плана" if o["size_mismatch"] else ""
        L.append(f"| `{o['id']}` | {o['name']} | {sz[0]} × {sz[1]} | {'<br>'.join(vs)} | {warn} |")
    L.append("")
open(os.path.join(ROOT, "docs", "PLAN.md"), "w").write("\n".join(L))
print(f"docs/PLAN.md: готово {ready} из {total}")
