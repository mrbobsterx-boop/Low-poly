"""Стул `chair_wood`, вариант `derevyannyy` (деревянный). ОС: 45 × 90 см. Образец: docs/ref/furniture/chair_wood.png
Версия 2 (подробная): сиденье из двух досок со щелью, гнутая (из 3 частей) верхняя перекладина, 3 планки спинки,
ножки с наклоном, царги, перекладины, гвозди.
Запуск: python3 models/furniture/chair_wood.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("chair_wood"))
D = 0.45
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


def myagkiy_stul():
    """Мягкий стул: металлические трубчатые ножки, мягкое сиденье и спинка (дерматин), как в старой столовой."""
    p = []
    R = 0.012
    for sx in (-1, 1):
        x = sx * (W / 2 - 0.05)
        p.append(L.tube((x, -(D / 2 - 0.05), 0), (x, -(D / 2 - 0.06), SEAT - 0.06), R, "steel", verts=6))
        p.append(L.tube((x, D / 2 - 0.05, 0), (x, D / 2 - 0.08, H - 0.05), R, "steel", verts=6))
        p.append(L.tube((x, -(D / 2 - 0.06), SEAT - 0.06), (x, D / 2 - 0.07, SEAT - 0.06), R, "steel", verts=6))
        p.append(L.cyl(0.016, 0.015, (x, -(D / 2 - 0.05), 0), "soot", verts=6))
        p.append(L.cyl(0.016, 0.015, (x, D / 2 - 0.05, 0), "soot", verts=6))
    p.append(L.tube((-(W / 2 - 0.05), D / 2 - 0.06, 0.15), (W / 2 - 0.05, D / 2 - 0.06, 0.15), R * 0.8, "steel", verts=6))
    p.append(L.soft((W - 0.02, D - 0.02, 0.07), (0, 0, SEAT - 0.06), "cloth_red"))
    p.append(L.soft((W - 0.06, 0.06, 0.30), (0, D / 2 - 0.08, SEAT + 0.12), "cloth_red", rot=(-6, 0, 0)))
    p.append(L.spot((-0.10, -(D / 2) + 0.006, SEAT - 0.03), 0.09, "khaki_light", seed=260, stretch=(1.4, 0.6)))  # протёрто
    p.append(L.spot((0.08, D / 2 - 0.12, SEAT + 0.30), 0.10, "cloth_beige", seed=261, stretch=(0.8, 1.2)))      # порвано
    p.append(L.spot((0.08, D / 2 - 0.13, SEAT + 0.30), 0.05, "khaki_light", seed=262))
    return p


def kreslo():
    """Кресло: мягкое, широкие подлокотники, короткие ножки; потёртая обивка (заплатка).
    Шире стула по природе — 80 см (отклонение от размера ОС 45 см, отмечено автору)."""
    W = 0.80
    p = []
    body, dark = "army_green", "olive_dark"
    p.append(L.soft((W, D + 0.25, 0.26), (0, 0.10, 0.10), body))                                   # основание
    p.append(L.soft((W - 0.18, D + 0.05, 0.12), (0, 0.02, 0.34), body))                            # подушка сиденья
    for sx in (-1, 1):
        p.append(L.soft((0.12, D + 0.22, 0.32), (sx * (W / 2 - 0.06), 0.10, 0.30), body))          # подлокотники
    p.append(L.soft((W - 0.04, 0.16, H - 0.30), (0, D / 2 + 0.12, 0.30), body, rot=(-8, 0, 0)))    # спинка
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.cyl(0.02, 0.10, (sx * (W / 2 - 0.05), 0.10 + sy * (D / 2), 0), "wood_dark", verts=6))
    p.append(L.box((W - 0.2, 0.01, 0.03), (0, -0.03, 0.32), dark, bevel=0))                        # шов
    p.append(L.box((0.10, 0.006, 0.08), (0.12, -0.03, 0.18), "khaki", rot=(0, 8, 0), bevel=0))     # заплатка
    for k in range(4):
        p.append(L.box((0.006, 0.004, 0.02), (0.08 + k * 0.026, -0.034, 0.255), "soot", bevel=0))  # стежки
    p.append(L.spot((-0.15, -0.032, 0.22), 0.08, "khaki_light", seed=265, stretch=(1.3, 0.8)))
    p.append(L.spot((W / 2 - 0.06, 0.10 - (D + 0.22) / 2 - 0.004, 0.45), 0.06, "khaki_light", seed=266))
    return p


def taburet():
    """Табурет: круглое сиденье из досок, четыре разведённые ножки, перекладины. Ниже стула (табурет по природе)."""
    p = []
    HS = 0.48
    p.append(L.cyl(0.19, 0.04, (0, 0, HS - 0.04), "wood_light", verts=10))
    p.append(L.box((0.36, 0.006, 0.042), (0, 0.0, HS - 0.041), "wood_dark", bevel=0))                 # шов досок
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.tube((sx * 0.17, sy * 0.15, 0), (sx * 0.10, sy * 0.09, HS - 0.04), 0.022, "wood", verts=4))
    for z, r in ((0.16, 0.14), (0.16, 0.14)):
        p.append(L.tube((-r, -0.12, z), (r, -0.12, z), 0.014, "wood_dark", verts=4))
        p.append(L.tube((-r, 0.12, z), (r, 0.12, z), 0.014, "wood_dark", verts=4))
    p.append(L.spot((0.05, 0.0, HS), 0.12, "wood", facing="top", seed=270, stretch=(1.5, 0.7)))
    return p


def barnyy_stul():
    """Барный стул: высокий, круглое сиденье, металлические ножки, кольцо-подножка, низкая спинка."""
    p = []
    HS = 0.72
    p.append(L.cyl(0.19, 0.06, (0, 0, HS - 0.06), "cloth_red", verts=10))
    p.append(L.cyl(0.20, 0.015, (0, 0, HS - 0.075), "steel_dark", verts=10))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.tube((sx * 0.19, sy * 0.17, 0), (sx * 0.12, sy * 0.11, HS - 0.07), 0.013, "steel", verts=6))
            p.append(L.cyl(0.02, 0.015, (sx * 0.19, sy * 0.17, 0), "soot", verts=6))
    pts = [(0.17, 0.0), (0.0, 0.15), (-0.17, 0.0), (0.0, -0.15)]
    for k in range(4):
        a, b = pts[k], pts[(k + 1) % 4]
        p.append(L.tube((a[0], a[1], 0.28), (b[0], b[1], 0.28), 0.011, "steel_light", verts=6))
    for sx in (-1, 1):
        p.append(L.tube((sx * 0.12, 0.12, HS - 0.03), (sx * 0.14, 0.16, H - 0.04), 0.012, "steel", verts=6))
    p.append(L.soft((0.30, 0.05, 0.12), (0, 0.16, H - 0.14), "cloth_red", rot=(-10, 0, 0)))
    p.append(L.spot((0.06, -0.10, HS), 0.10, "cloth_beige", facing="top", seed=275))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz in (("derevyannyy", chair_idle, (W * 100, H * 100)), ("myagkiy_stul", myagkiy_stul, (W * 100, H * 100)),
                        ("kreslo", kreslo, None), ("taburet", taburet, None),
                        ("barnyy_stul", barnyy_stul, (W * 100, H * 100))):
        L.make(fn, "furniture", "chair_wood", var, size_cm=sz, broken="legs")
    L.save_blend("furniture", "chair_wood")
