"""Мелочи кодом, партия «улица и следы» (просьба автора 2026-10-14, пункт 7): бордюры, разметка, столб с проводами,
рельсы (тупик, переезд), цепи, верёвка, кабели, кости, снег, следы. Заготовки, «нарисованная» текстура и выгрузка —
из tools/make_props.py (тот же стиль).

    python3 tools/make_props_street.py            # все → export/<имя>_idle.glb + лист renders/_review/street_props_<дата>.png
    python3 tools/make_props_street.py имя1 имя2  # только эти
"""
import math
import os
import sys

import bpy  # noqa: F401  (mathutils — только после bpy)
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_props as mp  # noqa: E402
from make_props import Mesh, mat, _box  # noqa: E402

CONCRETE = (0.62, 0.6, 0.56)
ASPHALT = (0.24, 0.24, 0.25)
RUST = (0.45, 0.27, 0.16)
STEEL = (0.42, 0.43, 0.45)
WOOD = (0.5, 0.36, 0.22)
BONE = (0.86, 0.82, 0.7)
SNOW = (0.9, 0.93, 0.97)


def _cyl(g, a, b, r, m, sides=8):
    g.tube([a, b], [r, r], m, sides=sides)


# ───────────── улица ─────────────

def curb_straight(rng):
    """Бордюр 1 м: бетонный брусок 15 × 30 см со скосом сверху, сколы по краям, кусок асфальта у основания."""
    g = Mesh("curb_straight")
    c, d = mat("concrete", CONCRETE), mat("concrete_dark", (0.5, 0.48, 0.45))
    _box(g, (0, 0, 0.12), (1.0, 0.15, 0.24), c)
    # скос сверху (к дороге, −Y)
    g.face([(-0.5, -0.075, 0.24), (0.5, -0.075, 0.24), (0.5, -0.03, 0.27), (-0.5, -0.03, 0.27)], c)
    g.face([(-0.5, -0.03, 0.27), (0.5, -0.03, 0.27), (0.5, 0.075, 0.27), (-0.5, 0.075, 0.27)], c)
    g.face([(-0.5, 0.075, 0.24), (-0.5, 0.075, 0.27), (0.5, 0.075, 0.27), (0.5, 0.075, 0.24)], c)
    for k in range(3):                                         # сколы
        x = rng.uniform(-0.4, 0.4)
        g.blob((x, -0.07, 0.25), (0.04, 0.02, 0.02), d, subdiv=0, rng=rng)
    return g.build()


def curb_corner(rng):
    """Угол бордюра: два куска по 50 см под прямым углом, скруглённый угол."""
    g = Mesh("curb_corner")
    c = mat("concrete", CONCRETE)
    _box(g, (-0.2125, 0, 0.135), (0.575, 0.15, 0.27), c)      # кусок вдоль X до угла включительно
    _box(g, (0.0, 0.2875, 0.135), (0.15, 0.425, 0.27), c)     # кусок вдоль Y — от угла, без нахлёста
    return g.build()


def road_marking_dash(rng):
    """Разметка: прерывистая белая полоса 3 м × 15 см (кладётся на асфальт), стёртая местами."""
    g = Mesh("road_marking_dash")
    w, w2 = mat("paint_white", (0.92, 0.91, 0.86)), mat("paint_worn", (0.7, 0.7, 0.68))
    x = -1.5
    while x < 1.5:
        L = min(0.35, 1.5 - x)
        _box(g, (x + L / 2, 0, 0.004), (L - 0.002, 0.15, 0.008), w if rng.random() > 0.25 else w2)
        x += L
    return g.build()


def road_marking_cross(rng):
    """Пешеходный переход: 6 белых полос 2,5 м × 40 см с промежутками (поперёк дороги, вдоль Y)."""
    g = Mesh("road_marking_cross")
    w, w2 = mat("paint_white", (0.92, 0.91, 0.86)), mat("paint_worn", (0.7, 0.7, 0.68))
    for k in range(6):
        x = -1.5 + k * 0.6
        _box(g, (x + 0.2, 0, 0.004), (0.4, 2.5, 0.008), w if k % 3 else w2)
    return g.build()


