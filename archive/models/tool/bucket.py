"""Ведро `bucket` (инструмент). Размер — из плана ОС (30 × 30 см). Варианты (только idle; «дырявое» — пропуск):
  metallicheskoe — оцинкованное: рёбра, дужка с деревянной ручкой; plastikovoe — синее пластиковое, дужка.
Запуск: python3 models/tool/bucket.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("bucket"))
ROUGH = {"min_area": 0.004, "k": 0.03, "amp_max": 0.004}


def bucket(body, rim, handle_grip):
    p = [L.cyl(0.11, H - 0.08, (0, 0, 0), body, verts=12, radius_top=0.14)]
    p.append(L.cyl(0.145, 0.02, (0, 0, H - 0.09), rim, verts=12))
    for z in (0.04, 0.12):
        p.append(L.cyl(0.115 + z * 0.22, 0.012, (0, 0, z), rim, verts=12))
    p.append(L.cyl(0.13, 0.004, (0, 0, H - 0.07), "stone_dark", verts=12))                 # внутри (тёмное)
    pts = [(-0.145, H - 0.10), (-0.10, H - 0.02), (0.10, H - 0.02), (0.145, H - 0.10)]       # дужка
    for a, b in zip(pts, pts[1:]):
        p.append(L.tube((a[0], 0, a[1]), (b[0], 0, b[1]), 0.004, "steel_dark", verts=4))
    p.append(L.tube((-0.04, 0, H - 0.02), (0.04, 0, H - 0.02), 0.012, handle_grip, verts=6))
    return p


def metallicheskoe():
    p = bucket("steel", "steel_light", "wood")
    for i, (x, z) in enumerate(((0.05, 0.05), (-0.08, 0.14))):
        p.append(L.spot((x, -0.13, z), 0.04, "rust", seed=560 + i))
    return p


def plastikovoe():
    return bucket("paint_blue", "paint_blue", "soot")


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("metallicheskoe", metallicheskoe), ("plastikovoe", plastikovoe)):
        L.make(fn, "tool", "bucket", var, size_cm=(W * 100, H * 100), limit="small", rough=ROUGH)
    L.save_blend("tool", "bucket")
