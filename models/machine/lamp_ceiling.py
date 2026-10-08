"""Лампа потолочная `lamp_ceiling`, вариант `svetodiodnaya` (светодиодная плоская панель — как на референсе автора).
ОС: 30 × 25 см. Висит: origin в точке крепления (верх), лампа вниз.
Запуск: python3 models/machine/lamp_ceiling.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = 0.30, 0.25


def lamp_idle():
    p = []
    p.append(L.box((0.12, 0.08, 0.02), (0, 0, -0.02), "steel_dark", bevel=0.005))           # крепление
    for x in (-0.09, 0.09):                                                                 # подвесы
        p.append(L.box((0.008, 0.008, 0.13), (x, 0, -0.15), "soot", bevel=0))
    # корпус: трапеция (шире книзу), крышка
    p.append(L.poly([(-0.11, 0.0), (0.11, 0.0), (0.15, -0.07), (-0.15, -0.07)], 0.12, (0, 0, -0.15), "steel_dark"))
    p.append(L.box((0.22, 0.10, 0.012), (0, 0, -0.152), "steel", bevel=0.003))
    # рассеиватель — светится
    # рассеиватель — светится; выступает вперёд и вниз, чтобы был виден при взгляде сверху
    p.append(L.box((0.27, 0.13, 0.04), (0, -0.01, -0.25), "glow_lamp", glow=True, bevel=0.006))
    for x in (-0.14, 0.14):
        p.append(L.box((0.014, 0.14, 0.045), (x, -0.01, -0.252), "steel_dark", bevel=0.003))
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(lamp_idle, "machine", "lamp_ceiling", "svetodiodnaya", size_cm=(30, 25), limit="small")  # в ОС не ломается
    L.save_blend("machine", "lamp_ceiling")
