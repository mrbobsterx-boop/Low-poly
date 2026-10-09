"""ПРОБА КАЧЕСТВА (docs/QUALITY.md): армейский шкафчик `locker_metal_armeyskiy` по образцам docs/ref/style/props_sheet_*.
Две дверцы с утопленными панелями, жалюзи сверху и снизу (настоящие щели), крупные ручки и петли, козырёк,
цоколь, плакат с черепом, номер-бирка, ржавые потёки снизу.
Запуск (только просмотр): python3 render/_lit_preview.py <папка> models/_probe/locker.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

L.quality()
W, H = 0.50, 1.80
D = 0.45
PL = 0.07
BODY, DARK = "army_green", "olive_dark"
F = -D / 2


def louvers(p, x, z, w, n=4, step=0.04):
    p.append(L.box((w + 0.02, 0.01, n * step + 0.02), (x, F - 0.016, z - 0.01), "soot", bevel=0.003))   # тёмная ниша
    for i in range(n):
        p.append(L.box((w, 0.016, 0.02), (x, F - 0.03, z + i * step), BODY, rot=(-30, 0, 0), bevel=0.004))


def door(p, x0, x1, right):
    w, cx = x1 - x0, (x0 + x1) / 2
    z0, z1 = PL + 0.025, H - 0.07
    p.append(L.box((w - 0.01, 0.02, z1 - z0), (cx, F - 0.01, z0), BODY, bevel=0.01))
    p.append(L.box((w - 0.07, 0.006, 0.78), (cx, F - 0.022, PL + 0.42), DARK, bevel=0.004))             # утопленная панель
    p.append(L.box((w - 0.09, 0.006, 0.74), (cx, F - 0.026, PL + 0.44), BODY, bevel=0.004))
    louvers(p, cx, H - 0.32, w - 0.08)
    louvers(p, cx, PL + 0.10, w - 0.08)
    hx = x0 + 0.035 if right else x1 - 0.035                                                           # ручка у середины
    p.append(L.box((0.03, 0.03, 0.03), (hx, F - 0.035, PL + 0.85), "steel_dark", bevel=0.005))
    p.append(L.box((0.03, 0.03, 0.03), (hx, F - 0.035, PL + 1.05), "steel_dark", bevel=0.005))
    p.append(L.box((0.026, 0.026, 0.24), (hx, F - 0.06, PL + 0.83), "steel_light", bevel=0.006))       # скоба — крупная
    ex = x1 - 0.006 if right else x0 + 0.006                                                           # петли
    for z in (PL + 0.20, H - 0.25):
        p.append(L.cyl(0.014, 0.10, (ex, F - 0.016, z), "steel_dark", verts=8))


def locker():
    p = []
    p.append(L.box((W, D, H - PL - 0.04), (0, 0, PL), BODY, bevel=0.012))
    p.append(L.box((W + 0.03, D + 0.03, 0.045), (0, 0, H - 0.045), DARK, bevel=0.01))                 # козырёк
    p.append(L.box((W - 0.02, D - 0.04, PL), (0, 0.01, 0), "soot", bevel=0.006))                       # цоколь
    p.append(L.box((W - 0.016, 0.006, H - PL - 0.08), (0, F - 0.001, PL + 0.02), "soot", bevel=0))     # зазор вокруг дверей
    door(p, -W / 2 + 0.012, -0.004, right=False)
    door(p, 0.004, W / 2 - 0.012, right=True)
    p.append(L.box((0.05, 0.035, 0.07), (0.0, F - 0.045, PL + 0.93), "steel", bevel=0.006))            # навесной замок
    p.append(L.cyl(0.018, 0.02, (0.0, F - 0.04, PL + 1.0), "steel_light", verts=10, rot=(90, 0, 0)))
    # плакат с черепом (правая дверь), бирка с номером (левая), вентиляция сбоку не видна
    p.append(L.decal("skull_poster", (0.125, F - 0.030, H - 0.62), 0.15))
    p.append(L.decal("label_white", (-0.125, F - 0.030, H - 0.50), 0.10))
    # износ: ржавые потёки снизу и у петель, царапины
    for i, (x, z, s) in enumerate(((-0.17, PL + 0.08, 0.10), (0.06, PL + 0.06, 0.12), (0.19, PL + 0.10, 0.07))):
        p.append(L.spot((x, F - 0.031, z), s, "rust", seed=600 + i, stretch=(1.0, 0.7)))
        p.append(L.spot((x + 0.01, F - 0.033, z - 0.02), s * 0.5, "rust_dark", seed=610 + i, stretch=(1.0, 0.6)))
    p.append(L.spot((0.20, F - 0.031, H - 0.30), 0.05, "rust", seed=620, stretch=(0.5, 1.8)))
    p.append(L.box((0.10, 0.004, 0.012), (-0.12, F - 0.028, 0.70), DARK, rot=(0, 20, 0), bevel=0))     # вмятина
    return p


if __name__ == "__main__":
    L.new_scene()
    L.make(locker, "_probe", "locker_metal", "armeyskiy", size_cm=(W * 100, H * 100), glb=False)
