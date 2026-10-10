"""Обработка моделей из Tripo → игра (docs/TRIPO.md, раздел 2). Blender как модуль bpy.

Запуск (из корня репозитория):
    python3 tools/tripo_process.py                 # всё новое из tripo/ (готовое в export/ пропускает)
    python3 tools/tripo_process.py --force         # заново всё
    python3 tools/tripo_process.py имя1 имя2       # только эти файлы (без .glb)
    python3 tools/tripo_process.py --color-test имя1 имя2 имя3
                                                   # цветовой фильтр tripo/color.json: лист «до / после», БЕЗ экспорта
Для каждой модели tripo/<id>_<вариант>.glb:
  1) импорт, все части — в один объект, трансформации применены;
  2) поворот передом к −Y (поправка — tripo/rotate.json: {"<имя файла>": градусы вокруг вертикали});
  3) точка опоры: пол — низ по центру (Z = 0); стена — спина в Y = 0, низ в Z = 0; потолок — верх в Z = 0
     (крепление — custom.mount из ОС, поле mount в docs/plan.json);
  4) высота — из ОС (docs/plan.json, size = [ширина, высота] см), пропорции — как у модели;
     ширина отличается > 15 % — строка в docs/DEVIATIONS.md;
  5) облегчение сетки (Decimate, UV сохраняются): мелкое ≤ 3 000, мебель ≤ 8 000, крупное ≤ 15 000 треугольников;
  6) текстуры ≤ 1024 (мелочь ≤ 512), металличность 0, шероховатость ≥ 0,7; цветовой фильтр — только если
     в tripo/color.json "approved": true;
  7) экспорт export/<id>_<вариант>_idle.glb (glTF 2.0, +Y вверх, текстуры внутри, JPEG), файл ≤ 3 МБ;
  8) отчёт docs/TRIPO_REPORT.md (+ данные docs/tripo_report.json) и лист превью renders/_review/tripo_<дата>.png:
     каждая модель со светом, спереди и в три четверти.
Ключи для проверки: --src <папка> (вместо tripo/), --out <папка> (вместо export/), --no-docs (не трогать docs/).
"""
import datetime
import json
import math
import os
import sys

import bpy
import bmesh  # noqa: E402 — только после bpy
import numpy as np
from mathutils import Matrix, Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LIMITS = {"small": 3000, "furniture": 8000, "large": 15000}
TEX = {"small": 512, "furniture": 1024, "large": 1024}
LARGE_CATS = {"machine", "building", "vehicle", "structure"}
MAX_MB = 3.0
ROUGH_MIN = 0.7
WIDTH_TOL = 0.15


# ───────────────────────── план ОС ─────────────────────────

def load_plan():
    return {o["id"]: o for o in json.load(open(os.path.join(ROOT, "docs", "plan.json")))}


def resolve(stem, plan):
    """Имя файла → (id, вариант, предупреждения). Самый длинный id из плана, с которого начинается имя."""
    warns = []
    ids = sorted((i for i in plan if stem == i or stem.startswith(i + "_")), key=len, reverse=True)
    if not ids:
        return None, None, [f"id не найден в плане ОС (docs/plan.json) — модель пропущена"]
    oid = ids[0]
    vars_ok = [v["slug"] for v in plan[oid]["variants"] if not v["skip"]]
    if stem == oid:
        var = vars_ok[0] if vars_ok else "default"
        warns.append(f"вариант не указан в имени — взят первый из плана: `{var}`")
    else:
        var = stem[len(oid) + 1:]
        if var not in vars_ok:
            skipped = [v["slug"] for v in plan[oid]["variants"] if v["skip"]]
            why = "этот вариант в плане пропускается (сломанный/состояние)" if var in skipped else "такого варианта нет в плане"
            warns.append(f"вариант `{var}`: {why} — проверить имя файла (варианты: {', '.join(vars_ok)})")
    return oid, var, warns


def size_class(o):
    w, h = (s / 100 for s in o["size"])
    if h >= 1.5 or o["cat"] in LARGE_CATS:
        return "large"
    if max(w, h) < 0.55:
        return "small"
    return "furniture"


# ───────────────────────── сетка ─────────────────────────

def tris(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)


