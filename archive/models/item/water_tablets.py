"""Таблетки для воды `water_tablets` (предмет). Размер — из плана ОС (6 × 10 см). Варианты (только idle):
  hlornye — белая пластиковая баночка с синей крышкой и этикеткой; yodnye — тёмное стекло, коричневая этикетка.
Запуск: python3 models/item/water_tablets.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("water_tablets"))
R = W / 2
ROUGH = {"min_area": 0.001, "k": 0.03, "amp_max": 0.0015}


def jar(body, cap, label, mark):
    p = [L.cyl(R * 0.95, H * 0.75, (0, 0, 0), body, verts=10)]
    p.append(L.cyl(R, H * 0.25, (0, 0, H * 0.75), cap, verts=10))
    for k in range(4):
        p.append(L.box((0.003, 0.004, H * 0.2), (-0.02 + k * 0.013, -R - 0.001, H * 0.77), body, bevel=0))
    p.append(L.cyl(R * 0.97, H * 0.4, (0, 0, H * 0.18), label, verts=10))
    p.append(L.box((0.02, 0.004, 0.006), (0, -R * 0.97 - 0.002, H * 0.42), mark, bevel=0))
    p.append(L.box((0.006, 0.004, 0.02), (0, -R * 0.97 - 0.002, H * 0.42 - 0.007), mark, bevel=0))
    return p


def hlornye():
    return jar("plastic_white", "paint_blue", "offwhite", "paint_blue")


def yodnye():
    return jar("rust_dark", "soot", "cloth_beige", "rust")


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("hlornye", hlornye), ("yodnye", yodnye)):
        L.make(fn, "item", "water_tablets", var, size_cm=(W * 100, H * 100), limit="small", rough=ROUGH)
    L.save_blend("item", "water_tablets")
