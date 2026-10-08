"""Стол `table_wood`, вариант `obedennyy` (обеденный). ОС: 120 × 75 см. Образец: docs/ref/furniture/table_wood.png
Версия 2 (подробная, под референс автора): столешница из досок со щелями, сужающиеся ножки, царга, уголки, гвозди.
Стулья с образца — отдельные предметы, сюда не входят.
Запуск: python3 models/furniture/table_wood.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 1.20, 0.70, 0.75
TOP = 0.045
LEG = 0.065


def leg(p, x, y):
    """Ножка: чуть сужается книзу (четырёхгранный усечённый конус) + тёмный «башмак»."""
    p.append(L.cyl(LEG * 0.62, H - TOP - 0.03, (x, y, 0.03), "wood_dark", verts=4, radius_top=LEG * 0.74))
    p.append(L.cyl(LEG * 0.66, 0.03, (x, y, 0), "stone_dark", verts=4))


def table_idle():
    p = []
    # столешница: 4 доски вдоль, щели между ними, разные оттенки
    n, gap = 4, 0.006
    bd = (D - gap * (n - 1)) / n
    for i, col in enumerate(["wood", "wood_light", "wood", "wood_light"]):
        y = -D / 2 + bd / 2 + i * (bd + gap)
        p.append(L.box((W, bd, TOP), (0, y, H - TOP), col, bevel=0.008))
    p.append(L.box((W - 0.02, D - 0.02, 0.01), (0, 0, H - TOP - 0.004), "soot", bevel=0))      # тень щелей
    # гвозди по краям досок (тёмные точки сверху)
    for i in range(n):
        y = -D / 2 + bd / 2 + i * (bd + gap)
        for x in (-W / 2 + 0.06, W / 2 - 0.06):
            p.append(L.box((0.012, 0.012, 0.003), (x, y, H), "steel_dark", bevel=0))
    # царга: доски под столешницей по периметру
    for sy in (-1, 1):
        p.append(L.box((W - 0.16, 0.025, 0.10), (0, sy * (D / 2 - 0.07), H - TOP - 0.10), "wood_dark", bevel=0.006))
    for sx in (-1, 1):
        p.append(L.box((0.025, D - 0.16, 0.10), (sx * (W / 2 - 0.08), 0, H - TOP - 0.10), "wood_dark", bevel=0.006))
    # ножки и нижняя перекладина
    for sx in (-1, 1):
        for sy in (-1, 1):
            leg(p, sx * (W / 2 - 0.08), sy * (D / 2 - 0.08))
    for sx in (-1, 1):
        p.append(L.box((0.03, D - 0.18, 0.04), (sx * (W / 2 - 0.08), 0, 0.16), "wood", bevel=0.006))
    p.append(L.box((W - 0.18, 0.03, 0.04), (0, 0, 0.16), "wood", bevel=0.006))
    # металлические уголки на царге спереди
    for sx in (-1, 1):
        p.append(L.box((0.05, 0.006, 0.05), (sx * (W / 2 - 0.12), -(D / 2 - 0.083), H - TOP - 0.08), "steel_dark", bevel=0.002))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(table_idle, "furniture", "table_wood", "obedennyy", size_cm=(120, 75), broken="legs")
    L.save_blend("furniture", "table_wood")
