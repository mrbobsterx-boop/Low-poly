"""Модели, нарисованные кодом (не Tripo): кусты у воды и стрелы, партия 1 — трава и природные мелочи (просьбы автора
2026-10-14). Blender как модуль bpy.

Запуск (из корня репозитория):
    python3 tools/make_props.py            # все → export/<имя>_idle.glb + лист превью renders/_review/props_<дата>.png
    python3 tools/make_props.py имя1 имя2  # только эти

Стиль — как у моделей Tripo «кровать-образец»: low poly, плоские грани, свои цвета, без блеска (шероховатость 1).
Перед — к −Y, точка опоры — низ по центру, 1 единица = 1 м, +Y вверх в glTF.
"""
import datetime
import math
import os
import random
import sys

import bpy
import bmesh
from mathutils import Matrix, Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))


# ───────────────────────── заготовки ─────────────────────────

_mats = {}


def mat(name, rgb):
    if name in _mats:
        return _mats[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*[c ** 2.2 for c in rgb], 1.0)   # цвета заданы как на картинке (sRGB)
    b.inputs["Roughness"].default_value = 1.0
    b.inputs["Metallic"].default_value = 0.0
    _mats[name] = m
    return m


class Mesh:
    """Набор граней одного объекта (у каждой — свой материал)."""

    def __init__(self, name):
        self.bm = bmesh.new()
        self.name = name
        self.mats = []

    def _mi(self, m):
        if m not in self.mats:
            self.mats.append(m)
        return self.mats.index(m)

    def face(self, pts, m):
        vs = [self.bm.verts.new(p) for p in pts]
        f = self.bm.faces.new(vs)
        f.material_index = self._mi(m)
        return f

    def tube(self, path, radii, m, sides=5, cap=True):
        """Трубка по точкам path с радиусами radii (сужение к концу) — стебель, ветка, древко."""
        rings = []
        for i, p in enumerate(path):
            p = Vector(p)
            d = (Vector(path[min(i + 1, len(path) - 1)]) - Vector(path[max(i - 1, 0)])).normalized()
            a = d.orthogonal().normalized()
            b = d.cross(a).normalized()
            r = radii[i]
            rings.append([self.bm.verts.new(p + (a * math.cos(t) + b * math.sin(t)) * r)
                          for t in [2 * math.pi * k / sides for k in range(sides)]])
        mi = self._mi(m)
        for r0, r1 in zip(rings, rings[1:]):
            for k in range(sides):
                f = self.bm.faces.new([r0[k], r0[(k + 1) % sides], r1[(k + 1) % sides], r1[k]])
                f.material_index = mi
        if cap:
            for r in (rings[0], rings[-1][::-1]):
                if radii[rings.index(r) if r in rings else -1] > 1e-5:
                    f = self.bm.faces.new(r[::-1])
                    f.material_index = mi

    def blob(self, c, size, m, subdiv=1, jitter=0.18, rng=None, squash=1.0):
        """Комок листвы / камень: икосфера, вершины чуть сдвинуты."""
        rng = rng or random
        tmp = bmesh.new()
        bmesh.ops.create_icosphere(tmp, subdivisions=subdiv, radius=1.0)
        mi = self._mi(m)
        vmap = {}
        for v in tmp.verts:
            q = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2] * squash))
            q *= 1.0 + rng.uniform(-jitter, jitter)
            vmap[v] = self.bm.verts.new(Vector(c) + q)
        for f in tmp.faces:
            nf = self.bm.faces.new([vmap[v] for v in f.verts])
            nf.material_index = mi
        tmp.free()

    def blade(self, base, direction, length, width, bend, m, segs=3):
        """Лист травы / осоки: узкая полоса, сужается к концу и гнётся наружу (две стороны — видно с обеих)."""
        base = Vector(base)
        d = Vector(direction).normalized()
        side = Vector((0, 0, 1)).cross(d)
        if side.length < 1e-4:
            side = Vector((1, 0, 0))
        side.normalize()
        out = Vector((d.x, d.y, 0))
        out = out.normalized() if out.length > 1e-4 else Vector((0, -1, 0))
        pts = []
        for i in range(segs + 1):
            t = i / segs
            p = base + Vector((0, 0, length * t)) + out * (bend * length * t * t)
            w = width * (1 - t) * 0.5
            pts.append((p - side * w, p + side * w))
        for (a0, b0), (a1, b1) in zip(pts, pts[1:]):
            self.face([a0, b0, b1, a1] if (a1 - b1).length > 1e-5 else [a0, b0, b1], m)

    def leaf(self, base, d, up, length, width, m, tip_bend=0.0):
        """Плоский лист-ромб от base в сторону d (up — «лицо» листа), две стороны видно (материал двусторонний)."""
        base, d, up = Vector(base), Vector(d).normalized(), Vector(up).normalized()
        side = d.cross(up).normalized()
        mid = base + d * length * 0.45
        tip = base + d * length - up * tip_bend * length
        return self.face([base, mid + side * width * 0.5, tip, mid - side * width * 0.5], m)

    def disc(self, c, rx, ry, h, m, n=9, jitter=0.25, rng=None):
        """Плоская неровная «лепёшка» на земле (мох, грязь, кусок асфальта): верх, бока, без низа."""
        rng = rng or random
        c = Vector(c)
        ring = []
        for k in range(n):
            t = 2 * math.pi * k / n
            r = 1.0 + rng.uniform(-jitter, jitter)
            ring.append(Vector((c.x + math.cos(t) * rx * r, c.y + math.sin(t) * ry * r, c.z)))
        top = [q + Vector((0, 0, h)) for q in ring]
        self.face(top, m)
        for k in range(n):
            self.face([ring[k], ring[(k + 1) % n], top[(k + 1) % n], top[k]], m)

    def build(self):
        me = bpy.data.meshes.new(self.name)
        bmesh.ops.remove_doubles(self.bm, verts=self.bm.verts, dist=1e-6)
        self.bm.normal_update()
        self.bm.to_mesh(me)
        self.bm.free()
        for m in self.mats:
            me.materials.append(m)
        for p in me.polygons:
            p.use_smooth = False
        ob = bpy.data.objects.new(self.name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob


# ───────────────────────── модели ─────────────────────────

def reeds(rng):
    """Камыш с рогозом: пучок стеблей (часть — с коричневыми «початками»), длинные листья, тёмная кочка."""
    g = Mesh("bush_water_reeds")
    stem, leaf, leaf2 = mat("reed_stem", (0.42, 0.5, 0.22)), mat("reed_leaf", (0.33, 0.45, 0.17)), mat("reed_leaf_dry", (0.6, 0.55, 0.3))
    head, mud = mat("cattail_head", (0.36, 0.2, 0.1)), mat("mud_clump", (0.22, 0.18, 0.12))
    g.blob((0, 0, 0.02), (0.38, 0.3, 0.09), mud, rng=rng)
    for i in range(16):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0.0, 0.3)
        x, y = math.cos(a) * r, math.sin(a) * r * 0.75
        h = rng.uniform(0.9, 1.55)
        lean = Vector((x, y, 0)) * 0.35 + Vector((rng.uniform(-0.06, 0.06), rng.uniform(-0.06, 0.06), 0))
        path = [(x + lean.x * t * t, y + lean.y * t * t, h * t) for t in (0, 0.35, 0.7, 1.0)]
        g.tube(path, [0.012, 0.01, 0.008, 0.003], stem, sides=4)
        if i % 3 == 0:   # рогоз: коричневый «початок» под макушкой
            p0, p1 = Vector(path[2]), Vector(path[3])
            c0 = p0.lerp(p1, 0.45)
            c1 = p0.lerp(p1, 0.85)
            g.tube([c0, c0.lerp(c1, 0.5), c1], [0.026, 0.03, 0.024], head, sides=6)
    for i in range(22):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0.02, 0.3)
        base = (math.cos(a) * r, math.sin(a) * r * 0.75, 0.04)
        g.blade(base, (math.cos(a), math.sin(a), 0), rng.uniform(0.55, 1.1), rng.uniform(0.035, 0.05),
                rng.uniform(0.25, 0.6), leaf if i % 5 else leaf2)
    return g.build()


