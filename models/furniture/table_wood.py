"""Стол `table_wood`, вариант `obedennyy` (обеденный). ОС: 120 × 75 см. Образец: docs/ref/furniture/table_wood.png
Запуск: python3 models/furniture/table_wood.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402
from mathutils import Matrix  # noqa: E402

W, D, H = 1.20, 0.70, 0.75     # ширина, глубина, высота
TOP = 0.05                     # толщина столешницы
LEG = 0.07                     # сечение ножки


def top(parts, z, rot=None, pivot_x=0.0):
    """Столешница: три доски вдоль стола (видны торцами спереди и полосами сверху)."""
    bd = D / 3
    for i, col in enumerate(["wood", "wood_light", "wood"]):
        b = L.box((W, bd - 0.004, TOP), (0, -D / 2 + bd * (i + 0.5), 0), col)
        parts.append(b)
    m = Matrix.Translation((pivot_x, 0, z))
    if rot:
        m = m @ Matrix.Rotation(math.radians(rot), 4, "Y")
    m = m @ Matrix.Translation((-pivot_x, 0, 0))
    for b in parts[-3:]:
        b.data.transform(m)


def table_idle():
    p = []
    top(p, H - TOP)
    # царга (рама под столешницей)
    for sy in (-1, 1):
        p.append(L.box((W - 0.12, 0.03, 0.09), (0, sy * (D / 2 - 0.07), H - TOP - 0.09), "wood_dark"))
    # ножки
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.box((LEG, LEG, H - TOP), (sx * (W / 2 - 0.08), sy * (D / 2 - 0.08), 0), "wood_dark"))
    # перекладина между ножками внизу
    p.append(L.box((W - 0.16, 0.04, 0.04), (0, 0, 0.14), "wood_dark"))
    return p


def table_broken():
    """Правая ножка сломана — столешница целая, но правым концом лежит на полу."""
    p = []
    lx = -(W / 2 - 0.08)                          # левые ножки
    ang = math.degrees(math.asin((H - TOP) / (W - 0.08)))
    top(p, H - TOP, rot=ang, pivot_x=lx)          # наклон вокруг левых ножек
    for sy in (-1, 1):
        p.append(L.box((LEG, LEG, H - TOP), (lx, sy * (D / 2 - 0.08), 0), "wood_dark"))
    # правые ножки: обломок стоит, вторая лежит на полу
    p.append(L.box((LEG, LEG, 0.24), (W / 2 - 0.20, -(D / 2 - 0.08), 0), "wood_dark", rot=(0, 8, 0)))
    p.append(L.box((H - TOP, LEG, LEG), (W / 2 + 0.05, D / 2 - 0.10, 0), "wood_dark", rot=(0, 0, 12)))
    # щепки
    p.append(L.box((0.12, 0.05, 0.025), (W / 2 - 0.05, -0.28, 0), "wood_light", rot=(0, 0, 30)))
    p.append(L.box((0.08, 0.04, 0.025), (W / 2 - 0.32, -0.30, 0), "wood", rot=(0, 0, -20)))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(table_idle(), "furniture", "table_wood", "obedennyy", "idle", size_cm=(120, 75))
    L.finish(table_broken(), "furniture", "table_wood", "obedennyy", "broken")
    L.save_blend("furniture", "table_wood")
