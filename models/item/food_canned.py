"""Консервы `food_canned` (предмет). Размер — из плана ОС (8 × 10 см). Варианты (только idle; «вздувшаяся» — пропуск):
  tushenka — тушёнка: банка с бумажной этикеткой (коровья голова — пятно); fasol — фасоль: зелёная этикетка;
  rybnye   — рыбные: низкая плоская банка с ключом; sguschenka — сгущёнка: голубая этикетка.
Запуск: python3 models/item/food_canned.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("food_canned"))
ROUGH = {"min_area": 0.0006, "k": 0.02, "amp_max": 0.0012}
N = 10


def can(label, mark, h=H, r=W / 2 - 0.002, seed=0):
    p = [L.cyl(r, h, (0, 0, 0), "steel", verts=N)]
    for z in (0.0, h - 0.006):                                                                 # закатка
        p.append(L.cyl(r + 0.002, 0.006, (0, 0, z), "steel_light", verts=N))
    p.append(L.cyl(r + 0.001, h * 0.66, (0, 0, h * 0.17), label, verts=N))                     # этикетка
    p.append(L.box((r * 0.9, 0.003, h * 0.25), (0, -r - 0.001, h * 0.38), mark, bevel=0))
    p.append(L.box((r * 1.2, 0.003, 0.006), (0, -r - 0.001, h * 0.70), "offwhite", bevel=0))
    p.append(L.spot((r * 0.4, -r - 0.003, h * 0.2), 0.012, "rust", seed=870 + seed))
    return p


def tushenka():
    return can("cloth_beige", "paint_red", seed=1)


def fasol():
    return can("plant", "offwhite", seed=2)


def sguschenka():
    return can("paint_blue", "offwhite", h=0.08, seed=3)


def rybnye():
    p = [L.box((W, 0.05, 0.03), (0, 0, 0), "steel_light", bevel=0.008)]                         # плоская банка
    p.append(L.box((W - 0.006, 0.045, 0.002), (0, 0, 0.03), "steel", bevel=0.002))
    p.append(L.box((W + 0.001, 0.051, 0.016), (0, 0, 0.007), "paint_blue", bevel=0.004))       # этикетка
    p.append(L.box((0.03, 0.003, 0.008), (0, -0.027, 0.011), "offwhite", bevel=0))
    p.append(L.tube((-W / 2, -0.02, 0.032), (W / 2 - 0.01, -0.02, 0.032), 0.003, "steel_light", verts=4))   # ключ
    p.append(L.box((0.012, 0.012, 0.004), (-W / 2 - 0.004, -0.02, 0.03), "steel_light", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("tushenka", tushenka), ("fasol", fasol), ("rybnye", rybnye), ("sguschenka", sguschenka)):
        L.make(fn, "item", "food_canned", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "food_canned")
