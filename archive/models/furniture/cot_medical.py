"""Медицинская койка `cot_medical`. Размер — из плана ОС (190 × 80 см). Без человека (занята — состояние игры).
Варианты (только idle): skladnaya — раскладушка: брезент на трубчатой раме, ножки-«ножницы»;
  bolnichnaya — больничная кровать: металлические спинки, колёсики, матрас с простынёй, подъём изголовья;
  polevaya — армейские носилки-койка на козлах. Запуск: python3 models/furniture/cot_medical.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("cot_medical"))
D = 0.75


def skladnaya():
    p = []
    zt = 0.42
    for sy in (-1, 1):                                                                           # продольные трубы
        p.append(L.tube((-W / 2 + 0.01, sy * D / 2 * 0.85, zt), (W / 2 - 0.01, sy * D / 2 * 0.85, zt), 0.014, "steel", verts=6))
    for x in (-W / 2 + 0.01, W / 2 - 0.01):
        p.append(L.tube((x, -D / 2 * 0.85, zt), (x, D / 2 * 0.85, zt), 0.014, "steel", verts=6))
    p.append(L.sheet(8, 3, W - 0.06, D * 0.82, (0, 0, zt + 0.005), "khaki",
                     z_fn=lambda u, v: -0.025 * (1 - (2 * v - 1) ** 2) * (1 - (2 * u - 1) ** 4), jitter=0.004, seed=11))
    for x in (-0.65, 0.0, 0.65):                                                                 # ножки-ножницы
        for sy in (-1, 1):
            y = sy * D / 2 * 0.85
            p.append(L.tube((x - 0.12, y, 0.0), (x + 0.12, y, zt), 0.011, "steel_dark", verts=5))
            p.append(L.tube((x + 0.12, y, 0.0), (x - 0.12, y, zt), 0.011, "steel_dark", verts=5))
    for i, (x, s, c) in enumerate(((-0.4, 0.12, "dirt"), (0.5, 0.10, "olive_dark"))):
        p.append(L.spot((x, -0.05, zt + 0.006), s, c, facing="top", seed=950 + i, stretch=(1.6, 0.7)))
    return p


def bolnichnaya():
    p = []
    zm = 0.50
    p.append(L.box((W - 0.12, D - 0.06, 0.05), (0, 0, zm - 0.08), "steel", bevel=0.008))             # рама
    p.append(L.soft((W - 0.16, D - 0.10, 0.12), (0, 0, zm - 0.04), "cloth_blue"))                   # матрас
    p += L.blanket(0.12, W - 0.50, D - 0.04, zm + 0.08, "offwhite", seed=12, hang=(0.06, 0.10), fold_color="plastic_white")
    p.append(L.soft((0.40, 0.55, 0.10), (-W / 2 + 0.33, 0.0, zm + 0.08), "plastic_white"))           # подушка
    for sx in (-1, 1):                                                                              # спинки
        x = sx * (W / 2 - 0.04)
        hb = H if sx < 0 else 0.70
        for sy in (-1, 1):
            p.append(L.cyl(0.018, hb - 0.10, (x, sy * (D / 2 - 0.04), 0.10), "steel_light", verts=6))
        p.append(L.tube((x, -(D / 2 - 0.04), hb), (x, D / 2 - 0.04, hb), 0.018, "steel_light", verts=6))
        p.append(L.box((0.03, D - 0.12, hb - zm - 0.06), (x, 0, zm + 0.0), "plastic_white", bevel=0.006))
        for sy in (-1, 1):                                                                          # колёсики
            p.append(L.cyl(0.04, 0.025, (x, sy * (D / 2 - 0.04), 0.04), "soot", verts=8, rot=(90, 0, 0)))
            p.append(L.cyl(0.014, 0.06, (x, sy * (D / 2 - 0.04), 0.06), "steel_dark", verts=6))
    # боковой поручень у изголовья (откидной) и нижняя рама
    y = -D / 2 + 0.01
    for z in (zm + 0.14, zm + 0.26):
        p.append(L.tube((-W / 2 + 0.12, y, z), (-0.10, y, z), 0.012, "steel_light", verts=6))
    for x in (-W / 2 + 0.12, -0.45, -0.10):
        p.append(L.tube((x, y, zm - 0.03), (x, y, zm + 0.26), 0.012, "steel_light", verts=6))
    p.append(L.tube((-W / 2 + 0.04, y + 0.02, 0.18), (W / 2 - 0.04, y + 0.02, 0.18), 0.014, "steel", verts=6))
    p.append(L.box((0.10, 0.03, 0.03), (W / 2 - 0.10, y - 0.01, zm - 0.10), "steel_dark", bevel=0.006))   # рукоятка подъёма
    p.append(L.spot((0.6, -D / 2 + 0.03, zm), 0.05, "rust", seed=955))
    return p


def polevaya():
    p = []
    zt = 0.45
    for sy in (-1, 1):                                                                             # жерди носилок
        p.append(L.tube((-W / 2, sy * 0.28, zt), (W / 2, sy * 0.28, zt), 0.02, "wood", verts=6))
    p.append(L.sheet(8, 3, W - 0.40, 0.56, (0, 0, zt + 0.006), "army_green",
                     z_fn=lambda u, v: -0.03 * (1 - (2 * v - 1) ** 2), jitter=0.004, seed=13))
    for x in (-0.70, 0.70):                                                                         # козлы
        p.append(L.box((0.06, D - 0.05, 0.05), (x, 0, zt - 0.07), "wood_dark", bevel=0.006))
        for sy in (-1, 1):
            for dx in (-0.1, 0.1):
                p.append(L.tube((x + dx, sy * 0.30, 0.0), (x, sy * 0.28, zt - 0.05), 0.02, "wood_dark", verts=5))
    for x in (-0.3, 0.3):                                                                           # ремни
        p.append(L.box((0.05, 0.58, 0.012), (x, 0, zt - 0.005), "olive_dark", bevel=0))
    p.append(L.cyl(0.05, 0.004, (0, -0.20, zt + 0.008), "offwhite", verts=10))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("skladnaya", skladnaya), ("bolnichnaya", bolnichnaya), ("polevaya", polevaya)):
        L.make(fn, "furniture", "cot_medical", var, broken="legs")
    L.save_blend("furniture", "cot_medical")
