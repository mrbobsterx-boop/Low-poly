"""Аптечка `first_aid_kit`. Размер — из плана ОС (25 × 18 см). Закрыта (открытая — состояние, не делаем).
Варианты (только idle): domashnyaya — белая пластиковая коробка с красным крестом и ручкой;
  avtomobilnaya — оранжево-красный футляр с защёлками; voennaya — подсумок хаки с клапаном и белым крестом в круге.
Запуск: python3 models/container/first_aid_kit.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("first_aid_kit"))
ROUGH = {"min_area": 0.002, "k": 0.025, "amp_max": 0.002}
D = 0.10


def cross(p, x, y, z, s, col):
    p.append(L.box((s, 0.004, s * 0.32), (x, y, z - s * 0.16), col, bevel=0))
    p.append(L.box((s * 0.32, 0.004, s), (x, y, z - s / 2), col, bevel=0))


def domashnyaya():
    p = [L.box((W, D, H - 0.03), (0, 0, 0), "plastic_white", bevel=0.01)]
    p.append(L.box((W + 0.004, D + 0.004, 0.012), (0, 0, (H - 0.03) * 0.75), "offwhite", bevel=0.004))   # шов крышки
    cross(p, 0, -D / 2 - 0.002, 0.10, 0.07, "paint_red")
    p.append(L.box((0.08, 0.025, 0.012), (0, 0, H - 0.012), "soot", bevel=0.004))                    # ручка
    for sx in (-1, 1):
        p.append(L.box((0.012, 0.02, 0.03), (sx * 0.04, 0, H - 0.04), "soot", bevel=0.003))
    p.append(L.spot((0.08, -D / 2 - 0.003, 0.03), 0.02, "dirt", seed=930))
    return p


def avtomobilnaya():
    p = [L.box((W, D, H), (0, 0, 0), "paint_red", bevel=0.02)]
    for sx in (-1, 1):
        p.append(L.box((0.03, 0.015, 0.03), (sx * 0.07, -D / 2 - 0.006, H * 0.62), "soot", bevel=0.004))   # защёлки
    p.append(L.box((W - 0.03, 0.004, 0.06), (0, -D / 2 - 0.002, 0.03), "offwhite", bevel=0))
    cross(p, 0, -D / 2 - 0.004, 0.08, 0.04, "paint_red")
    return p


def voennaya():
    p = [L.soft((W, D, H - 0.02), (0, 0, 0), "khaki")]
    p.append(L.box((W - 0.02, 0.02, 0.09), (0, -D / 2 + 0.005, H - 0.11), "olive_dark", bevel=0.006))   # клапан
    p.append(L.box((0.03, 0.015, 0.04), (0, -D / 2 - 0.008, H - 0.12), "soot", bevel=0.003))           # фастекс
    p.append(L.cyl(0.03, 0.004, (0, -D / 2 - 0.0, 0.06), "offwhite", verts=10, rot=(90, 0, 0)))
    cross(p, 0, -D / 2 - 0.006, 0.08, 0.04, "paint_red")
    for sx in (-1, 1):                                                                                # стропы
        p.append(L.box((0.025, 0.004, H - 0.03), (sx * 0.08, -D / 2 - 0.002, 0.01), "olive_dark", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("domashnyaya", domashnyaya), ("avtomobilnaya", avtomobilnaya), ("voennaya", voennaya)):
        L.make(fn, "container", "first_aid_kit", var, size_cm=(W * 100, H * 100), limit="small", broken=False, rough=ROUGH)
    L.save_blend("container", "first_aid_kit")
