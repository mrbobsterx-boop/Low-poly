"""Силовой кабель `power_cable` (предмет). Размер — из плана ОС (20 × 20 см). Варианты (только idle):
  tonkiy — моток тонкого провода; silovoy — толстый силовой кабель в бухте с наконечниками;
  udlinitel — удлинитель: катушка-бухта с колодкой на 3 розетки. Запуск: python3 models/item/power_cable.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("power_cable"))
ROUGH = {"min_area": 0.003, "k": 0.03, "amp_max": 0.003}


def coil(p, r, thick, color, turns=4, z0=0.0, seed=0, verts=5):
    """Бухта: несколько колец-торов (8-угольники из труб), слегка сдвинутых."""
    import random
    rnd = random.Random(seed)
    for t in range(turns):
        dx, dz = rnd.uniform(-0.01, 0.01), rnd.uniform(-0.01, 0.01)
        n = 8
        pts = [(r * math.cos(2 * math.pi * k / n) + dx, r * math.sin(2 * math.pi * k / n) + dz + r + thick + z0) for k in range(n)]
        for a, b in zip(pts, pts[1:] + pts[:1]):
            p.append(L.tube((a[0], -0.01 + t * 0.012, a[1]), (b[0], -0.01 + t * 0.012, b[1]), thick, color, verts=verts))


def tonkiy():
    p = []
    coil(p, 0.07, 0.006, "paint_red", turns=4, seed=1, verts=4)
    p.append(L.tube((0.05, -0.02, 0.03), (0.10, -0.03, 0.0), 0.006, "paint_red", verts=4))
    p.append(L.box((0.012, 0.01, 0.01), (0.10, -0.03, 0.0), "rust_light", bevel=0))
    return p


def silovoy():
    p = []
    coil(p, 0.075, 0.014, "soot", turns=3, seed=2)
    for x, c in ((-0.06, "paint_red"), (0.07, "paint_blue")):
        p.append(L.tube((x, -0.03, 0.04), (x * 1.2, -0.06, 0.0), 0.014, "soot", verts=5))
        p.append(L.box((0.03, 0.02, 0.02), (x * 1.2, -0.06, 0.0), c, bevel=0.004))
        p.append(L.box((0.02, 0.01, 0.012), (x * 1.2 + (0.02 if x > 0 else -0.02), -0.06, 0.004), "rust_light", bevel=0))
    return p


def udlinitel():
    p = [L.cyl(0.08, 0.06, (0, 0.0, 0.08), "hazard_yellow", verts=10, rot=(90, 0, 0))]
    p.append(L.cyl(0.10, 0.012, (0, 0.03, 0.08), "soot", verts=10, rot=(90, 0, 0)))
    p.append(L.cyl(0.10, 0.012, (0, -0.042, 0.08), "soot", verts=10, rot=(90, 0, 0)))
    p.append(L.cyl(0.015, 0.03, (0.0, -0.06, 0.08), "soot", verts=6, rot=(90, 0, 0)))                 # ручка
    p.append(L.box((0.09, 0.04, 0.03), (0, -0.01, 0.0), "soot", bevel=0.006))                        # колодка
    for k in range(3):
        p.append(L.cyl(0.008, 0.004, (-0.03 + k * 0.03, -0.01, 0.03), "stone_dark", verts=6))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("tonkiy", tonkiy), ("silovoy", silovoy), ("udlinitel", udlinitel)):
        L.make(fn, "item", "power_cable", var, limit="small", rough=ROUGH)
    L.save_blend("item", "power_cable")
