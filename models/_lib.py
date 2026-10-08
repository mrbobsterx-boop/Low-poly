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

TRI_LIMITS = {"small": 600, "furniture": 3000, "human": 3000, "room": 8000}
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
           frame_points=None, lit=False, rough=None, period=None):
    """Склеить, проверить, экспортировать .glb и отрендерить <id>_<вариация>_<состояние>(.png + _n.png).
    size_cm — (ширина, высота) из ОС для проверки (допуск 2 см). Возвращает объект."""
    name = f"{oid}_{variation}_{state}"
    obj = join(parts, name)
    if rough is not False:      # крупные неровные грани + разнобой оттенков (rough — параметры для roughen)
        roughen(obj, period=period, **(rough or {}))
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


def sheet(nx, ny, size_x, size_y, loc, color, z_fn=None, jitter=0.0, seed=1, thick=0.012, name="sheet"):
    """Ткань/лист из граней: сетка nx × ny, треугольники (видны грани), с толщиной.
    z_fn(u, v) → высота (u, v ∈ [0, 1]) — форма (складки, свес); jitter — случайная «мятость» (м).
    Сетка лежит в плоскости XY, loc — центр."""
    import random
    rnd = random.Random(seed)
    bm = bmesh.new()
    top, bot = {}, {}
    for j in range(ny + 1):
        for i in range(nx + 1):
            u, v = i / nx, j / ny
            z = (z_fn(u, v) if z_fn else 0.0) + (rnd.uniform(-jitter, jitter) if 0 < i < nx and 0 < j < ny else 0.0)
            x, y = (u - 0.5) * size_x, (v - 0.5) * size_y
            top[i, j] = bm.verts.new((x, y, z))
            bot[i, j] = bm.verts.new((x, y, z - thick))
    for j in range(ny):
        for i in range(nx):
            a, b, c, d = (i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)
            bm.faces.new([top[a], top[b], top[c], top[d]])
            bm.faces.new([bot[d], bot[c], bot[b], bot[a]])
    for i in range(nx):                                     # кромки
        bm.faces.new([top[i, 0], bot[i, 0], bot[i + 1, 0], top[i + 1, 0]])
        bm.faces.new([top[i + 1, ny], bot[i + 1, ny], bot[i, ny], top[i, ny]])
    for j in range(ny):
        bm.faces.new([top[0, j + 1], bot[0, j + 1], bot[0, j], top[0, j]])
        bm.faces.new([top[nx, j], bot[nx, j], bot[nx, j + 1], top[nx, j + 1]])
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _place(_from_bmesh(bm, name, color), loc, None)


def transform(objs, loc=(0, 0, 0), rot=None):
    """Сдвинуть/повернуть уже созданные куски (rot — градусы x, y, z вокруг начала координат)."""
    for o in objs:
        _place(o, loc, rot)
    return objs


def _rng(co, seed, period):
    """Случайность, зависящая от места (с периодом по X — чтобы бесшовные оболочки оставались бесшовными)."""
    import random
    x = (co.x % period) if period else co.x
    if period and abs(x - period) < 1e-3:
        x = 0.0
    return random.Random(hash((round(x, 3), round(co.y, 3), round(co.z, 3), seed)))


