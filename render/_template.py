"""Шаблон рендера для пути А (картинки в 2D) — см. README «Для пути А» и docs/IMAGES.md.

Запуск (из корня репозитория):
    python3 render/_template.py          # bpy как модуль Python (ставится сам при старте сессии)
    blender -b -P render/_template.py    # или обычный Blender

Что делает:
  1. Собирает сцену-шаблон: ортографическая камера, наклон сверху 12°, 200 px на метр,
     цвет Standard, прозрачный фон, без света. Сохраняет render/_template.blend.
  2. Рендерит проверочный куб 1×1×1 м: renders/_test/test_cube_1m_idle.png и …_n.png.

Модели подключают его так:
    import sys; sys.path.insert(0, "render"); import _template as rt
    rt.setup_scene()
    ... строим модель ...
    rt.render_pair([obj, ...], "renders/furniture/bed_single_zheleznaya_koyka_idle")
"""
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector

TILT_DEG = 12.0          # наклон камеры сверху
PX_PER_M = 200           # рендер вдвое крупнее игры (в игре 100 px на метр)
# Вертикаль растягиваем на 1/cos 12° (≈ +2,2 %): из-за наклона камеры вертикальные грани
# сжимаются, а в игре по вертикали точная сетка (этаж = 3 м + 1 м = 400 px).
# С растяжкой: 1 м по вертикали = ровно 200 px, глубина 1 м поднимает картинку на tan 12° ≈ 21 см.
V_STRETCH = 1.0 / math.cos(math.radians(TILT_DEG))
CAMERA_NAME = "RenderCamera"
NORMAL_MAT_NAME = "_override_normal"

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def camera_rotation():
    """Камера смотрит вдоль +Y и опущена на 12° вниз."""
    return Matrix.Rotation(math.radians(90.0 - TILT_DEG), 4, "X")


