"""Готовое блюдо `meal_soup` (предмет). Размер — из плана ОС (15 × 10 см). Горячее/холодное (пар) — состояние игры.
Варианты (только idle): ovoschnoy_sup — миска супа с кусочками овощей и ложкой; myasnoe_ragu — миска рагу с кусками
мяса; kasha — жестяная миска каши с ложкой. Запуск: python3 models/item/meal_soup.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("meal_soup"))
ROUGH = {"min_area": 0.0008, "k": 0.03, "amp_max": 0.0015}


def bowl(p, color, food, bits, seed):
    r = 0.06
    p.append(L.cyl(0.035, 0.012, (0, 0, 0), color, verts=10))                              # ножка-донце
    p.append(L.cyl(0.04, 0.05, (0, 0, 0.01), color, verts=10, radius_top=r))
    p.append(L.cyl(r + 0.003, 0.006, (0, 0, 0.056), color, verts=10))                       # край
    p.append(L.cyl(r - 0.004, 0.004, (0, 0, 0.054), food, verts=10))                       # еда
    rnd = random.Random(seed)
    for k in range(6):
        c = bits[k % len(bits)]
        p.append(L.box((0.012, 0.012, 0.008), (rnd.uniform(-0.035, 0.035), rnd.uniform(-0.03, 0.03), 0.055), c,
                       rot=(0, 0, rnd.uniform(0, 90)), bevel=0))
    # ложка: черенок наружу вправо
    p.append(L.tube((0.0, 0.0, 0.058), (0.075, -0.01, 0.095), 0.004, "steel_light", verts=4))
    return p


def ovoschnoy_sup():
    return bowl([], "plastic_white", "hazard_yellow", ["paint_red", "plant", "wood_light"], 1)


def myasnoe_ragu():
    return bowl([], "cloth_red", "rust", ["rust_dark", "wood_light", "hazard_yellow"], 2)


def kasha():
    p = []
    bowl(p, "steel", "cloth_beige", ["khaki_light", "wood_light"], 3)
    p.append(L.spot((-0.02, -0.065, 0.035), 0.015, "steel_dark", seed=910))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("ovoschnoy_sup", ovoschnoy_sup), ("myasnoe_ragu", myasnoe_ragu), ("kasha", kasha)):
        L.make(fn, "item", "meal_soup", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "meal_soup")
