"""Печь `stove_heat`. Размер — из плана ОС (60 × 90 см). Огонь — светящийся материал (горит/не горит — игра).
Варианты (только idle):
  stalnaya_bochka — буржуйка из бочки: обручи, дверца с решёткой огня, поддувало, дымоход, ножки;
  kirpichnaya     — кирпичная: кладка (кирпичи разных оттенков), чугунная дверца и плита, кирпичная труба;
  pohodnaya       — походная: стальной короб на ножках, окошко огня, складная труба, ручки.
Запуск: python3 models/machine/stove_heat.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("stove_heat"))
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


def kirpichnaya():
    p = []
    import random
    r = random.Random(7)
    BW, BH, D = 0.56, 0.62, 0.50
    bk_w, bk_h = 0.12, 0.065
    rows = int(BH / bk_h)
    p.append(L.box((BW - 0.02, D - 0.02, BH), (0, 0, 0), "soot", bevel=0))                          # раствор (швы)
    for j in range(rows):
        off = 0 if j % 2 == 0 else bk_w / 2
        x = -BW / 2 - off
        while x < BW / 2:
            x0, x1 = max(x, -BW / 2), min(x + bk_w, BW / 2)
            if x1 - x0 > 0.02:
                c = r.choice(["brick", "brick", "rust", "rust_light"])
                p.append(L.box((x1 - x0 - 0.008, D, bk_h - 0.008), ((x0 + x1) / 2, 0, j * bk_h + 0.004), c, bevel=0.006))
            x += bk_w
    p.append(L.box((BW + 0.03, D + 0.03, 0.03), (0, 0, BH), "steel_dark", bevel=0.006))             # чугунная плита
    p.append(L.cyl(0.08, 0.012, (0.10, 0.0, BH + 0.03), "soot", verts=8))                            # конфорка
    F = -D / 2
    p.append(L.box((0.24, 0.02, 0.20), (0, F - 0.006, 0.26), "soot", bevel=0.006))                   # дверца топки
    p.append(L.box((0.20, 0.012, 0.16), (0, F - 0.014, 0.28), "steel_dark", bevel=0.005))
    p.append(L.box((0.14, 0.006, 0.08), (0, F - 0.02, 0.32), "glow_fire", glow=True, bevel=0))
    for x in (-0.04, 0.0, 0.04):
        p.append(L.box((0.012, 0.01, 0.09), (x + 0.02, F - 0.024, 0.315), "soot", bevel=0.002))
    p.append(L.box((0.05, 0.025, 0.018), (0.12, F - 0.03, 0.34), "steel_light", bevel=0.005))
    p.append(L.box((0.18, 0.016, 0.06), (0, F - 0.004, 0.06), "steel_dark", bevel=0.004))             # поддувало
    # кирпичная труба
    for j in range(round((H - BH - 0.03) / bk_h)):
        for k in range(2):
            p.append(L.box((0.10, 0.20, bk_h - 0.008), (-0.06 + k * 0.11 + (0.0 if j % 2 else 0.0), 0.12,
                                                     BH + 0.03 + j * bk_h + 0.004), r.choice(["brick", "rust"]), bevel=0.006))
    p.append(L.spot((-0.18, F - 0.002, 0.45), 0.10, "soot", seed=410, stretch=(0.8, 1.6)))           # копоть
    p.append(L.spot((0.0, F - 0.002, 0.48), 0.12, "soot", seed=411, stretch=(1.2, 0.9)))
    return p


def pohodnaya():
    p = []
    BW, BH, D, LG = 0.44, 0.30, 0.34, 0.16
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.tube((sx * (BW / 2 - 0.03), sy * (D / 2 - 0.03), LG), (sx * (BW / 2 + 0.01), sy * (D / 2 + 0.01), 0),
                            0.01, "steel_dark", verts=4))
    p.append(L.box((BW, D, BH), (0, 0, LG), "steel_dark", bevel=0.012))
    p.append(L.box((BW + 0.01, D + 0.01, 0.015), (0, 0, LG + BH), "soot", bevel=0.004))
    F = -D / 2
    p.append(L.box((0.20, 0.012, 0.14), (-0.05, F - 0.006, LG + 0.08), "soot", bevel=0.005))          # дверца
    p.append(L.box((0.14, 0.006, 0.06), (-0.05, F - 0.013, LG + 0.12), "glow_fire", glow=True, bevel=0))   # окошко
    for x in (-0.09, -0.05, -0.01):
        p.append(L.box((0.008, 0.008, 0.07), (x, F - 0.016, LG + 0.115), "soot", bevel=0))
    p.append(L.box((0.04, 0.02, 0.015), (0.08, F - 0.016, LG + 0.15), "steel_light", bevel=0.004))
    for sx in (-1, 1):                                                                                 # ручки
        p.append(L.tube((sx * (BW / 2), -0.08, LG + BH - 0.06), (sx * (BW / 2 + 0.06), -0.08, LG + BH - 0.06), 0.008, "steel", verts=6))
        p.append(L.tube((sx * (BW / 2 + 0.06), -0.08, LG + BH - 0.06), (sx * (BW / 2 + 0.06), 0.08, LG + BH - 0.06), 0.008, "steel", verts=6))
        p.append(L.tube((sx * (BW / 2), 0.08, LG + BH - 0.06), (sx * (BW / 2 + 0.06), 0.08, LG + BH - 0.06), 0.008, "steel", verts=6))
    # складная труба: секции разного оттенка
    z = LG + BH
    for k, c in enumerate(("steel", "steel_light", "steel", "steel_light")):
        h = (H - z) / 4
        p.append(L.cyl(0.04 - k * 0.003, h + 0.01, (0.12, 0.05, z + k * h), c, verts=8))
    p.append(L.cyl(0.05, 0.015, (0.12, 0.05, H - 0.015), "soot", verts=8))
    for i, (x, zz) in enumerate(((0.15, LG + 0.05), (-0.18, LG + 0.25))):
        p.append(L.spot((x, F - 0.002, zz), 0.05, "rust", seed=420 + i))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("stalnaya_bochka", stove_idle), ("kirpichnaya", kirpichnaya), ("pohodnaya", pohodnaya)):
        L.make(fn, "machine", "stove_heat", var, size_cm=(W * 100, H * 100), broken="legs")
    L.save_blend("machine", "stove_heat")
