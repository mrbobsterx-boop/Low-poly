"""Рендер СО СВЕТОМ, как в игре (docs/QUALITY.md, «Как проверять»): тёмный фон, тёмно-синий общий свет,
одна тёплая лампа сверху-сбоку, мягкие тени и AO; пол и стена за предметом — чтобы было как в комнате.
Смотреть модели — только так (плоская картинка без света всегда выглядит «пластилином»).

1) Рендер моделей из скрипта (все варианты или только названные):
     python3 render/_lit_preview.py <папка> models/furniture/bed_single.py [zheleznaya_koyka ...]
   → <папка>/<имя>.png (200 px на метр) и <папка>/<имя>_game.png (игровой размер: 100 px на метр).
   Скрипт модели выполняется как обычно, но finish() только собирает модель (L.PREVIEW): без экспорта и рендера.

2) Лист «до / после»:
     python3 render/_lit_preview.py --compare <выход.png> <папка_до> <папка_после>
"""
import math
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

AMBIENT = (0.035, 0.042, 0.075)     # тёмно-синий общий свет (мир)
LAMP = (1.0, 0.70, 0.42)            # тёплая лампа
FLOOR = (0.030, 0.030, 0.034)       # тёмный серо-синий пол (как фон образцов)
WALL = (0.022, 0.023, 0.030)        # тёмная серо-синяя стена (как фон образцов docs/ref/style)
GAME_SCALE = 0.5                    # рендер 200 px/м → игра 100 px/м
MARGIN_PX = 40


def _diffuse(name, rgb):
    import bpy
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = 1.0
    return m


def _plane(name, verts, mat):
    import bpy
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], [(0, 1, 2, 3)])
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    return o


def render_lit(obj, out_path):
    """Один предмет: пол, стена сзади, свет; кадр — по предмету с полями."""
    import bpy
    sys.path.insert(0, HERE)
    import _template as rt
    scene = bpy.context.scene
    for o in scene.objects:
        if o.type == "MESH":
            o.hide_render = o is not obj
    vs = [obj.matrix_world @ v.co for v in obj.data.vertices]
    x0, x1 = min(v.x for v in vs), max(v.x for v in vs)
    y1 = max(v.y for v in vs)
    top = max(v.z for v in vs)
    size = max(x1 - x0, top, 0.3)
    added = [_plane("_floor", [(-20, -20, 0), (20, -20, 0), (20, 20, 0), (-20, 20, 0)], _diffuse("_floor", FLOOR)),
             _plane("_wall", [(-20, y1 + 0.02, -1), (20, y1 + 0.02, -1), (20, y1 + 0.02, 20), (-20, y1 + 0.02, 20)],
                    _diffuse("_wall", WALL))]
    lamp = bpy.data.lights.new("_lamp", "POINT")
    lamp.energy, lamp.shadow_soft_size, lamp.color = 120.0 * (0.6 + size) ** 2, 0.12, LAMP
    lo = bpy.data.objects.new("_lamp", lamp)
    lo.location = (x0 - 0.15 * size, -0.9 - 0.5 * size, top + 0.6 + 0.3 * size)    # сверху-сбоку (слева) и спереди
    scene.collection.objects.link(lo)
    added.append(lo)
    old_world = tuple(scene.world.color)
    scene.world.color = AMBIENT
    c = scene.cycles
    old = (c.samples, c.max_bounces, c.use_denoising)
    c.samples, c.max_bounces = 96, 4
    try:
        c.use_denoising, c.denoiser = True, "OPENIMAGEDENOISE"
    except Exception:
        c.use_denoising = False
    glows = []
    for mat in bpy.data.materials:
        if mat.node_tree:
            for n in mat.node_tree.nodes:
                if n.type == "EMISSION" and mat.name != rt.NORMAL_MAT_NAME:
                    glows.append((n, n.inputs["Strength"].default_value))
                    n.inputs["Strength"].default_value = 3.0
    rt.frame_objects([obj], MARGIN_PX)
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Punchy"
    scene.view_settings.exposure = 0.7
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    for n, s in glows:
        n.inputs["Strength"].default_value = s
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.0
    scene.render.film_transparent = True
    c.samples, c.max_bounces, c.use_denoising = old
    scene.world.color = old_world
    for o in added:
        bpy.data.objects.remove(o)
    from PIL import Image
    im = Image.open(out_path)
    im.resize((max(1, round(im.width * GAME_SCALE)), max(1, round(im.height * GAME_SCALE))), Image.LANCZOS) \
        .save(out_path[:-4] + "_game.png")


def run_script(outdir, script, variants):
    sys.path.insert(0, os.path.join(ROOT, "models"))
    import _lib as L
    L.PREVIEW = []
    L.save_blend = lambda *a, **k: None
    sys.path.insert(0, os.path.dirname(os.path.join(ROOT, script)))
    runpy.run_path(os.path.join(ROOT, script), run_name="__main__")
    os.makedirs(os.path.join(ROOT, outdir), exist_ok=True)
    for obj in L.PREVIEW:
        if variants and not any(f"_{v}_" in obj.name + "_" for v in variants):
            continue
        if getattr(L, "QUALITY", False):
            L.render_material(obj, True)
        out = os.path.join(ROOT, outdir, obj.name + ".png")
        render_lit(obj, out)
        print("со светом:", os.path.relpath(out, ROOT))


def compare(out, before, after):
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 16)
        small = ImageFont.truetype("DejaVuSans.ttf", 14)
    except OSError:
        font = small = ImageFont.load_default()
    names = sorted(f[:-4] for f in os.listdir(after) if f.endswith(".png") and not f.endswith("_game.png")
                   and os.path.exists(os.path.join(before, f)))
    PAD, TH, BG = 18, 24, (30, 31, 36)
    rows = []
    for n in names:
        ims = [(cap, Image.open(os.path.join(d, n + suf)).convert("RGB"))
               for cap, d, suf in (("до — со светом", before, ".png"), ("после — со светом", after, ".png"),
                                   ("до — в игре", before, "_game.png"), ("после — в игре", after, "_game.png"))]
        rows.append((n, ims))
    W = max(sum(im.width for _, im in ims) + PAD * (len(ims) + 1) for _, ims in rows)
    H = sum(max(im.height for _, im in ims) + TH * 2 + PAD for _, ims in rows) + PAD
    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)
    y = PAD
    for n, ims in rows:
        d.text((PAD, y), n, font=font, fill=(240, 240, 240))
        x, hm = PAD, max(im.height for _, im in ims)
        for cap, im in ims:
            d.text((x, y + TH), cap, font=small, fill=(175, 175, 175))
            sheet.paste(im, (x, y + TH * 2 + hm - im.height))
            x += im.width + PAD
        y += hm + TH * 2 + PAD
    sheet.save(out)
    print("лист до/после:", out)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--compare":
        compare(*a[1:4])
    else:
        run_script(a[0], a[1], a[2:])
