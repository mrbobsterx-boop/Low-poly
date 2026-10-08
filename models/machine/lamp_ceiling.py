"""Лампа `lamp_ceiling`. Размер — из плана ОС (30 × 25 см). Висит: origin в точке крепления (верх), лампа — вниз.
Настольная — стоит: origin внизу. Светящиеся части — материал emission (свет и вкл/выкл делает игра).
Варианты (только idle):
  lampa_nakalivaniya     — голая лампочка в патроне на шнуре, маленький жестяной отражатель;
  svetodiodnaya          — плоская светодиодная панель на подвесах (как на референсе автора);
  avariynaya             — аварийная красная: плафон в решётке на кронштейне;
  nastolnaya             — настольная на шарнирной ножке;
  podvesnaya_s_abazhurom — подвесная с эмалированным абажуром.
Запуск: python3 models/machine/lamp_ceiling.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("lamp_ceiling"))


def lampa_nakalivaniya():
    p = [L.cyl(0.04, 0.015, (0, 0, -0.015), "steel_dark", verts=8)]
    p.append(L.tube((0, 0, -0.015), (0, 0, -0.13), 0.005, "soot", verts=4))                       # шнур
    p.append(L.cyl(0.02, 0.04, (0, 0, -0.17), "soot", verts=8))                                   # патрон
    p.append(L.cyl(W / 2, 0.012, (0, 0, -0.155), "steel", verts=10, radius_top=0.03))             # отражатель-тарелка
    p.append(L.cyl(0.032, 0.03, (0, 0, -0.20), "glow_lamp", verts=8, radius_top=0.012, glow=True))   # горлышко
    p.append(L.cyl(0.036, 0.02, (0, 0, -0.22), "glow_lamp", verts=8, radius_top=0.032, glow=True))   # «груша»
    p.append(L.cyl(0.012, 0.03, (0, 0, -H), "glow_lamp", verts=8, radius_top=0.036, glow=True))
    p.append(L.spot((0.08, -0.06, -0.155), 0.04, "rust", facing="top", seed=340))
    return p


def svetodiodnaya():
    p = [L.box((0.12, 0.08, 0.02), (0, 0, -0.02), "steel_dark", bevel=0.005)]
    for x in (-0.09, 0.09):
        p.append(L.box((0.008, 0.008, 0.13), (x, 0, -0.15), "soot", bevel=0))
    p.append(L.poly([(-0.11, 0.0), (0.11, 0.0), (0.15, -0.07), (-0.15, -0.07)], 0.12, (0, 0, -0.15), "steel_dark"))
    p.append(L.box((0.22, 0.10, 0.012), (0, 0, -0.152), "steel", bevel=0.003))
    p.append(L.box((0.27, 0.13, 0.04), (0, -0.01, -0.25), "glow_lamp", glow=True, bevel=0.006))
    for x in (-0.14, 0.14):
        p.append(L.box((0.014, 0.14, 0.045), (x, -0.01, -0.252), "steel_dark", bevel=0.003))
    return p


def avariynaya():
    """Аварийная: кронштейн, основание, красный плафон (светится) в проволочной решётке."""
    p = [L.box((0.10, 0.08, 0.03), (0, 0, -0.03), "steel_dark", bevel=0.006)]
    p.append(L.box((0.03, 0.03, 0.06), (0, 0, -0.09), "steel_dark", bevel=0.004))
    p.append(L.cyl(W / 2, 0.03, (0, 0, -0.12), "hazard_yellow", verts=10, radius_top=0.10))        # основание
    p.append(L.cyl(0.08, 0.10, (0, 0, -0.22), "paint_red", verts=10, radius_top=0.085, glow=True))  # плафон (снизу)
    for k in range(6):                                                                              # решётка
        import math
        a = math.pi * k / 3
        x, y = 0.092 * math.cos(a), 0.092 * math.sin(a)
        p.append(L.tube((x, y, -0.12), (x * 0.8, y * 0.8, -H), 0.005, "soot", verts=4))
    p.append(L.cyl(0.095, 0.01, (0, 0, -0.18), "soot", verts=10))
    p.append(L.cyl(0.06, 0.01, (0, 0, -H), "soot", verts=8))
    for k in range(3):                                                                              # полосы на основании
        p.append(L.box((0.02, 0.004, 0.03), (-0.05 + k * 0.05, -0.1, -0.12), "soot", rot=(0, 35, 0), bevel=0))
    return p


def nastolnaya():
    """Настольная: тяжёлое основание, две трубки-шарнира, конус-плафон, лампочка (светится). Стоит — origin внизу."""
    p = [L.cyl(0.07, 0.025, (-0.08, 0, 0), "steel_dark", verts=10)]
    p.append(L.cyl(0.02, 0.02, (-0.08, 0, 0.025), "steel", verts=8))
    a, b, c = (-0.08, 0, 0.04), (-0.03, 0, 0.19), (0.07, 0, 0.235)
    p.append(L.tube(a, b, 0.008, "steel", verts=6))
    p.append(L.tube(b, c, 0.008, "steel", verts=6))
    p.append(L.cyl(0.014, 0.02, (b[0], -0.01, b[2]), "soot", verts=8, rot=(90, 0, 0)))             # шарнир
    p.append(L.cyl(0.07, 0.07, (0.10, 0, 0.155), "army_green", verts=10, radius_top=0.025, rot=(0, -30, 0)))  # плафон
    p.append(L.cyl(0.03, 0.03, (0.115, 0, 0.15), "glow_lamp", verts=8, glow=True, rot=(0, -30, 0)))
    p.append(L.spot((0.11, -0.05, 0.17), 0.03, "steel", seed=350))
    return p


def podvesnaya_s_abazhurom():
    p = [L.cyl(0.05, 0.02, (0, 0, -0.02), "steel_dark", verts=8)]
    p.append(L.tube((0, 0, -0.02), (0, 0, -0.10), 0.006, "steel_dark", verts=6))
    p.append(L.cyl(0.03, 0.03, (0, 0, -0.13), "steel", verts=8))
    p.append(L.cyl(W / 2, 0.09, (0, 0, -0.22), "plant_dark", verts=12, radius_top=0.04))           # абажур (эмаль)
    p.append(L.cyl(W / 2 - 0.008, 0.006, (0, 0, -0.223), "offwhite", verts=12))
    p.append(L.cyl(0.035, 0.03, (0, 0, -H), "glow_lamp", verts=8, glow=True))
    for i, (x, z) in enumerate(((-0.08, -0.17), (0.06, -0.20))):
        p.append(L.spot((x, -0.11 if z < -0.18 else -0.08, z), 0.03, "steel", seed=360 + i))       # сколы эмали
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("lampa_nakalivaniya", lampa_nakalivaniya), ("svetodiodnaya", svetodiodnaya),
                    ("avariynaya", avariynaya), ("nastolnaya", nastolnaya),
                    ("podvesnaya_s_abazhurom", podvesnaya_s_abazhurom)):
        L.make(fn, "machine", "lamp_ceiling", var, size_cm=(W * 100, H * 100), limit="small")   # в ОС не ломается
    L.save_blend("machine", "lamp_ceiling")
