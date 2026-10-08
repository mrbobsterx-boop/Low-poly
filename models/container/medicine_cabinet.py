"""Аптечный шкафчик `medicine_cabinet` (навесной). Размер — из плана ОС (50 × 60 см). Дверца закрыта.
Варианты (только idle): vannyy — белый шкафчик с зеркальной дверцей; medpunkt — белый с красным крестом и стеклом
(видны силуэты флаконов); metallicheskiy — серо-зелёный стальной с замком и трафаретом.
Висит на стене: задняя стенка — в +Y. Запуск: python3 models/container/medicine_cabinet.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("medicine_cabinet"))
D = 0.15
F = -D / 2


def shell(p, color):
    p.append(L.box((W, D, H), (0, 0, 0), color, bevel=0.01))
    p.append(L.box((W - 0.04, 0.02, H - 0.04), (0, F - 0.006, 0.02), color, bevel=0.008))         # дверца


def cross(p, x, y, z, s, col):
    p.append(L.box((s, 0.004, s * 0.32), (x, y, z - s * 0.16), col, bevel=0))
    p.append(L.box((s * 0.32, 0.004, s), (x, y, z - s / 2), col, bevel=0))


def vannyy():
    p = []
    shell(p, "plastic_white")
    p.append(L.box((W - 0.10, 0.006, H - 0.12), (0, F - 0.018, 0.06), "glass", bevel=0.003))       # зеркало
    p.append(L.box((0.04, 0.003, 0.25), (-0.10, F - 0.022, 0.20), "steel_light", rot=(0, 30, 0), bevel=0))   # блик-полоса
    p.append(L.box((0.016, 0.02, 0.08), (W / 2 - 0.045, F - 0.03, H / 2 - 0.04), "steel", bevel=0.004))
    p.append(L.box((W, D + 0.01, 0.02), (0, 0, H - 0.02), "offwhite", bevel=0.004))               # карниз
    for i, (x, z, s, c) in enumerate(((-0.15, 0.10, 0.04, "dirt"), (0.12, 0.45, 0.03, "rust"))):
        p.append(L.spot((x, F - 0.022, z), s, c, seed=940 + i))
    return p


def medpunkt():
    p = []
    shell(p, "offwhite")
    p.append(L.box((W - 0.10, 0.006, H * 0.38), (0, F - 0.018, H * 0.55), "glass", bevel=0.003))
    for x, h, c in ((-0.13, 0.10, "rust_dark"), (-0.06, 0.08, "plastic_white"), (0.02, 0.12, "glass"), (0.10, 0.07, "paint_blue")):
        p.append(L.box((0.04, 0.004, h), (x, F - 0.023, H * 0.62), c, bevel=0))                    # силуэты флаконов
    p.append(L.box((W - 0.10, 0.004, 0.008), (0, F - 0.023, H * 0.61), "steel_dark", bevel=0))
    cross(p, 0, F - 0.02, H * 0.38, 0.11, "paint_red")
    p.append(L.box((0.016, 0.02, 0.06), (W / 2 - 0.045, F - 0.03, H / 2 - 0.03), "steel", bevel=0.004))
    p.append(L.spot((0.15, F - 0.02, 0.06), 0.04, "dirt", seed=945))
    return p


def metallicheskiy():
    p = []
    shell(p, "army_green")
    for z in (0.10, H - 0.16):                                                                       # выштамповки
        p.append(L.box((W - 0.12, 0.004, 0.06), (0, F - 0.018, z), "olive_dark", bevel=0))
    p.append(L.box((0.04, 0.02, 0.06), (W / 2 - 0.06, F - 0.026, H / 2 - 0.03), "steel_dark", bevel=0.004))   # замок
    p.append(L.cyl(0.008, 0.004, (W / 2 - 0.06, F - 0.036, H / 2), "soot", verts=6, rot=(90, 0, 0)))
    cross(p, -0.05, F - 0.02, H / 2 + 0.07, 0.10, "offwhite")
    for sx in (-1, 1):
        for z in (0.06, H - 0.08):
            p.append(L.cyl(0.006, 0.006, (sx * (W / 2 - 0.012), F - 0.0, z), "steel", verts=6, rot=(90, 0, 0)))
    for i, (x, z, s, c) in enumerate(((-0.17, 0.05, 0.05, "rust"), (0.15, H - 0.06, 0.04, "rust_dark"), (0.0, 0.25, 0.04, "steel"))):
        p.append(L.spot((x, F - 0.022, z), s, c, seed=948 + i))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("vannyy", vannyy), ("medpunkt", medpunkt), ("metallicheskiy", metallicheskiy)):
        L.make(fn, "container", "medicine_cabinet", var, size_cm=(W * 100, H * 100), broken="door")
    L.save_blend("container", "medicine_cabinet")
