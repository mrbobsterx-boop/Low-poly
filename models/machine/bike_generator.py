"""Велогенератор `bike_generator`. Размер — из плана ОС (120 × 110 см). Смотрит вправо (вид сбоку).
Варианты (только idle): statsionarnyy — тяжёлая рама-велотренажёр, маховик, генератор на ремне, щиток;
skladnoy — велосипед на складном станке, генератор у заднего колеса. Запуск: python3 models/machine/bike_generator.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("bike_generator"))


def wheel(p, x, z, r, color="soot", spokes=6):
    p.append(L.cyl(r, 0.04, (x, 0.02, z), color, verts=14, rot=(90, 0, 0)))
    p.append(L.cyl(r * 0.85, 0.045, (x, 0.022, z), "steel_dark", verts=14, rot=(90, 0, 0)))
    for k in range(spokes):
        a = k * math.pi / spokes
        p.append(L.tube((x - r * 0.8 * math.cos(a), -0.03, z - r * 0.8 * math.sin(a)),
                        (x + r * 0.8 * math.cos(a), -0.03, z + r * 0.8 * math.sin(a)), 0.004, "steel", verts=4))
    p.append(L.cyl(0.03, 0.06, (x, 0.03, z), "steel", verts=8, rot=(90, 0, 0)))


def statsionarnyy():
    p = [L.box((W, 0.45, 0.05), (0, 0, 0), "steel_dark", bevel=0.01)]
    fr = "paint_red"
    p.append(L.tube((-0.35, 0, 0.05), (-0.15, 0, 0.70), 0.03, fr, verts=6))                          # стойка седла
    p.append(L.tube((0.30, 0, 0.05), (0.25, 0, 0.95), 0.03, fr, verts=6))                             # стойка руля
    p.append(L.tube((-0.15, 0, 0.55), (0.27, 0, 0.60), 0.03, fr, verts=6))
    p.append(L.box((0.24, 0.12, 0.05), (-0.17, 0, 0.72), "soot", bevel=0.02))                         # седло
    p.append(L.tube((0.18, -0.15, 0.97), (0.18, 0.15, 0.97), 0.015, "soot", verts=6))                 # руль
    p.append(L.tube((0.25, 0, 0.95), (0.18, 0, 0.97), 0.02, fr, verts=6))
    wheel(p, 0.40, 0.30, 0.25, "steel_dark")                                          # маховик
    p.append(L.cyl(0.08, 0.03, (0.02, -0.06, 0.30), "steel", verts=10, rot=(90, 0, 0)))              # звезда
    for a in (0, math.pi):
        p.append(L.tube((0.02, -0.08, 0.30), (0.02 + 0.13 * math.cos(a + 0.6), -0.10, 0.30 + 0.13 * math.sin(a + 0.6)), 0.012, "steel", verts=4))
    p.append(L.tube((0.02, -0.07, 0.38), (0.40, -0.07, 0.55), 0.006, "soot", verts=4))               # цепь
    p.append(L.cyl(0.08, 0.16, (-0.45, 0, 0.25), "army_green", verts=10, rot=(90, 0, 0)))           # генератор
    p.append(L.tube((-0.45, -0.09, 0.25), (0.40, -0.09, 0.30), 0.005, "soot", verts=4))              # ремень
    p.append(L.box((0.16, 0.06, 0.20), (0.32, -0.04, H - 0.20), "steel", bevel=0.01))                # щиток-индикатор
    p.append(L.box((0.10, 0.006, 0.05), (0.32, -0.073, H - 0.10), "glow_screen", glow=True, bevel=0))
    return p


def skladnoy():
    p = []
    for sx in (-1, 1):                                                                 # складной станок под задним колесом
        p.append(L.tube((-0.30 + sx * 0.12, -0.20, 0), (-0.30, -0.02, 0.36), 0.015, "steel", verts=4))
        p.append(L.tube((-0.30 + sx * 0.12, 0.20, 0), (-0.30, 0.02, 0.36), 0.015, "steel", verts=4))
    wheel(p, -0.30, 0.36, 0.32)
    wheel(p, 0.35, 0.32, 0.32)
    p.append(L.box((0.12, 0.30, 0.04), (0.35, 0, 0), "soot", bevel=0.01))                            # подставка переднего
    fr = "paint_blue"
    for a, b in (((-0.30, 0.36), (0.0, 0.32)), ((0.0, 0.32), (-0.12, 0.80)), ((-0.12, 0.80), (0.28, 0.80)),
                 ((0.28, 0.80), (0.0, 0.32)), ((0.28, 0.80), (0.35, 0.32)), ((-0.30, 0.36), (-0.12, 0.80))):
        p.append(L.tube((a[0], 0, a[1]), (b[0], 0, b[1]), 0.02, fr, verts=6))
    p.append(L.tube((-0.12, 0, 0.80), (-0.15, 0, 0.92), 0.015, "steel", verts=6))
    p.append(L.box((0.22, 0.10, 0.04), (-0.15, 0, 0.92), "soot", bevel=0.015))
    p.append(L.tube((0.28, 0, 0.80), (0.24, 0, H - 0.10), 0.016, "steel", verts=6))
    p.append(L.tube((0.24, -0.20, H - 0.08), (0.24, 0.20, H - 0.08), 0.014, "soot", verts=6))
    p.append(L.cyl(0.05, 0.10, (-0.30, -0.08, 0.06), "army_green", verts=8))                         # генератор у колеса
    p.append(L.tube((-0.30, -0.08, 0.16), (-0.55, -0.10, 0.02), 0.006, "soot", verts=4))
    p.append(L.box((0.12, 0.08, 0.10), (-0.55, -0.10, 0.0), "soot", bevel=0.01))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("statsionarnyy", statsionarnyy), ("skladnoy", skladnoy)):
        L.make(fn, "machine", "bike_generator", var, size_cm=None, broken="tilt")
    L.save_blend("machine", "bike_generator")
