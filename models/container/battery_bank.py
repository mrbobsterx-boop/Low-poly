"""Аккумулятор `battery_bank`. Размер — из плана ОС (60 × 40 см). Варианты (только idle; «разряженный» — пропуск):
  avtomobilnyy_12_v — автомобильный аккумулятор (меньше по природе — 32 × 24, отклонение);
  bunkernaya_batareya — шкаф-батарея бункера: банки в ряд, индикатор заряда (светится), клеммы, кабели.
Запуск: python3 models/container/battery_bank.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("battery_bank"))


def avtomobilnyy_12_v():
    p = [L.box((0.32, 0.18, 0.20), (0, 0, 0), "soot", bevel=0.01)]
    p.append(L.box((0.32, 0.18, 0.02), (0, 0, 0.20), "stone_dark", bevel=0.006))
    for x, c in ((-0.10, "paint_red"), (0.10, "paint_blue")):
        p.append(L.cyl(0.018, 0.025, (x, -0.03, 0.22), "steel_light", verts=8))
        p.append(L.box((0.05, 0.004, 0.03), (x, -0.091, 0.15), c, bevel=0))
    p.append(L.box((0.14, 0.004, 0.06), (0, -0.091, 0.07), "offwhite", bevel=0))                    # этикетка
    p.append(L.box((0.10, 0.004, 0.012), (0, -0.094, 0.10), "soot", bevel=0))
    p.append(L.tube((-0.12, 0.0, 0.22), (-0.12, 0.0, 0.24), 0.01, "soot", verts=4))                 # ручка
    p.append(L.tube((-0.12, 0.0, 0.24), (0.12, 0.0, 0.24), 0.01, "soot", verts=4))
    p.append(L.tube((0.12, 0.0, 0.24), (0.12, 0.0, 0.22), 0.01, "soot", verts=4))
    p.append(L.spot((0.10, -0.03, 0.247), 0.04, "offwhite", facing="top", seed=700))                 # налёт на клемме
    return p


def bunkernaya_batareya():
    p = [L.box((W, 0.35, H - 0.04), (0, 0, 0.04), "steel_dark", bevel=0.012)]
    for sx in (-1, 1):
        p.append(L.box((0.05, 0.30, 0.04), (sx * (W / 2 - 0.05), 0, 0), "soot", bevel=0.006))
    for k in range(4):                                                                 # банки в окне
        x = -0.21 + k * 0.14
        p.append(L.box((0.11, 0.01, 0.18), (x, -0.176, 0.10), "soot", bevel=0.004))
        p.append(L.box((0.09, 0.012, 0.15), (x, -0.18, 0.115), "khaki", bevel=0.004))
        p.append(L.cyl(0.012, 0.02, (x - 0.025, -0.15, H), "paint_red", verts=6))
        p.append(L.cyl(0.012, 0.02, (x + 0.025, -0.15, H), "soot", verts=6))
    for k in range(5):                                                                 # индикатор заряда
        p.append(L.box((0.03, 0.006, 0.02), (-0.20 + k * 0.035, -0.178, 0.32),
                       "glow_screen" if k < 3 else "soot", glow=k < 3, bevel=0))
    p.append(L.box((0.12, 0.006, 0.05), (0.18, -0.178, 0.31), "offwhite", bevel=0))
    p.append(L.tube((-0.25, -0.12, H + 0.01), (-0.27, -0.19, 0.20), 0.008, "paint_red", verts=4))   # кабели
    p.append(L.tube((0.25, -0.12, H + 0.01), (0.27, -0.19, 0.20), 0.008, "soot", verts=4))
    p.append(L.spot((0.2, -0.177, 0.07), 0.06, "rust", seed=705))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(avtomobilnyy_12_v, "container", "battery_bank", "avtomobilnyy_12_v", limit="small")
    L.make(bunkernaya_batareya, "container", "battery_bank", "bunkernaya_batareya", size_cm=(W * 100, H * 100))
    L.save_blend("container", "battery_bank")
