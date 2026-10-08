"""Консервный нож `tool_can_opener` (инструмент). Размер — из плана ОС (15 × 8 см). Варианты (только idle):
  ruchnoy — механический с двумя ручками и колёсиком; klyuch_otkryvashka — простой ключ-«клюв» с деревянной ручкой.
Лежат плашмя, видны сверху-спереди. Запуск: python3 models/tool/tool_can_opener.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("tool_can_opener"))
ROUGH = {"min_area": 0.0006, "k": 0.02, "amp_max": 0.001}


def ruchnoy():
    p = []
    for s in (-1, 1):                                                                         # две ручки, разведены
        p.append(L.box((0.10, 0.016, 0.012), (0.02, s * 0.012, 0.0), "paint_red", rot=(0, 0, s * 5), bevel=0.004))
    p.append(L.box((0.04, 0.04, 0.016), (-0.05, 0, 0.0), "steel", bevel=0.004))               # головка
    p.append(L.cyl(0.016, 0.03, (-0.05, 0, 0.016), "steel_light", verts=8))                    # барашек
    p.append(L.box((0.035, 0.008, 0.008), (-0.05, 0, 0.042), "steel_light", bevel=0))
    p.append(L.cyl(0.012, 0.006, (-0.05, -0.023, 0.008), "steel_dark", verts=8, rot=(90, 0, 0)))   # колёсико
    return p


def klyuch_otkryvashka():
    p = [L.box((0.08, 0.02, 0.016), (0.03, 0, 0), "wood", bevel=0.005)]                       # ручка
    p.append(L.box((0.06, 0.008, 0.004), (-0.035, 0, 0.006), "steel", bevel=0))               # полотно
    p.append(L.poly([(0.0, 0.0), (0.012, 0.0), (0.004, 0.025)], 0.004, (-0.07, 0.0, 0.004), "steel_light"))   # клюв
    for x in (0.01, 0.05):
        p.append(L.cyl(0.003, 0.002, (x, 0, 0.016), "steel_light", verts=6))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("ruchnoy", ruchnoy), ("klyuch_otkryvashka", klyuch_otkryvashka)):
        L.make(fn, "tool", "tool_can_opener", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("tool", "tool_can_opener")
