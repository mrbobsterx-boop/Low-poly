"""Полка настенная `shelf_wood`, вариант `derevyannaya_metal_ugolok` (доска на металлических уголках). ОС: 100 × 30 см.
Висит на стене: «спина» в плоскости Y = 0, низ уголков — Z = 0. На полке — банки и бутылки (как на референсе).
Запуск: python3 models/container/shelf_wood.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 1.00, 0.24, 0.30
BR = 0.14                 # высота уголков
PL = 0.03                 # толщина доски


def can(p, x, r, h, body, lid, label=None):
    z = BR + PL
    p.append(L.cyl(r, h, (x, -D / 2, z), body, verts=8))
    p.append(L.cyl(r * 0.9, 0.012, (x, -D / 2, z + h), lid, verts=8))
    if label:
        p.append(L.cyl(r + 0.002, h * 0.4, (x, -D / 2, z + h * 0.25), label, verts=8))


def bottle(p, x, r, h, body, cap):
    z = BR + PL
    p.append(L.cyl(r, h * 0.65, (x, -D / 2, z), body, verts=8))
    p.append(L.cyl(r, h * 0.12, (x, -D / 2, z + h * 0.65), body, verts=8, radius_top=r * 0.45))
    p.append(L.cyl(r * 0.45, h * 0.23, (x, -D / 2, z + h * 0.77), cap, verts=6))


def shelf_idle():
    p = []
    # уголки (металл): вертикаль по стене + горизонталь под доской + косынка
    for x in (-0.36, 0.36):
        p.append(L.box((0.03, 0.02, BR), (x, -0.01, 0), "steel_dark", bevel=0.004))
        p.append(L.box((0.03, D - 0.02, 0.02), (x, -D / 2 + 0.01, BR - 0.02), "steel_dark", bevel=0.004))
        p.append(L.box((0.012, 0.14, 0.02), (x, -0.075, BR - 0.11), "steel_dark", rot=(-45, 0, 0), bevel=0.003))
        p.append(L.box((0.012, 0.004, 0.012), (x, -0.022, BR - 0.04), "steel_light", bevel=0))      # шуруп
    # доска
    p.append(L.box((W, D, PL), (0, -D / 2, BR), "wood", bevel=0.008))
    p.append(L.box((W, 0.006, 0.008), (0, -D + 0.004, BR + PL - 0.008), "wood_light", bevel=0))
    # банки и бутылки
    can(p, -0.40, 0.035, 0.10, "paint_red", "steel", "offwhite")
    bottle(p, -0.31, 0.03, 0.13, "paint_blue", "soot")
    can(p, -0.22, 0.04, 0.08, "hazard_yellow", "steel_dark", None)
    can(p, -0.06, 0.03, 0.12, "steel", "soot", "paint_red")
    bottle(p, 0.03, 0.028, 0.13, "rust_light", "steel_dark")
    can(p, 0.16, 0.038, 0.09, "army_green", "steel", "offwhite")
    can(p, 0.27, 0.03, 0.07, "paint_blue", "steel", None)
    bottle(p, 0.38, 0.03, 0.12, "offwhite", "paint_red")
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(shelf_idle(), "container", "shelf_wood", "derevyannaya_metal_ugolok", "idle", size_cm=(100, 30))
    L.save_blend("container", "shelf_wood")