def willow(rng):
    """Ива-куст у воды: несколько тонких стволиков из одной кочки, свисающие узкие комки листвы (серо-зелёные)."""
    g = Mesh("bush_willow")
    bark, l1, l2 = mat("willow_bark", (0.35, 0.28, 0.2)), mat("willow_leaf", (0.45, 0.55, 0.3)), mat("willow_leaf_b", (0.55, 0.62, 0.4))
    g.blob((0, 0, 0.04), (0.3, 0.25, 0.1), mat("mud_clump", (0.22, 0.18, 0.12)), rng=rng)
    for i in range(6):
        a = 2 * math.pi * i / 6 + rng.uniform(-0.3, 0.3)
        out = Vector((math.cos(a), math.sin(a) * 0.7, 0))
        h = rng.uniform(0.9, 1.35)
        path = [Vector((0, 0, 0.05)) + out * 0.05, out * 0.18 + Vector((0, 0, h * 0.45)),
                out * 0.4 + Vector((0, 0, h * 0.85)), out * 0.55 + Vector((0, 0, h))]
        g.tube(path, [0.035, 0.025, 0.016, 0.008], bark, sides=5)
        for k in range(5):   # свисающие пряди листвы вдоль верхней части ветки
            t = 0.45 + 0.13 * k
            p = path[1].lerp(path[3], min(t, 1.0)) if t < 1 else path[3]
            for j in range(2):
                c = p + Vector((rng.uniform(-0.1, 0.1), rng.uniform(-0.08, 0.08), -0.16 - 0.1 * j))
                g.blob(c, (0.07, 0.06, 0.2), l1 if (i + k + j) % 3 else l2, rng=rng, jitter=0.25)
    for k in range(6):   # середина куста
        a = 2 * math.pi * k / 6
        g.blob((math.cos(a) * 0.18, math.sin(a) * 0.13, 0.95 + 0.1 * (k % 2)), (0.16, 0.13, 0.13), l1, rng=rng, jitter=0.25)
    return g.build()


def sedge(rng):
    """Осока с камнями у воды: веер жёстких листьев, пара мокрых камней."""
    g = Mesh("bush_water_sedge")
    l1, l2 = mat("sedge_leaf", (0.36, 0.48, 0.2)), mat("sedge_leaf_b", (0.5, 0.55, 0.25))
    stone = mat("stone_wet", (0.38, 0.38, 0.36))
    g.blob((0, 0, 0.02), (0.22, 0.18, 0.06), mat("mud_clump", (0.22, 0.18, 0.12)), rng=rng)
    for i in range(30):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0.0, 0.14)
        g.blade((math.cos(a) * r, math.sin(a) * r, 0.03), (math.cos(a), math.sin(a), 0), rng.uniform(0.3, 0.6),
                rng.uniform(0.02, 0.03), rng.uniform(0.35, 0.9), l1 if i % 3 else l2)
    g.blob((0.26, -0.08, 0.05), (0.12, 0.1, 0.08), stone, rng=rng, subdiv=1, jitter=0.12)
    g.blob((-0.22, 0.05, 0.04), (0.09, 0.08, 0.06), stone, rng=rng, subdiv=1, jitter=0.12)
    return g.build()


