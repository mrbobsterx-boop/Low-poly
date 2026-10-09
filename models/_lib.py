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

TRI_LIMITS = {"small": 600, "furniture": 3000, "large": 5000, "human": 3000, "room": 8000}
_saved = []          # готовые объекты — в общий .blend
QUALITY = False      # режим качества docs/QUALITY.md (включает скрипт модели: L.quality()) — см. ниже


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


def _from_bmesh(bm, name, color, glow=False, keep_smooth=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    me.materials.append(_material(glow))
    if not keep_smooth:
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


def _bevel(bm, width, segs=None, hard=True):
    if width <= 0:
        return
    if QUALITY and hard:        # хард-сёрфейс: фаска маленькая, 1 сегмент — ребро чёткое, ловит свет
        width, segs = max(0.004, min(width, 0.015)), 1
    bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=width, offset_type="OFFSET",
                    segments=segs or (BEVEL_SEGS if width >= 0.008 else 1), profile=0.5, affect="EDGES", clamp_overlap=True)


def box(size, loc, color, rot=None, name="box", glow=False, bevel=None, hard=True):
    """Коробка size=(ширина X, глубина Y, высота Z); loc — центр НИЗА коробки; rot — градусы (x, y, z)
    вокруг центра низа. bevel — фаска (по умолчанию BEVEL, но не больше трети самой тонкой стороны).
    hard=False — мягкое (подушка): в режиме качества фаска не урезается и сглаживается."""
    sx, sy, sz = size
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(0, 0, sz / 2), verts=bm.verts)
    _bevel(bm, min(BEVEL if bevel is None else bevel, min(size) / 3), hard=hard)
    smooth = QUALITY and not hard
    if smooth:
        for f in bm.faces:
            f.smooth = True
    return _place(_from_bmesh(bm, name, color, glow, keep_smooth=smooth), loc, rot)


def cyl(radius, height, loc, color, verts=8, rot=None, name="cyl", radius_top=None, glow=False):
    """Цилиндр (или конус, если radius_top) вдоль Z; loc — центр низа; verts — граней по кругу (low-poly: 6–10).
    В режиме качества: не меньше 8 граней (у толстых — 12), бока сглажены, торцы — чёткие."""
    if QUALITY:
        verts = max(verts, 12 if max(radius, radius_top or 0) > 0.05 else 8)
    bm = bmesh.new()
    rt_ = radius if radius_top is None else radius_top
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=radius, radius2=rt_, depth=height)
    bmesh.ops.translate(bm, vec=(0, 0, height / 2), verts=bm.verts)
    # повернуть, чтобы грань (а не ребро) смотрела на камеру
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / verts, 3, "Z"))
    if QUALITY:
        _smooth_by_angle(bm, 40)
    return _place(_from_bmesh(bm, name, color, glow, keep_smooth=QUALITY), loc, rot)


def _smooth_by_angle(bm, deg):
    """Сглаженные нормали, но рёбра острее deg градусов — чёткие (как Auto Smooth)."""
    bm.normal_update()
    lim = math.cos(math.radians(deg))
    for f in bm.faces:
        f.smooth = True
    for e in bm.edges:
        lf = e.link_faces
        e.smooth = not (len(lf) == 2 and lf[0].normal.dot(lf[1].normal) < lim)


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


PREVIEW = None      # список — режим render/_lit_preview.py: finish() только собирает модель


def assemble(parts, name, rough=None, period=None, chips_n=0):
    """Склеить куски в один объект + неровные грани (кроме режима качества — там roughen только у органики)."""
    obj = join(parts, name)
    if rough is not False and not (QUALITY and rough is None):
        roughen(obj, period=period, **(rough or {}))
    if chips_n:                 # сколы цветом палитры (для broken)
        obj = chips(obj, n=chips_n, seed=len(name))
    return obj


def finish(parts, category, oid, variation, state, size_cm=None, limit="furniture", glb=True, margin_px=0,
           frame_points=None, lit=False, rough=None, period=None, chips_n=0):
    """Склеить, проверить, экспортировать .glb и отрендерить <id>_<вариация>_<состояние>(.png + _n.png).
    size_cm — (ширина, высота) из ОС для проверки (допуск 2 см). Возвращает объект."""
    name = f"{oid}_{variation}_{state}"
    obj = assemble(parts, name, rough=rough, period=period, chips_n=chips_n)
    if PREVIEW is not None:     # режим просмотра (render/_lit_preview.py): только собрать, без экспорта и рендера
        PREVIEW.append(obj)
        return obj
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
    # палитру встроить в файл — иначе на другом компьютере модель будет розовой (нет пути к palette.png)
    for img in bpy.data.images:
        if img.filepath and not img.packed_file:
            img.pack()
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


