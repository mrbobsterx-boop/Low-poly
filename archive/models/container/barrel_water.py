"""Бочка для воды `barrel_water`. Размер — из плана ОС (60 × 90 см). Варианты (только idle):
  plastikovaya_200_l — синяя пластиковая бочка с рёбрами и пробками;
  metallicheskaya_200_l — стальная крашеная бочка с обручами, кран внизу;
  derevyannaya_100_l — деревянная бочка из клёпок с обручами, крышка, кран;
  malaya_kanistra_bochonok_30_l — малый бочонок 30 л (меньше по природе — отклонение).
Запуск: python3 models/container/barrel_water.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("barrel_water"))
R = W / 2 - 0.004              # 12-гранник: по бокам ~0,97 радиуса, + обручи
N = 12


def tap(p, z, r):
    p.append(L.cyl(0.02, 0.06, (0, -r - 0.05, z), "steel", verts=8, rot=(90, 0, 0)))
    p.append(L.box((0.06, 0.02, 0.012), (0, -r - 0.065, z + 0.03), "paint_red", bevel=0.004))
    p.append(L.cyl(0.012, 0.04, (0, -r - 0.08, z - 0.04), "steel", verts=6))


def plastikovaya_200_l():
    p = [L.cyl(R, H - 0.02, (0, 0, 0.01), "paint_blue", verts=N, radius_top=R - 0.01)]
    for z in (0.08, H * 0.36, H * 0.64, H - 0.10):
        p.append(L.cyl(R + 0.012, 0.03, (0, 0, z), "paint_blue", verts=N))                              # рёбра
    p.append(L.cyl(R - 0.02, 0.015, (0, 0, H - 0.027), "paint_blue", verts=N))
    for x in (-0.12, 0.13):
        p.append(L.cyl(0.035, 0.015, (x, 0.0, H - 0.025), "offwhite" if x < 0 else "paint_red", verts=8))   # пробки
    p.append(L.box((0.16, 0.004, 0.10), (0, -R * 0.97 - 0.004, H * 0.45), "offwhite", bevel=0))           # наклейка
    for k in range(3):
        p.append(L.box((0.12, 0.004, 0.008), (0, -R * 0.97 - 0.007, H * 0.45 + 0.02 + k * 0.025), "soot", bevel=0))
    p.append(L.spot((0.18, -R * 0.95, H * 0.2), 0.10, "dirt", seed=500, stretch=(1.0, 0.6)))
    return p


def metallicheskaya_200_l():
    p = [L.cyl(R, H - 0.02, (0, 0, 0.01), "army_green", verts=N)]
    for z in (0.01, H * 0.33, H * 0.66, H - 0.04):
        p.append(L.cyl(R + 0.014, 0.03, (0, 0, z), "olive_dark", verts=N))
    p.append(L.cyl(R - 0.01, 0.012, (0, 0, H - 0.027), "olive_dark", verts=N))
    p.append(L.cyl(0.03, 0.012, (0.13, 0.05, H - 0.015), "steel", verts=8))
    tap(p, 0.14, R)
    p.append(L.box((0.03, 0.004, 0.10), (-0.08, -R * 0.97 - 0.006, H * 0.40), "offwhite", bevel=0))   # трафарет «Н₂О» — полосы
    p.append(L.box((0.03, 0.004, 0.10), (-0.02, -R * 0.97 - 0.006, H * 0.40), "offwhite", bevel=0))
    for i, (x, z, s) in enumerate(((0.15, H * 0.18, 0.12), (-0.18, H * 0.75, 0.08), (0.05, 0.05, 0.10))):
        p.append(L.spot((x, -R * 0.97, z), s, "rust", seed=505 + i, stretch=(1.2, 0.8)))
    return p


def derevyannaya_100_l():
    import math
    p = []
    Hb, Rb = H * 0.78, R * 0.85
    n = 14
    # «пузатая» бочка из двух усечённых конусов, швы клёпок — тёмные полосы спереди
    p.append(L.cyl(Rb * 0.88, Hb / 2, (0, 0, 0), "wood", verts=n, radius_top=Rb))
    p.append(L.cyl(Rb, Hb / 2, (0, 0, Hb / 2), "wood", verts=n, radius_top=Rb * 0.88))
    for k in range(n):
        a = 2 * math.pi * k / n
        if math.sin(a) < -0.2:
            p.append(L.box((0.006, 0.006, Hb - 0.02), (Rb * 0.93 * math.cos(a), Rb * 0.93 * math.sin(a), 0.01), "wood_dark",
                           rot=(0, 0, math.degrees(a)), bevel=0))
    for z, rr in ((0.05, 0.90), (Hb * 0.3, 0.97), (Hb * 0.7, 0.97), (Hb - 0.08, 0.90)):
        p.append(L.cyl(Rb * rr + 0.012, 0.03, (0, 0, z), "steel_dark", verts=n))
    p.append(L.cyl(Rb * 0.88 + 0.01, 0.03, (0, 0, Hb), "wood_light", verts=n))                       # крышка
    p.append(L.box((0.20, 0.04, 0.03), (0, 0, Hb + 0.03), "wood_dark", bevel=0.006))
    tap(p, 0.10, Rb)
    p.append(L.spot((0.1, -Rb * 0.95, Hb * 0.5), 0.10, "wood_dark", seed=510, stretch=(0.7, 1.4)))
    return p


def malaya_kanistra_bochonok_30_l():
    """Бочонок 30 л: пластиковый, с ручкой и крышкой-горловиной (меньше бочки — отклонение от 60 × 90)."""
    p = [L.cyl(0.17, 0.40, (0, 0, 0), "plastic_white", verts=N, radius_top=0.16)]
    for z in (0.10, 0.28):
        p.append(L.cyl(0.178, 0.02, (0, 0, z), "offwhite", verts=N))
    p.append(L.cyl(0.07, 0.04, (0.06, 0, 0.40), "paint_blue", verts=8))
    p.append(L.tube((-0.10, 0, 0.40), (-0.10, 0, 0.47), 0.012, "paint_blue", verts=6))
    p.append(L.tube((-0.10, 0, 0.47), (0.0, 0, 0.47), 0.012, "paint_blue", verts=6))
    p.append(L.tube((0.0, 0, 0.47), (0.0, 0, 0.40), 0.012, "paint_blue", verts=6))
    p.append(L.box((0.12, 0.004, 0.08), (0, -0.168, 0.18), "paint_blue", bevel=0))
    p.append(L.spot((0.08, -0.16, 0.06), 0.06, "dirt", seed=515))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz in (("plastikovaya_200_l", plastikovaya_200_l, (W * 100, H * 100)),
                        ("metallicheskaya_200_l", metallicheskaya_200_l, (W * 100, H * 100)),
                        ("derevyannaya_100_l", derevyannaya_100_l, None),
                        ("malaya_kanistra_bochonok_30_l", malaya_kanistra_bochonok_30_l, None)):
        L.make(fn, "container", "barrel_water", var, size_cm=sz, broken="tilt")
    L.save_blend("container", "barrel_water")
