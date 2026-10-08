"""Антибиотики `antibiotics` (предмет). Размер — из плана ОС (6 × 8 см). Варианты (только idle):
  shirokogo_spektra — белая аптечная банка с синей этикеткой и капсулами рядом;
  uzkospetsialnye — картонная коробочка с зелёной полосой и флакон. Запуск: python3 models/item/antibiotics.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("antibiotics"))
ROUGH = {"min_area": 0.0004, "k": 0.02, "amp_max": 0.001}


def shirokogo_spektra():
    r = 0.022
    p = [L.cyl(r, 0.06, (-0.005, 0, 0), "plastic_white", verts=8)]
    p.append(L.cyl(r + 0.002, 0.016, (-0.005, 0, 0.06), "paint_blue", verts=8))
    p.append(L.cyl(r + 0.001, 0.03, (-0.005, 0, 0.012), "paint_blue", verts=8))
    p.append(L.box((0.02, 0.003, 0.012), (-0.005, -r - 0.002, 0.02), "offwhite", bevel=0))
    for x, c in ((0.022, "paint_red"), (0.028, "hazard_yellow")):                               # капсулы
        p.append(L.box((0.012, 0.006, 0.005), (x, -0.015 + (x - 0.022) * 3, 0), c, rot=(0, 0, 30), bevel=0.002))
    return p


def uzkospetsialnye():
    p = [L.box((0.04, 0.025, 0.07), (-0.01, 0.005, 0), "offwhite", bevel=0.003)]
    p.append(L.box((0.041, 0.003, 0.015), (-0.01, -0.008, 0.04), "plant", bevel=0))
    p.append(L.box((0.025, 0.003, 0.005), (-0.01, -0.008, 0.02), "soot", bevel=0))
    p.append(L.cyl(0.009, 0.035, (0.022, -0.01, 0), "glass", verts=6))                          # флакон
    p.append(L.cyl(0.008, 0.02, (0.022, -0.01, 0.002), "offwhite", verts=6))
    p.append(L.cyl(0.0095, 0.008, (0.022, -0.01, 0.035), "steel_light", verts=6))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("shirokogo_spektra", shirokogo_spektra), ("uzkospetsialnye", uzkospetsialnye)):
        L.make(fn, "item", "antibiotics", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "antibiotics")