def roughen(obj, seed=1, min_area=0.03, k=0.035, amp_max=0.012, levels=2, shade_p=0.4, period=None):
    """«Крупные неровные грани» + «лёгкий разнобой оттенков».
    1) Большие грани (лицом к камере или вверх) разбиваются на треугольники; новая точка сдвигается вбок
       и ВНУТРЬ (вмятина) — наружу ничего не выпирает, пятна/детали поверх остаются видны.
    2) Каждой крупной грани случайно — чуть темнее/светлее того же цвета палитры (полосы квадрата)."""
    sys.path.insert(0, os.path.join(ROOT, "palette"))
    import _palette
    glow_idx = {i for i, m in enumerate(obj.data.materials) if m and m.name == "palette_glow"}
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    for _ in range(levels):
        bm.normal_update()
        faces = [f for f in bm.faces if f.material_index not in glow_idx and f.calc_area() > min_area
                 and (f.normal.y < -0.3 or f.normal.z > 0.3 or abs(f.normal.x) > 0.6)]
        if not faces:
            break
        res = bmesh.ops.poke(bm, faces=faces, offset=0.0, center_mode="MEAN_WEIGHTED")
        bm.normal_update()
        for v in res["verts"]:
            area = sum(f.calc_area() for f in v.link_faces)
            r = _rng(v.co, seed, period)
            n = v.normal.copy()
            # сдвиг вбок — к случайному соседу (ломает симметрию «звезды»)
            nb = [e.other_vert(v).co for e in v.link_edges]
            if nb:
                tgt = nb[r.randrange(len(nb))]
                v.co = v.co.lerp(tgt, r.uniform(0.0, 0.35))
            v.co -= n * r.uniform(0.25, 1.0) * min(amp_max, k * area ** 0.5)
    # разнобой оттенков
    uvl = bm.loops.layers.uv.active
    if uvl is not None:
        for f in bm.faces:
            if f.material_index in glow_idx or f.calc_area() < min_area / 6:
                continue
            u, v = f.loops[0][uvl].uv
            name, sh = _palette.name_at(u, v)
            if name is None or sh != 0:
                continue
            r = _rng(f.calc_center_median(), seed + 7, period)
            x = r.random()
            s = -1 if x < shade_p / 2 else (1 if x < shade_p else 0)
            if s:
                nu, nv = _palette.uv(name, s)
                for lp in f.loops:
                    lp[uvl].uv = (nu, nv)
    bm.to_mesh(obj.data)
    bm.free()
    for p in obj.data.polygons:
        p.use_smooth = False
    return obj


def spot(center, size, color, facing="front", seed=1, n=7, lift=0.003, stretch=(1.0, 1.0), name="spot"):
    """Пятно износа (скол, ржавчина, потёртость, грязь): неровная «клякса» из треугольников, чуть над поверхностью.
    facing: front — на фасаде (лицом к −Y), top — сверху (лицом вверх), left/right — на боку."""
    import random
    r = random.Random(seed)
    bm = bmesh.new()
    pts = []
    for i in range(n):
        a = 2 * math.pi * (i + r.uniform(-0.3, 0.3)) / n
        rad = size / 2 * r.uniform(0.55, 1.0)
        pts.append((math.cos(a) * rad * stretch[0], math.sin(a) * rad * stretch[1]))
    cx, cy, cz = center

    def P(a, b):
        if facing == "front":
            return (cx + a, cy - lift, cz + b)
        if facing == "top":
            return (cx + a, cy + b, cz + lift)
        s = -1 if facing == "left" else 1
        return (cx + s * lift, cy + a, cz + b)
    c = bm.verts.new(P(0, 0))
    ring = [bm.verts.new(P(a, b)) for a, b in pts]
    for i in range(n):
        f = bm.faces.new([c, ring[i], ring[(i + 1) % n]])
    bm.normal_update()
    want = {"front": Vector((0, -1, 0)), "top": Vector((0, 0, 1)), "left": Vector((-1, 0, 0)),
            "right": Vector((1, 0, 0))}[facing]
    if list(bm.faces)[0].normal.dot(want) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    return _from_bmesh(bm, name, color)


def prism(points, axis, a0, a1, color, name="prism", face_colors=None):
    """Призма: многоугольник points (2D) вытянут вдоль оси axis ('x', 'y' или 'z') от a0 до a1.
    Для 'z' точки — (x, y); для 'x' — (y, z); для 'y' — (x, z). face_colors — {номер ребра: цвет} — покрасить
    боковую грань ребра i (между точками i и i+1), например скос."""
    def P(u, v, w):
        return {"z": (u, v, w), "x": (w, u, v), "y": (u, w, v)}[axis]
    bm = bmesh.new()
    lo = [bm.verts.new(P(u, v, a0)) for u, v in points]
    hi = [bm.verts.new(P(u, v, a1)) for u, v in points]
    n = len(points)
    bm.faces.new(lo[::-1])
    bm.faces.new(hi)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([lo[i], lo[j], hi[j], hi[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    obj = _from_bmesh(bm, name, color)
    for i, c in (face_colors or {}).items():
        rt.paint(obj, c, faces=[2 + i])
    return obj
