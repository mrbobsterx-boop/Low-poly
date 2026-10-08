"""Шкафчик `locker_metal`, вариант `armeyskiy` (армейский). ОС: 50 × 180 см. Образец: docs/ref/container/locker_metal.png
Версия 2 (подробная, под референс автора): утопленные дверцы с зазором, жалюзи, ручки, замки, петли, табличка, цоколь.
Запуск: python3 models/container/locker_metal.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 0.50, 0.50, 1.80
PLINTH = 0.07                  # цоколь
BODY = "army_green"
DARK = "olive_dark"
FRONT = -D / 2                 # плоскость фасада


def louvers(p, x, z, w, n=5, step=0.032):
    """Жалюзи: рамка-углубление + наклонные планки."""
    p.append(L.box((w + 0.02, 0.006, n * step + 0.016), (x, FRONT - 0.022, z - 0.008), "soot", bevel=0.002))
    for i in range(n):
        p.append(L.box((w, 0.010, 0.016), (x, FRONT - 0.030, z + i * step), DARK, rot=(-35, 0, 0), bevel=0.002))


def door(p, x0, x1, hinge_left):
    """Дверца от x0 до x1: панель, выпуклая филёнка, жалюзи сверху и снизу, ручка, замок, петли."""
    w = x1 - x0
    cx = (x0 + x1) / 2
    z0, z1 = PLINTH + 0.03, H - 0.05
    p.append(L.box((w - 0.012, 0.018, z1 - z0), (cx, FRONT - 0.009, z0), BODY, bevel=0.008))
    # филёнка (чуть выпуклая середина двери)
    p.append(L.box((w - 0.07, 0.008, 0.80), (cx, FRONT - 0.020, PLINTH + 0.42), BODY, bevel=0.006))
    louvers(p, cx, H - 0.30, w - 0.09)
    louvers(p, cx, PLINTH + 0.12, w - 0.09)
    # ручка: вертикальная скоба на двух стойках + замок
    hx = x1 - 0.035 if hinge_left else x0 + 0.035
    for dz in (0.0, 0.13):
        p.append(L.box((0.012, 0.025, 0.012), (hx, FRONT - 0.03, PLINTH + 0.86 + dz), "steel_dark", bevel=0.003))
    p.append(L.box((0.016, 0.014, 0.16), (hx, FRONT - 0.045, PLINTH + 0.845), "steel_light", bevel=0.005))
    p.append(L.cyl(0.013, 0.012, (hx, FRONT - 0.018, PLINTH + 1.06), "steel", verts=8, rot=(90, 0, 0)))
    p.append(L.box((0.004, 0.006, 0.012), (hx, FRONT - 0.031, PLINTH + 1.054), "soot", bevel=0))
    # петли на внешней кромке
    ex = x0 + 0.004 if hinge_left else x1 - 0.004
    for z in (PLINTH + 0.18, H - 0.22):
        p.append(L.cyl(0.009, 0.07, (ex, FRONT - 0.012, z), "steel_dark", verts=6))


def locker_idle():
    p = []
    # корпус: стенки, крыша с козырьком, цоколь на ножках
    p.append(L.box((W, D, H - PLINTH), (0, 0, PLINTH), BODY, bevel=0.012))
    p.append(L.box((W + 0.016, D + 0.016, 0.03), (0, 0, H - 0.03), DARK, bevel=0.01))
    p.append(L.box((W - 0.02, D - 0.04, PLINTH - 0.02), (0, 0.01, 0.02), "soot", bevel=0.006))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.box((0.045, 0.045, PLINTH), (sx * (W / 2 - 0.03), sy * (D / 2 - 0.03), 0), "steel_dark", bevel=0.008))
    # рамка проёма (тёмный зазор вокруг дверей)
    p.append(L.box((W - 0.024, 0.004, H - PLINTH - 0.06), (0, FRONT - 0.001, PLINTH + 0.025), "soot", bevel=0))
    door(p, -W / 2 + 0.014, -0.004, hinge_left=True)
    door(p, 0.004, W / 2 - 0.014, hinge_left=False)
    # табличка с номером (рамка + светлая вставка + «цифры») на левой двери
    p.append(L.box((0.11, 0.006, 0.06), (-0.12, FRONT - 0.026, H - 0.52), "steel_dark", bevel=0.003))
    p.append(L.box((0.095, 0.006, 0.045), (-0.12, FRONT - 0.030, H - 0.5125), "offwhite", bevel=0.002))
    for i in range(3):
        p.append(L.box((0.012, 0.004, 0.025), (-0.145 + i * 0.022, FRONT - 0.034, H - 0.503), "soot", bevel=0))
    # трафаретная звезда на правой двери (две плашки крест-накрест)
    p.append(L.poly([(0.0, 0.045), (0.012, 0.014), (0.043, 0.014), (0.018, -0.005), (0.027, -0.038), (0.0, -0.018),
                     (-0.027, -0.038), (-0.018, -0.005), (-0.043, 0.014), (-0.012, 0.014)], 0.003,
                    (0.12, FRONT - 0.030, H - 0.56), "offwhite"))
    # износ (формой и пятнами палитры): сколы до металла по кромкам дверей, ржавчина внизу, потёртость у ручек
    yf = FRONT - 0.021
    for i, (x, z, s, c) in enumerate(((-0.215, 1.48, 0.035, "steel"), (0.012, 1.10, 0.03, "steel"),
                                      (0.215, 0.55, 0.03, "steel"), (-0.012, 0.30, 0.025, "steel_dark"),
                                      (-0.13, 0.95, 0.07, "khaki"), (0.11, 0.98, 0.06, "khaki"),
                                      (0.18, 1.72, 0.04, "khaki_light"))):
        p.append(L.spot((x, yf, z), s, c, seed=i + 3))
    for i, (x, w) in enumerate(((-0.17, 0.10), (0.05, 0.14), (0.20, 0.07))):          # ржавчина у пола
        p.append(L.spot((x, yf - 0.002, PLINTH + 0.07), w, "rust", seed=20 + i, stretch=(1.0, 0.6)))
        p.append(L.spot((x + 0.01, yf - 0.004, PLINTH + 0.05), w * 0.5, "rust_dark", seed=30 + i, stretch=(1.0, 0.5)))
    p.append(L.spot((0.13, yf - 0.002, H - 0.28), 0.05, "rust_light", seed=41, stretch=(0.5, 1.6)))   # потёк
    # вмятина на правой дверце — тёмный «залом»
    p.append(L.box((0.10, 0.004, 0.012), (0.13, yf, 0.72), DARK, rot=(0, 18, 0), bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(locker_idle(), "container", "locker_metal", "armeyskiy", "idle", size_cm=(50, 180))
    L.save_blend("container", "locker_metal")
