"""Насос `water_pump`. Размер — из плана ОС (50 × 60 см). Варианты (только idle):
  ruchnoy_rychazhnyy — чугунная колонка с рычагом на станине; elektricheskiy — электродвигатель + улитка, кабель;
  benzinovyy — бензиновая мотопомпа в раме, бак, патрубки. Запуск: python3 models/machine/water_pump.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("water_pump"))


def ruchnoy_rychazhnyy():
    p = [L.box((0.40, 0.30, 0.05), (0, 0, 0), "wood", bevel=0.008)]
    p.append(L.cyl(0.07, 0.36, (-0.05, 0, 0.05), "army_green", verts=8))
    p.append(L.cyl(0.085, 0.06, (-0.05, 0, 0.41), "army_green", verts=8))
    p.append(L.tube((-0.05, -0.07, 0.30), (-0.05, -0.20, 0.24), 0.025, "army_green", verts=6))
    p.append(L.tube((-0.05, 0, 0.47), (W / 2, 0, H - 0.02), 0.018, "steel_dark", verts=6))
    p.append(L.tube((-0.15, 0, 0.47), (-0.05, 0, 0.47), 0.012, "steel_dark", verts=4))
    p.append(L.tube((0.10, 0.0, 0.05), (0.12, 0.0, -0.0), 0.03, "soot", verts=6))
    p.append(L.spot((-0.05, -0.072, 0.15), 0.05, "rust", seed=620, stretch=(0.6, 1.5)))
    return p


def elektricheskiy():
    p = [L.box((W, 0.30, 0.04), (0, 0, 0), "steel_dark", bevel=0.006)]
    p.append(L.cyl(0.11, 0.24, (-0.20, 0, 0.17), "paint_blue", verts=10, rot=(0, 90, 0)))           # мотор
    for k in range(5):
        p.append(L.cyl(0.115, 0.012, (-0.18 + k * 0.045, 0, 0.17), "paint_blue", verts=10, rot=(0, 90, 0)))   # рёбра
    p.append(L.cyl(0.14, 0.12, (0.06, 0, 0.17), "steel", verts=12, rot=(0, 90, 0)))                  # улитка
    p.append(L.tube((0.18, 0, 0.17), (W / 2, 0, 0.17), 0.035, "steel", verts=8))                    # вход
    p.append(L.tube((0.12, 0, 0.28), (0.12, 0, H - 0.02), 0.03, "steel", verts=8))                  # выход
    p.append(L.box((0.10, 0.08, 0.08), (-0.15, 0, 0.28), "steel_dark", bevel=0.008))                 # клеммная коробка
    p.append(L.tube((-0.15, -0.04, 0.32), (-W / 2, -0.10, 0.02), 0.008, "soot", verts=4))
    p.append(L.box((0.05, 0.004, 0.03), (-0.20, -0.112, 0.20), "offwhite", bevel=0))
    return p


def benzinovyy():
    p = []
    for sx in (-1, 1):                                                                 # рама из труб
        p.append(L.tube((sx * 0.22, -0.18, 0.02), (sx * 0.22, 0.18, 0.02), 0.015, "soot", verts=6))
        p.append(L.tube((sx * 0.22, -0.18, 0.02), (sx * 0.22, -0.18, H - 0.02), 0.015, "soot", verts=6))
        p.append(L.tube((sx * 0.22, 0.18, 0.02), (sx * 0.22, 0.18, H - 0.02), 0.015, "soot", verts=6))
    p.append(L.tube((-0.22, -0.18, H - 0.08), (0.22, -0.18, H - 0.02), 0.015, "soot", verts=6))
    p.append(L.box((0.20, 0.22, 0.22), (-0.08, 0, 0.06), "paint_red", bevel=0.02))                   # двигатель
    p.append(L.box((0.24, 0.20, 0.10), (-0.06, 0, H - 0.22), "paint_red", bevel=0.03))              # бак
    p.append(L.cyl(0.025, 0.02, (-0.10, 0, H - 0.12), "soot", verts=8))
    p.append(L.cyl(0.10, 0.10, (0.12, 0, 0.14), "steel", verts=10, rot=(0, 90, 0)))                  # улитка
    for z in (0.14, 0.30):
        p.append(L.tube((0.12, -0.02, z), (0.12, -0.20, z), 0.03, "steel_light", verts=8))
    p.append(L.box((0.06, 0.004, 0.04), (-0.08, -0.112, 0.20), "offwhite", bevel=0))
    p.append(L.box((0.02, 0.06, 0.02), (-0.16, -0.12, 0.25), "soot", bevel=0.004))                   # ручка стартера
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("ruchnoy_rychazhnyy", ruchnoy_rychazhnyy), ("elektricheskiy", elektricheskiy), ("benzinovyy", benzinovyy)):
        L.make(fn, "machine", "water_pump", var, size_cm=(W * 100, H * 100), broken="tilt")
    L.save_blend("machine", "water_pump")
