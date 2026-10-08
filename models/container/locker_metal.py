"""Шкафчик `locker_metal`, вариант `armeyskiy` (армейский). ОС: 50 × 180 см. Образец: docs/ref/container/locker_metal.png
Запуск: python3 models/container/locker_metal.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 0.50, 0.50, 1.80
FEET = 0.06
WALL = 0.02


def body(p):
    """Корпус без дверей: стенки, крыша, дно, полка внутри."""
    h = H - FEET
    for sx in (-1, 1):
        p.append(L.box((WALL, D, h), (sx * (W / 2 - WALL / 2), 0, FEET), "army_green"))
        p.append(L.box((0.04, 0.04, FEET), (sx * (W / 2 - 0.04), -(D / 2 - 0.04), 0), "steel_dark"))
        p.append(L.box((0.04, 0.04, FEET), (sx * (W / 2 - 0.04), D / 2 - 0.04, 0), "steel_dark"))
    p.append(L.box((W, D, WALL), (0, 0, H - WALL), "army_green"))
    p.append(L.box((W, D, WALL), (0, 0, FEET), "army_green"))
    p.append(L.box((W - 2 * WALL, WALL, h - 2 * WALL), (0, D / 2 - WALL / 2, FEET + WALL), "olive_dark"))  # задняя
    p.append(L.box((W - 2 * WALL, D - 0.04, 0.015), (0, 0, H - 0.40), "olive_dark"))                  # полка


def door(x0, width, p, color="army_green"):
    """Дверца с жалюзи (вверху и внизу) и ручкой; x0 — левый край; стоит в плоскости фасада."""
    y = -(D / 2) - 0.005
    h = H - FEET - 0.04
    parts = [L.box((width - 0.008, 0.012, h), (x0 + width / 2, y, FEET + 0.02), color)]
    for z0 in (H - 0.30, FEET + 0.12):
        for i in range(4):
            parts.append(L.box((width * 0.55, 0.008, 0.015), (x0 + width / 2, y - 0.008, z0 + i * 0.035), "olive_dark", bevel=0))
    parts.append(L.box((0.015, 0.02, 0.10), (x0 + (width - 0.04 if x0 < 0 else 0.04), y - 0.012, FEET + 0.80), "steel_light"))
    p += parts
    return parts


def locker_idle():
    p = []
    body(p)
    door(-W / 2 + WALL / 2, W / 2 - WALL / 2, p)
    door(0, W / 2 - WALL / 2, p)
    # белая трафаретная звезда — простым ромбом-плашкой на правой дверце
    p.append(L.box((0.10, 0.006, 0.10), (W / 4, -(D / 2) - 0.014, H - 0.52), "offwhite", rot=(0, 45, 0)))
    return p


def locker_broken():
    """Правая дверца сорвана и висит на одной петле, левая вмята; внутри пусто, крыша погнута."""
    p = []
    body(p)
    door(-W / 2 + WALL / 2, W / 2 - WALL / 2, p, "khaki")              # вмятая — другой оттенок
    hang = []
    door(0, W / 2 - WALL / 2, hang, "army_green")
    for o in hang:      # повернуть вокруг правой петли наружу и чуть вниз
        L._place(o, (0, 0, 0), None)
        o.data.transform(__import__("mathutils").Matrix.Translation((W / 2, -D / 2, 0))
                         @ __import__("mathutils").Matrix.Rotation(__import__("math").radians(-70), 4, "Z")
                         @ __import__("mathutils").Matrix.Rotation(__import__("math").radians(6), 4, "Y")
                         @ __import__("mathutils").Matrix.Translation((-W / 2, D / 2, 0)))
    p += hang
    p.append(L.box((0.12, 0.10, 0.04), (0.05, -0.30, 0), "rust", rot=(0, 0, 20)))       # обломок на полу
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(locker_idle(), "container", "locker_metal", "armeyskiy", "idle", size_cm=(50, 180))
    L.finish(locker_broken(), "container", "locker_metal", "armeyskiy", "broken")
    L.save_blend("container", "locker_metal")
