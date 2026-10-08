"""Кухонная тумба `kitchen_counter`. Размер — из плана ОС (120 × 90 см). Дверцы закрыты (открытое — состояние, не делаем).
Варианты (только idle):
  s_rakovinoy  — с раковиной: мойка со смесителем, две дверцы под ней;
  s_yaschikami — с ящиками: колонка ящиков + дверца, столешница со сколами;
  uglovaya     — угловая: Г-образная, столешница и дверцы на две стороны.
Предметы сверху (плита, посуда) — отдельные. Запуск: python3 models/container/kitchen_counter.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("kitchen_counter"))
D = 0.60
TOP = 0.04
F = -D / 2
PLINTH = 0.08


def carcass(p, w, x0=0.0, color="wood"):
    p.append(L.box((w - 0.02, D - 0.06, PLINTH), (x0, 0.02, 0), "soot", bevel=0.004))             # цоколь
    p.append(L.box((w, D - 0.02, H - TOP - PLINTH), (x0, 0.01, PLINTH), color, bevel=0.008))
    p.append(L.box((w + 0.02, D + 0.01, TOP), (x0, 0, H - TOP), "wood_dark", bevel=0.008))         # столешница
    p.append(L.box((w + 0.02, 0.006, 0.012), (x0, F - 0.004, H - TOP + 0.014), "steel", bevel=0))  # кромка


def door(p, x, w, h, z, color="wood_light", handle_side=1, y=F + 0.0):
    p.append(L.box((w - 0.012, 0.02, h - 0.012), (x, y - 0.006, z + 0.006), color, bevel=0.008))
    p.append(L.box((w - 0.08, 0.006, h - 0.08), (x, y - 0.018, z + 0.04), "wood", bevel=0.004))  # филёнка
    hx = x + handle_side * (w / 2 - 0.05)
    p.append(L.box((0.016, 0.02, 0.10), (hx, y - 0.03, z + h - 0.18), "steel", bevel=0.004))


def drawer(p, x, w, h, z, color="wood_light"):
    p.append(L.box((w - 0.012, 0.02, h - 0.012), (x, F - 0.006, z + 0.006), color, bevel=0.008))
    p.append(L.box((0.12, 0.02, 0.016), (x, F - 0.03, z + h / 2 - 0.008), "steel", bevel=0.004))


def s_rakovinoy():
    p = []
    carcass(p, W - 0.02)
    hb = H - TOP - PLINTH
    for k, s in ((-1, -1), (1, 1)):
        door(p, k * (W - 0.02) / 4, (W - 0.02) / 2, hb - 0.02, PLINTH, handle_side=-s)
    # мойка: чаша (тёмная впадина), бортик, смеситель
    p.append(L.box((0.50, 0.40, 0.006), (-0.15, 0.0, H), "steel_light", bevel=0.004))
    p.append(L.box((0.42, 0.32, 0.004), (-0.15, 0.0, H + 0.004), "steel_dark", bevel=0))
    p.append(L.cyl(0.02, 0.004, (-0.15, 0.03, H + 0.007), "soot", verts=8))                       # слив
    p.append(L.cyl(0.018, 0.10, (-0.15, 0.24, H), "steel", verts=8))
    p.append(L.tube((-0.15, 0.24, H + 0.10), (-0.15, 0.10, H + 0.13), 0.012, "steel", verts=6))
    p.append(L.tube((-0.15, 0.10, H + 0.13), (-0.15, 0.08, H + 0.10), 0.01, "steel", verts=6))
    for sx in (-1, 1):
        p.append(L.cyl(0.016, 0.03, (-0.15 + sx * 0.06, 0.24, H + 0.03), "paint_red" if sx < 0 else "paint_blue", verts=6))
    p.append(L.box((0.40, 0.30, 0.01), (0.30, 0.0, H), "wood_light", bevel=0.004))              # доска для сушки
    for i, (x, z, s, c) in enumerate(((-0.4, 0.3, 0.06, "dirt"), (0.35, 0.55, 0.05, "wood_dark"), (0.1, 0.15, 0.05, "rust"))):
        p.append(L.spot((x, F - 0.025, z), s, c, seed=840 + i))
    return p


def s_yaschikami():
    p = []
    carcass(p, W - 0.02)
    hb = H - TOP - PLINTH
    for k in range(4):                                                                            # колонка ящиков слева
        drawer(p, -0.30, 0.58, hb / 4, PLINTH + k * hb / 4)
    door(p, 0.29, 0.58, hb - 0.02, PLINTH, handle_side=-1)
    for i, (x, s, c) in enumerate(((-0.4, 0.08, "wood"), (0.2, 0.10, "soot"), (0.45, 0.06, "wood_light"))):
        p.append(L.spot((x, 0.0, H + 0.001), s, c, facing="top", seed=850 + i, stretch=(1.4, 0.7)))
    p.append(L.spot((0.5, F - 0.025, 0.30), 0.05, "dirt", seed=855))
    return p


def uglovaya():
    p = []
    # длинная часть вдоль стены + короткое «крыло» справа, выступающее вперёд (Г-образная)
    WL = W - 0.02
    carcass(p, WL)
    hb = H - TOP - PLINTH
    door(p, -WL / 2 + 0.20, 0.40, hb - 0.02, PLINTH, handle_side=1)
    door(p, -WL / 2 + 0.60, 0.40, hb - 0.02, PLINTH, handle_side=-1)
    # крыло: выдвинуто вперёд на 0.45 м, дверца смотрит на зрителя
    xw, ww = WL / 2 - 0.20, 0.40
    p.append(L.box((ww, 0.45, hb), (xw, F - 0.225 + 0.0, PLINTH), "wood", bevel=0.008))
    p.append(L.box((ww - 0.02, 0.40, PLINTH), (xw, F - 0.20, 0), "soot", bevel=0.004))
    p.append(L.box((ww + 0.02, 0.47, TOP), (xw, F - 0.225, H - TOP), "wood_dark", bevel=0.008))
    Fw = F - 0.45
    p.append(L.box((ww - 0.012, 0.02, hb - 0.032), (xw, Fw - 0.006, PLINTH + 0.006), "wood_light", bevel=0.008))
    p.append(L.box((ww - 0.08, 0.006, hb - 0.10), (xw, Fw - 0.018, PLINTH + 0.04), "wood", bevel=0.004))
    p.append(L.box((0.016, 0.02, 0.10), (xw - ww / 2 + 0.05, Fw - 0.03, H - TOP - 0.20), "steel", bevel=0.004))
    for i, (x, y, s, c) in enumerate(((-0.3, 0.0, 0.08, "soot"), (xw, F - 0.2, 0.07, "wood"))):
        p.append(L.spot((x, y, H + 0.001), s, c, facing="top", seed=860 + i, stretch=(1.4, 0.7)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("s_rakovinoy", s_rakovinoy), ("s_yaschikami", s_yaschikami), ("uglovaya", uglovaya)):
        L.make(fn, "container", "kitchen_counter", var, broken="door")
    L.save_blend("container", "kitchen_counter")
