"""Стул `chair_wood`, вариант `derevyannyy` (деревянный). ОС: 45 × 90 см. Образец: docs/ref/furniture/chair_wood.png
Версия 2 (подробная): сиденье из двух досок со щелью, гнутая (из 3 частей) верхняя перекладина, 3 планки спинки,
ножки с наклоном, царги, перекладины, гвозди.
Запуск: python3 models/furniture/chair_wood.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 0.45, 0.45, 0.90
SEAT = 0.46
LEG = 0.042


def chair_idle():
    p = []
    # сиденье: две доски поперёк с щелью, свес по краям
    for i, col in enumerate(["wood_light", "wood"]):
        p.append(L.box((W, D / 2 - 0.004, 0.035), (0, -D / 4 + i * D / 2, SEAT - 0.035), col, bevel=0.007))
    p.append(L.box((W - 0.02, D - 0.02, 0.006), (0, 0, SEAT - 0.036), "soot", bevel=0))
    # передние ножки (чуть разведены) и задние — продолжаются в спинку, слегка назад
    for sx in (-1, 1):
        p.append(L.cyl(LEG * 0.62, SEAT - 0.035, (sx * (W / 2 - 0.045), -(D / 2 - 0.045), 0), "wood",
                       verts=4, radius_top=LEG * 0.7, rot=(0, sx * -2, 0)))
        p.append(L.cyl(LEG * 0.62, H, (sx * (W / 2 - 0.045), D / 2 - 0.045, 0), "wood_dark",
                       verts=4, radius_top=LEG * 0.66, rot=(-6, 0, 0)))
    # верхняя перекладина спинки — из трёх частей с изгибом
    yb = D / 2 - 0.045 + 0.05
    p.append(L.box((0.16, 0.03, 0.09), (0, yb + 0.01, H - 0.12), "wood", bevel=0.007))
    for sx in (-1, 1):
        p.append(L.box((0.15, 0.03, 0.09), (sx * 0.14, yb, H - 0.12), "wood", rot=(0, 0, sx * -10), bevel=0.007))
    p.append(L.box((W - 0.06, 0.025, 0.04), (0, yb - 0.03, SEAT + 0.10), "wood_dark", bevel=0.005))   # нижняя
    for x in (-0.085, 0, 0.085):
        p.append(L.box((0.045, 0.02, H - SEAT - 0.24), (x, yb - 0.015, SEAT + 0.14), "wood_light", rot=(-5, 0, 0), bevel=0.005))
    # царги и перекладины ног
    p.append(L.box((W - 0.08, 0.02, 0.06), (0, -(D / 2 - 0.045), SEAT - 0.095), "wood_dark", bevel=0.005))
    for sx in (-1, 1):
        p.append(L.box((0.02, D - 0.09, 0.03), (sx * (W / 2 - 0.045), 0, 0.14), "wood_dark", bevel=0.004))
    p.append(L.box((W - 0.09, 0.02, 0.025), (0, -(D / 2 - 0.045), 0.20), "wood_dark", bevel=0.004))
    # гвозди на сиденье
    for x in (-W / 2 + 0.04, W / 2 - 0.04):
        for y in (-D / 4, D / 4):
            p.append(L.box((0.01, 0.01, 0.003), (x, y, SEAT), "steel_dark", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(chair_idle, "furniture", "chair_wood", "derevyannyy", size_cm=(45, 90), broken="legs")
    L.save_blend("furniture", "chair_wood")
