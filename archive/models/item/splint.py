"""Шина `splint` (предмет). Размер — из плана ОС (40 × 8 см). Варианты (только idle):
  gotovaya — алюминиевая шина в оранжевом поролоне, свёрнута в рулон-полосу; iz_dosok_i_tkani — 2 дощечки, обмотанные тканью.
Запуск: python3 models/item/splint.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("splint"))
ROUGH = {"min_area": 0.001, "k": 0.02, "amp_max": 0.0015}


def gotovaya():
    p = [L.box((W, 0.10, 0.012), (0, 0, 0), "hazard_yellow", bevel=0.004)]
    p.append(L.cyl(0.035, 0.10, (W / 2 - 0.03, 0.05, 0.035), "hazard_yellow", verts=8, rot=(90, 0, 0)))   # свёрнутый конец
    p.append(L.cyl(0.02, 0.102, (W / 2 - 0.03, 0.051, 0.035), "steel_light", verts=8, rot=(90, 0, 0)))
    p.append(L.box((0.06, 0.102, 0.013), (-0.08, 0, 0), "paint_blue", bevel=0))                     # липучка
    return p


def iz_dosok_i_tkani():
    p = []
    for y, c in ((-0.025, "wood_light"), (0.025, "wood")):
        p.append(L.box((W, 0.04, 0.02), (0, y, 0), c, bevel=0.004))
    for x in (-0.13, 0.0, 0.13):
        p.append(L.box((0.04, 0.10, 0.03), (x, 0, -0.003), "cloth_beige", rot=(0, 0, 8), bevel=0.004))
    p.append(L.sheet(2, 1, 0.06, 0.02, (0.06, -0.05, 0.002), "cloth_beige", jitter=0.002, thick=0.003, seed=5))   # хвостик
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("gotovaya", gotovaya), ("iz_dosok_i_tkani", iz_dosok_i_tkani)):
        L.make(fn, "item", "splint", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "splint")
