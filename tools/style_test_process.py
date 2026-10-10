"""Проба стиля (docs/TRIPO_STYLE_TEST.md, раздел 3): обработать tripo/style_test/<a|b|c>/<имя>.glb →
export/style_test/<a|b|c>/<имя>_idle.glb + лист превью (три ряда A, B, C — одни и те же предметы друг под другом).
Запуск: python3 tools/style_test_process.py   (сначала: python3 tools/drive_fetch.py --style-test)

Правила:
- перед — к −Y: у Tripo он обычно смотрит вбок → поворот 270°, исключения — tripo/style_test_rotate.json
  ({"<стиль>/<имя>": градусы} или {"<имя>": градусы} для всех стилей); проверено по превью с 4 сторон;
- размер — из таблицы раздела 2 (ширина × высота × глубина, м): высота — точно, пропорции — как у модели;
  линии (трубы, кабели) — точно по всем трём размерам (стыкуются через всю стену); плоское на стене (плакаты,
  решётка) — глубина ужимается до таблицы, если модель толще в 1,5 раза;
- опора: пол — низ по центру (Z = 0); на стене — спина в Y = 0, низ Z = 0; лампа — верх в Z = 0;
- облегчение: A ≤ 5 000; B и C: мелочь ≤ 3 000, мебель ≤ 8 000, персонаж ≤ 15 000; текстуры 1024, без блеска.
"""
import datetime
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tripo_process as T  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

ROOT = T.ROOT
SRC = os.path.join(ROOT, "tripo", "style_test")
OUT = os.path.join(ROOT, "export", "style_test")
STYLES = {"a": "A — low poly", "b": "B — реализм", "c": "C — рисованный"}
# имя: (ширина, высота, глубина) м — TRIPO_STYLE_TEST.md, раздел 2 (порядок — как в таблице)
SIZES = {
    "line_pipes": (3, 0.25, 0.2), "line_cable": (3, 0.08, 0.06),
    "decor_vent": (0.5, 0.5, 0.05), "decor_box": (0.35, 0.5, 0.12),
    "poster_1": (0.6, 0.8, 0.02), "poster_2": (0.8, 0.6, 0.02), "wall_shelf": (1, 0.35, 0.3),
    "bed": (2, 0.8, 0.9), "workbench": (1.6, 0.95, 0.8), "locker": (0.6, 1.8, 0.5), "stove": (0.6, 1, 0.6),
    "table": (1.2, 0.75, 0.7), "chair": (0.45, 0.9, 0.45), "lamp_ceiling": (0.35, 0.4, 0.35),
    "crate": (0.8, 0.5, 0.5), "barrel": (0.6, 0.9, 0.6), "radio": (0.4, 0.3, 0.25), "character": (0.5, 1.8, 0.3),
}
LINES = {"line_pipes", "line_cable"}
WALL = {"line_pipes", "line_cable", "decor_vent", "decor_box", "poster_1", "poster_2", "wall_shelf"}
FLAT = {"decor_vent", "poster_1", "poster_2"}
CEILING = {"lamp_ceiling"}
SMALL = {"decor_vent", "decor_box", "poster_1", "poster_2", "radio", "lamp_ceiling", "line_cable"}
DEFAULT_ROT = 270


def limit(style, name):
    if style == "a":
        return 5000
    if name == "character":
        return 15000
    return 3000 if name in SMALL else 8000


def rotation(style, name, cfg):
    return cfg.get(f"{style}/{name}", cfg.get(name, DEFAULT_ROT))


