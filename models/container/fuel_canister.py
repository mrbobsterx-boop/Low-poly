"""Канистра `fuel_canister`. Размер — из плана ОС (35 × 45 см). Варианты (только idle; «пустая» — пропуск):
  5_l, 10_l — пластиковые (красная, зелёная), меньше по природе; 20_l — стальная «джерри» с тремя ручками и выштамповкой.
Запуск: python3 models/container/fuel_canister.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("fuel_canister"))


def plastic(w, h, color):
    d = 0.14 if w < 0.25 else 0.16
    p = [L.box((w, d, h * 0.82), (0, 0, 0), color, bevel=0.025)]
    p.append(L.box((w * 0.55, d * 0.6, h * 0.10), (-w * 0.12, 0, h * 0.82), color, bevel=0.012))     # ручка-перемычка
    p.append(L.box((w * 0.35, d * 0.65, h * 0.06), (-w * 0.12, 0, h * 0.82), "stone_dark", bevel=0.004))   # окно ручки
    p.append(L.cyl(0.025, h * 0.10, (w * 0.32, 0, h * 0.82), color, verts=8))
    p.append(L.cyl(0.03, h * 0.08, (w * 0.32, 0, h * 0.92), "soot", verts=8))                          # крышка
    p.append(L.box((w * 0.5, 0.004, h * 0.25), (0, -d / 2 - 0.002, h * 0.30), "offwhite", bevel=0))   # наклейка
    p.append(L.box((w * 0.15, 0.004, h * 0.12), (0, -d / 2 - 0.004, h * 0.36), "soot", rot=(0, 45, 0), bevel=0))
    return p


def l5():
    return plastic(0.22, 0.30, "paint_red")


def l10():
    return plastic(0.27, 0.38, "plant_dark")


def l20():
    p = [L.box((W, 0.16, H - 0.07), (0, 0, 0), "army_green", bevel=0.02)]
    p.append(L.poly([(-0.10, -0.12), (0.10, -0.12), (0.0, 0.0)], 0.004, (0, -0.082, 0.24), "olive_dark"))   # выштамповка X
    p.append(L.poly([(-0.10, 0.12), (0.10, 0.12), (0.0, 0.0)], 0.004, (0, -0.082, 0.24), "olive_dark"))
    for x in (-0.10, 0.0, 0.10):                                                       # три ручки
        p.append(L.box((0.03, 0.08, 0.06), (x, 0, H - 0.07), "army_green", bevel=0.006))
    p.append(L.box((0.24, 0.06, 0.025), (0, 0, H - 0.025), "army_green", bevel=0.006))
    p.append(L.box((0.06, 0.06, 0.07), (W / 2 - 0.04, 0, H - 0.09), "steel_dark", bevel=0.006))      # горловина
    p.append(L.box((0.05, 0.004, 0.03), (-0.10, -0.082, 0.36), "offwhite", bevel=0))                  # маркировка
    for i, (x, z) in enumerate(((0.12, 0.05), (-0.13, 0.30))):
        p.append(L.spot((x, -0.082, z), 0.05, "steel", seed=760 + i))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz in (("5_l", l5, None), ("10_l", l10, None), ("20_l", l20, (W * 100, H * 100))):
        L.make(fn, "container", "fuel_canister", var, size_cm=sz, limit="small", broken="tilt",
               rough={"min_area": 0.02, "k": 0.03, "amp_max": 0.004, "levels": 1})
    L.save_blend("container", "fuel_canister")
