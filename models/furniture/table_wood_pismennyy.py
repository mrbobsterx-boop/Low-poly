"""Стол `table_wood`, вариант `pismennyy` (письменный). ОС: 120 × 75 см.
Как на референсе автора: толстая столешница из досок, справа тумба с двумя ящиками (крашеный металл), слева ножки.
Запуск: python3 models/furniture/table_wood_pismennyy.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 1.20, 0.65, 0.75
TOP = 0.05
PED_W = 0.42              # ширина тумбы


def drawer(p, cx, z, w, h, y):
    p.append(L.box((w, 0.02, h), (cx, y - 0.01, z), "army_green", bevel=0.008))
    p.append(L.box((w * 0.35, 0.02, 0.022), (cx, y - 0.028, z + h * 0.62), "steel_dark", bevel=0.005))     # ручка
    p.append(L.box((w * 0.28, 0.006, 0.012), (cx, y - 0.04, z + h * 0.62 + 0.005), "steel_light", bevel=0))
    p.append(L.box((0.05, 0.004, 0.025), (cx, y - 0.022, z + h - 0.045), "offwhite", bevel=0))            # ярлык


def desk_idle():
    p = []
    # столешница: 3 доски вдоль, со щелями, с кромкой
    n, gap = 3, 0.006
    bd = (D - gap * (n - 1)) / n
    for i, col in enumerate(["wood", "wood_light", "wood"]):
        p.append(L.box((W, bd, TOP), (0, -D / 2 + bd / 2 + i * (bd + gap), H - TOP), col, bevel=0.01))
    p.append(L.box((W - 0.02, D - 0.02, 0.01), (0, 0, H - TOP - 0.004), "soot", bevel=0))
    for i in range(n):
        for x in (-W / 2 + 0.05, W / 2 - 0.05):
            p.append(L.box((0.012, 0.012, 0.003), (x, -D / 2 + bd / 2 + i * (bd + gap), H), "steel_dark", bevel=0))
    # тумба справа: корпус крашеный, цоколь, два ящика
    cx = W / 2 - PED_W / 2 - 0.03
    zt = H - TOP
    p.append(L.box((PED_W, D - 0.06, zt - 0.04), (cx, 0, 0.04), "khaki", bevel=0.012))
    p.append(L.box((PED_W - 0.03, D - 0.10, 0.04), (cx, 0, 0), "soot", bevel=0.006))
    yf = -(D - 0.06) / 2
    dh = (zt - 0.04 - 0.06) / 2
    for k in range(2):
        drawer(p, cx, 0.06 + k * (dh + 0.01), PED_W - 0.05, dh - 0.01, yf)
    # слева: две ножки, перекладина, ящик под столешницей
    for sy in (-1, 1):
        p.append(L.box((0.06, 0.06, zt), (-W / 2 + 0.06, sy * (D / 2 - 0.07), 0), "wood_dark", bevel=0.01))
    p.append(L.box((0.03, D - 0.16, 0.05), (-W / 2 + 0.06, 0, 0.14), "wood_dark", bevel=0.006))
    p.append(L.box((W - PED_W - 0.12, 0.025, 0.09), (-0.20, -(D / 2 - 0.06), zt - 0.09), "wood_dark", bevel=0.007))
    p.append(L.box((0.10, 0.012, 0.018), (-0.20, -(D / 2 - 0.06) - 0.018, zt - 0.055), "steel", bevel=0.004))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(desk_idle(), "furniture", "table_wood", "pismennyy", "idle", size_cm=(120, 75))
    L.save_blend("furniture", "table_wood_pismennyy")
