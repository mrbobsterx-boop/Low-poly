"""Разрезать готовую модель на корпус и подвижные части (дверцы, крышки, двери вагона) — чтобы в игре они открывались.

  python3 tools/open_parts.py [имя …] [--preview]

Берёт export/<имя>_idle.glb и настройки из tripo/open_parts.json → export/parts/<имя>.glb:
- body — корпус; там, где была дверца, — проём, за ним пустота внутри (тёмные стенки, пол, потолок);
- door_l / door_r / lid / door_front … — отдельные куски; торцы, изнанка и стенки внутри — нарисованные доски
  цвета модели (своя маленькая картинка 256×256, повторяется);
- точка каждого куска (origin) — на петле: в игре дверцу достаточно повернуть вокруг своей точки
  (или сдвинуть — у раздвижной двери вагона). Куда и на сколько — в tripo/open_parts.json и docs/FOR_GAME.md.
Резка — логическими операциями Blender (Boolean, Exact) по коробкам из настроек.
--preview — лист «закрыто / открыто» в renders/_review/open_parts[_<--sheet имя>]_<дата>.jpg.
В настройке объекта: pattern — чем «нарисовано» внутри (wood — доски, metal — металл, plain — ткань/пластик),
inside_rgb — свой цвет внутри (0…1), cavity/box — коробка или цилиндр (см. box_obj),
add — коробки, которые добавить внутрь (сиденья в машине), hollow — ниша в самой дверце.
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
    return _image(name, base, v)


def metal_image(name, rgb, seed, px=256):
    """Крашеный металл: лёгкие продольные потёртости, шов листа, ряд заклёпок, пятна грязи."""
    rng = np.random.default_rng(seed)
    base = np.clip(np.asarray(rgb, float), 0, 1) ** (1 / 2.2)
    y, x = np.mgrid[0:px, 0:px] / px
    v = 1 + 0.03 * np.sin(2 * np.pi * (60 * x + rng.uniform(0, 6)))
    v += rng.normal(0, 0.025, (1, px)).repeat(px, 0)                         # продольные царапины
    for _ in range(4):                                                         # грязные пятна
        cx, cy, r = *rng.uniform(0, 1, 2), rng.uniform(0.08, 0.2)
        v *= 1 - 0.12 * np.exp(-(((x - cx) ** 2 + (y - cy) ** 2) / r ** 2))
    v *= 1 - 0.4 * np.exp(-((np.minimum(y, 1 - y) * px) / 1.4) ** 2)          # шов листа
    for k in range(8):                                                         # заклёпки вдоль шва
        cx = (k + 0.5) / 8
        d = ((x - cx) ** 2 + (y - 0.04) ** 2) * px * px
        v *= 1 - 0.3 * np.exp(-d / 6)
    return _image(name, base, v)


def plain_image(name, rgb, seed, px=256):
    """Ткань / пластик: ровный цвет с мелким зерном (сиденья, обивка, пластик)."""
    rng = np.random.default_rng(seed)
    base = np.clip(np.asarray(rgb, float), 0, 1) ** (1 / 2.2)
    v = 1 + rng.normal(0, 0.035, (px, px))
    return _image(name, base, v)


def _image(name, base, v):
    px = v.shape[0]
    img = np.clip(base[None, None, :] * v[..., None], 0, 1)
    im = bpy.data.images.new(name, px, px)
    im.pixels.foreach_set(np.concatenate([img[::-1], np.ones((px, px, 1))], 2).astype(np.float32).ravel())
    im.pack()
    return im


PATTERNS = {"wood": None, "metal": metal_image, "plain": plain_image}


def wood_mat(name, rgb, seed, pattern="wood"):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = (PATTERNS[pattern] or wood_image)(name, rgb, seed)
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
    """Режущая форма: коробка [xmin, ymin, zmin, xmax, ymax, zmax] или цилиндр
    {"cyl": [cx, cy, cz], "r": радиус, "axis": "x|y|z", "h": [от, до]} (круглые люки, крышки бочек)."""
    me = bpy.data.meshes.new("_cut")
    bm = bmesh.new()
    rz = 0.0
    if isinstance(b, dict) and "box" in b:              # повёрнутая коробка {"box": [...], "rz": градусы вокруг Z}
        b, rz = b["box"], b.get("rz", 0.0)
    if isinstance(b, dict):
        bmesh.ops.create_cone(bm, cap_ends=True, segments=48, radius1=1.0, radius2=1.0, depth=1.0, calc_uvs=True)
    else:
        bmesh.ops.create_cube(bm, size=1.0, calc_uvs=True)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("_cut", me)
    bpy.context.scene.collection.objects.link(o)
    if isinstance(b, dict):
        ax = "xyz".index(b["axis"])
        c = Vector(b["cyl"])
        c[ax] = (b["h"][0] + b["h"][1]) / 2
        o.location = c
        o.scale = (b["r"], b["r"], b["h"][1] - b["h"][0])
        o.rotation_euler = [(0, math.pi / 2, 0), (math.pi / 2, 0, 0), (0, 0, 0)][ax]
    else:
        lo, hi = Vector(b[:3]), Vector(b[3:])
        o.location = (lo + hi) / 2
        o.scale = hi - lo
        o.rotation_euler = (0, 0, math.radians(rz))
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


def part_boxes(p):
    return p["boxes"] if "boxes" in p else [p["box"]]


def set_origin(obj, p):
    p = Vector(p)
    obj.data.transform(Matrix.Translation(-p))
    obj.location = p


def build(name, cfg):
    obj, _ = T.import_joined(os.path.join(ROOT, "export", f"{name}_idle.glb"))
    T.clear_custom_normals(obj)
    c = avg_color(obj)
    pat = cfg.get("pattern", "wood")                  # wood — доски, metal — крашеный металл, plain — ткань/пластик
    c_in = np.array(cfg["inside_rgb"]) ** 2.2 if "inside_rgb" in cfg else c * 0.45
    m_cut = wood_mat(f"{name}_cut", c * 0.8, 1, cfg.get("cut_pattern", pat))   # торцы и обратная сторона дверцы
    m_in = wood_mat(f"{name}_inside", c_in, 2, pat)                             # пустота внутри
    obj.data.materials.append(m_cut)
    obj.data.materials.append(m_in)
    parts = []
    for p in cfg["parts"]:
        pieces = []
        for b in part_boxes(p):                         # кусок из нескольких коробок (не пересекаются) — склеить
            o = obj.copy()
            o.data = obj.data.copy()
            bpy.context.scene.collection.objects.link(o)
            cut = box_obj(b, m_cut)
            boolean(o, cut, "INTERSECT")
            bpy.data.objects.remove(cut)
            pieces.append(o)
        o = pieces[0]
        if len(pieces) > 1:
            bpy.ops.object.select_all(action="DESELECT")
            for q in pieces:
                q.select_set(True)
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.join()
        for h in p.get("hollow", []):                   # выдвижной ящик / ниша в дверце — вычесть изнутри куска
            cut = box_obj(h, m_in)
            boolean(o, cut, "DIFFERENCE")
            bpy.data.objects.remove(cut)
        o.name = o.data.name = p["name"]
        parts.append((o, p))
    for b in [b for p in cfg["parts"] for b in part_boxes(p)] + cfg.get("cavity", []):
        cut = box_obj(b, m_in)
        boolean(obj, cut, "DIFFERENCE")
        bpy.data.objects.remove(cut)
    for b in cfg.get("add", []):                        # простое нутро: сиденья, полки — коробки цвета «внутри»
        a = box_obj(b, m_in)
        a.hide_render = False
        a.data.materials.clear()
        for m in obj.data.materials:
            a.data.materials.append(m)
        for f in a.data.polygons:
            f.material_index = list(obj.data.materials).index(m_in)
        bpy.ops.object.select_all(action="DESELECT")
        a.select_set(True)
        bpy.context.view_layer.objects.active = a
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.join()
    obj.name = obj.data.name = "body"
    for o in [obj] + [o for o, _ in parts]:
        T.smooth_by_angle(o)
        project_uv(o, (m_cut, m_in))
    for o, p in parts:
        if isinstance(p["pivot"], str):                 # "left_edge" / "right_edge" — петля по краю полотна
            co = np.array([v.co[:] for v in o.data.vertices])
            x = co[:, 0].min() if p["pivot"] == "left_edge" else co[:, 0].max()
            edge = co[np.abs(co[:, 0] - x) < 0.04]
            p["pivot"] = [float(x), float(np.median(edge[:, 1])), 0.0]
        set_origin(o, p["pivot"])
    if not len(obj.data.polygons):                      # отдельное полотно двери — корпуса нет
        bpy.data.objects.remove(obj)
        obj = None
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
            if isinstance(ax, str):
                o.rotation_euler["xyz".index(ax)] = math.radians(deg * t)
            else:                                   # ось — вектор (петля не вдоль X/Y/Z)
                o.rotation_euler = Matrix.Rotation(math.radians(deg * t), 3, Vector(ax).normalized()).to_euler()
        if "move" in op:
            o.location = Vector(p["pivot"]) + Vector(op["move"]) * t


def preview(name, body, parts, tmp):
    objs = [o for o in [body] + [o for o, _ in parts] if o is not None]
    co = np.array([o.matrix_world @ v.co for o in objs for v in o.data.vertices])
    me = bpy.data.meshes.new("_frame")                  # невидимая «рамка» в мировых координатах — по ней камера
    me.from_pydata([tuple(co.min(0)), tuple(co.max(0))], [], [])
    fr = bpy.data.objects.new("_frame", me)
    bpy.context.scene.collection.objects.link(fr)
    rows = []
    for t, tag in ((0.0, "closed"), (1.0, "open")):
        pose(parts, t)
        bpy.context.view_layer.update()
        rows += T.render_views(fr, os.path.join(tmp, f"{name}_{tag}"), px=360, fit=1.7)
    pose(parts, 0.0)
    bpy.data.objects.remove(fr)
    return rows


def to_godot(v):
    """Blender (x, y, z), Z вверх → Godot (x, z, −y), Y вверх."""
    return [round(float(v[0]), 4), round(float(v[2]), 4), round(-float(v[1]), 4)]


def game_info(parts):
    """Для игры: имя узла, точка петли и как открыть — в координатах Godot (как в .glb)."""
    out = []
    for _, p in parts:
        op, d = p["open"], {"node": p["name"], "pivot": to_godot(p["pivot"])}
        if "rot" in op:
            ax, deg = op["rot"]
            axv = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[ax] if isinstance(ax, str) else ax
            d["rotate_axis"], d["rotate_deg"] = to_godot(axv), deg
        if "move" in op:
            d["move"] = to_godot(op["move"])
        out.append(d)
    return out


def save_game_info(name, parts):
    path = os.path.join(OUT, "open_parts.json")
    info = json.load(open(path)) if os.path.exists(path) else {}
    info["_comment"] = ("Открывающиеся модели export/parts/<имя>.glb: узел body — корпус, остальные узлы — подвижные части. "
                        "Точка узла (origin) уже стоит на петле (pivot). Открыть: повернуть узел вокруг rotate_axis на rotate_deg "
                        "градусов (локально, от закрытого положения) и/или сдвинуть на move (метры). Координаты Godot.")
    info[name] = game_info(parts)
    json.dump(info, open(path + ".tmp", "w"), ensure_ascii=False, indent=1)
    os.replace(path + ".tmp", path)


def main(argv):
    cfg = json.load(open(CFG))
    sheet_name = argv[argv.index("--sheet") + 1] if "--sheet" in argv else ""
    names = [a for a in argv if not a.startswith("--") and a != sheet_name] or [k for k in cfg if not k.startswith("_")]
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(ROOT, "renders", "_review", "tripo_views")
    os.makedirs(tmp, exist_ok=True)
    rows = []
    for n in names:
        body, parts = build(n, cfg[n])
        objs = [o for o in [body] + [o for o, _ in parts] if o is not None]
        mb = export(objs, os.path.join(OUT, f"{n}.glb"))
        tri = {o.name: T.tris(o) for o in objs}
        save_game_info(n, parts)
        print(f"[{n}] {mb:.2f} МБ, треугольники: {tri}", flush=True)
        if "--preview" in argv:
            ims = preview(n, body, parts, tmp)
            rows.append((f"{n}\nслева — закрыто (спереди, 3/4), справа — открыто; части: "
                         + ", ".join(p['name'] for _, p in parts), ims))
    if rows:
        out = os.path.join(ROOT, "renders", "_review", f"open_parts{'_' + sheet_name if sheet_name else ''}_{datetime.date.today()}.png")
        T.sheet(rows, out)
        from PIL import Image
        Image.open(out).convert("RGB").save(out[:-4] + ".jpg", quality=88)
        os.remove(out)
        print("лист:", out[:-4] + ".jpg")


if __name__ == "__main__":
    main(sys.argv[1:])
