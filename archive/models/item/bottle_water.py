"""Бутылка воды `bottle_water` (предмет). Размер — из плана ОС (8 × 25 см). Варианты (только idle; «пустая» — пропуск):
  plastikovaya_0_5_l, plastikovaya_1_5_l — прозрачно-голубой пластик с этикеткой и крышкой (0,5 л — ниже);
  steklyannaya — стеклянная бутылка с пробкой; flyaga — армейская фляга в чехле с крышкой на цепочке.
Запуск: python3 models/item/bottle_water.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("bottle_water"))
R = W / 2
ROUGH = {"min_area": 0.002, "k": 0.03, "amp_max": 0.002}


def plastic(h, label):
    p = [L.cyl(R * 0.95, h * 0.62, (0, 0, 0), "glass", verts=10)]
    p.append(L.cyl(R * 0.95, h * 0.2, (0, 0, h * 0.62), "glass", verts=10, radius_top=R * 0.4))
    p.append(L.cyl(R * 0.4, h * 0.08, (0, 0, h * 0.82), "glass", verts=8))
    p.append(L.cyl(R * 0.45, h * 0.10, (0, 0, h * 0.90), label, verts=8))                       # крышка
    p.append(L.cyl(R * 0.97, h * 0.22, (0, 0, h * 0.25), "offwhite", verts=10))                 # этикетка
    p.append(L.cyl(R * 0.98, h * 0.06, (0, 0, h * 0.33), label, verts=10))
    p.append(L.cyl(R * 0.85, h * 0.15, (0, 0, h * 0.02), "paint_blue", verts=10))               # вода видна снизу
    return p


def plastikovaya_0_5_l():
    return plastic(0.20, "paint_blue")


def plastikovaya_1_5_l():
    return plastic(H, "paint_red")


def steklyannaya():
    p = [L.cyl(R * 0.9, H * 0.6, (0, 0, 0), "glass", verts=10)]
    p.append(L.cyl(R * 0.9, H * 0.15, (0, 0, H * 0.6), "glass", verts=10, radius_top=R * 0.35))
    p.append(L.cyl(R * 0.35, H * 0.17, (0, 0, H * 0.75), "glass", verts=8))
    p.append(L.cyl(R * 0.3, H * 0.08, (0, 0, H * 0.92), "wood_light", verts=8))                 # пробка
    p.append(L.cyl(R * 0.92, H * 0.18, (0, 0, H * 0.2), "cloth_beige", verts=10))               # этикетка
    p.append(L.cyl(R * 0.8, H * 0.35, (0, 0, H * 0.02), "paint_blue", verts=10))
    return p


def flyaga():
    p = [L.box((W, 0.045, H * 0.72), (0, 0, 0), "army_green", bevel=0.02)]                       # чехол
    p.append(L.box((W + 0.004, 0.047, 0.02), (0, 0, H * 0.45), "olive_dark", bevel=0.005))     # ремешок
    p.append(L.box((0.03, 0.006, 0.02), (0, -0.026, H * 0.30), "steel", bevel=0))               # кнопка
    p.append(L.cyl(0.015, H * 0.12, (0, 0, H * 0.72), "steel", verts=8))                         # горлышко
    p.append(L.cyl(0.02, H * 0.08, (0, 0, H * 0.84), "olive_dark", verts=8))                     # крышка
    p.append(L.tube((0.02, -0.01, H * 0.88), (0.035, -0.015, H * 0.6), 0.002, "steel_light", verts=4))   # цепочка
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz in (("plastikovaya_0_5_l", plastikovaya_0_5_l, None), ("plastikovaya_1_5_l", plastikovaya_1_5_l, (W * 100, H * 100)),
                        ("steklyannaya", steklyannaya, (W * 100, H * 100)), ("flyaga", flyaga, None)):
        L.make(fn, "item", "bottle_water", var, size_cm=sz, limit="small", rough=ROUGH)
    L.save_blend("item", "bottle_water")
