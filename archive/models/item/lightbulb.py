"""Лампочка `lightbulb` (предмет). Размер — из плана ОС (6 × 12 см). Варианты (только idle; «перегоревшая» — пропуск):
  nakalivaniya — груша, цоколь с резьбой; svetodiodnaya — белый пластик, ребристый цоколь;
  lyuminestsentnaya_trubka — компактная трубка (две петли) на пластиковом цоколе.
Стекло — светлый цвет палитры (лампочка-предмет не светится). Запуск: python3 models/item/lightbulb.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("lightbulb"))
R = W / 2
ROUGH = {"min_area": 0.002, "k": 0.03, "amp_max": 0.002}


def base(p, h=0.025, color="steel"):
    p.append(L.cyl(R * 0.36, 0.006, (0, 0, 0), "soot", verts=8))
    for k in range(3):
        p.append(L.cyl(R * 0.45, 0.006, (0, 0, 0.006 + k * 0.006), color if k % 2 == 0 else "steel_dark", verts=8))
    p.append(L.cyl(R * 0.48, h - 0.024, (0, 0, 0.024), color, verts=8))


def nakalivaniya():
    p = []
    base(p)
    p.append(L.cyl(R * 0.48, 0.02, (0, 0, 0.025), "glass", verts=10, radius_top=R * 0.75))
    p.append(L.cyl(R * 0.75, 0.03, (0, 0, 0.045), "glass", verts=10, radius_top=R))
    p.append(L.cyl(R, 0.02, (0, 0, 0.075), "glass", verts=10, radius_top=R * 0.85))
    p.append(L.cyl(R * 0.85, 0.025, (0, 0, 0.095), "glass", verts=10, radius_top=R * 0.25))
    p.append(L.tube((-0.006, -0.002, 0.03), (-0.006, -0.002, 0.07), 0.0012, "soot", verts=4))     # нить
    p.append(L.tube((0.006, -0.002, 0.03), (0.006, -0.002, 0.07), 0.0012, "soot", verts=4))
    p.append(L.tube((-0.006, -0.002, 0.07), (0.006, -0.002, 0.07), 0.0015, "rust_light", verts=4))
    return p


def svetodiodnaya():
    p = []
    base(p, h=0.04, color="steel")
    p.append(L.cyl(R * 0.62, 0.025, (0, 0, 0.04), "plastic_white", verts=10, radius_top=R * 0.9))
    for k in range(3):
        p.append(L.box((0.002, 0.003, 0.018), (-0.012 + k * 0.012, -R * 0.66, 0.044), "offwhite", bevel=0))   # рёбра
    p.append(L.cyl(R * 0.95, 0.03, (0, 0, 0.065), "offwhite", verts=10, radius_top=R * 0.9))
    p.append(L.cyl(R * 0.9, 0.025, (0, 0, 0.095), "offwhite", verts=10, radius_top=R * 0.35))
    return p


def lyuminestsentnaya_trubka():
    p = []
    base(p, h=0.03)
    p.append(L.cyl(R * 0.75, 0.025, (0, 0, 0.03), "plastic_white", verts=10, radius_top=R * 0.7))
    for x in (-0.012, 0.012):
        for y in (-0.006, 0.006):
            p.append(L.cyl(0.0045, 0.06, (x, y, 0.055), "offwhite", verts=6))
        p.append(L.tube((x, -0.006, 0.115), (x, 0.006, 0.115), 0.0045, "offwhite", verts=6))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("nakalivaniya", nakalivaniya), ("svetodiodnaya", svetodiodnaya),
                    ("lyuminestsentnaya_trubka", lyuminestsentnaya_trubka)):
        L.make(fn, "item", "lightbulb", var, size_cm=(W * 100, H * 100), limit="small", rough=ROUGH)
    L.save_blend("item", "lightbulb")
