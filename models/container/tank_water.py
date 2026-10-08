"""Бак для воды `tank_water`. Размер — из плана ОС (160 × 190 см). Варианты (только idle):
  plastikovyy_1000_l — пластиковый еврокуб в стальной обрешётке на поддоне, кран;
  betonnyy_5000_l    — бетонная цистерна (кольца), люк, лесенка, труба;
  stalnoy_tsilindr   — стальной вертикальный цилиндр на опорах, водомерная трубка, лестница;
  podzemnyy          — подземный: из пола видна горловина с люком, труба и насосная колонка (ниже — отклонение).
Запуск: python3 models/container/tank_water.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("tank_water"))


def plastikovyy_1000_l():
    p = []
    D = 1.0
    PH = 0.15
    for k in range(5):                                                                 # поддон
        p.append(L.box((W, 0.12, 0.03), (0, -D / 2 + 0.06 + k * (D - 0.12) / 4, PH - 0.03), "wood", bevel=0.005))
    for x in (-W / 2 + 0.08, 0, W / 2 - 0.08):
        p.append(L.box((0.12, D, PH - 0.03), (x, 0, 0), "wood_dark", bevel=0.008))
    p.append(L.box((W - 0.08, D - 0.08, H - PH - 0.06), (0, 0, PH), "plastic_white", bevel=0.05))     # ёмкость
    # обрешётка: трубы по краям + сетка спереди
    g = "steel"
    for x in (-W / 2 + 0.02, W / 2 - 0.02):
        p.append(L.tube((x, -D / 2, PH), (x, -D / 2, H - 0.08), 0.02, g, verts=6))
    for z in (PH + 0.02, H - 0.08):
        p.append(L.tube((-W / 2 + 0.02, -D / 2, z), (W / 2 - 0.02, -D / 2, z), 0.02, g, verts=6))
    for k in range(1, 6):
        x = -W / 2 + 0.02 + k * (W - 0.04) / 6
        p.append(L.tube((x, -D / 2 - 0.01, PH + 0.02), (x, -D / 2 - 0.01, H - 0.08), 0.008, g, verts=4))
    for k in range(1, 5):
        z = PH + 0.02 + k * (H - PH - 0.10) / 5
        p.append(L.tube((-W / 2 + 0.02, -D / 2 - 0.012, z), (W / 2 - 0.02, -D / 2 - 0.012, z), 0.008, g, verts=4))
    p.append(L.cyl(0.10, 0.06, (0, 0, H - 0.06), "offwhite", verts=10))                                # крышка
    p.append(L.cyl(0.03, 0.10, (0, -D / 2 - 0.05, PH + 0.06), "soot", verts=8, rot=(90, 0, 0)))       # кран
    p.append(L.box((0.10, 0.03, 0.03), (0, -D / 2 - 0.12, PH + 0.08), "paint_red", bevel=0.006))
    p.append(L.box((0.30, 0.004, 0.20), (0.40, -D / 2 + 0.035, PH + 0.90), "offwhite", bevel=0))      # наклейка
    for i, (x, z) in enumerate(((-0.5, PH + 0.3), (0.3, PH + 0.15), (-0.2, H - 0.3))):
        p.append(L.spot((x, -D / 2 + 0.036, z), 0.18, "khaki_light", seed=520 + i, stretch=(1.4, 0.8)))   # водоросли/грязь
    return p


def betonnyy_5000_l():
    p = []
    R = W / 2 - 0.08                                       # + плита и труба сбоку — всего ~160
    for k in range(3):                                                                 # бетонные кольца
        p.append(L.cyl(R, (H - 0.25) / 3 - 0.01, (0, 0, k * (H - 0.25) / 3), "concrete", verts=14))
        p.append(L.cyl(R + 0.01, 0.025, (0, 0, (k + 1) * (H - 0.25) / 3 - 0.02), "concrete_dark", verts=14))
    p.append(L.cyl(R + 0.02, 0.10, (0, 0, H - 0.25), "concrete_dark", verts=14))                       # плита
    p.append(L.cyl(0.30, 0.12, (0.2, 0.1, H - 0.15), "concrete", verts=10))                            # горловина
    p.append(L.cyl(0.32, 0.03, (0.2, 0.1, H - 0.03), "steel_dark", verts=10))                          # люк
    p.append(L.tube((-R - 0.05, -0.2, 0.3), (-R - 0.05, -0.2, H - 0.3), 0.04, "steel", verts=8))     # труба
    p.append(L.tube((-R - 0.05, -0.2, 0.3), (-R + 0.05, -0.2, 0.3), 0.04, "steel", verts=8))
    for k in range(6):                                                                 # скобы-ступени
        p.append(L.box((0.25, 0.04, 0.025), (0.35, -R * 0.95 - 0.02, 0.2 + k * 0.25), "rust", bevel=0.005))
    for i, (x, z, s, c) in enumerate(((-0.3, 0.6, 0.35, "concrete_dark"), (0.2, 1.1, 0.25, "plant_dark"),
                                      (-0.1, 0.2, 0.3, "dirt"))):
        p.append(L.spot((x, -R * 0.96, z), s, c, seed=530 + i, stretch=(1.2, 0.8)))
    return p


def stalnoy_tsilindr():
    p = []
    R = 0.62
    LG = 0.35
    for x, y in ((-0.40, -0.30), (0.40, -0.30), (0, 0.45)):
        p.append(L.box((0.08, 0.08, LG + 0.05), (x, y, 0), "steel_dark", bevel=0.008))
    p.append(L.cyl(R, H - LG - 0.15, (0, 0, LG), "steel", verts=14))
    p.append(L.cyl(R, 0.15, (0, 0, H - 0.15), "steel", verts=14, radius_top=0.12))                    # купол
    for z in (LG + 0.25, LG + 0.75, H - 0.25):
        p.append(L.cyl(R + 0.012, 0.025, (0, 0, z), "steel_dark", verts=14))
    p.append(L.tube((0.25, -R - 0.03, LG + 0.1), (0.25, -R - 0.03, H - 0.25), 0.015, "glass", verts=6))  # водомер
    p.append(L.tube((0.25, -R - 0.03, LG + 0.1), (0.25, -R - 0.03, LG + 0.7), 0.016, "paint_blue", verts=6))
    for side in (-1, 1):
        p.append(L.tube((-R - 0.06 + side * 0.12, -0.05, 0), (-R - 0.06 + side * 0.12, -0.05, H - 0.2), 0.015, "steel_dark", verts=6))
    for k in range(7):
        p.append(L.tube((-R - 0.18, -0.05, 0.25 + k * 0.22), (-R + 0.06, -0.05, 0.25 + k * 0.22), 0.012, "steel_dark", verts=6))
    p.append(L.cyl(0.03, 0.12, (0.3, -0.2, LG - 0.02), "steel_dark", verts=8, rot=(90, 0, 0)))        # кран снизу
    p.append(L.box((0.10, 0.03, 0.03), (0.3, -0.36, LG + 0.0), "paint_red", bevel=0.006))
    for i, (x, z) in enumerate(((-0.25, LG + 0.15), (0.1, LG + 0.55), (0.35, H - 0.4))):
        p.append(L.spot((x, -R * 0.97, z), 0.14, "rust", seed=540 + i, stretch=(0.6, 1.6)))
    return p


def podzemnyy():
    """Подземный бак: над полом — горловина с люком, вентиляционная труба и ручная колонка (отклонение по высоте)."""
    p = [L.box((W, 1.0, 0.10), (0, 0, 0), "concrete_dark", bevel=0.02)]                                # плита-крышка
    p.append(L.cyl(0.35, 0.18, (-0.2, 0, 0.10), "concrete", verts=12))                                  # горловина
    p.append(L.cyl(0.37, 0.04, (-0.2, 0, 0.28), "steel_dark", verts=12))                                # люк
    p.append(L.box((0.50, 0.004, 0.012), (-0.2, -0.36, 0.30), "soot", bevel=0))                        # ручка люка
    p.append(L.tube((0.55, 0.1, 0.10), (0.55, 0.1, 0.95), 0.04, "steel", verts=8))                    # вент. труба
    p.append(L.tube((0.55, 0.1, 0.95), (0.65, 0.1, 1.05), 0.04, "steel", verts=8))
    p.append(L.cyl(0.07, 0.6, (0.25, -0.1, 0.10), "army_green", verts=8))                               # колонка
    p.append(L.tube((0.25, -0.1, 0.65), (0.45, -0.1, 0.85), 0.015, "steel_dark", verts=6))            # рычаг
    p.append(L.tube((0.25, -0.17, 0.55), (0.25, -0.30, 0.50), 0.02, "steel_dark", verts=6))           # носик
    for i, (x, s, c) in enumerate(((-0.6, 0.30, "dirt"), (0.5, 0.25, "concrete"))):
        p.append(L.spot((x, -0.5, 0.06), s, c, seed=550 + i, stretch=(1.3, 0.5)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz, lim in (("plastikovyy_1000_l", plastikovyy_1000_l, (W * 100, H * 100), "large"),
                             ("betonnyy_5000_l", betonnyy_5000_l, (W * 100, H * 100), "large"),
                             ("stalnoy_tsilindr", stalnoy_tsilindr, None, "large"),
                             ("podzemnyy", podzemnyy, None, "large")):
        L.make(fn, "container", "tank_water", var, size_cm=sz, limit=lim, broken="tilt")
    L.save_blend("container", "tank_water")
