"""Кровать `bed_single`, вариант `zheleznaya_koyka` (железная койка). ОС: 200 × 60 см.
Образец: docs/ref/furniture/bed_single.png (чемоданы под кроватью — отдельные предметы, сюда не входят).
Запуск: python3 models/furniture/bed_single.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, D, H = 2.00, 0.85, 0.60
FRAME_Z = 0.32              # высота рамы (сетки)
T = 0.035                   # толщина трубы


def end_rail(x, h, p, color="steel_dark"):
    """Спинка: две стойки, верхняя и нижняя перекладины, три прутка."""
    for sy in (-1, 1):
        p.append(L.box((T, T, h), (x, sy * (D / 2 - T / 2), 0), color))
    p.append(L.box((T, D, T), (x, 0, h - T), color))
    p.append(L.box((T, D, T), (x, 0, FRAME_Z - 0.04), color))
    for y in (-0.2, 0, 0.2):
        p.append(L.box((0.02, 0.02, h - FRAME_Z), (x, y, FRAME_Z - 0.04), color))


def bed_idle():
    p = []
    end_rail(-(W / 2 - T / 2), H, p)                 # изголовье
    end_rail(W / 2 - T / 2, H - 0.08, p)             # изножье ниже
    # боковые трубы рамы
    for sy in (-1, 1):
        p.append(L.box((W - 2 * T, T, T), (0, sy * (D / 2 - T / 2), FRAME_Z - 0.04), "steel"))
    # матрас (полосатый: три полосы хаки), одеяло, подушка
    mw = W - 2 * T - 0.02
    p.append(L.box((mw, D - 0.06, 0.12), (0, 0, FRAME_Z), "khaki_light"))
    p.append(L.box((mw * 0.62, D - 0.04, 0.03), (mw * 0.17, 0, FRAME_Z + 0.12), "khaki"))      # одеяло
    p.append(L.box((mw * 0.62 + 0.004, 0.02, 0.10), (mw * 0.17, -(D / 2 - 0.01), FRAME_Z + 0.04), "khaki"))  # свес
    p.append(L.box((0.42, D - 0.20, 0.10), (-(mw / 2 - 0.26), 0, FRAME_Z + 0.12), "offwhite"))  # подушка
    return p


def bed_broken():
    """Ножка у изножья подломилась: рама наклонена, матрас продавлен и порван, одеяло сползло на пол."""
    p = []
    end_rail(-(W / 2 - T / 2), H, p)
    # изножье завалилось
    q = []
    end_rail(0, H - 0.08, q, "rust")
    for o in q:
        L._place(o, (W / 2 - 0.10, 0, 0), (0, 25, 0))
    p += q
    import math
    ang = -math.degrees(math.atan((FRAME_Z - 0.10) / W))
    for sy in (-1, 1):
        p.append(L.box((W - 0.06, T, T), (0, sy * (D / 2 - T / 2), FRAME_Z - 0.16), "rust", rot=(0, -ang, 0)))
    mw = W - 0.12
    # матрас двумя кусками (провал посередине) и сползшее одеяло
    p.append(L.box((mw * 0.48, D - 0.08, 0.11), (-mw * 0.24, 0, FRAME_Z - 0.10), "khaki_light", rot=(0, -6, 0)))
    p.append(L.box((mw * 0.46, D - 0.10, 0.10), (mw * 0.27, 0, FRAME_Z - 0.20), "khaki_light", rot=(0, 10, 0)))
    p.append(L.box((0.30, D - 0.30, 0.03), (0.02, 0, FRAME_Z - 0.12), "dirt"))                    # дыра
    p.append(L.box((0.70, 0.40, 0.03), (0.55, -0.35, 0), "khaki", rot=(0, 0, 8)))                # одеяло на полу
    return p


if __name__ == "__main__":
    L.new_scene()
    L.finish(bed_idle(), "furniture", "bed_single", "zheleznaya_koyka", "idle", size_cm=(200, 60))
    L.finish(bed_broken(), "furniture", "bed_single", "zheleznaya_koyka", "broken")
    L.save_blend("furniture", "bed_single")