def pole_power(rng):
    """Деревянный столб ЛЭП 8 м: перекладина, 3 изолятора, обрывки провода; тень от «подкоса»."""
    g = Mesh("pole_power")
    wd, iso, cab = mat("wood_pole", (0.42, 0.3, 0.19)), mat("insulator", (0.75, 0.72, 0.62)), mat("cable", (0.12, 0.12, 0.13))
    g.tube([(0, 0, 0), (0, 0, 4), (0.02, 0, 8)], [0.14, 0.12, 0.1], wd, sides=8)
    _box(g, (0, 0, 7.4), (1.8, 0.12, 0.12), wd)
    for x in (-0.8, 0, 0.8):
        z = 7.46 if x else 7.95
        g.tube([(x, 0, z), (x, 0, z + 0.14)], [0.04, 0.03], iso, sides=6)
    for x in (-0.8, 0.8):                                      # концы провода
        g.tube([(x, 0, 7.6), (x + 0.15, 0, 7.4), (x + 0.2, 0, 7.0)], [0.012] * 3, cab, sides=4, cap=False)
    _box(g, (0, -0.08, 2.4), (0.25, 0.02, 0.35), mat("sign_tin", (0.7, 0.62, 0.2)))    # табличка
    return g.build()


def power_wires_span(rng):
    """Провода между столбами: 3 провисающих провода, пролёт 10 м (концы — на высоте перекладины 7,55 м)."""
    g = Mesh("power_wires_span")
    cab = mat("cable", (0.12, 0.12, 0.13))
    for x0, z0, sag in ((-0.8, 7.55, 0.7), (0, 8.05, 0.6), (0.8, 7.55, 0.75)):
        pts = [(-5 + 10 * t / 12, x0 * 0 + 0, z0 - sag * 4 * (t / 12) * (1 - t / 12)) for t in range(13)]
        pts = [(p[0], x0 * 0.05, p[2]) for p in pts]
        g.tube(pts, [0.012] * 13, cab, sides=4, cap=False)
    return g.build()


# ───────────── рельсы ─────────────

def _sleeper(g, x, m):
    _box(g, (x, 0, 0.06), (0.22, 1.7, 0.12), m)


def _rail(g, x0, x1, y, m):
    _box(g, ((x0 + x1) / 2, y, 0.16), (x1 - x0, 0.07, 0.08), m)
    _box(g, ((x0 + x1) / 2, y, 0.135), (x1 - x0, 0.14, 0.03), m)


def rails_buffer_stop(rng):
    """Тупик: конец пути 3 м с упором — рама из шпал и брёвен, красно-белый щит."""
    g = Mesh("rails_buffer_stop")
    sl, rl, wd = mat("wood_sleeper", (0.38, 0.28, 0.2)), mat("rail_rust", RUST), mat("wood", WOOD)
    red, white = mat("paint_red", (0.72, 0.18, 0.14)), mat("paint_white", (0.9, 0.88, 0.82))
    for k in range(5):
        _sleeper(g, -1.3 + k * 0.6, sl)
    for y in (-0.6, 0.6):
        _rail(g, -1.5, 1.2, y, rl)
        g.tube([(1.2, y, 0.18), (1.45, y, 0.9)], [0.07, 0.07], rl, sides=6)    # загнутый рельс-подкос
    for z in (0.35, 0.65, 0.95):
        _box(g, (1.5, 0, z), (0.22, 1.7, 0.22), wd)
    for k in range(4):
        _box(g, (1.38, -0.6 + k * 0.4, 0.75), (0.03, 0.4, 0.3), red if k % 2 else white)
    return g.build()


def rails_crossing(rng):
    """Переезд: кусок пути 3 м, между рельсами и по бокам — настил из досок (дорога через рельсы)."""
    g = Mesh("rails_crossing")
    sl, rl, wd = mat("wood_sleeper", (0.38, 0.28, 0.2)), mat("rail_rust", RUST), mat("wood_plank", (0.47, 0.36, 0.25))
    for k in range(5):
        _sleeper(g, -1.2 + k * 0.6, sl)
    for y in (-0.6, 0.6):
        _rail(g, -1.5, 1.5, y, rl)
    for y0, y1 in ((-1.4, -0.68), (-0.52, 0.52), (0.68, 1.4)):
        n = max(1, int((y1 - y0) / 0.18))
        for k in range(n):
            y = y0 + (k + 0.5) * (y1 - y0) / n
            _box(g, (0, y, 0.165), (3.0, (y1 - y0) / n - 0.015, 0.04), wd)
    return g.build()


# ───────────── цепи, верёвки, кабели ─────────────

def _link(g, c, along, vertical, m, L=0.06, r=0.022, t=0.007):
    """Звено цепи: вытянутое кольцо в плоскости (along, vertical-или-поперёк)."""
    c, a, b = Vector(c), Vector(along).normalized(), Vector(vertical).normalized()
    pts = []
    for k in range(9):
        th = 2 * math.pi * k / 8
        pts.append(c + a * (math.cos(th) * (L / 2)) + b * (math.sin(th) * r))
    g.tube(pts, [t] * len(pts), m, sides=4, cap=False)


