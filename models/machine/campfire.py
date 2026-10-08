"""Костёр `campfire`. Размер — из плана ОС (80 × 50 см). Огонь — светящиеся языки (glow_fire); свет, дым — игра.
Варианты (только idle):
  prostoy        — простой: поленья «шалашом», зола, языки пламени;
  s_kamnyami     — с камнями: кольцо камней, поленья, пламя;
  koster_s_kotlom — с котлом: рогатины, перекладина, котелок над огнём;
  dogorayuschiy  — догорающий: обугленные поленья, тлеющие угли, без пламени.
Запуск: python3 models/machine/campfire.py
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib as L  # noqa: E402

W, H = (s / 100 for s in L.size_cm("campfire"))
ROUGH = {"min_area": 0.006, "k": 0.03, "amp_max": 0.005}


def ash(p, r=0.24):
    p.append(L.cyl(r, 0.015, (0, 0, 0), "stone_dark", verts=10))
    p.append(L.cyl(r * 0.7, 0.018, (0, 0, 0), "soot", verts=8))


def hut(p, n=6, ln=0.40, r=0.03, tilt=58, bark="wood_dark", cut="wood_light", seed=1):
    """Поленья шалашом: каждое лежит на земле и опирается верхом на центр."""
    rnd = random.Random(seed)
    for k in range(n):
        a = 2 * math.pi * k / n + rnd.uniform(-0.2, 0.2)
        base = (math.cos(a) * ln * math.cos(math.radians(tilt)), math.sin(a) * ln * math.cos(math.radians(tilt)), 0.01)
        top = (math.cos(a) * 0.02, math.sin(a) * 0.02, ln * math.sin(math.radians(tilt)) * 0.9)
        p.append(L.tube(base, top, r * rnd.uniform(0.8, 1.1), rnd.choice([bark, bark, "wood"]), verts=5))
        p.append(L.cyl(r * 0.8, 0.006, base, cut, verts=5, rot=(0, 90 - tilt, math.degrees(a))))


def flames(p, h=0.30, seed=2):
    """Языки пламени: 3–4 вытянутых пирамидки разной высоты, ярче в середине."""
    rnd = random.Random(seed)
    for k, (dx, dy, kh, c) in enumerate(((0, 0, 1.0, "glow_lamp"), (-0.05, -0.02, 0.75, "glow_fire"),
                                          (0.05, -0.01, 0.8, "glow_fire"), (0.0, 0.04, 0.6, "glow_fire"))):
        hh = h * kh * rnd.uniform(0.9, 1.05)
        p.append(L.cyl(0.055 if k == 0 else 0.045, hh, (dx, dy, 0.03), c, verts=5, radius_top=0.004,
                       rot=(rnd.uniform(-8, 8), rnd.uniform(-8, 8), rnd.uniform(0, 70)), glow=True))


def stones(p, r=0.33, n=11, seed=3):
    rnd = random.Random(seed)
    for k in range(n):
        a = 2 * math.pi * k / n
        s = rnd.uniform(0.07, 0.095)
        p.append(L.cyl(s * 0.75, s * 0.85, (math.cos(a) * r, math.sin(a) * r, 0), rnd.choice(["stone_dark", "stone_dark", "concrete_dark"]),
                       verts=6, radius_top=s * 0.45, rot=(0, 0, rnd.uniform(0, 60))))


def prostoy():
    p = []
    ash(p, 0.30)
    hut(p, 7, ln=0.42, seed=1)
    flames(p, 0.34)
    for x, y, a in ((-0.33, -0.12, 20), (0.30, -0.14, -15)):                                      # запасные поленья
        p.append(L.tube((x - 0.07 * math.cos(math.radians(a)), y, 0.03), (x + 0.07 * math.cos(math.radians(a)), y + 0.05, 0.03),
                        0.03, "wood_dark", verts=5))
    return p


def s_kamnyami():
    p = []
    ash(p, 0.27)
    stones(p, 0.33)
    hut(p, 6, ln=0.34, seed=4)
    flames(p, 0.30, seed=5)
    return p


def koster_s_kotlom():
    p = []
    ash(p, 0.26)
    stones(p, 0.33, n=10, seed=6)
    hut(p, 5, ln=0.30, seed=7)
    flames(p, 0.20, seed=8)
    for sx in (-1, 1):                                                                             # рогатины
        x = sx * 0.36
        p.append(L.tube((x, 0.0, 0.0), (x, 0.0, 0.44), 0.016, "wood", verts=5))
        p.append(L.tube((x, 0.0, 0.40), (x - sx * 0.04, 0.0, 0.47), 0.012, "wood", verts=5))
        p.append(L.tube((x, 0.0, 0.40), (x + sx * 0.03, 0.0, 0.47), 0.012, "wood", verts=5))
    p.append(L.tube((-0.40, 0.0, 0.43), (0.40, 0.0, 0.43), 0.014, "wood_dark", verts=5))         # перекладина
    p.append(L.tube((0.0, 0.0, 0.43), (0.0, 0.0, 0.36), 0.004, "steel", verts=4))                 # дужка
    p.append(L.cyl(0.11, 0.13, (0, 0, 0.22), "soot", verts=10, radius_top=0.12))                    # котелок
    p.append(L.cyl(0.125, 0.015, (0, 0, 0.345), "steel_dark", verts=10))
    p.append(L.cyl(0.105, 0.004, (0, 0, 0.352), "cloth_beige", verts=10))                           # варево
    for sx in (-1, 1):
        p.append(L.tube((sx * 0.12, 0, 0.35), (0, 0, 0.40), 0.004, "steel", verts=4))
    return p


def dogorayuschiy():
    p = []
    ash(p, 0.30)
    rnd = random.Random(9)
    for k in range(5):                                                                             # обугленные поленья, лежат
        a = rnd.uniform(0, math.pi)
        ln = rnd.uniform(0.22, 0.34)
        x, y = rnd.uniform(-0.08, 0.08), rnd.uniform(-0.06, 0.06)
        p.append(L.tube((x - math.cos(a) * ln / 2, y - math.sin(a) * ln / 2, 0.035 + 0.02 * (k % 2)),
                        (x + math.cos(a) * ln / 2, y + math.sin(a) * ln / 2, 0.035 + 0.02 * (k % 2)), 0.028, "soot", verts=5))
    for k in range(9):                                                                             # тлеющие угли
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, 0.15)
        p.append(L.box((0.035, 0.03, 0.02), (math.cos(a) * r, math.sin(a) * r, 0.015), "glow_fire",
                       rot=(0, 0, rnd.uniform(0, 90)), glow=True, bevel=0))
    return p


if __name__ == "__main__":
    L.new_scene()
    for var, fn in (("prostoy", prostoy), ("s_kamnyami", s_kamnyami), ("koster_s_kotlom", koster_s_kotlom),
                    ("dogorayuschiy", dogorayuschiy)):
        L.make(fn, "machine", "campfire", var, limit="furniture", broken=False, rough=ROUGH)
    L.save_blend("machine", "campfire")
