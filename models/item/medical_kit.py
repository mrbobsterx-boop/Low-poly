"""Медицинский набор `medical_kit` (предмет). Размер — из плана ОС (35 × 25 см). Варианты (только idle):
  polevoy — брезентовая сумка-укладка с ремнём; hirurgicheskiy — металлический кейс-бикс с ручкой;
  ekstrennyy — ярко-оранжевый пластиковый кейс с защёлками. Запуск: python3 models/item/medical_kit.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("medical_kit"))
ROUGH = {"min_area": 0.003, "k": 0.025, "amp_max": 0.003}
D = 0.16


def cross(p, x, y, z, s, col):
    p.append(L.box((s, 0.004, s * 0.32), (x, y, z - s * 0.16), col, bevel=0))
    p.append(L.box((s * 0.32, 0.004, s), (x, y, z - s / 2), col, bevel=0))


def polevoy():
    p = [L.soft((W, D, H - 0.04), (0, 0, 0), "khaki")]
    p.append(L.box((W - 0.03, 0.02, 0.10), (0, -D / 2 + 0.006, H - 0.15), "khaki_light", bevel=0.006))
    for sx in (-1, 1):
        p.append(L.box((0.03, 0.02, 0.05), (sx * 0.08, -D / 2 - 0.006, H - 0.16), "soot", bevel=0.004))
    p.append(L.cyl(0.04, 0.004, (0, -D / 2 - 0.002, 0.08), "offwhite", verts=10, rot=(90, 0, 0)))
    cross(p, 0, -D / 2 - 0.004, 0.105, 0.05, "paint_red")
    for sx in (-1, 1):                                                                       # ремень
        p.append(L.tube((sx * (W / 2 - 0.02), 0, H - 0.06), (sx * 0.06, 0, H - 0.005), 0.008, "olive_dark", verts=4))
    p.append(L.tube((-0.06, 0, H - 0.005), (0.06, 0, H - 0.005), 0.008, "olive_dark", verts=4))
    return p


def hirurgicheskiy():
    p = [L.box((W, D, H - 0.04), (0, 0, 0), "steel_light", bevel=0.012)]
    p.append(L.box((W + 0.004, D + 0.004, 0.015), (0, 0, H - 0.10), "steel", bevel=0.004))
    for sx in (-1, 1):
        p.append(L.box((0.03, 0.012, 0.04), (sx * 0.11, -D / 2 - 0.006, H - 0.12), "steel_dark", bevel=0.004))
    p.append(L.box((0.10, 0.03, 0.015), (0, 0, H - 0.015), "soot", bevel=0.005))
    for sx in (-1, 1):
        p.append(L.box((0.012, 0.02, 0.03), (sx * 0.05, 0, H - 0.042), "steel_dark", bevel=0.003))
    cross(p, -0.1, -D / 2 - 0.002, 0.09, 0.04, "paint_red")
    p.append(L.spot((0.08, -D / 2 - 0.003, 0.05), 0.03, "steel", seed=935))
    return p


def ekstrennyy():
    p = [L.box((W, D, H - 0.03), (0, 0, 0), "hazard_yellow", bevel=0.018)]
    p.append(L.box((W + 0.004, D + 0.004, 0.014), (0, 0, H - 0.10), "soot", bevel=0.004))
    for sx in (-1, 1):
        p.append(L.box((0.035, 0.016, 0.035), (sx * 0.11, -D / 2 - 0.008, H - 0.11), "soot", bevel=0.005))
    p.append(L.box((0.10, 0.03, 0.02), (0, 0, H - 0.02), "soot", bevel=0.006))
    p.append(L.box((0.12, 0.004, 0.06), (0, -D / 2 - 0.002, 0.03), "offwhite", bevel=0))
    cross(p, 0, -D / 2 - 0.004, 0.08, 0.045, "paint_red")
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("polevoy", polevoy), ("hirurgicheskiy", hirurgicheskiy), ("ekstrennyy", ekstrennyy)):
        L.make(fn, "item", "medical_kit", var, size_cm=(W * 100, H * 100), limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "medical_kit")
