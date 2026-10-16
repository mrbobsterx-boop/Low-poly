"""Рисованные вещи кодом в стиле Tripo: неровные формы (точение по профилю, трубки по пути, рёбра) и раскраска
«кистью» — картинка запекается из процедурного шейдера (Cycles, Emit): цвет по высоте, мазки, волокна дерева,
кирпич, ржавые потёки, сварные швы, мох, тени в щелях (AO).

    b = PBuilder("body", seed=1)
    b.lathe([(r, z), …], "cactus", seg=16, ribs=8)
    b.tube([(x, y, z), …], [r, …], "cactus", seg=12, ribs=6)
    obj = b.obj()
    paint(obj, 512)        # → один материал с картинкой
"""
import math
import random

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

# стиль: base / top / bottom — цвета (sRGB) по высоте; остальное — узоры (см. _shader)
STYLES = {
    "cactus": dict(base=(0.25, 0.45, 0.2), top=(0.42, 0.58, 0.26), bottom=(0.22, 0.3, 0.16),
                   streak=("z", 0.5, (0.24, 0.42, 0.2), (0.45, 0.62, 0.3)), dots=((0.95, 0.9, 0.72), 40.0, 0.06)),
    "cactus_d": dict(base=(0.22, 0.4, 0.2), top=(0.38, 0.54, 0.26), bottom=(0.2, 0.28, 0.16),
                     streak=("z", 0.5, (0.22, 0.38, 0.19), (0.4, 0.56, 0.28)), dots=((0.95, 0.9, 0.72), 40.0, 0.06)),
    "flower": dict(base=(0.95, 0.42, 0.55), top=(1.0, 0.7, 0.75), bottom=(0.8, 0.3, 0.4)),
    "flower_y": dict(base=(0.98, 0.8, 0.3), top=(1.0, 0.92, 0.55), bottom=(0.9, 0.6, 0.2)),
    "straw": dict(base=(0.72, 0.52, 0.2), top=(0.82, 0.64, 0.3), bottom=(0.46, 0.33, 0.14),
                  streak=("z", 0.5, (0.45, 0.3, 0.1), (0.9, 0.74, 0.4)), strokes=0.35),
    "straw_d": dict(base=(0.66, 0.5, 0.24), top=(0.75, 0.6, 0.32), bottom=(0.45, 0.33, 0.17),
                    streak=("z", 0.35, (0.45, 0.32, 0.14), (0.85, 0.7, 0.4))),
    "wood_z": dict(base=(0.42, 0.3, 0.2), top=(0.5, 0.4, 0.3), bottom=(0.3, 0.21, 0.15),
                   streak=("z", 0.4, (0.27, 0.18, 0.12), (0.6, 0.46, 0.32)), strokes=0.2),
    "wood_grey": dict(base=(0.45, 0.4, 0.35), top=(0.55, 0.5, 0.45), bottom=(0.3, 0.26, 0.22),
                      streak=("z", 0.4, (0.28, 0.24, 0.2), (0.66, 0.6, 0.52)), strokes=0.2),
    "wood_x": dict(base=(0.45, 0.32, 0.21), top=(0.5, 0.38, 0.26), bottom=(0.32, 0.23, 0.16),
                   streak=("x", 0.4, (0.28, 0.19, 0.12), (0.62, 0.47, 0.32)), strokes=0.2),
    "wood_y": dict(base=(0.42, 0.33, 0.22), top=(0.48, 0.4, 0.28), bottom=(0.3, 0.24, 0.17),
                   streak=("y", 0.4, (0.26, 0.2, 0.13), (0.6, 0.5, 0.36)), strokes=0.2,
                   moss=((0.36, 0.45, 0.2), 0.58)),
    "wood_wet": dict(base=(0.33, 0.25, 0.18), top=(0.4, 0.32, 0.22), bottom=(0.2, 0.17, 0.13),
                     streak=("z", 0.4, (0.2, 0.15, 0.1), (0.48, 0.38, 0.26)), moss=((0.33, 0.42, 0.18), 0.55)),
    "ceramic": dict(base=(0.85, 0.86, 0.82), top=(0.95, 0.95, 0.92), bottom=(0.6, 0.62, 0.6)),
    "glass_g": dict(base=(0.45, 0.66, 0.6), top=(0.7, 0.85, 0.8), bottom=(0.3, 0.45, 0.42)),
    "wire": dict(base=(0.12, 0.11, 0.1)),
    "metal_iron": dict(base=(0.32, 0.31, 0.3), top=(0.38, 0.37, 0.35), bottom=(0.25, 0.22, 0.2),
                       rust=((0.5, 0.28, 0.14), 0.55)),
    "brick": dict(base=(0.6, 0.3, 0.21), top=(0.42, 0.24, 0.18), bottom=(0.55, 0.3, 0.22), brick=True,
                  soot=0.85),
    "brick_band": dict(base=(0.5, 0.25, 0.18), top=(0.4, 0.22, 0.16), bottom=(0.45, 0.24, 0.17), brick=True),
    "paint_w": dict(base=(0.88, 0.86, 0.8), top=(0.92, 0.9, 0.85), bottom=(0.7, 0.66, 0.6), stripe_rw=True),
    "concrete": dict(base=(0.6, 0.58, 0.54), top=(0.66, 0.64, 0.6), bottom=(0.45, 0.43, 0.4),
                     blotch=((0.5, 0.48, 0.44), 0.5)),
    "soot": dict(base=(0.2, 0.18, 0.17), top=(0.12, 0.11, 0.1), bottom=(0.3, 0.27, 0.25)),
    "tank": dict(base=(0.8, 0.8, 0.76), top=(0.87, 0.87, 0.84), bottom=(0.6, 0.58, 0.54),
                 rust=((0.55, 0.3, 0.15), 0.6), seams=1.5),
    "tank_g": dict(base=(0.55, 0.62, 0.55), top=(0.62, 0.7, 0.62), bottom=(0.42, 0.45, 0.4),
                   rust=((0.55, 0.3, 0.15), 0.6), seams=1.5),
    "rust": dict(base=(0.55, 0.3, 0.16), top=(0.62, 0.36, 0.2), bottom=(0.4, 0.22, 0.12),
                 blotch=((0.36, 0.2, 0.12), 0.45)),
    "steel": dict(base=(0.55, 0.57, 0.57), top=(0.62, 0.64, 0.64), bottom=(0.42, 0.42, 0.4),
                  rust=((0.5, 0.3, 0.17), 0.66)),
    "pipe_y": dict(base=(0.85, 0.66, 0.2), top=(0.9, 0.74, 0.3), bottom=(0.62, 0.45, 0.15),
                   rust=((0.5, 0.3, 0.15), 0.66)),
    "mud": dict(base=(0.33, 0.27, 0.18), top=(0.33, 0.37, 0.2), bottom=(0.24, 0.2, 0.15),
                blotch=((0.4, 0.34, 0.22), 0.45), moss=((0.32, 0.42, 0.18), 0.45)),
    "grass": dict(base=(0.5, 0.58, 0.26), top=(0.72, 0.74, 0.38), bottom=(0.32, 0.4, 0.18),
                  streak=("z", 0.4, (0.36, 0.45, 0.2), (0.7, 0.74, 0.38))),
    "grass_d": dict(base=(0.6, 0.55, 0.3), top=(0.8, 0.72, 0.42), bottom=(0.38, 0.38, 0.2),
                    streak=("z", 0.4, (0.45, 0.42, 0.22), (0.82, 0.74, 0.45))),
    "water": dict(base=(0.18, 0.24, 0.2)),
}


