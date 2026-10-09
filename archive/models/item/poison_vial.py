"""Яд `poison_vial` (предмет). Размер — из плана ОС (5 × 10 см). Варианты (только idle):
  slabyy — пузырёк с мутно-зелёной жидкостью, пробка; silnyy — тёмный пузырёк с черепом-меткой и сургучом;
  medlennyy — флакон с фиолетовой жидкостью и пипеткой; antidot — прозрачная ампула-флакон с белой этикеткой и крестом.
Запуск: python3 models/item/poison_vial.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("poison_vial"))
ROUGH = {"min_area": 0.0003, "k": 0.02, "amp_max": 0.0008}
N = 8


def vial(liquid, cork, label=None, r=W / 2):
    p = [L.cyl(r, 0.065, (0, 0, 0), "glass", verts=N)]
    p.append(L.cyl(r + 0.0006, 0.045, (0, 0, 0.004), liquid, verts=N))                  # жидкость видна сквозь стекло
    p.append(L.cyl(r, 0.015, (0, 0, 0.065), "glass", verts=N, radius_top=0.009))
    p.append(L.cyl(0.008, 0.008, (0, 0, 0.08), "glass", verts=N))
    p.append(L.cyl(0.0095, 0.012, (0, 0, H - 0.012), cork, verts=N, radius_top=0.011))
    if label:
        p.append(L.box((0.03, 0.003, 0.02), (0, -r - 0.002, 0.02), label, bevel=0))
    return p


def slabyy():
    return vial("plant", "wood")


def silnyy():
    p = vial("soot", "blood", "offwhite")
    p.append(L.box((0.008, 0.003, 0.008), (-0.004, -W / 2 - 0.005, 0.028), "soot", bevel=0))       # «череп»
    p.append(L.box((0.008, 0.003, 0.008), (0.006, -W / 2 - 0.005, 0.028), "soot", bevel=0))
    p.append(L.box((0.012, 0.003, 0.004), (0.001, -W / 2 - 0.005, 0.022), "soot", bevel=0))
    return p


def medlennyy():
    p = vial("glow_grow", "soot")
    p.append(L.cyl(0.003, 0.012, (0, 0, H - 0.012), "glass", verts=4))
    return p


def antidot():
    p = vial("steel_light", "plastic_white", "plastic_white")
    p.append(L.box((0.012, 0.003, 0.004), (0, -W / 2 - 0.005, 0.028), "paint_red", bevel=0))
    p.append(L.box((0.004, 0.003, 0.012), (0, -W / 2 - 0.005, 0.024), "paint_red", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("slabyy", slabyy), ("silnyy", silnyy), ("medlennyy", medlennyy), ("antidot", antidot)):
        L.make(fn, "item", "poison_vial", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "poison_vial")