def bbox(obj):
    co = np.empty(len(obj.data.vertices) * 3)
    obj.data.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    return co.min(0), co.max(0)


def import_joined(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    n_parts = len(meshes)
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    for o in list(bpy.context.scene.objects):
        if o.type != "MESH":
            bpy.data.objects.remove(o)
    if len(meshes) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    # glTF режет сетку по швам UV и нормалей — склеить совпадающие вершины (UV при этом сохраняются)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    lo, hi = bbox(obj)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=float(max(hi - lo)) * 1e-5)
    bm.to_mesh(obj.data)
    bm.free()
    return obj, n_parts


def smooth_by_angle(obj, deg=45):
    """Сглаживание как у Tripo, но острые рёбра (> deg) — чёткие."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.normal_update()
    lim = math.cos(math.radians(deg))
    for f in bm.faces:
        f.smooth = True
    for e in bm.edges:
        lf = e.link_faces
        e.smooth = not (len(lf) == 2 and lf[0].normal.dot(lf[1].normal) < lim)
    bm.to_mesh(obj.data)
    bm.free()


def islands(obj):
    """Связные куски сетки: список (число вершин, bbox min, bbox max)."""
    me = obj.data
    n = len(me.vertices)
    parent = np.arange(n)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    ev = np.empty(len(me.edges) * 2, dtype=np.int64)
    me.edges.foreach_get("vertices", ev)
    for a, b in ev.reshape(-1, 2):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    roots = np.array([find(i) for i in range(n)])
    co = np.empty(n * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    out = []
    for r in np.unique(roots):
        pts = co[roots == r]
        out.append((len(pts), pts.min(0), pts.max(0)))
    return sorted(out, key=lambda t: -t[0])


def check_mesh(obj):
    """Предупреждения: отдельные куски рядом с главным (приросшие лишние вещи), висящие в воздухе, дыры."""
    warns = []
    isl = islands(obj)
    lo, hi = bbox(obj)
    size = float(max(hi - lo))
    if isl:
        _, mlo, mhi = isl[0]
        tol = 0.02 + 0.02 * size
        apart, floating = 0, 0
        for cnt, a, b in isl[1:]:
            big = max(b - a) > 0.08 * size
            touches = all(a[k] <= mhi[k] + tol and b[k] >= mlo[k] - tol for k in range(3))
            if big and not touches:
                apart += 1
            if big and a[2] > lo[2] + 0.05 * size and not touches:
                floating += 1
        if apart:
            warns.append(f"{apart} отдельн. крупн. кус(ка/ков) в стороне от главного — возможно, лишняя вещь с картинки "
                         f"(рюкзак, ящик…) — посмотреть на превью")
        if floating:
            warns.append(f"{floating} кус(ка/ков) висит в воздухе")
        if len(isl) > 60:
            warns.append(f"много мелких отдельных кусков ({len(isl)}) — Tripo мог «насорить»")
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    open_edges = sum(1 for e in bm.edges if len(e.link_faces) == 1)
    bm.free()
    if open_edges > 0.02 * len(obj.data.edges) and open_edges > 50:
        warns.append(f"открытые края (дыры в сетке): {open_edges} рёбер")
    return warns


def place(obj, o, rot_deg):
    """Поворот, масштаб по высоте ОС, точка опоры по креплению. Возвращает (ширина, глубина, высота) м."""
    if rot_deg:
        obj.data.transform(Matrix.Rotation(math.radians(rot_deg), 4, "Z"))
    lo, hi = bbox(obj)
    h = float(hi[2] - lo[2])
    target_h = o["size"][1] / 100
    k = target_h / h if h > 1e-6 else 1.0
    obj.data.transform(Matrix.Scale(k, 4))
    lo, hi = bbox(obj)
    cx, cy = (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2
    mount = o.get("mount", "floor")
    if mount == "wall":
        shift = (-cx, -hi[1], -lo[2])          # спина к стене (Y = 0), низ — Z = 0
    elif mount == "ceiling":
        shift = (-cx, -cy, -hi[2])             # верх — в потолок (Z = 0), висит вниз
    else:
        shift = (-cx, -cy, -lo[2])             # низ по центру на полу
    obj.data.transform(Matrix.Translation(Vector(shift)))
    obj.data.update()
    lo, hi = bbox(obj)
    return tuple(float(x) for x in (hi - lo)), k, mount


def decimate(obj, limit, planar=False):
    t0 = tris(obj)
    if t0 <= limit:
        return t0
    if planar:                                  # плоское (стены): сначала убрать лишнее на ровных местах, UV не трогая
        md = obj.modifiers.new("plan", "DECIMATE")
        md.decimate_type = "DISSOLVE"
        md.angle_limit = math.radians(3)
        md.delimit = {"UV", "SEAM", "MATERIAL"}
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=md.name)
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.triangulate(bm, faces=bm.faces)
        bm.to_mesh(obj.data)
        bm.free()
    for _ in range(4):                          # Collapse иногда недотягивает — пара повторов
        t = tris(obj)
        if t <= limit:
            break
        md = obj.modifiers.new("dec", "DECIMATE")
        md.decimate_type = "COLLAPSE"
        md.ratio = max(0.001, limit / t * 0.98)
        md.use_collapse_triangulate = True
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=md.name)
    return tris(obj)


# ───────────────────────── текстуры и материалы ─────────────────────────

def _upstream_image(sock):
    """Картинка, от которой идёт вход (через промежуточные узлы)."""
    seen, stack = set(), [sock]
    while stack:
        s = stack.pop()
        for lk in s.links:
            n = lk.from_node
            if n in seen:
                continue
            seen.add(n)
            if n.type == "TEX_IMAGE" and n.image:
                return n.image
            stack += [i for i in n.inputs if i.is_linked]
    return None


def _pixels(img):
    a = np.empty(len(img.pixels), dtype=np.float32)
    img.pixels.foreach_get(a)
    return a.reshape(img.size[1], img.size[0], img.channels)


def _set_pixels(img, a):
    img.pixels.foreach_set(a.ravel())
    img.update()
    img.pack()


def color_filter(a, cfg):
    """Насыщенность / контраст / яркость / тёплый-холодный сдвиг по tripo/color.json (значения 1.0 — без изменений)."""
    rgb = a[..., :3]
    lum = (rgb * np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)).sum(-1, keepdims=True)
    rgb = lum + (rgb - lum) * cfg.get("saturation", 1.0)
    rgb = (rgb - 0.5) * cfg.get("contrast", 1.0) + 0.5
    rgb = rgb * cfg.get("brightness", 1.0)
    w = cfg.get("warmth", 0.0)
    rgb = rgb + np.array([w, w * 0.3, -w], dtype=np.float32)
    a[..., :3] = np.clip(rgb, 0, 1)
    return a


def fix_materials(obj, tex_max, color_cfg=None):
    """Без блеска (металличность 0, шероховатость ≥ 0,7), текстуры ≤ tex_max, цветовой фильтр (если дан).
    Возвращает сведения для отчёта."""
    info, done_imgs = [], set()
    for mat in obj.data.materials:
        if not mat or not mat.node_tree:
            continue
        nt = mat.node_tree
        for b in [n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"]:
            met = b.inputs["Metallic"]
            for lk in list(met.links):
                nt.links.remove(lk)
            met.default_value = 0.0
            rough = b.inputs["Roughness"]
            rimg = _upstream_image(rough) if rough.is_linked else None
            if rimg is not None and rimg.name not in done_imgs:
                a = _pixels(rimg)
                if a.shape[2] >= 3:
                    a[..., 1] = np.maximum(a[..., 1], ROUGH_MIN)   # glTF: G — шероховатость, B — металличность
                    a[..., 2] = 0.0
                _set_pixels(rimg, a)
                done_imgs.add(rimg.name)
            elif not rough.is_linked:
                rough.default_value = max(rough.default_value, ROUGH_MIN)
            if color_cfg:
                cimg = _upstream_image(b.inputs["Base Color"])
                if cimg is not None and cimg.name not in done_imgs:
                    _set_pixels(cimg, color_filter(_pixels(cimg), color_cfg))
                    done_imgs.add(cimg.name)
            for inp in ("Specular IOR Level", "Coat Weight", "Sheen Weight"):
                if inp in b.inputs and not b.inputs[inp].is_linked:
                    b.inputs[inp].default_value = 0.0 if inp != "Specular IOR Level" else 0.3
    for img in bpy.data.images:
        if img.size[0] == 0:
            continue
        w, h = img.size
        if max(w, h) > tex_max:
            k = tex_max / max(w, h)
            img.scale(max(1, round(w * k)), max(1, round(h * k)))
            img.pack()
            info.append(f"{img.name}: {w}→{img.size[0]}")
    return info


# ───────────────────────── экспорт ─────────────────────────

def export(obj, path):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    for q in (85, 70, 55):
        bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True,
                                  export_yup=True, export_animations=False, export_image_format="JPEG",
                                  export_jpeg_quality=q)
        mb = os.path.getsize(path) / 1e6
        if mb <= MAX_MB:
            break
    return mb, q


# ───────────────────────── превью со светом ─────────────────────────

def render_views(obj, out_base, px=360, res=None, fit=1.35):
    """Два кадра со светом: спереди и в три четверти. Тёмный фон, тёмно-синий общий свет, тёплая лампа сверху-сбоку."""
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 48
    try:
        sc.cycles.use_denoising, sc.cycles.denoiser = True, "OPENIMAGEDENOISE"
    except Exception:
        sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y = res or (px, px)
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "AgX"
    if sc.world is None:
        sc.world = bpy.data.worlds.new("w")
    sc.world.color = (0.03, 0.035, 0.06)
    lo, hi = bbox(obj)
    c = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))
    size = float(max(hi - lo))
    added = []
    fm = bpy.data.meshes.new("_floor")
    z0 = float(lo[2])
    fm.from_pydata([(-500, -500, z0), (500, -500, z0), (500, 500, z0), (-500, 500, z0)], [], [(0, 1, 2, 3)])
    mat = bpy.data.materials.new("_floor")
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.035, 0.035, 0.04, 1)
    fm.materials.append(mat)
    fo = bpy.data.objects.new("_floor", fm)
    sc.collection.objects.link(fo)
    added.append(fo)
    lamp = bpy.data.lights.new("_lamp", "POINT")
    lamp.energy, lamp.shadow_soft_size, lamp.color = 280.0 * size * size + 50, 0.2 * size, (1.0, 0.72, 0.45)
    lo_ = bpy.data.objects.new("_lamp", lamp)
    lo_.location = c + Vector((-0.7 * size, -1.0 * size, 1.1 * size))
    sc.collection.objects.link(lo_)
    added.append(lo_)
    fill = bpy.data.lights.new("_fill", "AREA")
    fill.energy, fill.size, fill.color = 40.0 * size * size + 10, 2.0 * size, (0.5, 0.6, 1.0)
    fl = bpy.data.objects.new("_fill", fill)
    fl.location = c + Vector((1.2 * size, -1.2 * size, 0.6 * size))
    fl.rotation_euler = (math.radians(70), 0, math.radians(45))
    sc.collection.objects.link(fl)
    added.append(fl)
    cam_d = bpy.data.cameras.new("_cam")
    cam_d.type = "ORTHO"
    cam = bpy.data.objects.new("_cam", cam_d)
    sc.collection.objects.link(cam)
    sc.camera = cam
    added.append(cam)
    outs = []
    for tag, yaw, pitch in (("front", 0.0, 12.0), ("34", -35.0, 22.0)):
        d = Matrix.Rotation(math.radians(yaw), 3, "Z") @ Matrix.Rotation(math.radians(-pitch), 3, "X") @ Vector((0, -1, 0))
        cam.location = c + d * (size * 4)          # d — от предмета к камере
        cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        cam_d.ortho_scale = size * fit
        cam_d.clip_end = size * 20
        sc.render.filepath = f"{out_base}_{tag}.png"
        bpy.ops.render.render(write_still=True)
        outs.append(sc.render.filepath)
    for o in added:
        bpy.data.objects.remove(o)
    return outs


def sheet(rows, out):
    """rows: [(подпись, [картинки…])] → один лист."""
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 15)
        small = ImageFont.truetype("DejaVuSans.ttf", 13)
    except OSError:
        font = small = ImageFont.load_default()
    PAD, TH = 14, 44
    ims = [[Image.open(p).convert("RGB") for p in ps] for _, ps in rows]
    W = max(sum(i.width for i in r) + PAD * (len(r) + 1) for r in ims)
    H = sum(max(i.height for i in r) + TH + PAD for r in ims) + PAD
    s = Image.new("RGB", (W, H), (24, 25, 30))
    d = ImageDraw.Draw(s)
    y = PAD
    for (cap, _), r in zip(rows, ims):
        title, sub = (cap.split("\n", 1) + [""])[:2]
        d.text((PAD, y), title, font=font, fill=(240, 240, 240))
        d.text((PAD, y + 20), sub, font=small, fill=(170, 170, 175))
        x = PAD
        for im in r:
            s.paste(im, (x, y + TH))
            x += im.width + PAD
        y += max(i.height for i in r) + TH + PAD
    os.makedirs(os.path.dirname(out), exist_ok=True)
    s.save(out)
    return out


# ───────────────────────── отчёт ─────────────────────────

def write_report(entries):
    data_p = os.path.join(ROOT, "docs", "tripo_report.json")
    data = json.load(open(data_p)) if os.path.exists(data_p) else {}
    data.update(entries)
    json.dump(data, open(data_p, "w"), ensure_ascii=False, indent=1)
    L = ["# Отчёт обработки моделей из Tripo", "",
         "Делает `tools/tripo_process.py` (правила — `docs/TRIPO.md`, раздел 2). Данные — `docs/tripo_report.json`.", "",
         "| Модель (export/) | Файл из tripo/ | Треугольники до → после (лимит) | Размер Ш × Г × В, см | ОС Ш × В, см | "
         "Масштаб | Поворот | Крепление | Текстуры | Файл, МБ | Предупреждения |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    import re
    for k in sorted(data):
        e = data[k]
        sizes = re.findall(r": (\d+→\d+)", e["textures"])
        tx = f"{len(sizes)} шт. {sizes[0]}" if sizes else e["textures"]
        w = "<br>".join("⚠ " + x for x in e["warnings"]) or "—"
        L.append(f"| `{k}` | `{e['src']}` | {e['tris_before']:,} → {e['tris_after']:,} ({e['limit']:,}) | "
                 f"{e['size_cm'][0]:.0f} × {e['size_cm'][1]:.0f} × {e['size_cm'][2]:.0f} | "
                 f"{e['os_cm'][0]} × {e['os_cm'][1]} | ×{e['scale']:.3g} | {e['rotate']}° | {e['mount']} | "
                 f"{tx} | {e['mb']:.2f} | {w} |".replace(",", " "))
    open(os.path.join(ROOT, "docs", "TRIPO_REPORT.md"), "w").write("\n".join(L) + "\n")


def add_deviation(name, w_cm, os_w):
    p = os.path.join(ROOT, "docs", "DEVIATIONS.md")
    s = open(p).read()
    head = "\n## Модели из Tripo: ширина отличается от ОС больше чем на 15 %\n\n| Модель | ОС Ш, см | Модель Ш, см |\n|---|---|---|\n"
    if head not in s:
        s = s.rstrip("\n") + "\n" + head
    line = f"| `{name}` | {os_w} | {w_cm:.0f} |"
    lines = [x for x in s.split("\n") if not x.startswith(f"| `{name}` |")]
    s = "\n".join(lines).rstrip("\n") + "\n" + line + "\n"
    open(p, "w").write(s)


# ───────────────────────── главное ─────────────────────────

SRC = os.path.join(ROOT, "tripo")


def load_json(name, default):
    p = os.path.join(SRC, name)
    return json.load(open(p)) if os.path.exists(p) else default


def process(path, plan, out_dir, rot_cfg, color_cfg, prev_dir):
    stem = os.path.basename(path)[:-4]
    oid, var, warns = resolve(stem, plan)
    if oid is None:
        print(f"[{stem}] ⚠ {warns[0]}")
        return None, None
    o = plan[oid]
    name = f"{oid}_{var}_idle"
    cls = size_class(o)
    obj, n_parts = import_joined(path)
    t0 = tris(obj)
    rot = rot_cfg.get(stem, rot_cfg.get(oid, 0))
    (w, d, h), k, mount = place(obj, o, rot)
    warns += check_mesh(obj)
    if n_parts > 1:
        warns.append(f"в файле {n_parts} отдельных объектов — склеены в один")
    if abs(w * 100 - o["size"][0]) > WIDTH_TOL * o["size"][0]:
        warns.append(f"ширина {w * 100:.0f} см, в ОС {o['size'][0]} см (> 15 %) — записано в DEVIATIONS.md")
    t1 = decimate(obj, LIMITS[cls])
    smooth_by_angle(obj)
    if t1 > LIMITS[cls]:
        warns.append(f"не удалось облегчить до лимита: {t1}")
    tex = fix_materials(obj, TEX[cls], color_cfg if color_cfg.get("approved") else None)
    if not obj.data.materials or not any(m and m.node_tree for m in obj.data.materials):
        warns.append("нет материала/текстуры")
    os.makedirs(out_dir, exist_ok=True)
    mb, q = export(obj, os.path.join(out_dir, name + ".glb"))
    if mb > MAX_MB:
        warns.append(f"файл {mb:.1f} МБ > {MAX_MB} МБ")
    views = render_views(obj, os.path.join(prev_dir, name))
    e = {"src": stem + ".glb", "tris_before": t0, "tris_after": t1, "limit": LIMITS[cls], "class": cls,
         "size_cm": [w * 100, d * 100, h * 100], "os_cm": o["size"], "scale": k, "rotate": rot, "mount": mount,
         "textures": ", ".join(tex) or "≤ лимита", "mb": mb, "jpeg_q": q, "warnings": warns,
         "date": datetime.date.today().isoformat()}
    print(f"[{name}] треугольников {t0} → {t1} (лимит {LIMITS[cls]}), {w * 100:.0f}×{d * 100:.0f}×{h * 100:.0f} см, "
          f"{mb:.2f} МБ" + "".join(f"\n  ⚠ {x}" for x in warns))
    cap = (f"{name}\n{t0:,} → {t1:,} треуг. · {w * 100:.0f}×{d * 100:.0f}×{h * 100:.0f} см · поворот {rot}° · "
           f"{mb:.2f} МБ" + (" · ⚠ " + str(len(warns)) if warns else "")).replace(",", " ")
    return (name, e), (cap, views)


# ───────────────────────── куски стен комнат (docs/TRIPO.md, раздел 5) ─────────────────────────
WALL_H, WALL_D, WALL_TRIS, WALL_CUT = 3.0, 0.30, 4000, 0.012


def clear_custom_normals(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    try:
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
    except Exception:
        pass


def wall_rotation(obj):
    """Плоскость стены — вдоль X, перед (трубы, выступы) — к −Y, ровная спина — к +Y. Возвращает градусы."""
    lo, hi = bbox(obj)
    rot = 0
    if hi[0] - lo[0] < hi[1] - lo[1]:             # стена стоит «вдоль Y» — перед смотрит вбок
        rot = 90
        obj.data.transform(Matrix.Rotation(math.radians(90), 4, "Z"))
    co = np.empty(len(obj.data.vertices) * 3)
    obj.data.vertices.foreach_get("co", co)
    y = co.reshape(-1, 3)[:, 1]
    band = 0.02 * (y.max() - y.min())
    near_max, near_min = (y > y.max() - band).sum(), (y < y.min() + band).sum()
    if near_min > near_max:                       # ровная спина (много вершин в одной плоскости) оказалась спереди
        rot += 180
        obj.data.transform(Matrix.Rotation(math.radians(180), 4, "Z"))
    return rot


def remove_back(obj):
    """Убрать заднюю сторону стены (смотрит в +Y, к земле — в игре её не видно): иначе при облегчении перед и спина
    тонкой стены слипаются и кусок разваливается на «осколки»."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.normal_update()
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.normal.y > 0.3], context="FACES")
    bm.to_mesh(obj.data)
    bm.free()


