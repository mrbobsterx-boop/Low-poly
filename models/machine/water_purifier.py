"""Очиститель воды `water_purifier`. Размер — из плана ОС (60 × 100 см). Варианты (только idle):
  keramicheskiy_filtr — два ведра-бака друг на друге с керамическими свечами, кран, подставка;
  kipyachenie_na_pechi — стойка-тренога над жаровней, котёл с крышкой (огонь светится);
  ugolnyy_filtr — бочка-колонна со слоями (песок/уголь/гравий в окошке), кран;
  himicheskie_tabletki — бак с дозатором таблеток и мерной кружкой. Запуск: python3 models/machine/water_purifier.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("water_purifier"))


def stand(p, h):
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.box((0.04, 0.04, h), (sx * 0.22, sy * 0.18, 0), "wood_dark", bevel=0.006))
    p.append(L.box((0.52, 0.44, 0.03), (0, 0, h), "wood", bevel=0.006))


def tap(p, x, z, y):
    p.append(L.cyl(0.015, 0.05, (x, y - 0.02, z), "steel", verts=6, rot=(90, 0, 0)))
    p.append(L.box((0.04, 0.012, 0.012), (x, y - 0.06, z + 0.02), "paint_blue", bevel=0.003))


def keramicheskiy_filtr():
    p = []
    stand(p, 0.35)
    for k, z in enumerate((0.38, 0.68)):
        p.append(L.cyl(0.21, 0.29, (0, 0, z), "steel_light" if k == 0 else "steel", verts=12))
        p.append(L.cyl(0.215, 0.015, (0, 0, z + 0.27), "steel_dark", verts=12))
    p.append(L.cyl(0.20, 0.03, (0, 0, H - 0.03), "steel_dark", verts=12))
    tap(p, 0.0, 0.43, -0.20)
    p.append(L.box((0.12, 0.004, 0.08), (0, -0.207, 0.80), "offwhite", bevel=0))
    return p


def kipyachenie_na_pechi():
    p = []
    import math
    for k in range(3):                                                                 # тренога
        a = math.pi / 2 + k * 2 * math.pi / 3
        p.append(L.tube((0.28 * math.cos(a), 0.22 * math.sin(a), 0), (0, 0, H - 0.04), 0.014, "soot", verts=4))
    p.append(L.cyl(0.18, 0.08, (0, 0, 0), "stone_dark", verts=10))                                   # жаровня
    p.append(L.cyl(0.14, 0.04, (0, 0, 0.08), "glow_fire", verts=8, glow=True))
    for k in range(3):
        p.append(L.box((0.22, 0.04, 0.04), (0, -0.04 + k * 0.04, 0.10), "wood_dark", rot=(0, 0, 30 * k - 30), bevel=0.006))
    p.append(L.tube((0, 0, H - 0.04), (0, 0, 0.62), 0.004, "steel_dark", verts=4))                  # цепь
    p.append(L.cyl(0.17, 0.22, (0, 0, 0.38), "soot", verts=12, radius_top=0.18))                     # котёл
    p.append(L.cyl(0.185, 0.02, (0, 0, 0.60), "steel_dark", verts=12))                                # крышка
    p.append(L.cyl(0.03, 0.03, (0, 0, 0.62), "soot", verts=6))
    p.append(L.spot((0.0, -0.17, 0.45), 0.10, "rust_dark", seed=630))
    return p


def ugolnyy_filtr():
    p = [L.cyl(0.24, H - 0.12, (0, 0, 0.06), "paint_blue", verts=12)]
    p.append(L.cyl(0.25, 0.06, (0, 0, 0), "steel_dark", verts=12))
    p.append(L.cyl(0.25, 0.06, (0, 0, H - 0.06), "steel_dark", verts=12))
    # окошко со слоями: гравий / уголь / песок
    z = 0.20
    for c, h in (("concrete_light", 0.12), ("soot", 0.18), ("cloth_beige", 0.14)):
        p.append(L.box((0.16, 0.012, h - 0.01), (0.0, -0.236, z), c, bevel=0))
        z += h
    p.append(L.box((0.19, 0.008, 0.46), (0.0, -0.232, 0.185), "steel", bevel=0.004))
    tap(p, 0.12, 0.12, -0.24)
    return p


def himicheskie_tabletki():
    p = []
    stand(p, 0.30)
    p.append(L.box((0.44, 0.36, 0.48), (0, 0, 0.33), "plastic_white", bevel=0.03))
    p.append(L.box((0.46, 0.38, 0.03), (0, 0, 0.81), "paint_blue", bevel=0.01))
    p.append(L.box((0.10, 0.10, 0.14), (0.12, 0, 0.84), "steel", bevel=0.01))                      # дозатор
    p.append(L.box((0.03, 0.04, 0.02), (0.12, -0.06, 0.92), "paint_red", bevel=0.005))
    p.append(L.box((0.16, 0.004, 0.10), (-0.08, -0.182, 0.62), "offwhite", bevel=0))               # инструкция
    for k in range(3):
        p.append(L.box((0.12, 0.004, 0.008), (-0.08, -0.185, 0.64 + k * 0.025), "soot", bevel=0))
    tap(p, 0.12, 0.38, -0.18)
    p.append(L.cyl(0.04, 0.08, (-0.15, -0.05, 0.84), "steel_light", verts=8))                       # кружка
    p.append(L.spot((0.0, -0.181, 0.40), 0.12, "khaki_light", seed=640, stretch=(1.3, 0.7)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz in (("keramicheskiy_filtr", keramicheskiy_filtr, None), ("kipyachenie_na_pechi", kipyachenie_na_pechi, None),
                        ("ugolnyy_filtr", ugolnyy_filtr, None), ("himicheskie_tabletki", himicheskie_tabletki, None)):
        L.make(fn, "machine", "water_purifier", var, size_cm=sz, broken="tilt")
    L.save_blend("machine", "water_purifier")
