"""Кастрюля `cooking_pot` (инструмент). Размер — из плана ОС (25 × 20 см). Варианты (только idle):
  alyuminievaya — алюминиевая кастрюля: две ручки, крышка с ручкой, вмятины;
  kotelok       — походный котелок: дужка, закопчённое дно;
  chugunnyy     — чугунный казан: толстые стенки, ушки, тяжёлая крышка.
Запуск: python3 models/tool/cooking_pot.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("cooking_pot"))
ROUGH = {"min_area": 0.004, "k": 0.03, "amp_max": 0.003}
N = 10


def alyuminievaya():
    r = W / 2 - 0.035
    p = [L.cyl(r, 0.15, (0, 0, 0), "steel_light", verts=N)]
    p.append(L.cyl(r + 0.004, 0.012, (0, 0, 0.14), "steel", verts=N))                         # завальцовка
    p.append(L.cyl(r - 0.005, 0.012, (0, 0, 0.152), "steel_light", verts=N, radius_top=r * 0.6))   # крышка
    p.append(L.cyl(r * 0.6, 0.02, (0, 0, 0.164), "steel_light", verts=N, radius_top=r * 0.3))
    p.append(L.box((0.05, 0.016, 0.016), (0, 0, H - 0.016), "soot", bevel=0.004))             # ручка крышки
    for sx in (-1, 1):
        p.append(L.box((0.035, 0.05, 0.014), (sx * (r + 0.017), 0, 0.11), "soot", bevel=0.004))
    for i, (x, z) in enumerate(((-0.04, 0.05), (0.05, 0.09))):
        p.append(L.spot((x, -r - 0.001, z), 0.025, "steel", seed=830 + i))
    p.append(L.cyl(r + 0.001, 0.02, (0, 0, 0), "soot", verts=N))                              # закопчённое дно
    return p


def kotelok():
    r = W / 2 - 0.02
    p = [L.cyl(r, 0.13, (0, 0, 0), "soot", verts=N, radius_top=r + 0.005)]
    p.append(L.cyl(r * 0.98, 0.05, (0, 0, 0.13 - 0.0), "steel_dark", verts=N, radius_top=r + 0.008))
    p.append(L.cyl(r + 0.01, 0.01, (0, 0, 0.17), "steel", verts=N))
    for sx in (-1, 1):                                                                         # ушки и дужка
        p.append(L.box((0.016, 0.02, 0.02), (sx * (r + 0.012), 0, 0.15), "steel", bevel=0.003))
        p.append(L.tube((sx * (r + 0.015), 0, 0.16), (sx * r * 0.6, 0, H - 0.008), 0.004, "steel_light", verts=4))
    p.append(L.tube((-r * 0.6, 0, H - 0.008), (r * 0.6, 0, H - 0.008), 0.004, "steel_light", verts=4))
    p.append(L.spot((0.03, -r - 0.003, 0.06), 0.04, "stone_dark", seed=835))
    return p


def chugunnyy():
    r = W / 2 - 0.025
    p = [L.cyl(r * 0.8, 0.03, (0, 0, 0), "soot", verts=N, radius_top=r)]
    p.append(L.cyl(r, 0.10, (0, 0, 0.03), "soot", verts=N, radius_top=r + 0.006))
    p.append(L.cyl(r + 0.012, 0.016, (0, 0, 0.125), "stone_dark", verts=N))                     # толстый край
    p.append(L.cyl(r, 0.03, (0, 0, 0.14), "soot", verts=N, radius_top=r * 0.55))               # крышка-купол
    p.append(L.cyl(0.02, 0.02, (0, 0, 0.17), "stone_dark", verts=6, radius_top=0.026))
    for sx in (-1, 1):                                                                         # ушки
        p.append(L.box((0.025, 0.06, 0.02), (sx * (r + 0.012), 0, 0.10), "stone_dark", bevel=0.006))
    for i, (x, z) in enumerate(((-0.05, 0.06), (0.06, 0.03))):
        p.append(L.spot((x, -r - 0.004, z), 0.03, "rust_dark", seed=838 + i))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("alyuminievaya", alyuminievaya), ("kotelok", kotelok), ("chugunnyy", chugunnyy)):
        L.make(fn, "tool", "cooking_pot", var, size_cm=(W * 100, H * 100), limit="small", broken=False, rough=ROUGH)
    L.save_blend("tool", "cooking_pot")
