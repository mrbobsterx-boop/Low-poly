"""Стул `chair_wood`, вариант `derevyannyy` (деревянный). ОС: 45 × 90 см. Образец: docs/ref/furniture/chair_wood.png
Запуск: python3 models/furniture/chair_wood.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 0.45, 0.45, 0.90
SEAT = 0.46                 # высота сиденья
LEG = 0.045


def chair_idle():
    p = []
    # сиденье: две доски вдоль
    for i, col in enumerate(["wood_light", "wood"]):
        p.append(L.box((W, D / 2 - 0.004, 0.04), (0, -D / 4 + i * D / 2, SEAT - 0.04), col))
    # передние ножки
    for sx in (-1, 1):
        p.append(L.box((LEG, LEG, SEAT - 0.04), (sx * (W / 2 - 0.04), -(D / 2 - 0.04), 0), "wood"))
    # задние ножки — до верха спинки
    for sx in (-1, 1):
        p.append(L.box((LEG, LEG, H), (sx * (W / 2 - 0.04), D / 2 - 0.04, 0), "wood_dark"))
    # спинка: верхняя перекладина + три планки
    p.append(L.box((W - 0.02, 0.035, 0.08), (0, D / 2 - 0.04, H - 0.10), "wood"))
    for x in (-0.09, 0, 0.09):
        p.append(L.box((0.05, 0.025, H - SEAT - 0.12), (x, D / 2 - 0.04, SEAT), "wood_dark"))
    # царга под сиденьем спереди и перекладины между ножками
    p.append(L.box((W - 0.06, 0.03, 0.06), (0, -(D / 2 - 0.04), SEAT - 0.10), "wood_dark"))
    p.append(L.box((W - 0.06, 0.03, 0.03), (0, -(D / 2 - 0.04), 0.15), "wood_dark"))
    p.append(L.box((0.03, D - 0.06, 0.03), (-(W / 2 - 0.04), 0, 0.12), "wood_dark"))
    p.append(L.box((0.03, D - 0.06, 0.03), (W / 2 - 0.04, 0, 0.12), "wood_dark"))
    return p


def chair_broken():
    """Передняя правая ножка сломана: стул завалился вперёд-вправо, одна планка спинки выбита."""
    p = []
    tilt = (0, 14, 0)        # наклон вправо
    for i, col in enumerate(["wood_light", "wood"]):
        p.append(L.box((W, D / 2 - 0.004, 0.04), (0.04, -D / 4 + i * D / 2, SEAT - 0.10), col, rot=tilt))
    p.append(L.box((LEG, LEG, SEAT - 0.08), (-(W / 2 - 0.04), -(D / 2 - 0.04), 0), "wood", rot=(0, 10, 0)))
    p.append(L.box((LEG, LEG, 0.16), (W / 2 - 0.02, -(D / 2 - 0.04), 0), "wood"))              # обломок
    for sx in (-1, 1):
        p.append(L.box((LEG, LEG, H - 0.04), (sx * (W / 2 - 0.04), D / 2 - 0.04, 0), "wood_dark", rot=tilt))
    p.append(L.box((W - 0.02, 0.035, 0.08), (0.18, D / 2 - 0.04, H - 0.16), "wood", rot=tilt))
    for x in (-0.06, 0.10):
        p.append(L.box((0.05, 0.025, H - SEAT - 0.12), (x + 0.07, D / 2 - 0.04, SEAT - 0.05), "wood_dark", rot=tilt))
    # выбитая планка и отломанная ножка на полу
    p.append(L.box((H - SEAT - 0.12, 0.05, 0.025), (0.30, -0.30, 0), "wood_dark", rot=(0, 0, 25)))
    p.append(L.box((0.26, LEG, LEG), (-0.30, -0.28, 0), "wood", rot=(0, 0, -15)))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(chair_idle(), "furniture", "chair_wood", "derevyannyy", "idle", size_cm=(45, 90))
    L.finish(chair_broken(), "furniture", "chair_wood", "derevyannyy", "broken")
    L.save_blend("furniture", "chair_wood")
