"""Выключатель `light_switch`. Размер — из плана ОС (8 × 12 см). Висит на стене: «спина» — Y = 0, низ — Z = 0.
Варианты (только idle; «сломанный» — пропуск): klavishnyy — бытовая клавиша; rychazhnyy — промышленный рубильник
с рычагом; tumbler_na_schitke — тумблер на железном щитке. Запуск: python3 models/machine/light_switch.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("light_switch"))
ROUGH = {"min_area": 0.0008, "k": 0.02, "amp_max": 0.001}


def klavishnyy():
    p = [L.box((W, 0.015, H), (0, -0.0075, 0), "offwhite", bevel=0.004)]
    p.append(L.box((W * 0.6, 0.012, H * 0.6), (0, -0.018, H * 0.2), "plastic_white", rot=(6, 0, 0), bevel=0.003))
    p.append(L.box((0.006, 0.004, 0.006), (0, -0.025, H * 0.65), "glow_fire", glow=True, bevel=0))
    p.append(L.spot((0.0, -0.016, H * 0.15), 0.02, "dirt", seed=790))
    return p


def rychazhnyy():
    p = [L.box((W, 0.03, H), (0, -0.015, 0), "steel_dark", bevel=0.004)]
    p.append(L.box((W * 0.7, 0.006, H * 0.7), (0, -0.033, H * 0.15), "soot", bevel=0.002))
    p.append(L.tube((0, -0.04, H * 0.45), (0.0, -0.05, H - 0.005), 0.004, "steel_light", verts=4))   # рычаг
    p.append(L.cyl(0.006, 0.012, (0.0, -0.06, H - 0.01), "paint_red", verts=6, rot=(90, 0, 0)))
    p.append(L.box((W * 0.5, 0.004, 0.008), (0, -0.032, H * 0.08), "hazard_yellow", bevel=0))
    return p


def tumbler_na_schitke():
    p = [L.box((W, 0.006, H), (0, -0.003, 0), "steel", bevel=0.002)]
    for x in (-W / 2 + 0.008, W / 2 - 0.008):
        p.append(L.cyl(0.003, 0.003, (x, -0.007, H - 0.008), "steel_dark", verts=6, rot=(90, 0, 0)))
    p.append(L.cyl(0.012, 0.012, (0, -0.012, H * 0.5), "steel_dark", verts=8, rot=(90, 0, 0)))
    p.append(L.tube((0, -0.016, H * 0.5), (0, -0.03, H * 0.65), 0.003, "steel_light", verts=4))
    p.append(L.box((W * 0.7, 0.004, 0.012), (0, -0.008, H * 0.12), "offwhite", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("klavishnyy", klavishnyy), ("rychazhnyy", rychazhnyy), ("tumbler_na_schitke", tumbler_na_schitke)):
        L.make(fn, "machine", "light_switch", var, size_cm=(W * 100, H * 100), limit="small", rough=ROUGH)
    L.save_blend("machine", "light_switch")
