"""Бинт `bandage` (предмет). Размер — из плана ОС (10 × 6 см). Варианты (только idle):
  sterilnyy — рулон в бумажной упаковке с красным крестом; samodelnyy_iz_tkani — скатанная полоска ткани, хвост;
  elastichnyy — эластичный бинт телесного цвета с застёжкой. Запуск: python3 models/item/bandage.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("bandage"))
ROUGH = {"min_area": 0.0004, "k": 0.02, "amp_max": 0.001}


def cross(p, x, y, z, s, col="paint_red"):
    p.append(L.box((s, 0.003, s * 0.33), (x, y, z - s * 0.165), col, bevel=0))
    p.append(L.box((s * 0.33, 0.003, s), (x, y, z - s / 2), col, bevel=0))


def sterilnyy():
    p = [L.box((W - 0.01, 0.05, H), (0, 0, 0), "offwhite", bevel=0.004)]
    p.append(L.box((W - 0.005, 0.052, 0.008), (0, 0, H - 0.008), "plastic_white", bevel=0))    # склейка
    cross(p, -0.02, -0.026, H * 0.55, 0.025)
    p.append(L.box((0.03, 0.003, 0.006), (0.022, -0.026, H * 0.5), "paint_blue", bevel=0))
    return p


def samodelnyy_iz_tkani():
    p = [L.cyl(0.028, 0.05, (0, 0, 0.028), "cloth_beige", verts=8, rot=(90, 0, 0))]
    L.transform([p[0]], (-0.015, 0.025, 0))
    p.append(L.cyl(0.01, 0.052, (-0.015, 0.026, 0.028), "dirt", verts=6, rot=(90, 0, 0)))          # серединка
    p.append(L.sheet(3, 1, 0.05, 0.045, (0.03, 0.0, 0.004), "cloth_beige", jitter=0.002, thick=0.003, seed=3))  # хвост
    p.append(L.spot((-0.02, -0.002, 0.03), 0.01, "blood", seed=920))
    return p


def elastichnyy():
    p = [L.cyl(0.03, 0.06, (0, 0, 0.03), "skin_mid", verts=10, rot=(90, 0, 0))]
    L.transform([p[0]], (0, 0.03, 0))
    p.append(L.cyl(0.012, 0.062, (0, 0.031, 0.03), "skin_light", verts=8, rot=(90, 0, 0)))
    p.append(L.box((0.015, 0.02, 0.012), (0.035, -0.0, 0.0), "steel_light", bevel=0.002))       # застёжка
    p.append(L.box((0.04, 0.05, 0.004), (0.028, 0.0, 0.0), "skin_mid", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("sterilnyy", sterilnyy), ("samodelnyy_iz_tkani", samodelnyy_iz_tkani), ("elastichnyy", elastichnyy)):
        L.make(fn, "item", "bandage", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "bandage")
