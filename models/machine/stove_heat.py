"""Буржуйка `stove_heat`, вариант `stalnaya_bochka` (стальная бочка). ОС: 60 × 90 см. Образец: docs/ref/machine/stove_heat.png
Версия 2 (подробная): 12-гранная бочка с обручами, дверца в рамке с решёткой огня (светится), петли, ручка,
поддувало, крышка-плита, дымоход с муфтой, разведённые ножки, заклёпки.
Запуск: python3 models/machine/stove_heat.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = 0.60, 0.90
R = 0.23
LEGS = 0.10
BARREL = 0.62
N = 12


def stove_idle():
    p = []
    zb = LEGS
    # ножки: три, разведены в стороны
    for x, y, rx, ry in ((-0.15, -0.12, 0, -12), (0.15, -0.12, 0, 12), (0.0, 0.17, 12, 0)):
        p.append(L.box((0.035, 0.035, LEGS + 0.03), (x, y, 0), "soot", rot=(rx, ry, 0), bevel=0.006))
        p.append(L.box((0.06, 0.05, 0.012), (x * 1.25, y * 1.1, 0), "soot", bevel=0.004))
    # бочка с обручами и заклёпками
    p.append(L.cyl(R, BARREL, (0, 0, zb), "steel_dark", verts=N))
    for z in (zb + 0.03, zb + BARREL * 0.5 - 0.012, zb + BARREL - 0.05):
        p.append(L.cyl(R + 0.012, 0.024, (0, 0, z), "rust_dark", verts=N))
    p.append(L.cyl(R + 0.008, 0.025, (0, 0, zb + BARREL), "steel_dark", verts=N))            # плита-крышка
    # боковые ручки-скобы (по ним ширина 60 см)
    for sx in (-1, 1):
        p.append(L.box((0.07, 0.025, 0.022), (sx * (R + 0.035), 0, zb + BARREL - 0.10), "soot", bevel=0.005))
        p.append(L.box((0.022, 0.025, 0.08), (sx * (R + 0.059), 0, zb + BARREL - 0.18), "soot", bevel=0.005))
    p.append(L.cyl(0.10, 0.012, (0.10, -0.05, zb + BARREL + 0.025), "steel_dark", verts=8))  # конфорка
    # ржавые потёки на бочке — тонкие «заплатки» точно на передних гранях
    import math
    for ang, z, h in ((-50, zb + 0.36, 0.12), (40, zb + 0.06, 0.09)):
        a = math.radians(ang - 90)
        r = R * math.cos(math.pi / N) + 0.002
        p.append(L.box((0.05, 0.004, h), (r * math.cos(a), r * math.sin(a), z), "rust", rot=(0, 0, ang), bevel=0))
    # дверца топки: рамка, дверца, решётка огня (светится), петли, ручка
    y = -R - 0.004
    p.append(L.box((0.25, 0.02, 0.21), (0, y + 0.004, zb + 0.20), "soot", bevel=0.006))
    p.append(L.box((0.21, 0.016, 0.17), (0, y - 0.008, zb + 0.22), "steel_dark", bevel=0.006))
    p.append(L.box((0.15, 0.006, 0.09), (0, y - 0.015, zb + 0.26), "glow_fire", glow=True, bevel=0))
    for x in (-0.05, 0, 0.05):
        p.append(L.box((0.016, 0.01, 0.10), (x + 0.025, y - 0.02, zb + 0.255), "soot", bevel=0.002))
    p.append(L.box((0.006, 0.012, 0.10), (-0.075, y - 0.02, zb + 0.255), "soot", bevel=0))
    for z in (zb + 0.24, zb + 0.35):
        p.append(L.cyl(0.01, 0.035, (-0.115, y - 0.012, z), "steel", verts=6))
    p.append(L.box((0.05, 0.03, 0.018), (0.12, y - 0.028, zb + 0.30), "steel_light", bevel=0.005))
    # поддувало
    p.append(L.box((0.16, 0.016, 0.05), (0, y - 0.004, zb + 0.08), "steel_dark", bevel=0.004))
    p.append(L.box((0.10, 0.006, 0.012), (0, y - 0.014, zb + 0.10), "soot", bevel=0))
    # дымоход: муфта, труба, верхний обрез
    yc = 0.08
    p.append(L.cyl(0.075, 0.04, (0, yc, zb + BARREL + 0.02), "rust_dark", verts=8))
    p.append(L.cyl(0.055, H - zb - BARREL - 0.06, (0, yc, zb + BARREL + 0.06), "steel", verts=8))
    p.append(L.cyl(0.065, 0.025, (0, yc, H - 0.025), "steel_dark", verts=8))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(stove_idle, "machine", "stove_heat", "stalnaya_bochka", size_cm=(60, 90), broken="legs")
    L.save_blend("machine", "stove_heat")
