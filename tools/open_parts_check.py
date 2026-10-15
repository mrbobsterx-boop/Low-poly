"""Проверка открывающихся моделей: в закрытом виде export/parts/<имя>.glb должен выглядеть как export/<имя>_idle.glb.

    python3 tools/open_parts_check.py [имя …] [--out папка]

Обе модели рисуются с 6 сторон одной камерой и одним светом; разница по пикселям показывает лишние вырезы (дыры
в корпусе, «оторванный» перед), сдвинутые детали, пропавшие куски. Печатает оценку каждой модели (доля пикселей,
заметно отличающихся) и сохраняет картинки: оригинал / из частей / разница (красным).
"""
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PX = 220
VIEWS = [("front", 0, 10), ("back", 180, 10), ("left", 90, 10), ("right", -90, 10), ("34a", -40, 30), ("34b", 140, 30)]


def scene_setup():
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 6
    sc.cycles.use_denoising = False
    sc.render.resolution_x = sc.render.resolution_y = PX
    sc.render.film_transparent = True
    sc.view_settings.view_transform = "Standard"
    sc.world = bpy.data.worlds.new("w")
    sc.world.color = (0.6, 0.6, 0.6)
    sun = bpy.data.lights.new("s", "SUN")
    sun.energy = 2.5
    so = bpy.data.objects.new("s", sun)
    so.rotation_euler = (0.6, 0.2, 0.8)
    sc.collection.objects.link(so)
    cam_d = bpy.data.cameras.new("c")
    cam_d.type = "ORTHO"
    cam = bpy.data.objects.new("c", cam_d)
    sc.collection.objects.link(cam)
    sc.camera = cam
    return cam


def load(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    for o in list(bpy.context.scene.objects):
        if o.type not in ("MESH",) and not o.children:
            bpy.data.objects.remove(o)
    return scene_setup()


def shots(cam, lo, hi, tag, out):
    c = (lo + hi) / 2
    size = float(max(hi - lo))
    imgs = []
    for name, yaw, pitch in VIEWS:
        d = Vector((math.sin(math.radians(yaw)) * math.cos(math.radians(pitch)),
                    -math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)), math.sin(math.radians(pitch))))
        cam.location = Vector(c) + d * size * 4
        cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        cam.data.ortho_scale = size * 1.15
        cam.data.clip_end = size * 20
        f = os.path.join(out, f"{tag}_{name}.png")
        bpy.context.scene.render.filepath = f
        bpy.ops.render.render(write_still=True)
        imgs.append(f)
    return imgs


def bounds():
    co = [o.matrix_world @ Vector(v) for o in bpy.context.scene.objects if o.type == "MESH" for v in o.bound_box]
    return np.min(co, 0), np.max(co, 0)


def check(name, out):
    from PIL import Image
    cam = load(os.path.join(ROOT, "export", f"{name}_idle.glb"))
    lo, hi = bounds()
    a = shots(cam, lo, hi, f"{name}_A", out)
    cam = load(os.path.join(ROOT, "export", "parts", f"{name}.glb"))
    b = shots(cam, lo, hi, f"{name}_B", out)
    scores, tiles = [], []
    for fa, fb in zip(a, b):
        ia = np.asarray(Image.open(fa).convert("RGBA")).astype(float)
        ib = np.asarray(Image.open(fb).convert("RGBA")).astype(float)
        obj = (ia[..., 3] > 10) | (ib[..., 3] > 10)
        diff = np.abs(ia[..., :3] - ib[..., :3]).max(-1) / 255 + np.abs(ia[..., 3] - ib[..., 3]) / 255
        bad = (diff > 0.25) & obj
        scores.append(bad.sum() / max(obj.sum(), 1))
        heat = np.zeros_like(ia[..., :3])
        heat[..., 0] = np.clip(diff * 2, 0, 1) * 255 * obj
        tiles.append([Image.open(fa).convert("RGB"), Image.open(fb).convert("RGB"), Image.fromarray(heat.astype(np.uint8))])
    W = Image.new("RGB", (PX * len(VIEWS), PX * 3), (30, 30, 30))
    for i, t in enumerate(tiles):
        for k, im in enumerate(t):
            W.paste(im, (i * PX, k * PX))
    W.save(os.path.join(out, f"{name}_check.png"))
    for f in a + b:
        os.remove(f)
    return scores


def main(argv):
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(ROOT, "renders", "_tmp_check")
    os.makedirs(out, exist_ok=True)
    names = [x for x in argv if not x.startswith("--") and x != out]
    for n in names:
        s = check(n, out)
        print(f"CHK {n} max {max(s):.3f} " + " ".join(f"{v:.3f}" for v in s), flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
