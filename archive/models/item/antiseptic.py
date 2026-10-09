"""Антисептик `antiseptic` (предмет). Размер — из плана ОС (6 × 14 см). Варианты (только idle):
  spirt — стеклянная бутылка спирта с этикеткой; perekis — пластиковый флакон перекиси; yod — тёмный пузырёк йода.
Запуск: python3 models/item/antiseptic.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("antiseptic"))
ROUGH = {"min_area": 0.0004, "k": 0.02, "amp_max": 0.001}
N = 8


def spirt():
    r = W / 2
    p = [L.cyl(r, 0.09, (0, 0, 0), "glass", verts=N)]
    p.append(L.cyl(r * 0.85, 0.07, (0, 0, 0.005), "steel_light", verts=N))                    # жидкость за стеклом
    p.append(L.cyl(r, 0.025, (0, 0, 0.09), "glass", verts=N, radius_top=0.012))
    p.append(L.cyl(0.011, 0.015, (0, 0, 0.115), "glass", verts=N))
    p.append(L.cyl(0.012, 0.012, (0, 0, H - 0.012), "paint_blue", verts=N))                   # пробка
    p.append(L.cyl(r + 0.001, 0.04, (0, 0, 0.025), "offwhite", verts=N))                      # этикетка
    p.append(L.box((0.03, 0.003, 0.008), (0, -r - 0.002, 0.045), "paint_blue", bevel=0))
    return p


def perekis():
    p = [L.box((0.05, 0.035, 0.10), (0, 0, 0), "plastic_white", bevel=0.008)]
    p.append(L.cyl(0.012, 0.025, (0, 0, 0.10), "plastic_white", verts=N, radius_top=0.006))
    p.append(L.cyl(0.014, 0.012, (0, 0, 0.10), "paint_red", verts=N))
    p.append(L.box((0.04, 0.003, 0.04), (0, -0.0185, 0.03), "paint_blue", bevel=0))
    p.append(L.box((0.03, 0.003, 0.006), (0, -0.0195, 0.045), "offwhite", bevel=0))
    return p


def yod():
    r = 0.017
    p = [L.cyl(r, 0.06, (0, 0, 0), "rust_dark", verts=N)]
    p.append(L.cyl(r, 0.015, (0, 0, 0.06), "rust_dark", verts=N, radius_top=0.008))
    p.append(L.cyl(0.011, 0.025, (0, 0, 0.075), "soot", verts=N))                              # крышка
    p.append(L.cyl(r + 0.001, 0.03, (0, 0, 0.012), "offwhite", verts=N))
    p.append(L.box((0.015, 0.003, 0.006), (0, -r - 0.002, 0.024), "rust", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("spirt", spirt), ("perekis", perekis), ("yod", yod)):
        L.make(fn, "item", "antiseptic", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "antiseptic")
