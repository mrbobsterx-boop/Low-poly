"""Общие заготовки для скриптов моделей (models/<категория>/<id>.py).

Модель строится из простых кусков (box, cyl, prism), каждый сразу красится цветом палитры по имени.
finish() склеивает куски, проверяет размер и треугольники, экспортирует .glb и рендерит пару картинок.

Правила (README): 1 = 1 м, origin внизу по центру (висящее — в точке крепления), «перед» к −Y,
плоское затенение, только цвета палитры, без света и грязи.
"""
import math
import os
import sys

import bpy
import bmesh  # noqa: E402 — только после bpy
from mathutils import Matrix, Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "render"))
import _template as rt  # noqa: E402

TRI_LIMITS = {"small": 300, "furniture": 1500, "human": 3000, "room": 8000}
_saved = []          # готовые объекты — в общий .blend


def new_scene():
    rt.setup_scene()
    _saved.clear()


def _material(glow=False):
    if not glow:
        return rt.palette_material()
    mat = bpy.data.materials.get("palette_glow")
    if mat:
        return mat
    # Светящееся: тот же цвет палитры, но Emission (в игре свечение добавит Godot)
    mat = bpy.data.materials.new("palette_glow")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.interpolation = "Closest"
    tex.image = bpy.data.images.load(os.path.join(ROOT, "palette", "palette.png"), check_existing=True)
    emi = nt.nodes.new("ShaderNodeEmission")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tex.outputs["Color"], emi.inputs["Color"])
    nt.links.new(emi.outputs["Emission"], out.inputs["Surface"])
    return mat


def _from_bmesh(bm, name, color, glow=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    me.materials.append(_material(glow))
    for p in me.polygons:
        p.use_smooth = False
    rt.paint(obj, color)
    return obj


def _place(obj, loc, rot):
    m = Matrix.Translation(Vector(loc))
    if rot:
        m = m @ Matrix.Rotation(math.radians(rot[2]), 4, "Z") @ Matrix.Rotation(math.radians(rot[1]), 4, "Y") \
            @ Matrix.Rotation(math.radians(rot[0]), 4, "X")
    obj.data.transform(m)
    return obj


BEVEL = 0.012   # фаска по рёбрам, м: рёбра ловят свет — «рубленые грани»


BEVEL_SEGS = 2  # сегментов фаски: 2 — мягкое ребро, ловит блик


def _bevel(bm, width, segs=None):
    if width <= 0:
        return
    bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=width, offset_type="OFFSET",
                    segments=segs or (BEVEL_SEGS if width >= 0.008 else 1), profile=0.5, affect="EDGES", clamp_overlap=True)


def box(size, loc, color, rot=None, name="box", glow=False, bevel=None):
    """Коробка size=(ширина X, глубина Y, высота Z); loc — центр НИЗА коробки; rot — градусы (x, y, z)
    вокруг центра низа. bevel — фаска (по умолчанию BEVEL, но не больше трети самой тонкой стороны)."""
    sx, sy, sz = size
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(0, 0, sz / 2), verts=bm.verts)
    _bevel(bm, min(BEVEL if bevel is None else bevel, min(size) / 3))
    return _place(_from_bmesh(bm, name, color, glow), loc, rot)


def cyl(radius, height, loc, color, verts=8, rot=None, name="cyl", radius_top=None, glow=False):
    """Цилиндр (или конус, если radius_top) вдоль Z; loc — центр низа; verts — граней по кругу (low-poly: 6–10)."""
    bm = bmesh.new()
    rt_ = radius if radius_top is None else radius_top
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=radius, radius2=rt_, depth=height)
    bmesh.ops.translate(bm, vec=(0, 0, height / 2), verts=bm.verts)
    # повернуть, чтобы грань (а не ребро) смотрела на камеру
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / verts, 3, "Z"))
    return _place(_from_bmesh(bm, name, color, glow), loc, rot)


def poly(points_xz, depth, loc, color, rot=None, name="poly", glow=False):
    """Плоская фигура по точкам (x, z) в плоскости фасада, вытянутая на depth по Y; loc — смещение."""
    bm = bmesh.new()
    front = [bm.verts.new((x, -depth / 2, z)) for x, z in points_xz]
    back = [bm.verts.new((x, depth / 2, z)) for x, z in points_xz]
    n = len(points_xz)
    bm.faces.new(front[::-1])
    bm.faces.new(back)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([front[i], front[j], back[j], back[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _place(_from_bmesh(bm, name, color, glow), loc, rot)


def join(objs, name):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    obj.data.name = name
    return obj


def tris(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)


def dims(obj):
    xs = [v.co.x for v in obj.data.vertices]
    ys = [v.co.y for v in obj.data.vertices]
    zs = [v.co.z for v in obj.data.vertices]
    return (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)), (min(zs), max(zs))


def finish(parts, category, oid, variation, state, size_cm=None, limit="furniture", glb=True, margin_px=0,
           frame_points=None, lit=True):
    """Склеить, проверить, экспортировать .glb и отрендерить <id>_<вариация>_<состояние>(.png + _n.png).
    size_cm — (ширина, высота) из ОС для проверки (допуск 2 см). Возвращает объект."""
    name = f"{oid}_{variation}_{state}"
    obj = join(parts, name)
    (w, d, h), (zmin, zmax) = dims(obj)
    t = tris(obj)
    print(f"[{name}] {w * 100:.0f} × {h * 100:.0f} см (глубина {d * 100:.0f}), треугольников {t}"
          f" / лимит {TRI_LIMITS[limit]}")
    if t > TRI_LIMITS[limit]:
        print(f"  !!! больше лимита")
    if size_cm and state == "idle":
        ok_w = abs(w * 100 - size_cm[0]) <= 2
        ok_h = abs(h * 100 - size_cm[1]) <= 2
        if not (ok_w and ok_h):
            print(f"  !!! размер не как в ОС ({size_cm[0]} × {size_cm[1]} см)")

    if glb:
        os.makedirs(os.path.join(ROOT, "export"), exist_ok=True)
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, "export", name + ".glb"), export_format="GLB",
                                  use_selection=True, export_apply=True, export_yup=True,
                                  export_animations=False)
    size = rt.render_pair([obj], f"renders/{category}/{name}", margin_px=margin_px, frame_points=frame_points)
    print(f"  рендер {size[0]} × {size[1]} px")
    if lit:   # показательные рендеры со светом — только для просмотра: прямо и с поворотом на 20°
        rt.render_lit([obj], f"renders/_review/{name}_lit.png")
        obj.rotation_euler[2] = math.radians(20)
        rt.render_lit([obj], f"renders/_review/{name}_lit_yaw20.png")
        obj.rotation_euler[2] = 0
    # убрать из кадра следующих рендеров, но сохранить в .blend
    obj.hide_render = True
    _saved.append(obj)
    return obj


def save_blend(category, oid):
    """Все варианты рядом (по X через 1 м) в models/<категория>/<id>.blend — посмотреть в Blender."""
    x = 0.0
    for o in _saved:
        (w, _, _), _ = dims(o)
        o.location.x = x + w / 2
        o.hide_render = False
        x += w + 1.0
    path = os.path.join(ROOT, "models", category, oid + ".blend")
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
    for o in _saved:
        o.location.x = 0
    print("  сохранено:", os.path.relpath(path, ROOT))
