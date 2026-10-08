"""Обезболивающее `painkiller` (предмет). Размер — из плана ОС (6 × 8 см). Варианты (только idle):
  tabletki — блистер с таблетками в картонной пачке; ampula — 2 ампулы и шприц; silnoe — оранжевая баночка с белой крышкой.
Запуск: python3 models/item/painkiller.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("painkiller"))
ROUGH = {"min_area": 0.0004, "k": 0.02, "amp_max": 0.001}


def tabletki():
    p = [L.box((W, 0.02, H), (0, 0.01, 0), "offwhite", bevel=0.003)]                          # пачка
    p.append(L.box((W - 0.004, 0.003, 0.025), (0, -0.0015, 0.045), "paint_blue", bevel=0))
    bl = L.box((0.045, 0.004, 0.06), (0, 0, 0), "steel_light", bevel=0)                         # блистер, прислонён
    L.transform([bl], (0.0, -0.012, 0.0), (-8, 0, 0))
    p.append(bl)
    for i in range(2):
        for j in range(3):
            p.append(L.cyl(0.006, 0.004, (-0.01 + i * 0.02, -0.018, 0.012 + j * 0.017), "plastic_white", verts=6, rot=(90, 0, 0)))
    return p


def ampula():
    p = []
    for x in (-0.018, 0.0):
        p.append(L.cyl(0.006, 0.045, (x, 0, 0), "glass", verts=6))
        p.append(L.cyl(0.005, 0.03, (x, 0, 0.003), "rust_light", verts=6))
        p.append(L.cyl(0.003, 0.012, (x, 0, 0.045), "glass", verts=6, radius_top=0.004))
        p.append(L.cyl(0.0065, 0.004, (x, 0, 0.03), "paint_red", verts=6))
    p.append(L.cyl(0.006, 0.05, (0.022, 0, 0), "plastic_white", verts=6))                        # шприц
    p.append(L.cyl(0.0015, 0.02, (0.022, 0, 0.05), "steel_light", verts=4))
    p.append(L.box((0.016, 0.004, 0.004), (0.022, 0, 0.0), "plastic_white", bevel=0))
    return p


def silnoe():
    r = 0.022
    p = [L.cyl(r, 0.06, (0, 0, 0), "hazard_yellow", verts=8)]
    p.append(L.cyl(r + 0.003, 0.018, (0, 0, 0.06), "plastic_white", verts=8))
    p.append(L.cyl(r + 0.001, 0.03, (0, 0, 0.012), "offwhite", verts=8))
    p.append(L.box((0.02, 0.003, 0.006), (0, -r - 0.002, 0.024), "paint_red", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("tabletki", tabletki), ("ampula", ampula), ("silnoe", silnoe)):
        L.make(fn, "item", "painkiller", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "painkiller")
