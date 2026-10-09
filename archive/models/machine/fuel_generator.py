"""Топливный генератор `fuel_generator`. Размер — из плана ОС (70 × 60 см). Варианты (только idle):
  portativnyy — красный в трубчатой раме, бак сверху, розетки, панель; statsionarnyy — в кожухе на салазках, глушитель;
  promyshlennyy — дизель в шумозащитном кожухе с жалюзи, дверцей, щитом. Запуск: python3 models/machine/fuel_generator.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("fuel_generator"))
D = 0.45


def panel(p, x, z, y):
    p.append(L.box((0.22, 0.012, 0.16), (x, y, z), "soot", bevel=0.005))
    for k, c in enumerate(("offwhite", "offwhite", "paint_red")):
        p.append(L.box((0.045, 0.006, 0.05), (x - 0.07 + k * 0.07, y - 0.008, z + 0.03), c, bevel=0.003))
    p.append(L.cyl(0.025, 0.006, (x + 0.05, y - 0.008, z + 0.12), "offwhite", verts=10, rot=(90, 0, 0)))  # вольтметр


def portativnyy():
    p = []
    for sx in (-1, 1):                                                                 # рама
        for sy in (-1, 1):
            p.append(L.tube((sx * (W / 2 - 0.02), sy * (D / 2 - 0.02), 0), (sx * (W / 2 - 0.02), sy * (D / 2 - 0.02), H - 0.04), 0.016, "soot", verts=6))
        p.append(L.tube((sx * (W / 2 - 0.02), -(D / 2 - 0.02), H - 0.04), (sx * (W / 2 - 0.02), D / 2 - 0.02, H - 0.04), 0.016, "soot", verts=6))
    for sy in (-1, 1):
        p.append(L.tube((-(W / 2 - 0.02), sy * (D / 2 - 0.02), H - 0.04), (W / 2 - 0.02, sy * (D / 2 - 0.02), H - 0.04), 0.016, "soot", verts=6))
    p.append(L.box((0.34, 0.32, 0.26), (-0.10, 0, 0.04), "steel_dark", bevel=0.02))                   # двигатель
    p.append(L.box((W - 0.12, D - 0.10, 0.16), (0, 0, H - 0.22), "paint_red", bevel=0.04))            # бак
    p.append(L.cyl(0.04, 0.03, (-0.15, 0, H - 0.06), "soot", verts=8))
    p.append(L.box((0.24, 0.30, 0.22), (0.18, 0, 0.06), "paint_red", bevel=0.02))                    # генератор
    panel(p, 0.18, 0.10, -0.16)
    p.append(L.cyl(0.05, 0.12, (-0.25, -0.12, 0.20), "steel", verts=8, rot=(0, 90, 0)))              # глушитель
    p.append(L.box((0.10, 0.004, 0.03), (0, -D / 2 + 0.05 - 0.004, H - 0.12), "offwhite", bevel=0))
    return p


def statsionarnyy():
    p = [L.box((W, D, 0.05), (0, 0, 0), "steel_dark", bevel=0.01)]
    p.append(L.box((W - 0.04, D - 0.04, H - 0.18), (0, 0, 0.05), "army_green", bevel=0.03))
    for k in range(5):
        p.append(L.box((0.20, 0.006, 0.015), (-0.18, -(D / 2) + 0.018, 0.15 + k * 0.05), "olive_dark", bevel=0))
    panel(p, 0.17, 0.20, -(D / 2) + 0.018)
    p.append(L.cyl(0.04, 0.16, (W / 2 - 0.10, 0.10, H - 0.16), "steel", verts=8))                     # выхлоп
    p.append(L.cyl(0.05, 0.03, (W / 2 - 0.10, 0.10, H - 0.03), "soot", verts=8))
    p.append(L.box((0.10, 0.004, 0.10), (0.17, -(D / 2) + 0.016, 0.40), "hazard_yellow", rot=(0, 45, 0), bevel=0))
    for i, (x, z) in enumerate(((-0.25, 0.10), (0.25, 0.42))):
        p.append(L.spot((x, -(D / 2) + 0.019, z), 0.06, "rust", seed=730 + i))
    return p


def promyshlennyy():
    p = [L.box((W, D, H - 0.03), (0, 0, 0.03), "hazard_yellow", bevel=0.02)]
    p.append(L.box((W - 0.02, D - 0.02, 0.03), (0, 0, 0), "soot", bevel=0.006))
    for k in range(6):                                                                 # жалюзи
        p.append(L.box((0.24, 0.012, 0.015), (0.18, -(D / 2) - 0.004, 0.12 + k * 0.045), "soot", rot=(-30, 0, 0), bevel=0))
    p.append(L.box((0.30, 0.012, 0.42), (-0.15, -(D / 2) - 0.003, 0.08), "hazard_yellow", bevel=0.006))  # дверца
    p.append(L.box((0.02, 0.02, 0.08), (-0.03, -(D / 2) - 0.012, 0.28), "soot", bevel=0.004))
    panel(p, -0.15, 0.30, -(D / 2) - 0.008)
    for x in (-0.28, 0.28):
        p.append(L.box((0.04, 0.004, 0.04), (x, -(D / 2) - 0.004, H - 0.06), "soot", bevel=0))
    p.append(L.box((0.20, 0.004, 0.04), (0.18, -(D / 2) - 0.005, 0.46), "soot", bevel=0))           # трафарет
    for i, (x, z) in enumerate(((0.3, 0.06), (-0.3, 0.5), (0.0, 0.03))):
        p.append(L.spot((x, -(D / 2) - 0.004, z), 0.08, "rust" if i else "soot", seed=735 + i, stretch=(1.3, 0.7)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("portativnyy", portativnyy), ("statsionarnyy", statsionarnyy), ("promyshlennyy", promyshlennyy)):
        L.make(fn, "machine", "fuel_generator", var, size_cm=(W * 100, H * 100), broken="tilt")
    L.save_blend("machine", "fuel_generator")
