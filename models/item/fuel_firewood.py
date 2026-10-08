"""Дрова `fuel_firewood` (предмет). Размер — из плана ОС (40 × 15 см). Варианты (только idle):
  polenya — 3 колотых полена (светлый скол, кора); vyazanka_hvorosta — вязанка тонких веток, верёвка;
  otsyrevshie — поленья тёмные, с мхом (сырые — горят хуже). Запуск: python3 models/item/fuel_firewood.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("fuel_firewood"))
ROUGH = {"min_area": 0.004, "k": 0.03, "amp_max": 0.003}


def log(p, x, y, z, ln, r, bark, cut, rot=0):
    o = L.cyl(r, ln, (0, 0, 0), bark, verts=6)
    L.transform([o], (x - ln / 2, y, z + r), (0, 90, rot))
    p.append(o)
    for sx in (-1, 1):                                                                 # торцы-сколы
        c = L.cyl(r * 0.85, 0.004, (0, 0, 0), cut, verts=6)
        L.transform([c], (x + sx * ln / 2 - (0.004 if sx > 0 else 0), y, z + r), (0, 90, rot))
        p.append(c)


def polenya():
    p = []
    log(p, -0.0, -0.02, 0.0, W - 0.02, 0.045, "wood_dark", "wood_light")
    log(p, 0.01, 0.07, 0.0, W - 0.04, 0.042, "wood_dark", "wood_light", rot=4)
    log(p, 0.0, 0.025, 0.07, W - 0.06, 0.04, "wood", "wood_light", rot=-3)
    return p


def vyazanka_hvorosta():
    import random
    r = random.Random(3)
    p = []
    for k in range(9):
        y, z = r.uniform(-0.03, 0.03), r.uniform(0.02, 0.12)
        p.append(L.tube((-W / 2 + r.uniform(0, 0.03), y, z + 0.015), (W / 2 - r.uniform(0, 0.03), y, z + 0.015 + r.uniform(-0.01, 0.01)),
                        0.008 + r.uniform(0, 0.005), r.choice(["wood_dark", "wood", "dirt"]), verts=4))
    for x in (-0.10, 0.10):
        p.append(L.cyl(0.06, 0.015, (x, 0, 0.06), "cloth_beige", verts=6, rot=(0, 90, 0)))           # верёвка
    return p


def otsyrevshie():
    p = []
    log(p, 0.0, -0.02, 0.0, W - 0.02, 0.045, "soot", "wood_dark")
    log(p, 0.01, 0.07, 0.0, W - 0.04, 0.042, "stone_dark", "wood_dark", rot=4)
    log(p, 0.0, 0.025, 0.07, W - 0.06, 0.04, "soot", "wood_dark", rot=-3)
    for i, (x, z) in enumerate(((-0.08, 0.06), (0.10, 0.03), (0.0, 0.12))):
        p.append(L.spot((x, -0.068, z), 0.05, "plant_dark", seed=780 + i, stretch=(1.3, 0.7)))          # мох
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("polenya", polenya), ("vyazanka_hvorosta", vyazanka_hvorosta), ("otsyrevshie", otsyrevshie)):
        L.make(fn, "item", "fuel_firewood", var, size_cm=(W * 100, H * 100), limit="small", rough=ROUGH)
    L.save_blend("item", "fuel_firewood")
