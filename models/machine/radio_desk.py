"""Радио `radio_desk`. Размер — из плана ОС (35 × 25 см). Варианты (только idle; «сломанный» — пропуск):
  nastolnyy — ламповый приёмник: деревянный корпус, ткань динамика, шкала (светится), ручки;
  ruchnoy — ручной с динамо: пластик, ручка-рукоять, антенна, маленький динамик;
  voennaya_ratsiya — военная рация: зелёный ящик, тумблеры, трубка на шнуре, антенна.
Запуск: python3 models/machine/radio_desk.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("radio_desk"))
D = 0.18
F = -D / 2
ROUGH = {"min_area": 0.006, "k": 0.03, "amp_max": 0.004}


def nastolnyy():
    p = [L.box((W, D, H - 0.02), (0, 0, 0.02), "wood", bevel=0.02)]
    for sx in (-1, 1):
        p.append(L.box((0.04, D - 0.04, 0.02), (sx * (W / 2 - 0.05), 0, 0), "soot", bevel=0.004))
    p.append(L.box((0.17, 0.006, 0.15), (-0.07, F - 0.003, 0.06), "cloth_beige", bevel=0.004))      # ткань динамика
    for k in range(5):
        p.append(L.box((0.17, 0.004, 0.006), (-0.07, F - 0.007, 0.075 + k * 0.028), "wood_dark", bevel=0))
    p.append(L.box((0.10, 0.006, 0.05), (0.10, F - 0.003, 0.15), "glow_lamp", glow=True, bevel=0.003))   # шкала
    for k in range(5):
        p.append(L.box((0.002, 0.004, 0.02), (0.065 + k * 0.018, F - 0.007, 0.165), "soot", bevel=0))
    for x in (0.07, 0.13):
        p.append(L.cyl(0.018, 0.02, (x, F - 0.01, 0.08), "wood_dark", verts=8, rot=(90, 0, 0)))
        p.append(L.box((0.004, 0.006, 0.015), (x, F - 0.022, 0.085), "offwhite", bevel=0))
    p.append(L.spot((-0.12, F - 0.004, 0.20), 0.03, "wood_light", seed=390))
    return p


def ruchnoy():
    p = [L.box((W * 0.75, D * 0.7, 0.15), (0, 0, 0.0), "paint_red", bevel=0.02)]
    p.append(L.box((W * 0.75 + 0.01, D * 0.7 + 0.01, 0.025), (0, 0, 0.0), "soot", bevel=0.008))
    p.append(L.cyl(0.04, 0.006, (-0.06, F * 0.7 - 0.003, 0.08), "soot", verts=10, rot=(90, 0, 0)))     # динамик
    for k in range(3):
        p.append(L.box((0.06, 0.004, 0.005), (-0.06, F * 0.7 - 0.007, 0.065 + k * 0.014), "steel_dark", bevel=0))
    p.append(L.box((0.07, 0.006, 0.025), (0.06, F * 0.7 - 0.003, 0.10), "glow_screen", glow=True, bevel=0.002))
    p.append(L.cyl(0.012, 0.015, (0.05, F * 0.7 - 0.008, 0.05), "steel", verts=8, rot=(90, 0, 0)))
    # рукоять динамо сбоку и ручка для переноски
    p.append(L.box((0.015, 0.02, 0.06), (W * 0.375 + 0.01, 0, 0.06), "steel_dark", bevel=0.004))
    p.append(L.box((0.05, 0.02, 0.012), (W * 0.375 + 0.035, 0, 0.115), "steel_dark", bevel=0.004))
    p.append(L.cyl(0.008, 0.03, (W * 0.375 + 0.055, -0.02, 0.10), "soot", verts=6, rot=(90, 0, 0)))
    p.append(L.tube((-0.08, 0, 0.15), (-0.08, 0, 0.17), 0.012, "soot", verts=6))
    p.append(L.tube((0.04, 0, 0.15), (0.04, 0, 0.17), 0.012, "soot", verts=6))
    p.append(L.tube((-0.08, 0, 0.17), (0.04, 0, 0.17), 0.012, "soot", verts=6))
    p.append(L.tube((-0.11, 0.02, 0.14), (-0.15, 0.02, H), 0.004, "steel_light", verts=4))          # антенна
    return p


def voennaya_ratsiya():
    p = [L.box((W - 0.02, D, H - 0.07), (0, 0, 0.0), "army_green", bevel=0.015)]
    p.append(L.box((W - 0.04, 0.008, H - 0.12), (0, F - 0.004, 0.025), "olive_dark", bevel=0.004))   # панель
    p.append(L.box((0.09, 0.006, 0.035), (-0.06, F - 0.008, 0.11), "glow_screen", glow=True, bevel=0.002))
    for k, x in enumerate((0.03, 0.07, 0.11)):
        p.append(L.cyl(0.012, 0.012, (x, F - 0.012, 0.12), "soot", verts=8, rot=(90, 0, 0)))
        p.append(L.box((0.006, 0.02, 0.006), (x, F - 0.02, 0.06), "steel_light", rot=(25, 0, 0), bevel=0))   # тумблеры
    p.append(L.box((0.05, 0.006, 0.015), (-0.06, F - 0.008, 0.05), "offwhite", bevel=0))                     # бирка
    # трубка на шнуре сбоку, антенна, ручка
    p.append(L.box((0.035, 0.03, 0.10), (-W / 2 - 0.01, 0, 0.02), "soot", bevel=0.008))
    p.append(L.tube((-W / 2 - 0.01, 0, 0.02), (-W / 2 + 0.03, F + 0.03, 0.03), 0.004, "soot", verts=4))
    p.append(L.tube((W / 2 - 0.05, 0.03, H - 0.07), (W / 2 - 0.04, 0.03, H), 0.005, "steel_dark", verts=4))
    p.append(L.box((0.12, 0.02, 0.015), (0, 0, H - 0.07), "soot", bevel=0.004))
    for i, (x, z) in enumerate(((0.12, 0.03), (-0.13, 0.16))):
        p.append(L.spot((x, F - 0.002, z), 0.025, "steel", seed=395 + i))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("nastolnyy", nastolnyy), ("ruchnoy", ruchnoy), ("voennaya_ratsiya", voennaya_ratsiya)):
        L.make(fn, "machine", "radio_desk", var, size_cm=(W * 100, H * 100), limit="small", rough=ROUGH, broken="tilt")
    L.save_blend("machine", "radio_desk")
