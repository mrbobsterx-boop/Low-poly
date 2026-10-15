"""Прицепы к машинам — сделаны кодом (в проекте их не было). Blender как модуль bpy.

    python3 tools/make_trailers.py [имя …]

Каждый прицеп → export/parts/<имя>.glb (части: body, wheel_N, борт/крышка, точка coupler — сцепка с фаркопом
машины) и export/<имя>_idle.glb (целиком, для каталога). Оси/углы — в export/parts/open_parts.json, как у
открывающихся моделей (tools/open_parts.py). Дышло — к +X Blender, низ — на земле, колёса стоят на Z = 0.
Лист превью: renders/_review/trailers_<дата>.jpg.
"""
import datetime
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import open_decor as D  # noqa: E402
import open_parts as OP  # noqa: E402
import tripo_process as T  # noqa: E402

WR = 0.3      # радиус колеса
WW = 0.17     # ширина колеса


def wheel(name, c, r=WR, w=WW, side=1):
    b = D.Builder(name)
    b.cyl((0, 0, 0), r, w, "rubber", axis="y", seg=16)
    b.cyl((0, side * (w / 2 + 0.003), 0), r * 0.6, 0.01, "metal", axis="y", seg=12)
    for k in range(5):                                       # гайки — видно, что колесо крутится
        import math
        a = 2 * math.pi * k / 5
        b.cyl((math.cos(a) * r * 0.3, side * (w / 2 + 0.01), math.sin(a) * r * 0.3), 0.02, 0.015, "metal_d", axis="y", seg=6)
    o = b.obj()
    o.location = Vector(c)
    return o, {"name": name, "pivot": list(c), "wheel": True, "radius": r, "open": {"spin": True}}


def drawbar(b, x0, y0, xc, z, col="metal_d"):
    """Дышло: две балки от углов к сцепке, сцепная головка, опорное колёсико."""
    import math
    for s in (-1, 1):
        ln = math.hypot(xc - x0, y0)
        a = math.atan2(-s * y0, xc - x0)
        b.box((x0 + (xc - x0) / 2 - ln / 2, s * y0 / 2 - 0.035, z - 0.04), (x0 + (xc - x0) / 2 + ln / 2, s * y0 / 2 + 0.035, z + 0.04),
              col, rz=a)
    b.box((xc - 0.05, -0.05, z - 0.05), (xc + 0.12, 0.05, z + 0.03), col)
    b.cyl((xc + 0.12, 0, z - 0.02), 0.045, 0.09, "metal", seg=10)
    xj = xc - 0.35
    b.cyl((xj, 0.09, (z + 0.12) / 2), 0.025, z, "metal", seg=8)
    b.box((xj - 0.03, 0.06, z - 0.33), (xj + 0.03, 0.12, z - 0.27), "metal_d")
    b.cyl((xj, 0.09, 0.06), 0.06, 0.04, "rubber", axis="y", seg=10)


def bed(b, x0, x1, w, z, sides_h, wood="wood_l", frame="metal_d"):
    """Платформа: рама, пол из досок, борта по бокам и спереди (зад — отдельный борт)."""
    h = w / 2
    for y in (-h + 0.06, h - 0.06):
        b.box((x0, y - 0.04, z - 0.12), (x1, y + 0.04, z - 0.02), frame)
    for x in D.row(x0, x1, 0.45):
        b.box((x - 0.03, -h + 0.06, z - 0.1), (x + 0.03, h - 0.06, z - 0.03), frame)
    for y in D.row(-h, h, 0.14):
        b.box((x0, y - 0.065, z - 0.02), (x1, y + 0.065, z + 0.02), b.rng.choice([wood, wood, "wood"]))
    if sides_h:
        for s in (-1, 1):
            for k in range(3):
                zz = z + 0.02 + k * sides_h / 3
                b.box((x0, s * h - 0.02, zz), (x1, s * h + 0.02, zz + sides_h / 3 - 0.01), wood)
        for k in range(3):
            zz = z + 0.02 + k * sides_h / 3
            b.box((x1 - 0.04, -h, zz), (x1, h, zz + sides_h / 3 - 0.01), wood)
        for x in (x0, x1):
            for s in (-1, 1):
                b.box((x - 0.03, s * h - 0.03, z - 0.02), (x + 0.03, s * h + 0.03, z + sides_h + 0.03), frame)
    b.box((x0 - 0.04, -h + 0.05, z - 0.1), (x0, -h + 0.2, z - 0.03), "red")      # фонари
    b.box((x0 - 0.04, h - 0.2, z - 0.1), (x0, h - 0.05, z - 0.03), "red")


def fender(b, x, y, r, w, col="metal"):
    s = 1 if y > 0 else -1
    b.box((x - r - 0.08, y - w / 2 - 0.02, r + 0.04), (x + r + 0.08, y + w / 2 + 0.02, r + 0.07), col)
    b.box((x - r - 0.08, y + s * (w / 2 + 0.02) - 0.01, r - 0.1), (x - r - 0.05, y + s * (w / 2 + 0.02) + 0.01, r + 0.07), col)
    b.box((x + r + 0.05, y + s * (w / 2 + 0.02) - 0.01, r - 0.1), (x + r + 0.08, y + s * (w / 2 + 0.02) + 0.01, r + 0.07), col)


