"""Фитолампа `grow_lamp`. Размер — из плана ОС (80 × 15 см). Висит: origin в точке крепления (верх).
Варианты (только idle): fioletovaya_led — светодиодная панель с фиолетовым свечением; lyuminestsentnaya — две трубки
в отражателе; slabaya — одна лампочка в жестяном отражателе. Запуск: python3 models/machine/grow_lamp.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("grow_lamp"))
ROUGH = {"min_area": 0.01, "k": 0.03, "amp_max": 0.004}


def hang(p, xs, h=0.07):
    for x in xs:
        p.append(L.tube((x, 0, 0), (x, 0, -h), 0.003, "steel_dark", verts=4))


def fioletovaya_led():
    p = []
    hang(p, (-0.30, 0.30))
    p.append(L.box((W, 0.20, 0.05), (0, 0, -0.12), "soot", bevel=0.01))
    for k in range(4):
        p.append(L.box((0.006, 0.20, 0.03), (-0.30 + k * 0.2, 0, -0.10), "stone_dark", bevel=0))     # рёбра радиатора
    p.append(L.box((W - 0.06, 0.16, 0.012), (0, -0.01, -H), "glow_grow", glow=True, bevel=0.003))
    for k in range(8):
        p.append(L.box((0.03, 0.004, 0.012), (-0.35 + k * 0.1, -0.101, -0.135), "glow_grow", glow=True, bevel=0))
    return p


def lyuminestsentnaya():
    p = []
    hang(p, (-0.32, 0.32))
    p.append(L.box((W, 0.18, 0.02), (0, 0, -0.09), "steel", bevel=0.005))
    for sy in (-1, 1):
        p.append(L.box((W, 0.02, 0.05), (0, sy * 0.08, -0.13), "steel", rot=(sy * 25, 0, 0), bevel=0.004))
    for y in (-0.03, 0.03):
        p.append(L.cyl(0.016, W - 0.10, (-(W - 0.10) / 2, y - 0.02, -0.12), "glow_lamp", verts=6, rot=(0, 90, 0), glow=True))
    for sx in (-1, 1):
        p.append(L.box((0.03, 0.12, 0.04), (sx * (W / 2 - 0.03), -0.01, -0.14), "soot", bevel=0.004))
    return p


def slabaya():
    p = []
    hang(p, (0.0,), 0.04)
    p.append(L.cyl(0.03, 0.03, (0, 0, -0.07), "soot", verts=8))
    p.append(L.cyl(0.22, 0.05, (0, 0, -0.12), "steel", verts=10, radius_top=0.04))
    p.append(L.cyl(0.03, 0.03, (0, 0, -H), "glow_lamp", verts=8, glow=True))
    p.append(L.spot((0.08, -0.15, -0.10), 0.05, "rust", seed=750))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz in (("fioletovaya_led", fioletovaya_led, (W * 100, H * 100)), ("lyuminestsentnaya", lyuminestsentnaya, (W * 100, H * 100)),
                        ("slabaya", slabaya, None)):
        L.make(fn, "machine", "grow_lamp", var, size_cm=sz, limit="small", rough=ROUGH)
    L.save_blend("machine", "grow_lamp")
