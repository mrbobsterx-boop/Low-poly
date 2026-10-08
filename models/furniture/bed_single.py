"""Кровать `bed_single`, вариант `derevyannaya_samodelnaya` (деревянная самодельная). ОС: 200 × 60 см.
Как на референсе автора (docs/ref/style): деревянная рама, спинка с планками, матрас, подушка, мятое одеяло из граней
со свесом вперёд. Высота по ОС — 60 см (спинка невысокая).
Запуск: python3 models/furniture/bed_single.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 2.00, 0.90, 0.60
POST = 0.07
RAIL_Z = 0.20            # низ царги
MAT_Z = 0.30             # верх рамы = низ матраса
MAT_H = 0.12


def bed_idle():
    p = []
    # стойки: изголовье (слева) до 60 см, изножье ниже
    for sx, h in ((-1, H), (1, 0.48)):
        for sy in (-1, 1):
            x = sx * (W / 2 - POST / 2)
            p.append(L.box((POST, POST, h), (x, sy * (D / 2 - POST / 2), 0), "wood_dark", bevel=0.01))
            p.append(L.box((POST + 0.012, POST + 0.012, 0.025), (x, sy * (D / 2 - POST / 2), h - 0.025), "wood", bevel=0.006))
    # изголовье: верхняя доска + 4 планки + нижняя доска
    xh = -(W / 2 - POST / 2)
    p.append(L.box((0.045, D - 0.08, 0.08), (xh, 0, H - 0.12), "wood", bevel=0.008))
    p.append(L.box((0.04, D - 0.08, 0.06), (xh, 0, MAT_Z), "wood_dark", bevel=0.006))
    for y in (-0.25, -0.085, 0.085, 0.25):
        p.append(L.box((0.03, 0.06, H - 0.12 - MAT_Z - 0.06), (xh, y, MAT_Z + 0.06), "wood", bevel=0.005))
    # изножье: широкая доска
    xf = W / 2 - POST / 2
    p.append(L.box((0.045, D - 0.08, 0.14), (xf, 0, MAT_Z - 0.04), "wood", bevel=0.008))
    # царги (боковые доски рамы) — передняя видна целиком
    for sy in (-1, 1):
        p.append(L.box((W - 2 * POST, 0.035, MAT_Z - RAIL_Z), (0, sy * (D / 2 - 0.03), RAIL_Z), "wood", bevel=0.008))
    # матрас: светлый, с кантом
    mw, md = W - 2 * POST - 0.02, D - 0.10
    p.append(L.box((mw, md, MAT_H), (0, 0, MAT_Z), "cloth_beige", bevel=0.03))
    p.append(L.box((mw + 0.004, md + 0.004, 0.018), (0, 0, MAT_Z + 0.03), "offwhite", bevel=0.006))
    # подушка у изголовья: «пухлая» — фаска побольше
    p.append(L.box((0.45, md - 0.20, 0.13), (-(mw / 2 - 0.27), 0.02, MAT_Z + MAT_H - 0.01), "offwhite", rot=(0, -4, 0), bevel=0.04))
    # одеяло: мятое, из граней, лежит на матрасе и свешивается вперёд (к камере)
    top_z = MAT_Z + MAT_H + 0.02
    import random
    rnd = random.Random(11)
    hang = [0.10 + rnd.uniform(0.0, 0.10) for _ in range(13)]       # неровный край свеса

    def blanket_z(u, v):
        fold = 0.02 + 0.022 * math.sin(u * 9.0 + v * 2.0) ** 2 + 0.015 * math.sin(u * 17.0 - v * 5.0) ** 2
        if v < 0.16:                                    # свес вперёд: вниз по переднему краю матраса
            k = (0.16 - v) / 0.16
            return -hang[round(u * 12)] * k * 1.6 + fold * (1 - k)
        return fold
    bl = L.sheet(12, 9, 1.30, md + 0.20, (0.24, -0.06, top_z), "cloth_blue", z_fn=blanket_z, jitter=0.01, seed=7)
    p.append(bl)
    # загнутый край одеяла (светлая изнанка-простыня) ближе к подушке
    p.append(L.sheet(3, 6, 0.16, md - 0.04, (-0.47, 0.0, top_z + 0.005), "offwhite",
                     z_fn=lambda u, v: 0.03 * math.sin(u * math.pi), jitter=0.008, seed=3))
    # износ: потёртости рамы (светлое дерево), тёмные пятна, пятно на матрасе и на подушке
    yr = -(D / 2 - 0.03) - 0.018
    for i, (x, z, s, c) in enumerate(((-0.55, 0.26, 0.10, "wood_light"), (0.35, 0.24, 0.08, "wood_dark"),
                                      (0.70, 0.27, 0.06, "wood_light"), (-W / 2 + 0.035, 0.45, 0.04, "wood_light"))):
        p.append(L.spot((x, yr, z), s, c, seed=90 + i, stretch=(1.6, 0.6)))
    p.append(L.spot((-0.62, -(md / 2) - 0.002, MAT_Z + 0.06), 0.09, "khaki_light", seed=99, stretch=(1.3, 0.7)))
    p.append(L.spot((-(mw / 2 - 0.27), -0.05, MAT_Z + MAT_H + 0.125), 0.08, "cloth_beige", facing="top", seed=101))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(bed_idle(), "furniture", "bed_single", "derevyannaya_samodelnaya", "idle", size_cm=(200, 60))
    L.save_blend("furniture", "bed_single")