def gate(name, x0, w, z, h, wood="wood_l", frame="metal_d"):
    """Задний борт, петли снизу — откидывается назад (к −X)."""
    b = D.Builder(name, 7)
    for k in range(3):
        zz = z + 0.02 + k * h / 3
        b.box((x0 - 0.04, -w / 2, zz), (x0, w / 2, zz + h / 3 - 0.01), wood)
    for s in (-1, 1):
        b.box((x0 - 0.05, s * (w / 2 - 0.05) - 0.02, z + 0.1), (x0 - 0.035, s * (w / 2 - 0.05) + 0.02, z + h - 0.05), frame)
    o = b.obj()
    return o, {"name": name, "pivot": [x0, 0.0, z], "open": {"rot": ["y", -95]}}


def axle(b, x, y, z):
    b.cyl((x, 0, z), 0.035, 2 * y, "metal_d", axis="y", seg=8)
    for s in (-1, 1):
        b.box((x - 0.35, s * (y - 0.12) - 0.03, z + 0.02), (x + 0.35, s * (y - 0.12) + 0.03, z + 0.07), "metal_d")


def cargo(name, covered=False):
    w, x0, x1, z, sh = 1.3, -1.2, 0.8, 0.66, 0.4
    yw = w / 2 + 0.14
    b = D.Builder(name)
    bed(b, x0, x1, w, z, sh)
    drawbar(b, x1, w / 2 - 0.08, 1.85, 0.48)
    axle(b, -0.2, yw, WR)
    for s in (-1, 1):
        fender(b, -0.2, s * yw, WR, WW)
    parts = []
    if covered:
        for x in (x0 + 0.03, (x0 + x1) / 2, x1 - 0.03):          # дуги
            for s in (-1, 1):
                b.box((x - 0.015, s * w / 2 - 0.015, z + sh), (x + 0.015, s * w / 2 + 0.015, z + 1.15), "metal")
        b.box((x0, -w / 2 - 0.01, z + sh - 0.02), (x1, w / 2 + 0.01, z + 1.15), "olive")     # тент (бока и перёд)
        b.box((x0 + 0.04, -w / 2 + 0.02, z + sh - 0.03), (x1 - 0.04, w / 2 - 0.02, z + 1.14), "black")  # внутри темно
        b.box((x0 - 0.02, -w / 2 - 0.03, z + 1.13), (x1 + 0.02, w / 2 + 0.03, z + 1.19), "olive")     # крыша
        fb = D.Builder(name + "_flap", 3)                          # задний полог — поднимается вверх
        fb.box((x0 - 0.03, -w / 2, z + sh + 0.02), (x0 - 0.005, w / 2, z + 1.13), "olive")
        fo = fb.obj()
        parts.append((fo, {"name": "flap", "pivot": [x0 - 0.02, 0.0, z + 1.13], "open": {"rot": ["y", -100]}}))
    else:
        D.crate_fill(b, (x0 + 0.1, -w / 2 + 0.1, z + 0.02), (x0 + 0.7, -0.05, z + 0.35), "tools")
        b.box((x0 + 0.85, 0.0, z + 0.02), (x0 + 1.45, w / 2 - 0.08, z + 0.42), "wood", rz=0.1)
    parts.append(gate("tailgate", x0, w, z, sh))
    for i, s in enumerate((-1, 1)):
        parts.append(wheel(f"wheel_{i + 1}", (-0.2, s * yw, WR), side=s))
    return b.obj(), parts, {"coupler": [1.97, 0.0, 0.46]}


def flatbed(name):
    w, x0, x1, z = 1.9, -2.0, 1.6, 0.72
    yw = 0.78
    b = D.Builder(name)
    bed(b, x0, x1, w, z, 0)
    for x in D.row(x0, x1, 0.6):                                   # стойки по краям
        for s in (-1, 1):
            b.box((x - 0.025, s * w / 2 - 0.025, z), (x + 0.025, s * w / 2 + 0.025, z + 0.3), "metal_d")
    b.box((x1 - 0.06, -w / 2, z), (x1, w / 2, z + 0.5), "metal")    # передний щит
    drawbar(b, x1, w / 2 - 0.15, 2.7, 0.5)
    parts = []
    for ax in (-0.75, -0.05):
        axle(b, ax, yw, WR)
    k = 1
    for ax in (-0.75, -0.05):
        for s in (-1, 1):
            parts.append(wheel(f"wheel_{k}", (ax, s * yw, WR), side=s))
            k += 1
    for s in (-1, 1):                                              # трапы — подняты, опускаются назад
        rb = D.Builder(f"{name}_ramp{s}", 5)
        y = s * 0.55
        rb.box((x0 - 0.06, y - 0.2, z), (x0, y + 0.2, z + 0.9), "metal")
        for zz in D.row(z, z + 0.9, 0.12):
            rb.box((x0 - 0.075, y - 0.2, zz - 0.01), (x0 - 0.06, y + 0.2, zz + 0.01), "metal_d")
        o = rb.obj()
        parts.append((o, {"name": f"ramp_{'l' if s < 0 else 'r'}", "pivot": [x0, y, z], "open": {"rot": ["y", -150]}}))
    return b.obj(), parts, {"coupler": [2.84, 0.0, 0.48]}


