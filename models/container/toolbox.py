"""Ящик с инструментами `toolbox`, вариант `metallicheskiy`. ОС: 40 × 25 см. Красный, как на референсе автора.
Запуск: python3 models/container/toolbox.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 0.40, 0.20, 0.25


def toolbox_idle():
    p = []
    p.append(L.box((W, D, 0.12), (0, 0, 0), "paint_red", bevel=0.01))
    p.append(L.box((W + 0.008, D + 0.008, 0.06), (0, 0, 0.12), "paint_red", bevel=0.012))           # крышка
    p.append(L.box((W - 0.04, D - 0.06, 0.012), (0, 0, 0.18), "paint_red", bevel=0.005))            # ступенька
    p.append(L.box((W + 0.01, D + 0.01, 0.008), (0, 0, 0.118), "rust_dark", bevel=0))                # шов
    for x in (-0.13, 0.13):                                                                         # защёлки
        p.append(L.box((0.04, 0.012, 0.05), (x, -D / 2 - 0.006, 0.09), "steel_light", bevel=0.004))
    # ручка: две стойки + перекладина
    for x in (-0.09, 0.09):
        p.append(L.box((0.016, 0.03, 0.05), (x, 0, 0.19), "steel_dark", bevel=0.004))
    p.append(L.box((0.20, 0.03, 0.02), (0, 0, H - 0.02), "soot", bevel=0.006))
    # сколы краски
    p.append(L.box((0.03, 0.003, 0.012), (0.15, -D / 2 - 0.002, 0.03), "steel", bevel=0))
    p.append(L.box((0.02, 0.003, 0.01), (-0.16, -D / 2 - 0.006, 0.15), "steel", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(toolbox_idle(), "container", "toolbox", "metallicheskiy", "idle", size_cm=(40, 25), limit="small")
    L.save_blend("container", "toolbox")