def _arrow(g, origin, d, length=0.75, shaft=None, head=None, feather=None, feather2=None):
    """Стрела вдоль d: древко, наконечник (листовидный, железо), три пера у хвоста и ушко."""
    o = Vector(origin)
    d = Vector(d).normalized()
    a = d.orthogonal().normalized()
    b = d.cross(a).normalized()
    tail, tip = o, o + d * length
    g.tube([tail, tail.lerp(tip, 0.5), tip - d * 0.06], [0.0055, 0.0055, 0.005], shaft, sides=6)
    hb = tip - d * 0.065   # наконечник: ромб в двух плоскостях + основание
    for s in (a, b):
        g.face([hb + s * 0.014, tip, hb - s * 0.014, hb - d * 0.015], head)
        g.face([hb - s * 0.014, tip, hb + s * 0.014, hb - d * 0.015], head)
    g.tube([tail - d * 0.01, tail + d * 0.012], [0.007, 0.007], mat("arrow_nock", (0.2, 0.16, 0.12)), sides=6)
    for k in range(3):   # перья: трапеции под 120°
        ang = 2 * math.pi * k / 3
        s = a * math.cos(ang) + b * math.sin(ang)
        p0, p1 = tail + d * 0.03, tail + d * 0.17
        m = feather if k else feather2
        q = [p0 + s * 0.005, p1 + s * 0.005, p1 + s * 0.012, p0 + s * 0.026]
        g.face(q, m)
        g.face(q[::-1], m)


def arrow(rng):
    """Одна стрела, 75 см, лежит на полу (вдоль X)."""
    g = Mesh("arrow_wood")
    _arrow(g, (-0.375, 0, 0.012), (1, 0, 0), shaft=mat("arrow_shaft", (0.62, 0.47, 0.3)), head=mat("arrow_head", (0.42, 0.42, 0.44)),
           feather=mat("feather_white", (0.85, 0.82, 0.75)), feather2=mat("feather_red", (0.62, 0.16, 0.12)))
    return g.build()


def arrows_bundle(rng):
    """Пучок из 6 стрел, перевязан бечёвкой, стоит наконечниками вверх (можно прислонить к стене / положить)."""
    g = Mesh("arrows_bundle")
    sh, hd = mat("arrow_shaft", (0.62, 0.47, 0.3)), mat("arrow_head", (0.42, 0.42, 0.44))
    fw, fr = mat("feather_white", (0.85, 0.82, 0.75)), mat("feather_red", (0.62, 0.16, 0.12))
    for i in range(6):
        a = 2 * math.pi * i / 6
        o = Vector((math.cos(a) * 0.018, math.sin(a) * 0.018, 0.0))
        d = Vector((math.cos(a) * 0.05, math.sin(a) * 0.05, 1))
        _arrow(g, o, d, shaft=sh, head=hd, feather=fw if i % 2 else mat("feather_grey", (0.5, 0.5, 0.48)), feather2=fr)
    twine = mat("twine", (0.7, 0.6, 0.4))
    for z in (0.3, 0.45):   # бечёвка: два витка
        ring = [(math.cos(t) * 0.032, math.sin(t) * 0.032, z) for t in [2 * math.pi * k / 10 for k in range(11)]]
        g.tube(ring, [0.005] * len(ring), twine, sides=4, cap=False)
    return g.build()


# ───────────── партия 1: трава и природные мелочи (автор 2026-10-14) ─────────────

GREENS = [(0.36, 0.5, 0.2), (0.42, 0.56, 0.22), (0.3, 0.44, 0.18), (0.5, 0.58, 0.26)]
DRY = [(0.72, 0.62, 0.36), (0.64, 0.54, 0.3), (0.78, 0.7, 0.44)]


def _tuft(g, rng, c, n, lo, hi, cols, spread=0.08, bend=(0.2, 0.7), width=(0.018, 0.03), name="grass"):
    """Пучок травинок вокруг c."""
    mats = [mat(f"{name}_{i}", col) for i, col in enumerate(cols)]
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0, spread)
        base = Vector(c) + Vector((math.cos(a) * r, math.sin(a) * r, 0))
        g.blade(base, (math.cos(a), math.sin(a), 0), rng.uniform(lo, hi), rng.uniform(*width), rng.uniform(*bend), mats[i % len(mats)])


def grass_short(rng):
    """Трава низкая: густой пучок 10–20 см."""
    g = Mesh("grass_short")
    for k in range(3):
        _tuft(g, rng, (rng.uniform(-0.15, 0.15), rng.uniform(-0.08, 0.08), 0), 18, 0.08, 0.2, GREENS, spread=0.1)
    return g.build()