def cut_flat(obj, inset):
    """Обрезать края ровно: левый, правый, низ, верх — плоскостью, на inset (доля размера) внутрь."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    lo, hi = bbox(obj)
    d = (hi - lo) * inset
    for co, no in (((lo[0] + d[0], 0, 0), (-1, 0, 0)), ((hi[0] - d[0], 0, 0), (1, 0, 0)),
                   ((0, 0, lo[2] + d[2] * 0.5), (0, 0, -1)), ((0, 0, hi[2] - d[2] * 0.5), (0, 0, 1))):
        geom = list(bm.verts) + list(bm.edges) + list(bm.faces)
        bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=no, clear_outer=True)
    bm.to_mesh(obj.data)
    bm.free()


def process_wall(path, out_dir, rot_cfg, prev_dir):
    stem = os.path.basename(path)[:-4]
    name = stem + "_idle"
    warns = []
    obj, n_parts = import_joined(path)
    t0 = tris(obj)
    clear_custom_normals(obj)
    if stem in rot_cfg:
        rot = rot_cfg[stem]
        obj.data.transform(Matrix.Rotation(math.radians(rot), 4, "Z"))
    else:
        rot = wall_rotation(obj)
    remove_back(obj)
    cut_flat(obj, WALL_CUT)
    lo, hi = bbox(obj)
    k = WALL_H / float(hi[2] - lo[2])                   # пропорции ширина : высота — как у модели
    obj.data.transform(Matrix.Scale(k, 4))
    lo, hi = bbox(obj)
    ky = WALL_D / float(hi[1] - lo[1])                  # толщина — ровно 0,3 м (трубы спереди «сплющиваются» вглубь)
    obj.data.transform(Matrix.Diagonal((1, ky, 1, 1)))
    lo, hi = bbox(obj)
    obj.data.transform(Matrix.Translation(Vector((-lo[0], -hi[1], -lo[2]))))   # левый край X = 0, спина Y = 0, низ Z = 0
    obj.data.update()
    lo, hi = bbox(obj)
    w, d, h = (float(x) for x in hi - lo)
    if n_parts > 1:
        warns.append(f"в файле {n_parts} отдельных объектов — склеены в один")
    t1 = decimate(obj, WALL_TRIS)
    smooth_by_angle(obj)
    if t1 > WALL_TRIS:
        warns.append(f"не удалось облегчить до лимита: {t1}")
    tex = fix_materials(obj, 1024)
    os.makedirs(out_dir, exist_ok=True)
    mb, q = export(obj, os.path.join(out_dir, name + ".glb"))
    if mb > MAX_MB:
        warns.append(f"файл {mb:.1f} МБ > {MAX_MB} МБ")
    e = {"src": stem + ".glb", "tris_before": t0, "tris_after": t1, "limit": WALL_TRIS, "class": "wall",
         "size_cm": [w * 100, d * 100, h * 100], "os_cm": ["—", 300], "scale": k, "rotate": rot, "mount": "стена комнаты",
         "textures": ", ".join(tex) or "≤ лимита", "mb": mb, "jpeg_q": q, "warnings": warns,
         "date": datetime.date.today().isoformat()}
    print(f"[{name}] треугольников {t0} → {t1} (лимит {WALL_TRIS}), {w * 100:.0f}×{d * 100:.0f}×{h * 100:.0f} см, "
          f"поворот {rot}°, {mb:.2f} МБ" + "".join(f"\n  ⚠ {x}" for x in warns))
    return name, e


def wall_row(names, out_dir, out_png, order=None):
    """Куски стены подряд (по порядку order) со светом, спереди и в три четверти — проверить стыки."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    order = order or names
    x = 0.0
    objs = []
    for n in order:
        bpy.ops.import_scene.gltf(filepath=os.path.join(out_dir, n + ".glb"))
        new = [o for o in bpy.context.selected_objects if o.type == "MESH"]
        for o in new:
            o.location.x += x
        lo, hi = None, None
        bpy.context.view_layer.update()
        xs = [(o.matrix_world @ Vector(c)).x for o in new for c in o.bound_box]
        x = max(xs)
        objs += new
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    for o in list(bpy.context.scene.objects):
        if o.type != "MESH":
            bpy.data.objects.remove(o)
    bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    views = render_views(obj, out_png[:-4], res=(1800, 520), fit=1.04)
    return views


