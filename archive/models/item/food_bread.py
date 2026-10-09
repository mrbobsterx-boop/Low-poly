"""Хлеб `food_bread` (предмет). Размер — из плана ОС (20 × 10 см). Варианты (только idle; «заплесневевший» — пропуск,
черствение/плесень — состояния игры):
  hleb — буханка «кирпичик»: верхняя корка темнее, надрезы; suhari — горка сухарей; lepeshka — плоская лепёшка.
Запуск: python3 models/item/food_bread.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("food_bread"))
ROUGH = {"min_area": 0.001, "k": 0.03, "amp_max": 0.003}


def hleb():
    p = [L.box((W, 0.10, H * 0.65), (0, 0, 0), "wood_light", bevel=0.015)]
    p.append(L.soft((W - 0.006, 0.10 - 0.006, H * 0.45), (0, 0, H * 0.55), "wood"))           # верхняя корка
    for x in (-0.05, 0.0, 0.05):
        p.append(L.box((0.008, 0.07, 0.006), (x, 0, H - 0.005), "wood_light", rot=(0, 0, 20), bevel=0))
    return p


def suhari():
    r = random.Random(4)
    p = []
    for k in range(9):
        lay = 0 if k < 5 else (1 if k < 8 else 2)
        x = -0.07 + (k if k < 5 else (k - 5) * 1.3 + 0.6 if k < 8 else 2) * 0.035
        p.append(L.box((0.05, 0.035, 0.03), (x, r.uniform(-0.03, 0.03), lay * 0.03), r.choice(["wood_light", "wood", "cloth_beige"]),
                       rot=(0, r.uniform(-10, 10), r.uniform(-30, 30)), bevel=0.006))
    return p


def lepeshka():
    p = [L.cyl(W / 2 - 0.005, 0.025, (0, 0, 0), "wood_light", verts=10, radius_top=W / 2 - 0.02)]
    p.append(L.cyl(W / 2 - 0.03, 0.005, (0, 0, 0.022), "cloth_beige", verts=10))
    rnd = random.Random(5)
    for k in range(6):
        p.append(L.spot((rnd.uniform(-0.05, 0.05), rnd.uniform(-0.05, 0.05), 0.0275), 0.012, "wood_dark", facing="top", seed=880 + k))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("hleb", hleb), ("suhari", suhari), ("lepeshka", lepeshka)):
        L.make(fn, "item", "food_bread", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "food_bread")
