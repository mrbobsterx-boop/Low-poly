"""Унитаз `toilet`. Размер — из плана ОС (40 × 75 см). Варианты (только idle; «сломанный» — пропуск):
  fayansovyy_so_smyvom — фаянсовый: чаша на ножке, сиденье, бачок с кнопкой, труба;
  samodelnyy           — самодельный: ведро с деревянным сиденьем-доской;
  suhoy                — сухой (компостный): деревянный короб с крышкой, ведро торфа, совок.
Вид сбоку игры — «перед» к камере: видна чаша спереди. Запуск: python3 models/furniture/toilet.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("toilet"))


def fayansovyy_so_smyvom():
    p = []
    p.append(L.cyl(0.11, 0.30, (0, -0.05, 0), "plastic_white", verts=10, radius_top=0.13))           # ножка
    p.append(L.cyl(0.18, 0.12, (0, -0.08, 0.28), "plastic_white", verts=12, radius_top=0.19))         # чаша
    p.append(L.cyl(0.195, 0.025, (0, -0.08, 0.40), "offwhite", verts=12))                             # сиденье
    p.append(L.cyl(0.13, 0.006, (0, -0.08, 0.425), "stone_dark", verts=12))                           # отверстие (тень)
    p.append(L.box((W - 0.02, 0.16, 0.30), (0, 0.15, 0.42), "plastic_white", bevel=0.02))             # бачок
    p.append(L.box((W, 0.18, 0.03), (0, 0.15, 0.72), "offwhite", bevel=0.01))                         # крышка бачка
    p.append(L.cyl(0.02, 0.012, (0, 0.15, H - 0.012), "steel", verts=8))                               # кнопка
    p.append(L.tube((0.14, 0.22, 0.45), (0.14, 0.22, 0.0), 0.012, "steel", verts=6))                   # подводка
    for i, (x, z, c) in enumerate(((0.08, 0.15, "khaki_light"), (-0.10, 0.35, "cloth_beige"), (0.12, 0.55, "rust_light"))):
        p.append(L.spot((x, -0.27 if z < 0.4 else 0.069, z), 0.06, c, seed=430 + i, stretch=(0.7, 1.4)))
    return p


def samodelnyy():
    p = []
    p.append(L.cyl(0.15, 0.36, (0, 0, 0), "paint_blue", verts=10, radius_top=0.17))                   # ведро
    for z in (0.05, 0.30):
        p.append(L.cyl(0.165 if z > 0.1 else 0.152, 0.012, (0, 0, z), "steel_dark", verts=10))
    p.append(L.box((W, 0.40, 0.025), (0, 0, 0.36), "wood", bevel=0.006))                              # доска-сиденье
    p.append(L.cyl(0.10, 0.006, (0, 0, 0.385), "stone_dark", verts=10))
    p.append(L.box((W - 0.06, 0.03, 0.02), (0, -0.19, 0.345), "wood_dark", bevel=0.004))              # бруски
    p.append(L.tube((-0.17, 0, 0.30), (-0.20, 0, 0.42), 0.005, "steel", verts=4))                     # дужка ведра
    p.append(L.spot((0.05, -0.155, 0.12), 0.07, "rust", seed=440, stretch=(0.8, 1.4)))
    p.append(L.spot((-0.08, -0.155, 0.20), 0.05, "steel", seed=441))
    return p


def suhoy():
    p = []
    p.append(L.box((W, 0.45, 0.42), (0, 0, 0), "wood", bevel=0.01))                                  # короб
    for k in range(3):
        p.append(L.box((W + 0.002, 0.004, 0.008), (0, -0.226, 0.13 + k * 0.13), "wood_dark", bevel=0))  # доски
    p.append(L.box((W + 0.02, 0.47, 0.03), (0, 0, 0.42), "wood_light", bevel=0.008))                  # крышка-сиденье
    p.append(L.box((W - 0.04, 0.03, 0.30), (0, 0.22, 0.42), "wood_light", rot=(-12, 0, 0), bevel=0.006))   # поднятая крышка
    p.append(L.cyl(0.07, 0.10, (0.0, 0.10, 0.45), "rust", verts=8))                                   # ведёрко торфа сзади
    p.append(L.cyl(0.06, 0.01, (0.0, 0.10, 0.55), "dirt", verts=8))
    p.append(L.tube((0.04, 0.10, 0.52), (0.10, 0.08, H - 0.02), 0.006, "wood_dark", verts=4))         # совок
    p.append(L.box((0.05, 0.04, 0.03), (0.11, 0.08, H - 0.03), "steel", bevel=0.004))
    p.append(L.spot((-0.10, -0.227, 0.08), 0.08, "wood_dark", seed=450, stretch=(1.3, 0.8)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("fayansovyy_so_smyvom", fayansovyy_so_smyvom), ("samodelnyy", samodelnyy), ("suhoy", suhoy)):
        L.make(fn, "furniture", "toilet", var, size_cm=(W * 100, H * 100), broken="tilt")
    L.save_blend("furniture", "toilet")
