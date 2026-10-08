"""Генератор-беговая дорожка `treadmill_generator`. Размер — из плана ОС (160 × 120 см). Вариант (только idle):
  begovaya_dorozhka — полотно на раме, поручни, стойка с панелью, генератор на валу. Запуск: python3 models/machine/treadmill_generator.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("treadmill_generator"))


def begovaya_dorozhka():
    p = [L.box((W - 0.10, 0.70, 0.12), (-0.05, 0, 0.04), "steel_dark", bevel=0.02)]                   # рама
    p.append(L.box((W - 0.25, 0.50, 0.02), (-0.08, 0, 0.16), "soot", bevel=0.004))                     # полотно
    for k in range(10):
        p.append(L.box((0.01, 0.50, 0.004), (-0.70 + k * 0.14, 0, 0.18), "stone_dark", bevel=0))
    for x in (-W / 2 + 0.08, W / 2 - 0.30):
        for sy in (-1, 1):
            p.append(L.box((0.06, 0.06, 0.04), (x, sy * 0.30, 0), "soot", bevel=0.006))
    for sy in (-1, 1):                                                                 # стойки и поручни
        p.append(L.tube((W / 2 - 0.25, sy * 0.33, 0.16), (W / 2 - 0.20, sy * 0.33, H - 0.10), 0.03, "steel", verts=6))
        p.append(L.tube((W / 2 - 0.20, sy * 0.33, 0.95), (0.05, sy * 0.33, 0.95), 0.022, "steel", verts=6))
    p.append(L.box((0.25, 0.70, 0.20), (W / 2 - 0.20, 0, H - 0.20), "steel_dark", bevel=0.02))          # панель
    p.append(L.box((0.16, 0.006, 0.08), (W / 2 - 0.20, -0.353, H - 0.12), "glow_screen", glow=True, bevel=0))
    p.append(L.cyl(0.09, 0.20, (-W / 2 + 0.03, 0, 0.12), "army_green", verts=10, rot=(90, 0, 0)))      # генератор
    p.append(L.box((0.10, 0.006, 0.10), (-W / 2 + 0.03, -0.106, 0.12), "hazard_yellow", rot=(0, 45, 0), bevel=0))
    p.append(L.tube((-W / 2 + 0.03, -0.1, 0.05), (-W / 2 + 0.25, -0.3, 0.0), 0.008, "soot", verts=4))
    p.append(L.spot((-0.3, -0.35, 0.10), 0.12, "rust", seed=720, stretch=(1.4, 0.6)))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(begovaya_dorozhka, "machine", "treadmill_generator", "begovaya_dorozhka", size_cm=(W * 100, H * 100), broken="tilt")
    L.save_blend("machine", "treadmill_generator")
