"""Декор внутри открывающихся моделей (tools/open_parts.py): что лежит за дверцей / под крышкой.

Всё делается кодом из простых форм (коробки, цилиндры, шары) в стиле low poly — только для вида, без логики.
Каждому виду (kind) — своя начинка: шкаф — одежда на штанге, холодильник — полки с едой, ящик — консервы в соломе…
Место — коробка box [xmin, ymin, zmin, xmax, ymax, zmax] (обычно та же, что вырезана внутри), перед — к −Y.
"""
import math
import random

import bmesh  # noqa: F401 — после bpy
import bpy
from mathutils import Matrix, Vector

C = {  # цвета (sRGB 0…1)
    "wood": (0.45, 0.30, 0.18), "wood_l": (0.62, 0.46, 0.30), "wood_d": (0.30, 0.20, 0.12),
    "metal": (0.45, 0.46, 0.48), "metal_d": (0.22, 0.23, 0.25), "rust": (0.45, 0.25, 0.15),
    "white": (0.85, 0.85, 0.82), "cream": (0.86, 0.80, 0.66), "red": (0.70, 0.15, 0.12), "green": (0.25, 0.40, 0.22),
    "olive": (0.38, 0.40, 0.22), "blue": (0.18, 0.30, 0.55), "yellow": (0.85, 0.70, 0.20), "orange": (0.90, 0.45, 0.10),
    "brown": (0.40, 0.26, 0.15), "black": (0.07, 0.07, 0.08), "grey": (0.40, 0.40, 0.40), "straw": (0.78, 0.66, 0.36),
    "paper": (0.80, 0.76, 0.66), "glass": (0.45, 0.60, 0.50), "water": (0.12, 0.28, 0.40), "money": (0.42, 0.55, 0.36),
    "gold": (0.85, 0.65, 0.18), "fabric1": (0.30, 0.35, 0.50), "fabric2": (0.55, 0.30, 0.25), "fabric3": (0.35, 0.45, 0.30),
    "fabric4": (0.55, 0.52, 0.45), "bag": (0.10, 0.10, 0.11), "ember": (1.0, 0.35, 0.05), "rubber": (0.09, 0.09, 0.09),
}


class Builder:
    """Копит формы в одну сетку; материал — по цвету."""

    def __init__(self, name, seed=1):
        self.bm = bmesh.new()
        self.mats = {}
        self.name = name
        self.rng = random.Random(seed)

    def _mat(self, col):
        if col not in self.mats:
            rgb = C[col] if isinstance(col, str) else col
            m = bpy.data.materials.new(f"{self.name}_{col}")
            m.use_nodes = True
            b = m.node_tree.nodes["Principled BSDF"]
            b.inputs["Base Color"].default_value = (*[c ** 2.2 for c in rgb], 1.0)
            b.inputs["Roughness"].default_value = 0.9
            if col == "ember":
                b.inputs["Emission Color"].default_value = (1.0, 0.3, 0.05, 1.0)
                b.inputs["Emission Strength"].default_value = 3.0
            self.mats[col] = len(self.mats), m
        return self.mats[col][0]

    def _add(self, geom_verts, col, M):
        mi = self._mat(col)
        faces = {f for v in geom_verts for f in v.link_faces}
        bmesh.ops.transform(self.bm, matrix=M, verts=list(geom_verts))
        for f in faces:
            f.material_index = mi

    def box(self, lo, hi, col, rz=0.0, rx=0.0, ry=0.0):
        lo, hi = Vector(lo), Vector(hi)
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        M = (Matrix.Translation((lo + hi) / 2) @ (Matrix.Rotation(rz, 4, "Z") @ Matrix.Rotation(ry, 4, "Y")
             @ Matrix.Rotation(rx, 4, "X")) @ Matrix.Diagonal((*(hi - lo), 1.0)))
        self._add(r["verts"], col, M)

    def cyl(self, c, r, h, col, axis="z", seg=10, rot=None):
        g = bmesh.ops.create_cone(self.bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=h)
        R = {"z": Matrix(), "x": Matrix.Rotation(math.pi / 2, 4, "Y"), "y": Matrix.Rotation(math.pi / 2, 4, "X")}[axis]
        if rot is not None:
            R = rot @ R
        self._add(g["verts"], col, Matrix.Translation(Vector(c)) @ R)

    def ball(self, c, r, col, sz=1.0):
        g = bmesh.ops.create_icosphere(self.bm, subdivisions=1, radius=r)
        self._add(g["verts"], col, Matrix.Translation(Vector(c)) @ Matrix.Diagonal((1, 1, sz, 1)))

    def obj(self):
        me = bpy.data.meshes.new(self.name)
        self.bm.to_mesh(me)
        self.bm.free()
        for i, m in sorted(self.mats.values(), key=lambda t: t[0]):
            me.materials.append(m)
        o = bpy.data.objects.new(self.name, me)
        bpy.context.scene.collection.objects.link(o)
        for f in me.polygons:
            f.use_smooth = False
        return o