# ───────────────────────── Поломка (broken) ─────────────────────────
# Правило автора: сломанный вид не рисуем отдельно — его делает break_parts() из целого.
# Только для предметов, которые в ОС ломаются (docs/breakable.json). Промежуточные стадии и анимацию — игра.

def breaks_in_os(oid):
    import json
    try:
        return oid in json.load(open(os.path.join(ROOT, "docs", "breakable.json")))["ids"]
    except FileNotFoundError:
        return False


def _bb(o):
    vs = [v.co for v in o.data.vertices]
    return (min(v.x for v in vs), max(v.x for v in vs), min(v.y for v in vs), max(v.y for v in vs),
            min(v.z for v in vs), max(v.z for v in vs))


def _color_of(o):
    sys.path.insert(0, os.path.join(ROOT, "palette"))
    import _palette
    uvl = o.data.uv_layers.active
    if not uvl or not len(o.data.loops):
        return None
    u, v = uvl.data[0].uv
    return _palette.name_at(u, v)[0]


CHIP = {  # чем «светит» скол/повреждение на этом цвете
    "wood": "wood_light", "wood_dark": "wood", "wood_light": "wood_dark",
    "army_green": "steel", "khaki": "steel", "olive_dark": "steel", "khaki_light": "steel",
    "paint_red": "steel", "paint_blue": "steel", "hazard_yellow": "steel",
    "steel": "rust", "steel_dark": "rust", "steel_light": "rust_light", "soot": "rust_dark",
    "rust": "rust_dark", "rust_dark": "rust", "cloth_blue": "dirt", "cloth_beige": "dirt",
    "offwhite": "dirt", "khaki_light_": "dirt", "concrete": "concrete_light", "concrete_dark": "concrete",
}


def _detect(parts):
    B = [_bb(o) for o in parts]
    X0, X1 = min(b[0] for b in B), max(b[1] for b in B)
    Y0 = min(b[2] for b in B)
    Z1 = max(b[5] for b in B)
    legs, doors, lids = [], [], []
    for o, b in zip(parts, B):
        dx, dy, dz = b[1] - b[0], b[3] - b[2], b[5] - b[4]
        if b[4] < 0.05 and dx < 0.13 and dy < 0.13 and dz > 0.12:
            legs.append(o)
        elif dy < 0.04 and dz > 0.3 and dx > 0.1 and b[2] < Y0 + 0.06:
            doors.append(o)
        elif b[5] > Z1 - max(0.03, 0.35 * Z1) and dx > 0.6 * (X1 - X0) and dz < 0.15 and b[4] > 0.05 * Z1:
            lids.append(o)
    return legs, doors, lids, (X0, X1, Y0, Z1)


def _move(objs, m):
    for o in objs:
        o.data.transform(m)


