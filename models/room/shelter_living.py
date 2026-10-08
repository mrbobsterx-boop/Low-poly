"""Оболочка комнаты бункера `shelter_living`, вариант `concrete`, состояние `normal` — версия 3 (по замечаниям автора).
Пустая коробка БЕЗ мебели (docs/IMAGES.md, раздел 2): стена — тёплый тёмный бетон; толстая бетонная рамка со скосом;
детали на стене; износ пятнами палитры; крупные неровные грани. Картинки:
  shelter_living_concrete_normal_mid   — сегмент 512 × 364 см, бесшовный
  shelter_living_concrete_normal_left  — срез левой стены 50 × 364 см (со скосом к комнате)
  shelter_living_concrete_normal_right — срез правой стены
  slab_bunker_concrete_normal          — перекрытие 512 × 100 см, бесшовное (скос снизу)
Выше ~2,35 м задняя стена закрыта перекрытием (камера сверху 12°) — детали ниже.
Запуск: python3 models/room/shelter_living.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

SEG, D, H, SLAB = 5.12, 3.0, 3.0, 1.0
X0, X1 = -SEG / 2, SEG / 2
OV = 0.04
WIDE = SEG + 2 * OV
STEP = 1.28
YW = D
WALL, FRAME, BEVEL_IN = "concrete_warm", "stone_dark", "concrete_dark"
FRAME_MID = [(X0, 0, 0), (X1, 0, 0), (X0, D, H), (X1, D, H)]
FRAME_SLAB = [(X0, 0, 0), (X1, 0, 0), (X0, 0, SLAB), (X1, 0, SLAB)]
ROUGH_SHELL = {"min_area": 0.12, "k": 0.03, "amp_max": 0.025, "levels": 2, "shade_p": 0.45}


def xs(offset=0.0):
    n = round(SEG / STEP)
    return [X0 + offset + STEP * i for i in range(-1, n + 1)]


def pipe_x(r, z, y, color, verts=8):
    return L.cyl(r, WIDE, (X0 - OV, y, z), color, verts=verts, rot=(0, 90, 0))


def shell_mid():
    p = []
    # пол: толстая плита (верх — Z = 0), швы, потёртости
    p.append(L.box((WIDE, D + 0.03, 0.08), (0, D / 2 - 0.015, -0.08), "concrete_dark", bevel=0))
    for x in xs(0.64):
        p.append(L.box((0.02, D, 0.003), (x, D / 2, 0), "stone_dark", bevel=0))
    p.append(L.box((WIDE, 0.02, 0.003), (0, 1.5, 0), "stone_dark", bevel=0))
    for i, (x, y, s, c) in enumerate(((-1.6, 0.6, 0.5, "stone_dark"), (0.4, 2.1, 0.6, "concrete"),
                                      (1.7, 1.0, 0.4, "stone_dark"), (-0.5, 1.2, 0.35, "dirt"))):
        p.append(L.spot((x, y, 0.0), s, c, facing="top", seed=200 + i, stretch=(1.6, 0.8)))
    # стена: панели тёплого бетона (толстые — для вмятин), между ними тёмный шов
    p.append(L.box((WIDE, 0.02, H + 0.05), (0, YW + 0.10, 0), "soot", bevel=0))
    for x in xs(0.0):
        p.append(L.box((STEP - 0.03, 0.10, H + 0.05), (x + STEP / 2, YW + 0.05, 0), WALL, bevel=0.015))   # лицо — Y = YW
    p.append(L.box((WIDE, 0.05, 0.16), (0, YW - 0.025, 0), "concrete_dark", bevel=0))           # плинтус
    for x in xs(0.0):                                                                           # болты на швах
        for z in (0.45, 1.05, 1.65, 2.2):
            p.append(L.box((0.03, 0.012, 0.03), (x, YW - 0.006, z), "steel_dark", bevel=0.004))
    # износ стены: сколы (светлее), потёки (темнее) — внутри сегмента
    for i, (x, z, s, c, st) in enumerate(((-2.1, 0.9, 0.14, "concrete", (1, 0.7)), (-0.2, 0.35, 0.18, "concrete", (1.3, 0.6)),
                                          (1.0, 1.55, 0.12, "concrete", (1, 1)), (2.3, 0.6, 0.10, "concrete", (1, 1)),
                                          (-1.25, 1.55, 0.30, "concrete_dark", (0.5, 1.8)), (0.95, 1.55, 0.26, "concrete_dark", (0.45, 2.0)),
                                          (-2.4, 1.70, 0.20, "concrete_dark", (0.5, 1.6)))):
        p.append(L.spot((x, YW - 0.003, z), s, c, seed=300 + i, stretch=st))
    # трещина — цепочка тонких тёмных штрихов
    for k, (dx, dz, rot) in enumerate(((0, 0, 20), (0.05, -0.06, -30), (0.09, -0.13, 15), (0.13, -0.20, -25))):
        p.append(L.box((0.09, 0.004, 0.008), (0.30 + dx, YW - 0.004, 1.30 + dz), "soot", rot=(0, rot, 0), bevel=0))
    # трубы, фланцы, ржавые потёки под фланцами
    p.append(pipe_x(0.075, 2.12, YW - 0.16, "steel_dark", verts=10))
    for x in xs(0.32):
        p.append(L.cyl(0.095, 0.05, (x - 0.025, YW - 0.16, 2.12), "rust_dark", verts=10, rot=(0, 90, 0)))
    for x in xs(0.32)[1:-1]:
        p.append(L.spot((x, YW - 0.004, 1.95), 0.10, "rust", seed=int(x * 100) % 97, stretch=(0.35, 2.2)))
    p.append(pipe_x(0.045, 1.93, YW - 0.08, "rust", verts=8))
    for k, z in enumerate((1.78, 1.75, 1.72)):
        p.append(pipe_x(0.014, z, YW - 0.03 - k * 0.012, "soot", verts=6))
    for x in xs(0.96):
        p.append(L.box((0.03, 0.06, 0.12), (x, YW - 0.03, 1.68), "steel", bevel=0.004))
    # колено вниз: вертикальная труба до пола + вентиль
    xv = X0 + 1.92
    p.append(L.cyl(0.075, 0.18, (xv, YW - 0.16, 2.0), "steel_dark", verts=10))
    p.append(L.cyl(0.09, 0.08, (xv, YW - 0.16, 1.95), "rust_dark", verts=10))
    p.append(L.cyl(0.06, 1.95, (xv, YW - 0.16, 0.0), "steel_dark", verts=10))
    for z in (0.9, 0.0):
        p.append(L.cyl(0.08, 0.05, (xv, YW - 0.16, z), "rust_dark", verts=10))
    p.append(L.cyl(0.07, 0.015, (xv, YW - 0.30, 1.2), "paint_red", verts=8, rot=(90, 0, 0)))
    p.append(L.box((0.02, 0.10, 0.02), (xv, YW - 0.24, 1.19), "steel", bevel=0.004))
    # щиток, кабель к нему, знак
    xb = X0 + 3.9
    p.append(L.box((0.34, 0.10, 0.46), (xb, YW - 0.05, 1.05), "steel", bevel=0.012))
    p.append(L.box((0.30, 0.012, 0.42), (xb, YW - 0.106, 1.07), "steel_light", bevel=0.006))
    p.append(L.box((0.10, 0.006, 0.09), (xb, YW - 0.114, 1.30), "hazard_yellow", rot=(0, 45, 0), bevel=0))
    p.append(L.box((0.03, 0.012, 0.05), (xb + 0.11, YW - 0.116, 1.20), "soot", bevel=0.003))
    p.append(L.box((0.03, 0.03, 0.22), (xb, YW - 0.03, 1.51), "soot", bevel=0))
    p.append(L.spot((xb + 0.08, YW - 0.118, 1.12), 0.05, "steel", seed=410))
    # карта на стене (бумага с пятнами-«местностью» и красным крестом), прикреплена кнопками
    xm, zm = X0 + 0.75, 1.30
    p.append(L.box((0.50, 0.006, 0.36), (xm, YW - 0.004, zm), "offwhite", rot=(0, 2, 0), bevel=0))
    for i, (dx, dz, s, c) in enumerate(((-0.12, 0.20, 0.16, "cloth_beige"), (0.10, 0.12, 0.14, "khaki_light"),
                                        (-0.02, 0.26, 0.10, "paint_blue"), (0.14, 0.27, 0.08, "cloth_beige"))):
        p.append(L.spot((xm + dx, YW - 0.009, zm + dz), s, c, seed=420 + i, stretch=(1.4, 0.8)))
    for rot in (40, -40):
        p.append(L.box((0.06, 0.004, 0.012), (xm + 0.06, YW - 0.012, zm + 0.15), "paint_red", rot=(0, rot, 0), bevel=0))
    for dx in (-0.23, 0.23):
        p.append(L.box((0.018, 0.008, 0.018), (xm + dx, YW - 0.012, zm + 0.33), "paint_red", bevel=0))
    # вентрешётка
    xg = X0 + 4.65
    p.append(L.box((0.42, 0.05, 0.30), (xg, YW - 0.025, 0.40), "steel_dark", bevel=0.01))
    for i in range(5):
        p.append(L.box((0.36, 0.02, 0.022), (xg, YW - 0.055, 0.44 + i * 0.048), "soot", rot=(-30, 0, 0), bevel=0))
    # трафарет «B-2» (простыми штрихами)
    xs_, zs = X0 + 2.65, 1.45
    for dx, dz, w, h in ((0, 0, 0.025, 0.16), (0.03, 0.145, 0.05, 0.02), (0.03, 0.07, 0.05, 0.02), (0.03, 0.0, 0.05, 0.02),
                         (0.065, 0.085, 0.022, 0.065), (0.065, 0.015, 0.022, 0.06),                     # B
                         (0.12, 0.07, 0.04, 0.02),                                                       # -
                         (0.20, 0.145, 0.07, 0.02), (0.245, 0.08, 0.025, 0.07), (0.20, 0.07, 0.07, 0.02),
                         (0.175, 0.0, 0.025, 0.07), (0.20, 0.0, 0.07, 0.02)):
        p.append(L.box((w, 0.004, h), (xs_ + dx, YW - 0.004, zs + dz), "offwhite", bevel=0))
    return p


def side_wall(sign):
    """Срез боковой стены: толстый бетон со скосом 12 см к комнате, сколы. sign: −1 левая, +1 правая."""
    # профиль в плане (x, y): внешний край — x0, внутренний (у комнаты) — x1
    x1 = 0.0
    x0 = -sign * 0.5 - sign * OV
    bev = 0.12
    pts = [(x0, -0.0), (x1 + sign * -bev, -0.0), (x1, bev), (x1, 0.6), (x0, 0.6)]
    if sign > 0:
        pts = pts[::-1]
    cols = {1: BEVEL_IN} if sign < 0 else {2: BEVEL_IN}
    p = [L.prism(pts, "z", -0.08, H + 0.05, FRAME, face_colors=cols)]
    xm = -sign * 0.25
    for i, (dx, z, s, c) in enumerate(((0.05, 0.4, 0.10, "concrete_dark"), (-0.08, 1.3, 0.14, "soot"),
                                       (0.06, 2.1, 0.08, "concrete_dark"), (-0.02, 2.7, 0.12, "concrete_dark"))):
        p.append(L.spot((xm + dx * sign, -0.002, z), s, c, seed=500 + i + (10 if sign > 0 else 0), stretch=(0.8, 1.3)))
    for z in (0.7, 1.6, 2.5):
        p.append(L.box((0.03, 0.008, 0.03), (xm + sign * 0.06, -0.004, z), "rust", bevel=0))
    frame = [(xm - 0.25, 0, 0), (xm + 0.25, 0, 0), (xm - 0.25, D, H), (xm + 0.25, D, H)]
    return p, frame


def slab():
    """Перекрытие: толстый бетон, скос 14 см снизу к комнате и 4 см сверху, торцы арматуры, сколы."""
    pts = [(0.0, 0.14), (0.14, -0.02), (0.6, -0.02), (0.6, SLAB + 0.02), (0.04, SLAB + 0.02), (0.0, SLAB - 0.02)]
    p = [L.prism(pts, "x", X0 - OV, X1 + OV, FRAME, face_colors={0: BEVEL_IN, 4: BEVEL_IN})]
    for x in xs(0.64):
        for z in (0.40, 0.70):
            p.append(L.box((0.035, 0.01, 0.035), (x + (0.32 if z > 0.5 else 0), -0.004, z), "rust", bevel=0))
    for x in xs(0.0)[1:-1]:
        p.append(L.spot((x + 0.5, -0.003, 0.55), 0.18, "concrete_dark", seed=int(x * 10) % 50 + 600, stretch=(1.6, 0.7)))
        p.append(L.spot((x + 0.95, -0.003, 0.30), 0.10, "soot", seed=int(x * 10) % 50 + 650))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(shell_mid(), "room", "shelter_living", "concrete", "normal_mid", limit="room", frame_points=FRAME_MID,
             rough=ROUGH_SHELL, period=SEG)
    for sign, side in ((-1, "left"), (1, "right")):
        parts, frame = side_wall(sign)
        L.finish(parts, "room", "shelter_living", "concrete", f"normal_{side}", limit="room", frame_points=frame,
                 rough=dict(ROUGH_SHELL, min_area=0.06))
    L.finish(slab(), "room", "slab_bunker", "concrete", "normal", limit="room", frame_points=FRAME_SLAB,
             rough=ROUGH_SHELL, period=SEG)
    L.save_blend("room", "shelter_living")
