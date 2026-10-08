"""Сырое мясо `meat_raw` (предмет). Размер — из плана ОС (15 × 8 см). Варианты (только idle; «тухлое» — пропуск,
порча — состояние игры):
  krolik — тушка кролика (без шкуры), лапки; sobaka — кусок мяса с костью (тёмнее); ptitsa — ощипанная птица.
Запуск: python3 models/item/meat_raw.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("meat_raw"))
ROUGH = {"min_area": 0.0008, "k": 0.03, "amp_max": 0.002}


def krolik():
    p = [L.soft((0.09, 0.05, 0.05), (0, 0, 0), "cloth_red")]
    p.append(L.soft((0.04, 0.04, 0.04), (-0.055, 0, 0.002), "cloth_red"))                     # голова/шея
    for x in (0.035, 0.05):                                                                  # задние лапки
        p.append(L.tube((x, -0.01, 0.015), (x + 0.025, -0.01, 0.005), 0.006, "skin_light", verts=4))
    p.append(L.spot((0.0, -0.026, 0.025), 0.015, "offwhite", seed=890, stretch=(1.6, 0.6)))   # жир
    return p


def sobaka():
    p = [L.soft((0.12, 0.06, 0.06), (0, 0, 0), "blood")]
    p.append(L.tube((-W / 2 + 0.005, 0, 0.03), (-0.03, 0, 0.03), 0.009, "offwhite", verts=6))   # кость
    p.append(L.cyl(0.013, 0.01, (-W / 2 + 0.005, 0, 0.03), "plastic_white", verts=6, rot=(0, 90, 0)))
    p.append(L.spot((0.02, -0.031, 0.03), 0.02, "cloth_red", seed=891, stretch=(1.5, 0.6)))
    return p


def ptitsa():
    p = [L.soft((0.10, 0.07, 0.065), (0.005, 0, 0), "skin_light")]
    for s in (-1, 1):                                                                       # ножки
        p.append(L.tube((0.045, s * 0.02, 0.03), (0.07, s * 0.02, 0.045), 0.01, "skin_light", verts=5))
        p.append(L.cyl(0.006, 0.01, (0.072, s * 0.02, 0.046), "offwhite", verts=5, rot=(0, 90, 0)))
    p.append(L.spot((-0.02, -0.036, 0.035), 0.02, "skin_mid", seed=892))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("krolik", krolik), ("sobaka", sobaka), ("ptitsa", ptitsa)):
        L.make(fn, "item", "meat_raw", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "meat_raw")
