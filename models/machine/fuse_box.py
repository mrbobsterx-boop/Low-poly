"""Электрощит `fuse_box`. Размер — из плана ОС (40 × 50 см). Висит на стене: «спина» — Y = 0, низ — Z = 0.
Варианты (только idle; «сгоревший» — пропуск): bytovoy — серый щиток с прозрачным окошком автоматов;
promyshlennyy — массивный шкаф с рукояткой-рубильником и знаком; samodelnyy — доска с пробками и проводами.
Запуск: python3 models/machine/fuse_box.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("fuse_box"))


def bytovoy():
    p = [L.box((W, 0.10, H), (0, -0.05, 0), "steel_light", bevel=0.012)]
    p.append(L.box((W - 0.04, 0.008, H - 0.04), (0, -0.104, 0.02), "steel", bevel=0.006))             # дверца
    p.append(L.box((0.26, 0.006, 0.08), (0, -0.11, H - 0.18), "glass", bevel=0.002))
    for k in range(6):
        p.append(L.box((0.03, 0.004, 0.05), (-0.10 + k * 0.04, -0.114, H - 0.165), "offwhite" if k != 4 else "paint_red", bevel=0))
    p.append(L.box((0.02, 0.02, 0.06), (W / 2 - 0.04, -0.12, 0.20), "soot", bevel=0.004))
    p.append(L.box((0.08, 0.004, 0.07), (0, -0.11, 0.12), "hazard_yellow", rot=(0, 45, 0), bevel=0))
    p.append(L.spot((0.12, -0.109, 0.06), 0.05, "rust", seed=795))
    return p


def promyshlennyy():
    p = [L.box((W, 0.16, H), (0, -0.08, 0), "steel_dark", bevel=0.015)]
    p.append(L.box((W - 0.04, 0.008, H - 0.04), (0, -0.164, 0.02), "steel", bevel=0.006))
    p.append(L.box((0.04, 0.05, 0.14), (W / 2 - 0.07, -0.19, H * 0.45), "soot", bevel=0.006))         # рубильник
    p.append(L.box((0.05, 0.06, 0.03), (W / 2 - 0.07, -0.22, H * 0.45 + 0.12), "paint_red", bevel=0.006))
    p.append(L.box((0.12, 0.004, 0.11), (-0.06, -0.17, H - 0.18), "hazard_yellow", rot=(0, 45, 0), bevel=0))
    p.append(L.box((0.03, 0.004, 0.06), (-0.06, -0.173, H - 0.17), "soot", rot=(0, 20, 0), bevel=0))    # молния
    for x in (-W / 2 + 0.03, W / 2 - 0.03):
        for z in (0.03, H - 0.03):
            p.append(L.cyl(0.008, 0.006, (x, -0.168, z), "steel_light", verts=6, rot=(90, 0, 0)))
    p.append(L.spot((-0.1, -0.169, 0.08), 0.07, "rust", seed=796, stretch=(1.2, 0.8)))
    return p


def samodelnyy():
    p = [L.box((W, 0.025, H), (0, -0.0125, 0), "wood", bevel=0.008)]
    for k in range(4):                                                                 # пробки
        x = -0.12 + k * 0.08
        p.append(L.cyl(0.022, 0.03, (x, -0.04, H - 0.15), "plastic_white", verts=8, rot=(90, 0, 0)))
        p.append(L.cyl(0.012, 0.012, (x, -0.06, H - 0.15), "soot" if k != 2 else "paint_red", verts=6, rot=(90, 0, 0)))
    p.append(L.box((0.10, 0.04, 0.12), (0.08, -0.045, 0.10), "soot", bevel=0.008))                    # счётчик
    p.append(L.box((0.07, 0.006, 0.03), (0.08, -0.068, 0.17), "glass", bevel=0))
    import random
    r = random.Random(4)
    for k in range(5):                                                                 # провода
        x0 = -0.12 + k * 0.06
        c = r.choice(["paint_red", "soot", "paint_blue", "hazard_yellow"])
        p.append(L.tube((x0, -0.03, H - 0.10), (x0 + r.uniform(-0.05, 0.05), -0.035, H + 0.0), 0.004, c, verts=4))
        p.append(L.tube((x0, -0.03, 0.30), (x0 + r.uniform(-0.04, 0.04), -0.035, 0.0), 0.004, c, verts=4))
    p.append(L.box((0.06, 0.004, 0.02), (-0.10, -0.027, 0.06), "offwhite", bevel=0))                 # бирка
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("bytovoy", bytovoy), ("promyshlennyy", promyshlennyy), ("samodelnyy", samodelnyy)):
        L.make(fn, "machine", "fuse_box", var, size_cm=(W * 100, H * 100), limit="small")
    L.save_blend("machine", "fuse_box")
