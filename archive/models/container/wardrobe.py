"""Шкаф `wardrobe`. Размер — из плана ОС (100 × 200 см). Варианты (только idle; «Открытый / выпотрошенный» — пропуск):
  derevyannyy_dvustvorchatyy — деревянный, две створки с филёнками, карниз, цоколь;
  garderob_s_zerkalom        — створка с зеркалом + деревянная створка + ящик внизу;
  metallicheskiy_shkafchik   — металлический двухдверный (серо-синий), жалюзи, ручка-замок.
Запуск: python3 models/container/wardrobe.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

WF, H = (s / 100 for s in L.size_cm("wardrobe"))
W = WF - 0.05                   # корпус; карниз выступает — всего WF (100 см)
WM = WF - 0.012                 # металлический — без карниза
D = 0.55
F = -D / 2                      # плоскость фасада
PL, CR = 0.08, 0.06             # цоколь, карниз


def carcass(p, body, trim):
    p.append(L.box((W, D, H - PL - CR), (0, 0, PL), body, bevel=0.012))
    p.append(L.box((W + 0.04, D + 0.03, CR), (0, 0.0, H - CR), trim, bevel=0.012))             # карниз
    p.append(L.box((W + 0.05, D + 0.04, 0.02), (0, 0.0, H - 0.02), trim, bevel=0.006))
    p.append(L.box((W - 0.02, D - 0.02, PL), (0, 0.01, 0), trim, bevel=0.01))                 # цоколь
    p.append(L.box((W - 0.03, 0.004, H - PL - CR - 0.02), (0, F - 0.002, PL + 0.01), "soot", bevel=0))  # зазор


def wood_door(p, x0, x1, z0, z1, body, panel, handle_left):
    cx, w = (x0 + x1) / 2, x1 - x0
    p.append(L.box((w - 0.008, 0.022, z1 - z0), (cx, F - 0.011, z0), body, bevel=0.01))
    # две филёнки (рамка тёмная + выпуклая середина)
    h = (z1 - z0 - 0.18) / 2
    for k in range(2):
        z = z0 + 0.06 + k * (h + 0.06)
        p.append(L.box((w - 0.10, 0.008, h), (cx, F - 0.024, z), "wood_dark", bevel=0.004))
        p.append(L.box((w - 0.14, 0.012, h - 0.04), (cx, F - 0.030, z + 0.02), panel, bevel=0.01))
    hx = x1 - 0.04 if handle_left is False else x0 + 0.04
    p.append(L.box((0.018, 0.02, 0.14), (hx, F - 0.04, z0 + (z1 - z0) * 0.45), "steel_dark", bevel=0.005))
    for z in (z0 + 0.15, z1 - 0.15):
        ex = x0 + 0.006 if handle_left is False else x1 - 0.006
        p.append(L.cyl(0.008, 0.06, (ex, F - 0.012, z), "steel", verts=6))


def derevyannyy_dvustvorchatyy():
    p = []
    carcass(p, "wood", "wood_dark")
    z0, z1 = PL + 0.02, H - CR - 0.02
    wood_door(p, -W / 2 + 0.02, -0.004, z0, z1, "wood", "wood_light", handle_left=False)
    wood_door(p, 0.004, W / 2 - 0.02, z0, z1, "wood", "wood_light", handle_left=True)
    p.append(L.box((0.012, 0.006, 0.025), (0.03, F - 0.04, z0 + (z1 - z0) * 0.55), "soot", bevel=0))      # скважина
    for i, (x, z, s, c) in enumerate(((-0.30, 0.40, 0.08, "wood_light"), (0.32, 1.10, 0.06, "wood_dark"),
                                      (0.05, 0.20, 0.07, "wood_light"), (-0.42, 1.60, 0.05, "wood_light"))):
        p.append(L.spot((x, F - 0.036, z), s, c, seed=200 + i, stretch=(1.2, 0.8)))
    return p


def garderob_s_zerkalom():
    p = []
    carcass(p, "wood_dark", "wood")
    z0, z1 = PL + 0.30, H - CR - 0.02
    # левая створка — зеркало в раме
    x0, x1 = -W / 2 + 0.02, -0.004
    cx, w = (x0 + x1) / 2, x1 - x0
    p.append(L.box((w - 0.008, 0.022, z1 - z0), (cx, F - 0.011, z0), "wood", bevel=0.01))
    p.append(L.box((w - 0.10, 0.008, z1 - z0 - 0.14), (cx, F - 0.026, z0 + 0.07), "glass", bevel=0.004))
    for i, (dx, dz) in enumerate(((-0.10, 0.30), (0.06, 0.90))):                                          # блики-полосы
        p.append(L.box((0.03, 0.004, 0.40), (cx + dx, F - 0.031, z0 + dz), "plastic_white", rot=(0, 25, 0), bevel=0))
    p.append(L.spot((cx + 0.10, F - 0.031, z0 + 0.20), 0.10, "steel", seed=210, stretch=(1.0, 0.7)))      # облезлая амальгама
    p.append(L.box((0.018, 0.02, 0.14), (x1 - 0.04, F - 0.04, z0 + 0.60), "steel", bevel=0.005))
    # правая створка — деревянная
    wood_door(p, 0.004, W / 2 - 0.02, z0, z1, "wood", "wood_light", handle_left=True)
    # ящик внизу на всю ширину
    p.append(L.box((W - 0.05, 0.022, 0.24), (0, F - 0.011, PL + 0.03), "wood", bevel=0.01))
    p.append(L.box((W - 0.15, 0.008, 0.16), (0, F - 0.024, PL + 0.07), "wood_light", bevel=0.006))
    p.append(L.box((0.16, 0.02, 0.025), (0, F - 0.036, PL + 0.14), "steel", bevel=0.005))
    for i, (x, z, s) in enumerate(((0.30, 0.95, 0.07), (-0.38, 0.25, 0.06), (0.20, 1.6, 0.05))):
        p.append(L.spot((x, F - 0.036, z), s, "wood_light", seed=215 + i, stretch=(1.2, 0.8)))
    return p


def metallicheskiy_shkafchik():
    p = []
    body, dark = "steel", "steel_dark"
    p.append(L.box((WM, D, H - PL), (0, 0, PL), body, bevel=0.012))
    p.append(L.box((WM + 0.012, D + 0.012, 0.03), (0, 0, H - 0.03), dark, bevel=0.008))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.box((0.05, 0.05, PL), (sx * (WM / 2 - 0.04), sy * (D / 2 - 0.04), 0), "soot", bevel=0.008))
    p.append(L.box((WM - 0.03, 0.004, H - PL - 0.08), (0, F - 0.002, PL + 0.03), "soot", bevel=0))
    z0, z1 = PL + 0.04, H - 0.06
    for x0, x1, hl in ((-WM / 2 + 0.015, -0.004, False), (0.004, WM / 2 - 0.015, True)):
        cx, w = (x0 + x1) / 2, x1 - x0
        p.append(L.box((w - 0.006, 0.018, z1 - z0), (cx, F - 0.009, z0), "paint_blue", bevel=0.008))
        p.append(L.box((w - 0.10, 0.008, 0.9), (cx, F - 0.020, z0 + 0.45), "paint_blue", bevel=0.006))   # выштамповка
        for zz in (z1 - 0.28, z0 + 0.10):                                                                  # жалюзи
            p.append(L.box((w - 0.12, 0.006, 0.16), (cx, F - 0.020, zz), "soot", bevel=0.002))
            for k in range(5):
                p.append(L.box((w - 0.14, 0.01, 0.014), (cx, F - 0.028, zz + 0.012 + k * 0.03), dark,
                               rot=(-35, 0, 0), bevel=0.002))
    # центральная ручка-замок
    p.append(L.box((0.03, 0.03, 0.20), (0.0, F - 0.03, PL + 0.85), "steel_light", bevel=0.006))
    p.append(L.cyl(0.015, 0.012, (0.0, F - 0.05, PL + 1.08), "steel_light", verts=8, rot=(90, 0, 0)))
    p.append(L.box((0.12, 0.005, 0.06), (-0.25, F - 0.026, H - 0.42), "offwhite", bevel=0))               # бирка
    for i, (x, z, s, c) in enumerate(((-0.40, 0.25, 0.06, "rust"), (0.35, 0.15, 0.08, "rust"), (0.20, 1.2, 0.04, "steel"),
                                      (-0.15, 0.7, 0.035, "steel"), (0.42, 1.7, 0.05, "rust_light"))):
        p.append(L.spot((x, F - 0.024, z), s, c, seed=220 + i, stretch=(1.0, 1.3)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("derevyannyy_dvustvorchatyy", derevyannyy_dvustvorchatyy), ("garderob_s_zerkalom", garderob_s_zerkalom),
                    ("metallicheskiy_shkafchik", metallicheskiy_shkafchik)):
        L.make(fn, "container", "wardrobe", var, size_cm=(WF * 100, H * 100), broken="door")
    L.save_blend("container", "wardrobe")