def process(style, name, rot):
    W, H, D = SIZES[name]
    obj, n_parts = T.import_joined(os.path.join(SRC, style, name + ".glb"))
    t0 = T.tris(obj)
    T.clear_custom_normals(obj)
    if rot:
        obj.data.transform(Matrix.Rotation(math.radians(rot), 4, "Z"))
    if name in FLAT:                          # плоское: задняя сторона не видна, а при облегчении слипается с передом
        T.remove_back(obj)
    lo, hi = T.bbox(obj)
    w, h, d = (float(x) for x in (hi[0] - lo[0], hi[2] - lo[2], hi[1] - lo[1]))
    if name in LINES:
        obj.data.transform(Matrix.Diagonal((W / w, D / d, H / h, 1)))
    else:
        obj.data.transform(Matrix.Scale(H / h, 4))
        lo, hi = T.bbox(obj)
        dd = float(hi[1] - lo[1])
        if name in FLAT and dd > D * 1.5:
            obj.data.transform(Matrix.Diagonal((1, D / dd, 1, 1)))
    lo, hi = T.bbox(obj)
    cx, cy = (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2
    if name in WALL:
        shift = (-cx, -hi[1], -lo[2])
    elif name in CEILING:
        shift = (-cx, -cy, -hi[2])
    else:
        shift = (-cx, -cy, -lo[2])
    obj.data.transform(Matrix.Translation(Vector(shift)))
    obj.data.update()
    lim = limit(style, name)
    t1 = T.decimate(obj, lim)
    T.smooth_by_angle(obj)
    T.fix_materials(obj, 1024)
    os.makedirs(os.path.join(OUT, style), exist_ok=True)
    mb, _ = T.export(obj, os.path.join(OUT, style, name + "_idle.glb"))
    lo, hi = T.bbox(obj)
    size = [float(hi[0] - lo[0]) * 100, float(hi[2] - lo[2]) * 100, float(hi[1] - lo[1]) * 100]
    warns = []
    if t1 > lim:
        warns.append(f"не облегчилось до лимита: {t1}")
    if abs(size[0] - W * 100) > 0.15 * W * 100:
        warns.append(f"ширина {size[0]:.0f} см, в таблице {W * 100:.0f}")
    views = T.render_views(obj, os.path.join(ROOT, "renders", "_review", "tripo_views", f"st_{style}_{name}"), px=220)
    print(f"[{style}/{name}] {t0} → {t1} (≤ {lim}), {size[0]:.0f}×{size[1]:.0f}×{size[2]:.0f} см, поворот {rot}°, "
          f"{mb:.2f} МБ" + "".join(f"  ⚠ {x}" for x in warns), flush=True)
    return {"tris": [t0, t1, lim], "size_cm": size, "table_cm": [W * 100, H * 100, D * 100], "rotate": rot,
            "mb": mb, "warnings": warns, "views": views}


def sheet(res, out):
    from PIL import Image, ImageDraw, ImageFont
    try:
        big = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 14)
        small = ImageFont.truetype("DejaVuSans.ttf", 12)
    except OSError:
        big = font = small = ImageFont.load_default()
    C, PAD, HEAD, LAB = 220, 8, 30, 30
    names = list(SIZES)
    W = 150 + len(names) * (C + PAD)
    H = HEAD + len(STYLES) * (2 * C + LAB + PAD * 3)
    s = Image.new("RGB", (W, H), (24, 25, 30))
    d = ImageDraw.Draw(s)
    for j, n in enumerate(names):
        d.text((150 + j * (C + PAD), 8), n, font=font, fill=(240, 240, 240))
    y = HEAD
    for st, title in STYLES.items():
        d.text((10, y + C // 2), title.split(" — ")[0], font=big, fill=(255, 210, 120))
        d.text((10, y + C // 2 + 28), title.split(" — ")[1], font=small, fill=(190, 190, 190))
        d.text((10, y + C + C // 2), "в 3/4", font=small, fill=(150, 150, 150))
        d.text((10, y + C // 2 + 46), "спереди", font=small, fill=(150, 150, 150))
        for j, n in enumerate(names):
            x = 150 + j * (C + PAD)
            r = res.get(st, {}).get(n)
            if not r:
                d.rectangle((x, y, x + C, y + 2 * C + PAD), outline=(70, 70, 75))
                d.text((x + 10, y + C), "нет модели", font=font, fill=(150, 150, 150))
                continue
            for k, v in enumerate(r["views"]):
                s.paste(Image.open(v).convert("RGB").resize((C, C)), (x, y + k * (C + PAD)))
            t = r["tris"]
            d.text((x, y + 2 * C + PAD + 4), f"{t[1]} тр. · {r['size_cm'][0]:.0f}×{r['size_cm'][1]:.0f} см",
                   font=small, fill=(180, 180, 185) if not r["warnings"] else (255, 190, 120))
        y += 2 * C + LAB + PAD * 3
    os.makedirs(os.path.dirname(out), exist_ok=True)
    s.save(out)
    return out


def report(res):
    L = ["# Проба стиля — отчёт обработки", "",
         "`tools/style_test_process.py` (правила — `docs/TRIPO_STYLE_TEST.md`, раздел 3). Размер Ш × В × Г, см; "
         "в таблице — из раздела 2. Высота — точно, пропорции — модели (линии — точно по всем трём).", "",
         "| Стиль | Модель | Треугольники до → после (лимит) | Размер, см | По таблице, см | Поворот | МБ | Предупреждения |",
         "|---|---|---|---|---|---|---|---|"]
    for st in STYLES:
        for n in SIZES:
            r = res.get(st, {}).get(n)
            if not r:
                L.append(f"| {st.upper()} | `{n}` | — | — | — | — | — | нет модели |")
                continue
            t, s, tb = r["tris"], r["size_cm"], r["table_cm"]
            L.append(f"| {st.upper()} | `{n}` | {t[0]:,} → {t[1]:,} ({t[2]:,}) | {s[0]:.0f} × {s[1]:.0f} × {s[2]:.0f} | "
                     f"{tb[0]:.0f} × {tb[1]:.0f} × {tb[2]:.0f} | {r['rotate']}° | {r['mb']:.2f} | "
                     f"{'<br>'.join('⚠ ' + w for w in r['warnings']) or '—'} |".replace(",", " "))
    open(os.path.join(ROOT, "docs", "TRIPO_STYLE_REPORT.md"), "w").write("\n".join(L) + "\n")


def main():
    p = os.path.join(ROOT, "tripo", "style_test_rotate.json")
    cfg = json.load(open(p)) if os.path.exists(p) else {}
    cfg = {k: v for k, v in cfg.items() if not k.startswith("_")}
    res = {}
    for st in STYLES:
        for n in SIZES:
            if os.path.exists(os.path.join(SRC, st, n + ".glb")):
                res.setdefault(st, {})[n] = process(st, n, rotation(st, n, cfg))
            else:
                print(f"[{st}/{n}] нет модели — пропуск")
    out = os.path.join(ROOT, "renders", "_review", f"style_test_{datetime.date.today().isoformat()}.png")
    print("лист превью:", sheet(res, out))
    report(res)
    print("отчёт: docs/TRIPO_STYLE_REPORT.md")


if __name__ == "__main__":
    main()
