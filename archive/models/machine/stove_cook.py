"""Плита `stove_cook`. Размер — из плана ОС (70 × 90 см). Варианты (только idle; «сломанная» — пропуск):
  gazovaya        — газовая: белая эмаль, 4 конфорки с решётками, ручки, духовка со стеклом, баллон сбоку не впечён;
  elektricheskaya — электрическая: 4 чугунных блина, панель с ручками и лампой, духовка;
  drovyanaya      — дровяная: чугунная плита с кольцами, топка и поддувало, дымоход назад, ножки.
Огонь/нагрев — игра. Запуск: python3 models/machine/stove_cook.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("stove_cook"))
D = 0.60
F = -D / 2


def body(p, color, top_h, panel=True):
    """Корпус-шкаф: тумба, ножки-регулировки, духовка со стеклом и ручкой-трубой, щиток сзади."""
    p.append(L.box((W, D, top_h - 0.04), (0, 0, 0.04), color, bevel=0.012))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.append(L.cyl(0.02, 0.04, (sx * (W / 2 - 0.05), sy * (D / 2 - 0.05), 0), "soot", verts=6))
    p.append(L.box((W - 0.02, 0.01, 0.04), (0, F + 0.04, 0.0), "soot", bevel=0))                       # цоколь
    p.append(L.box((W - 0.08, 0.02, top_h * 0.55), (0, F - 0.006, 0.12), color, bevel=0.01))          # дверца духовки
    p.append(L.box((W - 0.24, 0.008, top_h * 0.28), (0, F - 0.018, 0.22), "glass", bevel=0.004))
    p.append(L.box((W - 0.26, 0.004, top_h * 0.24), (0, F - 0.022, 0.235), "soot", bevel=0))           # темнота внутри
    p.append(L.tube((-(W / 2 - 0.10), F - 0.05, top_h * 0.62), ((W / 2 - 0.10), F - 0.05, top_h * 0.62), 0.012, "steel_light", verts=6))
    for sx in (-1, 1):
        p.append(L.box((0.02, 0.04, 0.02), (sx * (W / 2 - 0.10), F - 0.03, top_h * 0.62 - 0.01), "steel", bevel=0.003))
    p.append(L.box((W - 0.08, 0.02, 0.06), (0, F - 0.006, 0.05), color, bevel=0.006))                  # ящик внизу
    p.append(L.box((0.12, 0.012, 0.012), (0, F - 0.02, 0.075), "steel", bevel=0.002))
    if panel:
        p.append(L.box((W, 0.04, H - top_h), (0, D / 2 - 0.02, top_h), color, bevel=0.008))            # щиток сзади


def knobs(p, z, n=4, color="soot"):
    for k in range(n):
        x = -W / 2 + 0.11 + k * (W - 0.22) / (n - 1)
        p.append(L.cyl(0.02, 0.025, (x, F - 0.006, z), color, verts=8, rot=(90, 0, 0)))
        p.append(L.box((0.006, 0.004, 0.026), (x, F - 0.032, z - 0.013), "offwhite", bevel=0))


def gazovaya():
    p = []
    TH = 0.85
    body(p, "plastic_white", TH)
    p.append(L.box((W, D, 0.02), (0, 0, TH - 0.02), "steel_light", bevel=0.006))                       # варочная панель
    for x in (-0.17, 0.17):
        for y in (-0.13, 0.12):
            p.append(L.cyl(0.05, 0.02, (x, y, TH), "soot", verts=8))                                   # рассекатель
            p.append(L.cyl(0.03, 0.01, (x, y, TH + 0.02), "steel_dark", verts=8))
            for a in (0, 90):                                                                           # решётка-крест
                p.append(L.box((0.20, 0.014, 0.014), (x, y, TH + 0.028), "soot", rot=(0, 0, a + 10), bevel=0))
    p.append(L.box((W - 0.04, 0.03, 0.05), (0, F + 0.01, TH - 0.07), "plastic_white", bevel=0.006))
    knobs(p, TH - 0.045)
    for i, (x, z, s, c) in enumerate(((-0.2, 0.55, 0.06, "dirt"), (0.25, 0.30, 0.05, "rust"), (0.1, 0.70, 0.04, "soot"))):
        p.append(L.spot((x, F - 0.017, z), s, c, seed=800 + i))
    p.append(L.spot((0.05, 0.0, TH + 0.001), 0.10, "soot", facing="top", seed=805, stretch=(1.5, 0.8)))   # нагар
    return p


def elektricheskaya():
    p = []
    TH = 0.85
    body(p, "offwhite", TH)
    p.append(L.box((W, D, 0.02), (0, 0, TH - 0.02), "steel_dark", bevel=0.006))
    for (x, y), r in (((-0.17, -0.13), 0.085), ((0.17, -0.13), 0.07), ((-0.17, 0.12), 0.07), ((0.17, 0.12), 0.085)):
        p.append(L.cyl(r + 0.01, 0.008, (x, y, TH), "steel", verts=10))                                # обод
        p.append(L.cyl(r, 0.018, (x, y, TH), "soot", verts=10))                                        # блин
        p.append(L.cyl(r * 0.35, 0.002, (x, y, TH + 0.018), "stone_dark", verts=8))
    # пульт на щитке: ручки + лампа
    for k in range(4):
        x = -W / 2 + 0.11 + k * 0.12
        p.append(L.cyl(0.022, 0.03, (x, D / 2 - 0.04, TH + 0.025), "soot", verts=8, rot=(90, 0, 0)))
    p.append(L.cyl(0.01, 0.01, (W / 2 - 0.12, D / 2 - 0.045, TH + 0.025), "paint_red", verts=6, rot=(90, 0, 0)))
    for i, (x, z, s, c) in enumerate(((0.2, 0.62, 0.06, "dirt"), (-0.22, 0.12, 0.05, "rust"), (-0.05, 0.75, 0.04, "steel"))):
        p.append(L.spot((x, F - 0.017, z), s, c, seed=810 + i))
    return p


def drovyanaya():
    p = []
    TH = 0.72
    LG = 0.10
    BW = W - 0.06
    for sx in (-1, 1):                                                                                  # ножки
        for sy in (-1, 1):
            p.append(L.cyl(0.025, LG, (sx * (BW / 2 - 0.05), sy * (D / 2 - 0.06), 0), "soot", verts=6, radius_top=0.035))
    p.append(L.box((BW, D - 0.04, TH - LG - 0.035), (0, 0, LG), "steel_dark", bevel=0.012))
    for z in (LG + 0.02, TH - 0.07):                                                                    # уголки-рама
        p.append(L.box((BW + 0.01, D - 0.03, 0.025), (0, 0, z), "soot", bevel=0.004))
    p.append(L.box((W, D, 0.035), (0, 0, TH - 0.035), "soot", bevel=0.006))                            # чугунная плита
    for (x, y), r in (((-0.15, -0.06), 0.11), ((0.17, -0.06), 0.08)):
        p.append(L.cyl(r, 0.012, (x, y, TH), "steel_dark", verts=10))                                  # кольца конфорок
        p.append(L.cyl(r * 0.6, 0.016, (x, y, TH), "soot", verts=10))
        p.append(L.cyl(r * 0.25, 0.02, (x, y, TH), "steel", verts=6))
    p.append(L.box((W - 0.04, 0.012, 0.012), (0, F + 0.006, TH + 0.012), "steel", bevel=0))           # поручень спереди
    Fy = -(D - 0.04) / 2
    p.append(L.box((0.26, 0.02, 0.20), (-0.12, Fy - 0.006, 0.36), "soot", bevel=0.006))               # дверца топки
    p.append(L.box((0.20, 0.012, 0.15), (-0.12, Fy - 0.014, 0.385), "steel_dark", bevel=0.005))
    for x in (-0.17, -0.12, -0.07):
        p.append(L.box((0.012, 0.01, 0.10), (x, Fy - 0.02, 0.41), "soot", bevel=0))
    p.append(L.box((0.05, 0.025, 0.018), (0.02, Fy - 0.03, 0.45), "steel_light", bevel=0.005))
    p.append(L.box((0.22, 0.016, 0.06), (-0.12, Fy - 0.004, 0.17), "steel_dark", bevel=0.004))        # поддувало
    p.append(L.box((0.22, 0.02, 0.36), (0.20, Fy - 0.006, 0.16), "steel_dark", bevel=0.006))           # духовой шкаф
    p.append(L.box((0.03, 0.03, 0.02), (0.12, Fy - 0.025, 0.40), "steel_light", bevel=0.004))
    # дымоход сзади: колено и труба вверх до 90 см
    p.append(L.cyl(0.06, H - TH, (0.20, D / 2 - 0.10, TH), "steel", verts=8))
    p.append(L.cyl(0.07, 0.03, (0.20, D / 2 - 0.10, TH), "rust_dark", verts=8))
    p.append(L.cyl(0.07, 0.025, (0.20, D / 2 - 0.10, H - 0.025), "steel_dark", verts=8))
    for i, (x, z, s, c) in enumerate(((-0.25, 0.55, 0.07, "rust"), (0.25, 0.60, 0.05, "rust_dark"), (-0.05, 0.25, 0.06, "soot"))):
        p.append(L.spot((x, Fy - 0.002, z), s, c, seed=820 + i))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("gazovaya", gazovaya), ("elektricheskaya", elektricheskaya), ("drovyanaya", drovyanaya)):
        L.make(fn, "machine", "stove_cook", var, size_cm=(W * 100, H * 100), broken="legs")
    L.save_blend("machine", "stove_cook")
