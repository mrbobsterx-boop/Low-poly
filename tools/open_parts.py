"""Разрезать готовую модель на корпус и подвижные части (дверцы, крышки, двери вагона) — чтобы в игре они открывались.

  python3 tools/open_parts.py [имя …] [--preview]

Берёт export/<имя>_idle.glb и настройки из tripo/open_parts.json → export/parts/<имя>.glb:
- body — корпус; там, где была дверца, — проём, за ним пустота внутри (тёмные стенки, пол, потолок);
- door_l / door_r / lid / door_front … — отдельные куски; торцы, изнанка и стенки внутри — нарисованные доски
  цвета модели (своя маленькая картинка 256×256, повторяется);
- точка каждого куска (origin) — на петле: в игре дверцу достаточно повернуть вокруг своей точки
  (или сдвинуть — у раздвижной двери вагона). Куда и на сколько — в tripo/open_parts.json и docs/FOR_GAME.md.
Резка — логическими операциями Blender (Boolean, Exact) по коробкам из настроек.
--preview — лист «закрыто / открыто» в renders/_review/open_parts_<дата>.jpg.
"""
import datetime
import json
import math
import os
import sys

import bpy
import bmesh  # noqa: E402 — после bpy
import numpy as np
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tripo_process as T  # noqa: E402

CFG = os.path.join(ROOT, "tripo", "open_parts.json")
OUT = os.path.join(ROOT, "export", "parts")


def avg_color(obj):
    """Средний цвет текстуры модели (по картинке Base Color)."""
    for slot in obj.material_slots:
        m = slot.material
        if not (m and m.use_nodes):
            continue
        img = T._upstream_image(m.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
        if img is not None:
            a = T._pixels(img)
            return (a[..., :3].reshape(-1, 3) ** 2.2).mean(0)     # картинка в sRGB → линейный цвет
    return np.array([0.3, 0.22, 0.15])


def wood_image(name, rgb, seed, px=256):
    """Нарисованные доски цвета модели: 4 доски на картинку, швы, волокна, пара сучков (повторяется плиткой)."""
    rng = np.random.default_rng(seed)
    base = np.clip(np.asarray(rgb, float), 0, 1) ** (1 / 2.2)           # линейный → sRGB
    y, x = np.mgrid[0:px, 0:px] / px
    rows = 4
    k = np.floor(y * rows).astype(int)
    shade = 1 + rng.uniform(-0.09, 0.09, rows)[k]                         # каждая доска чуть своего тона
    grain = np.zeros((px, px))
    for f, a in ((7, 0.05), (19, 0.035), (47, 0.02)):                    # волокна вдоль доски
        ph = rng.uniform(0, 2 * np.pi, 3)
        grain += a * np.sin(2 * np.pi * (f * y + 0.6 * np.sin(2 * np.pi * (x + ph[0])) + ph[1]))
    v = shade + grain
    fy = (y * rows) % 1
    v *= 1 - 0.45 * np.exp(-((np.minimum(fy, 1 - fy) * px / rows) / 1.6) ** 2)   # швы между досками
    for r in range(0, rows, 2):                                           # торцевой стык через доску
        jx = rng.uniform(0.1, 0.9)
        m = (k == r) & (np.abs(x - jx) * px < 1.5)
        v[m] *= 0.75
    for _ in range(2):                                                    # сучки
        cx, cy = rng.uniform(0.1, 0.9, 2)
        d = ((x - cx) * 2.5) ** 2 + ((y - cy) * 7) ** 2
        v *= 1 - 0.35 * np.exp(-d * 400)
    img = np.clip(base[None, None, :] * v[..., None], 0, 1)
    im = bpy.data.images.new(name, px, px)
    im.pixels.foreach_set(np.concatenate([img[::-1], np.ones((px, px, 1))], 2).astype(np.float32).ravel())
    im.pack()
    return im


def wood_mat(name, rgb, seed):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = wood_image(name, rgb, seed)
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 1.0
    b.inputs["Metallic"].default_value = 0.0
    return m


TILE = 0.5          # метров на одну картинку досок (доска ≈ 12 см)


def project_uv(obj, mats):
    """Грани из вырезов (торцы, изнанка, стенки внутри) — развёртка «коробкой»: доски лежат вдоль самой длинной
    стороны грани по горизонтали."""
    idx = {i for i, s in enumerate(obj.material_slots) if s.material in mats}
    me = obj.data
    uv = me.uv_layers.active
    for f in me.polygons:
        if f.material_index not in idx:
            continue
        n = f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        u_ax, v_ax = {0: (1, 2), 1: (0, 2), 2: (0, 1)}[ax]
        for li in f.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (co[u_ax] / TILE, co[v_ax] / TILE)


def box_obj(b, mat):
    me = bpy.data.meshes.new("_cut")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0, calc_uvs=True)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("_cut", me)
    bpy.context.scene.collection.objects.link(o)
    lo, hi = Vector(b[:3]), Vector(b[3:])
    o.location = (lo + hi) / 2
    o.scale = hi - lo
    me.materials.append(mat)
    o.hide_render = True
    return o


