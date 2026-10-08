"""Готовое мясо `meat_cooked` (предмет). Размер — из плана ОС (15 × 8 см). Варианты (только idle):
  zharenoe — жареный кусок на кости, корочка с подпалинами; varenoe — варёный кусок, бледный;
  kopchenoe — копчёный окорок, тёмный, перевязан бечёвкой.
Запуск: python3 models/item/meat_cooked.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("meat_cooked"))
ROUGH = {"min_area": 0.0008, "k": 0.03, "amp_max": 0.002}


def zharenoe():
    p = [L.soft((0.11, 0.06, 0.065), (0.015, 0, 0), "rust")]
    p.append(L.tube((-W / 2 + 0.005, 0, 0.03), (-0.03, 0, 0.03), 0.008, "offwhite", verts=6))
    p.append(L.cyl(0.012, 0.01, (-W / 2 + 0.005, 0, 0.03), "plastic_white", verts=6, rot=(0, 90, 0)))
    for i, x in enumerate((-0.01, 0.04)):
        p.append(L.spot((x, -0.031, 0.04), 0.014, "rust_dark", seed=895 + i))
    return p


def varenoe():
    p = [L.soft((0.13, 0.07, 0.06), (0, 0, 0), "skin_mid")]
    p.append(L.spot((0.02, -0.036, 0.03), 0.02, "cloth_beige", seed=897, stretch=(1.6, 0.6)))
    p.append(L.spot((-0.03, 0.0, 0.061), 0.02, "skin_light", facing="top", seed=898))
    return p


def kopchenoe():
    p = [L.soft((0.12, 0.07, 0.075), (0.01, 0, 0), "rust_dark")]
    p.append(L.cyl(0.015, 0.03, (-0.06, 0, 0.03), "wood", verts=6, rot=(0, 90, 0)))
    for x in (-0.02, 0.03):                                                                  # бечёвка
        p.append(L.cyl(0.04, 0.006, (x, 0, 0.037), "cloth_beige", verts=6, rot=(0, 90, 0)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("zharenoe", zharenoe), ("varenoe", varenoe), ("kopchenoe", kopchenoe)):
        L.make(fn, "item", "meat_cooked", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "meat_cooked")