# ───────────────────────── мелочи ─────────────────────────

def can(b, x, y, z, s=1.0, col=None):
    col = col or b.rng.choice(["red", "blue", "green", "yellow", "metal"])
    b.cyl((x, y, z + 0.055 * s), 0.035 * s, 0.11 * s, col)
    b.cyl((x, y, z + 0.112 * s), 0.036 * s, 0.006 * s, "metal")


def bottle(b, x, y, z, s=1.0, col=None):
    col = col or b.rng.choice(["glass", "brown", "green", "white"])
    b.cyl((x, y, z + 0.08 * s), 0.03 * s, 0.16 * s, col, seg=8)
    b.cyl((x, y, z + 0.19 * s), 0.012 * s, 0.06 * s, col, seg=6)


def jar(b, x, y, z, s=1.0):
    b.cyl((x, y, z + 0.05 * s), 0.04 * s, 0.10 * s, "glass", seg=8)
    b.cyl((x, y, z + 0.105 * s), 0.041 * s, 0.015 * s, b.rng.choice(["red", "metal", "yellow"]), seg=8)


def pack(b, x, y, z, w, d, h, col=None):
    b.box((x - w / 2, y - d / 2, z), (x + w / 2, y + d / 2, z + h), col or b.rng.choice(["paper", "red", "blue", "white", "yellow"]))


def row(x0, x1, step):
    n = max(1, int((x1 - x0) / step))
    return [x0 + (i + 0.5) * (x1 - x0) / n for i in range(n)]


def shelves(b, lo, hi, n, col="wood_l"):
    zs = [lo[2] + (hi[2] - lo[2]) * (i + 1) / (n + 1) for i in range(n)]
    for z in zs:
        b.box((lo[0], lo[1] + 0.01, z - 0.012), (hi[0], hi[1], z + 0.012), col)
    return [lo[2]] + [z + 0.012 for z in zs]


def fill_shelf(b, x0, x1, y, z, hmax, kinds):
    x = x0 + 0.03
    while x < x1 - 0.05:
        k = b.rng.choice(kinds)
        if k == "can" and hmax > 0.13:
            can(b, x + 0.035, y, z); x += 0.08
        elif k == "bottle" and hmax > 0.24:
            bottle(b, x + 0.03, y, z); x += 0.075
        elif k == "jar" and hmax > 0.13:
            jar(b, x + 0.04, y, z); x += 0.09
        elif k == "pack" and hmax > 0.1:
            w = b.rng.uniform(0.06, 0.12)
            pack(b, x + w / 2, y, z, w, 0.07, min(hmax * 0.8, b.rng.uniform(0.08, 0.2))); x += w + 0.02
        elif k == "pill":
            b.cyl((x + 0.02, y, z + 0.035), 0.018, 0.07, b.rng.choice(["white", "orange", "brown"]), seg=8)
            b.cyl((x + 0.02, y, z + 0.075), 0.02, 0.012, "white", seg=8); x += 0.05
        elif k == "box_s":
            w = b.rng.uniform(0.04, 0.07)
            pack(b, x + w / 2, y, z, w, 0.04, min(hmax * 0.8, 0.09)); x += w + 0.015
        else:
            x += 0.05


