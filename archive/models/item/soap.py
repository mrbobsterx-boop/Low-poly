"""Мыло `soap` (предмет). Размер — из плана ОС (8 × 4 см). Варианты (только idle):
  kusok_myla — брусок хозяйственного мыла с выдавленной надписью; gel — флакон геля с дозатором;
  dezinfitsiruyuschee — белая бутылочка санитайзера с синей этикеткой. Запуск: python3 models/item/soap.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("soap"))
ROUGH = {"min_area": 0.0003, "k": 0.02, "amp_max": 0.0008}


def kusok_myla():
    p = [L.box((W, 0.05, H), (0, 0, 0), "wood_light", bevel=0.008)]
    p.append(L.box((0.04, 0.003, 0.008), (0, -0.026, 0.016), "wood", bevel=0))
    return p


def gel():
    p = [L.box((0.045, 0.03, 0.09), (0, 0, 0), "plant", bevel=0.008)]
    p.append(L.cyl(0.01, 0.025, (0, 0, 0.09), "plastic_white", verts=6))
    p.append(L.box((0.025, 0.008, 0.008), (0.008, 0, 0.11), "plastic_white", bevel=0.002))
    p.append(L.box((0.035, 0.003, 0.03), (0, -0.0165, 0.025), "offwhite", bevel=0))
    return p


def dezinfitsiruyuschee():
    p = [L.cyl(0.02, 0.08, (0, 0, 0), "plastic_white", verts=8)]
    p.append(L.cyl(0.012, 0.015, (0, 0, 0.08), "paint_blue", verts=8))
    p.append(L.cyl(0.021, 0.035, (0, 0, 0.02), "paint_blue", verts=8))
    p.append(L.box((0.02, 0.003, 0.006), (0, -0.022, 0.035), "offwhite", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("kusok_myla", kusok_myla), ("gel", gel), ("dezinfitsiruyuschee", dezinfitsiruyuschee)):
        L.make(fn, "item", "soap", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "soap")
