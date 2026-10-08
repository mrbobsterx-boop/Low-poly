"""Буржуйка `stove_heat`, вариант `stalnaya_bochka` (стальная бочка). ОС: 60 × 90 см.
Образец: docs/ref/machine/stove_heat.png
Запуск: python3 models/machine/stove_heat.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = 0.60, 0.90
R = 0.255                   # радиус бочки
LEGS = 0.10
BARREL = 0.58
N = 10                      # граней у бочки


def barrel(p, color="steel_dark", ring="rust_dark"):
    p.append(L.cyl(R, BARREL, (0, 0, LEGS), color, verts=N))
    for z in (LEGS + 0.12, LEGS + BARREL - 0.14):
        p.append(L.cyl(R + 0.012, 0.025, (0, 0, z), ring, verts=N))
    p.append(L.cyl(R - 0.02, 0.02, (0, 0, LEGS + BARREL), "steel", verts=N))     # крышка


def legs(p):
    for x, y in ((-0.17, -0.12), (0.17, -0.12), (0, 0.18)):
        p.append(L.box((0.035, 0.035, LEGS + 0.02), (x, y, 0), "soot"))


def stove_idle():
    p = []
    legs(p)
    barrel(p)
    # дверца топки: рамка + три щели огня (светятся)
    y = -R - 0.005
    p.append(L.box((0.24, 0.02, 0.18), (0, y, LEGS + 0.16), "soot"))
    for x in (-0.06, 0, 0.06):
        p.append(L.box((0.03, 0.01, 0.10), (x, y - 0.012, LEGS + 0.20), "glow_fire", glow=True))
    # ручка дверцы и боковые ручки-скобы (по ним ширина 60 см)
    p.append(L.box((0.06, 0.03, 0.02), (0.15, y - 0.01, LEGS + 0.25), "steel_light"))
    for sx in (-1, 1):
        p.append(L.box((0.045, 0.03, 0.10), (sx * (R + 0.0225), 0, LEGS + BARREL - 0.24), "soot"))
    p.append(L.box((0.20, 0.02, 0.04), (0, y, LEGS + 0.06), "soot"))                         # поддувало
    # дымоход: по центру, наружу вверх
    p.append(L.cyl(0.055, H - LEGS - BARREL, (0, 0.05, LEGS + BARREL), "steel", verts=8))
    p.append(L.cyl(0.07, 0.03, (0, 0.05, H - 0.10), "rust", verts=8))
    return p


def stove_broken():
    """Прогорела и завалилась: бочка наклонена, огня нет, дымоход упал рядом, на полу зола."""
    p = []
    q = []
    legs(q)
    barrel(q, "rust_dark", "rust")
    y = -R - 0.005
    q.append(L.box((0.24, 0.02, 0.18), (0, y, LEGS + 0.16), "soot"))
    q.append(L.box((0.16, 0.012, 0.12), (-0.02, y - 0.012, LEGS + 0.32), "soot"))       # прогар
    for o in q:
        L._place(o, (0, 0, 0), (0, -12, 0))
    p += q
    p.append(L.cyl(0.055, 0.40, (0.30, -0.05, 0.055), "steel", verts=8, rot=(0, 80, 0)))  # дымоход лежит
    p.append(L.box((0.30, 0.20, 0.03), (-0.20, -0.25, 0), "soot", rot=(0, 0, 10)))          # зола
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(stove_idle(), "machine", "stove_heat", "stalnaya_bochka", "idle", size_cm=(60, 90))
    L.finish(stove_broken(), "machine", "stove_heat", "stalnaya_bochka", "broken")
    L.save_blend("machine", "stove_heat")