def boolean(obj, cutter, op):
    mod = obj.modifiers.new("b", "BOOLEAN")
    mod.operation = op
    mod.solver = "EXACT"
    mod.object = cutter
    mod.material_mode = "TRANSFER"
    mod.use_hole_tolerant = True
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)


def set_origin(obj, p):
    p = Vector(p)
    obj.data.transform(Matrix.Translation(-p))
    obj.location = p


def build(name, cfg):
    obj, _ = T.import_joined(os.path.join(ROOT, "export", f"{name}_idle.glb"))
    T.clear_custom_normals(obj)
    c = avg_color(obj)
    m_cut = wood_mat(f"{name}_cut", c * 0.8, 1)       # торцы и обратная сторона дверцы
    m_in = wood_mat(f"{name}_inside", c * 0.45, 2)    # пустота внутри
    obj.data.materials.append(m_cut)
    obj.data.materials.append(m_in)
    parts = []
    for p in cfg["parts"]:
        o = obj.copy()
        o.data = obj.data.copy()
        bpy.context.scene.collection.objects.link(o)
        cut = box_obj(p["box"], m_cut)
        boolean(o, cut, "INTERSECT")
        bpy.data.objects.remove(cut)
        o.name = o.data.name = p["name"]
        parts.append((o, p))
    for b in [p["box"] for p in cfg["parts"]] + cfg.get("cavity", []):
        cut = box_obj(b, m_in)
        boolean(obj, cut, "DIFFERENCE")
        bpy.data.objects.remove(cut)
    obj.name = obj.data.name = "body"
    for o in [obj] + [o for o, _ in parts]:
        T.smooth_by_angle(o)
        project_uv(o, (m_cut, m_in))
    for o, p in parts:
        set_origin(o, p["pivot"])
    return obj, parts


def export(objs, path):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_yup=True,
                              export_animations=False, export_image_format="JPEG", export_jpeg_quality=85)
    return os.path.getsize(path) / 1e6


def pose(parts, t):
    """t = 0 — закрыто, 1 — открыто."""
    for o, p in parts:
        op = p["open"]
        o.rotation_mode = "XYZ"                     # после импорта glTF — кватернионы
        o.rotation_euler = (0, 0, 0)
        o.location = Vector(p["pivot"])
        if "rot" in op:
            ax, deg = op["rot"]
            o.rotation_euler["xyz".index(ax)] = math.radians(deg * t)
        else:
            o.location = Vector(p["pivot"]) + Vector(op["move"]) * t


def preview(name, body, parts, tmp):
    rows = []
    for t, tag in ((0.0, "closed"), (1.0, "open")):
        pose(parts, t)
        bpy.context.view_layer.update()
        rows += T.render_views(body, os.path.join(tmp, f"{name}_{tag}"), px=360, fit=1.7)
    pose(parts, 0.0)
    return rows


def main(argv):
    cfg = json.load(open(CFG))
    names = [a for a in argv if not a.startswith("--")] or [k for k in cfg if not k.startswith("_")]
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(ROOT, "renders", "_review", "tripo_views")
    os.makedirs(tmp, exist_ok=True)
    rows = []
    for n in names:
        body, parts = build(n, cfg[n])
        mb = export([body] + [o for o, _ in parts], os.path.join(OUT, f"{n}.glb"))
        tri = {o.name: T.tris(o) for o in [body] + [o for o, _ in parts]}
        print(f"[{n}] {mb:.2f} МБ, треугольники: {tri}", flush=True)
        if "--preview" in argv:
            ims = preview(n, body, parts, tmp)
            rows.append((f"{n}\nслева — закрыто (спереди, 3/4), справа — открыто; части: "
                         + ", ".join(p['name'] for _, p in parts), ims))
    if rows:
        out = os.path.join(ROOT, "renders", "_review", f"open_parts_{datetime.date.today()}.png")
        T.sheet(rows, out)
        from PIL import Image
        Image.open(out).convert("RGB").save(out[:-4] + ".jpg", quality=88)
        os.remove(out)
        print("лист:", out[:-4] + ".jpg")


if __name__ == "__main__":
    main(sys.argv[1:])
