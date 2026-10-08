"""Лампа потолочная `lamp_ceiling`, вариант `nakalivaniya_plafon_zelenyy`. ОС: 30 × 25 см, висит под потолком.
Origin — в точке крепления (верх по центру), лампа — вниз от неё. Сломанного вида в ОС нет.
Образец: docs/ref/machine/lamp_ceiling.png
Запуск: python3 models/machine/lamp_ceiling.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = 0.30, 0.25


def lamp_idle():
    p = []
    p.append(L.cyl(0.06, 0.02, (0, 0, -0.02), "steel_dark", verts=8))                    # чашка у потолка
    p.append(L.cyl(0.008, 0.10, (0, 0, -0.12), "steel_dark", verts=6))                   # трубка
    p.append(L.cyl(0.03, 0.03, (0, 0, -0.14), "steel", verts=8))                         # патрон
    # плафон: конус зелёный снаружи, светлый внутри
    p.append(L.cyl(W / 2, 0.08, (0, 0, -0.22), "plant_dark", verts=10, radius_top=0.04))
    p.append(L.cyl(W / 2 - 0.01, 0.005, (0, 0, -0.222), "offwhite", verts=10))           # обод изнутри
    p.append(L.cyl(0.035, 0.035, (0, 0, -0.25), "glow_lamp", verts=8, glow=True))        # лампочка
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(lamp_idle(), "machine", "lamp_ceiling", "nakalivaniya_plafon_zelenyy", "idle", size_cm=(30, 25),
             limit="small")
    L.save_blend("machine", "lamp_ceiling")
