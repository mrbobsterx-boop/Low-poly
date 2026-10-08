"""Оболочка комнаты бункера `shelter_living`, вариант `concrete`, состояние `normal` — версия 2, по референсу автора.
Пустая коробка БЕЗ мебели (docs/IMAGES.md, раздел 2). Картинки:
  shelter_living_concrete_normal_mid   — сегмент 512 × 364 см, бесшовный
  shelter_living_concrete_normal_left  — срез левой стены 50 × 364 см (рубленый камень)
  shelter_living_concrete_normal_right — срез правой стены
  slab_bunker_concrete_normal          — перекрытие 512 × 100 см, бесшовное (рубленый камень + балка)
Выше ~2,35 м задняя стена закрыта перекрытием (камера сверху 12°) — трубы и щитки ниже.
Запуск: python3 models/room/shelter_living.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

SEG, D, H, SLAB = 5.12, 3.0, 3.0, 1.0
X0, X1 = -SEG / 2, SEG / 2
OV = 0.04                 # модель шире кадра — края сплошные
WIDE = SEG + 2 * OV
T = 0.0001
STEP = 1.28               # шаг узора (панели, хомуты) — период сегмента
YW = D                    # плоскость задней стены
FRAME_MID = [(X0, 0, 0), (X1, 0, 0), (X0, D, H), (X1, D, H)]
FRAME_SLAB = [(X0, 0, 0), (X1, 0, 0), (X0, 0, SLAB), (X1, 0, SLAB)]


def xs(offset=0.0):
    """X узора с шагом STEP на всю ширину с запасом."""
    n = round(SEG / STEP)
    return [X0 + offset + STEP * i for i in range(-1, n + 1)]


def pipe_x(r, z, y, color, verts=8):
    return L.cyl(r, WIDE, (X0 - OV, y, z), color, verts=verts, rot=(0, 90, 0))


def rock_face(w, h, loc, color, seed, nx, ny, depth=0.05):
    """Рубленый камень: вертикальная «ткань» из граней лицом к камере (края ровные — для стыков)."""
    s = L.sheet(nx, ny, w, h, (0, 0, 0), color, jitter=depth, seed=seed, thick=0.02)
    L.transform([s], loc, (90, 0, 0))
    return s


def shell_mid():
    p = []
    # пол: бетонные плиты с швами + передняя кромка
    p.append(L.box((WIDE, D + 0.03, T), (0, D / 2 - 0.015, -T), "concrete_dark", bevel=0))
    for x in xs(0.64):
        p.append(L.box((0.02, D, 0.002), (x, D / 2, 0), "stone_dark", bevel=0))
    p.append(L.box((WIDE, 0.002, 0.002), (0, 1.5, 0), "stone_dark", bevel=0))
    # стена: панели (чередуются оттенком), швы, плинтус
    for x in xs(0.0):
        p.append(L.box((STEP - 0.02, 0.004, H + 0.05), (x + STEP / 2, YW - 0.002, 0), "concrete", bevel=0))
    p.append(L.box((WIDE, T, H + 0.05), (0, YW, 0), "stone_dark", bevel=0))                 # швы между панелями
    p.append(L.box((WIDE, 0.04, 0.14), (0, YW - 0.02, 0), "concrete_dark", bevel=0))        # плинтус
    for x in xs(0.0):                                                                        # заклёпки на швах
        for z in (0.4, 1.0, 1.6):
            p.append(L.box((0.02, 0.006, 0.02), (x, YW - 0.006, z), "steel_dark", bevel=0))
    # трубы: толстая с фланцами, тонкая ржавая, пучок кабелей на скобах
    p.append(pipe_x(0.075, 2.12, YW - 0.16, "steel_dark", verts=10))
    for x in xs(0.32):
        p.append(L.cyl(0.095, 0.05, (x - 0.025, YW - 0.16, 2.12), "rust_dark", verts=10, rot=(0, 90, 0)))
    p.append(pipe_x(0.045, 1.93, YW - 0.08, "rust", verts=8))
    for k, z in enumerate((1.78, 1.75, 1.72)):
        p.append(pipe_x(0.014, z, YW - 0.03 - k * 0.012, "soot", verts=6))
    for x in xs(0.96):
        p.append(L.box((0.03, 0.06, 0.12), (x, YW - 0.03, 1.68), "steel", bevel=0.004))
    # колено вниз: вертикальная труба до пола (одна на сегмент, внутри кадра)
    xv = X0 + 1.92
    p.append(L.cyl(0.075, 0.18, (xv, YW - 0.16, 2.0), "steel_dark", verts=10))
    p.append(L.cyl(0.09, 0.08, (xv, YW - 0.16, 1.95), "rust_dark", verts=10))
    p.append(L.cyl(0.06, 1.95, (xv, YW - 0.16, 0.0), "steel_dark", verts=10))
    p.append(L.cyl(0.08, 0.05, (xv, YW - 0.16, 0.9), "rust_dark", verts=10))
    p.append(L.cyl(0.085, 0.06, (xv, YW - 0.16, 0.0), "rust_dark", verts=10))
    # вентиль на вертикальной трубе
    p.append(L.cyl(0.07, 0.015, (xv, YW - 0.30, 1.2), "paint_red", verts=8, rot=(90, 0, 0)))
    p.append(L.box((0.02, 0.10, 0.02), (xv, YW - 0.24, 1.19), "steel", bevel=0.004))
    # щиток с кабелем и предупреждающий знак
    xb = X0 + 3.9
    p.append(L.box((0.34, 0.10, 0.46), (xb, YW - 0.05, 1.05), "steel", bevel=0.012))
    p.append(L.box((0.30, 0.012, 0.42), (xb, YW - 0.106, 1.07), "steel_light", bevel=0.006))
    p.append(L.box((0.10, 0.006, 0.09), (xb, YW - 0.114, 1.30), "hazard_yellow", rot=(0, 45, 0), bevel=0))
    p.append(L.box((0.03, 0.012, 0.05), (xb + 0.11, YW - 0.116, 1.20), "soot", bevel=0.003))
    p.append(L.box((0.03, 0.03, 0.22), (xb, YW - 0.03, 1.51), "soot", bevel=0))
    return p


def side_wall(sign):
    """Срез боковой стены 0,5 м: рубленый тёмный камень + бетонная кромка со стороны комнаты."""
    x = sign * 0.25
    p = [L.box((0.5 + 2 * OV, D, H + 0.05), (x, D / 2, -0.03), "soot", bevel=0)]
    p.append(rock_face(0.5 + 2 * OV, H + 0.1, (x, -0.03, (H + 0.05) / 2), "stone_dark", seed=20 + sign, nx=4, ny=14))
    p.append(L.box((0.06, 0.06, H + 0.05), (x - sign * 0.22, -0.02, -0.03), "concrete_dark", bevel=0.01))
    frame = [(x - 0.25, 0, 0), (x + 0.25, 0, 0), (x - 0.25, D, H), (x + 0.25, D, H)]
    return p, frame


def slab():
    """Перекрытие: рубленый камень + бетонная балка-кромка снизу (потолок) и сверху (пол этажа)."""
    p = [L.box((WIDE, T, SLAB + 0.06), (0, 0.03, -0.03), "soot", bevel=0)]
    p.append(rock_face(WIDE, SLAB - 0.2, (0, -0.04, 0.5), "stone_dark", seed=31, nx=24, ny=5, depth=0.04))
    p.append(L.box((WIDE, 0.10, 0.12), (0, -0.04, -0.03), "concrete_dark", bevel=0))
    p.append(L.box((WIDE, 0.10, 0.10), (0, -0.04, SLAB - 0.07), "concrete_dark", bevel=0))
    for x in xs(0.64):
        p.append(L.box((0.03, 0.012, 0.03), (x, -0.095, 0.03), "rust", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(shell_mid(), "room", "shelter_living", "concrete", "normal_mid", limit="room", frame_points=FRAME_MID, lit=False)
    for sign, side in ((-1, "left"), (1, "right")):
        parts, frame = side_wall(sign)
        L.finish(parts, "room", "shelter_living", "concrete", f"normal_{side}", limit="room", frame_points=frame, lit=False)
    L.finish(slab(), "room", "slab_bunker", "concrete", "normal", limit="room", frame_points=FRAME_SLAB, lit=False)
    L.save_blend("room", "shelter_living")