def clothes(b, lo, hi):
    """Штанга, вешалки с одеждой, полка сверху (шапка, коробка), обувь внизу."""
    w = hi[0] - lo[0]
    zt = hi[2] - min(0.32, (hi[2] - lo[2]) * 0.18)
    yc = (lo[1] + hi[1]) / 2
    b.box((lo[0], lo[1] + 0.02, zt), (hi[0], hi[1], zt + 0.02), "wood_l")
    zr = zt - 0.07
    b.cyl(((lo[0] + hi[0]) / 2, yc, zr), 0.012, w, "metal", axis="x", seg=8)
    depth = min(0.42, (hi[1] - lo[1]) * 0.85)
    for x in row(lo[0] + 0.03, hi[0] - 0.03, 0.11):
        col = b.rng.choice(["fabric1", "fabric2", "fabric3", "fabric4", "black"])
        ln = b.rng.uniform(0.55, 0.95) * min(1.0, (zr - lo[2]) / 1.1)
        b.box((x - 0.035, yc - depth / 2, zr - ln), (x + 0.035, yc + depth / 2, zr - 0.03), col)
        b.cyl((x, yc, zr - 0.015), 0.008, 0.02, "metal", seg=6)
    if hi[2] - zt > 0.15:
        pack(b, lo[0] + w * 0.3, yc, zt + 0.02, min(0.3, w * 0.35), 0.25, 0.14, "paper")
        b.ball((hi[0] - w * 0.25, yc, zt + 0.07), 0.08, "olive", 0.6)
    for x in row(lo[0] + 0.05, hi[0] - 0.05, 0.22)[:3]:
        for dx in (-0.045, 0.045):
            b.box((x + dx - 0.035, yc - 0.12, lo[2]), (x + dx + 0.035, yc + 0.12, lo[2] + 0.08), "brown")


def rifles(b, lo, hi):
    """Оружейный шкаф: стойка, винтовки, полка с ящиками патронов."""
    yc = (lo[1] + hi[1]) / 2
    zt = hi[2] - 0.35
    b.box((lo[0], lo[1] + 0.02, zt), (hi[0], hi[1], zt + 0.02), "metal_d")
    b.box((lo[0], hi[1] - 0.08, lo[2]), (hi[0], hi[1] - 0.04, lo[2] + 0.12), "wood_d")
    for x in row(lo[0] + 0.05, hi[0] - 0.05, 0.12):
        h = min(1.05, zt - lo[2] - 0.08)
        b.box((x - 0.022, yc - 0.03, lo[2] + 0.02), (x + 0.022, yc + 0.03, lo[2] + 0.02 + h * 0.4), "wood")
        b.box((x - 0.014, yc - 0.02, lo[2] + 0.02 + h * 0.4), (x + 0.014, yc + 0.02, lo[2] + 0.02 + h), "black")
    for x in row(lo[0] + 0.05, hi[0] - 0.05, 0.2):
        pack(b, x, yc, zt + 0.02, 0.16, 0.1, 0.1, "olive")


def fridge(b, lo, hi):
    z = shelves(b, lo, hi, 3, "white")
    yc = (lo[1] + hi[1]) / 2
    for i, zz in enumerate(z):
        top = (z[i + 1] if i + 1 < len(z) else hi[2]) - zz
        fill_shelf(b, lo[0], hi[0], yc - 0.05, zz, top, ["can", "bottle", "jar", "pack"])
        if i == 0:
            b.ball((hi[0] - 0.12, yc + 0.05, zz + 0.07), 0.07, "red")
            b.ball((hi[0] - 0.25, yc + 0.08, zz + 0.06), 0.06, "green")


