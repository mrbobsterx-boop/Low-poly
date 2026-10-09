"""ПРОБА КАЧЕСТВА (docs/QUALITY.md): письменный стол `table_wood_pismennyy` по образцам docs/ref/style/props_sheet_1, room_workshop.
Столешница из толстых досок с гвоздями, слева — ножки с перекладиной, справа — тумба с тремя КРАСНЫМИ ящиками
(акцентный цвет), крупные металлические ручки, записка, заплатка-доска другого цвета.
Запуск (только просмотр): python3 render/_lit_preview.py <папка> models/_probe/desk.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

L.quality()
W, H = (s / 100 for s in L.size_cm("table_wood"))   # 120 × 75
D = 0.65
TOP = 0.055
LEG = 0.075                  # ножки толще реальных («chunky»)
PW = 0.44                    # тумба


def desk():
    p = []
    # столешница: 4 толстые доски вдоль, щели, одна доска — другого оттенка (заменённая)
    n, gap = 4, 0.008
    bd = (D - gap * (n - 1)) / n
    for i, col in enumerate(["wood_light", "wood_light", "wood", "wood_light"]):
        y = -D / 2 + bd / 2 + i * (bd + gap)
        p.append(L.box((W, bd, TOP), (0, y, H - TOP), col, bevel=0.008))
    p.append(L.box((W - 0.02, D - 0.02, 0.012), (0, 0, H - TOP - 0.002), "wood_dark", bevel=0))      # тёмные щели
    for i in range(n):                                                                               # гвозди — крупные
        y = -D / 2 + bd / 2 + i * (bd + gap)
        for x in (-W / 2 + 0.05, -0.05, W / 2 - 0.05):
            p.append(L.cyl(0.008, 0.004, (x, y, H), "steel_dark", verts=6))
    # слева: две пары ножек, царга, перекладина
    xl = -W / 2 + 0.06
    for sy in (-1, 1):
        p.append(L.box((LEG, LEG, H - TOP), (xl, sy * (D / 2 - 0.06), 0), "wood", bevel=0.008))
    p.append(L.box((LEG * 0.7, D - 0.12, 0.06), (xl, 0, 0.14), "wood_dark", bevel=0.006))            # перекладина
    p.append(L.box((W - PW - 0.08, 0.03, 0.09), (-PW / 2 + 0.01, -(D / 2 - 0.05), H - TOP - 0.09), "wood", bevel=0.006))  # царга
    p.append(L.box((W - PW - 0.08, 0.03, 0.09), (-PW / 2 + 0.01, D / 2 - 0.05, H - TOP - 0.09), "wood", bevel=0.006))
    # справа: тумба — деревянный корпус, три красных ящика, ручки-скобы, цоколь
    xp = W / 2 - PW / 2 - 0.02
    p.append(L.box((PW, D - 0.06, H - TOP - 0.05), (xp, 0.0, 0.05), "wood", bevel=0.01))
    p.append(L.box((PW - 0.04, D - 0.10, 0.05), (xp, 0.0, 0.0), "wood_dark", bevel=0.006))
    F = -(D - 0.06) / 2
    hz = (H - TOP - 0.08) / 3
    for k in range(3):
        z = 0.065 + k * hz
        p.append(L.box((PW - 0.05, 0.02, hz - 0.02), (xp, F - 0.008, z), "paint_red", bevel=0.008))
        p.append(L.box((PW - 0.11, 0.006, hz - 0.08), (xp, F - 0.020, z + 0.03), "cloth_red", bevel=0.003))   # филёнка
        hzc = z + (hz - 0.02) / 2
        for sx in (-1, 1):
            p.append(L.box((0.016, 0.03, 0.022), (xp + sx * 0.06, F - 0.03, hzc - 0.011), "steel_dark", bevel=0.004))
        p.append(L.box((0.15, 0.022, 0.024), (xp, F - 0.05, hzc - 0.012), "steel_light", bevel=0.006))        # ручка-скоба
    # износ ящиков: сколы краски до дерева
    for i, (x, z) in enumerate(((xp - 0.17, 0.32), (xp + 0.15, 0.14), (xp + 0.16, 0.50), (xp - 0.10, 0.08))):
        p.append(L.spot((x, F - 0.0205, z), 0.035, "wood", seed=500 + i))
    # бирка на верхнем ящике и записка на краю столешницы, свисает вперёд
    p.append(L.decal("label_white", (xp - 0.12, F - 0.021, 0.53), 0.08))
    p.append(L.decal("note", (-0.30, -D / 2 + 0.06, H + 0.0), 0.12, facing="top", rot=8))
    # потёртости на столешнице
    for i, (x, s) in enumerate(((-0.25, 0.14), (0.20, 0.12))):
        p.append(L.spot((x, 0.05, H + 0.0005), s, "wood", facing="top", seed=510 + i, stretch=(1.8, 0.5)))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(desk, "_probe", "table_wood", "pismennyy", size_cm=(W * 100, H * 100), glb=False)
