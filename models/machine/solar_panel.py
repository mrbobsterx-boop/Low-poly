"""Солнечная панель `solar_panel`. Размер — из плана ОС (120 × 80 см). Панель наклонена к камере (видна сверху).
Варианты (только idle): malaya_100_vt — небольшая панель на подставке; bolshaya_300_vt — большая на раме-опоре;
skladnaya_portativnaya — складная из трёх секций на ножках, с кабелем. Ячейки — тёмно-синие с сеткой.
Запуск: python3 models/machine/solar_panel.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("solar_panel"))
TILT = 35


def panel(p, w, d, center, cols, rows, tilt=TILT):
    """Панель w × d, центр, наклон (поверхность к камере и вверх)."""
    cx, cy, cz = center
    parts = [L.box((w, d, 0.03), (0, 0, -0.015), "steel_light", bevel=0.006)]
    parts.append(L.box((w - 0.03, d - 0.03, 0.004), (0, 0, 0.015), "cloth_blue", bevel=0))
    cw, ch = (w - 0.03) / cols, (d - 0.03) / rows
    for i in range(1, cols):
        parts.append(L.box((0.004, d - 0.03, 0.003), (-(w - 0.03) / 2 + i * cw, 0, 0.019), "steel", bevel=0))
    for j in range(1, rows):
        parts.append(L.box((w - 0.03, 0.004, 0.003), (0, -(d - 0.03) / 2 + j * ch, 0.019), "steel", bevel=0))
    L.transform(parts, (cx, cy, cz), ((90 - tilt), 0, 0))     # ячейки — к камере и вверх
    p += parts


def malaya_100_vt():
    p = []
    panel(p, 0.70, 0.50, (0, 0.05, 0.40), 4, 3)
    p.append(L.tube((0, 0.12, 0.30), (0, 0.18, 0.0), 0.02, "steel_dark", verts=6))
    p.append(L.tube((-0.25, 0.0, 0.0), (0.25, 0.0, 0.0), 0.02, "steel_dark", verts=6))
    p.append(L.tube((0, -0.05, 0.0), (0, 0.25, 0.0), 0.02, "steel_dark", verts=6))
    p.append(L.box((0.10, 0.04, 0.06), (0.25, 0.10, 0.25), "soot", bevel=0.006))                    # контроллер
    return p


def bolshaya_300_vt():
    p = []
    panel(p, W, 0.90, (0, 0.10, 0.45), 6, 4)
    for sx in (-1, 1):
        p.append(L.tube((sx * (W / 2 - 0.10), -0.20, 0.0), (sx * (W / 2 - 0.10), -0.15, 0.12), 0.025, "steel_dark", verts=6))
        p.append(L.tube((sx * (W / 2 - 0.10), 0.40, 0.0), (sx * (W / 2 - 0.10), 0.35, 0.70), 0.025, "steel_dark", verts=6))
        p.append(L.tube((sx * (W / 2 - 0.10), -0.20, 0.0), (sx * (W / 2 - 0.10), 0.40, 0.0), 0.02, "steel_dark", verts=6))
    p.append(L.box((0.12, 0.05, 0.08), (W / 2 - 0.25, 0.30, 0.40), "soot", bevel=0.006))
    for i, (x, y) in enumerate(((-0.3, 0.0), (0.35, 0.2))):
        p.append(L.spot((x, y - 0.25, 0.30), 0.12, "dirt", facing="front", seed=710 + i, stretch=(1.4, 0.6)))
    return p


def skladnaya_portativnaya():
    p = []
    for k, ang in enumerate((-12, 0, 12)):
        parts = []
        panel(parts, 0.36, 0.55, (0, 0, 0), 2, 3)
        L.transform(parts, (-0.38 + k * 0.38, 0.05, 0.36), (0, 0, ang))
        p += parts
    for x in (-0.50, 0.50):
        p.append(L.tube((x, 0.2, 0.36), (x, 0.32, 0.0), 0.012, "steel", verts=4))                    # ножки-подпорки
    p.append(L.box((0.10, 0.03, 0.05), (0.0, 0.12, 0.10), "soot", bevel=0.006))
    p.append(L.tube((0.0, 0.12, 0.10), (0.35, -0.15, 0.01), 0.008, "soot", verts=4))
    p.append(L.box((0.12, 0.04, 0.04), (0.42, -0.18, 0.0), "paint_red", bevel=0.006))                 # разъём
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn, sz in (("malaya_100_vt", malaya_100_vt, None), ("bolshaya_300_vt", bolshaya_300_vt, (W * 100, H * 100)),
                        ("skladnaya_portativnaya", skladnaya_portativnaya, None)):
        L.make(fn, "machine", "solar_panel", var, size_cm=sz, broken="tilt")
    L.save_blend("machine", "solar_panel")