def medicine(b, lo, hi):
    z = shelves(b, lo, hi, 2, "white")
    yc = (lo[1] + hi[1]) / 2
    for i, zz in enumerate(z):
        top = (z[i + 1] if i + 1 < len(z) else hi[2]) - zz
        fill_shelf(b, lo[0], hi[0], yc, zz, top, ["pill", "box_s", "bottle", "pill"])


def oven(b, lo, hi):
    yc = (lo[1] + hi[1]) / 2
    zr = lo[2] + (hi[2] - lo[2]) * 0.4
    for x in row(lo[0] + 0.02, hi[0] - 0.02, 0.04):
        b.box((x - 0.003, lo[1] + 0.02, zr - 0.003), (x + 0.003, hi[1], zr + 0.003), "metal")
    b.box(((lo[0] + hi[0]) / 2 - 0.15, yc - 0.1, zr + 0.003), ((lo[0] + hi[0]) / 2 + 0.15, yc + 0.1, zr + 0.025), "metal_d")
    b.ball(((lo[0] + hi[0]) / 2, yc, zr + 0.05), 0.07, "brown", 0.55)


def fire(b, c, r, y0, y1):
    """Печь: поленья и угли."""
    for i in range(3):
        b.cyl((c[0] + (i - 1) * r * 0.45, (y0 + y1) / 2, c[2] - r * 0.55), r * 0.18, (y1 - y0) * 0.7, "wood", axis="y", seg=7)
    for i in range(6):
        b.ball((c[0] + b.rng.uniform(-r, r) * 0.6, b.rng.uniform(y0, y1), c[2] - r * 0.7), r * 0.13, "ember", 0.6)


def safe(b, lo, hi):
    z = shelves(b, lo, hi, 1, "metal_d")
    yc = (lo[1] + hi[1]) / 2
    for i, x in enumerate(row(lo[0] + 0.03, hi[0] - 0.03, 0.085)):
        b.box((x - 0.035, yc - 0.06, z[0]), (x + 0.035, yc + 0.06, z[0] + 0.03 + 0.012 * (i % 3)), "money")
    for k in range(3):
        b.box((lo[0] + 0.04 + k * 0.08, yc - 0.03, z[1]), (lo[0] + 0.1 + k * 0.08, yc + 0.03, z[1] + 0.03), "gold")
    pack(b, hi[0] - 0.08, yc, z[1], 0.1, 0.14, 0.02, "paper")


def electric(b, lo, hi):
    """Щит: ряды автоматов, провода."""
    yb = hi[1] - 0.01
    nr = max(1, int((hi[2] - lo[2]) / 0.25))
    for i in range(nr):
        z = lo[2] + (hi[2] - lo[2]) * (i + 0.5) / nr
        b.box((lo[0] + 0.02, yb - 0.03, z - 0.01), (hi[0] - 0.02, yb, z + 0.01), "metal")
        for x in row(lo[0] + 0.03, hi[0] - 0.03, 0.04):
            b.box((x - 0.016, yb - 0.07, z - 0.045), (x + 0.016, yb - 0.01, z + 0.045), "white")
            b.box((x - 0.006, yb - 0.08, z), (x + 0.006, yb - 0.07, z + 0.02), b.rng.choice(["black", "red"]))
    for col, x in (("red", lo[0] + 0.03), ("blue", lo[0] + 0.05), ("yellow", hi[0] - 0.04)):
        b.cyl((x, yb - 0.02, (lo[2] + hi[2]) / 2), 0.006, hi[2] - lo[2] - 0.04, col, seg=6)


