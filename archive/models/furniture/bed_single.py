"""Кровать `bed_single`. Размер — из плана ОС (200 × 60 см). Варианты (план ОС, только idle):
  zheleznaya_koyka         — железная койка: трубчатая рама с прутьями, полосатый матрас, шерстяное одеяло;
  derevyannaya_samodelnaya — деревянная самодельная: рама, спинка с планками, мятое одеяло из граней;
  nizkaya                  — низкая: матрас на подставке из поддона;
  krovat_s_tumboy          — кровать с тумбой: деревянная кровать + тумбочка у изголовья (вместе 200 см).
Стиль — docs/STYLE.md, референс docs/ref/style. Запуск: python3 models/furniture/bed_single.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("bed_single"))
D = 0.90


def wooden(w, x0=0.0, seed=7, blanket="cloth_blue"):
    """Деревянная кровать шириной w с центром x0 (спинка слева)."""
    POST, RAIL_Z, MAT_Z, MAT_H = 0.07, 0.20, 0.30, 0.12
    p = []
    for sx, h in ((-1, H), (1, 0.48)):
        for sy in (-1, 1):
            x = x0 + sx * (w / 2 - POST / 2)
            p.append(L.box((POST, POST, h), (x, sy * (D / 2 - POST / 2), 0), "wood_dark", bevel=0.01))
            p.append(L.box((POST + 0.012, POST + 0.012, 0.025), (x, sy * (D / 2 - POST / 2), h - 0.025), "wood", bevel=0.006))
    xh = x0 - (w / 2 - POST / 2)
    p.append(L.box((0.045, D - 0.08, 0.08), (xh, 0, H - 0.12), "wood", bevel=0.008))
    p.append(L.box((0.04, D - 0.08, 0.06), (xh, 0, MAT_Z), "wood_dark", bevel=0.006))
    for y in (-0.25, -0.085, 0.085, 0.25):
        p.append(L.box((0.03, 0.06, H - 0.12 - MAT_Z - 0.06), (xh, y, MAT_Z + 0.06), "wood", bevel=0.005))
    p.append(L.box((0.045, D - 0.08, 0.14), (x0 + w / 2 - POST / 2, 0, MAT_Z - 0.04), "wood", bevel=0.008))
    for sy in (-1, 1):
        p.append(L.box((w - 2 * POST, 0.035, MAT_Z - RAIL_Z), (x0, sy * (D / 2 - 0.03), RAIL_Z), "wood", bevel=0.008))
    mw, md = w - 2 * POST - 0.02, D - 0.10
    p.append(L.box((mw, md, MAT_H), (x0, 0, MAT_Z), "cloth_beige", bevel=0.03))
    p.append(L.box((mw + 0.004, md + 0.004, 0.018), (x0, 0, MAT_Z + 0.03), "offwhite", bevel=0.006))
    p.append(L.box((0.45, md - 0.20, 0.13), (x0 - (mw / 2 - 0.27), 0.02, MAT_Z + MAT_H - 0.01), "offwhite",
                   rot=(0, -4, 0), bevel=0.04))
    p += L.blanket(x0 + mw * 0.12, mw * 0.68, md, MAT_Z + MAT_H + 0.02, blanket, seed=seed)
    yr = -(D / 2 - 0.03) - 0.018
    for i, (dx, z, s, c) in enumerate(((-0.55, 0.26, 0.10, "wood_light"), (0.35, 0.24, 0.08, "wood_dark"),
                                       (0.70, 0.27, 0.06, "wood_light"), (-w / 2 + 0.035, 0.45, 0.04, "wood_light"))):
        p.append(L.spot((x0 + dx * w / 2, yr, z), s, c, seed=90 + i + seed, stretch=(1.6, 0.6)))
    p.append(L.spot((x0 - mw * 0.30, -(md / 2) - 0.002, MAT_Z + 0.06), 0.09, "khaki_light", seed=99, stretch=(1.3, 0.7)))
    return p


def derevyannaya_samodelnaya():
    return wooden(W)


def zheleznaya_koyka():
    """Железная койка: рама из труб (крашеная, со сколами до металла), спинки с прутьями, сетка, полосатый матрас,
    подушка, сложенное шерстяное одеяло в ногах."""
    p = []
    R = 0.017
    FR, MAT_Z = "army_green", 0.34
    xs = (-(W / 2 - R * 1.5), W / 2 - R * 1.5)
    for x, h in zip(xs, (H, H - 0.08)):
        for sy in (-1, 1):
            y = sy * (D / 2 - R)
            p.append(L.tube((x, y, 0.0), (x, y, h - 0.03), R, FR, verts=8))
            p.append(L.cyl(R * 1.6, 0.03, (x, y, 0), "soot", verts=8))                       # резиновые пятки
            p.append(L.cyl(R * 1.4, 0.03, (x, y, h - 0.03), "steel", verts=8))             # колпачки
        p.append(L.tube((x, -(D / 2 - R), h - 0.04), (x, D / 2 - R, h - 0.04), R, FR, verts=8))
        p.append(L.tube((x, -(D / 2 - R), MAT_Z - 0.04), (x, D / 2 - R, MAT_Z - 0.04), R, FR, verts=8))
        for k in range(6):
            y = -(D / 2 - 0.12) + k * (D - 0.24) / 5
            p.append(L.tube((x, y, MAT_Z - 0.04), (x, y, h - 0.04), 0.008, FR, verts=6))
    for sy in (-1, 1):                                                                      # боковые трубы рамы
        p.append(L.tube((xs[0], sy * (D / 2 - R), MAT_Z - 0.06), (xs[1], sy * (D / 2 - R), MAT_Z - 0.06), R, FR, verts=8))
    for k in range(12):                                                                     # пружинная сетка
        x = -W / 2 + 0.12 + k * (W - 0.24) / 11
        p.append(L.tube((x, -(D / 2 - 0.03), MAT_Z - 0.06), (x, D / 2 - 0.03, MAT_Z - 0.06), 0.004, "steel_dark", verts=4))
    # матрас: полосы хаки
    mw, md, mh = W - 0.10, D - 0.08, 0.11
    n = 9
    for k in range(n):
        p.append(L.box((mw / n + 0.002, md, mh), (-mw / 2 + mw / n * (k + 0.5), 0, MAT_Z - 0.04),
                       "khaki_light" if k % 2 else "cloth_beige", bevel=0.02 if k in (0, n - 1) else 0.004))
    top = MAT_Z - 0.04 + mh
    p.append(L.soft((0.42, md - 0.22, 0.12), (-(mw / 2 - 0.26), 0.03, top - 0.01), "offwhite", rot=(0, -5, 0)))
    p.append(L.soft((0.46, md - 0.06, 0.10), (mw / 2 - 0.30, 0.0, top - 0.005), "army_green"))       # одеяло сложено
    p.append(L.box((0.462, md - 0.055, 0.015), (mw / 2 - 0.30, 0.0, top + 0.04), "olive_dark", bevel=0.004))
    # износ: сколы краски до металла, ржавчина у пяток, пятно на матрасе
    for i, (x, z, s) in enumerate(((-0.99, 0.48, 0.03), (-0.99, 0.12, 0.025), (0.98, 0.30, 0.03), (0.40, 0.28, 0.035),
                                   (-0.30, 0.28, 0.03))):
        p.append(L.spot((x, -(D / 2) - 0.002, z), s, "steel", seed=140 + i))
    for i, x in enumerate(xs):
        p.append(L.spot((x, -(D / 2) - 0.003, 0.05), 0.04, "rust", seed=150 + i, stretch=(0.7, 1.4)))
    p.append(L.spot((0.15, -(md / 2) - 0.002, MAT_Z + 0.02), 0.12, "khaki", seed=155, stretch=(1.4, 0.6)))
    return p


def nizkaya():
    """Низкая: матрас на подставке из поддона (доски + бруски), мятое одеяло, подушка."""
    p = []
    PH = 0.15
    # поддон: верхние доски поперёк, бруски-опоры, нижние доски
    nb = 9
    bw = (W - 0.08) / nb
    for k in range(nb):
        x = -W / 2 + 0.04 + bw * (k + 0.5)
        p.append(L.box((bw - 0.02, D, 0.025), (x, 0, PH - 0.025), "wood_light" if k % 3 == 1 else "wood", bevel=0.005))
    for x in (-(W / 2 - 0.08), 0.0, W / 2 - 0.08):
        for y in (-(D / 2 - 0.06), 0.0, D / 2 - 0.06):
            p.append(L.box((0.10, 0.09, PH - 0.05), (x, y, 0.025), "wood_dark", bevel=0.008))
    for y in (-(D / 2 - 0.06), D / 2 - 0.06):
        p.append(L.box((W - 0.02, 0.09, 0.025), (0, y, 0.0), "wood", bevel=0.005))
    # матрас (толстый, просел посередине — две половины), подушка, одеяло
    mw, md = W - 0.12, D - 0.06
    p.append(L.soft((mw * 0.5 + 0.01, md, 0.17), (-mw / 4, 0, PH), "cloth_beige"))
    p.append(L.soft((mw * 0.5 + 0.01, md, 0.16), (mw / 4, 0, PH), "cloth_beige"))
    p.append(L.box((mw, md + 0.006, 0.02), (0, 0, PH + 0.05), "khaki_light", bevel=0.006))
    top = PH + 0.17
    p.append(L.soft((0.44, md - 0.24, 0.12), (-(mw / 2 - 0.27), 0.04, top - 0.02), "offwhite", rot=(0, -6, 0)))
    p += L.blanket(mw * 0.10, mw * 0.70, md, top + 0.005, "khaki", seed=21, hang=(0.08, 0.16))
    # износ: тёмные пятна на досках, пятно на матрасе
    for i, (x, s) in enumerate(((-0.6, 0.10), (0.2, 0.08), (0.8, 0.07))):
        p.append(L.spot((x, -D / 2 - 0.002, PH - 0.012), s, "wood_dark", seed=160 + i, stretch=(1.4, 0.5)))
    p.append(L.spot((0.35, -(md / 2) - 0.002, PH + 0.09), 0.10, "khaki_light", seed=165, stretch=(1.3, 0.7)))
    return p


def krovat_s_tumboy():
    """Деревянная кровать 155 см + тумбочка 43 см у изголовья (вместе — 200 см по плану)."""
    TW, TH, TD = 0.43, 0.55, 0.40
    bw = W - TW - 0.02
    p = wooden(bw, x0=W / 2 - bw / 2, seed=33, blanket="paint_red")
    tx = -W / 2 + TW / 2
    p.append(L.box((TW, TD, TH - 0.03), (tx, 0.05, 0.05), "wood", bevel=0.012))
    p.append(L.box((TW + 0.02, TD + 0.02, 0.03), (tx, 0.05, TH - 0.03), "wood_dark", bevel=0.008))      # крышка
    for sx in (-1, 1):
        p.append(L.box((0.04, 0.04, 0.05), (tx + sx * (TW / 2 - 0.04), 0.05 - TD / 2 + 0.04, 0), "wood_dark", bevel=0.006))
    yf = 0.05 - TD / 2
    p.append(L.box((TW - 0.05, 0.02, 0.12), (tx, yf - 0.008, TH - 0.19), "wood_light", bevel=0.006))   # ящик
    p.append(L.box((TW - 0.05, 0.02, 0.26), (tx, yf - 0.008, 0.08), "wood_light", bevel=0.006))         # дверца
    p.append(L.box((0.08, 0.02, 0.018), (tx, yf - 0.026, TH - 0.13), "steel", bevel=0.004))
    p.append(L.cyl(0.012, 0.02, (tx + 0.13, yf - 0.02, 0.25), "steel", verts=6, rot=(90, 0, 0)))
    p.append(L.spot((tx - 0.08, yf - 0.02, 0.15), 0.06, "wood_dark", seed=170))
    p.append(L.spot((tx + 0.05, 0.0, TH), 0.08, "wood_light", facing="top", seed=171, stretch=(1.5, 0.7)))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("zheleznaya_koyka", zheleznaya_koyka), ("derevyannaya_samodelnaya", derevyannaya_samodelnaya),
                    ("nizkaya", nizkaya), ("krovat_s_tumboy", krovat_s_tumboy)):
        L.make(fn, "furniture", "bed_single", var, size_cm=(W * 100, H * 100), broken="legs")
    L.save_blend("furniture", "bed_single")
