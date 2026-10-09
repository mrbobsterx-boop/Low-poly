"""Холодильник `fridge`. Размер — из плана ОС (70 × 180 см). Варианты (только idle):
  elektricheskiy — старый белый двухкамерный, ручки, решётка, ржавые края;
  yaschik_so_ldom — деревянный ледник-ящик с металлической обивкой (ниже по природе — отклонение);
  morozilnaya_kamera — морозильный ларь с крышкой (ниже — отклонение). Запуск: python3 models/machine/fridge.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("fridge"))
D = 0.65
F = -D / 2


def elektricheskiy():
    p = [L.box((W, D, H - 0.06), (0, 0, 0.06), "plastic_white", bevel=0.05)]
    p.append(L.box((W - 0.06, D - 0.06, 0.06), (0, 0.02, 0), "soot", bevel=0.01))
    p.append(L.box((W - 0.02, 0.01, 0.006), (0, F - 0.002, 1.20), "stone_dark", bevel=0))           # шов дверей
    for z0, z1 in ((0.10, 1.18), (1.22, H - 0.04)):
        p.append(L.box((W - 0.04, 0.02, z1 - z0), (0, F - 0.008, z0), "plastic_white", bevel=0.02))
    for z in (0.95, 1.30):
        p.append(L.box((0.03, 0.04, 0.20), (W / 2 - 0.07, F - 0.04, z), "steel_light", bevel=0.008))
    p.append(L.box((0.20, 0.006, 0.05), (-0.12, F - 0.02, 1.08), "steel", bevel=0))                  # шильдик
    for i, (x, z, s) in enumerate(((-0.30, 0.15, 0.08), (0.28, 0.40, 0.06), (-0.10, 1.25, 0.05), (0.30, H - 0.10, 0.07))):
        p.append(L.spot((x, F - 0.019, z), s, "rust", seed=740 + i, stretch=(1.0, 1.3)))
    p.append(L.box((0.12, 0.004, 0.12), (-0.15, F - 0.019, 1.45), "paint_red", rot=(0, 10, 0), bevel=0))   # магнит-записка
    p.append(L.box((0.09, 0.004, 0.11), (0.05, F - 0.019, 1.50), "offwhite", rot=(0, -6, 0), bevel=0))
    return p


def yaschik_so_ldom():
    p = [L.box((W, 0.55, 0.85), (0, 0, 0.10), "wood", bevel=0.015)]
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.box((0.05, 0.05, 0.10), (sx * (W / 2 - 0.05), sy * 0.22, 0), "wood_dark", bevel=0.006))
    for z in (0.12, 0.92):
        p.append(L.box((W + 0.006, 0.556, 0.03), (0, 0, z), "steel", bevel=0.004))                    # обивка
    p.append(L.box((W - 0.08, 0.02, 0.60), (0, -0.285, 0.22), "wood_light", bevel=0.01))              # дверца
    p.append(L.box((0.10, 0.03, 0.04), (0.20, -0.30, 0.55), "steel_light", bevel=0.006))
    for z in (0.30, 0.70):
        p.append(L.box((0.06, 0.02, 0.06), (-0.28, -0.30, z), "steel_dark", bevel=0.004))             # петли
    p.append(L.spot((0.05, -0.296, 0.35), 0.10, "wood_dark", seed=748, stretch=(0.8, 1.3)))
    return p


def morozilnaya_kamera():
    p = [L.box((W + 0.30, 0.65, 0.80), (0, 0, 0.05), "plastic_white", bevel=0.04)]
    p.append(L.box((W + 0.30, 0.67, 0.08), (0, 0, 0.85), "offwhite", bevel=0.03))                     # крышка
    p.append(L.box((0.25, 0.04, 0.03), (0, -0.345, 0.84), "steel_light", bevel=0.008))
    for k in range(6):
        p.append(L.box((0.008, 0.006, 0.18), (-0.38 + k * 0.03, -0.326, 0.10), "stone_dark", bevel=0))  # решётка
    p.append(L.box((W + 0.26, 0.6, 0.05), (0, 0, 0.0), "soot", bevel=0.006))
    p.append(L.box((0.03, 0.006, 0.02), (0.30, -0.326, 0.70), "glow_screen", glow=True, bevel=0))
    p.append(L.spot((0.2, -0.326, 0.25), 0.10, "rust", seed=749))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz in (("elektricheskiy", elektricheskiy, (W * 100, H * 100)), ("yaschik_so_ldom", yaschik_so_ldom, None),
                        ("morozilnaya_kamera", morozilnaya_kamera, None)):
        L.make(fn, "machine", "fridge", var, size_cm=sz, broken="door")
    L.save_blend("machine", "fridge")
