"""Оболочка комнаты бункера `shelter_living` (жилая), вариант `concrete`, состояние `normal`.
Пустая коробка БЕЗ мебели (docs/IMAGES.md, раздел 2): задняя стена + полоса пола + «неживой» декор.
Картинки:
  shelter_living_concrete_normal_mid   — сегмент 512 × 364 см, бесшовный по горизонтали
  shelter_living_concrete_normal_left  — срез левой стены, 50 × 364 см
  shelter_living_concrete_normal_right — срез правой стены, 50 × 364 см
  slab_bunker_concrete_normal          — перекрытие (передний срез), 512 × 100 см, бесшовное
Запуск: python3 models/room/shelter_living.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

SEG = 5.12          # ширина сегмента
D = 3.0             # глубина комнаты
H = 3.0             # высота комнаты
SLAB = 1.0          # толщина перекрытия
X0, X1 = -SEG / 2, SEG / 2
OV = 0.04           # модель шире кадра на 4 см с каждой стороны — края картинки сплошные
NB = 0              # без фасок у всего, что выходит за край кадра
T = 0.0001          # «бумажная» толщина: видна только лицевая сторона
# Кадр задаётся точно (frame_points), модель — чуть больше. Узор с шагом 1,28 м → стык при повторе невидим.
FRAME_MID = [(X0, 0, 0), (X1, 0, 0), (X0, D, H), (X1, D, H)]
FRAME_SLAB = [(X0, 0, 0), (X1, 0, 0), (X0, 0, SLAB), (X1, 0, SLAB)]


def along_x(radius, z, y, color, verts=8):
    """Труба/кабель на всю ширину (с запасом за край кадра)."""
    return L.cyl(radius, SEG + 2 * OV, (X0 - OV, y, z), color, verts=verts, rot=(0, 90, 0))


def repeat_x(step, offset=0.0):
    """Координаты X узора с шагом step на всю ширину с запасом (узор периодичен с периодом сегмента)."""
    n = round(SEG / step)
    return [X0 + offset + step * i for i in range(-1, n + 1)]


def shell_mid():
    p = []
    wide = SEG + 2 * OV
    # пол: плиты 1,28 м, швы посередине между краями сегмента
    p.append(L.box((wide, D + 0.03, T), (0, D / 2 - 0.015, -T), "concrete_dark", bevel=NB))   # на 3 см за кадр
    for x in repeat_x(1.28, 0.64):
        p.append(L.box((0.025, D, 0.002), (x, D / 2, 0), "stone_dark", bevel=NB))
    # задняя стена (до 3,05 м — верх закроет перекрытие): бетон, низ — тёмная полоса
    yw = D
    p.append(L.box((wide, T, H + 0.05), (0, yw, 0), "concrete_dark", bevel=NB))
    p.append(L.box((wide, 0.002, 1.05), (0, yw - 0.002, 0), "stone_dark", bevel=NB))
    for x in repeat_x(1.28, 0.64):
        p.append(L.box((0.025, 0.004, H + 0.05), (x, yw - 0.004, 0), "stone_dark", bevel=NB))
    p.append(L.box((wide, 0.004, 0.025), (0, yw - 0.004, 2.0), "stone_dark", bevel=NB))
    # трубы и кабель. Выше ~2,3 м задняя стена закрыта перекрытием (вид сверху 12°) — трубы ниже.
    p.append(along_x(0.07, 2.12, yw - 0.12, "steel"))
    p.append(along_x(0.045, 1.92, yw - 0.08, "rust"))
    p.append(along_x(0.015, 1.80, yw - 0.03, "soot", verts=6))
    # хомуты труб — раз в 1,28 м (на швах панелей, не на краю кадра)
    for x in repeat_x(1.28, 0.64)[1:-1]:
        p.append(L.box((0.04, 0.16, 0.30), (x, yw - 0.08, 1.88), "steel_dark"))
    # вентиляционная решётка и распределительная коробка — по одной на сегмент, внутри кадра
    p.append(L.box((0.50, 0.04, 0.30), (1.28, yw - 0.02, 1.30), "steel_dark"))
    for i in range(4):
        p.append(L.box((0.44, 0.02, 0.025), (1.28, yw - 0.045, 1.35 + i * 0.06), "soot", bevel=0))
    p.append(L.box((0.16, 0.06, 0.22), (-1.92, yw - 0.03, 1.40), "steel"))
    p.append(L.box((0.02, 0.02, 0.20), (-1.92, yw - 0.02, 1.62), "soot", bevel=0))
    return p


def side_wall(sign):
    """Срез боковой стены 0,5 м: торец к камере тёмный (разрез), как у перекрытия.
    Кадр 50 × 364 см; модель выше и шире кадра, чтобы края были сплошные."""
    x = sign * 0.25
    p = [L.box((0.5 + 2 * OV, D, H + 0.05), (x, D / 2, -0.03), "stone_dark", bevel=NB)]
    p.append(L.box((0.04, 0.004, H + 0.05), (x - sign * 0.23, -0.004, 0), "concrete_dark", bevel=0))
    for z in (0.6, 1.5, 2.4):
        p.append(L.box((0.03, 0.004, 0.03), (x + sign * 0.05, -0.005, z), "rust", bevel=0))
    frame = [(x - 0.25, 0, 0), (x + 0.25, 0, 0), (x - 0.25, D, H), (x + 0.25, D, H)]
    return p, frame


def slab():
    """Передний срез перекрытия 1 м: тёмный бетон, стяжка сверху, торцы арматуры (шаг 0,64 м)."""
    wide = SEG + 2 * OV
    p = [L.box((wide, T, SLAB + 0.04), (0, 0, -0.02), "stone_dark", bevel=NB)]
    p.append(L.box((wide, T, 0.10), (0, -T, SLAB - 0.08), "concrete_dark", bevel=NB))    # стяжка пола выше
    p.append(L.box((wide, T, 0.05), (0, -T, -0.02), "concrete_dark", bevel=NB))          # потолок ниже
    for z, off in ((0.30, 0.32), (0.65, 0.0)):
        for x in repeat_x(0.64, off):
            p.append(L.box((0.035, T, 0.035), (x, -2 * T, z), "rust", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(shell_mid(), "room", "shelter_living", "concrete", "normal_mid", limit="room", frame_points=FRAME_MID)
    for sign, side in ((-1, "left"), (1, "right")):
        parts, frame = side_wall(sign)
        L.finish(parts, "room", "shelter_living", "concrete", f"normal_{side}", limit="room", frame_points=frame)
    L.finish(slab(), "room", "slab_bunker", "concrete", "normal", limit="room", frame_points=FRAME_SLAB)
    L.save_blend("room", "shelter_living")
