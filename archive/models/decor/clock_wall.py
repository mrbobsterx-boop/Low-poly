"""Часы настенные `clock_wall`. Размер — из плана ОС (30 × 30 см). Висят: «спина» — Y = 0, низ — Z = 0.
Варианты (только idle; «сломанные» — пропуск): mehanicheskie — круглые, рамка, циферблат, стрелки 10:10;
elektronnye — корпус с табло (цифры светятся). Стрелки/цифры — в картинке (если игре нужно двигать — дать отдельно).
Запуск: python3 models/decor/clock_wall.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("clock_wall"))
R = W / 2
ROUGH = {"min_area": 0.004, "k": 0.03, "amp_max": 0.003}


def mehanicheskie():
    p = []
    zc = R
    p.append(L.cyl(R, 0.04, (0, 0.0, zc), "wood_dark", verts=16, rot=(90, 0, 0)))                  # рама (от стены к нам)
    p.append(L.cyl(R - 0.025, 0.006, (0, -0.044, zc), "offwhite", verts=16, rot=(90, 0, 0)))         # циферблат
    for k in range(12):
        a = math.pi / 2 - k * math.pi / 6
        L_ = 0.025 if k % 3 == 0 else 0.012
        x, z = (R - 0.04) * math.cos(a), (R - 0.04) * math.sin(a)
        p.append(L.box((0.006 if k % 3 else 0.01, 0.004, L_), (x, -0.049, zc + z - L_ / 2), "soot",
                       rot=(0, -math.degrees(math.pi / 2 - a), 0), bevel=0))
    for ang, ln, w in ((-60, 0.065, 0.008), (60, 0.095, 0.006)):     # 10:10 — часовая к 10, минутная к 2
        a = math.radians(90 - ang)
        p.append(L.tube((0, -0.052, zc), (ln * math.cos(a), -0.052, zc + ln * math.sin(a)), w / 2, "soot", verts=4))
    p.append(L.cyl(0.008, 0.008, (0, -0.058, zc), "paint_red", verts=8, rot=(90, 0, 0)))
    p.append(L.box((0.05, 0.003, 0.015), (0.07, -0.063, zc + 0.06), "plastic_white", rot=(0, 30, 0), bevel=0))   # блик
    p.append(L.spot((-0.09, -0.042, zc - 0.10), 0.03, "wood_light", seed=380))
    return p


def elektronnye():
    p = []
    p.append(L.box((W, 0.05, H * 0.55), (0, -0.025, H * 0.2), "soot", bevel=0.012))
    p.append(L.box((W - 0.04, 0.006, H * 0.35), (0, -0.052, H * 0.29), "stone_dark", bevel=0.003))
    # цифры «12:00» семисегментные — светятся
    segs = {"1": "bc", "2": "abged", "0": "abcdef"}
    pos = {"a": (0, 1, 1, 0), "b": (1, 1, 0, 1), "c": (1, 0, 0, 1), "d": (0, 0, 1, 0), "e": (0, 0, 0, 1),
           "f": (0, 1, 0, 1), "g": (0, 0.5, 1, 0)}
    cw, ch = 0.035, 0.06
    z0 = H * 0.29 + 0.025
    for i, d in enumerate("1200"):
        x0 = -0.105 + i * 0.055 + (0.02 if i > 1 else 0)
        for s in segs[d]:
            sx, sz, horiz, vert = pos[s]
            if horiz:
                p.append(L.box((cw, 0.004, 0.006), (x0 + cw / 2, -0.056, z0 + sz * ch - 0.003), "glow_screen", glow=True, bevel=0))
            else:
                half = 0 if sz == 0 else 1
                p.append(L.box((0.006, 0.004, ch / 2 - 0.004), (x0 + sx * cw, -0.056, z0 + half * ch / 2 + 0.002),
                               "glow_screen", glow=True, bevel=0))
    for dz in (0.018, 0.04):
        p.append(L.box((0.006, 0.004, 0.006), (0.0, -0.056, z0 + dz), "glow_screen", glow=True, bevel=0))
    for k in range(3):
        p.append(L.cyl(0.007, 0.006, (-0.06 + k * 0.03, -0.05, H * 0.24), "steel", verts=6, rot=(90, 0, 0)))
    p.append(L.tube((W / 2 - 0.03, -0.01, H * 0.2), (W / 2 - 0.03, -0.01, 0.0), 0.004, "soot", verts=4))   # провод
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("mehanicheskie", mehanicheskie), ("elektronnye", elektronnye)):
        L.make(fn, "decor", "clock_wall", var, size_cm=(W * 100, H * 100), limit="small", rough=ROUGH)
    L.save_blend("decor", "clock_wall")
