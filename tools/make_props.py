"""Модели, нарисованные кодом (не Tripo): кусты у воды и стрелы (просьба автора 2026-10-14). Blender как модуль bpy.

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


MODELS = {"bush_water_reeds": reeds, "bush_willow": willow, "bush_water_sedge": sedge, "arrow_wood": arrow, "arrows_bundle": arrows_bundle}


# ───────────────────────── экспорт ─────────────────────────

def clear():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def ground(ob):
    """Низ — в Z = 0, по центру X / Y."""
    vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
    mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
    mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
    off = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
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
        size = ground(ob)
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
        out = os.path.join(ROOT, "renders", "_review", f"props_{datetime.date.today().isoformat()}.png")
        try:
            sheet(rows, out)
            print("лист:", out)
        except Exception as e:
            print("лист не вышел:", e)


if __name__ == "__main__":
    main()