def kitchen(b, lo, hi):
    """Под раковиной: сифон, ведро, бутылки."""
    yc = (lo[1] + hi[1]) / 2
    cx = (lo[0] + hi[0]) / 2
    b.cyl((cx, yc + 0.05, hi[2] - 0.12), 0.025, 0.24, "white", seg=8)
    b.cyl((cx, yc + 0.05, hi[2] - 0.25), 0.05, 0.08, "white", seg=8)
    b.cyl((cx, hi[1] - 0.06, hi[2] - 0.25), 0.02, 0.2, "white", axis="y", seg=8)
    b.cyl((lo[0] + 0.15, yc, lo[2] + 0.12), 0.11, 0.24, "blue", seg=12)
    for i, x in enumerate(row(cx + 0.05, hi[0] - 0.03, 0.08)):
        bottle(b, x, yc - 0.05, lo[2], 1.2, ["yellow", "blue", "white"][i % 3])


def crate_fill(b, lo, hi, items):
    """Открытая сверху тара: подложка и вещи по виду."""
    w, d = hi[0] - lo[0], hi[1] - lo[1]
    floor = lo[2] + (hi[2] - lo[2]) * 0.35 if items not in ("dynamite", "ammo", "garbage") else lo[2]
    if items in ("food", "tools", "medical"):
        b.box((lo[0], lo[1], lo[2]), (hi[0], hi[1], floor), "straw" if items == "food" else "paper")
    s = min(1.0, max(0.35, min(w, d) / 0.4))
    if items == "food":
        for x in row(lo[0] + 0.03, hi[0] - 0.03, 0.09 * s):
            for y in row(lo[1] + 0.03, hi[1] - 0.03, 0.09 * s):
                (can if b.rng.random() < 0.6 else jar)(b, x, y, floor, s)
    elif items == "dynamite":
        for z in range(3):
            for y in row(lo[1] + 0.01, hi[1] - 0.01, 0.06):
                b.cyl(((lo[0] + hi[0]) / 2, y, floor + 0.03 + z * 0.058), 0.028, w * 0.85, "red", axis="x", seg=8)
        b.cyl((hi[0] - 0.1, (lo[1] + hi[1]) / 2, floor + 0.2), 0.005, 0.25, "black", axis="y", seg=5)
    elif items == "ammo":
        for x in row(lo[0] + 0.01, hi[0] - 0.01, 0.022):
            for y in row(lo[1] + 0.01, hi[1] - 0.01, 0.022):
                b.cyl((x, y, floor + 0.03), 0.008, 0.06, "gold", seg=6)
                b.cyl((x, y, floor + 0.068), 0.006, 0.016, "rust", seg=6)
    elif items == "tools":
        cx, cy = (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2
        b.box((lo[0] + 0.02, cy - 0.012, floor), (lo[0] + 0.02 + w * 0.55, cy + 0.012, floor + 0.02), "wood")
        b.box((lo[0] + 0.02 + w * 0.5, cy - 0.03, floor), (lo[0] + 0.02 + w * 0.62, cy + 0.03, floor + 0.035), "metal_d")
        b.box((cx - w * 0.3, lo[1] + 0.012, floor), (cx + w * 0.25, lo[1] + 0.032, floor + 0.015), "metal")
        b.box((cx - w * 0.4, hi[1] - 0.03, floor), (cx - w * 0.1, hi[1] - 0.012, floor + 0.02), "red")
        b.box((cx - w * 0.1, hi[1] - 0.025, floor), (cx + w * 0.3, hi[1] - 0.017, floor + 0.01), "metal")
        b.cyl((hi[0] - 0.04, cy, floor + 0.02), 0.02, 0.04, "yellow", seg=8)
    elif items == "medical":
        cy = (lo[1] + hi[1]) / 2
        for i, x in enumerate(row(lo[0] + 0.02, hi[0] - 0.02, 0.045)):
            if i % 3 == 0:
                b.cyl((x, cy, floor + 0.022), 0.02, d * 0.7, "white", axis="y", seg=8)
            elif i % 3 == 1:
                b.cyl((x, cy, floor + 0.03), 0.015, 0.06, b.rng.choice(["orange", "white", "brown"]), seg=8)
            else:
                pack(b, x, cy, floor, 0.035, d * 0.6, 0.03, b.rng.choice(["white", "red", "blue"]))
    elif items == "garbage":
        for x in row(lo[0] + 0.05, hi[0] - 0.05, 0.28):
            for y in row(lo[1] + 0.05, hi[1] - 0.05, 0.28):
                r = b.rng.uniform(0.12, 0.17)
                b.ball((x, y, lo[2] + r * 0.8 + b.rng.uniform(0, 0.12)), r, "bag", 0.8)
        for i in range(4):
            pack(b, b.rng.uniform(lo[0] + 0.1, hi[0] - 0.1), b.rng.uniform(lo[1] + 0.1, hi[1] - 0.1),
                 lo[2] + 0.2, 0.12, 0.08, 0.1, b.rng.choice(["paper", "white"]))
    elif items == "water":
        b.box((lo[0], lo[1], lo[2]), (hi[0], hi[1], lo[2] + (hi[2] - lo[2]) * 0.7), "water")


def vehicle(b, front, seats_x, lo, hi, bag=True):
    """Салон: руль (слева по ходу), рычаг, сумка на заднем сиденье. seats_x — передняя кромка салона."""
    f = front
    fx = seats_x
    yd = 0.38 * f  # водитель слева по ходу: при переде к +X это +Y
    zb = lo[2] + 0.55
    rot = Matrix.Rotation(-f * math.radians(65), 4, "Y")
    b.cyl((fx - f * 0.2, yd, zb), 0.17, 0.03, "black", axis="z", seg=12, rot=rot)
    b.cyl((fx - f * 0.12, yd, zb - 0.08), 0.025, 0.2, "black", axis="x", seg=6)
    b.cyl((fx - f * 0.45, 0.0, lo[2] + 0.25), 0.012, 0.2, "metal_d", seg=6)
    b.ball((fx - f * 0.45, 0.0, lo[2] + 0.36), 0.025, "black")
    if bag:
        rx = fx - f * 1.35
        pack(b, rx, -0.25 * f, lo[2] + 0.26, 0.3, 0.2, 0.18, b.rng.choice(["olive", "fabric2", "blue"]))


def cargo(b, lo, hi, kind="mixed"):
    """Груз на полу: ящики, мешки, бочки (вагоны, контейнер, гараж)."""
    xs = row(lo[0] + 0.3, hi[0] - 0.3, 0.75)
    for i, x in enumerate(xs):
        side = lo[1] + 0.35 if i % 2 == 0 else hi[1] - 0.35
        k = (i * 7 + 3) % 4
        if k == 0:
            b.box((x - 0.3, side - 0.28, lo[2]), (x + 0.3, side + 0.28, lo[2] + 0.5), "wood_l")
            b.box((x - 0.2, side - 0.2, lo[2] + 0.5), (x + 0.2, side + 0.2, lo[2] + 0.85), "wood", rz=0.2)
        elif k == 1:
            for j in range(3):
                b.ball((x + (j - 1) * 0.22, side, lo[2] + 0.13), 0.17, "straw", 0.65)
            b.ball((x, side, lo[2] + 0.33), 0.17, "straw", 0.65)
        elif k == 2:
            b.cyl((x, side, lo[2] + 0.42), 0.27, 0.84, b.rng.choice(["rust", "blue", "green"]), seg=12)
        else:
            b.box((x - 0.4, side - 0.3, lo[2]), (x + 0.4, side + 0.3, lo[2] + 0.12), "wood_l")
            pack(b, x, side, lo[2] + 0.12, 0.6, 0.45, 0.35, "paper")


def benches(b, lo, hi):
    """Пассажирский вагон: лавки по обе стороны прохода, полки для вещей."""
    for x in row(lo[0] + 0.2, hi[0] - 0.2, 0.9):
        for y0, y1 in ((lo[1] + 0.03, -0.32), (0.32, hi[1] - 0.03)):
            b.box((x - 0.24, y0, lo[2] + 0.38), (x + 0.24, y1, lo[2] + 0.48), "wood")
            b.box((x + 0.2, y0, lo[2]), (x + 0.26, y1, lo[2] + 0.95), "wood_d")
            b.box((x - 0.2, y0, lo[2]), (x - 0.16, y1, lo[2] + 0.38), "wood_d")
        if b.rng.random() < 0.5:
            pack(b, x, lo[1] + 0.25, lo[2] + 0.48, 0.3, 0.22, 0.2, b.rng.choice(["brown", "fabric1", "olive"]))
    for y0, y1 in ((lo[1] + 0.02, lo[1] + 0.35), (hi[1] - 0.35, hi[1] - 0.02)):
        b.box((lo[0] + 0.1, y0, hi[2] - 0.35), (hi[0] - 0.1, y1, hi[2] - 0.32), "metal")


def booth(b, lo, hi):
    """Будка: столик у окна, стул, рация, кружка."""
    yt = hi[1] - 0.3
    b.box((lo[0] + 0.05, yt - 0.25, lo[2] + 0.75), (lo[0] + 0.85, hi[1] - 0.02, lo[2] + 0.8), "wood")
    b.box((lo[0] + 0.1, yt, lo[2]), (lo[0] + 0.15, yt + 0.05, lo[2] + 0.75), "wood_d")
    b.box((lo[0] + 0.75, yt, lo[2]), (lo[0] + 0.8, yt + 0.05, lo[2] + 0.75), "wood_d")
    pack(b, lo[0] + 0.3, yt + 0.05, lo[2] + 0.8, 0.18, 0.12, 0.1, "olive")
    b.cyl((lo[0] + 0.6, yt + 0.05, lo[2] + 0.84), 0.035, 0.08, "white", seg=8)
    cx = lo[0] + 0.45
    b.box((cx - 0.2, yt - 0.7, lo[2] + 0.42), (cx + 0.2, yt - 0.3, lo[2] + 0.46), "metal_d")
    for dx in (-0.17, 0.17):
        for dy in (-0.67, -0.33):
            b.box((cx + dx - 0.015, yt + dy - 0.015, lo[2]), (cx + dx + 0.015, yt + dy + 0.015, lo[2] + 0.42), "metal_d")
    b.box((cx - 0.2, yt - 0.72, lo[2] + 0.46), (cx + 0.2, yt - 0.68, lo[2] + 0.85), "metal_d")


def garage(b, lo, hi):
    """Гараж: колёса стопкой, стеллаж с банками, канистра, бочка."""
    for i in range(4):
        b.cyl((lo[0] + 0.45, hi[1] - 0.45, lo[2] + 0.1 + i * 0.2), 0.32, 0.19, "rubber", seg=12)
    sx0, sx1 = lo[0] + 1.0, min(hi[0] - 0.3, lo[0] + 2.2)
    z = lo[2]
    for k in range(4):
        b.box((sx0, hi[1] - 0.45, z + k * 0.45), (sx1, hi[1] - 0.05, z + k * 0.45 + 0.03), "metal")
        if k:
            fill_shelf(b, sx0, sx1, hi[1] - 0.25, z + k * 0.45 + 0.03, 0.4, ["can", "pack", "can", "bottle"])
    for x in (sx0, sx1):
        b.box((x - 0.02, hi[1] - 0.45, z), (x + 0.02, hi[1] - 0.41, z + 1.4), "metal_d")
    b.cyl((hi[0] - 0.4, hi[1] - 0.4, lo[2] + 0.45), 0.3, 0.9, "rust", seg=12)
    b.box((hi[0] - 0.95, hi[1] - 0.25, lo[2]), (hi[0] - 0.75, hi[1] - 0.12, lo[2] + 0.32), "red")


def ladder(b, c, r, z0, z1):
    """Люк: лестница вниз в темноту."""
    y = c[1] + r * 0.75
    for x in (c[0] - 0.18, c[0] + 0.18):
        b.box((x - 0.015, y - 0.015, z0), (x + 0.015, y + 0.015, z1), "metal")
    z = z0 + 0.03
    while z < z1:
        b.cyl((c[0], y, z), 0.01, 0.36, "metal", axis="x", seg=6)
        z += 0.07


def motorhome(b, lo, hi):
    """Дом на колёсах: столик с лавками, кровать, шкафчик."""
    cx = lo[0] + 0.9
    b.box((cx - 0.3, -0.4, lo[2] + 0.7), (cx + 0.3, 0.3, lo[2] + 0.74), "wood_l")
    b.box((cx - 0.03, -0.1, lo[2]), (cx + 0.03, 0.0, lo[2] + 0.7), "metal")
    for dx in (-0.55, 0.55):
        b.box((cx + dx - 0.2, -0.7, lo[2]), (cx + dx + 0.2, 0.7, lo[2] + 0.42), "fabric1")
        b.box((cx + dx + (0.15 if dx > 0 else -0.2), -0.7, lo[2] + 0.42), (cx + dx + (0.2 if dx > 0 else -0.15), 0.7, lo[2] + 0.9), "fabric1")
    b.box((lo[0] + 0.05, -0.95, lo[2]), (lo[0] + 0.5, 0.95, lo[2] + 0.45), "fabric4")
    b.box((lo[0] + 0.05, -0.95, lo[2] + 0.45), (lo[0] + 0.5, 0.95, lo[2] + 0.55), "white")
    b.box((hi[0] - 0.9, hi[1] - 0.5, lo[2]), (hi[0] - 0.2, hi[1] - 0.05, lo[2] + 0.9), "wood_l")


KINDS = {
    "clothes": clothes, "rifles": rifles, "fridge": fridge, "medicine": medicine, "oven": oven, "safe": safe,
    "electric": electric, "kitchen": kitchen, "cargo": cargo, "benches": benches, "booth": booth, "garage": garage,
    "motorhome": motorhome,
}


def build(name, d, seed=1):
    """d — настройка декора: {"kind": …, "box": [...], ещё поля для отдельных видов}. → объект Blender."""
    b = Builder(f"{name}_decor", seed)
    k = d["kind"]
    if k == "crate":
        crate_fill(b, d["box"][:3], d["box"][3:], d["items"])
    elif k == "fire":
        fire(b, d["c"], d["r"], d["y0"], d["y1"])
    elif k == "ladder":
        ladder(b, d["c"], d["r"], d["z0"], d["z1"])
    elif k == "vehicle":
        vehicle(b, d["front"], d["x"], d["box"][:3], d["box"][3:], d.get("bag", True))
    elif k == "water":
        b.cyl(d["c"], d["r"], 0.01, "water", seg=16)
    elif k == "multi":
        for sub in d["list"]:
            o = build(name + "_s", sub, seed + 1)
            o_bm = bmesh.new()
            o_bm.from_mesh(o.data)
            for m in o.data.materials:
                b.mats.setdefault(m.name, (len(b.mats), m))
            idx = {i: b.mats[m.name][0] for i, m in enumerate(o.data.materials)}
            for f in o_bm.faces:
                f.material_index = idx[f.material_index]
            me = bpy.data.meshes.new("t")
            o_bm.to_mesh(me)
            b.bm.from_mesh(me)
            o_bm.free()
            bpy.data.objects.remove(o)
    else:
        KINDS[k](b, d["box"][:3], d["box"][3:])
    return b.obj()
