"""Двухъярусная койка `bunk_bed`. Размер — из плана ОС (200 × 180 см). Варианты (только idle):
  metallicheskaya — трубчатая рама (крашеная), сетки, полосатые матрасы, лестница спереди;
  derevyannaya    — брусья, доски, бортик наверху, лестница спереди.
(«Трёхъярусная» в плане — «позже», не делаем.) Запуск: python3 models/furniture/bunk_bed.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("bunk_bed"))
D = 0.90
Z1, Z2 = 0.30, 1.22          # верх рамы нижнего и верхнего яруса


def tier_bedding(p, z, seed, blanket, metal):
    mw, md = W - 0.14, D - 0.10
    if metal:
        n = 9
        for k in range(n):
            p.append(L.box((mw / n + 0.002, md, 0.10), (-mw / 2 + mw / n * (k + 0.5), 0, z),
                           "khaki_light" if k % 2 else "cloth_beige", bevel=0.02 if k in (0, n - 1) else 0.004))
    else:
        p.append(L.soft((mw, md, 0.11), (0, 0, z), "cloth_beige"))
    top = z + 0.10
    p.append(L.soft((0.40, md - 0.24, 0.11), (-(mw / 2 - 0.25), 0.03, top - 0.01), "offwhite", rot=(0, -5, 0)))
    p += L.blanket(mw * 0.12, mw * 0.66, md, top + 0.01, blanket, seed=seed, hang=(0.06, 0.12))


def ladder(p, x, color, r=None):
    """Лестница спереди, чуть наклонена (верх у верхнего яруса)."""
    y0, y1 = -(D / 2) - 0.10, -(D / 2) + 0.01
    for dx in (-0.17, 0.17):
        if r:
            p.append(L.tube((x + dx, y0, 0.0), (x + dx, y1, Z2 + 0.25), r, color, verts=8))
        else:
            p.append(L.tube((x + dx, y0, 0.0), (x + dx, y1, Z2 + 0.25), 0.025, color, verts=4))
    for k in range(5):
        t = (k + 1) / 6
        y, z = y0 + (y1 - y0) * t, (Z2 + 0.25) * t
        p.append(L.tube((x - 0.17, y, z), (x + 0.17, y, z), (r or 0.02) * 0.8, color, verts=6))


def metallicheskaya():
    p = []
    R, FR = 0.02, "steel_dark"
    xs = (-(W / 2 - 0.03), W / 2 - 0.03)
    for x in xs:
        for sy in (-1, 1):
            y = sy * (D / 2 - R)
            p.append(L.tube((x, y, 0), (x, y, H - 0.03), R, FR, verts=8))
            p.append(L.cyl(R * 1.5, 0.03, (x, y, 0), "soot", verts=8))
            p.append(L.cyl(R * 1.4, 0.03, (x, y, H - 0.03), "steel", verts=8))
        for z in (Z1 - 0.06, Z2 - 0.06, H - 0.08):
            p.append(L.tube((x, -(D / 2 - R), z), (x, D / 2 - R, z), R, FR, verts=8))
    for z in (Z1 - 0.06, Z2 - 0.06):
        for sy in (-1, 1):
            p.append(L.tube((xs[0], sy * (D / 2 - R), z), (xs[1], sy * (D / 2 - R), z), R, FR, verts=8))
        for k in range(12):
            x = -W / 2 + 0.12 + k * (W - 0.24) / 11
            p.append(L.tube((x, -(D / 2 - 0.03), z), (x, D / 2 - 0.03, z), 0.004, "steel", verts=4))
    # бортик верхнего яруса (передний, на половину длины)
    p.append(L.tube((xs[0], -(D / 2 - R), Z2 + 0.25), (0.15, -(D / 2 - R), Z2 + 0.25), R * 0.8, FR, verts=8))
    p.append(L.tube((0.15, -(D / 2 - R), Z2 - 0.06), (0.15, -(D / 2 - R), Z2 + 0.25), R * 0.8, FR, verts=8))
    tier_bedding(p, Z1 - 0.04, 41, "army_green", True)
    tier_bedding(p, Z2 - 0.04, 42, "cloth_blue", True)
    ladder(p, W / 2 - 0.40, FR, r=0.016)
    for i, (x, z) in enumerate(((-0.98, 0.9), (0.98, 1.5), (-0.4, Z2 - 0.06), (0.98, 0.2))):
        p.append(L.spot((x, -(D / 2) - 0.004, z), 0.035, "rust", seed=180 + i, stretch=(1.0, 1.4)))
    return p


def derevyannaya():
    p = []
    POST = 0.08
    xs = (-(W / 2 - POST / 2), W / 2 - POST / 2)
    for x in xs:
        for sy in (-1, 1):
            p.append(L.box((POST, POST, H), (x, sy * (D / 2 - POST / 2), 0), "wood_dark", bevel=0.01))
        for z in (Z1 + 0.02, Z2 + 0.02, H - 0.12):
            p.append(L.box((0.04, D - 0.08, 0.10), (x, 0, z), "wood", bevel=0.008))
    for z in (Z1 - 0.10, Z2 - 0.10):
        for sy in (-1, 1):
            p.append(L.box((W - 2 * POST, 0.04, 0.12), (0, sy * (D / 2 - 0.03), z), "wood", bevel=0.008))
    # бортик верхнего яруса: доска на половину длины + стойка
    p.append(L.box((W * 0.55, 0.035, 0.12), (-W * 0.225 + 0.0, -(D / 2 - 0.03), Z2 + 0.16), "wood_light", bevel=0.008))
    p.append(L.box((0.05, 0.04, 0.30), (W * 0.05 + 0.0, -(D / 2 - 0.03), Z2 + 0.0), "wood_dark", bevel=0.008))
    tier_bedding(p, Z1 + 0.02, 43, "khaki", False)
    tier_bedding(p, Z2 + 0.02, 44, "cloth_red", False)
    ladder(p, W / 2 - 0.40, "wood_light")
    for i, (x, z, c) in enumerate(((-0.6, Z1 - 0.04, "wood_light"), (0.4, Z2 - 0.05, "wood_dark"),
                                   (-0.96, 0.8, "wood_light"), (0.96, 1.4, "wood_light"))):
        p.append(L.spot((x, -(D / 2) - 0.012, z), 0.07, c, seed=190 + i, stretch=(1.5, 0.6)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("metallicheskaya", metallicheskaya), ("derevyannaya", derevyannaya)):
        L.make(fn, "furniture", "bunk_bed", var, size_cm=(W * 100, H * 100), limit="large", broken="legs")
    L.save_blend("furniture", "bunk_bed")
