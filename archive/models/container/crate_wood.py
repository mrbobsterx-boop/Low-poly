"""Ящик `crate_wood`. ОС: 60 × 50 см. Варианты (только idle; «открытый/разграбленный», «разбитый» — пропуск):
  malyy — деревянный из досок с рамкой по углам и гвоздями;
  bolshoy — такой же, но крупнее: 90 × 70 см (глубина 60) — размер выбран сам (в ОС один размер на объект),
            плюс верёвочные ручки по бокам и трафарет;
  voennyy — военный зелёный с рёбрами, защёлками, ручками и трафаретом.
Запуск: python3 models/container/crate_wood.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 0.60, 0.45, 0.50


def crate_malyy():
    p = []
    n = 4
    hb = H - 0.02                                       # корпус; сверху крышка 2 см
    sh = hb / n
    for k in range(n):                                  # доски фасада (по высоте) — оттенки чередуются
        col = "wood_light" if k % 2 else "wood"
        p.append(L.box((W - 0.01, D - 0.01, sh - 0.008), (0, 0, k * sh + 0.004), col, bevel=0.007))
    p.append(L.box((W - 0.03, D - 0.03, hb - 0.02), (0, 0, 0.01), "soot", bevel=0))    # щели между досками
    # рамка-уголки
    for sx in (-1, 1):
        p.append(L.box((0.06, D + 0.008, hb), (sx * (W / 2 - 0.03), 0, 0), "wood_dark", bevel=0.008))
    for z in (0.0, hb - 0.05):
        p.append(L.box((W - 0.12, 0.02, 0.05), (0, -D / 2 - 0.006, z), "wood_dark", bevel=0.006))
    # гвозди
    for sx in (-1, 1):
        for z in (0.03, hb / 2, hb - 0.03):
            p.append(L.box((0.012, 0.004, 0.012), (sx * (W / 2 - 0.03), -D / 2 - 0.008, z), "steel_dark", bevel=0))
    # крышка (видна сверху)
    p.append(L.box((W - 0.004, D + 0.004, 0.02), (0, 0, hb), "wood", bevel=0.006))
    return p


def crate_bolshoy():
    global W, D, H
    old = W, D, H
    W, D, H = 0.86, 0.60, 0.70                          # корпус; верёвочные ручки добирают ширину до 90 см
    try:
        p = crate_malyy()
        for sx in (-1, 1):                              # верёвочные ручки на боковых брусках
            p.append(L.tube((sx * W / 2, -0.10, H * 0.62), (sx * (W / 2 + 0.02), 0.0, H * 0.58), 0.008, "cloth_beige", verts=4))
            p.append(L.tube((sx * (W / 2 + 0.02), 0.0, H * 0.58), (sx * W / 2, 0.10, H * 0.62), 0.008, "cloth_beige", verts=4))
        p.append(L.box((0.24, 0.004, 0.05), (0, -D / 2 - 0.004, H * 0.45), "soot", bevel=0))      # трафарет
        p.append(L.box((0.16, 0.004, 0.012), (0, -D / 2 - 0.004, H * 0.36), "soot", bevel=0))
        return p
    finally:
        W, D, H = old


def crate_voennyy():
    p = []
    body = "army_green"
    W = 0.56                                            # корпус уже: боковые ручки добирают до 60 см
    p.append(L.box((W, D, H - 0.08), (0, 0, 0.0), body, bevel=0.015))
    p.append(L.box((W + 0.012, D + 0.012, 0.09), (0, 0, H - 0.09), body, bevel=0.015))    # крышка
    p.append(L.box((W + 0.014, D + 0.014, 0.012), (0, 0, H - 0.095), "olive_dark", bevel=0.003))
    # рёбра жёсткости
    for x in (-0.20, 0.20):
        p.append(L.box((0.03, 0.012, H - 0.12), (x, -D / 2 - 0.006, 0.02), "olive_dark", bevel=0.004))
    # защёлки
    for x in (-0.13, 0.13):
        p.append(L.box((0.05, 0.016, 0.06), (x, -D / 2 - 0.012, H - 0.12), "steel", bevel=0.005))
        p.append(L.box((0.03, 0.01, 0.025), (x, -D / 2 - 0.022, H - 0.10), "steel_dark", bevel=0.003))
    # ручки по бокам
    for sx in (-1, 1):
        p.append(L.box((0.02, 0.14, 0.03), (sx * (W / 2 + 0.012), 0, H - 0.20), "soot", bevel=0.005))
    # трафарет: полосы и «номер»
    p.append(L.box((0.22, 0.004, 0.02), (0, -D / 2 - 0.004, 0.24), "offwhite", bevel=0))
    for i in range(4):
        p.append(L.box((0.025, 0.004, 0.04), (-0.06 + i * 0.04, -D / 2 - 0.004, 0.15), "offwhite", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(crate_malyy, "container", "crate_wood", "malyy", size_cm=(60, 50), broken="lid")
    L.make(crate_bolshoy, "container", "crate_wood", "bolshoy", size_cm=(90, 70), broken="lid")
    L.make(crate_voennyy, "container", "crate_wood", "voennyy", size_cm=(60, 50), broken="lid")
    L.save_blend("container", "crate_wood")