def _cut(o, z, keep_below):
    """Разрезать кусок плоскостью Z = z; оставить нижнюю (keep_below) или верхнюю часть."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    geom = list(bm.verts) + list(bm.edges) + list(bm.faces)
    res = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, z), plane_no=(0, 0, 1),
                                 clear_outer=keep_below, clear_inner=not keep_below)
    edges = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    if edges:
        bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    bm.to_mesh(o.data)
    bm.free()


def _debris(parts, colors, box_bb, seed, n=6):
    import random
    r = random.Random(seed)
    X0, X1, Y0, _ = box_bb
    out = []
    for i in range(n):
        s = r.uniform(0.03, 0.10)
        x = r.uniform(X0 - 0.10, X1 + 0.10)
        y = Y0 - r.uniform(0.02, 0.18)
        out.append(box((s, s * r.uniform(0.4, 1.0), s * r.uniform(0.25, 0.6)), (x, y, 0), r.choice(colors),
                       rot=(0, 0, r.uniform(0, 180)), bevel=0.004))
    return parts + out


def break_parts(parts, kind="auto", seed=1):
    """Сломать предмет из целых кусков. kind: auto | legs | door | lid | tilt.
    legs — подломить ножки одной стороны, предмет заваливается, обломок на полу;
    door — сорвать дверцу (висит на одной петле, распахнута); lid — сбить крышку, выбить доску;
    tilt — завалить набок. Всегда: обломки на полу (сколы цветом — в finish, state=broken)."""
    import random
    r = random.Random(seed)
    legs, doors, lids, bb = _detect(parts)
    X0, X1, Y0, Z1 = bb
    if kind == "auto":
        kind = "door" if doors else ("legs" if len(legs) >= 2 else ("lid" if lids else "tilt"))
    colors = [c for c in (_color_of(o) for o in parts) if c and not c.startswith("glow")]
    main = max(set(colors), key=colors.count) if colors else "steel"
    deb_cols = [main, CHIP.get(main, main), "soot"]

    if kind == "legs":
        side = 1 if any(_bb(o)[0] > (X0 + X1) / 2 for o in legs) else -1
        broken = [o for o in legs if (_bb(o)[0] + _bb(o)[1]) / 2 * side > (X0 + X1) / 2 * side]
        cut_z = min(_bb(o)[5] for o in broken) * 0.40
        gap = min(0.14, cut_z * 0.8)
        stubs, fallen = [], []
        for o in broken:
            b = _bb(o)
            stub = o.copy()
            stub.data = o.data.copy()
            bpy.context.scene.collection.objects.link(stub)
            _cut(stub, cut_z, keep_below=True)
            _cut(o, cut_z + gap, keep_below=False)
            stubs.append(stub)
            w = max(b[1] - b[0], b[3] - b[2])
            fallen.append(box((gap + 0.04, w, w), ((b[0] + b[1]) / 2 + side * 0.12, Y0 - 0.12, 0),
                              _color_of(o) or main, rot=(0, 0, r.uniform(-30, 30)), bevel=0.004))
        rest = [o for o in parts if o not in stubs]
        pivot_x = X0 if side > 0 else X1
        ang = math.atan2(gap, (X1 - X0)) * side
        _move(rest, Matrix.Translation((pivot_x, 0, 0)) @ Matrix.Rotation(ang, 4, "Y")
              @ Matrix.Translation((-pivot_x, 0, 0)))
        parts = rest + stubs + fallen

    elif kind == "door":
        door = max(doors, key=lambda o: (_bb(o)[0] + _bb(o)[1]) / 2)
        db = _bb(door)
        hinge_right = (db[0] + db[1]) / 2 > (X0 + X1) / 2
        hx = db[1] if hinge_right else db[0]
        group = [o for o in parts if o is door or (
            db[0] - 0.01 <= (_bb(o)[0] + _bb(o)[1]) / 2 <= db[1] + 0.01 and _bb(o)[3] <= db[3] + 0.002
            and _bb(o)[4] >= db[4] - 0.01 and _bb(o)[5] <= db[5] + 0.01)]
        ang = math.radians(80 if hinge_right else -80)
        sag = math.radians(-7 if hinge_right else 7)
        m = (Matrix.Translation((hx, db[2], db[5])) @ Matrix.Rotation(sag, 4, "Y")
             @ Matrix.Rotation(ang, 4, "Z") @ Matrix.Translation((-hx, -db[2], -db[5]))
             @ Matrix.Translation((0, 0, -0.03)))
        _move(group, m)

    elif kind == "lid":
        lid_z0 = min(_bb(o)[4] for o in lids)
        group = [o for o in parts if _bb(o)[4] >= lid_z0 - 0.005]
        gb = [_bb(o) for o in group]
        yb, zb = max(b[3] for b in gb), lid_z0
        m = (Matrix.Translation((X1 + 0.05, 0, 0)) @ Matrix.Rotation(math.radians(-15), 4, "Z")
             @ Matrix.Translation((0, 0, 0.0)) @ Matrix.Rotation(math.radians(-8), 4, "Y")
             @ Matrix.Translation((-X0, 0, -zb)))
        _move(group, m)                                   # крышка сбита и лежит рядом справа
        body = [o for o in parts if o not in group]
        fronts = [o for o in body if _bb(o)[2] < Y0 + 0.03 and (_bb(o)[1] - _bb(o)[0]) > 0.2]
        if fronts:                                        # выбить одну переднюю доску/панель
            knocked = r.choice(fronts)
            kb = _bb(knocked)
            parts = [o for o in parts if o is not knocked]
            _move([knocked], Matrix.Translation(((kb[0] + kb[1]) / 2 + 0.0, Y0 - 0.25, -kb[4]))
                  @ Matrix.Rotation(math.radians(12), 4, "Z")
                  @ Matrix.Translation((-(kb[0] + kb[1]) / 2, -kb[2], 0)))
            parts.append(knocked)
            parts.append(box((kb[1] - kb[0] - 0.02, 0.01, kb[5] - kb[4]), ((kb[0] + kb[1]) / 2, kb[2] + 0.03, kb[4]),
                             "soot", bevel=0))            # тёмная пустота внутри
    else:  # tilt
        ang = math.radians(9)
        _move(parts, Matrix.Translation((X1, 0, 0)) @ Matrix.Rotation(ang, 4, "Y") @ Matrix.Translation((-X1, 0, 0)))

    # опустить на пол: нижняя точка — Z = 0
    zmin = min(_bb(o)[4] for o in parts)
    _move(parts, Matrix.Translation((0, 0, -zmin)))
    return _debris(parts, deb_cols, (X0, X1, Y0, Z1), seed)


def chips(obj, n=10, seed=1):
    """Сколы/вмятины цветом палитры на передних гранях (луч спереди → точка на поверхности)."""
    import random
    from mathutils.bvhtree import BVHTree
    sys.path.insert(0, os.path.join(ROOT, "palette"))
    import _palette
    r = random.Random(seed)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    uvl = bm.loops.layers.uv.active
    tree = BVHTree.FromBMesh(bm)
    x0, x1, y0, _, z0, z1 = _bb(obj)
    out = []
    tries = 0
    while len(out) < n and tries < n * 12:
        tries += 1
        x, z = r.uniform(x0, x1), r.uniform(z0 + 0.02, z1)
        loc, nor, idx, _ = tree.ray_cast(Vector((x, y0 - 1.0, z)), Vector((0, 1, 0)))
        if loc is None or nor.y > -0.5:
            continue
        f = bm.faces[idx]
        name = _palette.name_at(*f.loops[0][uvl].uv)[0] if uvl else None
        if not name or name.startswith("glow"):
            continue
        s = r.uniform(0.025, 0.07)
        out.append(spot((loc.x, loc.y, loc.z), s, CHIP.get(name, "soot"), seed=seed * 31 + tries,
                        stretch=(r.uniform(0.7, 1.4), r.uniform(0.6, 1.2))))
    bm.free()
    if out:
        obj = join([obj] + out, obj.name)
    return obj


MAKE_BROKEN = False   # решение автора: пока только idle; сломанный вид — break_parts(), включить здесь


def make(builder, category, oid, variation, size_cm=None, limit="furniture", broken="auto", seed=1, **kw):
    """Целый вид + (если в ОС ломается) сломанный — одним параметром broken (auto | legs | door | lid | tilt | None)."""
    finish(builder(), category, oid, variation, "idle", size_cm=size_cm, limit=limit, **kw)
    if MAKE_BROKEN and broken and breaks_in_os(oid):
        parts = break_parts(builder(), broken, seed=seed)
        rough = dict(kw.pop("rough", None) or {})
        rough.setdefault("amp_max", 0.02)
        rough.setdefault("shade_p", 0.55)
        finish(parts, category, oid, variation, "broken", limit=limit, rough=rough, chips_n=12, **kw)


# ───────────────────────── Размер из плана ОС и детали ─────────────────────────
def size_cm(oid):
    """(ширина, высота) объекта в см — из docs/plan.json (ОС; при расхождении — план, решение автора)."""
    import json
    for o in json.load(open(os.path.join(ROOT, "docs", "plan.json"))):
        if o["id"] == oid:
            return tuple(o["size"])
    raise KeyError(oid)


def tube(a, b, r, color, verts=6, name="tube", glow=False):
    """Труба/пруток от точки a до точки b (мира), радиус r."""
    a, b = Vector(a), Vector(b)
    d = b - a
    o = cyl(r, d.length, (0, 0, 0), color, verts=verts, name=name, glow=glow)
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    o.data.transform(Matrix.Translation(a) @ q.to_matrix().to_4x4())
    return o


def soft(size, loc, color, rot=None, name="soft"):
    """Мягкое (подушка, сиденье, матрас): коробка с крупной фаской — «пухлая»."""
    return box(size, loc, color, rot=rot, name=name, bevel=min(size) * 0.3, hard=False)


def blanket(cx, width, depth, top_z, color, seed=7, hang=(0.10, 0.20), fold_color="offwhite", fold_side=-1):
    """Мятое одеяло из граней: лежит на матрасе (центр cx, ширина width, глубина depth, верх top_z) и неровно
    свешивается вперёд; у края fold_side (−1 слева / +1 справа) — отвёрнутый край-простыня. Возвращает список."""
    import random
    rnd = random.Random(seed)
    hng = [rnd.uniform(*hang) for _ in range(13)]

    def z(u, v):
        f = 0.02 + 0.022 * math.sin(u * 9.0 + v * 2.0 + seed) ** 2 + 0.015 * math.sin(u * 17.0 - v * 5.0) ** 2
        if v < 0.16:
            k = (0.16 - v) / 0.16
            return -hng[round(u * 12)] * k * 1.6 + f * (1 - k)
        return f
    out = [sheet(12, 9, width, depth + 0.20, (cx, -0.06, top_z), color, z_fn=z, jitter=0.01, seed=seed)]
    if fold_color:
        out.append(sheet(3, 6, 0.16, depth - 0.04, (cx + fold_side * (width / 2 + 0.06), 0.0, top_z + 0.005), fold_color,
                         z_fn=lambda u, v: 0.03 * math.sin(u * math.pi), jitter=0.008, seed=seed + 1))
    return out