def water(name):
    w, x0, x1, z = 1.2, -1.1, 0.9, 0.62
    yw = 0.74
    b = D.Builder(name)
    bed(b, x0, x1, w, z, 0)
    b.cyl(((x0 + x1) / 2, 0, z + 0.6), 0.55, x1 - x0 - 0.1, "blue", axis="x", seg=16)
    for x in (x0 + 0.05, x1 - 0.05):
        b.cyl((x, 0, z + 0.6), 0.5, 0.06, "white", axis="x", seg=16)
    for x in (x0 + 0.4, x1 - 0.4):                                 # хомуты
        b.cyl((x, 0, z + 0.6), 0.565, 0.05, "metal_d", axis="x", seg=16)
    b.cyl((x0 - 0.06, 0, z + 0.25), 0.04, 0.14, "metal", axis="x", seg=8)    # кран сзади
    b.box((x0 - 0.15, -0.025, z + 0.2), (x0 - 0.12, 0.025, z + 0.3), "red")
    b.cyl((0.0, 0, z + 1.16), 0.17, 0.04, "white", seg=12)          # горловина
    drawbar(b, x1, w / 2 - 0.08, 1.95, 0.48)
    axle(b, -0.1, yw, WR)
    for s in (-1, 1):
        fender(b, -0.1, s * yw, WR, WW)
    cb = D.Builder(name + "_cap", 4)
    cb.cyl((0, 0, z + 1.2), 0.14, 0.06, "metal", seg=12)
    co = cb.obj()
    parts = [(co, {"name": "cap", "pivot": [0.0, 0.0, z + 1.17], "open": {"move": [0, 0, 0.25]}})]
    for i, s in enumerate((-1, 1)):
        parts.append(wheel(f"wheel_{i + 1}", (-0.1, s * yw, WR), side=s))
    return b.obj(), parts, {"coupler": [2.07, 0.0, 0.46]}


TRAILERS = {
    "trailer_cargo": lambda n: cargo(n),
    "trailer_covered": lambda n: cargo(n, covered=True),
    "trailer_flatbed": flatbed,
    "trailer_water": water,
}


def make(name):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    body, parts, pts = TRAILERS[name](name)
    body.name = body.data.name = "body"
    for o, p in parts:                                              # точка куска — на петле / оси
        if o.type == "MESH" and not p.get("wheel"):
            OP.set_origin(o, p["pivot"])
        o.name = p["name"]
        if o.data:
            o.data.name = p["name"]
    for n, at in pts.items():
        e = bpy.data.objects.new(n, None)
        e.empty_display_size = 0.1
        bpy.context.scene.collection.objects.link(e)
        e.location = Vector(at)
        parts.append((e, {"name": n, "pivot": at, "marker": True, "open": {}}))
    objs = [body] + [o for o, _ in parts]
    os.makedirs(OP.OUT, exist_ok=True)
    mb = OP.export(objs, os.path.join(OP.OUT, f"{name}.glb"))
    OP.save_game_info(name, parts)
    # целиком — для каталога
    meshes = [o for o in objs if o.type == "MESH"]
    bpy.ops.object.select_all(action="DESELECT")
    cp = []
    for o in meshes:
        c = o.copy()
        c.data = o.data.copy()
        bpy.context.scene.collection.objects.link(c)
        cp.append(c)
    for c in cp:
        c.select_set(True)
    bpy.context.view_layer.objects.active = cp[0]
    bpy.ops.object.join()
    whole = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    T.export(whole, os.path.join(ROOT, "export", f"{name}_idle.glb"))
    bpy.data.objects.remove(whole)
    print(f"[{name}] {mb:.2f} МБ, треугольники: {sum(T.tris(o) for o in meshes)}", flush=True)
    return body, parts


def main(argv):
    names = [a for a in argv if not a.startswith("--")] or list(TRAILERS)
    tmp = os.path.join(ROOT, "renders", "_review", "tripo_views")
    os.makedirs(tmp, exist_ok=True)
    rows = []
    for n in names:
        body, parts = make(n)
        ims = OP.preview(n, body, parts, tmp)
        rows.append((f"{n}\nслева — как есть, справа — открыто (борт/трап/крышка), колёса отодвинуты; "
                     "сцепка — точка coupler на конце дышла", ims))
    out = os.path.join(ROOT, "renders", "_review", f"trailers_{datetime.date.today()}.png")
    T.sheet(rows, out)
    from PIL import Image
    Image.open(out).convert("RGB").save(out[:-4] + ".jpg", quality=88)
    os.remove(out)
    print("лист:", out[:-4] + ".jpg")


if __name__ == "__main__":
    main(sys.argv[1:])