def grass_tall(rng):
    """Трава высокая: 40–75 см, у части — метёлки семян."""
    g = Mesh("grass_tall")
    _tuft(g, rng, (0, 0, 0), 40, 0.35, 0.75, GREENS, spread=0.14, bend=(0.15, 0.45), width=(0.02, 0.032))
    seed = mat("grass_seed", (0.62, 0.58, 0.38))
    stem = mat("grass_stem", (0.48, 0.55, 0.28))
    for i in range(7):
        a = rng.uniform(0, 2 * math.pi)
        base = Vector((math.cos(a) * 0.06, math.sin(a) * 0.06, 0))
        h = rng.uniform(0.6, 0.85)
        lean = Vector((math.cos(a), math.sin(a), 0)) * rng.uniform(0.05, 0.15)
        top = base + lean + Vector((0, 0, h))
        g.tube([base, base + lean * 0.4 + Vector((0, 0, h * 0.5)), top], [0.005, 0.004, 0.003], stem, sides=4)
        g.tube([top, top + lean * 0.3 + Vector((0, 0, 0.1))], [0.012, 0.004], seed, sides=5)
    return g.build()


def grass_dry(rng):
    """Трава сухая жёлтая: полёгшая, 20–50 см."""
    g = Mesh("grass_dry")
    for k in range(2):
        _tuft(g, rng, (rng.uniform(-0.12, 0.12), rng.uniform(-0.05, 0.05), 0), 26, 0.2, 0.5, DRY, spread=0.12,
              bend=(0.5, 1.1), name="grass_dry")
    return g.build()


def grass_patchy(rng):
    """Трава клочками у дороги: полоса ~1 м — несколько пучков разной высоты на пятне земли, зелёная с сухой."""
    g = Mesh("grass_patchy")
    g.disc((0, 0, 0), 0.55, 0.2, 0.015, mat("dirt", (0.36, 0.29, 0.2)), n=11, rng=rng)
    for k in range(5):
        x = -0.45 + 0.22 * k + rng.uniform(-0.05, 0.05)
        _tuft(g, rng, (x, rng.uniform(-0.08, 0.08), 0.01), 14, 0.08, rng.uniform(0.2, 0.4),
              GREENS[:2] + DRY[:1] if k % 2 else GREENS, spread=0.07)
    return g.build()


def grass_asphalt(rng):
    """Трава сквозь трещину в асфальте: кусок асфальта с трещиной, травинки растут вдоль трещины."""
    g = Mesh("grass_asphalt")
    asph = mat("asphalt", (0.27, 0.27, 0.28))
    crack = mat("asphalt_crack", (0.1, 0.09, 0.08))
    pts = [Vector((-0.42 + 0.84 * t, 0.08 * math.sin(t * 9 + 1) + rng.uniform(-0.03, 0.03), 0)) for t in [k / 8 for k in range(9)]]
    for half, sgn in ((0, 1), (1, -1)):   # две плиты по сторонам трещины
        edge = [p + Vector((0, 0.015 * sgn, 0)) for p in pts]
        outer = [Vector((p.x, 0.32 * sgn + rng.uniform(-0.03, 0.03), 0)) for p in edge]
        for a0, a1, b0, b1 in zip(edge, edge[1:], outer, outer[1:]):
            q = [a0, a1, b1, b0] if sgn > 0 else [a0, b0, b1, a1]
            g.face([v + Vector((0, 0, 0.02)) for v in q], asph)
    for a0, a1 in zip(pts, pts[1:]):
        g.face([a0 + Vector((0, -0.016, 0.004)), a1 + Vector((0, -0.016, 0.004)), a1 + Vector((0, 0.016, 0.004)), a0 + Vector((0, 0.016, 0.004))], crack)
    for k in range(6):
        p = pts[1 + k]
        _tuft(g, rng, (p.x, p.y, 0.005), 8, 0.06, 0.22, GREENS, spread=0.02, width=(0.012, 0.02))
    return g.build()


def _stalk_with_leaves(g, rng, base, h, stem, leaf_m, pairs, leaf_len, leaf_w, droop=0.25):
    base = Vector(base)
    lean = Vector((rng.uniform(-0.06, 0.06), rng.uniform(-0.06, 0.06), 0))
    path = [base + lean * t * t + Vector((0, 0, h * t)) for t in (0, 0.33, 0.66, 1.0)]
    g.tube(path, [0.009, 0.008, 0.006, 0.003], stem, sides=4)
    rot = rng.uniform(0, math.pi)
    for k in range(pairs):
        t = 0.25 + 0.7 * k / max(pairs, 1)
        p = path[0].lerp(path[3], t)
        L = leaf_len * (1.15 - 0.6 * t)
        for sgn in (1, -1):
            ang = rot + k * math.pi / 2 + (0 if sgn > 0 else math.pi)
            d = Vector((math.cos(ang), math.sin(ang), -droop))
            g.leaf(p, d, (0, 0, 1), L, leaf_w * (1.15 - 0.6 * t), leaf_m, tip_bend=0.15)
    return path[3]


def weed_nettle(rng):
    """Крапива: несколько стеблей 50–80 см, парные листья-сердечки с зазубринами (ромбы)."""
    g = Mesh("weed_nettle")
    stem, l1, l2 = mat("nettle_stem", (0.34, 0.42, 0.2)), mat("nettle_leaf", (0.27, 0.42, 0.16)), mat("nettle_leaf_b", (0.33, 0.48, 0.2))
    for i in range(7):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0, 0.16)
        _stalk_with_leaves(g, rng, (math.cos(a) * r, math.sin(a) * r, 0), rng.uniform(0.45, 0.8), stem, l1 if i % 2 else l2, 5, 0.12, 0.07)
    return g.build()


