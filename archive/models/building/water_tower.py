"""Водонапорная башня `water_tower` (здание, улица). Размер — из плана ОС (400 × 1000 см). Варианты (только idle;
«разрушенная» — пропуск): kirpichnaya — кирпичный ствол с окнами, деревянный бак-«шапка» с крышей;
stalnaya_na_oporah — стальной бак на решётчатых опорах, лестница, трубы. Запуск: python3 models/building/water_tower.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("water_tower"))
ROUGH = {"min_area": 0.4, "k": 0.03, "amp_max": 0.05, "shade_p": 0.45}


def kirpichnaya():
    p = []
    Rb, Hb = 1.30, 6.5
    for k in range(13):                                                               # кирпичные пояса (оттенки)
        p.append(L.cyl(Rb - k * 0.015, Hb / 13 + 0.005, (0, 0, k * Hb / 13), "brick" if k % 3 else "rust", verts=12,
                       radius_top=Rb - (k + 1) * 0.015))
    p.append(L.cyl(Rb + 0.08, 0.30, (0, 0, 0), "concrete_dark", verts=12))                            # цоколь
    p.append(L.cyl(Rb - 0.10, 0.25, (0, 0, Hb), "brick", verts=12, radius_top=W / 2 - 0.05))         # карниз-расширение
    # бак — деревянная «шапка», крыша-шатёр
    p.append(L.cyl(W / 2 - 0.05, 1.8, (0, 0, Hb + 0.25), "wood", verts=14))
    for z in (Hb + 0.6, Hb + 1.2, Hb + 1.8):
        p.append(L.cyl(W / 2 - 0.03, 0.06, (0, 0, z), "steel_dark", verts=14))
    p.append(L.cyl(W / 2, H - Hb - 2.05, (0, 0, Hb + 2.05), "rust_dark", verts=14, radius_top=0.15))  # крыша
    for k in range(5):                                                                # окна и дверь
        z = 1.3 + k * 1.05
        p.append(L.box((0.35, 0.05, 0.60), (0, -Rb + 0.02 + k * 0.015, z), "soot", bevel=0.02))
        p.append(L.cyl(0.175, 0.05, (0, -Rb + 0.03 + k * 0.015, z + 0.60), "soot", verts=8, rot=(90, 0, 0)))
    p.append(L.box((0.80, 0.10, 1.6), (0, -Rb - 0.03, 0.10), "wood_dark", bevel=0.02))               # дверь
    p.append(L.box((0.95, 0.12, 0.10), (0, -Rb - 0.04, 1.70), "concrete_dark", bevel=0.01))
    for i, (x, z, s, c) in enumerate(((-0.6, 2.5, 0.8, "concrete"), (0.5, 4.0, 0.6, "soot"), (0.2, 0.8, 0.7, "plant_dark"),
                                      (-0.4, 5.6, 0.5, "concrete"))):
        p.append(L.spot((x, -Rb * 0.97, z), s, c, seed=570 + i, stretch=(0.9, 1.3)))
    return p


def stalnaya_na_oporah():
    p = []
    Rt, Zt = 1.70, 6.0
    feet = [(-1.6, -1.2), (1.6, -1.2), (-1.6, 1.2), (1.6, 1.2)]
    top = [(-1.1, -0.8), (1.1, -0.8), (-1.1, 0.8), (1.1, 0.8)]
    for (x0, y0), (x1, y1) in zip(feet, top):                                          # опоры
        p.append(L.tube((x0, y0, 0), (x1, y1, Zt), 0.08, "steel_dark", verts=6))
        p.append(L.box((0.4, 0.4, 0.3), (x0, y0, 0), "concrete", bevel=0.03))
    for z in (1.5, 3.0, 4.5):                                                          # пояса и раскосы спереди
        t = z / Zt
        xl, xr = -1.6 + 0.5 * t, 1.6 - 0.5 * t
        y = -1.2 + 0.4 * t
        p.append(L.tube((xl, y, z), (xr, y, z), 0.04, "steel_dark", verts=6))
    for z0, z1 in ((0, 1.5), (1.5, 3.0), (3.0, 4.5), (4.5, 6.0)):
        t0, t1 = z0 / Zt, z1 / Zt
        p.append(L.tube((-1.6 + 0.5 * t0, -1.2 + 0.4 * t0, z0), (1.6 - 0.5 * t1, -1.2 + 0.4 * t1, z1), 0.03, "steel_dark", verts=4))
        p.append(L.tube((1.6 - 0.5 * t0, -1.2 + 0.4 * t0, z0), (-1.6 + 0.5 * t1, -1.2 + 0.4 * t1, z1), 0.03, "steel_dark", verts=4))
    p.append(L.cyl(Rt + 0.3, 0.12, (0, 0, Zt), "steel", verts=14))                                     # площадка
    p.append(L.cyl(Rt, 2.6, (0, 0, Zt + 0.12), "paint_blue", verts=14))                                # бак
    for z in (Zt + 0.8, Zt + 1.6, Zt + 2.4):
        p.append(L.cyl(Rt + 0.02, 0.06, (0, 0, z), "steel_dark", verts=14))
    p.append(L.cyl(Rt, H - Zt - 2.72, (0, 0, Zt + 2.72), "paint_blue", verts=14, radius_top=0.2))      # купол
    for k in range(10):                                                                # перила площадки
        a = math.pi + k * math.pi / 9
        x, y = (Rt + 0.28) * math.cos(a), (Rt + 0.28) * math.sin(a) * 0.6
        p.append(L.tube((x, y - 0.0, Zt + 0.12), (x, y, Zt + 1.0), 0.02, "steel", verts=4))
    p.append(L.tube((-(Rt + 0.28), -0.0, Zt + 1.0), (Rt + 0.28, 0.0, Zt + 1.0), 0.025, "steel", verts=4))
    for side in (-1, 1):                                                               # лестница
        p.append(L.tube((0.9 + side * 0.2, -1.35, 0), (0.9 + side * 0.2, -1.35, Zt + 1.0), 0.025, "steel", verts=4))
    for k in range(22):
        p.append(L.tube((0.7, -1.35, 0.3 + k * 0.3), (1.1, -1.35, 0.3 + k * 0.3), 0.02, "steel", verts=4))
    p.append(L.tube((-0.5, -0.4, 0), (-0.5, -0.4, Zt), 0.12, "steel", verts=8))                      # труба
    for i, (x, z, s) in enumerate(((-0.8, Zt + 0.6, 0.8), (0.6, Zt + 1.8, 0.6), (0.2, Zt + 1.1, 0.5))):
        p.append(L.spot((x, -Rt * 0.97, z), s, "rust", seed=580 + i, stretch=(0.6, 1.8)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("kirpichnaya", kirpichnaya), ("stalnaya_na_oporah", stalnaya_na_oporah)):
        L.make(fn, "building", "water_tower", var, size_cm=(W * 100, H * 100), limit="room", rough=ROUGH)
    L.save_blend("building", "water_tower")
