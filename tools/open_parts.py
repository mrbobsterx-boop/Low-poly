"""Разрезать готовую модель на корпус и подвижные части (дверцы, крышки, двери вагона) — чтобы в игре они открывались.

  python3 tools/open_parts.py [имя …] [--preview]

Берёт export/<имя>_idle.glb и настройки из tripo/open_parts.json → export/parts/<имя>.glb:
- body — корпус; там, где была дверца, — проём, за ним пустота внутри (тёмные стенки, пол, потолок);
- door_l / door_r / lid / door_front … — отдельные куски; торцы и обратная сторона — цвета дерева/металла модели;
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


def flat_mat(name, rgb):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*[float(c) for c in rgb], 1.0)
    b.inputs["Roughness"].default_value = 1.0
    b.inputs["Metallic"].default_value = 0.0
    return m


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
    m_cut = flat_mat(f"{name}_cut", c * 0.8)          # торцы и обратная сторона дверцы
    m_in = flat_mat(f"{name}_inside", c * 0.4)        # пустота внутри
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
