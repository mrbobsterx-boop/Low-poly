"""Батарейка `battery_cell` (предмет). Размер — из плана ОС (3 × 6 см). Варианты (только idle; «разряженная» — пропуск):
  odnorazovaya — пальчиковая щелочная (жёлто-чёрная); perezaryazhaemaya — аккумулятор (синий с белой полосой).
Запуск: python3 models/item/battery_cell.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("battery_cell"))
R = W / 2
ROUGH = {"min_area": 0.0005, "k": 0.02, "amp_max": 0.001}


def cell(body, band, band_z):
    p = [L.cyl(R, H - 0.004, (0, 0, 0), body, verts=10)]
    p.append(L.cyl(R * 1.005, H * 0.3, (0, 0, band_z), band, verts=10))
    p.append(L.cyl(R * 0.35, 0.004, (0, 0, H - 0.004), "steel_light", verts=8))
    p.append(L.box((0.006, 0.002, 0.006), (0, -R - 0.0005, H * 0.75), "soot", bevel=0))               # «+»
    return p


def odnorazovaya():
    return cell("hazard_yellow", "soot", 0.0)


def perezaryazhaemaya():
    return cell("paint_blue", "plastic_white", H * 0.35)


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("odnorazovaya", odnorazovaya), ("perezaryazhaemaya", perezaryazhaemaya)):
        L.make(fn, "item", "battery_cell", var, size_cm=(W * 100, H * 100), limit="small", rough=ROUGH)
    L.save_blend("item", "battery_cell")
