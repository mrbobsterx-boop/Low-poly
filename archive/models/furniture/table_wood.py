"""Стол `table_wood`. Размер — из плана ОС (120 × 75 см). Варианты (только idle):
  obedennyy      — обеденный: столешница из досок со щелями, сужающиеся ножки, царга, уголки, гвозди;
  pismennyy      — письменный: тумба с ящиками (скрипт table_wood_pismennyy.py);
  skladnoy       — складной: лёгкая столешница с алюминиевой кромкой, ножки-«ножницы»;
  metallicheskiy — металлический: стальная столешница с завальцованной кромкой, ножки-уголки, полка внизу;
  kuhonnyy_stol  — кухонный: клеёнка в клетку, ящик в царге, точёные ножки.
Предметы на столе — отдельные объекты (ставит игра). Запуск: python3 models/furniture/table_wood.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("table_wood"))
D = 0.70
TOP = 0.045
LEG = 0.065


def leg(p, x, y):
    """Ножка: чуть сужается книзу (четырёхгранный усечённый конус) + тёмный «башмак»."""
    p.append(L.cyl(LEG * 0.62, H - TOP - 0.03, (x, y, 0.03), "wood_dark", verts=4, radius_top=LEG * 0.74))
    p.append(L.cyl(LEG * 0.66, 0.03, (x, y, 0), "stone_dark", verts=4))


def table_idle():
    p = []
    # столешница: 4 доски вдоль, щели между ними, разные оттенки
    n, gap = 4, 0.006
    bd = (D - gap * (n - 1)) / n
    for i, col in enumerate(["wood", "wood_light", "wood", "wood_light"]):
        y = -D / 2 + bd / 2 + i * (bd + gap)
        p.append(L.box((W, bd, TOP), (0, y, H - TOP), col, bevel=0.008))
    p.append(L.box((W - 0.02, D - 0.02, 0.01), (0, 0, H - TOP - 0.004), "soot", bevel=0))      # тень щелей
    # гвозди по краям досок (тёмные точки сверху)
    for i in range(n):
        y = -D / 2 + bd / 2 + i * (bd + gap)
        for x in (-W / 2 + 0.06, W / 2 - 0.06):
            p.append(L.box((0.012, 0.012, 0.003), (x, y, H), "steel_dark", bevel=0))
    # царга: доски под столешницей по периметру
    for sy in (-1, 1):
        p.append(L.box((W - 0.16, 0.025, 0.10), (0, sy * (D / 2 - 0.07), H - TOP - 0.10), "wood_dark", bevel=0.006))
    for sx in (-1, 1):
        p.append(L.box((0.025, D - 0.16, 0.10), (sx * (W / 2 - 0.08), 0, H - TOP - 0.10), "wood_dark", bevel=0.006))
    # ножки и нижняя перекладина
    for sx in (-1, 1):
        for sy in (-1, 1):
            leg(p, sx * (W / 2 - 0.08), sy * (D / 2 - 0.08))
    for sx in (-1, 1):
        p.append(L.box((0.03, D - 0.18, 0.04), (sx * (W / 2 - 0.08), 0, 0.16), "wood", bevel=0.006))
    p.append(L.box((W - 0.18, 0.03, 0.04), (0, 0, 0.16), "wood", bevel=0.006))
    # металлические уголки на царге спереди
    for sx in (-1, 1):
        p.append(L.box((0.05, 0.006, 0.05), (sx * (W / 2 - 0.12), -(D / 2 - 0.083), H - TOP - 0.08), "steel_dark", bevel=0.002))
    return p


def skladnoy():
    p = []
    TOP = 0.03
    n = 5
    bd = (D - 0.06) / n
    for k in range(n):
        p.append(L.box((W - 0.04, bd - 0.006, TOP), (0, -(D - 0.06) / 2 + bd * (k + 0.5), H - TOP),
                       "wood_light" if k % 2 else "cloth_beige", bevel=0.004))
    for sy in (-1, 1):                                                                         # кромка-рамка
        p.append(L.box((W, 0.02, 0.045), (0, sy * (D / 2 - 0.01), H - 0.045), "steel_light", bevel=0.005))
    for sx in (-1, 1):
        p.append(L.box((0.02, D, 0.045), (sx * (W / 2 - 0.01), 0, H - 0.045), "steel_light", bevel=0.005))
    # ножки-«ножницы»: две пары крест-накрест спереди и сзади + перекладины
    zt = H - 0.05
    for sy in (-1, 1):
        y = sy * (D / 2 - 0.06)
        for sx in (-1, 1):
            p.append(L.tube((sx * (W / 2 - 0.10), y, 0.0), (-sx * (W / 2 - 0.30), y, zt), 0.014, "steel", verts=6))
            p.append(L.box((0.05, 0.03, 0.015), (sx * (W / 2 - 0.10), y, 0.0), "soot", bevel=0.004))
        p.append(L.cyl(0.02, 0.03, (0.0 + 0.0, y - 0.015, zt * 0.5 - 0.0), "steel_dark", verts=8, rot=(90, 0, 0)))
    for sx in (-1, 1):
        p.append(L.tube((sx * (W / 2 - 0.10), -(D / 2 - 0.06), 0.02), (sx * (W / 2 - 0.10), D / 2 - 0.06, 0.02), 0.012,
                        "steel", verts=6))
    for i, (x, s) in enumerate(((-0.3, 0.12), (0.25, 0.10), (0.05, 0.07))):
        p.append(L.spot((x, -0.05 + i * 0.1, H), s, "wood", facing="top", seed=230 + i, stretch=(1.6, 0.6)))
    return p


def metallicheskiy():
    p = []
    TOP = 0.03
    p.append(L.box((W, D, TOP), (0, 0, H - TOP), "steel", bevel=0.006))
    p.append(L.box((W + 0.01, 0.025, 0.06), (0, -(D / 2), H - 0.06), "steel_light", bevel=0.008))     # кромка
    p.append(L.box((W - 0.08, D - 0.08, 0.05), (0, 0, H - TOP - 0.05), "steel_dark", bevel=0.004))     # рама
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (W / 2 - 0.05), sy * (D / 2 - 0.05)
            p.append(L.box((0.05, 0.05, H - TOP), (x, y, 0), "steel_dark", bevel=0.006))
            p.append(L.box((0.07, 0.07, 0.015), (x, y, 0), "soot", bevel=0.004))
    p.append(L.box((W - 0.12, D - 0.12, 0.02), (0, 0, 0.18), "steel", bevel=0.004))                    # полка
    for sx in (-1, 1):
        for x in (sx * (W / 2 - 0.05),):
            for z in (H - 0.05, 0.20):
                p.append(L.cyl(0.008, 0.01, (x, -(D / 2) - 0.002, z), "steel_light", verts=6, rot=(90, 0, 0)))
    for i, (x, y, s, c) in enumerate(((-0.35, -0.1, 0.20, "steel_light"), (0.2, 0.12, 0.16, "steel_dark"),
                                      (0.45, -0.2, 0.10, "rust"), (-0.05, 0.0, 0.06, "rust_dark"))):
        p.append(L.spot((x, y, H), s, c, facing="top", seed=240 + i, stretch=(1.8, 0.4)))
    p.append(L.spot((0.5, -(D / 2) - 0.014, H - 0.04), 0.05, "rust", seed=245, stretch=(1.3, 0.6)))
    return p


def kuhonnyy_stol():
    p = []
    TOP = 0.04
    W = globals()["W"] - 0.02                        # клеёнка свисает на 1 см с каждой стороны — всего 120
    p.append(L.box((W, D, TOP), (0, 0, H - TOP - 0.006), "wood", bevel=0.008))
    # клеёнка в клетку: светлая, свисает спереди; клетки — красные квадраты
    p.append(L.box((W + 0.02, D + 0.02, 0.006), (0, 0, H), "offwhite", bevel=0.002))
    p.append(L.box((W + 0.02, 0.006, 0.12), (0, -(D / 2) - 0.012, H - 0.114), "offwhite", bevel=0.002))
    for i in range(12):
        for j in range(2):
            if (i + j) % 2 == 0:
                p.append(L.box((0.05, 0.004, 0.05), (-W / 2 + 0.05 + i * 0.1, -(D / 2) - 0.016, H - 0.10 + j * 0.06),
                               "paint_red", bevel=0))
    for i in range(12):
        for j in range(7):
            if (i + j) % 2 == 0:
                p.append(L.box((0.05, 0.05, 0.003), (-W / 2 + 0.05 + i * 0.1, -D / 2 + 0.05 + j * 0.1, H + 0.006),
                               "paint_red", bevel=0))
    # царга с ящиком и ручкой
    p.append(L.box((W - 0.12, 0.025, 0.10), (0, -(D / 2 - 0.06), H - TOP - 0.10), "wood_dark", bevel=0.006))
    p.append(L.box((0.40, 0.02, 0.07), (0.15, -(D / 2 - 0.06) - 0.015, H - TOP - 0.087), "wood_light", bevel=0.005))
    p.append(L.cyl(0.015, 0.02, (0.15, -(D / 2 - 0.06) - 0.035, H - TOP - 0.05), "wood_dark", verts=8, rot=(90, 0, 0)))
    # точёные ножки: цилиндры с утолщениями
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (W / 2 - 0.08), sy * (D / 2 - 0.08)
            p.append(L.cyl(0.026, H - TOP - 0.10, (x, y, 0), "wood_dark", verts=8, radius_top=0.032))
            for z in (0.12, 0.42):
                p.append(L.cyl(0.038, 0.04, (x, y, z), "wood", verts=8))
            p.append(L.box((0.07, 0.07, 0.10), (x, y, H - TOP - 0.10), "wood_dark", bevel=0.006))
    p.append(L.spot((-0.3, -0.1, H + 0.009), 0.10, "cloth_beige", facing="top", seed=250))           # пятно на клеёнке
    return p


if __name__ == "__main__":
    import table_wood_pismennyy as tp
    L.new_scene()
    for var, fn in (("obedennyy", table_idle), ("pismennyy", tp.desk_idle), ("skladnoy", skladnoy),
                    ("metallicheskiy", metallicheskiy), ("kuhonnyy_stol", kuhonnyy_stol)):
        L.make(fn, "furniture", "table_wood", var, size_cm=(W * 100, H * 100), broken="legs")
    L.save_blend("furniture", "table_wood")
