"""Сухпаёк `ration_dry` (предмет). Размер — из плана ОС (15 × 10 см). Варианты (только idle):
  armeyskiy — армейский: картонная коробка цвета хаки с трафаретом; spasatelnyy_nabor — оранжево-жёлтый вакуумный
  пакет с полосой; kosmicheskiy — серебристые тюбик и пакет (редкий). Запуск: python3 models/item/ration_dry.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("ration_dry"))
ROUGH = {"min_area": 0.0008, "k": 0.03, "amp_max": 0.0015}


def armeyskiy():
    p = [L.box((W, 0.08, H), (0, 0, 0), "khaki", bevel=0.004)]
    p.append(L.box((W + 0.002, 0.03, 0.004), (0, 0, H), "khaki_light", bevel=0))            # скотч
    p.append(L.box((0.09, 0.003, 0.03), (0, -0.041, 0.05), "olive_dark", bevel=0))            # трафарет
    p.append(L.box((0.05, 0.003, 0.008), (0, -0.041, 0.025), "soot", bevel=0))
    p.append(L.spot((0.05, -0.042, 0.02), 0.02, "dirt", seed=915))
    return p


def spasatelnyy_nabor():
    p = [L.soft((W, 0.07, H * 0.8), (0, 0, 0), "hazard_yellow")]
    p.append(L.box((W - 0.01, 0.003, 0.02), (0, -0.036, 0.035), "paint_red", bevel=0))
    p.append(L.box((0.03, 0.003, 0.03), (-0.04, -0.037, 0.03), "offwhite", bevel=0))
    p.append(L.box((W + 0.004, 0.02, 0.012), (0, 0, H * 0.8 - 0.006), "hazard_yellow", bevel=0.002))   # шов
    return p


def kosmicheskiy():
    p = [L.soft((0.10, 0.06, 0.08), (-0.025, 0, 0), "steel_light")]
    p.append(L.box((0.05, 0.003, 0.02), (-0.025, -0.031, 0.035), "paint_blue", bevel=0))
    p.append(L.cyl(0.015, 0.09, (0, 0, 0), "steel_light", verts=8, radius_top=0.012, rot=(0, 0, 0)))   # тюбик
    L.transform([p[-1]], (0.055, 0.0, 0.0))
    p.append(L.cyl(0.008, 0.012, (0.055, 0, 0.09), "paint_red", verts=6))
    p.append(L.box((0.032, 0.012, 0.012), (0.055, 0, 0.0), "steel", bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("armeyskiy", armeyskiy), ("spasatelnyy_nabor", spasatelnyy_nabor), ("kosmicheskiy", kosmicheskiy)):
        L.make(fn, "item", "ration_dry", var, limit="small", broken=False, rough=ROUGH)
    L.save_blend("item", "ration_dry")
