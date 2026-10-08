"""Раковина с краном `sink_tap`. Размер — из плана ОС (80 × 90 см). Варианты (только idle):
  kuhonnaya — тумба со шкафчиком, стальная мойка, смеситель; vannaya — фаянсовая раковина на тумбе-пьедестале, зеркальце;
  umyvalnik — рукомойник (бачок с носиком) над тазом на стойке; ulichnaya_kolonka — уличная колонка с рычагом.
Запуск: python3 models/furniture/sink_tap.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("sink_tap"))
D = 0.55
F = -D / 2


def mixer(p, x, z):
    p.append(L.cyl(0.025, 0.08, (x, 0.12, z), "steel_light", verts=8))
    p.append(L.tube((x, 0.12, z + 0.08), (x, -0.02, z + 0.12), 0.012, "steel_light", verts=6))
    p.append(L.tube((x, -0.02, z + 0.12), (x, -0.04, z + 0.07), 0.012, "steel_light", verts=6))
    for dx in (-0.06, 0.06):
        p.append(L.cyl(0.018, 0.03, (x + dx, 0.12, z), "steel_light", verts=6))


def kuhonnaya():
    p = [L.box((W, D, 0.72), (0, 0, 0.0), "wood", bevel=0.012)]
    p.append(L.box((W - 0.04, 0.02, 0.56), (0, F - 0.01, 0.08), "wood_light", bevel=0.01))
    p.append(L.box((0.004, 0.022, 0.54), (0, F - 0.021, 0.09), "wood_dark", bevel=0))
    for x in (-0.04, 0.04):
        p.append(L.box((0.015, 0.02, 0.10), (x, F - 0.03, 0.50), "steel", bevel=0.004))
    p.append(L.box((W + 0.02, D + 0.02, 0.04), (0, 0, 0.72), "steel", bevel=0.008))                  # столешница-мойка
    p.append(L.box((0.48, 0.36, 0.006), (-0.05, 0.0, 0.76), "stone_dark", bevel=0))                    # чаша (тень)
    p.append(L.box((0.52, 0.40, 0.008), (-0.05, 0.0, 0.754), "steel_light", bevel=0.003))
    mixer(p, -0.05, 0.76)
    p.append(L.box((W - 0.02, 0.04, 0.06), (0, F + 0.01, 0.0), "soot", bevel=0.006))
    for i, (x, z) in enumerate(((0.25, 0.30), (-0.25, 0.15))):
        p.append(L.spot((x, F - 0.021, z), 0.08, "wood_dark", seed=650 + i))
    return p


def vannaya():
    p = [L.cyl(0.10, 0.62, (0, 0.05, 0), "plastic_white", verts=10, radius_top=0.13)]                 # пьедестал
    p.append(L.box((0.62, 0.45, 0.18), (0, 0.0, 0.62), "plastic_white", bevel=0.05))                  # раковина
    p.append(L.box((0.48, 0.32, 0.006), (0, -0.01, 0.80), "stone_dark", bevel=0))
    mixer(p, 0.0, 0.80)
    p.append(L.box((0.40, 0.03, 0.06), (0, 0.18, H - 0.06), "glass", bevel=0.008))                    # полочка
    for i, (x, z, c) in enumerate(((0.15, 0.70, "khaki_light"), (-0.1, 0.30, "rust_light"))):
        p.append(L.spot((x, -0.226 if z > 0.6 else -0.06, z), 0.06, c, seed=655 + i, stretch=(0.7, 1.4)))
    return p


def umyvalnik():
    p = []
    for sx in (-1, 1):
        p.append(L.box((0.04, 0.04, H), (sx * 0.28, 0.12, 0), "wood_dark", bevel=0.006))
    p.append(L.box((0.60, 0.04, 0.04), (0, 0.12, 0.55), "wood", bevel=0.006))
    p.append(L.box((0.60, 0.03, 0.30), (0, 0.15, 0.58), "wood", bevel=0.006))                       # доска-задник
    p.append(L.cyl(0.25, 0.10, (0, -0.05, 0.50), "steel_light", verts=12, radius_top=0.28))           # таз
    p.append(L.cyl(0.22, 0.004, (0, -0.05, 0.60), "paint_blue", verts=12))
    p.append(L.box((0.24, 0.16, 0.20), (0, 0.06, H - 0.22), "steel", bevel=0.02))                    # бачок
    p.append(L.box((0.25, 0.17, 0.02), (0, 0.06, H - 0.02), "steel_dark", bevel=0.006))
    p.append(L.cyl(0.012, 0.08, (0, -0.03, H - 0.30), "steel_dark", verts=6))                         # носик
    p.append(L.box((0.10, 0.06, 0.03), (-0.20, -0.0, 0.88), "offwhite", bevel=0.01))                  # мыло
    p.append(L.spot((0.05, -0.02, H - 0.10), 0.05, "rust", seed=660, stretch=(0.6, 1.5)))
    return p


def ulichnaya_kolonka():
    p = [L.box((0.40, 0.40, 0.10), (0, 0, 0), "concrete", bevel=0.02)]
    p.append(L.cyl(0.08, H - 0.20, (0, 0, 0.10), "army_green", verts=10))
    p.append(L.cyl(0.10, 0.12, (0, 0, H - 0.20), "army_green", verts=10, radius_top=0.06))
    p.append(L.tube((0, -0.08, 0.55), (0, -0.25, 0.45), 0.03, "army_green", verts=6))
    p.append(L.tube((0.05, 0, H - 0.12), (0.30, 0.0, H - 0.04), 0.015, "steel_dark", verts=6))
    p.append(L.box((0.30, 0.25, 0.03), (0, -0.30, 0.0), "steel", bevel=0.006))                         # решётка-слив
    for k in range(5):
        p.append(L.box((0.28, 0.01, 0.006), (0, -0.40 + k * 0.05, 0.03), "soot", bevel=0))
    p.append(L.spot((0.0, -0.081, 0.35), 0.06, "rust", seed=665, stretch=(0.6, 1.6)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz in (("kuhonnaya", kuhonnaya, (W * 100, H * 100)), ("vannaya", vannaya, None),
                        ("umyvalnik", umyvalnik, None), ("ulichnaya_kolonka", ulichnaya_kolonka, None)):
        L.make(fn, "furniture", "sink_tap", var, size_cm=sz, broken="tilt")
    L.save_blend("furniture", "sink_tap")