def setup_scene():
    """Пустая сцена с камерой и настройками рендера. Возвращает сцену."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene

    cam_data = bpy.data.cameras.new(CAMERA_NAME)
    cam_data.type = "ORTHO"
    cam_data.clip_start = 0.01
    cam_data.clip_end = 1000.0
    cam = bpy.data.objects.new(CAMERA_NAME, cam_data)
    scene.collection.objects.link(cam)
    cam.matrix_world = camera_rotation()
    scene.camera = cam

    r = scene.render
    r.engine = "CYCLES"
    r.film_transparent = True
    r.resolution_percentage = 100
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGBA"
    r.image_settings.color_depth = "8"
    r.dither_intensity = 0.0

    c = scene.cycles
    c.device = "CPU"
    c.samples = 16           # только для сглаживания краёв, шума нет — всё через Emission
    c.use_denoising = False
    c.max_bounces = 0        # никакого отражённого света
    c.use_adaptive_sampling = False

    # Мир чёрный — света нет вообще.
    world = bpy.data.worlds.new("NoLight")
    world.color = (0, 0, 0)
    scene.world = world

    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0
    scene.sequencer_colorspace_settings.name = "sRGB"
    return scene


def _mesh_points_world(objs):
    deps = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in objs:
        if o.type != "MESH":
            continue
        ev = o.evaluated_get(deps)
        mw = ev.matrix_world
        pts += [mw @ v.co for v in ev.data.vertices]
    return pts


def frame_objects(objs, margin_px=0, frame_points=None):
    """Ставит камеру и размер картинки по контуру объектов: 200 px на метр,
    низ картинки = самая нижняя точка, без пустых полей. Возвращает (ширина, высота) в px.
    frame_points — точки (мир), задающие кадр точно (для бесшовных оболочек: модель чуть больше кадра,
    чтобы края были сплошные)."""
    scene = bpy.context.scene
    cam = scene.camera
    rot = camera_rotation()
    inv = rot.to_3x3().transposed()
    pts_all = [inv @ p for p in _mesh_points_world(objs)]
    pts = [inv @ Vector(p) for p in frame_points] if frame_points else pts_all
    if not pts:
        raise ValueError("Нечего рендерить: нет мешей")
    xmin = min(p.x for p in pts); xmax = max(p.x for p in pts)
    ymin = min(p.y for p in pts); ymax = max(p.y for p in pts)
    zmax = max(p.z for p in pts_all)

    m = margin_px / PX_PER_M
    k = V_STRETCH
    # ceil с допуском 0,05 px: 1 м ровно = 200 px, а не 201 из-за погрешности
    w_px = max(1, math.ceil((xmax - xmin + 2 * m) * PX_PER_M - 0.05))
    h_px = max(1, math.ceil(((ymax - ymin) * k + 2 * m) * PX_PER_M - 0.05))
    # метров камеры на пиксель: по ширине 1/200, по высоте 1/(200·k)
    w_cam, h_cam = w_px / PX_PER_M, h_px / (PX_PER_M * k)

    # центр по ширине — середина контура; по высоте — низ картинки ровно по нижней точке
    cx = (xmin + xmax) / 2
    cy = ymin - m / k + h_cam / 2
    cam.matrix_world = Matrix.Translation(rot.to_3x3() @ Vector((cx, cy, zmax + 10.0))) @ rot
    # Пиксель «шире» в k раз — так Blender растягивает картинку по вертикали, геометрию не трогая
    scene.render.pixel_aspect_x = k
    scene.render.pixel_aspect_y = 1.0
    cam.data.sensor_fit = "AUTO"
    cam.data.ortho_scale = max(w_px * k, h_px) / (PX_PER_M * k)
    scene.render.resolution_x = w_px
    scene.render.resolution_y = h_px
    return w_px, h_px


def _flat_color_materials():
    """Временная подмена всех материалов на «чистый цвет» (Emission того же цвета, что Base Color).
    Возвращает функцию, которая всё вернёт обратно."""
    undo = []
    for mat in bpy.data.materials:
        if not mat.use_nodes or mat.name == NORMAL_MAT_NAME:
            continue
        nt = mat.node_tree
        out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL" and n.is_active_output), None)
        if out is None or not out.inputs["Surface"].is_linked:
            continue
        old_link = out.inputs["Surface"].links[0]
        old_from = old_link.from_socket
        src = old_from.node
        if src.type == "EMISSION":
            continue  # светящееся уже «чистое»
        emi = nt.nodes.new("ShaderNodeEmission")
        emi.inputs["Strength"].default_value = 1.0
        base = src.inputs.get("Base Color") or src.inputs.get("Color")
        if base is not None and base.is_linked:
            nt.links.new(base.links[0].from_socket, emi.inputs["Color"])
        elif base is not None:
            emi.inputs["Color"].default_value = base.default_value
        nt.links.remove(old_link)
        nt.links.new(emi.outputs["Emission"], out.inputs["Surface"])
        undo.append((nt, emi, old_from, out))

    def restore():
        for nt, emi, old_from, out in undo:
            nt.nodes.remove(emi)
            nt.links.new(old_from, out.inputs["Surface"])
    return restore


def normal_material():
    """Материал-замена для карты нормалей: нормаль в пространстве камеры × 0,5 + 0,5.
    R — вправо, G — вверх, B — на камеру (формат OpenGL). Стена лицом к камере = (128, 128, 255)."""
    mat = bpy.data.materials.get(NORMAL_MAT_NAME)
    if mat:
        return mat
    mat = bpy.data.materials.new(NORMAL_MAT_NAME)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    vt = nt.nodes.new("ShaderNodeVectorTransform")
    vt.vector_type = "NORMAL"
    vt.convert_from = "WORLD"
    vt.convert_to = "CAMERA"
    # В Cycles ось Z камеры смотрит ОТ камеры — переворачиваем, чтобы B было «на камеру»
    fix = nt.nodes.new("ShaderNodeVectorMath"); fix.operation = "MULTIPLY"
    fix.inputs[1].default_value = (1.0, 1.0, -1.0)
    mad = nt.nodes.new("ShaderNodeVectorMath"); mad.operation = "MULTIPLY_ADD"
    mad.inputs[1].default_value = (0.5, 0.5, 0.5)
    mad.inputs[2].default_value = (0.5, 0.5, 0.5)
    emi = nt.nodes.new("ShaderNodeEmission")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(geo.outputs["Normal"], vt.inputs["Vector"])
    nt.links.new(vt.outputs["Vector"], fix.inputs[0])
    nt.links.new(fix.outputs["Vector"], mad.inputs[0])
    nt.links.new(mad.outputs["Vector"], emi.inputs["Color"])
    nt.links.new(emi.outputs["Emission"], out.inputs["Surface"])
    return mat


def render_pair(objs, out_base, margin_px=0, frame_points=None):
    """Рендерит <out_base>.png (цвет) и <out_base>_n.png (нормали), одного размера.
    out_base — путь без .png, от корня репозитория."""
    scene = bpy.context.scene
    size = frame_objects(objs, margin_px, frame_points)
    out_base = os.path.join(ROOT, out_base)
    os.makedirs(os.path.dirname(out_base), exist_ok=True)

    # 1) цвет: чистые цвета палитры, Standard
    restore = _flat_color_materials()
    scene.view_settings.view_transform = "Standard"
    scene.render.filepath = out_base + ".png"
    bpy.ops.render.render(write_still=True)
    restore()

    # 2) нормали: материал-замена, без цветокоррекции (Raw)
    vl = bpy.context.view_layer
    vl.material_override = normal_material()
    scene.view_settings.view_transform = "Raw"
    scene.render.filepath = out_base + "_n.png"
    bpy.ops.render.render(write_still=True)
    vl.material_override = None
    scene.view_settings.view_transform = "Standard"
    return size


def render_lit(objs, out_path, margin_px=24, lamp_xyz=None, glow_strength=2.5, samples=96):
    """Показательный рендер СО СВЕТОМ (как на референсе): тёплая лампа сверху-спереди, холодная слабая
    подсветка, мягкие тени. ТОЛЬКО для просмотра — в игру идёт render_pair (без света)."""
    scene = bpy.context.scene
    frame_objects(objs, margin_px)
    pts = _mesh_points_world(objs)
    top = max(p.z for p in pts)
    cx = (min(p.x for p in pts) + max(p.x for p in pts)) / 2
    added = []
    # тёплая лампа над предметом и чуть спереди — свет сверху вниз, как от потолочной лампы
    lamp = bpy.data.lights.new("_lamp", "POINT")
    lamp.energy, lamp.shadow_soft_size, lamp.color = 90.0 + 60.0 * top, 0.15, (1.0, 0.72, 0.42)
    o = bpy.data.objects.new("_lamp", lamp)
    o.location = lamp_xyz or (cx - 0.2, -0.9, top + 0.55)
    scene.collection.objects.link(o)
    added.append(o)
    fill = bpy.data.lights.new("_fill", "AREA")
    fill.energy, fill.size, fill.color = 18.0, 3.0, (0.45, 0.55, 0.9)
    o = bpy.data.objects.new("_fill", fill)
    o.location = (-2.0, -3.0, 1.2)
    o.rotation_euler = (math.radians(80), 0, math.radians(-35))
    scene.collection.objects.link(o)
    added.append(o)
    old_world = tuple(scene.world.color)
    scene.world.color = (0.012, 0.013, 0.02)
    c = scene.cycles
    old = (c.samples, c.max_bounces, c.use_denoising)
    c.samples, c.max_bounces = samples, 4
    try:
        c.use_denoising = True
        c.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        c.use_denoising = False
    glows = []
    for mat in bpy.data.materials:
        if mat.node_tree:
            for n in mat.node_tree.nodes:
                if n.type == "EMISSION" and mat.name != NORMAL_MAT_NAME:
                    glows.append((n, n.inputs["Strength"].default_value))
                    n.inputs["Strength"].default_value = glow_strength
    scene.view_settings.view_transform = "AgX"
    scene.render.filepath = os.path.join(ROOT, out_path)
    bpy.ops.render.render(write_still=True)
    for n, s in glows:
        n.inputs["Strength"].default_value = s
    scene.view_settings.view_transform = "Standard"
    c.samples, c.max_bounces, c.use_denoising = old
    scene.world.color = old_world
    for o in added:
        bpy.data.objects.remove(o)


def palette_material():
    """Общий материал моделей: текстура palette/palette.png без сглаживания (каждый квадрат — свой цвет)."""
    mat = bpy.data.materials.get("palette")
    if mat:
        return mat
    mat = bpy.data.materials.new("palette")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 1.0
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.interpolation = "Closest"
    tex.image = bpy.data.images.load(os.path.join(ROOT, "palette", "palette.png"), check_existing=True)
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    return mat


def color_uv(name):
    """UV-центр цвета палитры по имени: color_uv("rust"). Цвета — palette/palette.md."""
    sys.path.insert(0, os.path.join(ROOT, "palette"))
    import _palette
    return _palette.uv(name)


def paint(obj, name, faces=None):
    """Красит грани меша (все или список индексов) цветом палитры по имени."""
    me = obj.data
    if me.uv_layers.active is None:
        me.uv_layers.new(name="UVMap")
    uv_layer = me.uv_layers.active.data
    u, v = color_uv(name)
    polys = me.polygons if faces is None else [me.polygons[i] for i in faces]
    for poly in polys:
        for li in poly.loop_indices:
            uv_layer[li].uv = (u, v)


def _test_cube():
    """Проверочный куб 1×1×1 м, origin внизу по центру, плоское затенение, один цвет."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    cube = bpy.context.active_object
    cube.name = "test_cube_1m"
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.object.shade_flat()
    mat = bpy.data.materials.new("test_grey")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
    cube.data.materials.append(mat)
    return cube


def main():
    setup_scene()
    blend = os.path.join(ROOT, "render", "_template.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend)

    cube = _test_cube()
    w, h = render_pair([cube], "renders/_test/test_cube_1m_idle")
    print(f"Проверочный куб: {w}×{h} px (ожидается 200×{math.ceil((1 + math.tan(math.radians(TILT_DEG))) * PX_PER_M)}: перед 200 + верх 43)")
    print("Шаблон сохранён:", blend)


if __name__ == "__main__":
    # Под `blender -b -P` аргументы после `--`; под python3 их нет.
    main()
