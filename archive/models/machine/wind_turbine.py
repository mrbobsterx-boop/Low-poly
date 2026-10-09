"""Ветрогенератор `wind_turbine`. Размер — из плана ОС (100 × 300 см). Лопасти — лицом к камере (вид спереди).
Варианты (только idle): malyy_gorizontalnyy — три лопасти на мачте с хвостом; vertikalnyy — вертикальный (ротор
из лопастей-«бочек» Савониуса); samodelnyy_iz_ventilyatora — крыльчатка вентилятора на трубе, хвост из жести.
Запуск: python3 models/machine/wind_turbine.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("wind_turbine"))


def mast(p, h, color="steel"):
    p.append(L.box((0.40, 0.40, 0.08), (0, 0, 0), "concrete", bevel=0.02))
    p.append(L.cyl(0.04, h, (0, 0, 0.08), color, verts=8, radius_top=0.03))
    for k in range(3):
        a = math.pi / 2 + k * 2 * math.pi / 3
        p.append(L.tube((0, 0, h * 0.5), (0.45 * math.cos(a), 0.45 * math.sin(a), 0.0), 0.006, "steel_dark", verts=4))  # растяжки


def blades(p, cz, r, n, color, cy=-0.12, width=0.10):
    for k in range(n):
        a = math.pi / 2 + k * 2 * math.pi / n
        parts = [L.poly([(0, -width / 2), (r, -width * 0.25), (r, width * 0.15), (0, width / 2)], 0.02, (0, 0, 0), color)]
        L.transform(parts, (0, cy, cz), (0, -math.degrees(a), 0))
        p += parts


def malyy_gorizontalnyy():
    p = []
    mast(p, H - 0.55)
    hz = H - W / 2
    p.append(L.cyl(0.07, 0.30, (0, -0.10, hz), "plastic_white", verts=8, rot=(-90, 0, 0)))          # гондола
    p.append(L.cyl(0.07, 0.10, (0, -0.10, hz), "plastic_white", verts=8, rot=(90, 0, 0), radius_top=0.01))   # кок
    blades(p, hz, W / 2 - 0.02, 3, "offwhite", cy=-0.14)
    p.append(L.tube((0, 0.18, hz), (0, 0.45, hz + 0.05), 0.012, "steel", verts=4))
    p.append(L.poly([(0, 0), (0.0, 0.20), (0.02, 0.20), (0.02, 0)], 0.25, (0, 0.50, hz - 0.05), "paint_red"))
    p.append(L.box((0.12, 0.08, 0.16), (0, -0.05, 0.40), "steel_dark", bevel=0.01))                 # контроллер
    return p


def vertikalnyy():
    p = []
    mast(p, H - 1.2, "steel_dark")
    z0 = H - 1.15
    p.append(L.cyl(0.03, 1.15, (0, 0, z0), "steel", verts=8))
    for k in range(3):                                                                 # лопасти-полубочки (спираль)
        a = k * 2 * math.pi / 3
        x, y = 0.25 * math.cos(a), 0.25 * math.sin(a)
        p.append(L.cyl(0.22, 0.95, (x, y, z0 + 0.10), "steel_light" if k % 2 else "paint_blue", verts=6))
    for z in (z0 + 0.08, z0 + 1.07):
        p.append(L.cyl(W / 2, 0.03, (0, 0, z), "steel_dark", verts=10))
    return p


def samodelnyy_iz_ventilyatora():
    p = []
    p.append(L.box((0.30, 0.30, 0.06), (0, 0, 0), "wood", bevel=0.01))
    p.append(L.cyl(0.035, H - 0.45, (0, 0, 0.06), "rust", verts=8))
    for z in (0.6, 1.4):                                                               # хомуты-проволока
        p.append(L.cyl(0.045, 0.03, (0, 0, z), "steel_dark", verts=8))
    hz = H - 0.40
    p.append(L.cyl(0.10, 0.18, (0, -0.06, hz), "army_green", verts=10, rot=(-90, 0, 0)))            # моторчик
    p.append(L.cyl(0.04, 0.06, (0, -0.10, hz), "steel", verts=8, rot=(90, 0, 0)))
    blades(p, hz, 0.34, 4, "paint_blue", cy=-0.16, width=0.16)
    p.append(L.tube((0, 0.10, hz), (0, 0.40, hz), 0.01, "steel_dark", verts=4))
    p.append(L.poly([(0, -0.12), (0.0, 0.12), (0.01, 0.12), (0.01, -0.12)], 0.30, (0, 0.45, hz), "steel"))
    p.append(L.tube((0.0, -0.05, hz - 0.10), (0.15, -0.10, 0.5), 0.006, "soot", verts=4))          # провод
    p.append(L.box((0.12, 0.06, 0.10), (0.18, -0.10, 0.42), "steel_dark", bevel=0.008))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("malyy_gorizontalnyy", malyy_gorizontalnyy), ("vertikalnyy", vertikalnyy),
                    ("samodelnyy_iz_ventilyatora", samodelnyy_iz_ventilyatora)):
        L.make(fn, "machine", "wind_turbine", var, size_cm=None, broken="tilt")
    L.save_blend("machine", "wind_turbine")