def weed_burdock(rng):
    """Лопухи: большие широкие листья у земли и пара стеблей с колючими фиолетовыми шариками."""
    g = Mesh("weed_burdock")
    l1, l2 = mat("burdock_leaf", (0.3, 0.45, 0.2)), mat("burdock_leaf_b", (0.36, 0.5, 0.24))
    stem, burr = mat("burdock_stem", (0.45, 0.35, 0.3)), mat("burdock_burr", (0.48, 0.3, 0.45))
    for i in range(7):
        a = 2 * math.pi * i / 7 + rng.uniform(-0.2, 0.2)
        d = Vector((math.cos(a), math.sin(a), 0.35))
        base = Vector((0, 0, 0.03))
        L = rng.uniform(0.38, 0.52)
        g.tube([base, base + d * 0.12], [0.012, 0.01], stem, sides=4)
        g.leaf(base + d * 0.1, (d.x, d.y, 0.15), (0, 0, 1), L, L * 0.75, l1 if i % 2 else l2, tip_bend=0.2)
    for k in range(2):
        top = _stalk_with_leaves(g, rng, (rng.uniform(-0.06, 0.06), rng.uniform(-0.06, 0.06), 0), rng.uniform(0.7, 0.9), stem, l2, 2, 0.16, 0.11)
        for j in range(4):
            c = top + Vector((rng.uniform(-0.07, 0.07), rng.uniform(-0.07, 0.07), rng.uniform(-0.1, 0.02)))
            g.blob(c, (0.028, 0.028, 0.028), burr, subdiv=1, jitter=0.35, rng=rng)
    return g.build()


def _flower(g, c, petals, r, petal_m, center_m, n=8, cup=0.15):
    """Цветок: кружок лепестков вокруг серединки (смотрит вверх, чуть чашечкой)."""
    c = Vector(c)
    for k in range(n):
        a = 2 * math.pi * k / n
        d = Vector((math.cos(a), math.sin(a), cup))
        g.leaf(c, d, (0, 0, 1), r, r * 0.45, petal_m)
    g.blob(c + Vector((0, 0, 0.004)), (r * 0.3, r * 0.3, r * 0.18), center_m, subdiv=1, jitter=0.1)


def flowers_dandelion(rng):
    """Одуванчики: розетка зубчатых листьев у земли, жёлтые головки и пара белых пушистых шариков."""
    g = Mesh("flowers_dandelion")
    leaf_m, stem = mat("dand_leaf", (0.33, 0.5, 0.2)), mat("dand_stem", (0.42, 0.55, 0.26))
    yel, puff = mat("dand_yellow", (0.95, 0.78, 0.15)), mat("dand_puff", (0.92, 0.92, 0.88))
    for i in range(10):
        a = 2 * math.pi * i / 10 + rng.uniform(-0.15, 0.15)
        g.leaf((0, 0, 0.01), (math.cos(a), math.sin(a), 0.12), (0, 0, 1), rng.uniform(0.14, 0.2), 0.05, leaf_m, tip_bend=-0.05)
    for i in range(7):
        a = rng.uniform(0, 2 * math.pi)
        lean = Vector((math.cos(a), math.sin(a), 0)) * rng.uniform(0.03, 0.09)
        h = rng.uniform(0.14, 0.28)
        top = lean + Vector((0, 0, h))
        g.tube([Vector((0, 0, 0)), lean * 0.4 + Vector((0, 0, h * 0.5)), top], [0.004, 0.0035, 0.003], stem, sides=4)
        if i < 5:
            g.blob(top, (0.022, 0.022, 0.012), yel, subdiv=1, jitter=0.15, rng=rng)
        else:
            g.blob(top + Vector((0, 0, 0.012)), (0.02, 0.02, 0.02), puff, subdiv=2, jitter=0.1, rng=rng)
    return g.build()


def flowers_daisy(rng):
    """Ромашки: пучок травы и 8 цветков на тонких стеблях (белые лепестки, жёлтая серединка)."""
    g = Mesh("flowers_daisy")
    _tuft(g, rng, (0, 0, 0), 16, 0.08, 0.2, GREENS, spread=0.1)
    stem, white, yel = mat("daisy_stem", (0.4, 0.55, 0.24)), mat("daisy_white", (0.95, 0.94, 0.9)), mat("daisy_yellow", (0.95, 0.75, 0.2))
    for i in range(8):
        a = rng.uniform(0, 2 * math.pi)
        base = Vector((math.cos(a) * 0.06, math.sin(a) * 0.06, 0))
        lean = Vector((math.cos(a), math.sin(a), 0)) * rng.uniform(0.02, 0.1)
        h = rng.uniform(0.22, 0.4)
        top = base + lean + Vector((0, 0, h))
        g.tube([base, base + lean * 0.4 + Vector((0, 0, h * 0.5)), top], [0.004, 0.0035, 0.003], stem, sides=4)
        _flower(g, top, 10, 0.03, white, yel, n=10, cup=0.1)
    return g.build()


