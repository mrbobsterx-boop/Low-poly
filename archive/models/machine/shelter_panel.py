"""Пульт убежища `shelter_panel`. Размер — из плана ОС (60 × 70 см). Вариант (только idle): prostoy_pult —
настенный пульт: экран (светится), лампочки-индикаторы, тумблеры, переключатели, решётка динамика, кабели снизу.
Висит на стене: «спина» — Y = 0, низ — Z = 0. Запуск: python3 models/machine/shelter_panel.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("shelter_panel"))
D = 0.14
F = -D


def prostoy_pult():
    p = [L.box((W, D, H - 0.06), (0, -D / 2, 0.06), "steel", bevel=0.015)]
    p.append(L.box((W - 0.04, 0.008, H - 0.12), (0, F - 0.004, 0.09), "steel_dark", bevel=0.004))
    p.append(L.box((0.30, 0.012, 0.18), (-0.08, F - 0.01, H - 0.28), "soot", bevel=0.006))            # экран
    p.append(L.box((0.26, 0.006, 0.14), (-0.08, F - 0.016, H - 0.26), "glow_screen", glow=True, bevel=0))
    for k in range(6):                                                                 # график на экране
        p.append(L.box((0.03, 0.004, 0.012 + (k % 3) * 0.02), (-0.18 + k * 0.04, F - 0.019, H - 0.24), "plant_dark", bevel=0))
    for k, c in enumerate(("glow_screen", "glow_fire", "glow_lamp", "soot")):         # индикаторы
        p.append(L.cyl(0.012, 0.012, (0.15, F - 0.012, H - 0.12 - k * 0.045), c, verts=8, rot=(90, 0, 0), glow=c.startswith("glow")))
    for k in range(5):                                                                 # тумблеры
        x = -0.22 + k * 0.08
        p.append(L.box((0.03, 0.01, 0.04), (x, F - 0.008, 0.26), "soot", bevel=0.003))
        p.append(L.box((0.008, 0.03, 0.008), (x, F - 0.025, 0.29), "steel_light", rot=(25, 0, 0), bevel=0))
    for x in (0.10, 0.20):                                                             # поворотные переключатели
        p.append(L.cyl(0.025, 0.02, (x, F - 0.012, 0.28), "soot", verts=8, rot=(90, 0, 0)))
        p.append(L.box((0.006, 0.006, 0.03), (x, F - 0.025, 0.285), "offwhite", bevel=0))
    for k in range(4):                                                                 # решётка динамика
        p.append(L.box((0.12, 0.006, 0.008), (-0.18, F - 0.012, 0.13 + k * 0.02), "soot", bevel=0))
    p.append(L.box((0.10, 0.006, 0.03), (0.15, F - 0.012, 0.14), "hazard_yellow", bevel=0))
    for x in (-0.15, 0.0, 0.15):                                                       # кабели снизу
        p.append(L.tube((x, -0.06, 0.06), (x * 1.1, -0.04, 0.0), 0.01, "soot", verts=4))
    p.append(L.spot((0.22, F - 0.009, 0.40), 0.05, "rust", seed=770))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(prostoy_pult, "machine", "shelter_panel", "prostoy_pult", size_cm=(W * 100, H * 100))
    L.save_blend("machine", "shelter_panel")
