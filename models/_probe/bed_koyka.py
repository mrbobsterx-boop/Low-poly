"""ПРОБА КАЧЕСТВА (docs/QUALITY.md): железная койка `bed_single_zheleznaya_koyka` по образцам docs/ref/style/props_sheet_*.
Чёткая рама из квадратной трубы, белый матрас, одеяло — симуляцией ткани, свешивается вперёд; красное полотенце,
изолента на стойке, табличка. Запуск (только просмотр): python3 render/_lit_preview.py <папка> models/_probe/bed_koyka.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

L.quality()
W, H = (s / 100 for s in L.size_cm("bed_single"))   # 200 × 60
D = 0.90
T = 0.045                    # квадратная труба — толще реальной («chunky»)
FR = "steel"
MAT_Z, MAT_H = 0.27, 0.15


def koyka():
    p = []
    xs = (-(W / 2 - T / 2), W / 2 - T / 2)
    for x, h in zip(xs, (H, H - 0.06)):
        for sy in (-1, 1):
            y = sy * (D / 2 - T / 2)
            p.append(L.box((T, T, h), (x, y, 0), FR, bevel=0.006))                                # стойка
            p.append(L.box((T + 0.016, T + 0.016, 0.03), (x, y, 0), "soot", bevel=0.005))          # резиновая пятка
            p.append(L.box((T + 0.01, T + 0.01, 0.018), (x, y, h - 0.018), "steel", bevel=0.004))  # заглушка
        p.append(L.box((T, D - T, T), (x, 0, h - T - 0.01), FR, bevel=0.006))                       # верхняя перекладина
        p.append(L.box((T, D - T, T * 0.8), (x, 0, MAT_Z - 0.02), FR, bevel=0.006))                 # нижняя
        for k in range(3):                                                                           # прутья
            y = -(D / 2 - 0.22) + k * (D - 0.44) / 2
            p.append(L.box((0.026, 0.026, h - MAT_Z - T), (x, y, MAT_Z - 0.01), FR, bevel=0.004))
    for sy in (-1, 1):                                                                               # боковины рамы
        p.append(L.box((W - 2 * T, T, T * 1.1), (0, sy * (D / 2 - T / 2), MAT_Z - 0.06), FR, bevel=0.006))
    for k in range(5):                                                                               # поперечины под матрасом
        x = -W / 2 + 0.25 + k * (W - 0.5) / 4
        p.append(L.box((0.03, D - 2 * T, 0.02), (x, 0, MAT_Z - 0.04), "steel_dark", bevel=0.004))
    # матрас (белый, мягкий), шов-кант, подушка
    mw, md = W - 2 * T - 0.02, D - 2 * T
    mat = L.soft((mw, md, MAT_H), (0, 0, MAT_Z), "offwhite")
    p.append(mat)
    p.append(L.box((mw + 0.004, md + 0.004, 0.012), (0, 0, MAT_Z + MAT_H * 0.55), "cloth_beige", bevel=0.004))
    p.append(L.soft((0.42, md - 0.20, 0.11), (-(mw / 2 - 0.25), 0.03, MAT_Z + MAT_H - 0.02), "plastic_white"))
    # одеяло — ткань симуляцией: падает на матрас и свешивается вперёд и назад
    p.append(L.drape(1.15, 1.00, (0.36, -0.13, MAT_Z + MAT_H + 0.05), [mat], "army_green", name="blanket", noise=0.025, seed=4, frames=40))
    # красное полотенце, переброшенное через перекладину у изголовья
    rail = p[3 * 2 + 0]                                                   # верхняя перекладина изголовья
    p.append(L.drape(0.30, 0.20, (xs[0], -0.16, H + 0.05), [rail, mat], "paint_red", res=0.025,
                     thick=0.005, name="towel"))
    # изолента на стойке (история предмета) и табличка с номером на спинке
    x, y = xs[1], -(D / 2 - T / 2)
    p.append(L.box((T + 0.008, T + 0.008, 0.06), (x, y, 0.30), "paint_red", bevel=0.003))
    p.append(L.box((0.17, 0.008, 0.09), (xs[0] + 0.03, -0.10, H - 0.16), "steel", rot=(0, 0, 90), bevel=0.003))
    p.append(L.decal("b2", (xs[0] - 0.0 + 0.036, -0.10, H - 0.115), 0.07, facing="left"))
    # износ: ржавые пятна на раме у пола и на стыках
    for i, (x, z, s) in enumerate(((xs[0], 0.10, 0.05), (xs[1], 0.12, 0.05), (-0.4, MAT_Z - 0.03, 0.06), (0.6, MAT_Z - 0.03, 0.05))):
        p.append(L.spot((x, -(D / 2) - 0.0, z), s, "rust_dark", seed=300 + i, stretch=(0.8, 1.2)))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(koyka, "_probe", "bed_single", "zheleznaya_koyka", size_cm=(W * 100, H * 100), glb=False)