def flowers_fireweed(rng):
    """Иван-чай: высокие стебли 0,8–1,2 м, узкие листья, сверху — розово-фиолетовые колосья цветков."""
    g = Mesh("flowers_fireweed")
    stem, leaf_m = mat("fw_stem", (0.42, 0.32, 0.3)), mat("fw_leaf", (0.32, 0.47, 0.22))
    pinks = [mat("fw_pink", (0.85, 0.35, 0.6)), mat("fw_pink_b", (0.72, 0.3, 0.62))]
    for i in range(6):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0, 0.15)
        top = _stalk_with_leaves(g, rng, (math.cos(a) * r, math.sin(a) * r, 0), rng.uniform(0.75, 1.2), stem, leaf_m, 5, 0.14, 0.03, droop=0.1)
        for k in range(7):   # колос: цветки по спирали, к верху мельче
            t = k / 7
            ang = k * 2.4
            c = top - Vector((0, 0, 0.28 * (1 - t))) + Vector((math.cos(ang), math.sin(ang), 0)) * 0.025 * (1 - t * 0.6)
            g.blob(c, (0.022 * (1 - t * 0.5),) * 3, pinks[(i + k) % 2], subdiv=1, jitter=0.2, rng=rng)
    return g.build()


def vine_wall(rng):
    """Вьюн по стене (вешается на стену): извилистые стебли снизу вверх ~1 × 1,5 м, листья-сердечки."""
    g = Mesh("vine_wall")
    stem, l1, l2 = mat("vine_stem", (0.38, 0.3, 0.2)), mat("vine_leaf", (0.3, 0.48, 0.2)), mat("vine_leaf_b", (0.4, 0.55, 0.24))
    for i in range(5):
        x0 = -0.4 + 0.2 * i + rng.uniform(-0.05, 0.05)
        h = rng.uniform(0.9, 1.5)
        path = []
        for k in range(8):
            t = k / 7
            path.append(Vector((x0 + 0.12 * math.sin(t * 6 + i) + rng.uniform(-0.02, 0.02), -0.02, h * t)))
        g.tube(path, [0.009 - 0.0008 * k for k in range(8)], stem, sides=4)
        for k in range(1, 8):
            for j in range(2):
                p = path[k - 1].lerp(path[k], 0.5 * j + 0.25)
                ang = rng.uniform(0, 2 * math.pi)
                d = Vector((math.cos(ang), -0.25, math.sin(ang) * 0.8 + 0.2))
                g.leaf(p, d, (0, -1, 0), rng.uniform(0.06, 0.1), 0.06, l1 if (k + j) % 2 else l2)
    return g.build()


def fern(rng):
    """Папоротник: 8 изогнутых вай (листьев) из одной точки, по бокам — мелкие листочки."""
    g = Mesh("fern")
    stem, l1, l2 = mat("fern_stem", (0.3, 0.4, 0.18)), mat("fern_leaf", (0.28, 0.48, 0.2)), mat("fern_leaf_b", (0.36, 0.55, 0.22))
    for i in range(8):
        a = 2 * math.pi * i / 8 + rng.uniform(-0.2, 0.2)
        out = Vector((math.cos(a), math.sin(a), 0))
        L = rng.uniform(0.45, 0.65)
        path = [out * L * 0.8 * t + Vector((0, 0, L * (1.6 * t - 1.1 * t * t) + 0.02)) for t in [k / 6 for k in range(7)]]
        g.tube(path, [0.006 - 0.0007 * k for k in range(7)], stem, sides=4)
        side = out.cross(Vector((0, 0, 1))).normalized()
        for k in range(1, 7):
            p = path[k]
            w = 0.13 * (1.1 - k / 7)
            for sgn in (1, -1):
                g.leaf(p, side * sgn + Vector((0, 0, -0.1)) + out * 0.3, (0, 0, 1), w, w * 0.5, l1 if k % 2 else l2)
    return g.build()


def mushrooms(rng):
    """Грибы кучкой: 5 штук разного размера, светлые ножки, коричневые и рыжие шляпки."""
    g = Mesh("mushrooms")
    st = mat("mush_stem", (0.88, 0.84, 0.74))
    caps = [mat("mush_cap", (0.55, 0.33, 0.18)), mat("mush_cap_b", (0.75, 0.42, 0.16)), mat("mush_cap_c", (0.45, 0.3, 0.2))]
    g.disc((0, 0, 0), 0.15, 0.12, 0.01, mat("dirt", (0.36, 0.29, 0.2)), rng=rng)
    for i in range(5):
        a = 2 * math.pi * i / 5 + rng.uniform(-0.3, 0.3)
        r = 0.03 + 0.06 * (i % 3) / 2
        base = Vector((math.cos(a) * r, math.sin(a) * r, 0.005))
        s = rng.uniform(0.6, 1.2)
        h = 0.07 * s
        lean = Vector((math.cos(a), math.sin(a), 0)) * 0.015 * s
        g.tube([base, base + lean + Vector((0, 0, h))], [0.012 * s, 0.009 * s], st, sides=6)
        g.blob(base + lean + Vector((0, 0, h + 0.008 * s)), (0.04 * s, 0.04 * s, 0.022 * s), caps[i % 3], subdiv=1, jitter=0.08, rng=rng)
    return g.build()


def moss_patch(rng):
    """Мох пятном: низкая бугристая зелёная подушка ~60 × 50 см."""
    g = Mesh("moss_patch")
    m1, m2 = mat("moss", (0.32, 0.45, 0.16)), mat("moss_b", (0.4, 0.52, 0.2))
    g.disc((0, 0, 0), 0.3, 0.25, 0.015, m1, n=12, rng=rng)
    for k in range(9):
        c = (rng.uniform(-0.2, 0.2), rng.uniform(-0.16, 0.16), 0.012)
        g.blob(c, (rng.uniform(0.06, 0.1), rng.uniform(0.05, 0.09), 0.03), m2 if k % 2 else m1, subdiv=1, jitter=0.3, rng=rng)
    return g.build()