def lin(c):
    return tuple(x ** 2.2 for x in c[:3]) + (1.0,)


class PBuilder:
    """Копит формы в одну сетку; материал — стиль из STYLES (или цвет кортежем)."""

    def __init__(self, name, seed=1):
        self.bm = bmesh.new()
        self.mats = {}
        self.name = name
        self.rng = random.Random(seed)

    def _mat(self, style):
        if style not in self.mats:
            key = style if isinstance(style, str) else "c%.2f_%.2f_%.2f" % tuple(style)
            m = bpy.data.materials.new(f"style:{key}")
            m.use_nodes = True
            base = STYLES[style]["base"] if isinstance(style, str) else style
            m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = lin(base)
            m["style"] = key
            if not isinstance(style, str):
                STYLES.setdefault(key, dict(base=tuple(style)))
            self.mats[style] = len(self.mats), m
        return self.mats[style][0]

    def _faces(self, faces, style):
        mi = self._mat(style)
        for f in faces:
            f.material_index = mi

    def _jit(self, amt):
        return Vector((self.rng.uniform(-amt, amt), self.rng.uniform(-amt, amt), self.rng.uniform(-amt, amt) * 0.5))

    # ── простые формы ──
    def box(self, lo, hi, style, rz=0.0, rx=0.0, ry=0.0, jit=0.0):
        lo, hi = Vector(lo), Vector(hi)
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        M = (Matrix.Translation((lo + hi) / 2) @ (Matrix.Rotation(rz, 4, "Z") @ Matrix.Rotation(ry, 4, "Y")
             @ Matrix.Rotation(rx, 4, "X")) @ Matrix.Diagonal((*(hi - lo), 1.0)))
        bmesh.ops.transform(self.bm, matrix=M, verts=r["verts"])
        if jit:
            for v in r["verts"]:
                v.co += self._jit(jit)
        self._faces({f for v in r["verts"] for f in v.link_faces}, style)

    def beam(self, p0, p1, w, style, h=None):
        """Брус квадратного сечения от p0 до p1."""
        p0, p1 = Vector(p0), Vector(p1)
        v = p1 - p0
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        q = Vector((0, 0, 1)).rotation_difference(v.normalized()).to_matrix().to_4x4()
        M = Matrix.Translation((p0 + p1) / 2) @ q @ Matrix.Diagonal((w, h or w, v.length, 1.0))
        bmesh.ops.transform(self.bm, matrix=M, verts=r["verts"])
        self._faces({f for v in r["verts"] for f in v.link_faces}, style)

    def ball(self, c, r, style, sz=1.0, sub=1, jit=0.0):
        g = bmesh.ops.create_icosphere(self.bm, subdivisions=sub, radius=r)
        bmesh.ops.transform(self.bm, matrix=Matrix.Translation(Vector(c)) @ Matrix.Diagonal((1, 1, sz, 1)), verts=g["verts"])
        if jit:
            for v in g["verts"]:
                v.co += self._jit(jit * r)
        self._faces({f for v in g["verts"] for f in v.link_faces}, style)

    def ellipsoid(self, c, radii, rot_y, style, sub=1, jit=0.0):
        """Сплюснутый шар (лепёшка опунции и т. п.), повёрнут вокруг оси Y."""
        g = bmesh.ops.create_icosphere(self.bm, subdivisions=sub, radius=1.0)
        M = Matrix.Translation(Vector(c)) @ Matrix.Rotation(rot_y, 4, "Y") @ Matrix.Diagonal((*radii, 1.0))
        bmesh.ops.transform(self.bm, matrix=M, verts=g["verts"])
        if jit:
            for v in g["verts"]:
                v.co += self._jit(jit * min(radii))
        self._faces({f for v in g["verts"] for f in v.link_faces}, style)

    def blade(self, base, top, w, style):
        """Травинка / соломинка: узкий треугольник (двусторонний — 2 грани)."""
        base, top = Vector(base), Vector(top)
        d = (top - base)
        side = d.cross(Vector((0, 0, 1)))
        if side.length < 1e-4:
            side = Vector((1, 0, 0))
        side = side.normalized() * w / 2
        side = Matrix.Rotation(self.rng.uniform(0, 3.14), 3, d.normalized()) @ side
        a, b_, c = self.bm.verts.new(base - side), self.bm.verts.new(base + side), self.bm.verts.new(top)
        f1 = self.bm.faces.new((a, b_, c))
        self._faces([f1], style)

    # ── точение и трубки ──
    def _rings(self, centers, frames, radii, seg, ribs=0, rib_amp=0.12, jit=0.0, twist=0.0):
        rings = []
        for k, (c, (u, v), r) in enumerate(zip(centers, frames, radii)):
            ring = []
            for i in range(seg):
                a = 2 * math.pi * i / seg + twist * k
                rr = r
                if ribs and r > 0:
                    rr = r * (1 + rib_amp * (1 if (i * ribs * 2 // seg) % 2 == 0 else -1) * 0.5)
                p = c + (u * math.cos(a) + v * math.sin(a)) * rr
                if jit and r > 0:
                    p += self._jit(jit * r)
                ring.append(self.bm.verts.new(p))
            rings.append(ring)
        return rings

    def _skin(self, rings, style, cap0=True, tip=None):
        faces = []
        seg = len(rings[0])
        for a, b_ in zip(rings, rings[1:]):
            for i in range(seg):
                j = (i + 1) % seg
                faces.append(self.bm.faces.new((a[i], a[j], b_[j], b_[i])))
        if cap0:
            faces.append(self.bm.faces.new(list(reversed(rings[0]))))
        if tip is not None:
            t = self.bm.verts.new(tip)
            last = rings[-1]
            for i in range(seg):
                faces.append(self.bm.faces.new((last[i], last[(i + 1) % seg], t)))
        else:
            faces.append(self.bm.faces.new(rings[-1]))
        self._faces(faces, style)
        return faces

    def lathe(self, profile, style, seg=12, c=(0, 0, 0), ribs=0, rib_amp=0.12, jit=0.0, tip=True, cap0=True, lean=(0, 0)):
        """Тело вращения по профилю [(r, z), …] снизу вверх; последний r = 0 — макушка точкой."""
        c = Vector(c)
        pts = profile[:-1] if (tip and profile[-1][0] == 0) else profile
        centers = [c + Vector((lean[0] * z, lean[1] * z, z)) for r, z in pts]
        frames = [(Vector((1, 0, 0)), Vector((0, 1, 0)))] * len(pts)
        rings = self._rings(centers, frames, [r for r, z in pts], seg, ribs, rib_amp, jit)
        top = None
        if tip and profile[-1][0] == 0:
            z = profile[-1][1]
            top = c + Vector((lean[0] * z, lean[1] * z, z))
        return self._skin(rings, style, cap0, top)

    def tube(self, path, radii, style, seg=8, ribs=0, rib_amp=0.12, jit=0.0, dome=True, cap0=True):
        """Трубка по пути (ломаная), радиусы по точкам; dome — скруглённый конец."""
        path = [Vector(p) for p in path]
        centers, frames = [], []
        prev_u = None
        for k, p in enumerate(path):
            t = (path[min(k + 1, len(path) - 1)] - path[max(k - 1, 0)]).normalized()
            ref = Vector((0, 0, 1)) if abs(t.z) < 0.9 else Vector((1, 0, 0))
            u = (ref.cross(t)).normalized() if prev_u is None else (prev_u - t * prev_u.dot(t)).normalized()
            v = t.cross(u).normalized()
            prev_u = u
            centers.append(p)
            frames.append((u, v))
        rings = self._rings(centers, frames, radii, seg, ribs, rib_amp, jit)
        tip = None
        if dome:
            t = (path[-1] - path[-2]).normalized()
            tip = path[-1] + t * radii[-1] * 0.8
        return self._skin(rings, style, cap0, tip)

    def obj(self):
        me = bpy.data.meshes.new(self.name)
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
        self.bm.to_mesh(me)
        self.bm.free()
        for i, m in sorted(self.mats.values(), key=lambda t: t[0]):
            me.materials.append(m)
        o = bpy.data.objects.new(self.name, me)
        bpy.context.scene.collection.objects.link(o)
        for f in me.polygons:
            f.use_smooth = False
        return o


# ───────────────────────── раскраска ─────────────────────────

class _N:
    def __init__(self, nt):
        self.nt = nt

    def __call__(self, kind, **kw):
        n = self.nt.nodes.new(kind)
        for k, v in kw.items():
            if k.startswith("in_"):
                key = k[3:]
                key = int(key) if key.isdigit() else key
                n.inputs[key].default_value = v
            else:
                setattr(n, k, v)
        return n

    def link(self, a, b):
        self.nt.links.new(a, b)


def _mix(N, a, b, fac, blend="MIX"):
    m = N("ShaderNodeMix", data_type="RGBA", blend_type=blend)
    for src, dst in ((fac, m.inputs[0]), (a, m.inputs[6]), (b, m.inputs[7])):
        if isinstance(src, (float, int)):
            dst.default_value = src
        elif isinstance(src, tuple):
            dst.default_value = src
        else:
            N.link(src, dst)
    return m.outputs[2]


def _maprange(N, x, a, b, c=0.0, d=1.0):
    m = N("ShaderNodeMapRange", clamp=True)
    N.link(x, m.inputs["Value"])
    m.inputs["From Min"].default_value, m.inputs["From Max"].default_value = a, b
    m.inputs["To Min"].default_value, m.inputs["To Max"].default_value = c, d
    return m.outputs["Result"]


def _shader(mat, st, zr, size):
    """Эмиссионный шейдер «рисунка» для запекания."""
    nt = mat.node_tree
    nt.nodes.clear()
    N = _N(nt)
    out = N("ShaderNodeOutputMaterial")
    em = N("ShaderNodeEmission")
    N.link(em.outputs[0], out.inputs["Surface"])
    tc = N("ShaderNodeTexCoord")
    P = tc.outputs["Object"]
    sep = N("ShaderNodeSeparateXYZ")
    N.link(P, sep.inputs[0])
    geo = N("ShaderNodeNewGeometry")
    base, top, bottom = st["base"], st.get("top", st["base"]), st.get("bottom", st["base"])
    # высота: низ → середина → верх
    g = _maprange(N, sep.outputs["Z"], zr[0], zr[1])
    g1 = _maprange(N, g, 0.0, 0.55)
    g2 = _maprange(N, g, 0.45, 1.0)
    col = _mix(N, lin(bottom), lin(base), g1)
    col = _mix(N, col, lin(top), g2)
    # мазки кистью: крупные пятна-оттенки
    nz = N("ShaderNodeTexNoise", in_Scale=1.6 / max(0.4, size ** 0.5), in_Detail=3.0, in_Roughness=0.6)
    N.link(P, nz.inputs["Vector"])
    v = _maprange(N, nz.outputs["Fac"], 0.3, 0.7, 0.74, 1.18)
    vc = N("ShaderNodeCombineColor")
    for i in range(3):
        N.link(v, vc.inputs[i])
    col = _mix(N, col, vc.outputs[0], 1.0, "MULTIPLY")
    # волокна / полосы вдоль оси (дерево, солома, рёбра кактуса)
    if "streak" in st:
        ax, amt, c0, c1 = st["streak"]
        sc = {"x": (0.25, 9.0, 9.0), "y": (9.0, 0.25, 9.0), "z": (9.0, 9.0, 0.25)}[ax]
        mp = N("ShaderNodeMapping", in_3=Vector(sc))
        N.link(P, mp.inputs["Vector"])
        sn = N("ShaderNodeTexNoise", in_Scale=2.5, in_Detail=6.0, in_Roughness=0.65, in_Distortion=0.4)
        N.link(mp.outputs[0], sn.inputs["Vector"])
        f = _maprange(N, sn.outputs["Fac"], 0.32, 0.68)
        sc_ = _mix(N, lin(c0), lin(c1), f)
        col = _mix(N, col, sc_, amt)
        # тонкие тёмные линии волокон (как прорисованные)
        wv = N("ShaderNodeTexWave", wave_type="BANDS", bands_direction={"x": "Y", "y": "X", "z": "X"}[ax],
               in_Scale=3.0, in_Distortion=6.0, in_Detail=3.0)
        N.link(P, wv.inputs["Vector"])
        lines = _maprange(N, wv.outputs["Fac"], 0.0, 0.12, 0.72, 1.0)
        lc = N("ShaderNodeCombineColor")
        for i in range(3):
            N.link(lines, lc.inputs[i])
        col = _mix(N, col, lc.outputs[0], 0.55, "MULTIPLY")
    # кирпич: по развёртке цилиндра (угол × радиус, высота)
    if st.get("brick"):
        ax = N("ShaderNodeMath", operation="ARCTAN2")
        N.link(sep.outputs["Y"], ax.inputs[0])
        N.link(sep.outputs["X"], ax.inputs[1])
        u = N("ShaderNodeMath", operation="MULTIPLY", in_1=1.1)
        N.link(ax.outputs[0], u.inputs[0])
        cv = N("ShaderNodeCombineXYZ")
        N.link(u.outputs[0], cv.inputs[0])
        N.link(sep.outputs["Z"], cv.inputs[1])
        br = N("ShaderNodeTexBrick", in_Scale=1.0, offset=0.5)
        br.inputs["Mortar Size"].default_value = 0.025
        br.inputs["Brick Width"].default_value = 0.5
        br.inputs["Row Height"].default_value = 0.22
        br.inputs["Bias"].default_value = 0.0
        br.inputs["Color1"].default_value = lin(base)
        br.inputs["Color2"].default_value = lin(tuple(c * 0.8 for c in base))
        br.inputs["Mortar"].default_value = lin((0.32, 0.26, 0.22))
        N.link(cv.outputs[0], br.inputs["Vector"])
        col = _mix(N, col, br.outputs["Color"], 0.75, "MULTIPLY")
        col = _mix(N, col, br.outputs["Color"], 0.35)
    # пятна (бетон, ржавчина, грязь)
    if "blotch" in st:
        c2, thr = st["blotch"]
        bn = N("ShaderNodeTexNoise", in_Scale=3.0, in_Detail=5.0, in_Roughness=0.7)
        N.link(P, bn.inputs["Vector"])
        col = _mix(N, col, lin(c2), _maprange(N, bn.outputs["Fac"], thr, thr + 0.12))
    # сварные швы (баки): тёмные кольца
    if "seams" in st:
        wv = N("ShaderNodeTexWave", wave_type="BANDS", bands_direction="Z", in_Scale=2 * math.pi / (20 * st["seams"]))
        N.link(P, wv.inputs["Vector"])
        s = _maprange(N, wv.outputs["Fac"], 0.0, 0.05, 0.62, 1.0)
        sc_ = N("ShaderNodeCombineColor")
        for i in range(3):
            N.link(s, sc_.inputs[i])
        col = _mix(N, col, sc_.outputs[0], 1.0, "MULTIPLY")
    # ржавые потёки — вертикальные полосы, гуще сверху
    if "rust" in st:
        c2, thr = st["rust"]
        mp = N("ShaderNodeMapping", in_3=Vector((7.0, 7.0, 0.35)))
        N.link(P, mp.inputs["Vector"])
        rn = N("ShaderNodeTexNoise", in_Scale=2.0, in_Detail=6.0, in_Roughness=0.7)
        N.link(mp.outputs[0], rn.inputs["Vector"])
        f = _maprange(N, rn.outputs["Fac"], thr, thr + 0.1)
        col = _mix(N, col, lin(c2), f)
        bn = N("ShaderNodeTexNoise", in_Scale=4.0, in_Detail=6.0, in_Roughness=0.75)
        N.link(P, bn.inputs["Vector"])
        col = _mix(N, col, lin(tuple(c * 0.8 for c in c2)), _maprange(N, bn.outputs["Fac"], thr + 0.05, thr + 0.12))
    # красно-белые полосы (труба) — в верхней части
    if st.get("stripe_rw"):
        wv = N("ShaderNodeTexWave", wave_type="BANDS", bands_direction="Z", in_Scale=0.25, wave_profile="SAW")
        N.link(P, wv.inputs["Vector"])
        f = _maprange(N, wv.outputs["Fac"], 0.49, 0.51)
        col = _mix(N, col, lin((0.75, 0.2, 0.15)), f)
    # мох — пятнами на верхних гранях
    if "moss" in st:
        c2, thr = st["moss"]
        mn = N("ShaderNodeTexNoise", in_Scale=2.5, in_Detail=5.0, in_Roughness=0.7)
        N.link(P, mn.inputs["Vector"])
        up = N("ShaderNodeSeparateXYZ")
        N.link(geo.outputs["Normal"], up.inputs[0])
        f = N("ShaderNodeMath", operation="MULTIPLY")
        N.link(_maprange(N, mn.outputs["Fac"], thr, thr + 0.08), f.inputs[0])
        N.link(_maprange(N, up.outputs["Z"], 0.2, 0.7), f.inputs[1])
        col = _mix(N, col, lin(c2), f.outputs[0])
    # колючки / точки
    if "dots" in st:
        c2, scale, rad = st["dots"]
        vo = N("ShaderNodeTexVoronoi", in_Scale=scale / max(0.6, size ** 0.5))
        N.link(P, vo.inputs["Vector"])
        col = _mix(N, col, lin(c2), _maprange(N, vo.outputs["Distance"], rad, rad * 0.6))
    # солома: светлые штрихи-соломинки
    if st.get("strokes"):
        mp = N("ShaderNodeMapping", in_3=Vector((14.0, 14.0, 1.2)))
        N.link(P, mp.inputs["Vector"])
        vo = N("ShaderNodeTexVoronoi", in_Scale=3.0, feature="DISTANCE_TO_EDGE")
        N.link(mp.outputs[0], vo.inputs["Vector"])
        f = _maprange(N, vo.outputs["Distance"], 0.06, 0.0)
        col = _mix(N, col, _mix(N, col, (1.0, 1.0, 1.0, 1.0), 0.25), f)
        col = _mix(N, col, (0.0, 0.0, 0.0, 1.0), _maprange(N, vo.outputs["Distance"], 0.02, 0.0, 0.0, st["strokes"]))
    # тень в щелях и у земли
    ao = N("ShaderNodeAmbientOcclusion", samples=16, inside=False, only_local=True)
    ao.inputs["Distance"].default_value = min(0.6, 0.12 * size + 0.05)
    aof = _maprange(N, ao.outputs["AO"], 0.0, 1.0, 0.42, 1.0)
    ac = N("ShaderNodeCombineColor")
    for i in range(3):
        N.link(aof, ac.inputs[i])
    col = _mix(N, col, ac.outputs[0], 1.0, "MULTIPLY")
    # копоть на трубе
    if "soot" in st:
        s = _maprange(N, g, st["soot"], 1.0)
        col = _mix(N, col, lin((0.12, 0.1, 0.09)), s)
    N.link(col, em.inputs["Color"])


def paint(obj, px=512, margin=0.02):
    """Запечь «рисунок» всех материалов в одну картинку px×px; объект получает один материал с ней."""
    me = obj.data
    sc = bpy.context.scene
    for o in list(sc.objects):
        o.select_set(o is obj)
    bpy.context.view_layer.objects.active = obj
    co = np.array([v.co[:] for v in me.vertices])
    lo, hi = co.min(0), co.max(0)
    size = float(max(hi - lo))
    # развёртка
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(55), island_margin=margin, area_weight=0.0)
    bpy.ops.object.mode_set(mode="OBJECT")
    img = bpy.data.images.new("painted", px, px, alpha=False)
    for m in me.materials:
        st = STYLES.get(m.get("style", ""), dict(base=(0.5, 0.5, 0.5)))
        _shader(m, st, (float(lo[2]), float(hi[2])), size)
        tn = m.node_tree.nodes.new("ShaderNodeTexImage")
        tn.image = img
        m.node_tree.nodes.active = tn
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 32
    sc.render.bake.margin = 6
    bpy.ops.object.bake(type="EMIT")
    img.pack()
    # один материал с картинкой, без блеска
    mat = bpy.data.materials.new("painted")
    mat.use_nodes = True
    nt = mat.node_tree
    tn = nt.nodes.new("ShaderNodeTexImage")
    tn.image = img
    bsdf = nt.nodes["Principled BSDF"]
    nt.links.new(tn.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 1.0
    bsdf.inputs["Metallic"].default_value = 0.0
    me.materials.clear()
    me.materials.append(mat)
    for f in me.polygons:
        f.material_index = 0
    return obj