def chain_hanging(rng):
    """Цепь висит со стены/балки, 1 м, внизу — крюк (звенья через одно повёрнуты)."""
    g = Mesh("chain_hanging")
    m = mat("chain_rust", (0.4, 0.3, 0.22))
    n = 18
    for k in range(n):
        z = 1.0 - k * 0.052
        _link(g, (0, 0, z), (0, 0, 1), (1, 0, 0) if k % 2 else (0, 1, 0), m)
    g.tube([(0, 0, 0.06), (0, 0, 0.02), (0.04, 0, -0.01), (0.07, 0, 0.02), (0.07, 0, 0.05)], [0.01] * 5, m, sides=5)
    _box(g, (0, 0.03, 1.04), (0.08, 0.02, 0.06), mat("steel", STEEL))     # скоба крепления
    return g.build()


def chain_pile(rng):
    """Цепь кучей на полу: ~2 м звеньев петлями, ~40 см."""
    g = Mesh("chain_pile")
    m = mat("chain_rust", (0.4, 0.3, 0.22))
    t = 0.0
    for k in range(36):
        t += 0.32
        r = 0.08 + 0.1 * (k % 12) / 12
        c = (math.cos(t) * r, math.sin(t) * r * 0.8, 0.025 + 0.02 * (k // 12))
        d = (-math.sin(t), math.cos(t), 0)
        _link(g, c, d, (0, 0, 1) if k % 2 else (math.cos(t), math.sin(t), 0), m)
    return g.build()


def rope_hanging(rng):
    """Верёвка свисает с крюка, 1,2 м, с петлёй-узлом внизу."""
    g = Mesh("rope_hanging")
    m = mat("rope", (0.72, 0.6, 0.4))
    pts = [(0.015 * math.sin(k * 0.9), 0, 1.2 - k * 0.1) for k in range(10)]
    g.tube(pts, [0.016] * len(pts), m, sides=6)
    loop = [(0.09 * math.sin(2 * math.pi * k / 10), 0, 0.2 - 0.09 + 0.09 * math.cos(2 * math.pi * k / 10)) for k in range(11)]
    g.tube(loop, [0.014] * len(loop), m, sides=6, cap=False)
    g.blob((0, 0, 0.29), (0.035, 0.035, 0.045), m, subdiv=1, rng=rng)
    _box(g, (0, 0.02, 1.22), (0.06, 0.03, 0.05), mat("steel", STEEL))
    return g.build()


def cable_floor(rng):
    """Кабели по полу: 2 провода змейкой 2 м (чёрный и рыжий), изолента на стыке."""
    g = Mesh("cable_floor")
    for col, ph, w in (((0.1, 0.1, 0.11), 0.0, 0.014), ((0.75, 0.4, 0.12), 1.3, 0.011)):
        m = mat(f"cable_{col[0]}", col)
        pts = [(-1 + k * 0.1, 0.12 * math.sin(k * 0.45 + ph), w) for k in range(21)]
        g.tube(pts, [w] * len(pts), m, sides=5)
    _box(g, (0.2, 0.05, 0.015), (0.06, 0.06, 0.03), mat("tape", (0.2, 0.25, 0.55)))
    return g.build()


def cable_hanging(rng):
    """Провода свисают с потолка петлями (вешается на потолок: верх — Z = 0, всё вниз), ~1,2 м."""
    g = Mesh("cable_hanging")
    for k, (col, sag) in enumerate((((0.1, 0.1, 0.11), 0.45), ((0.55, 0.15, 0.12), 0.3), ((0.75, 0.68, 0.2), 0.6))):
        m = mat(f"cable_h{k}", col)
        pts = [(-0.6 + 1.2 * i / 10, 0.04 * k, 0.6 - sag * 4 * (i / 10) * (1 - i / 10)) for i in range(11)]
        g.tube(pts, [0.012] * 11, m, sides=4)
    g.tube([(0.3, 0.1, 0.55), (0.32, 0.1, 0.2), (0.34, 0.1, 0.05)], [0.01] * 3, mat("cable_h0", (0.1, 0.1, 0.11)), sides=4)
    return g.build()


# ───────────── кости, снег, следы ─────────────

def _long_bone(g, a, b, m, r=0.018):
    a, b = Vector(a), Vector(b)
    g.tube([a, b], [r, r * 0.8], m, sides=6)
    for p in (a, b):
        g.blob(p, (r * 1.7, r * 1.7, r * 1.5), m, subdiv=0)


def bones_pile(rng):
    """Кости: череп, длинные кости, рёбра — россыпь ~70 см."""
    g = Mesh("bones_pile")
    m, d = mat("bone", BONE), mat("bone_dark", (0.3, 0.26, 0.22))
    g.blob((0.12, 0.05, 0.08), (0.08, 0.1, 0.075), m, subdiv=1, jitter=0.08, rng=rng)       # череп
    for x, y in ((0.09, -0.04), (0.15, -0.04)):                                               # глазницы
        g.blob((x, y - 0.045, 0.09), (0.02, 0.012, 0.02), d, subdiv=0, rng=rng)
    g.blob((0.12, -0.04, 0.03), (0.05, 0.04, 0.02), m, subdiv=0, rng=rng)                    # челюсть
    for k in range(4):
        a = rng.uniform(0, math.pi)
        c = Vector((rng.uniform(-0.3, 0.1), rng.uniform(-0.2, 0.2), 0.02))
        dv = Vector((math.cos(a), math.sin(a), 0)) * rng.uniform(0.16, 0.22)
        _long_bone(g, c - dv, c + dv, m)
    for k in range(5):                                                                       # рёбра — дуги
        c = Vector((-0.1 + 0.05 * k, 0.22, 0.015))
        pts = [c + Vector((0.12 * math.sin(t), -0.06 * (1 - math.cos(t)), 0.03 * math.sin(t))) for t in (0, 0.6, 1.2, 1.8)]
        g.tube(pts, [0.008] * 4, m, sides=4)
    return g.build()


def snow_pile(rng):
    """Сугроб ~1,2 × 0,5 м: бугристая куча снега."""
    g = Mesh("snow_pile")
    s, s2 = mat("snow", SNOW), mat("snow_shadow", (0.78, 0.84, 0.92))
    g.blob((0, 0, 0.0), (0.7, 0.45, 0.24), s, subdiv=2, jitter=0.1, rng=rng)
    for k in range(4):
        g.blob((rng.uniform(-0.6, 0.6), rng.uniform(-0.3, 0.3), -0.05), (0.28, 0.22, 0.12), s2 if k % 2 else s, subdiv=1, jitter=0.15, rng=rng)
    return g.build()


def snow_patch(rng):
    """Снег пятном на земле ~1,5 м (тонкий слой — на траву, крышу машины, у стены)."""
    g = Mesh("snow_patch")
    g.disc((0, 0, 0), 0.75, 0.5, 0.025, mat("snow", SNOW), n=16, jitter=0.25, rng=rng)
    g.disc((0.25, 0.1, 0.02), 0.3, 0.2, 0.02, mat("snow_shadow", (0.78, 0.84, 0.92)), n=10, jitter=0.3, rng=rng)
    return g.build()


def _print(g, c, a, m, L=0.26, W=0.1):
    """Отпечаток подошвы: подошва и каблук — тонкие плашки."""
    c = Vector(c)
    f = Vector((math.cos(a), math.sin(a), 0))
    s = Vector((-f.y, f.x, 0))
    for off, ln, w in ((0.05, 0.15, W), (-0.09, 0.07, W * 0.85)):
        p = c + f * off
        _box(g, p, (ln, w, 0.006), m, rz=a)


def footprints_mud(rng):
    """Следы ботинок в грязи — 6 шагов по прямой ~2,5 м (кладутся на землю/пол)."""
    g = Mesh("footprints_mud")
    m = mat("mud_wet", (0.25, 0.2, 0.14))
    for k in range(6):
        _print(g, (-1.1 + k * 0.42, 0.09 if k % 2 else -0.09, 0.003), rng.uniform(-0.08, 0.08), m)
    return g.build()


def footprints_snow(rng):
    """Следы на снегу — 6 шагов по полосе снега ~2,6 м."""
    g = Mesh("footprints_snow")
    g.disc((0, 0, 0), 1.35, 0.35, 0.02, mat("snow", SNOW), n=18, jitter=0.12, rng=rng)
    m = mat("snow_print", (0.62, 0.7, 0.82))
    for k in range(6):
        _print(g, (-1.05 + k * 0.42, 0.09 if k % 2 else -0.09, 0.022), rng.uniform(-0.08, 0.08), m)
    return g.build()


NEW = {f.__name__: f for f in (curb_straight, curb_corner, road_marking_dash, road_marking_cross, pole_power,
                                power_wires_span, rails_buffer_stop, rails_crossing, chain_hanging, chain_pile,
                                rope_hanging, cable_floor, cable_hanging, bones_pile, snow_pile, snow_patch,
                                footprints_mud, footprints_snow)}

if __name__ == "__main__":
    mp.MODELS.clear()
    mp.MODELS.update(NEW)
    mp.WALL.clear()
    mp.WALL.update({"chain_hanging", "rope_hanging"})
    os.environ.setdefault("SHEET", "street_props")
    sys.argv = [sys.argv[0]] + ([a for a in sys.argv[1:] if not a.startswith("-")] or list(NEW))
    mp.main()