STONES = [(0.4, 0.39, 0.37), (0.47, 0.45, 0.42), (0.33, 0.32, 0.31)]


def rocks_small(rng):
    """Россыпь камней: 9 камешков 5–15 см."""
    g = Mesh("rocks_small")
    ms = [mat(f"stone_{i}", c) for i, c in enumerate(STONES)]
    for k in range(9):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0, 0.28)
        s = rng.uniform(0.04, 0.1)
        g.blob((math.cos(a) * r, math.sin(a) * r * 0.7, s * 0.4), (s, s * 0.85, s * 0.6), ms[k % 3], subdiv=1, jitter=0.25, rng=rng)
    return g.build()


def rock_boulder(rng):
    """Валун ~1 м, гранёный, с пятном мха сверху и парой камешков рядом."""
    g = Mesh("rock_boulder")
    g.blob((0, 0, 0.32), (0.5, 0.4, 0.38), mat("stone_0", STONES[0]), subdiv=2, jitter=0.12, rng=rng)
    g.blob((0.05, -0.04, 0.63), (0.25, 0.2, 0.06), mat("moss", (0.32, 0.45, 0.16)), subdiv=1, jitter=0.2, rng=rng)
    g.blob((0.55, -0.15, 0.05), (0.09, 0.08, 0.06), mat("stone_1", STONES[1]), subdiv=1, jitter=0.2, rng=rng)
    g.blob((-0.5, 0.1, 0.04), (0.07, 0.06, 0.05), mat("stone_2", STONES[2]), subdiv=1, jitter=0.2, rng=rng)
    return g.build()


BARK, WOOD = (0.36, 0.26, 0.18), (0.78, 0.62, 0.42)


def stump(rng):
    """Пень: невысокий срез 40 см, светлый торец с кольцами, корни расходятся в землю."""
    g = Mesh("stump")
    bark, wood, ring = mat("bark", BARK), mat("wood_cut", WOOD), mat("wood_ring", (0.62, 0.46, 0.3))
    n = 9
    rs = [0.26 + rng.uniform(-0.02, 0.02) for _ in range(n)]
    for zb, zt, s in ((0, 0.4, 1.0),):
        bot = [Vector((math.cos(2 * math.pi * k / n) * rs[k] * 1.12, math.sin(2 * math.pi * k / n) * rs[k] * 1.12, zb)) for k in range(n)]
        top = [Vector((math.cos(2 * math.pi * k / n) * rs[k], math.sin(2 * math.pi * k / n) * rs[k], zt + rng.uniform(-0.03, 0.03))) for k in range(n)]
        for k in range(n):
            g.face([bot[k], bot[(k + 1) % n], top[(k + 1) % n], top[k]], bark)
        c = sum(top, Vector()) / n
        g.face(top, wood)
        for f in (0.66, 0.33):   # годовые кольца — кольца потемнее чуть выше торца
            ringp = [c.lerp(t, f) + Vector((0, 0, 0.003)) for t in top]
            inner = [c.lerp(t, f - 0.06) + Vector((0, 0, 0.003)) for t in top]
            for k in range(n):
                g.face([inner[k], inner[(k + 1) % n], ringp[(k + 1) % n], ringp[k]], ring)
    for k in range(5):   # корни
        a = 2 * math.pi * k / 5 + rng.uniform(-0.2, 0.2)
        out = Vector((math.cos(a), math.sin(a), 0))
        g.tube([out * 0.2 + Vector((0, 0, 0.18)), out * 0.38 + Vector((0, 0, 0.06)), out * 0.55 + Vector((0, 0, -0.02))], [0.07, 0.045, 0.02], bark, sides=5)
    return g.build()


def log_fallen(rng):
    """Поваленное бревно 2 м: кора, светлые торцы, обломанный сук, мох."""
    g = Mesh("log_fallen")
    bark, wood = mat("bark", BARK), mat("wood_cut", WOOD)
    n, R = 8, 0.17
    path = [Vector((-1.0 + 2.0 * t, 0.04 * math.sin(t * 3), R)) for t in [k / 4 for k in range(5)]]
    g.tube(path, [R * (1.05 - 0.1 * k / 4) for k in range(5)], bark, sides=n, cap=False)
    for p, sgn, r in ((path[0], -1, R * 1.05), (path[-1], 1, R * 0.95)):
        ring = [p + Vector((0, math.cos(2 * math.pi * k / n) * r, math.sin(2 * math.pi * k / n) * r)) for k in range(n)]
        g.face(ring if sgn > 0 else ring[::-1], wood)
    g.tube([Vector((0.3, -0.05, R * 1.6)), Vector((0.42, -0.1, R * 2.6))], [0.04, 0.02], bark, sides=5)   # сук
    g.blob((-0.4, 0.02, R * 1.85), (0.25, 0.12, 0.04), mat("moss", (0.32, 0.45, 0.16)), subdiv=1, jitter=0.2, rng=rng)
    return g.build()


