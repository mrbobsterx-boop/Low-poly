"""Зерно `food_grain` (предмет). Размер — из плана ОС (15 × 15 см). Варианты (только idle):
  pshenitsa — сноп колосьев, перевязанный бечёвкой; kukuruza — 2 початка с листьями; ris — мешочек риса, горловина завязана.
Запуск: python3 models/item/food_grain.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("food_grain"))
ROUGH = {"min_area": 0.0008, "k": 0.03, "amp_max": 0.002}


def pshenitsa():
    p = []
    for k in range(7):
        a = math.radians(-33 + k * 11)
        top = (math.sin(a) * 0.10, (k % 2) * 0.01, 0.10 + math.cos(a) * 0.0)
        p.append(L.tube((math.sin(a) * 0.012, 0, 0.0), (top[0], top[1], 0.10), 0.0035, "khaki", verts=4))
        p.append(L.cyl(0.009, 0.05, (top[0], top[1], 0.095), "khaki_light", verts=5, radius_top=0.003,
                       rot=(0, math.degrees(a), 0)))
    p.append(L.cyl(0.018, 0.012, (0, 0, 0.04), "wood_dark", verts=6))                           # бечёвка
    return p


def kukuruza():
    p = []
    for x, a in ((-0.03, 14), (0.035, -10)):
        c = L.cyl(0.025, 0.12, (0, 0, 0), "hazard_yellow", verts=8, radius_top=0.015)
        L.transform([c], (x, 0, 0.02), (0, a, 0))
        p.append(c)
        for s in (-1, 1):                                                                     # листья-обёртка
            lf = L.poly([(-0.02, 0.0), (0.02, 0.0), (0.0, 0.10)], 0.004, (0, 0, 0), "plant")
            L.transform([lf], (x + s * 0.02, -0.02, 0.0), (0, a + s * 18, 0))
            p.append(lf)
    return p


def ris():
    p = [L.soft((0.12, 0.08, 0.10), (0, 0, 0), "cloth_beige")]
    p.append(L.cyl(0.03, 0.03, (0, 0, 0.10), "cloth_beige", verts=6, radius_top=0.04))        # горловина
    p.append(L.cyl(0.033, 0.01, (0, 0, 0.105), "wood_dark", verts=6))                           # завязка
    p.append(L.box((0.05, 0.003, 0.03), (0, -0.041, 0.03), "offwhite", bevel=0))                 # штамп
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("pshenitsa", pshenitsa), ("kukuruza", kukuruza), ("ris", ris)):
        L.make(fn, "item", "food_grain", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "food_grain")
