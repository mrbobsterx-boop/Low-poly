"""Овощи `veg_potato` (предмет). Размер — из плана ОС (8 × 8 см). Варианты (только idle):
  kartofel — картофелина с глазками; morkov — морковь с ботвой; pomidor — помидор с хвостиком; luk — луковица.
Запуск: python3 models/item/veg_potato.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("veg_potato"))
ROUGH = {"min_area": 0.0004, "k": 0.03, "amp_max": 0.0015}


def kartofel():
    p = [L.soft((0.08, 0.06, 0.055), (0, 0, 0), "wood_light")]
    for i, (x, z) in enumerate(((-0.02, 0.03), (0.015, 0.02), (0.025, 0.04))):
        p.append(L.spot((x, -0.031, z), 0.006, "wood", seed=900 + i))
    return p


def morkov():
    p = [L.cyl(0.016, 0.065, (0, 0, 0), "hazard_yellow", verts=6, radius_top=0.003, rot=(0, -90, 0))]
    L.transform(p, (0.035, 0, 0.016))
    p[0].data.vertices  # noqa
    for a in (-25, 0, 25):                                                                   # ботва
        lf = L.poly([(-0.004, 0.0), (0.004, 0.0), (0.0, 0.05)], 0.003, (0, 0, 0), "plant")
        L.transform([lf], (-0.03, 0, 0.016), (0, a - 60, 0))
        p.append(lf)
    return p


def pomidor():
    p = [L.cyl(0.035, 0.05, (0, 0, 0), "paint_red", verts=10)]
    L.transform([p[0]], (0, 0, 0))
    p[0] = L.soft((0.075, 0.07, 0.06), (0, 0, 0), "paint_red")
    p.append(L.cyl(0.012, 0.006, (0, 0, 0.06), "plant", verts=5))
    p.append(L.cyl(0.002, 0.012, (0, 0, 0.064), "plant_dark", verts=4))
    return p


def luk():
    p = [L.soft((0.065, 0.06, 0.055), (0, 0, 0), "rust_light")]
    p.append(L.cyl(0.018, 0.022, (0, 0, 0.05), "rust_light", verts=6, radius_top=0.004))
    p.append(L.cyl(0.004, 0.02, (0, 0, 0.07), "khaki", verts=4, radius_top=0.001))
    p.append(L.spot((0.012, -0.031, 0.025), 0.012, "rust", seed=905, stretch=(0.5, 1.6)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("kartofel", kartofel), ("morkov", morkov), ("pomidor", pomidor), ("luk", luk)):
        L.make(fn, "item", "veg_potato", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "veg_potato")
