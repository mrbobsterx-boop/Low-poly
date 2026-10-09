"""Дождесборник `rain_collector`. Размер — из плана ОС (110 × 60 см). Варианты (только idle):
  plenka_i_zhelob   — плёнка (брезент) на раме воронкой + жёлоб и шланг вниз;
  kryshnaya_voronka — жестяная воронка-раструб с сеткой и трубой;
  bolshaya_ploschadka — широкий поддон-площадка из листа на ножках со сливом.
Воду собирает в бочку (отдельный объект). Запуск: python3 models/machine/rain_collector.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("rain_collector"))


def plenka_i_zhelob():
    p = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.box((0.04, 0.04, H), (sx * (W / 2 - 0.03), sy * 0.30, 0), "wood_dark", bevel=0.006))
    for sy in (-1, 1):
        p.append(L.box((W, 0.04, 0.04), (0, sy * 0.30, H - 0.04), "wood", bevel=0.006))
    # плёнка: провисает к центру (воронка)
    import math
    p.append(L.sheet(8, 5, W - 0.06, 0.62, (0, 0, H - 0.02), "khaki_light",
                     z_fn=lambda u, v: -0.18 * math.sin(u * math.pi) * math.sin(v * math.pi), jitter=0.01, seed=600))
    p.append(L.cyl(0.04, 0.10, (0, 0, H - 0.28), "soot", verts=8))                                    # слив
    p.append(L.tube((0, 0, H - 0.28), (0.25, -0.15, 0.05), 0.022, "plant_dark", verts=6))            # шланг
    return p


def kryshnaya_voronka():
    p = [L.cyl(0.08, 0.15, (0, 0, H - 0.40), "steel", verts=10, radius_top=W / 2 - 0.02)]           # раструб
    p.append(L.cyl(W / 2 - 0.02, 0.25, (0, 0, H - 0.25), "steel", verts=10, radius_top=W / 2))
    p.append(L.cyl(W / 2 - 0.03, 0.006, (0, 0, H - 0.01), "steel_dark", verts=10))                   # сетка
    for k in range(5):
        p.append(L.box((W - 0.12, 0.006, 0.006), (0, -0.20 + k * 0.10, H - 0.004), "soot", bevel=0))
    p.append(L.cyl(0.06, H - 0.40, (0, 0, 0), "steel_light", verts=8))                               # труба вниз
    p.append(L.cyl(0.075, 0.04, (0, 0, 0.10), "steel_dark", verts=8))
    for sx in (-1, 1):                                                                 # растяжки-держатели
        p.append(L.tube((sx * 0.08, 0, H - 0.38), (sx * (W / 2 - 0.05), 0, 0.0), 0.012, "steel_dark", verts=4))
    for i, (x, z) in enumerate(((-0.25, H - 0.15), (0.2, H - 0.10))):
        p.append(L.spot((x, -(W / 2 - 0.03), z), 0.08, "rust", seed=605 + i, stretch=(0.7, 1.5)))
    return p


def bolshaya_ploschadka():
    p = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.box((0.04, 0.04, H - 0.10), (sx * (W / 2 - 0.05), sy * 0.35, 0), "steel_dark", bevel=0.006))
    p.append(L.box((W, 0.80, 0.03), (0, 0, H - 0.10), "steel", bevel=0.006))                         # лист
    for sx in (-1, 1):
        p.append(L.box((0.03, 0.80, 0.10), (sx * (W / 2 - 0.015), 0, H - 0.10), "steel", bevel=0.006))
    p.append(L.box((W, 0.03, 0.10), (0, 0.385, H - 0.10), "steel", bevel=0.006))
    p.append(L.box((W, 0.03, 0.05), (0, -0.385, H - 0.10), "steel", bevel=0.006))                   # передний борт ниже
    for k in range(6):                                                                 # гофры
        p.append(L.box((0.03, 0.78, 0.008), (-0.45 + k * 0.18, 0, H - 0.07), "steel_light", bevel=0))
    p.append(L.tube((0.45, -0.38, H - 0.08), (0.52, -0.42, 0.10), 0.03, "steel_light", verts=6))     # слив
    for i, (x, s) in enumerate(((-0.3, 0.15), (0.2, 0.12))):
        p.append(L.spot((x, 0.0, H - 0.069), s, "rust", facing="top", seed=610 + i, stretch=(1.6, 0.7)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("plenka_i_zhelob", plenka_i_zhelob), ("kryshnaya_voronka", kryshnaya_voronka),
                    ("bolshaya_ploschadka", bolshaya_ploschadka)):
        L.make(fn, "machine", "rain_collector", var, size_cm=(W * 100, H * 100))
    L.save_blend("machine", "rain_collector")