def color_test(names, plan, src, prev_dir):
    """Лист «до / после» цветового фильтра на нескольких моделях — без экспорта."""
    cfg = load_json("color.json", {})
    rows = []
    for stem in names:
        path = os.path.join(src, stem + ".glb")
        oid, var, _ = resolve(stem, plan)
        if oid is None:
            print("нет в плане:", stem)
            continue
        views = []
        for tag, c in (("before", None), ("after", cfg)):
            obj, _ = import_joined(path)
            place(obj, plan[oid], load_json("rotate.json", {}).get(stem, 0))
            fix_materials(obj, 1024, c)
            views.append(render_views(obj, os.path.join(prev_dir, f"color_{stem}_{tag}"))[1])
        desc = ", ".join(f"{k} {v}" for k, v in cfg.items() if k != "approved")
        rows.append((f"{stem}\nслева — как из Tripo, справа — с фильтром ({desc})", views))
    out = os.path.join(ROOT, "renders", "_review", f"tripo_color_{datetime.date.today().isoformat()}.png")
    print("лист цвета:", sheet(rows, out))


def main(argv):
    force = "--force" in argv
    no_docs = "--no-docs" in argv
    src, out_dir = os.path.join(ROOT, "tripo"), os.path.join(ROOT, "export")
    args, i = [], 0
    while i < len(argv):
        a = argv[i]
        if a in ("--src", "--out"):
            v = os.path.abspath(argv[i + 1])
            src, out_dir = (v, out_dir) if a == "--src" else (src, v)
            i += 2
            continue
        if not a.startswith("--"):
            args.append(a)
        i += 1
    global SRC
    SRC = src
    plan = load_plan()
    prev_dir = os.path.join(ROOT, "renders", "_review", "tripo_views")
    os.makedirs(prev_dir, exist_ok=True)
    if "--color-test" in argv:
        color_test(args, plan, src, prev_dir)
        return
    files = sorted(f for f in os.listdir(src) if f.lower().endswith(".glb"))
    if args:
        files = [f for f in files if f[:-4] in args]
    rot_cfg, color_cfg = load_json("rotate.json", {}), load_json("color.json", {})
    entries, rows = {}, []
    walls = []
    for f in files:
        stem = f[:-4]
        if stem.startswith("room_") and "_wall_" in stem:          # кусок стены комнаты — отдельные правила
            if not force and os.path.exists(os.path.join(out_dir, stem + "_idle.glb")):
                print(f"[{stem}] уже есть в export/ — пропуск (--force — заново)")
                continue
            n, e = process_wall(os.path.join(src, f), out_dir, rot_cfg, prev_dir)
            entries[n] = e
            walls.append(n)
            continue
        oid, var, _ = resolve(stem, plan)
        if oid and not force and os.path.exists(os.path.join(out_dir, f"{oid}_{var}_idle.glb")):
            print(f"[{stem}] уже есть в export/ — пропуск (--force — заново)")
            continue
        r, row = process(os.path.join(src, f), plan, out_dir, rot_cfg, color_cfg, prev_dir)
        if r:
            entries[r[0]] = r[1]
            rows.append(row)
    if walls:                                                       # стыки: куски подряд, вперемешку, 2 круга
        sets = {}
        for n in walls:
            sets.setdefault(n.split("_wall_")[0], []).append(n)
        for setname, ns in sets.items():
            order = sorted(ns) * 2 if len(ns) < 4 else sorted(ns) + sorted(ns)[:2]   # вперемешку, 2 круга
            png = os.path.join(prev_dir, f"{setname}_row.png")
            v = wall_row(ns, out_dir, png, order)
            rows.append((f"{setname}: {len(order)} кусков подряд ({', '.join(x.split('_wall_')[1][:-5] for x in order)})\n"
                         f"сверху — спереди, как в игре; снизу — в три четверти. Смотреть стыки", [v[0]]))
            rows.append(("", [v[1]]))
    if not rows:
        print("нечего обрабатывать")
        return
    out = os.path.join(ROOT, "renders", "_review", f"tripo_{datetime.date.today().isoformat()}.png")
    print("лист превью:", sheet(rows, out))
    if not no_docs:
        for name, e in entries.items():
            if any("DEVIATIONS" in w for w in e["warnings"]):
                add_deviation(name, e["size_cm"][0], e["os_cm"][0])
        write_report(entries)
        print("отчёт: docs/TRIPO_REPORT.md")


if __name__ == "__main__":
    main(sys.argv[1:])
