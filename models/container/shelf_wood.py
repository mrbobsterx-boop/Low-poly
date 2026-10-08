"""Полка настенная `shelf_wood`. Размер — из плана ОС (100 × 30 см). Висит на стене: «спина» — Y = 0, низ — Z = 0.
План: «открытая полка, предметы на ней видны и стоят сверху» — поэтому полки ПУСТЫЕ, вещи ставит игра.
Варианты (только idle):
  derevyannaya               — деревянная доска на металлических уголках с косынками;
  metallicheskaya_ugolkovaya — стальная полка из перфорированного уголка, на болтах;
  uglovaya                   — угловая: две доски-четверти круга на стойке (ставится в угол);
  dvoynaya                   — двойная: две доски на деревянных боковинах.
Запуск: python3 models/container/shelf_wood.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("shelf_wood"))
D = 0.24


def derevyannaya():
    p = []
    BR, PL = H - 0.03, 0.03
    for x in (-0.36, 0.36):
        p.append(L.box((0.03, 0.02, BR), (x, -0.01, 0), "steel_dark", bevel=0.004))
        p.append(L.box((0.03, D - 0.02, 0.02), (x, -D / 2 + 0.01, BR - 0.02), "steel_dark", bevel=0.004))
        p.append(L.box((0.012, 0.16, 0.02), (x, -0.085, BR - 0.15), "steel_dark", rot=(-45, 0, 0), bevel=0.003))
        p.append(L.box((0.012, 0.004, 0.012), (x, -0.022, BR - 0.06), "steel_light", bevel=0))
        p.append(L.spot((x, -0.021, 0.05), 0.03, "rust", seed=300 + int(x * 10), stretch=(0.7, 1.4)))
    p.append(L.box((W, D, PL), (0, -D / 2, BR), "wood", bevel=0.008))
    p.append(L.box((W, 0.006, 0.008), (0, -D + 0.004, BR + PL - 0.008), "wood_light", bevel=0))
    for i, (x, s) in enumerate(((-0.25, 0.14), (0.15, 0.10), (0.40, 0.08))):
        p.append(L.spot((x, -D / 2, H), s, "wood_light" if i % 2 else "wood_dark", facing="top", seed=305 + i,
                        stretch=(1.6, 0.6)))
    p.append(L.spot((0.30, -D - 0.002, BR + 0.015), 0.04, "wood_light", seed=309))
    return p


def metallicheskaya_ugolkovaya():
    p = []
    PL = 0.025
    for x in (-(W / 2 - 0.03), W / 2 - 0.03):
        p.append(L.box((0.035, 0.035, H), (x, -0.0175, 0), "steel", bevel=0.003))                  # стойка-уголок
        p.append(L.box((0.035, D, 0.035), (x, -D / 2, 0.02), "steel", bevel=0.003))                # кронштейн
        for z in (0.06, 0.14, 0.22):
            p.append(L.box((0.012, 0.004, 0.02), (x, -0.037, z), "soot", bevel=0))                 # перфорация
        p.append(L.tube((x, -0.03, 0.08), (x, -D + 0.03, 0.04), 0.008, "steel_dark", verts=4))    # раскос
    p.append(L.box((W, D, PL), (0, -D / 2, H - PL), "steel_light", bevel=0.004))
    p.append(L.box((W, 0.02, 0.05), (0, -D + 0.01, H - 0.05), "steel", bevel=0.004))               # отбортовка
    for x in (-0.3, 0.0, 0.3):
        p.append(L.cyl(0.008, 0.006, (x, -D - 0.002, H - 0.025), "steel_dark", verts=6, rot=(90, 0, 0)))
    for i, (x, s, c) in enumerate(((-0.35, 0.06, "rust"), (0.2, 0.05, "rust_light"), (0.42, 0.04, "rust"))):
        p.append(L.spot((x, -D - 0.003, H - 0.03), s, c, seed=310 + i, stretch=(1.4, 0.6)))
    return p


def uglovaya():
    """Две доски — четверть круга (угол комнаты сзади-слева… в 2D видна как полукруглая полка на стойке)."""
    p = []
    import math
    R = W / 2
    pts = [(0.0, 0.0)] + [(R * math.cos(a), -R * 0.5 * math.sin(a)) for a in [math.pi * k / 8 for k in range(9)]]
    pts = [(x, y) for x, y in pts[1:]]          # полукруг (плоская задняя сторона — у стены)
    for z in (0.02, H - 0.03):
        p.append(L.prism(pts, "z", z, z + 0.025, "wood"))
        p.append(L.prism([(x * 1.0, y * 1.0) for x, y in pts], "z", z + 0.02, z + 0.026, "wood_light"))
    p.append(L.box((0.04, 0.03, H), (0, -0.015, 0), "wood_dark", bevel=0.006))                   # стойка у стены
    for sx in (-1, 1):
        p.append(L.box((0.025, 0.02, H - 0.03), (sx * (R - 0.05), -0.04, 0.02), "wood_dark", bevel=0.004))
    p.append(L.spot((0.1, -0.08, H - 0.004), 0.10, "wood_dark", facing="top", seed=320, stretch=(1.5, 0.6)))
    return p


def dvoynaya():
    p = []
    PL = 0.022
    for sx in (-1, 1):
        p.append(L.box((0.025, D, H), (sx * (W / 2 - 0.0125), -D / 2, 0), "wood_dark", bevel=0.006))  # боковины
    for z in (0.0, H / 2 - PL / 2):
        p.append(L.box((W - 0.05, D - 0.01, PL), (0, -D / 2, z), "wood", bevel=0.006))
        p.append(L.box((W - 0.05, 0.004, 0.006), (0, -D + 0.004, z + PL - 0.006), "wood_light", bevel=0))
    p.append(L.box((W - 0.05, 0.02, 0.025), (0, -D + 0.01, H - 0.025), "wood", bevel=0.005))       # верхний брусок
    p.append(L.box((W - 0.05, 0.01, H - 0.01), (0, -0.005, 0.0), "wood_dark", bevel=0))             # задняя стенка
    for sx in (-1, 1):
        p.append(L.box((0.03, 0.006, 0.03), (sx * (W / 2 - 0.0125), -D - 0.003, H - 0.04), "steel_dark", bevel=0))
    for i, (x, z, s) in enumerate(((-0.3, H / 2 + 0.01, 0.12), (0.25, 0.02, 0.10))):
        p.append(L.spot((x, -D / 2, z + PL - 0.0), s, "wood_light", facing="top", seed=330 + i, stretch=(1.5, 0.6)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("derevyannaya", derevyannaya), ("metallicheskaya_ugolkovaya", metallicheskaya_ugolkovaya),
                    ("uglovaya", uglovaya), ("dvoynaya", dvoynaya)):
        L.make(fn, "container", "shelf_wood", var, size_cm=(W * 100, H * 100))   # в ОС не ломается
    L.save_blend("container", "shelf_wood")