def branches_pile(rng):
    """Ветки кучкой: 10 сухих веток с развилками, лежат вперемешку, ~1 м."""
    g = Mesh("branches_pile")
    bark = [mat("branch", (0.42, 0.32, 0.22)), mat("branch_b", (0.5, 0.4, 0.28))]
    for i in range(10):
        a = rng.uniform(0, math.pi)
        d = Vector((math.cos(a), math.sin(a) * 0.6, 0))
        L = rng.uniform(0.5, 1.0)
        c = Vector((rng.uniform(-0.15, 0.15), rng.uniform(-0.1, 0.1), 0.03 + 0.03 * (i % 3)))
        p0, p1 = c - d * L / 2, c + d * L / 2 + Vector((0, 0, rng.uniform(0, 0.08)))
        g.tube([p0, p0.lerp(p1, 0.5), p1], [0.022, 0.016, 0.008], bark[i % 2], sides=5)
        f = p0.lerp(p1, 0.55)   # развилка
        side = d.cross(Vector((0, 0, 1))) * rng.choice((1, -1))
        g.tube([f, f + (d + side * 0.8).normalized() * L * 0.3 + Vector((0, 0, 0.05))], [0.012, 0.005], bark[i % 2], sides=4)
    return g.build()


def leaves_fallen(rng):
    """Опавшие листья: ~70 листочков лежат на земле пятном ~1 м, осенние цвета."""
    g = Mesh("leaves_fallen")
    cols = [mat("leaf_y", (0.88, 0.65, 0.2)), mat("leaf_o", (0.82, 0.42, 0.15)), mat("leaf_r", (0.65, 0.22, 0.12)),
            mat("leaf_br", (0.5, 0.35, 0.2))]
    for i in range(70):
        a = rng.uniform(0, 2 * math.pi)
        r = 0.5 * math.sqrt(rng.random())
        c = Vector((math.cos(a) * r, math.sin(a) * r * 0.75, 0.004 + 0.004 * (i % 3)))
        ang = rng.uniform(0, 2 * math.pi)
        d = Vector((math.cos(ang), math.sin(ang), rng.uniform(-0.1, 0.25)))
        g.leaf(c - d * 0.03, d, (0, 0, 1), rng.uniform(0.05, 0.08), 0.045, cols[i % 4])
    return g.build()


BATCH1 = {"grass_short": grass_short, "grass_tall": grass_tall, "grass_dry": grass_dry, "grass_patchy": grass_patchy,
          "grass_asphalt": grass_asphalt, "weed_nettle": weed_nettle, "weed_burdock": weed_burdock,
          "flowers_dandelion": flowers_dandelion, "flowers_daisy": flowers_daisy, "flowers_fireweed": flowers_fireweed,
          "vine_wall": vine_wall, "fern": fern, "mushrooms": mushrooms, "moss_patch": moss_patch, "rocks_small": rocks_small,
          "rock_boulder": rock_boulder, "stump": stump, "log_fallen": log_fallen, "branches_pile": branches_pile,
          "leaves_fallen": leaves_fallen}
WALL = {"vine_wall"}   # на стену: спина в Y = 0, низ в Z = 0


MODELS = {"bush_water_reeds": reeds, "bush_willow": willow, "bush_water_sedge": sedge, "arrow_wood": arrow, "arrows_bundle": arrows_bundle, **BATCH1}


# ───────────────────────── экспорт ─────────────────────────

def clear():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def ground(ob, wall=False):
    """Низ — в Z = 0, по центру X / Y; на стену — спина (самое дальнее от камеры, +Y) в Y = 0."""
    vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
    mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
    mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
    off = Vector(((mn.x + mx.x) / 2, mx.y if wall else (mn.y + mx.y) / 2, mn.z))
    ob.data.transform(Matrix.Translation(-off))
    return mx - mn


def main():
    names = [a for a in sys.argv[1:] if not a.startswith("-")] or list(MODELS)
    import tripo_process
    from tripo_process import render_views, sheet   # тот же свет и лист превью, что у моделей Tripo

    class _Mats:   # в bpy 4.2 новый материал без узлов — превью Tripo ждёт узлы
        def __getattr__(self, k):
            return getattr(bpy.data.materials, k)

        def new(self, name):
            m = bpy.data.materials.new(name)
            m.use_nodes = True
            return m

    class _Data:
        materials = _Mats()

        def __getattr__(self, k):
            return getattr(bpy.data, k)

    class _Bpy:
        data = _Data()

        def __getattr__(self, k):
            return getattr(bpy, k)

    tripo_process.bpy = _Bpy()
    rows = []
    for nm in names:
        clear()
        _mats.clear()
        rng = random.Random(nm)
        ob = MODELS[nm](rng)
        size = ground(ob, nm in WALL)
        bpy.ops.object.select_all(action="DESELECT")
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob
        path = os.path.join(ROOT, "export", f"{nm}_idle.glb")
        bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True, export_yup=True)
        tri = sum(len(p.vertices) - 2 for p in ob.data.polygons)
        print(f"{nm}: {size.x:.2f} × {size.z:.2f} м (глубина {size.y:.2f}), треугольников {tri}, {os.path.getsize(path) // 1024} КБ")
        prev = os.path.join(ROOT, "renders", "_review", f"_prev_{nm}")
        try:
            rows.append((nm, render_views(ob, prev)))
        except Exception as e:   # без превью — модель всё равно готова
            print("  превью не вышло:", e)
    if rows:
        tag = os.environ.get("SHEET", "props")
        out = os.path.join(ROOT, "renders", "_review", f"{tag}_{datetime.date.today().isoformat()}.png")
        try:
            sheet(rows, out)
            print("лист:", out)
        except Exception as e:
            print("лист не вышел:", e)


if __name__ == "__main__":
    main()
