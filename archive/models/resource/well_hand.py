"""Колодец `well_hand` (ресурс). Размер — из плана ОС (90 × 130 см). Варианты (только idle; «пересохший» — пропуск):
  ruchnoy_kolodets_s_vorotom — каменный сруб, ворот с ручкой, крыша-домик, ведро на цепи;
  skvazhina_s_ruchnoy_pompoy — бетонное кольцо-оголовок, чугунная ручная колонка с рычагом;
  skvazhina_s_elektronasosom — оголовок, насос в кожухе, кабель, кран, щиток.
Запуск: python3 models/resource/well_hand.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("well_hand"))


def ruchnoy_kolodets_s_vorotom():
    p = []
    import random
    r = random.Random(3)
    for k in range(4):                                                                 # каменный сруб
        for j in range(5):
            x = -0.36 + j * 0.18 + (0.09 if k % 2 else 0)
            if abs(x) <= 0.40:
                p.append(L.box((0.17, 0.70, 0.12), (x, 0, k * 0.125), r.choice(["concrete", "concrete_light", "stone_dark"]), bevel=0.02))
    p.append(L.box((W - 0.04, 0.74, 0.04), (0, 0, 0.50), "wood_dark", bevel=0.01))
    for sx in (-1, 1):                                                                 # стойки
        p.append(L.box((0.07, 0.07, 0.62), (sx * 0.38, 0, 0.50), "wood_dark", bevel=0.01))
    p.append(L.cyl(0.07, 0.68, (-0.34, 0, 0.88), "wood", verts=8, rot=(0, 90, 0)))                   # ворот
    p.append(L.box((0.03, 0.03, 0.18), (0.38, -0.06, 0.80), "steel_dark", bevel=0.004))               # ручка (вперёд)
    p.append(L.box((0.03, 0.10, 0.03), (0.38, -0.10, 0.80), "steel_dark", bevel=0.004))
    p.append(L.tube((0.0, -0.05, 0.86), (0.0, -0.05, 0.62), 0.006, "steel", verts=4))                # цепь
    p.append(L.cyl(0.10, 0.15, (0.0, -0.05, 0.48), "steel", verts=8, radius_top=0.12))               # ведро
    pts = [(-W / 2, 1.12), (0, H), (W / 2, 1.12)]                                      # крыша-домик
    p.append(L.prism([(-W / 2 - 0.02, 1.10), (0, H), (W / 2 + 0.02, 1.10), (W / 2 + 0.02, 1.06), (0, H - 0.05),
                      (-W / 2 - 0.02, 1.06)], "y", -0.42, 0.42, "wood"))
    for i, (x, z) in enumerate(((-0.25, 0.15), (0.2, 0.32))):
        p.append(L.spot((x, -0.352, z), 0.14, "plant_dark", seed=590 + i, stretch=(1.3, 0.7)))
    return p


def skvazhina_s_ruchnoy_pompoy():
    p = [L.cyl(0.42, 0.35, (0, 0, 0), "concrete", verts=12), L.cyl(0.38, 0.04, (0, 0, 0.35), "steel_dark", verts=12)]
    p.append(L.cyl(0.08, 0.75, (0, 0, 0.39), "army_green", verts=8))                                 # корпус колонки
    p.append(L.cyl(0.10, 0.08, (0, 0, 1.08), "army_green", verts=8))
    p.append(L.tube((0.0, -0.08, 0.85), (0.0, -0.30, 0.78), 0.03, "army_green", verts=6))            # носик
    p.append(L.tube((0.0, 0.0, 1.15), (0.40, 0.0, H - 0.06), 0.022, "steel_dark", verts=6))          # рычаг
    p.append(L.cyl(0.03, 0.10, (0.40, 0.0, H - 0.12), "wood", verts=6))
    p.append(L.cyl(0.25, 0.04, (0.0, -0.25, 0.39), "steel", verts=10))                                # поддон
    for i, (x, z) in enumerate(((-0.2, 0.15), (0.25, 0.25))):
        p.append(L.spot((x, -0.41, z), 0.12, "concrete_dark", seed=595 + i))
    p.append(L.spot((0.0, -0.09, 0.6), 0.05, "rust", seed=597, stretch=(0.6, 1.6)))
    return p


def skvazhina_s_elektronasosom():
    p = [L.cyl(0.42, 0.35, (0, 0, 0), "concrete", verts=12), L.cyl(0.38, 0.04, (0, 0, 0.35), "steel_dark", verts=12)]
    p.append(L.box((0.40, 0.35, 0.40), (0, 0, 0.39), "paint_blue", bevel=0.03))                       # кожух насоса
    for k in range(4):
        p.append(L.box((0.30, 0.004, 0.02), (0, -0.177, 0.48 + k * 0.06), "soot", bevel=0))
    p.append(L.tube((0.20, 0.0, 0.60), (0.35, 0.0, 0.60), 0.035, "steel", verts=8))                  # выход трубы
    p.append(L.tube((0.35, 0.0, 0.60), (0.35, 0.0, 1.00), 0.035, "steel", verts=8))
    p.append(L.cyl(0.04, 0.06, (0.35, -0.04, 0.92), "paint_red", verts=8, rot=(90, 0, 0)))           # кран
    p.append(L.box((0.22, 0.10, 0.28), (-0.20, 0.10, H - 0.28), "steel", bevel=0.01))                # щиток на стойке
    p.append(L.box((0.04, 0.04, H - 0.30), (-0.20, 0.18, 0.0), "steel_dark", bevel=0.006))
    p.append(L.box((0.08, 0.004, 0.07), (-0.20, 0.048, H - 0.12), "hazard_yellow", rot=(0, 45, 0), bevel=0))
    p.append(L.tube((-0.20, 0.10, H - 0.28), (-0.05, 0.0, 0.79), 0.01, "soot", verts=4))            # кабель
    p.append(L.spot((0.1, -0.176, 0.5), 0.08, "rust", seed=598))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz in (("ruchnoy_kolodets_s_vorotom", ruchnoy_kolodets_s_vorotom, (W * 100, H * 100)),
                        ("skvazhina_s_ruchnoy_pompoy", skvazhina_s_ruchnoy_pompoy, (W * 100, H * 100)),
                        ("skvazhina_s_elektronasosom", skvazhina_s_elektronasosom, (W * 100, H * 100))):
        L.make(fn, "resource", "well_hand", var, size_cm=sz)
    L.save_blend("resource", "well_hand")
