"""Ванна `bathtub`. Размер — из плана ОС (170 × 60 см). Варианты (только idle):
  chugunnaya — чугунная на ножках-лапах, белая эмаль внутри, сколы; plastikovaya — акриловая с экраном;
  emalirovannaya — стальная эмалированная на кирпичах. Смеситель на бортике. Запуск: python3 models/furniture/bathtub.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("bathtub"))
D = 0.75


def tub(p, z0, outer, inner, h):
    p.append(L.box((W - 0.02, D, h), (0, 0, z0), outer, bevel=0.08))
    p.append(L.box((W - 0.16, D - 0.16, 0.006), (0, 0, z0 + h - 0.002), inner, bevel=0))
    p.append(L.box((W - 0.22, D - 0.22, 0.004), (0, 0, z0 + h + 0.002), "stone_dark", bevel=0))     # дно (тень)
    p.append(L.cyl(0.02, 0.05, (-W / 2 + 0.12, 0.25, z0 + h), "steel_light", verts=6))             # смеситель
    p.append(L.tube((-W / 2 + 0.12, 0.25, z0 + h + 0.05), (-W / 2 + 0.22, 0.25, z0 + h + 0.04), 0.012, "steel_light", verts=6))


def chugunnaya():
    p = []
    tub(p, 0.14, "plastic_white", "offwhite", H - 0.20)
    p.append(L.box((W - 0.04, 0.02, 0.06), (0, -D / 2 + 0.01, H - 0.08), "offwhite", bevel=0.02))  # отбортовка
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.cyl(0.035, 0.16, (sx * (W / 2 - 0.22), sy * 0.26, 0), "steel_dark", verts=6, radius_top=0.025))
            p.append(L.cyl(0.05, 0.03, (sx * (W / 2 - 0.22), sy * 0.26, 0), "steel_dark", verts=6))
    for i, (x, z, s) in enumerate(((-0.5, 0.30, 0.06), (0.35, 0.45, 0.05), (0.6, 0.25, 0.08))):
        p.append(L.spot((x, -D / 2 + 0.006, z), s, "soot", seed=670 + i))                          # сколы эмали
    p.append(L.spot((0.1, -0.05, H - 0.054), 0.25, "rust_light", facing="top", seed=675, stretch=(2.0, 0.5)))
    return p


def plastikovaya():
    p = []
    tub(p, 0.0, "plastic_white", "plastic_white", H - 0.06)
    p.append(L.box((W - 0.06, 0.01, H - 0.12), (0, -D / 2 - 0.004, 0.02), "plastic_white", bevel=0.004))   # экран
    p.append(L.box((0.25, 0.006, 0.2), (0.4, -D / 2 - 0.01, 0.15), "offwhite", bevel=0.004))             # лючок
    p.append(L.spot((-0.3, -D / 2 - 0.01, 0.25), 0.12, "khaki_light", seed=680, stretch=(1.5, 0.6)))
    return p


def emalirovannaya():
    p = []
    tub(p, 0.12, "steel_light", "offwhite", H - 0.18)
    import random
    r = random.Random(5)
    for x in (-W / 2 + 0.25, W / 2 - 0.25):                                            # подпорки из кирпичей
        for k in range(2):
            p.append(L.box((0.22, 0.10, 0.06), (x + r.uniform(-0.02, 0.02), -0.22, k * 0.06), r.choice(["brick", "rust"]), bevel=0.01))
            p.append(L.box((0.22, 0.10, 0.06), (x + r.uniform(-0.02, 0.02), 0.22, k * 0.06), r.choice(["brick", "rust"]), bevel=0.01))
    for i, (x, z) in enumerate(((-0.4, 0.25), (0.5, 0.35))):
        p.append(L.spot((x, -D / 2 + 0.006, z), 0.10, "rust", seed=685 + i, stretch=(1.3, 0.7)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("chugunnaya", chugunnaya), ("plastikovaya", plastikovaya), ("emalirovannaya", emalirovannaya)):
        L.make(fn, "furniture", "bathtub", var, size_cm=(W * 100, H * 100), broken="tilt")
    L.save_blend("furniture", "bathtub")
